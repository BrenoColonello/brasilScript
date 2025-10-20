import os
from Semana_6.lexer import build_afd, Lexer


def load_example(name):
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "exemplos", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_hello_world_tokens():
    src = load_example("hello_world.bs")
    dfa = build_afd()
    lex = Lexer(dfa, src)
    tokens = []
    while True:
        t = lex.next_token()
        if t is None:
            break
        tokens.append((t.type, t.lexeme))
    # expect at least shows and string tokens present
    assert any(t[0] == "PALAVRA_CHAVE" and t[1] == "mostrar" for t in tokens)
    assert any(t[0] == "STRING_LITERAL" for t in tokens)


def test_positions():
    src = load_example("hello_world.bs")
    dfa = build_afd()
    lex = Lexer(dfa, src)
    # find first PALAVRA_CHAVE token and check its line is > 0
    while True:
        t = lex.next_token()
        if t is None:
            break
        if t.type == "PALAVRA_CHAVE":
            assert t.line >= 1
            assert t.col >= 1
            return
    assert False, "PALAVRA_CHAVE not found"
