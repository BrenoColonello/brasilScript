"""
Testes para o Parser do BrasilScript

Este módulo contém testes unitários para validar o funcionamento
do parser recursivo descendente.
"""

try:
    import pytest
except ImportError:
    # Mock pytest para quando não estiver disponível
    class pytest:
        @staticmethod
        def raises(exception):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    try:
                        func(*args, **kwargs)
                        raise AssertionError(f"Expected {exception} to be raised")
                    except exception:
                        pass  # Esperado
                return wrapper
            return decorator

from src.parser.brasilscript_parser import (
    parse_brasilscript, ParseError, Program, Declaration, Assignment,
    IfStatement, WhileStatement, FunctionDecl, PrintStatement,
    BinaryOperation, Literal, Identifier, FunctionCall, ListLiteral,
    ForEachStatement, RepeatStatement
)


class TestBrasilScriptParser:
    """Testes para o parser do BrasilScript"""
    
    def test_simple_declaration(self):
        """Testa declaração simples de variável"""
        code = "declarar x como numero"
        ast = parse_brasilscript(code)
        
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], Declaration)
        assert ast.statements[0].identifier == "x"
        assert ast.statements[0].type_name == "numero"
        assert ast.statements[0].initial_value is None
    
    def test_declaration_with_initialization(self):
        """Testa declaração com inicialização"""
        code = "declarar idade como numero = 25"
        ast = parse_brasilscript(code)
        
        decl = ast.statements[0]
        assert isinstance(decl, Declaration)
        assert decl.identifier == "idade"
        assert decl.type_name == "numero"
        assert isinstance(decl.initial_value, Literal)
        assert decl.initial_value.value == 25
    
    def test_assignment(self):
        """Testa atribuição simples"""
        code = "x = 42"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.identifier == "x"
        assert isinstance(stmt.value, Literal)
        assert stmt.value.value == 42
    
    def test_print_statement(self):
        """Testa comando mostrar"""
        code = 'mostrar "Ola, mundo!"'
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, PrintStatement)
        assert len(stmt.expressions) == 1
        assert isinstance(stmt.expressions[0], Literal)
        assert stmt.expressions[0].value == '"Ola, mundo!"'
    
    def test_if_statement(self):
        """Testa estrutura condicional"""
        code = '''
        se x > 10 entao
            mostrar "maior"
        fim_se
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert isinstance(stmt.condition, BinaryOperation)
        assert stmt.condition.operator == ">"
        assert len(stmt.then_block) == 1
        assert isinstance(stmt.then_block[0], PrintStatement)
    
    def test_if_else_statement(self):
        """Testa if-else"""
        code = '''
        se x > 10 entao
            mostrar "maior"
        senao
            mostrar "menor ou igual"
        fim_se
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.else_block is not None
        assert len(stmt.else_block) == 1
        assert isinstance(stmt.else_block[0], PrintStatement)
    
    def test_while_statement(self):
        """Testa loop while"""
        code = '''
        enquanto i < 10 faca
            i = i + 1
        fim_enquanto
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileStatement)
        assert isinstance(stmt.condition, BinaryOperation)
        assert len(stmt.body) == 1
        assert isinstance(stmt.body[0], Assignment)
    
    def test_function_declaration(self):
        """Testa declaração de função"""
        code = '''
        funcao somar(a, b)
            retornar a + b
        fim_funcao
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionDecl)
        assert stmt.name == "somar"
        assert stmt.parameters == ["a", "b"]
        assert len(stmt.body) == 1
    
    def test_arithmetic_expression(self):
        """Testa expressões aritméticas"""
        code = "resultado = a + b * 2"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, Assignment)
        
        # Deve respeitar precedência: a + (b * 2)
        expr = stmt.value
        assert isinstance(expr, BinaryOperation)
        assert expr.operator == "+"
        assert isinstance(expr.left, Identifier)
        assert expr.left.name == "a"
        assert isinstance(expr.right, BinaryOperation)
        assert expr.right.operator == "*"
    
    def test_logical_expression(self):
        """Testa expressões lógicas"""
        code = '''
        se x > 5 e y < 10 entao
            mostrar "ok"
        fim_se
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        condition = stmt.condition
        assert isinstance(condition, BinaryOperation)
        assert condition.operator == "e"
    
    def test_list_declaration(self):
        """Testa declaração de lista"""
        code = "declarar numeros como lista[numero]"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, Declaration)
        assert stmt.type_name == "lista[numero]"
    
    def test_complex_program(self):
        """Testa programa mais complexo"""
        code = '''
        declarar idade como numero = 18
        declarar nome como texto = "Maria"
        
        se idade >= 18 entao
            mostrar nome + " e maior de idade"
        senao
            mostrar nome + " e menor de idade"
        fim_se
        
        funcao cumprimentar(pessoa)
            mostrar "Ola, " + pessoa
        fim_funcao
        
        cumprimentar(nome)
        '''
        
        ast = parse_brasilscript(code)
        assert isinstance(ast, Program)
        assert len(ast.statements) == 4  # 2 declarações, 1 if, 1 função, 1 chamada
    
    def test_syntax_error(self):
        """Testa detecção de erro de sintaxe"""
        code = "declarar x como"  # Tipo faltando
        
        with pytest.raises(ParseError):
            parse_brasilscript(code)
    
    def test_nested_expressions(self):
        """Testa expressões aninhadas"""
        code = "resultado = (a + b) * (c - d)"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        expr = stmt.value
        assert isinstance(expr, BinaryOperation)
        assert expr.operator == "*"
        # Ambos os lados devem ser expressões em parênteses
        assert isinstance(expr.left, BinaryOperation)
        assert isinstance(expr.right, BinaryOperation)
    
    def test_function_call(self):
        """Testa chamada de função"""
        code = "resultado = somar(10, 20)"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, FunctionCall)
        assert stmt.value.name == "somar"
        assert len(stmt.value.arguments) == 2
    
    def test_list_literal(self):
        """Testa literal de lista"""
        code = "numeros = [1, 2, 3, 4]"
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt.value, ListLiteral)
        assert len(stmt.value.elements) == 4
    
    def test_for_each_loop(self):
        """Testa loop para_cada"""
        code = '''
        para_cada item em lista faca
            mostrar item
        fim_para_cada
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, ForEachStatement)
        assert stmt.variable == "item"
        assert isinstance(stmt.iterable, Identifier)
        assert stmt.iterable.name == "lista"
    
    def test_repeat_loop(self):
        """Testa loop repetir"""
        code = '''
        repetir 5 vezes
            mostrar "repetindo"
        fim_repetir
        '''
        ast = parse_brasilscript(code)
        
        stmt = ast.statements[0]
        assert isinstance(stmt, RepeatStatement)
        assert isinstance(stmt.count, Literal)
        assert stmt.count.value == 5


