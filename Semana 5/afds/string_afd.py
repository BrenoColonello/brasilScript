def accepts_string_literal(s: str) -> bool:
    """AFD for string literals: double- or single-quoted with escapes.

    Regex: "(?:[^"\\]|\\.)*"  and  '(?:[^'\\]|\\.)*'
    """
    if len(s) < 2:
        return False
    quote = s[0]
    if quote not in ('"', "'"):
        return False
    if s[-1] != quote:
        return False
    i = 1
    n = len(s)
    while i < n - 1:
        c = s[i]
        if c == '\\':
            # escape next char if present
            i += 2
            continue
        # disallow raw newline characters inside string
        if c == '\n' or c == '\r':
            return False
        i += 1
    # last char matched quote
    return True
