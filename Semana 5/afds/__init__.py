# AFD implementations for BrasilScript lexer
from .number_afd import accepts_numero_literal
from .string_afd import accepts_string_literal
from .identifier_afd import accepts_identificador, accepts_identificador_invalido
from .logical_afd import accepts_logico_literal
from .comment_afd import accepts_comment
from .whitespace_afd import accepts_whitespace
from .operators_afd import (
    accepts_op_relacional_multi,
    accepts_op_relacional_single,
    accepts_op_aritmetico,
)
from .newline_afd import accepts_newline
from .keywords_afd import accepts_kw
from .delimiters_afd import accepts_delimiter

__all__ = [
    "accepts_numero_literal",
    "accepts_string_literal",
    "accepts_identificador",
    "accepts_identificador_invalido",
    "accepts_logico_literal",
    "accepts_comment",
    "accepts_whitespace",
    "accepts_op_relacional_multi",
    "accepts_op_relacional_single",
    "accepts_op_aritmetico",
    "accepts_newline",
    "accepts_kw",
    "accepts_delimiter",
]
