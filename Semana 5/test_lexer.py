
"""Small smoke tests for Semana 5 lexer."""
import os
import sys

# Ensure the directory containing this test is on sys.path so we can import lexer.py
here = os.path.dirname(__file__)
if here not in sys.path:
    sys.path.insert(0, here)

from lexer import Lexer, Token


def simple_tokens(source):
    return list(Lexer(source).tokenize())


def test_keywords_and_identifiers():
    src = "declarar MeuNome como texto"
    toks = simple_tokens(src)
    kinds = [t.tipo for t in toks]
    assert "PALAVRA_CHAVE" in kinds
    assert "IDENTIFICADOR" in kinds


def test_numbers_and_strings():
    src = 'Preco = 99.99\nNome = "produto"'
    toks = simple_tokens(src)
    kinds = [t.tipo for t in toks]
    assert "NUMERO_LITERAL" in kinds
    assert "STRING_LITERAL" in kinds


def test_operators_and_delims():
    src = "(a + b) != c;"
    toks = simple_tokens(src)
    kinds = [t.tipo for t in toks]
    assert any(k == "OP" for k in kinds)
    assert any(k in ("LPAREN", "RPAREN", "SEMICOLON") for k in kinds)


if __name__ == "__main__":
    test_keywords_and_identifiers()
    test_numbers_and_strings()
    test_operators_and_delims()
    print("All tests passed")
