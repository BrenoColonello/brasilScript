from .token_types import STRING_LITERAL


def accepts_string_literal(s: str):
    """Return STRING_LITERAL if s is a quoted string literal, else None."""
    if len(s) < 2:
        return None
    quote = s[0]
    if quote not in ('"', "'"):
        return None
    if s[-1] != quote:
        return None
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
            return None
        i += 1
    # last char matched quote
    return STRING_LITERAL
