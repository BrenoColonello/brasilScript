"""Quick smoke test for src/lexer/lexer.py"""
from src.lexer.lexer import build_lexer_dfa, tokenize_with_dfa


def test_tokenize():
    dfa = build_lexer_dfa()
    toks = tokenize_with_dfa(dfa, "a = 123 b = abc")
    assert ("NUMERO_LITERAL", "123") in toks
    assert ("IDENTIFICADOR", "a") in toks


if __name__ == '__main__':
    test_tokenize()
    print('ok')
