def accepts_identificador(s: str) -> bool:
    """AFD for identifiers: [a-zA-Z_][a-zA-Z0-9_]*"""
    if not s:
        return False
    first = s[0]
    if not (first.isalpha() or first == '_'):
        return False
    for c in s[1:]:
        if not (c.isalnum() or c == '_'):
            return False
    return True


def accepts_identificador_invalido(s: str) -> bool:
    """AFD for identifiers starting with a digit: \d[a-zA-Z0-9_]*"""
    if not s:
        return False
    if not s[0].isdigit():
        return False
    for c in s[1:]:
        if not (c.isalnum() or c == '_'):
            return False
    return True
