def accepts_comment(s: str) -> bool:
    """AFD for comment: #[^\r\n]*  (starts with #, no CR/LF inside)"""
    if not s:
        return False
    if s[0] != '#':
        return False
    for c in s[1:]:
        if c == '\r' or c == '\n':
            return False
    return True
