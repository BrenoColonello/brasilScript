# Autômatos Finitos (Mermaid) — BrasilScript Lexer

Este documento contém diagramas Mermaid dos autômatos finitos determinísticos (DFAs) que correspondem aos principais padrões de tokens do lexer BrasilScript (`Semana 5/lexer.py`).

Os diagramas foram construídos baseados nas expressões regulares reais usadas no código do lexer e seguem a ordem de prioridade definida em `token_specification`.

---

## 1. Comentários e Espaços em Branco

### Comentário: `#[^\r\n]*`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Comment : \#
    Comment --> Comment : qualquer exceto \\r \\n
    Comment --> [*] : \\r ou \\n ou EOF
```

### Espaço em Branco: `[ \t]+`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Whitespace : espaço ou tab
    Whitespace --> Whitespace : espaço ou tab
    Whitespace --> [*] : qualquer outro
```

## 2. Literais de String

### String com Aspas Duplas: `"(?:[^"\\]|\\.)*"`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> InString : "
    InString --> InString : char normal
    InString --> Escape : \\
    Escape --> InString : qualquer char
    InString --> Accept : "
    Accept --> [*]
```

### String com Aspas Simples: `'(?:[^'\\]|\\.)*'`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> InString : '
    InString --> InString : char normal
    InString --> Escape : \\
    Escape --> InString : qualquer char
    InString --> Accept : '
    Accept --> [*]
```

## 3. Números

### Número Literal: `\d+(?:\.\d+)?(?:[eE][+-]?\d+)?`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Integer : dígito
    Integer --> Integer : dígito
    Integer --> Dot : .
    Integer --> ExpStart : e ou E
    Integer --> [*] : fim
    
    Dot --> Decimal : dígito
    Decimal --> Decimal : dígito
    Decimal --> ExpStart : e ou E
    Decimal --> [*] : fim
    
    ExpStart --> ExpSign : + ou -
    ExpStart --> ExpDigits : dígito
    ExpSign --> ExpDigits : dígito
    ExpDigits --> [*] : fim
```

## 4. Literais Lógicos

### Booleanos: `\b(?:verdadeiro|falso)\b`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> V : v
    V --> VE : e
    VE --> VER : r
    VER --> VERD : d
    VERD --> VERDA : a
    VERDA --> VERDAD : d
    VERDAD --> VERDADE : e
    VERDADE --> VERDADEI : i
    VERDADEI --> VERDADEIR : r
    VERDADEIR --> VERDADEIRO : o
    VERDADEIRO --> [*] : boundary
    
    Start --> F : f
    F --> FA : a
    FA --> FAL : l
    FAL --> FALS : s
    FALS --> FALSO : o
    FALSO --> [*] : boundary
```

## 5. Palavras-Chave

### Keywords: Lista completa das palavras reservadas

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Keyword : palavra reservada
    Keyword --> [*] : boundary
    
    note right of Keyword : declarar, como, mostrar, perguntar, guardar_em, se, entao, senao, senao_se, fim_se, repetir, vezes, enquanto, faca, fim_enquanto, fim_repetir, funcao, fim_funcao, retornar, para_cada, em, fim_para_cada, parar, e, ou, nao, lista, texto, numero, logico
```

## 6. Identificadores

### Identificador: `[a-zA-Z_][a-zA-Z0-9_]*`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> FirstChar : letra ou _
    FirstChar --> RestChars : letra, dígito ou _
    RestChars --> RestChars : letra, dígito ou _
    FirstChar --> [*] : fim
    RestChars --> [*] : fim
```

---

## 7. Operadores

### Operadores Relacionais Multi-char: `!=|<=|>=`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Exclamation : !
    Exclamation --> NotEqual : =
    NotEqual --> [*]
    
    Start --> Less : <
    Less --> LessEqual : =
    Less --> [*] : fim
    LessEqual --> [*]
    
    Start --> Greater : >
    Greater --> GreaterEqual : =
    Greater --> [*] : fim
    GreaterEqual --> [*]
```

### Operadores Aritméticos: `[+\-*/%]`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Plus : +
    Start --> Minus : -
    Start --> Multiply : *
    Start --> Divide : /
    Start --> Modulo : %
    Plus --> [*]
    Minus --> [*]
    Multiply --> [*]
    Divide --> [*]
    Modulo --> [*]
```

### Operadores Relacionais Single-char: `=|<|>`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Equal : =
    Start --> Less : <
    Start --> Greater : >
    Equal --> [*]
    Less --> [*]
    Greater --> [*]
```

## 8. Delimitadores

### Parênteses: `\(` e `\)`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> LParen : (
    Start --> RParen : )
    LParen --> [*]
    RParen --> [*]

stateDiagram-v2
    [*] --> Start
    Start --> LBracket : [

### Chaves: `\{` e `\}`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> LBrace : {
    Start --> RBrace : }
    LBrace --> [*]
    RBrace --> [*]
```

### Outros Delimitadores: `,|;|:|\.`

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Comma : ,
    Start --> Semicolon : ;
    Start --> Colon : :
    Start --> Dot : .
    Comma --> [*]
    Semicolon --> [*]
    Colon --> [*]
    Dot --> [*]
```

## Ordem de Prioridade no Lexer

O lexer processa os padrões na seguinte ordem (conforme `token_specification` em `lexer.py`):

1. **COMMENT** - Comentários (`#[^\r\n]*`)
2. **WHITESPACE** - Espaços e tabs (`[ \t]+`)
3. **STRING_LITERAL** - Strings com aspas (`"..."` ou `'...'`)
4. **NUMERO_LITERAL** - Números (`\d+...`)
5. **LOGICO_LITERAL** - Booleanos (`verdadeiro|falso`)
6. **KW** - Palavras-chave (lista completa)
7. **OP_RELACIONAL** (multi-char) - `!=`, `<=`, `>=`
8. **OP_ARITMETICO** - `+`, `-`, `*`, `/`, `%`
9. **OP_RELACIONAL** (single-char) - `=`, `<`, `>`
10. **Delimitadores** - `()`, `[]`, `{}`, `,`, `;`, `:`, `.`
11. **IDENTIFICADOR** - Identificadores (`[a-zA-Z_][a-zA-Z0-9_]*`)
12. **MISMATCH** - Caracteres não reconhecidos (`.`)

Esta ordem garante que:

- Palavras-chave sejam reconhecidas antes de identificadores
- Operadores multi-caractere sejam reconhecidos antes de single-char
- Strings e números tenham prioridade sobre outros padrões

---

## Notas de Implementação

- Tokens `WHITESPACE` e `COMMENT` são **ignorados** pelo lexer (não retornados)
- Tokens `MISMATCH` geram `LexerError`
- O lexer normaliza tipos: `KW` → `PALAVRA_CHAVE`, `OP_*` → `OP`
- Quebras de linha em tokens são tratadas para contagem correta de posição

## Minimização de AFD (Semana 5 extras)

Implementamos uma versão didática do algoritmo de minimização de AFD (Hopcroft) em `Semana 5/afds/minimization.py`.

- Exemplos: `Semana 5/afds/example_dfas.py` contém DFAs simples (identificador e número) usados para demonstração.
- Testes: `Semana 5/test_minimization.py` demonstra que a minimização preserva a linguagem de entrada e normalmente reduz o número de estados.

Observação: a implementação é intencionalmente simples e usa representações em dicionários; para produção, converta para representações mais compactas e otimizadas.
