"""
Uso:
    from parser.brasilscript_parser import parse_brasilscript
    from parser.semantic import SemanticAnalyzer
    ast = parse_brasilscript(code)
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    if errors:
        for e in errors:
            print(e)
    else:
        print("Análise semântica: OK")
"""
from typing import List, Dict, Optional
from parser.brasilscript_parser import (
    Program,
    Declaration,
    Assignment,
    Literal,
    Identifier,
    BinaryOperation,
    UnaryOperation,
    ListLiteral,
    IndexAccess,
    FunctionDecl,
    FunctionCall,
    IfStatement,
    WhileStatement,
    ForEachStatement,
    RepeatStatement,
    ReturnStatement,
    PrintStatement,
    InputStatement,
)

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        # tabela de símbolos: nome -> tipo (ex.: 'numero', 'texto', 'logico', 'lista[numero]')
        self.symbols: Dict[str, str] = {}
        self.errors: List[str] = []

    def analyze(self, program: Program) -> List[str]:
        self.symbols.clear()
        self.errors.clear()

        for stmt in program.statements:
            self._check_statement(stmt)

        return self.errors

    # ---------- checagem de statements ----------
    def _check_statement(self, stmt):
        if isinstance(stmt, Declaration):
            self._check_declaration(stmt)
        elif isinstance(stmt, Assignment):
            self._check_assignment(stmt)
        elif isinstance(stmt, FunctionDecl):
            # comportamento mínimo: registrar nome da função (sem suporte a assinatura)
            if stmt.name in self.symbols:
                self.errors.append(f"Redeclaração: função '{stmt.name}' já declarada como variável")
            else:
                self.symbols[stmt.name] = 'funcao'
            # verificação do corpo em um novo escopo (temporário) foi omitida por simplicidade
        elif isinstance(stmt, IfStatement):
            self._infer_type(stmt.condition)
            for s in stmt.then_block:
                self._check_statement(s)
            for (_, block) in stmt.else_ifs:
                for s in block:
                    self._check_statement(s)
            if stmt.else_block:
                for s in stmt.else_block:
                    self._check_statement(s)
        elif isinstance(stmt, WhileStatement):
            self._infer_type(stmt.condition)
            for s in stmt.body:
                self._check_statement(s)
        elif isinstance(stmt, ForEachStatement):
            self._infer_type(stmt.iterable)
            # não inferimos o tipo da variável do laço aqui; mantemos simples
            for s in stmt.body:
                self._check_statement(s)
        elif isinstance(stmt, RepeatStatement):
            self._infer_type(stmt.count)
            for s in stmt.body:
                self._check_statement(s)
        elif isinstance(stmt, PrintStatement):
            for expr in stmt.expressions:
                self._infer_type(expr)
        elif isinstance(stmt, InputStatement):
            # prompt pode ser uma expressão
            self._infer_type(stmt.prompt)
            # a variável deve existir, não fazemos auto-declaração aqui
            if stmt.variable not in self.symbols:
                self.errors.append(f"Identificador não declarado: '{stmt.variable}' usado em 'perguntar'")
        elif isinstance(stmt, ReturnStatement):
            if stmt.value is not None:
                self._infer_type(stmt.value)
        elif stmt is None:
            return
        else:
            # tipos de statements desconhecidos - ser tolerante
            pass

    def _check_declaration(self, decl: Declaration):
        if decl.identifier in self.symbols:
            self.errors.append(f"Redeclaração: identificador '{decl.identifier}' já declarado")
            return

        declared_type = decl.type_name
        # registrar símbolo primeiro para permitir usos recursivos (comportamento simples)
        self.symbols[decl.identifier] = declared_type

        if decl.initial_value is not None:
            inferred = self._infer_type(decl.initial_value)
            if inferred is None:
                # erro já registrado
                return
            if not self._compatible(declared_type, inferred):
                self.errors.append(
                    f"Incompatibilidade de tipos na inicialização de '{decl.identifier}': declarado {declared_type}, inicializado com {inferred}"
                )

    def _check_assignment(self, assign: Assignment):
        if assign.identifier not in self.symbols:
            self.errors.append(f"Identificador não declarado: '{assign.identifier}' na atribuição")
            return

        expected = self.symbols[assign.identifier]
        inferred = self._infer_type(assign.value)
        if inferred is None:
            return
        if not self._compatible(expected, inferred):
            self.errors.append(
                f"Incompatibilidade de tipos na atribuição para '{assign.identifier}': esperado {expected}, obtido {inferred}"
            )

    # ---------- inferência de tipos ----------
    def _infer_type(self, node) -> Optional[str]:
        try:
            if isinstance(node, Literal):
                return node.type

            if isinstance(node, Identifier):
                if node.name not in self.symbols:
                    self.errors.append(f"Identificador não declarado: '{node.name}'")
                    return None
                return self.symbols[node.name]

            if isinstance(node, ListLiteral):
                # inferir tipo dos elementos
                if not node.elements:
                    return "lista[any]"  # lista vazia - flexível
                elem_types = [self._infer_type(e) for e in node.elements]
                if any(t is None for t in elem_types):
                    return None
                first = elem_types[0]
                for t in elem_types[1:]:
                    if t != first:
                        self.errors.append(f"Elementos de lista com tipos mistos: {elem_types}")
                        return None
                return f"lista[{first}]"

            if isinstance(node, IndexAccess):
                obj_type = self._infer_type(node.object)
                idx_type = self._infer_type(node.index)
                if obj_type is None or idx_type is None:
                    return None
                if not obj_type.startswith("lista"):
                    self.errors.append(f"Acesso por índice em tipo não-lista: {obj_type}")
                    return None
                if idx_type != "numero":
                    self.errors.append(f"Índice de lista deve ser 'numero', encontrado {idx_type}")
                    return None
                # extrair tipo do elemento de lista[T]
                if obj_type == "lista[any]":
                    return "any"
                if obj_type.startswith("lista[") and obj_type.endswith("]"):
                    return obj_type[6:-1]
                return None

            if isinstance(node, UnaryOperation):
                op = node.operator
                operand_type = self._infer_type(node.operand)
                if operand_type is None:
                    return None
                if op == "-":
                    if operand_type != "numero":
                        self.errors.append(f"Operador unário '-' aplicado a tipo não-numérico: {operand_type}")
                        return None
                    return "numero"
                if op == "nao":
                    if operand_type != "logico":
                        self.errors.append(f"Operador 'nao' aplicado a tipo não-lógico: {operand_type}")
                        return None
                    return "logico"
                return None

            if isinstance(node, BinaryOperation):
                left_t = self._infer_type(node.left)
                right_t = self._infer_type(node.right)
                if left_t is None or right_t is None:
                    return None
                op = node.operator

                # operadores lógicos
                if op in ("e", "ou"):
                    if left_t != "logico" or right_t != "logico":
                        self.errors.append(f"Operador lógico '{op}' requer operandos 'logico', encontrados {left_t} e {right_t}")
                        return None
                    return "logico"

                # operadores aritméticos
                if op in ("+", "-", "*", "/", "%"):
                    # '+' também pode concatenar texto
                    if op == "+":
                        if left_t == "texto" and right_t == "texto":
                            return "texto"
                        if left_t == "numero" and right_t == "numero":
                            return "numero"
                        self.errors.append(f"Operador '+' requisitos: ambos 'numero' ou ambos 'texto' - encontrados {left_t} e {right_t}")
                        return None
                    # outros operadores aritméticos requerem 'numero'
                    if left_t != "numero" or right_t != "numero":
                        self.errors.append(f"Operador '{op}' requer operandos 'numero', encontrados {left_t} e {right_t}")
                        return None
                    return "numero"

                # operadores relacionais
                if op in ("==", "!=", "<", "<=", ">", ">=", "="):
                    # permitir comparação entre mesmos tipos (listas também compatíveis por estrutura)
                    if left_t != right_t and not (left_t.startswith("lista") and right_t.startswith("lista")):
                        self.errors.append(f"Operador relacional '{op}' entre tipos incompatíveis: {left_t} e {right_t}")
                        return None
                    return "logico"

                # tratamento padrão
                return None

            if isinstance(node, FunctionCall):
                # sem informação de assinatura neste analisador simples
                # apenas garantir que a função existe e foi declarada como 'funcao'
                if node.name not in self.symbols:
                    self.errors.append(f"Chamada para função não declarada: '{node.name}'")
                    return None
                if self.symbols[node.name] != 'funcao':
                    self.errors.append(f"'{node.name}' não é uma função")
                    return None
                # tipo de retorno desconhecido
                return "any"

            # tratamento padrão para outros tipos de nó
            return None
        except Exception as e:
            self.errors.append(f"Erro interno na inferência de tipos: {e}")
            return None

    def _compatible(self, declared: str, inferred: str) -> bool:
        # igualdade exata
        if declared == inferred:
            return True
        # número: int/float são representados por 'numero'
        if declared == 'numero' and inferred == 'numero':
            return True
        # permitir atribuir lista[any] para lista[T] e vice-versa
        if declared.startswith('lista[') and inferred.startswith('lista['):
            d_inner = declared[6:-1]
            i_inner = inferred[6:-1]
            if d_inner == 'any' or i_inner == 'any' or d_inner == i_inner:
                return True
        # permitir atribuição quando houver 'any'
        if declared == 'any' or inferred == 'any':
            return True
        return False