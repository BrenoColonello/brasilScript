def accepts_numero_literal(s: str) -> bool:
    """AFD for regex: \d+(?:\.\d+)?(?:[eE][+-]?\d+)?

    Accepts integers, decimals and scientific notation.
    """
    i = 0
    n = len(s)
    # At least one digit
    if i >= n or not s[i].isdigit():
        return False
    while i < n and s[i].isdigit():
        i += 1
    # optional fractional part
    if i < n and s[i] == '.':
        i += 1
        # must have at least one digit after dot
        if i >= n or not s[i].isdigit():
            return False
        while i < n and s[i].isdigit():
            i += 1
    # optional exponent
    if i < n and (s[i] == 'e' or s[i] == 'E'):
        i += 1
        if i < n and s[i] in ('+', '-'):
            i += 1
        # must have at least one digit in exponent
        if i >= n or not s[i].isdigit():
            return False
        while i < n and s[i].isdigit():
            i += 1
    # accept only if consumed all
    return i == n
