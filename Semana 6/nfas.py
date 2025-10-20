def make_nfa_for_whitespace(token_name="WHITESPACE"):
    s0 = fresh_state("ws"); s1 = fresh_state("ws")
    delta = {s0: {}, s1: {}}
    for c in " \t":
        delta[s0].setdefault(c, set()).add(s1)
        delta[s1].setdefault(c, set()).add(s1)
    return {"states": {s0, s1}, "alphabet": set(" \t"), "delta": delta, "start": s0, "accepts": {s1: token_name}}

def make_nfa_for_newline(token_name="NEWLINE"):
    s0 = fresh_state("nl"); s1 = fresh_state("nl")
    delta = {s0: {}, s1: {}}
    delta[s0]['\n'] = {s1}
    delta[s0]['\r'] = {s1}
    return {"states": {s0, s1}, "alphabet": set("\r\n"), "delta": delta, "start": s0, "accepts": {s1: token_name}}

def make_nfa_for_comment(token_name="COMMENT"):
    s0 = fresh_state("cmt"); s1 = fresh_state("cmt")
    delta = {s0: {}, s1: {}}
    delta[s0]['#'] = {s1}
    for c in (chr(i) for i in range(32, 127)):
        if c not in ('\n', '\r'):
            delta[s1].setdefault(c, set()).add(s1)
    return {"states": {s0, s1}, "alphabet": set(chr(i) for i in range(32, 127)), "delta": delta, "start": s0, "accepts": {s1: token_name}}

def make_nfa_for_keywords(token_name="PALAVRA_CHAVE"):
    keywords = [
        "declarar", "como", "mostrar", "perguntar", "guardar_em", "se", "entao", "senao", "senao_se", "fim_se",
        "repetir", "vezes", "enquanto", "faca", "fim_enquanto", "fim_repetir", "funcao", "fim_funcao", "retornar",
        "para_cada", "em", "fim_para_cada", "parar", "e", "ou", "nao", "lista", "texto", "numero", "logico"
    ]
    nfas = []
    for kw in keywords:
        states = []
        for i in range(len(kw)+1):
            states.append(fresh_state(f"kw{i}"))
        delta = {s: {} for s in states}
        for i, c in enumerate(kw):
            delta[states[i]].setdefault(c, set()).add(states[i+1])
        nfas.append({"states": set(states), "alphabet": set(kw), "delta": delta, "start": states[0], "accepts": {states[-1]: token_name}})
    return combine_nfas(nfas)

def make_nfa_for_logico(token_name="LOGICO_LITERAL"):
    nfas = []
    for word in ["verdadeiro", "falso"]:
        states = []
        for i in range(len(word)+1):
            states.append(fresh_state(f"log{i}"))
        delta = {s: {} for s in states}
        for i, c in enumerate(word):
            delta[states[i]].setdefault(c, set()).add(states[i+1])
        nfas.append({"states": set(states), "alphabet": set(word), "delta": delta, "start": states[0], "accepts": {states[-1]: token_name}})
    return combine_nfas(nfas)

def make_nfa_for_delimiters():
    chars = [
        ("(", "LPAREN"), (")", "RPAREN"), ("[", "LBRACKET"), ("]", "RBRACKET"),
        ("{", "LBRACE"), ("}", "RBRACE"), (",", "COMMA"), (";", "SEMICOLON"),
        (":", "COLON"), (".", "DOT")
    ]
    nfas = []
    for ch, token in chars:
        s0 = fresh_state(f"dlm{ch}"); s1 = fresh_state(f"dlm{ch}")
        delta = {s0: {}, s1: {}}
        delta[s0][ch] = {s1}
        nfas.append({"states": {s0, s1}, "alphabet": set(ch), "delta": delta, "start": s0, "accepts": {s1: token}})
    return combine_nfas(nfas)
