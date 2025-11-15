"""
Parser Recursivo Descendente para BrasilScript

Este módulo implementa um parser recursivo descendente básico seguindo
a gramática formal definida para o BrasilScript.
"""

from typing import List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass

# Assumindo que temos o lexer disponível (pacote top-level `lexer`)
from lexer.lexer import tokenize_text


class TokenType(Enum):
    """Tipos de tokens reconhecidos pelo lexer"""
    PALAVRA_CHAVE = "PALAVRA_CHAVE"
    IDENTIFICADOR = "IDENTIFICADOR"
    NUMERO_LITERAL = "NUMERO_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    LOGICO_LITERAL = "LOGICO_LITERAL"
    OP = "OP"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    DOT = "DOT"
    EOF = "EOF"


@dataclass
class Token:
    """Representa um token do código fonte"""
    type: str
    value: str
    line: int = 0
    column: int = 0


# Nós da AST (tentar importar do módulo compartilhado `src.parser.ast`)
try:
    from src.parser.ast import (
        Program, Declaration, Assignment, FunctionDecl, IfStatement,
        WhileStatement, RepeatStatement, ForEachStatement, PrintStatement,
        InputStatement, ReturnStatement, FunctionCall, BinaryOperation,
        UnaryOperation, Literal, Identifier, ListLiteral, IndexAccess
    )
except Exception:
    # Import fallback (mantém as definições locais caso o módulo não esteja disponível)
    from dataclasses import dataclass
    from typing import List, Optional, Union

    @dataclass
    class ASTNode:
        pass

    @dataclass
    class Program(ASTNode):
        statements: List[ASTNode]

    @dataclass
    class Declaration(ASTNode):
        identifier: str
        type_name: str
        initial_value: Optional[ASTNode] = None

    @dataclass
    class Assignment(ASTNode):
        identifier: str
        value: ASTNode

    @dataclass
    class FunctionDecl(ASTNode):
        name: str
        parameters: List[str]
        body: List[ASTNode]

    @dataclass
    class IfStatement(ASTNode):
        condition: ASTNode
        then_block: List[ASTNode]
        else_ifs: List[tuple]
        else_block: Optional[List[ASTNode]] = None

    @dataclass
    class WhileStatement(ASTNode):
        condition: ASTNode
        body: List[ASTNode]

    @dataclass
    class RepeatStatement(ASTNode):
        count: ASTNode
        body: List[ASTNode]

    @dataclass
    class ForEachStatement(ASTNode):
        variable: str
        iterable: ASTNode
        body: List[ASTNode]

    @dataclass
    class PrintStatement(ASTNode):
        expressions: List[ASTNode]

    @dataclass
    class InputStatement(ASTNode):
        prompt: ASTNode
        variable: str

    @dataclass
    class ReturnStatement(ASTNode):
        value: Optional[ASTNode] = None

    @dataclass
    class FunctionCall(ASTNode):
        name: str
        arguments: List[ASTNode]

    @dataclass
    class BinaryOperation(ASTNode):
        left: ASTNode
        operator: str
        right: ASTNode

    @dataclass
    class UnaryOperation(ASTNode):
        operator: str
        operand: ASTNode

    @dataclass
    class Literal(ASTNode):
        value: Union[int, float, str, bool]
        type: str

    @dataclass
    class Identifier(ASTNode):
        name: str

    @dataclass
    class ListLiteral(ASTNode):
        elements: List[ASTNode]

    @dataclass
    class IndexAccess(ASTNode):
        object: ASTNode
        index: ASTNode


class ParseError(Exception):
    """Exceção lançada quando há erro de sintaxe"""
    pass


