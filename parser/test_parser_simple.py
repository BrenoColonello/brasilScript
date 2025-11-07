#!/usr/bin/env python3
"""
Script para testar o parser do BrasilScript com exemplos simples (sem strings)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser.brasilscript_parser import parse_brasilscript, ParseError


def test_example(name: str, code: str):
    """Testa um exemplo de código"""
    print(f"\n🧪 Testando: {name}")
    print("=" * 50)
    print("Código:")
    print(code.strip())
    print("\nResultado:")
    
    try:
        ast = parse_brasilscript(code)
        print(f"✅ Parse realizado com sucesso!")
        print(f"📊 {len(ast.statements)} statement(s) encontrado(s)")
        
        # Mostrar estrutura básica
        for i, stmt in enumerate(ast.statements):
            if stmt:  # Ignorar None
                print(f"  {i+1}. {type(stmt).__name__}")
        
    except ParseError as e:
        print(f"❌ Erro de sintaxe: {e}")
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Função principal com exemplos simples"""
    
    print("🚀 Testador Simples do Parser BrasilScript")
    print("==========================================")
    
    # Teste 1: Declaração simples
    test_example("Declaração Simples", '''
    declarar x como numero
    ''')
    
    # Teste 2: Declaração com valor
    test_example("Declaração com Valor", '''
    declarar x como numero = 42
    ''')
    
    # Teste 3: Atribuição
    test_example("Atribuição", '''
    declarar x como numero
    x = 10
    ''')
    
    # Teste 4: Múltiplas declarações
    test_example("Múltiplas Declarações", '''
    declarar a como numero = 1
    declarar b como numero = 2
    declarar c como numero = 3
    ''')
    
    # Teste 5: Expressão aritmética
    test_example("Expressão Aritmética", '''
    declarar resultado como numero
    resultado = 10 + 20 * 2
    ''')
    
    # Teste 6: Condicional simples
    test_example("Condicional Simples", '''
    declarar x como numero = 10
    se x > 5 entao
        declarar y como numero = 1
    fim_se
    ''')
    
    # Teste 7: Loop enquanto
    test_example("Loop Enquanto", '''
    declarar i como numero = 0
    enquanto i < 5 faca
        i = i + 1
    fim_enquanto
    ''')
    
    # Teste 8: Função simples
    test_example("Função Simples", '''
    funcao somar(a, b)
        declarar resultado como numero
        resultado = a + b
        retornar resultado
    fim_funcao
    ''')
    
    print("\n🎯 Todos os testes concluídos!")


if __name__ == "__main__":
    main()