def make_basic_nfa_for_string(token_name="STRING_LITERAL"):
    # Aspas duplas
    s0 = fresh_state("str")
    s1 = fresh_state("str")
    s2 = fresh_state("str")
    states = {s0, s1, s2}
    alphabet = set(chr(i) for i in range(32, 127))
    delta = {s0: {}, s1: {}, s2: {}}
    delta[s0]['"'] = {s1}
    for c in alphabet:
        if c not in ('"', '\\'):
            delta[s1].setdefault(c, set()).add(s1)
    delta[s1]['\\'] = {s2}
    for c in alphabet:
        delta[s2].setdefault(c, set()).add(s1)
    delta[s1]['"'] = {s0}
    # Aspas simples
    s3 = fresh_state("str")
    s4 = fresh_state("str")
    s5 = fresh_state("str")
    states.update([s3, s4, s5])
    delta[s3] = {}; delta[s4] = {}; delta[s5] = {}
    delta[s3]["'"] = {s4}
    for c in alphabet:
        if c not in ("'", "\\"):
            delta[s4].setdefault(c, set()).add(s4)
    delta[s4]["\\"] = {s5}
    for c in alphabet:
        delta[s5].setdefault(c, set()).add(s4)
    delta[s4]["'"] = {s3}
    accepts = {s0: token_name, s3: token_name}
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": accepts}
"""NFA builders for Semana 6 local folder (adapted from src)."""
from typing import Dict, Set, Any


def fresh_state(prefix="q"):
    fresh_state.counter += 1
    return f"{prefix}{fresh_state.counter}"


fresh_state.counter = 0


def make_basic_nfa_for_identifier(token_name="IDENTIFICADOR"):
    s0 = fresh_state()
    s1 = fresh_state()
    states = {s0, s1}
    alphabet = set(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"))
    delta = {s0: {}, s1: {}}
    for ch in alphabet:
        if ch.isalpha() or ch == '_':
            delta[s0].setdefault(ch, set()).add(s1)
            delta[s1].setdefault(ch, set()).add(s1)
        else:
            delta[s1].setdefault(ch, set()).add(s1)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name}}


def make_basic_nfa_for_number(token_name="NUMERO_LITERAL"):
    s0 = fresh_state()
    s1 = fresh_state()
    s2 = fresh_state()
    states = {s0, s1, s2}
    alphabet = set(list("0123456789."))
    delta = {s0: {}, s1: {}, s2: {}}
    for d in "0123456789":
        delta[s0].setdefault(d, set()).add(s1)
        delta[s1].setdefault(d, set()).add(s1)
        delta[s2].setdefault(d, set()).add(s2)
    delta[s1].setdefault('.', set()).add(s2)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name, s2: token_name}}


def combine_nfas(nfas):
    """
    Combina vários NFAs (um para cada token) em um AFN global.
    - Cria um novo estado inicial (start_global).
    - Para cada NFA de token, adiciona uma transição epsilon (None) do start_global para o estado inicial daquele NFA.
    - Isso significa que, ao iniciar a análise, o AFN pode, sem consumir nenhum caractere, escolher qualquer token para tentar reconhecer.
    - O algoritmo de subset construction (em afn_to_afd.py) irá calcular o epsilon-closure desse novo estado inicial, incluindo todos os estados iniciais dos NFAs de token.
    - Assim, o AFN global está pronto para ser convertido em um AFD único que reconhece todos os tokens.
    """
    states = set()
    alphabet = set()
    delta = {}
    # Novo estado inicial global do AFN
    start = fresh_state("start")
    accepts = {}
    # Adiciona transições epsilon (None) do novo estado inicial para cada NFA/token
    delta[start] = {None: set()}
    for nfa in nfas:
        states.update(nfa["states"]) 
        alphabet.update(nfa["alphabet"]) 
        for s, trans in nfa["delta"].items():
            delta.setdefault(s, {})
            for a, tgt in trans.items():
                delta[s].setdefault(a, set()).update(tgt)
        # Adiciona transição epsilon do novo estado inicial para o início de cada NFA
        # Isso permite que o AFN global tente reconhecer qualquer token a partir do início
        delta[start][None].add(nfa["start"])
        accepts.update(nfa.get("accepts", {}))
    states.add(start)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": start, "accepts": accepts}


def make_basic_nfa_for_operators(token_name="OP"):
    ops = list("+-*/%=!<>:,;().{}[]")
    s0 = fresh_state()
    s1 = fresh_state()
    states = {s0, s1}
    alphabet = set(ops)
    delta = {s0: {}, s1: {}}
    for ch in alphabet:
        delta[s0].setdefault(ch, set()).add(s1)
    return {"states": states, "alphabet": alphabet, "delta": delta, "start": s0, "accepts": {s1: token_name}}
