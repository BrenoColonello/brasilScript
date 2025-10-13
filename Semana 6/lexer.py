
"""Lexer Semana 6 usando um AFN global convertido para AFD.
Lê arquivos da pasta exemplos e tokeniza usando o AFD gerado a partir do AFN.
"""
import os
import sys
from typing import List, Tuple
from nfas import make_basic_nfa_for_identifier, make_basic_nfa_for_number, make_basic_nfa_for_operators, combine_nfas
from afn_to_afd import nfa_to_dfa

# Prioridade dos tokens (ordem para resolver conflitos)
TOKEN_PRIORITY = [
    "NEWLINE", "COMMENT", "WHITESPACE", "NUMERO_LITERAL", "IDENTIFICADOR_INVALIDO", "STRING_LITERAL", "LOGICO_LITERAL", "PALAVRA_CHAVE", "IDENTIFICADOR", "OP", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "COMMA", "SEMICOLON", "COLON", "DOT"
]

def build_afn_global():
    """
    Monta o AFN global combinando todos os NFAs de tokens via transições epsilon.
    O novo estado inicial do AFN global tem transições epsilon para o início de cada NFA de token.
    """
    from nfas import (
        make_basic_nfa_for_number, make_basic_nfa_for_identifier, make_basic_nfa_for_operators, make_basic_nfa_for_string,
        make_nfa_for_whitespace, make_nfa_for_newline, make_nfa_for_comment, make_nfa_for_keywords, make_nfa_for_logico, make_nfa_for_delimiters
    )
    nfas = [
        make_nfa_for_newline("NEWLINE"),
        make_nfa_for_comment("COMMENT"),
        make_nfa_for_whitespace("WHITESPACE"),
        make_basic_nfa_for_number("NUMERO_LITERAL"),
        make_basic_nfa_for_identifier("IDENTIFICADOR"),
        make_basic_nfa_for_operators("OP"),
        make_basic_nfa_for_string("STRING_LITERAL"),
        make_nfa_for_logico("LOGICO_LITERAL"),
        make_nfa_for_keywords("PALAVRA_CHAVE"),
        make_nfa_for_delimiters(),
    ]
    return combine_nfas(nfas)

def build_afd():
    """
    Constrói o AFD único a partir do AFN global usando subset construction.
    """
    afn = build_afn_global()
    return nfa_to_dfa(afn, token_priority=TOKEN_PRIORITY)

def tokenize_with_afd(dfa, text: str) -> List[Tuple[str, str]]:
    """
    Tokeniza o texto usando o AFD gerado a partir do AFN global.
    - Para cada posição, simula o AFD (maximal munch):
      - Avança enquanto houver transição.
      - Guarda o último estado de aceitação encontrado.
      - Quando não houver mais transição, retorna o maior prefixo aceito.
      - Se não houver prefixo aceito, retorna MISMATCH.
    """
    pos = 0
    n = len(text)
    tokens: List[Tuple[str, str]] = []
    delta = dfa["delta"]
    accepts = dfa["accepts"]
    start = dfa["start"]
    while pos < n:
        cur_state = start
        last_accept_pos = -1
        last_accept_tok = None
        i = pos
        while i < n:
            c = text[i]
            cur_state = delta.get(cur_state, {}).get(c)
            if cur_state is None:
                break
            if cur_state in accepts:
                last_accept_pos = i
                last_accept_tok = accepts[cur_state]
            i += 1
        if last_accept_pos < 0:
            tokens.append(("MISMATCH", text[pos]))
            pos += 1
            continue
        lexeme = text[pos:last_accept_pos + 1]
        tokens.append((last_accept_tok, lexeme))
        pos = last_accept_pos + 1
    return tokens


def _exemplos_dir() -> str:
    # Semana 6 está em .../brasilScript/Semana 6
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(base_dir)
    return os.path.join(repo_dir, "exemplos")


def read_file_from_exemplos(filename: str) -> str:
    exemplos_dir = _exemplos_dir()
    path = os.path.join(exemplos_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_exemplos_files(ext: str = ".bs") -> List[str]:
    exemplos_dir = _exemplos_dir()
    if not os.path.isdir(exemplos_dir):
        return []
    return [name for name in os.listdir(exemplos_dir) if name.lower().endswith(ext)]


if __name__ == '__main__':
    dfa = build_afd()
    # Uso:
    #   python "Semana 6/lexer.py" hello_world.bs
    # ou sem argumento: tokeniza todos os .bs na pasta exemplos
    def _exemplos_dir() -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(base_dir)
        return os.path.join(repo_dir, "exemplos")

    def read_file_from_exemplos(filename: str) -> str:
        exemplos_dir = _exemplos_dir()
        path = os.path.join(exemplos_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def list_exemplos_files(ext: str = ".bs") -> List[str]:
        exemplos_dir = _exemplos_dir()
        if not os.path.isdir(exemplos_dir):
            return []
        return [name for name in os.listdir(exemplos_dir) if name.lower().endswith(ext)]

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            src = read_file_from_exemplos(filename)
        except FileNotFoundError:
            print(f"Arquivo não encontrado em exemplos: {filename}")
            sys.exit(1)
        tokens = tokenize_with_afd(dfa, src)
        for t, lex in tokens:
            print(f"{t}\t{lex}")
    else:
        files = list_exemplos_files(".bs")
        if not files:
            print("Nenhum arquivo .bs encontrado na pasta 'exemplos'.")
            sys.exit(0)
        for filename in files:
            print(f"\n==> Tokenizando {filename}")
            src = read_file_from_exemplos(filename)
            tokens = tokenize_with_afd(dfa, src)
            for t, lex in tokens:
                print(f"{t}\t{lex}")
