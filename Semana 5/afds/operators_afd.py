from .token_types import OP


def accepts_op_relacional_multi(s: str):
    return OP if s in ("!=", "<=", ">=") else None


def accepts_op_relacional_single(s: str):
    return OP if s in ("=", "<", ">") else None


def accepts_op_aritmetico(s: str):
    return OP if len(s) == 1 and s in "+-*/%" else None
