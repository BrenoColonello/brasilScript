def test_lexer_smoke():
    from lexer import build_lexer_dfa, tokenize_with_dfa
    dfa = build_lexer_dfa()
    toks = tokenize_with_dfa(dfa, 'x = 123 y = abc')
    assert ('NUMERO_LITERAL', '123') in toks
    assert ('IDENTIFICADOR', 'x') in toks

if __name__ == '__main__':
    test_lexer_smoke()
    print('ok')
