def accepts_op_relacional_multi(s: str) -> bool:
    return s in ("!=", "<=", ">=")


def accepts_op_relacional_single(s: str) -> bool:
    return s in ("=", "<", ">")


def accepts_op_aritmetico(s: str) -> bool:
    return len(s) == 1 and s in "+-*/%"
