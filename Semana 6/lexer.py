
"""Lexer Semana 6 usando os AFDs da pasta Semana 5/afds para cada token.
Lê arquivos da pasta exemplos e tokeniza usando os AFDs reais, sem fallback manual.
"""
import os
import sys
from typing import List, Tuple

# Importar todos os AFDs da Semana 5
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Semana 5')))
from afds.token_types import *
from afds.keywords_afd import accepts_kw
from afds.string_afd import accepts_string_literal
from afds.comment_afd import accepts_comment
from afds.number_afd import accepts_numero_literal
from afds.identifier_afd import accepts_identificador, accepts_identificador_invalido
from afds.logical_afd import accepts_logico_literal
from afds.operators_afd import accepts_op_relacional_multi, accepts_op_relacional_single, accepts_op_aritmetico
from afds.delimiters_afd import accepts_delimiter
from afds.whitespace_afd import accepts_whitespace
from afds.newline_afd import accepts_newline

# Lista de (nome, função) em ordem de prioridade (maior para menor)
TOKEN_CHECKERS = [
    (NEWLINE, accepts_newline),
    (COMMENT, accepts_comment),
    (WHITESPACE, accepts_whitespace),
    (NUMERO_LITERAL, accepts_numero_literal),
    (IDENTIFICADOR_INVALIDO, accepts_identificador_invalido),
    (STRING_LITERAL, accepts_string_literal),
    (LOGICO_LITERAL, accepts_logico_literal),
    (PALAVRA_CHAVE, accepts_kw),
    (IDENTIFICADOR, accepts_identificador),
    (OP, accepts_op_relacional_multi),
    (OP, accepts_op_relacional_single),
    (OP, accepts_op_aritmetico),
    (LPAREN, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == LPAREN else None),
    (RPAREN, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == RPAREN else None),
    (LBRACKET, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == LBRACKET else None),
    (RBRACKET, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == RBRACKET else None),
    (LBRACE, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == LBRACE else None),
    (RBRACE, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == RBRACE else None),
    (COMMA, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == COMMA else None),
    (SEMICOLON, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == SEMICOLON else None),
    (COLON, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == COLON else None),
    (DOT, lambda s: accepts_delimiter(s) if accepts_delimiter(s) == DOT else None),
]

def tokenize_with_afds(text: str) -> List[Tuple[str, str]]:
    pos = 0
    n = len(text)
    tokens: List[Tuple[str, str]] = []
    while pos < n:
        # Ignorar whitespace entre tokens
        if text[pos] in (' ', '\t', '\r', '\n'):
            # whitespace e newline são tokens próprios
            for name, fn in [(WHITESPACE, accepts_whitespace), (NEWLINE, accepts_newline)]:
                for end in range(pos+1, n+1):
                    lex = text[pos:end]
                    if fn(lex) == name:
                        last_good = end
                    else:
                        break
                else:
                    last_good = n
                if last_good > pos:
                    tokens.append((name, text[pos:last_good]))
                    pos = last_good
                    break
            else:
                pos += 1
            continue

        # Tentar todos os AFDs, maior prefixo e maior prioridade
        best = None
        best_type = None
        best_len = 0
        for name, fn in TOKEN_CHECKERS:
            for end in range(pos+1, n+1):
                lex = text[pos:end]
                typ = fn(lex)
                if typ == name:
                    if end - pos > best_len:
                        best = lex
                        best_type = typ
                        best_len = end - pos
        if best:
            tokens.append((best_type, best))
            pos += best_len
        else:
            tokens.append(("MISMATCH", text[pos]))
            pos += 1
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
    # Uso:
    #   python "Semana 6/lexer.py" hello_world.bs
    # ou sem argumento: tokeniza todos os .bs na pasta exemplos
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            src = read_file_from_exemplos(filename)
        except FileNotFoundError:
            print(f"Arquivo não encontrado em exemplos: {filename}")
            sys.exit(1)
        tokens = tokenize_with_afds(src)
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
            tokens = tokenize_with_afds(src)
            for t, lex in tokens:
                print(f"{t}\t{lex}")
