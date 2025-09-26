# Instruções: executar o analisador léxico (lexer)

Este documento mostra como executar o `lexer` localizado em `Semana 5/lexer.py` usando o exemplo `exemplos/calculadora.bs`.

Pré-requisito
- Python 3 instalado.

Executar o lexer em um arquivo

1. Abra um terminal na pasta do projeto ou use o caminho absoluto.
2. Execute:

```bash
cd "Semana 5"               # ou use o caminho completo da pasta
python3 lexer.py "../exemplos/calculadora.bs"
```

Também é possível enviar o conteúdo via stdin:

```bash
cat exemplos/calculadora.bs | python3 Semana\ 5/lexer.py
```

Formato de saída
- O lexer imprime tokens no formato: Token('TIPO', 'valor')
- Tokens comuns: `PALAVRA_CHAVE`, `IDENTIFICADOR`, `NUMERO_LITERAL`, `STRING_LITERAL`, `LOGICO_LITERAL`, `OP`, etc.
- Se o lexer encontrar um caractere inválido único (por exemplo `$`), ele interrompe e imprime um erro léxico.
- Se encontrar uma palavra que começa por dígito seguida de letras (ex.: `4F373bd9`), o lexer emite um token especial `IDENTIFICADOR_INVALIDO`. Cabe ao parser detectar esse token e reportar erro de identificação inválida.

Exemplos

1) Arquivo sem erros (tokens impressos):

- Comportamento esperado (exemplo simplificado):
```
Token('PALAVRA_CHAVE', 'mostrar')
Token('STRING_LITERAL', '"=== CALCULADORA SIMPLES ==="')
Token('PALAVRA_CHAVE', 'perguntar')
...
```

2) Arquivo contendo identificador inválido (começa com dígito)
- Se a última linha contiver `4F373bd9`, o lexer emitirá o token:
```
Token('IDENTIFICADOR_INVALIDO', '4F373bd9')
```
- Nesse caso, o lexer não lança erro automático; o parser deve checar `IDENTIFICADOR_INVALIDO` e emitir mensagem de erro apropriada (por exemplo: "Identificador inválido: 4F373bd9 — identificadores não podem começar com dígitos").

3) Arquivo contendo caractere inválido isolado
- Se a última linha contiver `$4373bd9` (o caractere `$` não é parte de qualquer token válido), o lexer interrompe com erro léxico. Exemplo de saída:

```
...tokens anteriores...
Erro léxico: Caractere inválido: '$'
```



Fim.
