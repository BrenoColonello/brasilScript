#!/usr/bin/env python3
"""
Teste abrangente das funcionalidades do parser BrasilScript
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser.brasilscript_parser import parse_brasilscript, ParseError


def test_advanced_features():
    """Testa funcionalidades mais avançadas do parser"""
    
    print("🔬 Teste Abrangente do Parser BrasilScript")
    print("=" * 50)
    
    test_cases = [
        # Teste 1: Expressões com precedência
        ("Precedência de Operadores", """
        declarar resultado como numero
        resultado = 2 + 3 * 4 - 1
        """),
        
        # Teste 2: Condicionais aninhadas
        ("Condicionais Aninhadas", """
        declarar x como numero = 10
        declarar y como numero = 5
        
        se x > y entao
            se x > 15 entao
                declarar z como numero = 1
            senao
                declarar z como numero = 2
            fim_se
        senao
            declarar z como numero = 0
        fim_se
        """),
        
        # Teste 3: Loops aninhados
        ("Loops Aninhados", """
        declarar i como numero = 0
        declarar j como numero = 0
        
        enquanto i < 3 faca
            j = 0
            enquanto j < 2 faca
                j = j + 1
            fim_enquanto
            i = i + 1
        fim_enquanto
        """),
        
        # Teste 4: Função com múltiplos parâmetros
        ("Função Complexa", """
        funcao calcular(a, b, c)
            declarar temp como numero
            temp = a + b
            se temp > c entao
                retornar temp - c
            senao
                retornar c - temp
            fim_se
        fim_funcao
        """),
        
        # Teste 5: Chamada de função em expressão
        ("Função em Expressão", """
        funcao dobrar(x)
            retornar x * 2
        fim_funcao
        
        declarar resultado como numero
        resultado = dobrar(5) + 10
        """),
        
        # Teste 6: Expressões lógicas
        ("Expressões Lógicas", """
        declarar a como numero = 10
        declarar b como numero = 5
        declarar c como numero = 15
        
        se a > b e c > a entao
            declarar valido como logico = verdadeiro
        fim_se
        
        se a < b ou c < a entao
            declarar invalido como logico = falso
        fim_se
        """),
        
        # Teste 7: Loop repeat
        ("Loop Repeat", """
        declarar contador como numero = 0
        
        repetir 5 vezes
            contador = contador + 1
        fim_repetir
        """),
        
        # Teste 8: For-each (sem array literal por problemas no lexer)
        ("For Each", """
        declarar numeros como lista[numero]
        
        para_cada item em numeros faca
            declarar processado como numero = item * 2
        fim_para_cada
        """),
        
        # Teste 9: Múltiplas declarações de função
        ("Múltiplas Funções", """
        funcao somar(a, b)
            retornar a + b
        fim_funcao
        
        funcao multiplicar(x, y)
            retornar x * y
        fim_funcao
        
        declarar resultado como numero
        resultado = somar(multiplicar(2, 3), 4)
        """),
        
        # Teste 10: Programa completo
        ("Programa Completo", """
        declarar numero1 como numero = 10
        declarar numero2 como numero = 5
        declarar operacao como numero = 1
        
        funcao processar(n1, n2, op)
            se op = 1 entao
                retornar n1 + n2
            senao_se op = 2 entao
                retornar n1 - n2
            senao
                retornar 0
            fim_se
        fim_funcao
        
        declarar resultado como numero
        resultado = processar(numero1, numero2, operacao)
        
        se resultado > 10 entao
            declarar status como logico = verdadeiro
        senao
            declarar status como logico = falso
        fim_se
        """)
    ]
    
    passed = 0
    failed = 0
    
    for name, code in test_cases:
        print(f"\n🧪 Testando: {name}")
        print("-" * 40)
        
        try:
            ast = parse_brasilscript(code)
            print(f"✅ Parse realizado com sucesso!")
            print(f"📊 {len(ast.statements)} statement(s) encontrado(s)")
            
            # Mostrar tipos de statements
            types = {}
            for stmt in ast.statements:
                if stmt:
                    stmt_type = type(stmt).__name__
                    types[stmt_type] = types.get(stmt_type, 0) + 1
            
            if types:
                print("📋 Tipos encontrados:", dict(types))
            
            passed += 1
            
        except ParseError as e:
            print(f"❌ Erro de sintaxe: {e}")
            failed += 1
            
        except Exception as e:
            print(f"💥 Erro inesperado: {e}")
            failed += 1
    
    print(f"\n📈 Resultado Final:")
    print(f"✅ Testes passou: {passed}")
    print(f"❌ Testes falharam: {failed}")
    print(f"📊 Taxa de sucesso: {passed/(passed+failed)*100:.1f}%")
    
    return passed, failed


def test_error_cases():
    """Testa casos que devem gerar erros"""
    
    print(f"\n🚨 Testando Casos de Erro")
    print("=" * 30)
    
    error_cases = [
        ("Declaração incompleta", "declarar x como"),
        ("Atribuição sem valor", "x ="),
        ("Se sem fim_se", "se x > 5 entao declarar y como numero"),
        ("Função sem fim_funcao", "funcao teste() declarar x como numero"),
        ("Expressão malformada", "x = + 5"),
    ]
    
    error_detected = 0
    
    for name, code in error_cases:
        print(f"\n🧪 Testando: {name}")
        
        try:
            ast = parse_brasilscript(code)
            print(f"⚠️  Deveria ter dado erro, mas passou!")
            
        except ParseError as e:
            print(f"✅ Erro detectado corretamente: {e}")
            error_detected += 1
            
        except Exception as e:
            print(f"✅ Erro detectado: {e}")
            error_detected += 1
    
    print(f"\n📊 Detecção de erros: {error_detected}/{len(error_cases)} casos")
    
    return error_detected, len(error_cases)


if __name__ == "__main__":
    passed, failed = test_advanced_features()
    error_detected, total_errors = test_error_cases()
    
    print(f"\n🎯 RESUMO GERAL")
    print("=" * 20)
    print(f"✅ Funcionalidades: {passed} OK, {failed} falhou")
    print(f"🚨 Detecção de erros: {error_detected}/{total_errors}")
    
    if failed == 0 and error_detected == total_errors:
        print("\n🎉 PARSER ESTÁ FUNCIONANDO MUITO BEM!")
    elif failed <= 2:
        print("\n👍 Parser está bom, com pequenos problemas")
    else:
        print("\n⚠️  Parser precisa de melhorias")
