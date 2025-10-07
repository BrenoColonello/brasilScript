from .token_types import COMMENT


def accepts_comment(s: str):
    """Return COMMENT if s is a comment starting with # and no newline, else None."""
    if not s:
        return None
    if s[0] != '#':
        return None
    for c in s[1:]:
        if c == '\r' or c == '\n':
            return None
    return COMMENT
