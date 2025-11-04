#!/usr/bin/env python3

from src.parser.brasilscript_parser import parse_brasilscript

try:
    code = "declarar lista como lista[numero]"
    print(f"Testando: {code}")
    ast = parse_brasilscript(code)
    print(f"✅ Lista funcionou! {len(ast.statements)} statements")
    print(f"Tipo: {ast.statements[0].type_name}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
