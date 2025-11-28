"""
Uso:
    from codegen import CodeGen
    cg = CodeGen()
    module = cg.generate(program_ast)
    print(module)

Requer: llvmlite
    pip install llvmlite
"""
from llvmlite import ir
from typing import Dict


class CodeGen:
    def __init__(self):
        self.module = ir.Module(name="brasilscript")
        self.printf = None
        self.functions: Dict[str, ir.Function] = {}
        # mapeamento nome da função atual -> tabela de símbolos local (nome->alloca)
        self.locals = {}
        # auxiliar para gerar nomes de strings únicos
        self._str_count = 0

    # --- declarações de tempo de execução ---
    def declare_printf(self):
        if self.printf is None:
            voidptr_ty = ir.IntType(8).as_pointer()
            printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, printf_ty, name="printf")
        return self.printf

    def new_string_constant(self, value: str) -> ir.Constant:
        # cria uma constante global (string em C) e retorna char*
        name = f".str{self._str_count}"
        self._str_count += 1
        data = bytearray(value.encode("utf8")) + b"\x00"
        arr_ty = ir.ArrayType(ir.IntType(8), len(data))
        gvar = ir.GlobalVariable(self.module, arr_ty, name=name)
        gvar.global_constant = True
        gvar.initializer = ir.Constant(arr_ty, data)
        return gvar.bitcast(ir.IntType(8).as_pointer())

    # --- criação de módulo/função ---
    def declare_function_prototypes(self, program):
        # percorre declarações de função e cria protótipos (retorno double, parâmetros double)
        for stmt in program.statements:
            if type(stmt).__name__ == "FunctionDecl":
                param_count = len(stmt.parameters)
                func_ty = ir.FunctionType(ir.DoubleType(), [ir.DoubleType()] * param_count)
                fn = ir.Function(self.module, func_ty, name=stmt.name)
                # nomeia parâmetros
                for i, name in enumerate(stmt.parameters):
                    fn.args[i].name = name
                self.functions[stmt.name] = fn

    def generate(self, program):
        # declara printf
        self.declare_printf()
        # declara protótipos
        self.declare_function_prototypes(program)
        # gera corpos das funções
        for stmt in program.statements:
            if type(stmt).__name__ == "FunctionDecl":
                self.gen_function(stmt)
        # gera função main que executa statements de nível superior
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main_fn = ir.Function(self.module, main_ty, name="main")
        block = main_fn.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        # configura tabela de locais (variáveis) para main
        self.locals = {}
        self._builder = builder
        for stmt in program.statements:
            if type(stmt).__name__ != "FunctionDecl":
                self.gen_statement(stmt)
        builder.ret(ir.Constant(ir.IntType(32), 0))
        return self.module

    # --- auxiliares para gerenciar variáveis locais ---
    def alloc_local(self, name: str):
        # aloca na entrada da função atual
        builder = self._builder
        ptr = builder.alloca(ir.DoubleType(), name=name)
        self.locals[name] = ptr
        return ptr

    def get_local(self, name: str):
        return self.locals.get(name)

    # --- geração de código para statements ---
    def gen_statement(self, stmt):
        kind = type(stmt).__name__
        if kind == "Declaration":
            self.gen_declaration(stmt)
        elif kind == "Assignment":
            self.gen_assignment(stmt)
        elif kind == "PrintStatement":
            self.gen_print(stmt)
        elif kind == "IfStatement":
            self.gen_if(stmt)
        elif kind == "WhileStatement":
            self.gen_while(stmt)
        elif kind == "RepeatStatement":
            self.gen_repeat(stmt)
        elif kind == "ReturnStatement":
            # return válido apenas dentro de funções - ignorar no nível do módulo
            pass
        else:
            # statements não suportados: ForEach, FunctionCall no nível superior
            if kind == "FunctionCall":
                self.gen_function_call(stmt)
            else:
                # ignorar outros statements por enquanto
                pass

    def gen_declaration(self, decl):
        ptr = self.alloc_local(decl.identifier)
        if decl.initial_value is not None:
            val = self.gen_expr(decl.initial_value)
            # tenta armazenar double
            if val.type == ir.DoubleType():
                self._builder.store(val, ptr)
            else:
                # tenta converter i1 para double
                if isinstance(val.type, ir.IntType) and val.type.width == 1:
                    conv = self._builder.uitofp(val, ir.DoubleType())
                    self._builder.store(conv, ptr)
                else:
                    # tipo não suportado, armazena 0.0
                    self._builder.store(ir.Constant(ir.DoubleType(), 0.0), ptr)

    def gen_assignment(self, stmt):
        ptr = self.get_local(stmt.identifier)
        if ptr is None:
            ptr = self.alloc_local(stmt.identifier)
        val = self.gen_expr(stmt.value)
        if val.type == ir.DoubleType():
            self._builder.store(val, ptr)
        else:
            if isinstance(val.type, ir.IntType) and val.type.width == 1:
                conv = self._builder.uitofp(val, ir.DoubleType())
                self._builder.store(conv, ptr)
            else:
                # não suportado - armazena 0
                self._builder.store(ir.Constant(ir.DoubleType(), 0.0), ptr)

    def gen_print(self, stmt):
        printf = self.declare_printf()
        for expr in stmt.expressions:
            # se for um literal texto
            from parser.ast import Literal
            if isinstance(expr, Literal) and expr.type == "texto":
                ptr = self.new_string_constant(expr.value)
                fmt = ptr
                # chama printf com string única
                self._builder.call(printf, [fmt])
            else:
                # tratar como número
                val = self.gen_expr(expr)
                # cria string de formato "%f\n"
                fmtptr = self.new_string_constant("%f\n")
                self._builder.call(printf, [fmtptr, val])

    # --- expressões ---
    def gen_expr(self, node):
        from parser.ast import Literal, Identifier, BinaryOperation, UnaryOperation, FunctionCall
        if isinstance(node, Literal):
            if node.type == "numero":
                return ir.Constant(ir.DoubleType(), float(node.value))
            if node.type == "texto":
                return self.new_string_constant(node.value)
            if node.type == "logico":
                return ir.Constant(ir.IntType(1), 1 if node.value else 0)
            # fallback / caso padrão
            return ir.Constant(ir.DoubleType(), 0.0)
        if isinstance(node, Identifier):
            ptr = self.get_local(node.name)
            if ptr is None:
                # inicializa implicitamente com zero
                ptr = self.alloc_local(node.name)
                self._builder.store(ir.Constant(ir.DoubleType(), 0.0), ptr)
            return self._builder.load(ptr)
        if isinstance(node, UnaryOperation):
            op = node.operator
            val = self.gen_expr(node.operand)
            if op == "-":
                return self._builder.fsub(ir.Constant(ir.DoubleType(), 0.0), val)
            if op == "nao":
                # not lógico: assume operando é i1 ou conversível
                if isinstance(val.type, ir.IntType) and val.type.width == 1:
                    return self._builder.not_(val)
                else:
                    # compara com zero
                    cmp = self._builder.fcmp_ordered('==', val, ir.Constant(ir.DoubleType(), 0.0))
                    return cmp
        if isinstance(node, BinaryOperation):
            l = self.gen_expr(node.left)
            r = self.gen_expr(node.right)
            op = node.operator
            if op == "+":
                return self._builder.fadd(l, r)
            if op == "-":
                return self._builder.fsub(l, r)
            if op == "*":
                return self._builder.fmul(l, r)
            if op == "/":
                return self._builder.fdiv(l, r)
            if op in ("==", "!=", "<", "<=", ">", ">="):
                if op == "==":
                    cmp = self._builder.fcmp_ordered('==', l, r)
                elif op == "!=":
                    cmp = self._builder.fcmp_ordered('!=', l, r)
                elif op == "<":
                    cmp = self._builder.fcmp_ordered('<', l, r)
                elif op == "<=":
                    cmp = self._builder.fcmp_ordered('<=', l, r)
                elif op == ">":
                    cmp = self._builder.fcmp_ordered('>', l, r)
                else:
                    cmp = self._builder.fcmp_ordered('>=', l, r)
                # retorna i1
                return cmp
            # fallback / padrão
            return l
        if isinstance(node, FunctionCall):
            fn = self.functions.get(node.name)
            if fn is None:
                # função desconhecida - retorna 0.0
                return ir.Constant(ir.DoubleType(), 0.0)
            args = [self._coerce_to_double(self.gen_expr(a)) for a in node.arguments]
            return self._builder.call(fn, args)
        # padrão
        return ir.Constant(ir.DoubleType(), 0.0)

    def _coerce_to_double(self, val):
        if val.type == ir.DoubleType():
            return val
        if isinstance(val.type, ir.IntType) and val.type.width == 1:
            return self._builder.uitofp(val, ir.DoubleType())
        return val

    # --- fluxo de controle ---
    def gen_if(self, stmt):
        condv = self.gen_expr(stmt.condition)
        # garante i1
        if isinstance(condv.type, ir.DoubleType):
            cond = self._builder.fcmp_ordered('!=', condv, ir.Constant(ir.DoubleType(), 0.0))
        else:
            cond = condv
        then_bb = self._builder.append_basic_block('then')
        else_bb = self._builder.append_basic_block('else')
        end_bb = self._builder.append_basic_block('ifend')
        self._builder.cbranch(cond, then_bb, else_bb)
        # then
        self._builder.position_at_end(then_bb)
        for s in stmt.then_block:
            self.gen_statement(s)
        self._builder.branch(end_bb)
        # else/elseifs
        self._builder.position_at_end(else_bb)
        # trata apenas o primeiro else_if por simplicidade
        if stmt.else_ifs:
            # apenas trata o primeiro else_if
            cond2, block2 = stmt.else_ifs[0]
            for s in block2:
                self.gen_statement(s)
        if stmt.else_block:
            for s in stmt.else_block:
                self.gen_statement(s)
        self._builder.branch(end_bb)
        self._builder.position_at_end(end_bb)

    def gen_while(self, stmt):
        loop_bb = self._builder.append_basic_block('loop')
        after_bb = self._builder.append_basic_block('loopend')
        # branch inicial
        self._builder.branch(loop_bb)
        self._builder.position_at_end(loop_bb)
        condv = self.gen_expr(stmt.condition)
        if isinstance(condv.type, ir.DoubleType):
            cond = self._builder.fcmp_ordered('!=', condv, ir.Constant(ir.DoubleType(), 0.0))
        else:
            cond = condv
        # corpo
        for s in stmt.body:
            self.gen_statement(s)
        # reavalia e faz branch
        self._builder.cbranch(cond, loop_bb, after_bb)
        self._builder.position_at_end(after_bb)

    def gen_repeat(self, stmt):
        # repeat N vezes -> traduz para loop com contador simples
        cnt = self.gen_expr(stmt.count)
        # coerção para int por truncamento
        if isinstance(cnt.type, ir.DoubleType):
            n_int = self._builder.fptoui(cnt, ir.IntType(32))
        else:
            n_int = cnt
        # aloca contador
        cptr = self._builder.alloca(ir.IntType(32), name='rep_cnt')
        self._builder.store(ir.Constant(ir.IntType(32), 0), cptr)
        loop_bb = self._builder.append_basic_block('reploop')
        end_bb = self._builder.append_basic_block('repend')
        self._builder.branch(loop_bb)
        self._builder.position_at_end(loop_bb)
        cur = self._builder.load(cptr)
        cmp = self._builder.icmp_unsigned('<', cur, n_int)
        self._builder.cbranch(cmp, loop_bb.append_basic_block('repl_body'), end_bb)
        # ajuste de posição do corpo
        body_bb = loop_bb.get_next_block()
        self._builder.position_at_end(body_bb)
        for s in stmt.body:
            self.gen_statement(s)
        # incremento
        cur2 = self._builder.add(cur, ir.Constant(ir.IntType(32), 1))
        self._builder.store(cur2, cptr)
        self._builder.branch(loop_bb)
        self._builder.position_at_end(end_bb)

    # --- funções ---
    def gen_function(self, fdecl):
        fn = self.functions.get(fdecl.name)
        if fn is None:
            return
        block = fn.append_basic_block('entry')
        builder = ir.IRBuilder(block)
        # salva builder e tabela de locais
        prev_builder = getattr(self, '_builder', None)
        prev_locals = self.locals
        self._builder = builder
        self.locals = {}
        # argumentos de entrada
        for arg in fn.args:
            # aloca local e armazena argumento
            ptr = builder.alloca(ir.DoubleType(), name=arg.name)
            builder.store(arg, ptr)
            self.locals[arg.name] = ptr
        # gera corpo
        ret_val = None
        for s in fdecl.body:
            if type(s).__name__ == 'ReturnStatement':
                if s.value is not None:
                    rv = self.gen_expr(s.value)
                    rv = self._coerce_to_double(rv)
                    builder.ret(rv)
                    ret_val = True
                else:
                    builder.ret(ir.Constant(ir.DoubleType(), 0.0))
                    ret_val = True
                break
            else:
                self.gen_statement(s)
        if not ret_val:
            # garante que a função retorne algo
            builder.ret(ir.Constant(ir.DoubleType(), 0.0))
        # restaura
        self._builder = prev_builder
        self.locals = prev_locals

    def gen_function_call(self, callnode):
        # permite chamada de função como statement
        fn = self.functions.get(callnode.name)
        if fn is None:
            return None
        args = [self._coerce_to_double(self.gen_expr(a)) for a in callnode.arguments]
        return self._builder.call(fn, args)

    def _coerce_to_double(self, val):
        if val.type == ir.DoubleType():
            return val
        if isinstance(val.type, ir.IntType) and val.type.width == 1:
            return self._builder.uitofp(val, ir.DoubleType())
        return val
