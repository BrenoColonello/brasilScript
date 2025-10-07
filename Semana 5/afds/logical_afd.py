from .token_types import LOGICO_LITERAL


def accepts_logico_literal(s: str):
    return LOGICO_LITERAL if s == "verdadeiro" or s == "falso" else None
