#!/usr/bin/env python3
"""Lexer for BrasilScript language.

This lexer follows the token specifications described in
`Semana 2/SintaxeDaLinguagem.md` and
`Semana 4/1_especificacao_expressoes_regulares.md`.

Usage:
    from semana5.lexer import Lexer
    tokens = list(Lexer(source).tokenize())
"""
from dataclasses import dataclass
import re
from typing import Iterator, List, Optional, Tuple


@dataclass
class Token:
    tipo: str
    valor: str

    def __repr__(self) -> str:  # friendly repr for tests/printing
        return f"Token({self.tipo!r}, {self.valor!r})"


class LexerError(Exception):
    pass


class Lexer:
    """Regex-based lexer for BrasilScript.

    Produces Token objects with attributes (tipo, valor).
    """

    # Order matters: longer/more specific patterns first
    token_specification: List[Tuple[str, str]] = [
        # Newlines (track lines explicitly)
        ("NEWLINE", r"\r\n|\n"),

        # Comments and horizontal whitespace
        ("COMMENT", r"#[^\r\n]*"),
        ("WHITESPACE", r"[ \t]+"),

        # Invalid identifiers (identifiers starting with digits) - must come
        # before numbers so the whole word is matched as one token
        ("IDENTIFICADOR_INVALIDO", r"\d[a-zA-Z0-9_]*"),

        # Numbers (integers, decimals, scientific)
        ("NUMERO_LITERAL", r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"),

        # Strings (double and single quoted)
        ("STRING_LITERAL", r'"(?:[^"\\]|\\.)*"'),
        ("STRING_LITERAL", r"'(?:[^'\\]|\\.)*'"),

        # Logical literals
        ("LOGICO_LITERAL", r"\b(?:verdadeiro|falso)\b"),

        # Keywords (word boundaries ensure whole-word match)
        ("KW", r"\b(?:declarar|como|mostrar|perguntar|guardar_em|se|entao|senao|senao_se|fim_se|repetir|vezes|enquanto|faca|fim_enquanto|fim_repetir|funcao|fim_funcao|retornar|para_cada|em|fim_para_cada|parar|e|ou|nao|lista|texto|numero|logico)\b"),

        # Multi-char operators first
        ("OP_RELACIONAL", r"!=|<=|>="),

        # Single-char operators and delimiters
        ("OP_ARITMETICO", r"[+\-*/%]"),
        ("OP_RELACIONAL", r"=|<|>"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACKET", r"\["),
        ("RBRACKET", r"\]"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("COMMA", r","),
        ("SEMICOLON", r";"),
        ("COLON", r":"),
        ("DOT", r"\."),

        # Identifiers (after keywords to avoid masking kw)
        ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),

        # Any other single character is an error
        ("MISMATCH", r".")
    ]

    def __init__(self, source: str):
        self.source = source
        # Build master regex
        parts = []
        for idx, (name, pattern) in enumerate(self.token_specification):
            parts.append(f"(?P<T{idx}>{pattern})")
        # Use DOTALL only indirectly -- we handle newlines explicitly above
        self.master_re = re.compile("|".join(parts))

    def tokenize(self) -> Iterator[Token]:
        # Iterate matches in source
        for mo in self.master_re.finditer(self.source):
            kind = None
            value = mo.group(0)
            # determine which named group matched
            groupdict = mo.groupdict()
            for idx, (name, _) in enumerate(self.token_specification):
                if groupdict.get(f"T{idx}") is not None:
                    kind = name
                    break

            if kind is None:
                # should not happen because MISMATCH covers others
                raise LexerError("Token desconhecido")

            if kind in ("WHITESPACE", "COMMENT", "NEWLINE"):
                # skip but continue (we still consume these parts)
                continue

            if kind == "MISMATCH":
                # unexpected single character
                raise LexerError(f"Caractere inválido: {value!r}")

            # For invalid identifiers, produce a token so parser can report error
            normalized_kind = kind
            if kind == "KW":
                normalized_kind = "PALAVRA_CHAVE"
            elif kind == "IDENTIFICADOR":
                normalized_kind = "IDENTIFICADOR"
            elif kind == "IDENTIFICADOR_INVALIDO":
                normalized_kind = "IDENTIFICADOR_INVALIDO"
            elif kind == "NUMERO_LITERAL":
                normalized_kind = "NUMERO_LITERAL"
            elif kind == "STRING_LITERAL":
                normalized_kind = "STRING_LITERAL"
            elif kind == "LOGICO_LITERAL":
                normalized_kind = "LOGICO_LITERAL"
            elif kind in ("OP_ARITMETICO", "OP_RELACIONAL"):
                normalized_kind = "OP"

            yield Token(normalized_kind, value)


if __name__ == "__main__":
    import sys
    text = sys.stdin.read() if not sys.argv[1:] else open(sys.argv[1]).read()
    lx = Lexer(text)
    try:
        for t in lx.tokenize():
            print(t)
    except LexerError as e:
        print(f"Erro léxico: {e}")
