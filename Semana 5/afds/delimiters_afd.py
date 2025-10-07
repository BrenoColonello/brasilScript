from .token_types import (
    LPAREN,
    RPAREN,
    LBRACKET,
    RBRACKET,
    LBRACE,
    RBRACE,
    COMMA,
    SEMICOLON,
    COLON,
    DOT,
)


def accepts_delimiter(s: str):
    """Return the specific delimiter token type for single-char delimiters, else None."""
    if len(s) != 1:
        return None
    ch = s
    return {
        '(': LPAREN,
        ')': RPAREN,
        '[': LBRACKET,
        ']': RBRACKET,
        '{': LBRACE,
        '}': RBRACE,
        ',': COMMA,
        ';': SEMICOLON,
        ':': COLON,
        '.': DOT,
    }.get(ch)
