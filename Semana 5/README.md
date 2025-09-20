Semana 5 - Lexer
=================

Este diretório contém uma implementação simples de um analisador léxico (lexer)
para a linguagem BrasilScript, baseada nas especificações presentes em
`Semana 2/SintaxeDaLinguagem.md` e `Semana 4/1_especificacao_expressoes_regulares.md`.

Arquivos:

- `lexer.py`: implementação do lexer (classe `Lexer` e dataclass `Token`).
- `test_lexer.py`: pequenos testes de fumaça que verificam tokens básicos.

Como rodar:

1. Execute os testes rápidos com:

```bash
PYTHONPATH=. python3 Semana\ 5/test_lexer.py
```

2. Use o lexer de forma programática:

```python
from Semana_5.lexer import Lexer
src = 'declarar x como numero\nx = 10\n'
tokens = list(Lexer(src).tokenize())
for t in tokens:
    print(t)
```

Observações:

- O lexer ignora espaços em branco e comentários iniciados por `#`.
- Strings suportam sequências de escape simples (ex: `\n`, `\"`).
