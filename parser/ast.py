from dataclasses import dataclass
from typing import Any, List, Optional

# Nó raiz
@dataclass
class Program:
    statements: List[Any]

# Literais e identificadores
@dataclass
class Literal:
    value: Any
    type: str  # ex: 'numero', 'texto', 'logico'
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class Identifier:
    name: str
    line: Optional[int] = None
    column: Optional[int] = None

# Declarações e atribuições
@dataclass
class Declaration:
    identifier: str
    type_name: str
    initial_value: Optional[Any] = None
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class Assignment:
    identifier: str
    value: Any
    line: Optional[int] = None
    column: Optional[int] = None

# Operações
@dataclass
class BinaryOperation:
    left: Any
    operator: str
    right: Any
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class UnaryOperation:
    operator: str
    operand: Any
    line: Optional[int] = None
    column: Optional[int] = None

# Listas e acessos por índice
@dataclass
class ListLiteral:
    elements: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class IndexAccess:
    object: Any
    index: Any
    line: Optional[int] = None
    column: Optional[int] = None

# Funções e chamadas
@dataclass
class FunctionDecl:
    name: str
    parameters: List[str]
    body: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class FunctionCall:
    name: str
    arguments: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

# Controle de fluxo
@dataclass
class IfStatement:
    condition: Any
    then_block: List[Any]
    else_ifs: List[tuple]  # lista de (condition, block)
    else_block: Optional[List[Any]] = None
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class WhileStatement:
    condition: Any
    body: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class ForEachStatement:
    variable: str
    iterable: Any
    body: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class RepeatStatement:
    count: Any
    body: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class ReturnStatement:
    value: Optional[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class PrintStatement:
    expressions: List[Any]
    line: Optional[int] = None
    column: Optional[int] = None

@dataclass
class InputStatement:
    variable: str
    prompt: Optional[Any] = None
    line: Optional[int] = None
    column: Optional[int] = None

# Exporte explícito
__all__ = [
    "Program", "Literal", "Identifier", "Declaration", "Assignment",
    "BinaryOperation", "UnaryOperation", "ListLiteral", "IndexAccess",
    "FunctionDecl", "FunctionCall", "IfStatement", "WhileStatement",
    "ForEachStatement", "RepeatStatement", "ReturnStatement", "PrintStatement",
    "InputStatement",
]
