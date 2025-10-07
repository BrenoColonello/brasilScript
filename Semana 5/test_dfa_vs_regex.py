"""Compare tokens produced by regex-based Lexer and DFA-based Lexer on sample inputs."""
import os
import sys
here = os.path.dirname(__file__)
if here not in sys.path:
    sys.path.insert(0, here)

from lexer import Lexer as RegexLexer
from dfa_lexer import LexerDFA


CASES = [
    'declarar MeuNome como texto',
    'Preco = 99.99\nNome = "produto"',
    '(a + b) != c;',
    "# comentario\nmostrar 'oi'\n",
    'x = 1e-3; y = 42',
]


def tokens_from_regex(src):
    return [(t.tipo, t.valor) for t in RegexLexer(src).tokenize()]


def tokens_from_dfa(src):
    return [(t.tipo, t.valor) for t in LexerDFA(src).tokenize()]


def test_equivalence_on_cases():
    for src in CASES:
        r = tokens_from_regex(src)
        d = tokens_from_dfa(src)
        assert r == d, f"Mismatch on {src!r}:\nregex={r}\ndfa={d}\n"


if __name__ == '__main__':
    test_equivalence_on_cases()
    print('Equivalence tests passed')
