# Gramática resumida — BrasilScript (exemplos)

Este documento reúne as palavras-chave, os tipos de tokens e exemplos de uso da linguagem BrasilScript, conforme implementado no repositório.

## Palavras-chave

- declarar, como
- mostrar
- perguntar, guardar_em
- se, entao, senao_se, senao, fim_se
- enquanto, faca, fim_enquanto
- repetir, vezes, fim_repetir
- para_cada, em, fim_para_cada
- funcao, fim_funcao, retornar
- parar
- e, ou, nao
- lista, texto, numero, logico

## Tokens principais

- IDENTIFICADOR: nomes de variáveis/funções (ex.: `x`, `MeuNome`)
- NUMERO_LITERAL: números (inteiros, decimais, notação científica)
- STRING_LITERAL: texto entre aspas duplas "..." ou simples '...'
- LOGICO_LITERAL: `verdadeiro` / `falso`
- OP: operadores aritméticos e relacionais (`+ - * / % == != < <= > >= =`)
- Delimitadores: `(` `)` `[` `]` `{` `}` `,` `;` `:` `.`
- Comentários: iniciam com `#` até o fim da linha

## Tipos primitivos

- numero  — números (int/float)
- texto   — strings
- logico  — booleanos
- lista[T] — listas de elementos do tipo T (ex.: `lista[numero]`)

## Regras e exemplos

### Declaração de variável
```
declarar preco como numero
declarar nomes como lista[texto]
```
Também é possível inicializar:
```
declarar x como numero = 10
declarar saudacao como texto = "Ola"
```

Se a inicialização for incompatível com o tipo declarado, o analisador semântico reporta erro:
`Incompatibilidade de tipos na inicialização de 'x': declarado numero, inicializado com texto`.

### Atribuição
```
preco = 19.99
nome = "BrasilScript"
lista[0] = 5  # acesso por índice
```
Erros:
- Variável não declarada -> `Identificador não declarado: 'a' na atribuição`
- Tipo incompatível -> `Incompatibilidade de tipos na atribuição para 'nome': esperado numero, obtido texto`

### Impressão
```
mostrar "Ola, mundo!"
mostrar "Preco final: " + preco
mostrar a, b, c  # múltiplas expressões separadas por vírgula
```

### Entrada do usuário
```
perguntar "Qual seu nome?" guardar_em nome
```
- Se a variável não existir, o analisador semântico aponta `Identificador não declarado`.

### Estruturas de controle

If / Else:
```
se x > 0 entao
  mostrar "positivo"
senao
  mostrar "nao positivo"
fim_se
```

While:
```
enquanto preco < 25 faca
  mostrar preco
  preco = preco + 1.0
fim_enquanto
```

Repeat:
```
repetir 5 vezes
  mostrar "oi"
fim_repetir
```

For-each:
```
para_cada item em minha_lista faca
  mostrar item
fim_para_cada
```

### Funções

Declaração e retorno:
```
funcao soma(a, b)
  retornar a + b
fim_funcao
```

Chamada:
```
resultado = soma(3, 4)
mostrar resultado
```

### Expressões e operadores
- A ordem de precedência segue: unário (`-`), multiplicação/divisão (`* / %`), adição/subtração (`+ -`), comparações e operadores lógicos (`== != < > <= >=`, `e`, `ou`).
- `+` também concatena strings quando ambos operandos são `texto`.

### Listas e indexação
```
declarar numeros como lista[numero] = [1, 2, 3]
mostrar numeros[0]
```
- Índice deve ser `numero`.
- Acesso a não-lista gera erro semântico: `Acesso por índice em tipo não-lista: ...`.

## Comentários
Qualquer texto após `#` na mesma linha é um comentário.

## Erros léxicos / sintáticos
- Caracteres inesperados no lexer geram erro (ex.: caractere acentuado ou símbolo inválido) — o parser/runner reportará `token invalido, digite da forma correta` com detalhes do lexer.
- Sintaxe inesperada: o parser coleta erros de parse não-fatais e tenta montar uma AST parcial; o runner pode imprimir esses erros junto com a AST usando a flag `--print-ast`.

## Exemplos completos

Exemplo 1 — Ola Mundo:
```
# Ola mundo
mostrar "Ola, mundo!"
```

Exemplo 2 — Laço e acumulador:
```
declarar preco como numero = 19.99
enquanto preco < 25 faca
  mostrar preco
  preco = preco + 1.0
fim_enquanto
mostrar "Preco final: " + preco
```

Exemplo 3 — Função e chamada:
```
funcao dobro(x)
  retornar x * 2
fim_funcao

declarar n como numero = 5
mostrar dobro(n)
```

## Notas finais
- Para testar um arquivo e ver AST + erros: execute

```
PYTHONPATH=. python3 run_parser.py --print-ast exemplos/hello_world.bs
```

- Mensagens semânticas e de tipo são emitidas pelo `parser/semantic.py`.

Se quiser, eu posso gerar um arquivo adicional com exemplos de teste (vários `.bs`) ou converter este documento para `docs/GRAMATICA.md`. Quer que eu também coloque este arquivo em `docs/`?"
