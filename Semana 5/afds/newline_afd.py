from .token_types import NEWLINE


def accepts_newline(s: str):
    return NEWLINE if s == "\r\n" or s == "\n" else None
