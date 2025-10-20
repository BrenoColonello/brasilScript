
"""Lexer Semana 6 usando um AFN global convertido para AFD.
Lê arquivos da pasta exemplos e tokeniza usando o AFD gerado a partir do AFN.
"""
import os
import sys
from typing import List, Tuple
from nfas import make_basic_nfa_for_identifier, make_basic_nfa_for_number, make_basic_nfa_for_operators, combine_nfas
from afn_to_afd import nfa_to_dfa
from dataclasses import dataclass
from collections import deque
import itertools
from typing import Optional, Iterator

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





@dataclass
class Token:
    type: str
    lexeme: str
    pos: int
    line: int = 0
    col: int = 0
    value: object = None


class Lexer:
    """Buffered lexer using the AFD produced from the AFN global.

    - Implements maximal-munch (longest match) using the AFD table.
    - Provides next_token() and peek() with simple buffering.
    """

    def __init__(self, dfa: dict, text: str):
        self.dfa = dfa
        self.text = text
        self.pos = 0
        self.N = len(text)
        self.buffer = deque()
        # position tracking
        self.line = 1
        self.col = 1
        # tokens the lexer will skip by default (parser usually doesn't need them)
        self.skip_types = {"WHITESPACE", "COMMENT"}

    def _scan_one(self) -> Optional[Token]:
        if self.pos >= self.N:
            return None
        delta = self.dfa["delta"]
        accepts = self.dfa["accepts"]
        start = self.dfa["start"]
        cur_state = start
        last_accept_pos = -1
        last_accept_tok = None
        i = self.pos
        # temporary line/col for scanning ahead (do not modify self.line/self.col until commit)
        tline = self.line
        tcol = self.col
        last_accept_line = tline
        last_accept_col = tcol
        while i < self.N:
            c = self.text[i]
            cur_state = delta.get(cur_state, {}).get(c)
            if cur_state is None:
                break
            if cur_state in accepts:
                last_accept_pos = i
                last_accept_tok = accepts[cur_state]
                last_accept_line = tline
                last_accept_col = tcol
            i += 1
            # update temp line/col as we consumed c
            if c == "\n":
                tline += 1
                tcol = 1
            else:
                tcol += 1

        if last_accept_pos < 0:
            # single-character mismatch
            ch = self.text[self.pos]
            tok = Token("MISMATCH", ch, self.pos, self.line, self.col)
            # advance position by one and update line/col
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
            return tok

        lexeme = self.text[self.pos:last_accept_pos+1]
        tok = Token(last_accept_tok, lexeme, self.pos, last_accept_line, last_accept_col)

        # set token.value for useful token types
        if last_accept_tok == "NUMERO_LITERAL":
            # try int then float
            s = lexeme
            try:
                if ("." in s) or ("e" in s) or ("E" in s):
                    tok.value = float(s)
                else:
                    tok.value = int(s)
            except Exception:
                tok.value = s
        elif last_accept_tok == "STRING_LITERAL":
            # strip surrounding quotes and unescape simple escapes
            if len(lexeme) >= 2 and lexeme[0] == lexeme[-1] and lexeme[0] in ('"', "'"):
                inner = lexeme[1:-1]
                inner = inner.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                tok.value = inner
            else:
                tok.value = lexeme
        elif last_accept_tok == "COMMENT":
            # store comment without leading '#'
            tok.value = lexeme[1:]

        # advance self.pos and update line/col to the end of the lexeme
        # use tline/tcol which reflect position after i advanced
        # compute end line/col by replaying characters from current pos to last_accept_pos
        e_line = self.line
        e_col = self.col
        for ch in self.text[self.pos:last_accept_pos+1]:
            if ch == '\n':
                e_line += 1
                e_col = 1
            else:
                e_col += 1
        self.line = e_line
        self.col = e_col
        self.pos = last_accept_pos + 1
        return tok

    def next_token(self) -> Optional[Token]:
        if self.buffer:
            return self.buffer.popleft()
        while True:
            tok = self._scan_one()
            if tok is None:
                return None
            if tok.type in self.skip_types:
                # skip and continue to next
                continue
            return tok

    def peek(self, k=1) -> List[Optional[Token]]:
        # ensure buffer has k tokens
        while len(self.buffer) < k:
            t = self._scan_one()
            if t is None:
                self.buffer.append(None)
                break
            # if the token is skippable, push it but mark for skipping on consumption
            self.buffer.append(t)
        # return exactly k items (pad with None if needed)
        res = []
        for i in range(k):
            res.append(self.buffer[i] if i < len(self.buffer) else None)
        return res


def simple_parser(lexer: Lexer) -> None:
    """Pequena função demonstrativa de integração com o analisador sintático.

    Apenas consome tokens e imprime uma estrutura simples (exemplo).
    """
    print(">>> Parser: iniciando consumo de tokens")
    while True:
        t = lexer.next_token()
        if t is None:
            break
        print(f"NODE: {t.type} -> {t.lexeme!r} @ {t.pos}")
    print(">>> Parser: fim")


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
