def accepts_whitespace(s: str) -> bool:
    """AFD for whitespace: [ \t]+  (one or more spaces or tabs)"""
    if not s:
        return False
    for c in s:
        if c not in (' ', '\t'):
            return False
    return True
