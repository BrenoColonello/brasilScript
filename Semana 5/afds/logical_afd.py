def accepts_logico_literal(s: str) -> bool:
    """AFD for logical literals: \b(?:verdadeiro|falso)\b"""
    return s == "verdadeiro" or s == "falso"
