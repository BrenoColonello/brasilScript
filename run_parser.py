#!/usr/bin/env python3
"""Runner simples: tokeniza, faz parse e análise semântica, exibindo mensagens amigáveis.

Uso:
    PYTHONPATH=. python3 run_parser.py exemplos/hello_world.bs
"""
import sys
from pathlib import Path

from parser.brasilscript_parser import parse_brasilscript, ParseError
from parser.semantic import SemanticAnalyzer
from pprint import pprint



def main(argv):
    # Support a --print-ast flag and accept either a path or a filename inside exemplos/
    examples_dir = Path("exemplos")
    print_ast = False
    # collect CLI args after program name
    cli_args = list(argv[1:])
    if '--print-ast' in cli_args:
        print_ast = True
        # remove all occurrences of the flag
        cli_args = [a for a in cli_args if a != '--print-ast']

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
                # show available examples to help the user
                if examples_dir.exists() and examples_dir.is_dir():
                    files = sorted([p.name for p in examples_dir.iterdir() if p.is_file() and p.suffix.lower() == ".bs"]) 
                    if files:
                        print("Arquivos disponíveis em exemplos/:")
                        for f in files:
                            print(" -", f)
                return 2
    else:
        print("Uso: PYTHONPATH=. python3 run_parser.py [--print-ast] <arquivo.bs>")
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
        # If user requested AST printing, show the error message and exit (no AST available)
        if print_ast:
            print('\nNenhum AST gerado devido a erro léxico crítico.')
        return 1
 
    # 2) Análise semântica (tipos, declarações, etc.)
    # If requested, print AST and any parse-time (non-fatal) errors collected by the parser
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
    # aqui você poderia seguir para geração de código / interpretação
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
