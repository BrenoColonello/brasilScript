import importlib.util
import os
import sys


def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    base = os.path.abspath(os.path.dirname(__file__))
    lexer_path = os.path.join(base, "Semana 6", "lexer.py")
    if not os.path.exists(lexer_path):
        print("lexer.py not found at", lexer_path)
        sys.exit(2)
    # Ensure the 'Semana 6' folder is on sys.path so lexer.py can import local modules
    semana6_dir = os.path.dirname(lexer_path)
    if semana6_dir not in sys.path:
        sys.path.insert(0, semana6_dir)
    mod = load_module_from_path("semana6_lexer", lexer_path)
    # build afd and run smoke-tests similar to pytest tests
    dfa = mod.build_afd()
    src_path = os.path.join(base, "exemplos", "hello_world.bs")
    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()
    lexer = mod.Lexer(dfa, src)
    toks = []
    while True:
        t = lexer.next_token()
        if t is None:
            break
        toks.append(t)

    # basic assertions
    ok = True
    if not any(t.type == "PALAVRA_CHAVE" and t.lexeme == "mostrar" for t in toks):
        print("FAIL: PALAVRA_CHAVE 'mostrar' not found")
        ok = False
    if not any(t.type == "STRING_LITERAL" for t in toks):
        print("FAIL: no STRING_LITERAL found")
        ok = False
    # check positions for first PALAVRA_CHAVE
    for t in toks:
        if t.type == "PALAVRA_CHAVE":
            if t.line < 1 or t.col < 1:
                print("FAIL: position invalid", t)
                ok = False
            break

    if ok:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)


if __name__ == '__main__':
    main()
