#!/usr/bin/env python3
"""Runner simples: tokeniza, faz parse e análise semântica, exibindo mensagens amigáveis.

Uso:
    PYTHONPATH=. python3 run_parser.py exemplos/hello_world.bs
"""
import sys
from pathlib import Path
import subprocess
import shutil

from parser.brasilscript_parser import parse_brasilscript, ParseError
from parser.semantic import SemanticAnalyzer
from pprint import pprint
from codegen import CodeGen



def main(argv):
    # Suporta flags: --print-ast, --emit-llvm e --run
    examples_dir = Path("exemplos")
    print_ast = False
    emit_llvm = False
    run_exec = False
    # coleta argumentos da linha de comando depois do nome do programa
    cli_args = list(argv[1:])
    if '--print-ast' in cli_args:
        print_ast = True
        cli_args = [a for a in cli_args if a != '--print-ast']
    if '--emit-llvm' in cli_args:
        emit_llvm = True
        cli_args = [a for a in cli_args if a != '--emit-llvm']
    if '--run' in cli_args:
        run_exec = True
        cli_args = [a for a in cli_args if a != '--run']

    if len(cli_args) >= 1:
        requested = Path(cli_args[0])
        if requested.exists():
            path = requested
        else:
            candidate = examples_dir / cli_args[0]
            candidate_bs = examples_dir / (cli_args[0] + '.bs') if not cli_args[0].lower().endswith('.bs') else candidate
            if candidate.exists():
                path = candidate
            elif candidate_bs.exists():
                path = candidate_bs
            else:
                print(f"Arquivo não encontrado: {requested}")
                # mostra exemplos disponíveis para ajudar o usuário
                if examples_dir.exists() and examples_dir.is_dir():
                    files = sorted([p.name for p in examples_dir.iterdir() if p.is_file() and p.suffix.lower() == ".bs"]) 
                    if files:
                        print("Arquivos disponíveis em exemplos/:")
                        for f in files:
                            print(" -", f)
                return 2
    else:
        print("Uso: PYTHONPATH=. python3 run_parser.py [--print-ast] [--emit-llvm] [--run] <arquivo.bs>")
        if examples_dir.exists() and examples_dir.is_dir():
            files = sorted([p.name for p in examples_dir.iterdir() if p.is_file() and p.suffix.lower() == ".bs"]) 
            if files:
                print("Arquivos disponíveis em exemplos/:")
                for f in files:
                    print(" -", f)
        return 2

    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return 2

    code = path.read_text(encoding="utf-8")

    # 1) Parse (captura erros léxicos/sintáticos)
    try:
        ast = parse_brasilscript(code)
    except ParseError as e:
        # Mensagem amigável já construída pelo parser
        print(f"Erro durante a análise: {e}")
        # Se o usuário solicitou imprimir o AST, mostra a mensagem de erro e sai (nenhum AST disponível)
        if print_ast:
            print('\nNenhum AST gerado devido a erro léxico crítico.')
        return 1
 
    # 2) Análise semântica (tipos, declarações, etc.)
    # Se solicitado, imprime o AST e quaisquer erros de parse (não fatais) coletados pelo parser
    if print_ast:
        print('\n--- AST ---')
        pprint(ast)
        if hasattr(ast, '_errors') and getattr(ast, '_errors'):
            print('\nErros encontrados durante o parse:')
            for err in getattr(ast, '_errors'):
                print(' -', err)
        else:
            print('\nNenhum erro de parse não-fatal registrado.')
        print('--- End AST ---\n')

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    if errors:
        print("Erros semânticos encontrados:")
        for err in errors:
            print(f" - {err}")
        return 3

    print("Compilação estática: OK (sem erros léxicos, sintáticos ou semânticos)")
    # emissão de LLVM IR
    if emit_llvm:
        try:
            cg = CodeGen()
            module = cg.generate(ast)
            out_name = Path(path).stem + '.ll'
            with open(out_name, 'w', encoding='utf-8') as f:
                f.write(str(module))
            print(f"LLVM IR escrito em: {out_name}")

            # Tenta compilar para executável nativo com clang, se disponível
            clang_path = shutil.which('clang')
            if clang_path:
                exe_name = Path(path).stem
                try:
                    print(f"Invocando clang para produzir executável: {exe_name}")
                    res = subprocess.run([clang_path, out_name, '-O2', '-o', exe_name], check=True, capture_output=True, text=True)
                    print(f"Executável gerado: {exe_name}")
                    if run_exec:
                        print(f"Executando: ./{exe_name}")
                        runp = subprocess.run([f"./{exe_name}"], shell=True)
                except subprocess.CalledProcessError as e:
                    print(f"clang falhou: {e.stderr}\n{e.stdout}")
            else:
                print("clang não encontrado no PATH; pulando compilação para executável.")

            # Tenta produzir bitcode LLVM com llvm-as, se disponível
            llvmas_path = shutil.which('llvm-as')
            if llvmas_path:
                bc_name = Path(path).stem + '.bc'
                try:
                    print(f"Invocando llvm-as para produzir bitcode: {bc_name}")
                    res = subprocess.run([llvmas_path, out_name, '-o', bc_name], check=True, capture_output=True, text=True)
                    print(f"Bitcode escrito: {bc_name}")
                except subprocess.CalledProcessError as e:
                    print(f"llvm-as falhou: {e.stderr}\n{e.stdout}")
            else:
                print("llvm-as não encontrado no PATH; pulando geração de bitcode.")

        except Exception as e:
            print(f"Erro ao gerar LLVM IR: {e}")
            return 4

    
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
