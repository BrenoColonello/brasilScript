#!/usr/bin/env python3
"""
Demonstração dos problemas LL(1) na gramática BrasilScript

Este script mostra casos onde a gramática atual é ambígua e requer
lookahead maior que 1 para fazer a decisão correta de parsing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer.lexer import tokenize_text
from src.parser.brasilscript_parser import parse_brasilscript, ParseError


def test_ambiguity_cases():
    """Testa casos que demonstram a não-LL(1) natureza da gramática"""
    
    print(" Demonstração de Problemas LL(1) na Gramática BrasilScript")
    print("=" * 65)
    
    print("\n1.  PROBLEMA: Ambiguidade entre Assignment e Function Call")
    print("-" * 60)
    
    # Casos problemáticos: o parser precisa de mais de 1 token de lookahead
    cases = [
        ("x = 10", "Assignment - precisa ver '=' para decidir"),
        ("x(10)", "Function Call - precisa ver '(' para decidir"),  
        ("resultado = func(a, b)", "Assignment com function call - mais complexo")
    ]
    
    for code, description in cases:
        print(f"\nTeste: {code}")
        print(f"Descrição: {description}")
        
        # Mostrar tokens para análise
        try:
            tokens = tokenize_text(code)
            print("Tokens:", [f"{t[0]}:{t[1]}" for t in tokens if t[0] not in ["WHITESPACE"]])
            
            # Demonstrar a decisão que um parser LL(1) precisa fazer
            first_token = tokens[0] if tokens else None
            second_token = tokens[1] if len(tokens) > 1 and tokens[1][0] != "WHITESPACE" else None
            if len(tokens) > 2 and tokens[1][0] == "WHITESPACE":
                second_token = tokens[2] if len(tokens) > 2 else None
                
            print(f"Primeiro token: {first_token}")
            print(f"Segundo token: {second_token}")
            
            if first_token and first_token[0] == "IDENTIFICADOR":
                print("  PROBLEMA LL(1): Com apenas o primeiro token (IDENTIFICADOR),")
                print("   não é possível decidir entre <Assignment> ou <FuncCall>")
                print("   É necessário lookahead de 2 tokens para ver se vem '=' ou '('")
            
            # Tentar fazer o parse
            try:
                ast = parse_brasilscript(code)
                print(" Parser atual conseguiu processar (com lookahead implementado)")
                if ast.statements:
                    print(f"   Resultado: {type(ast.statements[0]).__name__}")
            except Exception as e:
                print(f" Erro no parser: {e}")
                
        except Exception as e:
            print(f" Erro no lexer: {e}")
        
        print()
    
    print("\n2.  PROBLEMA: Ambiguidade em Factor")
    print("-" * 40)
    
    factor_cases = [
        ("x", "Identifier simples"),
        ("func()", "Function call"),
        ("arr[0]", "Array access")
    ]
    
    for code, description in factor_cases:
        print(f"\nTeste: {code}")
        print(f"Descrição: {description}")
        
        try:
            tokens = tokenize_text(code)
            clean_tokens = [t for t in tokens if t[0] not in ["WHITESPACE"]]
            print("Tokens:", [f"{t[0]}:{t[1]}" for t in clean_tokens])
            
            if clean_tokens and clean_tokens[0][0] == "IDENTIFICADOR":
                print(" PROBLEMA LL(1): Todos começam com IDENTIFICADOR")
                print("  Parser LL(1) não consegue decidir qual produção de <Factor> usar")
                print(" Precisa ver o próximo token: '(', '[', ou fim da expressão")
        
        except Exception as e:
            print(f"Erro no lexer: {e}")
    
    print("\n3.  Análise de Lookahead Necessário")
    print("-" * 45)
    
    lookahead_examples = [
        ("x", 1, "Identifier simples - LL(1) OK"),
        ("x = 10", 2, "Assignment - precisa de LL(2)"),
        ("x()", 2, "Function call - precisa de LL(2)"),
        ("x[0]", 2, "Array access - precisa de LL(2)"),
        ("x[0] = 5", 3, "Array assignment - precisa de LL(3)+"),
        ("func(a, b)", 2, "Function call com params - precisa de LL(2)"),
    ]
    
    print("Código                | k  | Análise")
    print("-" * 50)
    for code, k, analysis in lookahead_examples:
        print(f"{code:<20} | {k}  | {analysis}")
    
    print("\n4. Soluções Possíveis")
    print("-" * 30)
    
    solutions = [
        "1. Refatorar gramática para LL(1) - Fatorar produções com prefixos comuns",
        "2. Usar parser LR(1) - Mais poderoso, lida com essas ambiguidades",
        "3. Parser recursivo descendente com backtracking - Atual implementação",
        "4. Parser LL(k) com k > 1 - Permite mais lookahead"
    ]
    
    for solution in solutions:
        print(f"  {solution}")
    
    print("\n5.  Conclusão")
    print("-" * 15)
    print("A gramática BrasilScript atual NÃO é LL(1) devido a:")
    print("  • Ambiguidade entre Assignment e Function Call")
    print("  • Ambiguidade em Factor (identifier, function call, array access)")
    print("  • Necessidade de lookahead k > 1 em vários casos")
    print("\nO parser atual funciona porque implementa lookahead além de 1 token,")
    print("mas tecnicamente não é um parser LL(1) puro.")


if __name__ == "__main__":
    test_ambiguity_cases()
