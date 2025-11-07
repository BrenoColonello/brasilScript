#!/usr/bin/env python3
"""
Script para testar o parser do BrasilScript com exemplos
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
            print(f"  {i+1}. {type(stmt).__name__}")
        
    except ParseError as e:
        print(f"❌ Erro de sintaxe: {e}")
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")


def main():
    """Função principal com exemplos de teste"""
    
    print("🚀 Testador do Parser BrasilScript")
    print("==================================")
    
    # Teste 1: Declarações básicas
    test_example("Declarações Básicas", '''
    declarar nome como texto = "BrasilScript"
    declarar versao como numero = 1.0
    declarar ativo como logico = verdadeiro
    ''')
    
    # Teste 2: Estrutura condicional
    test_example("Estrutura Condicional", '''
    declarar idade como numero = 20
    
    se idade >= 18 entao
        mostrar "Maior de idade"
    senao
        mostrar "Menor de idade"
    fim_se
    ''')
    
    # Teste 3: Loop while
    test_example("Loop While", '''
    declarar contador como numero = 0
    
    enquanto contador < 5 faca
        mostrar "Contador: " + contador
        contador = contador + 1
    fim_enquanto
    ''')
    
    # Teste 4: Função
    test_example("Função", '''
    funcao somar(a, b)
        declarar resultado como numero
        resultado = a + b
        retornar resultado
    fim_funcao
    
    declarar x como numero = somar(10, 20)
    mostrar x
    ''')
    
    # Teste 5: Expressões complexas
    test_example("Expressões Complexas", '''
    declarar a como numero = 10
    declarar b como numero = 5
    declarar c como numero = 2
    
    declarar resultado como numero
    resultado = (a + b) * c - a / b
    
    se resultado > 20 e a > b entao
        mostrar "Resultado grande!"
    fim_se
    ''')
    
    # Teste 6: Listas
    test_example("Listas", '''
    declarar numeros como lista[numero]
    numeros = [1, 2, 3, 4, 5]
    
    declarar primeiro como numero
    primeiro = numeros[0]
    
    para_cada num em numeros faca
        mostrar num
    fim_para_cada
    ''')
    
    # Teste 7: Exemplo com erro
    test_example("Código com Erro", '''
    declarar nome como
    mostrar nome
    ''')
    
    # Teste 8: Hello World
    test_example("Hello World", '''
    mostrar "Olá, mundo!"
    mostrar "Bem-vindo ao BrasilScript!"
    ''')
    
    print("\n🎯 Todos os testes concluídos!")


if __name__ == "__main__":
    main()
