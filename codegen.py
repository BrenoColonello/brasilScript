"""
Usage:
    from codegen import CodeGen
    cg = CodeGen()
    module = cg.generate(program_ast)
    print(module)

Requires: llvmlite
    pip install llvmlite
"""
from llvmlite import ir
from typing import Dict


class CodeGen:
    def __init__(self):
        self.module = ir.Module(name="brasilscript")
        self.printf = None
        self.functions: Dict[str, ir.Function] = {}
        # mapping current function name -> local symbol table (name->alloca)
        self.locals = {}
        # helper for generating unique string names
        self._str_count = 0

    # --- runtime declarations ---
    def declare_printf(self):
        if self.printf is None:
            voidptr_ty = ir.IntType(8).as_pointer()
            printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            self.printf = ir.Function(self.module, printf_ty, name="printf")
        return self.printf

    def new_string_constant(self, value: str) -> ir.Constant:
        # create a global constant C string and return char*
        name = f".str{self._str_count}"
        self._str_count += 1
        data = bytearray(value.encode("utf8")) + b"\x00"
        arr_ty = ir.ArrayType(ir.IntType(8), len(data))
        gvar = ir.GlobalVariable(self.module, arr_ty, name=name)
        gvar.global_constant = True
        gvar.initializer = ir.Constant(arr_ty, data)
        return gvar.bitcast(ir.IntType(8).as_pointer())

    # --- module/function creation ---
    def declare_function_prototypes(self, program):
        # scan function decls and create prototypes (return double, params double)
        for stmt in program.statements:
            if type(stmt).__name__ == "FunctionDecl":
                param_count = len(stmt.parameters)
                func_ty = ir.FunctionType(ir.DoubleType(), [ir.DoubleType()] * param_count)
                fn = ir.Function(self.module, func_ty, name=stmt.name)
                # name parameters
                for i, name in enumerate(stmt.parameters):
                    fn.args[i].name = name
                self.functions[stmt.name] = fn

    def generate(self, program):
        # declare printf
        self.declare_printf()
        # declare prototypes
        self.declare_function_prototypes(program)
        # generate functions bodies
        for stmt in program.statements:
            if type(stmt).__name__ == "FunctionDecl":
                self.gen_function(stmt)
        # generate main function that executes top-level statements
        main_ty = ir.FunctionType(ir.IntType(32), [])
        main_fn = ir.Function(self.module, main_ty, name="main")
        block = main_fn.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        # setup locals table for main
        self.locals = {}
        self._builder = builder
        for stmt in program.statements:
            if type(stmt).__name__ != "FunctionDecl":
                self.gen_statement(stmt)
        builder.ret(ir.Constant(ir.IntType(32), 0))
        return self.module

    # --- helpers to manage locals ---
    def alloc_local(self, name: str):
        # allocate in current function entry
        builder = self._builder
        ptr = builder.alloca(ir.DoubleType(), name=name)
        self.locals[name] = ptr
        return ptr

    def get_local(self, name: str):
        return self.locals.get(name)

    # --- code generation for statements ---
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
            # return only valid inside functions - ignore at module level
            pass
        else:
            # unsupported statements: ForEach, FunctionCall at top-level
            if kind == "FunctionCall":
                self.gen_function_call(stmt)
            else:
                # ignore other statements for now
                pass

    def gen_declaration(self, decl):
        ptr = self.alloc_local(decl.identifier)
        if decl.initial_value is not None:
            val = self.gen_expr(decl.initial_value)
            # attempt to store double
            if val.type == ir.DoubleType():
                self._builder.store(val, ptr)
            else:
                # try to convert i1 to double
                if isinstance(val.type, ir.IntType) and val.type.width == 1:
                    conv = self._builder.uitofp(val, ir.DoubleType())
                    self._builder.store(conv, ptr)
                else:
                    # unsupported type, store 0.0
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
                # unsupported - store 0
                self._builder.store(ir.Constant(ir.DoubleType(), 0.0), ptr)

    def gen_print(self, stmt):
        printf = self.declare_printf()
        for expr in stmt.expressions:
            # if it's a literal texto
            from parser.ast import Literal
            if isinstance(expr, Literal) and expr.type == "texto":
                ptr = self.new_string_constant(expr.value)
                fmt = ptr
                # call printf with single string
                self._builder.call(printf, [fmt])
            else:
                # treat as number
                val = self.gen_expr(expr)
                # create format string "%f\n"
                fmtptr = self.new_string_constant("%f\n")
                self._builder.call(printf, [fmtptr, val])

    # --- expressions ---
    def gen_expr(self, node):
        from parser.ast import Literal, Identifier, BinaryOperation, UnaryOperation, FunctionCall
        if isinstance(node, Literal):
            if node.type == "numero":
                return ir.Constant(ir.DoubleType(), float(node.value))
            if node.type == "texto":
                return self.new_string_constant(node.value)
            if node.type == "logico":
                return ir.Constant(ir.IntType(1), 1 if node.value else 0)
            # fallback
            return ir.Constant(ir.DoubleType(), 0.0)
        if isinstance(node, Identifier):
            ptr = self.get_local(node.name)
            if ptr is None:
                # implicit zero-initialized
                ptr = self.alloc_local(node.name)
                self._builder.store(ir.Constant(ir.DoubleType(), 0.0), ptr)
            return self._builder.load(ptr)
        if isinstance(node, UnaryOperation):
            op = node.operator
            val = self.gen_expr(node.operand)
            if op == "-":
                return self._builder.fsub(ir.Constant(ir.DoubleType(), 0.0), val)
            if op == "nao":
                # logical not: assume operand is i1 or convertible
                if isinstance(val.type, ir.IntType) and val.type.width == 1:
                    return self._builder.not_(val)
                else:
                    # compare to zero
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
                # return i1
                return cmp
            # fallback
            return l
        if isinstance(node, FunctionCall):
            fn = self.functions.get(node.name)
            if fn is None:
                # unknown function - return 0.0
                return ir.Constant(ir.DoubleType(), 0.0)
            args = [self._coerce_to_double(self.gen_expr(a)) for a in node.arguments]
            return self._builder.call(fn, args)
        # default
        return ir.Constant(ir.DoubleType(), 0.0)

    def _coerce_to_double(self, val):
        if val.type == ir.DoubleType():
            return val
        if isinstance(val.type, ir.IntType) and val.type.width == 1:
            return self._builder.uitofp(val, ir.DoubleType())
        return val

    # --- control flow ---
    def gen_if(self, stmt):
        condv = self.gen_expr(stmt.condition)
        # ensure i1
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
        # handle else_ifs sequentially by nesting (simple)
        if stmt.else_ifs:
            # only handle first else_if for simplicity
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
        # initial branch
        self._builder.branch(loop_bb)
        self._builder.position_at_end(loop_bb)
        condv = self.gen_expr(stmt.condition)
        if isinstance(condv.type, ir.DoubleType):
            cond = self._builder.fcmp_ordered('!=', condv, ir.Constant(ir.DoubleType(), 0.0))
        else:
            cond = condv
        # body
        for s in stmt.body:
            self.gen_statement(s)
        # re-evaluate and branch
        self._builder.cbranch(cond, loop_bb, after_bb)
        self._builder.position_at_end(after_bb)

    def gen_repeat(self, stmt):
        # repeat N times -> translate to a simple counter loop
        cnt = self.gen_expr(stmt.count)
        # coerce to int by truncating
        if isinstance(cnt.type, ir.DoubleType):
            n_int = self._builder.fptoui(cnt, ir.IntType(32))
        else:
            n_int = cnt
        # alloc counter
        cptr = self._builder.alloca(ir.IntType(32), name='rep_cnt')
        self._builder.store(ir.Constant(ir.IntType(32), 0), cptr)
        loop_bb = self._builder.append_basic_block('reploop')
        end_bb = self._builder.append_basic_block('repend')
        self._builder.branch(loop_bb)
        self._builder.position_at_end(loop_bb)
        cur = self._builder.load(cptr)
        cmp = self._builder.icmp_unsigned('<', cur, n_int)
        self._builder.cbranch(cmp, loop_bb.append_basic_block('repl_body'), end_bb)
        # body position fix
        body_bb = loop_bb.get_next_block()
        self._builder.position_at_end(body_bb)
        for s in stmt.body:
            self.gen_statement(s)
        # increment
        cur2 = self._builder.add(cur, ir.Constant(ir.IntType(32), 1))
        self._builder.store(cur2, cptr)
        self._builder.branch(loop_bb)
        self._builder.position_at_end(end_bb)

    # --- functions ---
    def gen_function(self, fdecl):
        fn = self.functions.get(fdecl.name)
        if fn is None:
            return
        block = fn.append_basic_block('entry')
        builder = ir.IRBuilder(block)
        # save builder and locals
        prev_builder = getattr(self, '_builder', None)
        prev_locals = self.locals
        self._builder = builder
        self.locals = {}
        # incoming arguments
        for arg in fn.args:
            # allocate local and store incoming
            ptr = builder.alloca(ir.DoubleType(), name=arg.name)
            builder.store(arg, ptr)
            self.locals[arg.name] = ptr
        # generate body
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
            # ensure function returns something
            builder.ret(ir.Constant(ir.DoubleType(), 0.0))
        # restore
        self._builder = prev_builder
        self.locals = prev_locals

    def gen_function_call(self, callnode):
        # allow calling functions as statements
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
