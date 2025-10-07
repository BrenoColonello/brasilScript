"""Unit tests for AFD acceptors in Semana 5/afds."""
import os
import sys
here = os.path.dirname(__file__)
if here not in sys.path:
    sys.path.insert(0, here)

from afds import (
    accepts_numero_literal,
    accepts_string_literal,
    accepts_identificador,
    accepts_identificador_invalido,
    accepts_logico_literal,
    accepts_comment,
    accepts_whitespace,
    accepts_op_relacional_multi,
    accepts_op_relacional_single,
    accepts_op_aritmetico,
    accepts_newline,
    accepts_kw,
    accepts_delimiter,
)


def test_numero_literal():
    assert accepts_numero_literal("0") == "NUMERO_LITERAL"
    assert accepts_numero_literal("123") == "NUMERO_LITERAL"
    assert accepts_numero_literal("3.14") == "NUMERO_LITERAL"
    assert accepts_numero_literal("10e5") == "NUMERO_LITERAL"
    assert accepts_numero_literal("1E-10") == "NUMERO_LITERAL"
    assert accepts_numero_literal(".") is None
    assert accepts_numero_literal("1.") is None
    assert accepts_numero_literal("e10") is None


def test_string_literal():
    assert accepts_string_literal('"hello"') == "STRING_LITERAL"
    assert accepts_string_literal("'o\\'la'") == "STRING_LITERAL"
    assert accepts_string_literal('"a\\nb"') == "STRING_LITERAL"
    assert accepts_string_literal('"unterminated') is None
    assert accepts_string_literal('noquotes') is None


def test_identifiers():
    assert accepts_identificador("_abc123") == "IDENTIFICADOR"
    assert accepts_identificador("var") == "IDENTIFICADOR"
    assert accepts_identificador("1abc") is None
    assert accepts_identificador_invalido("1abc") == "IDENTIFICADOR_INVALIDO"
    assert accepts_identificador_invalido("a1") is None


def test_logico_comment_whitespace_and_ops():
    assert accepts_logico_literal("verdadeiro") == "LOGICO_LITERAL"
    assert accepts_logico_literal("falso") == "LOGICO_LITERAL"
    assert accepts_logico_literal("verdadeira") is None

    assert accepts_comment("# isso eh um comentario") == "COMMENT"
    assert accepts_comment("#linha\noutra") is None

    assert accepts_whitespace("   \t \t") == "WHITESPACE"
    assert accepts_whitespace(" \n ") is None

    assert accepts_op_relacional_multi("!=") == "OP"
    assert accepts_op_relacional_multi("<=") == "OP"
    assert accepts_op_relacional_single("=") == "OP"
    assert accepts_op_aritmetico("+") == "OP"


def test_newline_keywords_delimiters():
    assert accepts_newline("\n") == "NEWLINE"
    assert accepts_newline("\r\n") == "NEWLINE"

    assert accepts_kw("declarar") == "PALAVRA_CHAVE"
    assert accepts_kw("mostrar") == "PALAVRA_CHAVE"
    assert accepts_kw("declaracao") is None

    assert accepts_delimiter("(") == "LPAREN"
    assert accepts_delimiter(")") == "RPAREN"
    assert accepts_delimiter(",") == "COMMA"
    assert accepts_delimiter(".") == "DOT"


if __name__ == "__main__":
    test_numero_literal()
    test_string_literal()
    test_identifiers()
    test_logico_comment_whitespace_and_ops()
    print("AFD tests passed")
