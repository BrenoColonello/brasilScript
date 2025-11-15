#!/usr/bin/env python3
"""
Teste simples do lexer e parser sem strings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer.lexer import tokenize_text
from parser.brasilscript_parser import parse_brasilscript, ParseError


def test_lexer():
    """Testa o lexer com código simples"""
    print("🔍 Testando Lexer")
    print("=" * 30)
    
    # Teste simples sem strings
    code = "declarar x como numero"
    print(f"Código: {code}")
    
    try:
        tokens = tokenize_text(code)
        print("Tokens:")
        for token in tokens:
            print(f"  {token}")
    except Exception as e:
        print(f"Erro no lexer: {e}")


def test_parser():
    """Testa o parser com código simples"""
    print("\n🔧 Testando Parser")
    print("=" * 30)
    
    # Teste muito simples
    code = "declarar x como numero"
    print(f"Código: {code}")
    
    try:
        ast = parse_brasilscript(code)
        print(f"✅ Parser funcionou!")
        print(f"Statements: {len(ast.statements)}")
        if ast.statements:
            stmt = ast.statements[0]
            print(f"Tipo: {type(stmt).__name__}")
    except Exception as e:
        print(f"❌ Erro no parser: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_lexer()
    test_parser()
