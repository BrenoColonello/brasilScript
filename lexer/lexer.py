"""Final DFA-based lexer using subset-construction output.

This module builds simple NFAs for identifiers, numbers and operators,
converts them to a single DFA using `afn_to_afd.nfa_to_dfa`, and exposes a
`tokenize` function that performs maximal-munch tokenization on input text.

Note: This is a compact, educational implementation that focuses on
readability over performance. It mirrors the Week 6 working code.
"""
from typing import Dict, Any, Tuple, List
from .afn_to_afd import nfa_to_dfa, epsilon_closure, move


# Token names used in the DFA accepts map
TOKENS = [
    "PALAVRA_CHAVE",
    "IDENTIFICADOR",
    "IDENTIFICADOR_INVALIDO",
    "NUMERO_LITERAL",
    "STRING_LITERAL",
    "LOGICO_LITERAL",
    "OP",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "SEMICOLON",
    "COLON",
    "DOT",
    "WHITESPACE",
    "COMMENT",
    "NEWLINE",
]



# Utilitário para gerar estados únicos
def _fresh(prefix="q"):
    _fresh.counter += 1
    return f"{prefix}{_fresh.counter}"
_fresh.counter = 0

def _make_nfa_identifier():
    s0 = _fresh("id")
    s1 = _fresh("id")
    delta = {s0: {}, s1: {}}
    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        delta[s0].setdefault(c, set()).add(s1)
        delta[s1].setdefault(c, set()).add(s1)
    for d in "0123456789":
        delta[s1].setdefault(d, set()).add(s1)
    accepts = {s1: "IDENTIFICADOR"}
    return {"start": s0, "delta": delta, "alphabet": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"), "accepts": accepts}

def _make_nfa_identifier_invalido():
    s0 = _fresh("inv")
    s1 = _fresh("inv")
    delta = {s0: {}, s1: {}}
    for d in "0123456789":
        delta[s0].setdefault(d, set()).add(s1)
        delta[s1].setdefault(d, set()).add(s1)
    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_":
        delta[s1].setdefault(c, set()).add(s1)
    accepts = {s1: "IDENTIFICADOR_INVALIDO"}
    return {"start": s0, "delta": delta, "alphabet": set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"), "accepts": accepts}

def _make_nfa_numero():
    # Aceita inteiros, decimais e notação científica
    s0 = _fresh("num")
    s1 = _fresh("num")
    s2 = _fresh("num")
    s3 = _fresh("num")
    s4 = _fresh("num")
    s5 = _fresh("num")
    delta = {s0: {}, s1: {}, s2: {}, s3: {}, s4: {}, s5: {}}
    for d in "0123456789":
        delta[s0].setdefault(d, set()).add(s1)
        delta[s1].setdefault(d, set()).add(s1)
        delta[s2].setdefault(d, set()).add(s3)
        delta[s3].setdefault(d, set()).add(s3)
        delta[s5].setdefault(d, set()).add(s5)
    delta[s1]["."] = {s2}
    delta[s1]["e"] = {s4}
    delta[s1]["E"] = {s4}
    delta[s3]["e"] = {s4}
    delta[s3]["E"] = {s4}
    delta[s4]["+"] = {s5}
    delta[s4]["-"] = {s5}
    for d in "0123456789":
        delta[s4].setdefault(d, set()).add(s5)
    accepts = {s1: "NUMERO_LITERAL", s3: "NUMERO_LITERAL", s5: "NUMERO_LITERAL"}
    alphabet = set("0123456789.eE+-")
    return {"start": s0, "delta": delta, "alphabet": alphabet, "accepts": accepts}

def _make_nfa_string():
    # Aspas duplas
    s0 = _fresh("str")
    s1 = _fresh("str")
    s2 = _fresh("str")
    delta = {s0: {}, s1: {}, s2: {}}
    delta[s0]['"'] = {s1}
    for c in (chr(i) for i in range(32, 127)):
        if c not in ('"', '\\'):
            delta[s1].setdefault(c, set()).add(s1)
    delta[s1]['\\'] = {s2}
    for c in (chr(i) for i in range(32, 127)):
        delta[s2].setdefault(c, set()).add(s1)
    delta[s1]['"'] = {s0}
    accepts = {s0: "STRING_LITERAL"}
    # Aspas simples (repete estrutura)
    s3 = _fresh("str")
    s4 = _fresh("str")
    s5 = _fresh("str")
    delta[s3] = {}; delta[s4] = {}; delta[s5] = {}
    delta[s3]["'"] = {s4}
    for c in (chr(i) for i in range(32, 127)):
        if c not in ("'", "\\"):
            delta[s4].setdefault(c, set()).add(s4)
    delta[s4]["\\"] = {s5}
    for c in (chr(i) for i in range(32, 127)):
        delta[s5].setdefault(c, set()).add(s4)
    delta[s4]["'"] = {s3}
    accepts[s3] = "STRING_LITERAL"
    alphabet = set(chr(i) for i in range(32, 127))
    return {"start": s0, "delta": delta, "alphabet": alphabet, "accepts": accepts}

def _make_nfa_logico():
    # Aceita 'verdadeiro' e 'falso'
    def word_nfa(word, token):
        states = []
        for i in range(len(word)+1):
            states.append(_fresh(f"log{i}"))
        delta = {s: {} for s in states}
        for i, c in enumerate(word):
            delta[states[i]].setdefault(c, set()).add(states[i+1])
        accepts = {states[-1]: token}
        return {"start": states[0], "delta": delta, "alphabet": set(word), "accepts": accepts}
    nfa1 = word_nfa("verdadeiro", "LOGICO_LITERAL")
    nfa2 = word_nfa("falso", "LOGICO_LITERAL")
    return _combine_nfas([nfa1, nfa2])

def _make_nfa_keywords():
    keywords = [
        "declarar", "como", "mostrar", "perguntar", "guardar_em", "se", "entao", "senao", "senao_se", "fim_se",
        "repetir", "vezes", "enquanto", "faca", "fim_enquanto", "fim_repetir", "funcao", "fim_funcao", "retornar",
        "para_cada", "em", "fim_para_cada", "parar", "e", "ou", "nao", "lista", "texto", "numero", "logico"
    ]
    def word_nfa(word, token):
        states = []
        for i in range(len(word)+1):
            states.append(_fresh(f"kw{i}"))
        delta = {s: {} for s in states}
        for i, c in enumerate(word):
            delta[states[i]].setdefault(c, set()).add(states[i+1])
        accepts = {states[-1]: token}
        return {"start": states[0], "delta": delta, "alphabet": set(word), "accepts": accepts}
    nfas = [word_nfa(kw, "PALAVRA_CHAVE") for kw in keywords]
    return _combine_nfas(nfas)

def _make_nfa_comment():
    s0 = _fresh("cmt")
    s1 = _fresh("cmt")
    delta = {s0: {}, s1: {}}
    delta[s0]['#'] = {s1}
    for c in (chr(i) for i in range(32, 127)):
        if c not in ('\n', '\r'):
            delta[s1].setdefault(c, set()).add(s1)
    accepts = {s1: "COMMENT"}
    return {"start": s0, "delta": delta, "alphabet": set(chr(i) for i in range(32, 127)), "accepts": accepts}

def _make_nfa_whitespace():
    s0 = _fresh("ws")
    s1 = _fresh("ws")
    delta = {s0: {}, s1: {}}
    for c in " \t":
        delta[s0].setdefault(c, set()).add(s1)
        delta[s1].setdefault(c, set()).add(s1)
    accepts = {s1: "WHITESPACE"}
    return {"start": s0, "delta": delta, "alphabet": set(" \t"), "accepts": accepts}

def _make_nfa_newline():
    s0 = _fresh("nl")
    s1 = _fresh("nl")
    s2 = _fresh("nl")
    delta = {s0: {}, s1: {}, s2: {}}
    delta[s0]['\n'] = {s1}
    delta[s0]['\r'] = {s2}
    delta[s2]['\n'] = {s1}
    accepts = {s1: "NEWLINE"}
    return {"start": s0, "delta": delta, "alphabet": set("\r\n"), "accepts": accepts}

def _make_nfa_delimiters():
    # Parênteses, colchetes, chaves, vírgula, ponto e vírgula, dois pontos, ponto
    chars = [
        ("(", "LPAREN"), (")", "RPAREN"), ("[", "LBRACKET"), ("]", "RBRACKET"),
        ("{", "LBRACE"), ("}", "RBRACE"), (",", "COMMA"), (";", "SEMICOLON"),
        (":", "COLON"), (".", "DOT")
    ]
    nfas = []
    for ch, token in chars:
        s0 = _fresh(f"dlm{ch}")
        s1 = _fresh(f"dlm{ch}")
        delta = {s0: {}, s1: {}}
        delta[s0][ch] = {s1}
        accepts = {s1: token}
        nfas.append({"start": s0, "delta": delta, "alphabet": set(ch), "accepts": accepts})
    return _combine_nfas(nfas)


def _make_basic_nfa_for_number(start_id=1000):
    s0 = f"n{start_id}"
    s1 = f"n{start_id+1}"
    delta = {s0: {}, s1: {}}
    for d in "0123456789":
        delta[s0].setdefault(d, set()).add(s1)
        delta[s1].setdefault(d, set()).add(s1)
    accepts = {s1: "NUMERO_LITERAL"}
    return {"start": s0, "delta": delta, "alphabet": set(list("0123456789")), "accepts": accepts}


def _make_basic_nfa_for_operators(start_id=2000):
    # Create single-char operator NFAs for simplicity
    ops = ["+", "-", "*", "/", "=", "==", "<=", ">=", "<", ">", "!", "!=", "&&", "||"]
    delta = {}
    start = f"op{start_id}"
    delta[start] = {}
    accepts = {}
    alphabet = set()
    for idx, op in enumerate(ops):
        cur = start
        for ch in op:
            nxt = f"op_{idx}_{ch}"
            delta.setdefault(cur, {}).setdefault(ch, set()).add(nxt)
            delta.setdefault(nxt, {})
            cur = nxt
            alphabet.add(ch)
        accepts[cur] = "OP"
    return {"start": start, "delta": delta, "alphabet": alphabet, "accepts": accepts}


def _combine_nfas(nfas: List[Dict]) -> Dict:
    base_start = "S_COMB"
    delta = {base_start: {None: set()}}
    alphabet = set()
    accepts = {}
    for nfa in nfas:
        # merge states
        for s, trans in nfa["delta"].items():
            if s in delta:
                # merge transitions
                for a, targets in trans.items():
                    delta[s].setdefault(a, set()).update(targets)
            else:
                delta[s] = {k: set(v) for k, v in trans.items()}
        # add epsilon from new start
        delta[base_start][None].add(nfa["start"])
        alphabet.update(nfa.get("alphabet", set()))
        accepts.update(nfa.get("accepts", {}))
    return {"start": base_start, "delta": delta, "alphabet": alphabet, "accepts": accepts}


def build_lexer_dfa() -> Dict[str, Any]:
    nfas = [
        _make_nfa_newline(),
        _make_nfa_comment(),
        _make_nfa_whitespace(),
        _make_nfa_numero(),
        _make_nfa_identifier_invalido(),
        _make_nfa_string(),
        _make_nfa_logico(),
        _make_nfa_keywords(),
        _make_nfa_identifier(),
        _make_basic_nfa_for_operators(),
        _make_nfa_delimiters(),
    ]
    # Prioridade igual ao regex lexer
    token_priority = [
        "NEWLINE", "COMMENT", "WHITESPACE", "NUMERO_LITERAL", "IDENTIFICADOR_INVALIDO", "STRING_LITERAL", "LOGICO_LITERAL", "PALAVRA_CHAVE", "IDENTIFICADOR", "OP", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "COMMA", "SEMICOLON", "COLON", "DOT"
    ]
    combined = _combine_nfas(nfas)
    dfa = nfa_to_dfa(combined, token_priority=token_priority)
    return dfa


def tokenize(dfa: Dict[str, Any], text: str):
    out = []
    pos = 0
    N = len(text)
    delta = dfa["delta"]
    accepts = dfa["accepts"]
    start = dfa["start"]

    while pos < N:
        cur_state = start
        last_accept_pos = -1
        last_accept_tok = None
        i = pos
        while i < N:
            c = text[i]
            cur_state = delta.get(cur_state, {}).get(c)
            if cur_state is None:
                break
            if cur_state in accepts:
                last_accept_pos = i
                last_accept_tok = accepts[cur_state]
            i += 1
        if last_accept_pos < 0:
            raise ValueError(f"Unexpected character at {pos}: {text[pos]!r}")
        lexeme = text[pos:last_accept_pos + 1]
        out.append((last_accept_tok, lexeme))
        pos = last_accept_pos + 1
    return out


# convenience: build and expose tokenizer
_default_dfa = build_lexer_dfa()

def tokenize_text(text: str):
    return tokenize(_default_dfa, text)
