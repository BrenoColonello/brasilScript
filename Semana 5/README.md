Semana 5 - Lexer
=================

Este diretório contém uma implementação simples de um analisador léxico (lexer)
para a linguagem BrasilScript.

Arquivos:

- `lexer.py`: implementação do lexer (classe `Lexer` e dataclass `Token`).
- `test_lexer.py`: pequenos testes de fumaça que verificam tokens básicos.

Como rodar:

1. Execute os testes rápidos com:

```bash
PYTHONPATH=. python3 Semana\ 5/test_lexer.py

Observações:

- O lexer ignora espaços em branco e comentários iniciados por `#`.
- Strings suportam sequências de escape simples (ex: `\n`, `\"`).