class BrasilScriptParser:
    """Parser recursivo descendente para BrasilScript"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        
    def peek(self) -> Token:
        """Retorna o token atual sem consumir"""
        if self.current >= len(self.tokens):
            return Token("EOF", "")
        return self.tokens[self.current]
    
    def advance(self) -> Token:
        """Consome e retorna o token atual"""
        token = self.peek()
        if self.current < len(self.tokens):
            self.current += 1
        return token
    
    def match(self, expected: Union[str, List[str]]) -> bool:
        """Verifica se o token atual casa com o esperado"""
        current_token = self.peek()
        if isinstance(expected, str):
            # Se é um tipo de token (maiúsculo)
            if expected.isupper():
                return current_token.type == expected
            # Se é um valor específico
            return current_token.value == expected
        
        # Lista de expectativas
        for exp in expected:
            if exp.isupper():
                if current_token.type == exp:
                    return True
            else:
                if current_token.value == exp:
                    return True
        return False
    
    def consume(self, expected: str) -> Token:
        """Consome um token esperado ou lança erro"""
        current = self.peek()
        
        # Se esperamos um tipo de token (maiúsculo)
        if expected.isupper():
            if current.type == expected:
                return self.advance()
            raise ParseError(f"Esperado token {expected}, encontrado {current.type}: '{current.value}'")
        
        # Se esperamos um valor específico
        if current.value == expected:
            return self.advance()
        raise ParseError(f"Esperado '{expected}', encontrado '{current.value}'")
    
    def parse(self) -> Program:
        """Ponto de entrada do parser - programa completo"""
        statements = self.parse_statement_list()
        return Program(statements)
    
    def parse_statement_list(self) -> List[ASTNode]:
        """StatementList = { Statement }"""
        statements = []
        while not self.match("EOF") and not self.match(["fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", "fim_funcao"]):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Statement = Declaration | Assignment | IfStmt | WhileStmt | ..."""
        current = self.peek()
        
        # Pular se chegou ao fim
        if current.type == "EOF":
            return None
            
        # Verificar palavra-chave ou identificador
        if current.type == "PALAVRA_CHAVE":
            if current.value == "declarar":
                return self.parse_declaration()
            elif current.value == "se":
                return self.parse_if_statement()
            elif current.value == "enquanto":
                return self.parse_while_statement()
            elif current.value == "repetir":
                return self.parse_repeat_statement()
            elif current.value == "para_cada":
                return self.parse_foreach_statement()
            elif current.value == "mostrar":
                return self.parse_print_statement()
            elif current.value == "perguntar":
                return self.parse_input_statement()
            elif current.value == "retornar":
                return self.parse_return_statement()
            elif current.value == "funcao":
                return self.parse_function_decl()
            elif current.value == "parar":
                self.advance()
                return None  # Break statement (pode ser representado diferente)
        elif current.type == "IDENTIFICADOR":
            # Pode ser assignment ou function call
            next_token = self.tokens[self.current + 1] if self.current + 1 < len(self.tokens) else None
            if next_token and next_token.value == "=":
                return self.parse_assignment()
            elif next_token and next_token.value == "(":
                return self.parse_function_call()
        
        # Se chegou aqui, não reconheceu o statement - pular este token
        print(f"⚠️  Token não reconhecido: {current.type} = '{current.value}'")
        self.advance()
        return None
    
    def parse_declaration(self) -> Declaration:
        """Declaration = "declarar" Identifier "como" Type [ "=" Expression ]"""
        self.consume("declarar")
        identifier = self.consume("IDENTIFICADOR").value
        self.consume("como")
        type_name = self.parse_type()
        
        initial_value = None
        if self.match("="):
            self.advance()
            initial_value = self.parse_expression()
        
        return Declaration(identifier, type_name, initial_value)
    
    def parse_type(self) -> str:
        """Type = "numero" | "texto" | "logico" | "lista" [ "[" Type "]" ]"""
        current = self.peek()
        if current.type == "PALAVRA_CHAVE" and current.value in ["numero", "texto", "logico", "lista"]:
            type_name = self.advance().value
            if type_name == "lista" and self.match("["):
                self.consume("[")
                element_type = self.parse_type()
                self.consume("]")
                return f"lista[{element_type}]"
            return type_name
        else:
            raise ParseError(f"Tipo esperado, encontrado '{current.type}:{current.value}'")
    
    def parse_assignment(self) -> Assignment:
        """Assignment = Identifier "=" Expression"""
        identifier = self.consume("IDENTIFICADOR").value
        self.consume("=")
        value = self.parse_expression()
        return Assignment(identifier, value)
    
    def parse_function_decl(self) -> FunctionDecl:
        """FuncDecl = "funcao" Identifier "(" [ FormalParams ] ")" StatementList "fim_funcao" """
        self.consume("funcao")
        name = self.consume("IDENTIFICADOR").value
        self.consume("(")
        
        parameters = []
        if not self.match(")"):
            parameters = self.parse_formal_params()
        
        self.consume(")")
        body = self.parse_statement_list()
        self.consume("fim_funcao")
        
        return FunctionDecl(name, parameters, body)
    
    def parse_formal_params(self) -> List[str]:
        """FormalParams = Identifier { "," Identifier }"""
        params = [self.consume("IDENTIFICADOR").value]
        
        while self.match(","):
            self.advance()
            params.append(self.consume("IDENTIFICADOR").value)
        
        return params
    
    def parse_if_statement(self) -> IfStatement:
        """IfStmt = "se" Condition "entao" StatementList { "senao_se" Condition "entao" StatementList } [ "senao" StatementList ] "fim_se" """
        self.consume("se")
        condition = self.parse_condition()
        self.consume("entao")
        then_block = self.parse_statement_list()
        
        else_ifs = []
        while self.match("senao_se"):
            self.advance()
            elif_condition = self.parse_condition()
            self.consume("entao")
            elif_block = self.parse_statement_list()
            else_ifs.append((elif_condition, elif_block))
        
        else_block = None
        if self.match("senao"):
            self.advance()
            else_block = self.parse_statement_list()
        
        self.consume("fim_se")
        return IfStatement(condition, then_block, else_ifs, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        """WhileStmt = "enquanto" Condition "faca" StatementList "fim_enquanto" """
        self.consume("enquanto")
        condition = self.parse_condition()
        self.consume("faca")
        body = self.parse_statement_list()
        self.consume("fim_enquanto")
        return WhileStatement(condition, body)
    
    def parse_repeat_statement(self) -> RepeatStatement:
        """RepeatStmt = "repetir" Expression "vezes" StatementList "fim_repetir" """
        self.consume("repetir")
        count = self.parse_expression()
        self.consume("vezes")
        body = self.parse_statement_list()
        self.consume("fim_repetir")
        return RepeatStatement(count, body)
    
    def parse_foreach_statement(self) -> ForEachStatement:
        """ForStmt = "para_cada" Identifier "em" Expression "faca" StatementList "fim_para_cada" """
        self.consume("para_cada")
        variable = self.consume("IDENTIFICADOR").value
        self.consume("em")
        iterable = self.parse_expression()
        self.consume("faca")
        body = self.parse_statement_list()
        self.consume("fim_para_cada")
        return ForEachStatement(variable, iterable, body)
    
    def parse_print_statement(self) -> PrintStatement:
        """PrintStmt = "mostrar" Expression { "," Expression }"""
        self.consume("mostrar")
        expressions = [self.parse_expression()]
        
        while self.match(","):
            self.advance()
            expressions.append(self.parse_expression())
        
        return PrintStatement(expressions)
    
    def parse_input_statement(self) -> InputStatement:
        """InputStmt = "perguntar" Expression "guardar_em" Identifier"""
        self.consume("perguntar")
        prompt = self.parse_expression()
        self.consume("guardar_em")
        variable = self.consume("IDENTIFICADOR").value
        return InputStatement(prompt, variable)
    
    def parse_return_statement(self) -> ReturnStatement:
        """ReturnStmt = "retornar" [ Expression ]"""
        self.consume("retornar")
        value = None
        if not self.match(["fim_funcao", "EOF"]):
            value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_function_call(self) -> FunctionCall:
        """FuncCall = Identifier "(" [ ActualParams ] ")" """
        name = self.consume("IDENTIFICADOR").value
        self.consume("(")
        
        arguments = []
        if not self.match(")"):
            arguments = self.parse_actual_params()
        
        self.consume(")")
        return FunctionCall(name, arguments)
    
    def parse_actual_params(self) -> List[ASTNode]:
        """ActualParams = Expression { "," Expression }"""
        params = [self.parse_expression()]
        
        while self.match(","):
            self.advance()
            params.append(self.parse_expression())
        
        return params
    
    def parse_condition(self) -> ASTNode:
        """Condition = OrCondition"""
        return self.parse_or_condition()
    
    def parse_or_condition(self) -> ASTNode:
        """OrCondition = AndCondition { "ou" AndCondition }"""
        left = self.parse_and_condition()
        
        while self.match("ou"):
            operator = self.advance().value
            right = self.parse_and_condition()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_and_condition(self) -> ASTNode:
        """AndCondition = NotCondition { "e" NotCondition }"""
        left = self.parse_not_condition()
        
        while self.match("e"):
            operator = self.advance().value
            right = self.parse_not_condition()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_not_condition(self) -> ASTNode:
        """NotCondition = "nao" PrimaryCondition | PrimaryCondition"""
        if self.match("nao"):
            operator = self.advance().value
            operand = self.parse_primary_condition()
            return UnaryOperation(operator, operand)
        
        return self.parse_primary_condition()
    
    def parse_primary_condition(self) -> ASTNode:
        """PrimaryCondition = Expression [ RelOp Expression ] | "(" Condition ")" """
        if self.match("("):
            self.advance()
            condition = self.parse_condition()
            self.consume(")")
            return condition
        
        left = self.parse_expression()
        
        # Verificar operadores relacionais
        current = self.peek()
        if current.value in ["==", "!=", "<", "<=", ">", ">=", "="]:
            operator = self.advance().value
            right = self.parse_expression()
            return BinaryOperation(left, operator, right)
        
        return left
    
    def parse_expression(self) -> ASTNode:
        """Expression = Term { ArithOp Term }"""
        left = self.parse_term()
        
        while self.match(["+", "-"]):
            operator = self.advance().value
            right = self.parse_term()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        """Term = Factor { MulOp Factor }"""
        left = self.parse_factor()
        
        while self.match(["*", "/", "%"]):
            operator = self.advance().value
            right = self.parse_factor()
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def parse_factor(self) -> ASTNode:
        """Factor = Identifier | Literal | FuncCall | "(" Expression ")" | "[" ListLiteral "]" | IndexAccess"""
        current = self.peek()
        
        if current.type == "IDENTIFICADOR":
            name = self.advance().value
            
            # Verificar se é function call
            if self.match("("):
                self.advance()
                arguments = []
                if not self.match(")"):
                    arguments = self.parse_actual_params()
                self.consume(")")
                return FunctionCall(name, arguments)
            
            # Verificar se é index access
            elif self.match("["):
                self.advance()
                index = self.parse_expression()
                self.consume("]")
                return IndexAccess(Identifier(name), index)
            
            # Simples identifier
            return Identifier(name)
        
        elif current.type == "NUMERO_LITERAL":
            value = self.advance().value
            return Literal(float(value) if '.' in value else int(value), "numero")
        
        elif current.type == "STRING_LITERAL":
            value = self.advance().value
            return Literal(value, "texto")
        
        elif current.value in ["verdadeiro", "falso"]:
            value = self.advance().value
            return Literal(value == "verdadeiro", "logico")
        
        elif current.value == "(":
            self.advance()
            expr = self.parse_expression()
            self.consume(")")
            return expr
        
        elif current.value == "[":
            self.advance()
            elements = []
            if not self.match("]"):
                elements = self.parse_actual_params()
            self.consume("]")
            return ListLiteral(elements)
        
        elif current.value == "-":
            # Unary minus
            operator = self.advance().value
            operand = self.parse_factor()
            return UnaryOperation(operator, operand)
        
        else:
            raise ParseError(f"Fator inesperado: '{current.value}'")


def parse_brasilscript(code: str) -> Program:
    """Função de conveniência para fazer o parse de código BrasilScript"""
    # Tokenizar o código
    raw_tokens = tokenize_text(code)
    
    # Converter para objetos Token (filtrando whitespace e comentários)
    tokens = []
    for token_type, token_value in raw_tokens:
        if token_type not in ["WHITESPACE", "COMMENT", "NEWLINE"]:
            tokens.append(Token(token_type, token_value))
    
    # Adicionar token EOF
    tokens.append(Token("EOF", ""))
    
    # Fazer o parse
    parser = BrasilScriptParser(tokens)
    return parser.parse()


# Exemplo de uso
if __name__ == "__main__":
    code = '''
    declarar x como numero = 10
    declarar nome como texto
    nome = "BrasilScript"
    mostrar "Ola, " + nome
    
    se x > 5 entao
        mostrar "x e maior que 5"
    fim_se
    '''
    
    try:
        ast = parse_brasilscript(code)
        print("Parse realizado com sucesso!")
        print(f"AST: {ast}")
    except ParseError as e:
        print(f"Erro de sintaxe: {e}")
