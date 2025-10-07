"""DFA-based lexer that uses per-token AFD acceptors in `afds/`.

This lexer implements a simple longest-match algorithm that tries all
prefixes and uses the priority order from the regex-based lexer to
break ties. It's intentionally simple and educational.
"""
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Optional

from lexer import Token as RegexToken
from afds import (
    accepts_newline,
    accepts_comment,
    accepts_whitespace,
    accepts_identificador_invalido,
    accepts_numero_literal,
    accepts_string_literal,
    accepts_logico_literal,
    accepts_kw,
    accepts_op_relacional_multi,
    accepts_op_aritmetico,
    accepts_op_relacional_single,
    accepts_delimiter,
    accepts_identificador,
)


@dataclass
class Token:
    tipo: str
    valor: str

    def __repr__(self) -> str:
        return f"Token({self.tipo!r}, {self.valor!r})"


# Priority-ordered list of token checkers matching `lexer.py` token_specification
# Each entry: (name, checker_function)
PRIORITY_CHECKERS: List[Tuple[str, callable]] = [
    ("NEWLINE", accepts_newline),
    ("COMMENT", accepts_comment),
    ("WHITESPACE", accepts_whitespace),
    ("NUMERO_LITERAL", accepts_numero_literal),
    ("IDENTIFICADOR_INVALIDO", accepts_identificador_invalido),
    ("STRING_LITERAL", accepts_string_literal),
    ("LOGICO_LITERAL", accepts_logico_literal),
    ("KW", accepts_kw),
    ("OP_RELACIONAL_MULTI", accepts_op_relacional_multi),
    ("OP_ARITMETICO", accepts_op_aritmetico),
    ("OP_RELACIONAL_SINGLE", accepts_op_relacional_single),
    # Delimiters and single-char tokens handled by accepts_delimiter
    ("DELIMITER", accepts_delimiter),
    ("IDENTIFICADOR", accepts_identificador),
]


class LexerDFA:
    """Simple lexer that uses AFD acceptor functions to tokenize input.

    Notes:
    - Uses longest-match (maximal munch). If multiple token types match the
      same longest lexeme, the priority order above is used to break ties.
    - Tokens WHITESPACE, COMMENT and NEWLINE are skipped to mirror `lexer.py`.
    """

    def __init__(self, source: str):
        self.source = source
        self.n = len(source)

    def tokenize(self) -> Iterator[Token]:
        pos = 0
        s = self.source
        while pos < self.n:
            best_end: Optional[int] = None
            # Track any matching end positions
            for end in range(pos + 1, self.n + 1):
                substr = s[pos:end]
                matched = False
                # Try any checker to see if substring is a full token
                for _, checker in PRIORITY_CHECKERS:
                    try:
                        res = checker(substr)
                    except Exception:
                        res = None
                    if res is not None:
                        matched = True
                        break
                if matched:
                    best_end = end

            if best_end is None:
                # No token matched at this position -> lexical error similar to MISMATCH
                raise ValueError(f"Caractere inválido na posição {pos}: {s[pos]!r}")

            lexeme = s[pos:best_end]

            # For the chosen longest lexeme, pick the highest-priority token
            chosen_type = None
            chosen_value = lexeme
            for name, checker in PRIORITY_CHECKERS:
                try:
                    res = checker(lexeme)
                except Exception:
                    res = None
                if res is not None:
                    # Normalize to the same token names used by lexer.py
                    if res == "PALAVRA_CHAVE":
                        chosen_type = "PALAVRA_CHAVE"
                    elif res in ("LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "COMMA", "SEMICOLON", "COLON", "DOT"):
                        chosen_type = res
                    elif res == "IDENTIFICADOR_INVALIDO":
                        chosen_type = "IDENTIFICADOR_INVALIDO"
                    elif res == "IDENTIFICADOR":
                        chosen_type = "IDENTIFICADOR"
                    elif res == "NUMERO_LITERAL":
                        chosen_type = "NUMERO_LITERAL"
                    elif res == "STRING_LITERAL":
                        chosen_type = "STRING_LITERAL"
                    elif res == "LOGICO_LITERAL":
                        chosen_type = "LOGICO_LITERAL"
                    elif res == "COMMENT":
                        chosen_type = "COMMENT"
                    elif res == "WHITESPACE":
                        chosen_type = "WHITESPACE"
                    elif res == "NEWLINE":
                        chosen_type = "NEWLINE"
                    elif res == "OP":
                        chosen_type = "OP"
                    else:
                        # accepts_kw returns PALAVRA_CHAVE, accepts_delimiter returns specific token names
                        chosen_type = res
                    break

            if chosen_type is None:
                # Shouldn't happen, but guard
                raise ValueError(f"Token não reconhecido: {lexeme!r}")

            # skip ignored tokens
            if chosen_type in ("WHITESPACE", "COMMENT", "NEWLINE"):
                pos = best_end
                continue

            yield Token(chosen_type, chosen_value)
            pos = best_end


def dfa_tokens(source: str) -> List[Tuple[str, str]]:
    return [(t.tipo, t.valor) for t in LexerDFA(source).tokenize()]


if __name__ == "__main__":
    import sys
    text = sys.stdin.read() if not sys.argv[1:] else open(sys.argv[1]).read()
    for t in LexerDFA(text).tokenize():
        print(t)
