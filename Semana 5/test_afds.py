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
)


def test_numero_literal():
    assert accepts_numero_literal("0")
    assert accepts_numero_literal("123")
    assert accepts_numero_literal("3.14")
    assert accepts_numero_literal("10e5")
    assert accepts_numero_literal("1E-10")
    assert not accepts_numero_literal(".")
    assert not accepts_numero_literal("1.")
    assert not accepts_numero_literal("e10")


def test_string_literal():
    assert accepts_string_literal('"hello"')
    assert accepts_string_literal("'o\\'la'")
    assert accepts_string_literal('"a\\nb"')
    assert not accepts_string_literal('"unterminated')
    assert not accepts_string_literal('noquotes')


def test_identifiers():
    assert accepts_identificador("_abc123")
    assert accepts_identificador("var")
    assert not accepts_identificador("1abc")
    assert accepts_identificador_invalido("1abc")
    assert not accepts_identificador_invalido("a1")


def test_logico_comment_whitespace_and_ops():
    assert accepts_logico_literal("verdadeiro")
    assert accepts_logico_literal("falso")
    assert not accepts_logico_literal("verdadeira")

    assert accepts_comment("# isso eh um comentario")
    assert not accepts_comment("#linha\noutra")

    assert accepts_whitespace("   \t \t")
    assert not accepts_whitespace(" \n ")

    assert accepts_op_relacional_multi("!=")
    assert accepts_op_relacional_multi("<=")
    assert accepts_op_relacional_single("=")
    assert accepts_op_aritmetico("+")


if __name__ == "__main__":
    test_numero_literal()
    test_string_literal()
    test_identifiers()
    test_logico_comment_whitespace_and_ops()
    print("AFD tests passed")
