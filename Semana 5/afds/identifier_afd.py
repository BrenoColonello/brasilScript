from .token_types import IDENTIFICADOR, IDENTIFICADOR_INVALIDO


def accepts_identificador(s: str):
    """Return IDENTIFICADOR if s matches identifier pattern, else None."""
    if not s:
        return None
    first = s[0]
    if not (first.isalpha() or first == '_'):
        return None
    for c in s[1:]:
        if not (c.isalnum() or c == '_'):
            return None
    return IDENTIFICADOR


def accepts_identificador_invalido(s: str):
    """Return IDENTIFICADOR_INVALIDO if s starts with digit and rest valid, else None."""
    if not s:
        return None
    if not s[0].isdigit():
        return None
    for c in s[1:]:
        if not (c.isalnum() or c == '_'):
            return None
    return IDENTIFICADOR_INVALIDO