# Testes de integração com exemplos reais
class TestRealExamples:
    """Testes com exemplos reais do BrasilScript"""
    
    def test_hello_world(self):
        """Testa exemplo hello world"""
        code = '''
        mostrar "Ola, mundo!"
        mostrar "Bem-vindo a BrasilScript!"
        '''
        
        ast = parse_brasilscript(code)
        assert len(ast.statements) == 2
        assert all(isinstance(stmt, PrintStatement) for stmt in ast.statements)
    
    def test_calculator_example(self):
        """Testa exemplo de calculadora (simplificado)"""
        code = '''
        declarar num1 como numero = 10
        declarar num2 como numero = 5
        declarar resultado como numero
        
        se operacao = "+" entao
            resultado = num1 + num2
        senao_se operacao = "-" entao
            resultado = num1 - num2
        fim_se
        
        mostrar "Resultado: " + resultado
        '''
        
        ast = parse_brasilscript(code)
        assert len(ast.statements) == 4  # 3 declarações, 1 if, 1 print
    
    def test_function_example(self):
        """Testa exemplo com função"""
        code = '''
        funcao somar(a, b)
            declarar soma como numero
            soma = a + b
            retornar soma
        fim_funcao
        
        declarar x como numero = 5
        declarar y como numero = 3
        declarar resultado como numero
        resultado = somar(x, y)
        mostrar resultado
        '''
        
        ast = parse_brasilscript(code)
        assert len(ast.statements) == 5  # 1 função, 3 declarações, 1 assignment, 1 print


if __name__ == "__main__":
    # Executar testes simples
    test = TestBrasilScriptParser()
    
    try:
        test.test_simple_declaration()
        print("✓ Teste de declaração simples passou")
        
        test.test_declaration_with_initialization()
        print("✓ Teste de declaração com inicialização passou")
        
        test.test_assignment()
        print("✓ Teste de atribuição passou")
        
        test.test_print_statement()
        print("✓ Teste de print passou")
        
        print("\n🎉 Todos os testes básicos passaram!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
