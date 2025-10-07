from .token_types import WHITESPACE


def accepts_whitespace(s: str):
    """Return WHITESPACE if s is one or more spaces/tabs, else None."""
    if not s:
        return None
    for c in s:
        if c not in (' ', '\t'):
            return None
    return WHITESPACE
