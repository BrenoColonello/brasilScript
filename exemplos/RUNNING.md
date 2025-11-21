# Como executar o projeto BrasilScript (guia rápido)

Este documento mostra comandos e exemplos práticos para executar o parser, gerar AST, rodar checagem semântica e gerar/compilar LLVM IR a partir dos exemplos em `exemplos/`.

Requisitos
- Python 3.8+
- (Opcional, para gerar/executar LLVM) clang/llvm-as no PATH
- (Opcional para geração via llvmlite) pip install llvmlite

Executar o runner (parser + semântica)
Do diretório raiz do repositório (onde está o `run_parser.py`) execute:

- Analisar um arquivo (obrigatório informar arquivo ou nome presente em `exemplos/`):

  PYTHONPATH=. python3 run_parser.py exemplos/hello_world.bs

- Imprimir AST (antes da análise semântica):

  PYTHONPATH=. python3 run_parser.py --print-ast exemplos/hello_world.bs

- Gerar LLVM IR (arquivo `.ll`) e tentar compilar/executar com clang/llvm-as se disponíveis:

  PYTHONPATH=. python3 run_parser.py --emit-llvm --run exemplos/funcoes.bs

  Comportamento:
  - Gera `<arquivo>.ll` no diretório atual (por exemplo `funcoes.ll`).
  - Se `clang` estiver instalado, tentará compilar o `.ll` para um executável com o mesmo nome (por exemplo `funcoes`).
  - Se `--run` for passado, o runner tentará executar o binário gerado.
  - Se `llvm-as` estiver instalado, criará também `<arquivo>.bc`.

Uso com nomes curtos dos exemplos
- Você pode passar só o nome do arquivo se ele estiver em `exemplos/` ou `exemplos/erros/`:

  PYTHONPATH=. python3 run_parser.py --print-ast soma.bs

Inspecionar AST via one-liner (alternativa)

PYTHONPATH=. python3 - <<'PY'
from parser.brasilscript_parser import parse_brasilscript
from pprint import pprint
code = open('exemplos/hello_world.bs', 'r', encoding='utf-8').read()
ast = parse_brasilscript(code)
pprint(ast)
print('statements:', len(ast.statements))
PY

Executar testes / ferramentas auxiliares
- Rodar testes rápidos do lexer (Semana 6, se existir):

  PYTHONPATH=. python3 run_semana6_tests.py

- Debug do lexer + parser (script de exemplo):

  PYTHONPATH=. python3 parser/debug_lexer_parser.py

Erros léxicos / sintáticos
- O lexer agora reporta mensagens mais completas com posição (linha/coluna) e trecho com `^` apontando.
- O parser coleta erros não-fatais e o runner pode mostrar esses erros com `--print-ast`.
- Para erros semânticos (tipos, identificadores não-declarados) o runner imprime mensagens detalhadas.

Dependências comuns
- Instale llvmlite (se for gerar IR via Python):

  pip install llvmlite

- clang / llvm-as: instale via gerenciador do seu sistema (ex.: `dnf install clang llvm` no Fedora / `apt install clang llvm` no Debian/Ubuntu).


