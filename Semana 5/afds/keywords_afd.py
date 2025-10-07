KEYWORDS = {
    "declarar",
    "como",
    "mostrar",
    "perguntar",
    "guardar_em",
    "se",
    "entao",
    "senao",
    "senao_se",
    "fim_se",
    "repetir",
    "vezes",
    "enquanto",
    "faca",
    "fim_enquanto",
    "fim_repetir",
    "funcao",
    "fim_funcao",
    "retornar",
    "para_cada",
    "em",
    "fim_para_cada",
    "parar",
    "e",
    "ou",
    "nao",
    "lista",
    "texto",
    "numero",
    "logico",
}


def accepts_kw(s: str) -> bool:
    """Return PALAVRA_CHAVE if s is in the keywords set, else None."""
    from .token_types import PALAVRA_CHAVE
    return PALAVRA_CHAVE if s in KEYWORDS else None
