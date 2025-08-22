# Especificação Técnica - BrasilScript

## 1. Visão Geral

A BrasilScript é uma linguagem de programação educacional projetada especificamente para estudantes brasileiros, eliminando a barreira linguística do inglês e fornecendo uma sintaxe natural em português.

## 2. Alfabeto e Conjuntos de Caracteres

### 2.1 Alfabeto Básico (Σ)

```
Σ = Σ_letras ∪ Σ_dígitos ∪ Σ_operadores ∪ Σ_delimitadores ∪ Σ_especiais ∪ Σ_acentos
```

**Onde:**
- `Σ_letras = {a, b, c, ..., z, A, B, C, ..., Z}`
- `Σ_dígitos = {0, 1, 2, ..., 9}`
- `Σ_operadores = {+, -, *, /, %, =, <, >, !}`
- `Σ_delimitadores = {(, ), [, ], {, }, ", ', #, _, ., ,, ;}`
- `Σ_especiais = {espaço, tab, quebra_de_linha}`
- `Σ_acentos = {ç, ã, õ, é, ê, í, ó, ô, ú, ü}`

### 2.2 Codificação de Caracteres

- **Padrão:** UTF-8
- **Suporte:** Caracteres acentuados do português brasileiro
- **Case-sensitivity:** Sim (distingue maiúsculas de minúsculas)

## 3. Definição Formal dos Tokens

### 3.1 Identificadores

```
ID = (letra | _) (letra | dígito | _)*
```

**Regras:**
- Deve começar com letra ou underscore
- Pode conter letras, dígitos e underscores
- Case-sensitive
- Não pode ser uma palavra-chave

**Exemplos válidos:**
- `nome`, `idade_aluno`, `primeiroNome`, `número1`, `_variável`

### 3.2 Literais Numéricos

#### Inteiros
```
INTEIRO = dígito+
```

#### Decimais
```
DECIMAL = dígito+ . dígito+
```

#### Notação Científica
```
CIENTIFICO = (dígito+ | dígito+ . dígito+) [e|E] [+|-]? dígito+
```

### 3.3 Strings

```
STRING = " (caractere | escape)* "
```

**Sequências de escape:**
- `\\` - Barra invertida
- `\"` - Aspas duplas
- `\n` - Quebra de linha
- `\t` - Tabulação

### 3.4 Comentários

```
COMENTARIO = # (caractere)* quebra_de_linha
```

### 3.5 Palavras-Chave

```
PALAVRAS_CHAVE = {
    # Declaração
    declarar, como,
    
    # Entrada/Saída
    mostrar, perguntar, guardar_em,
    
    # Controle de Fluxo
    se, então, senão, senão_se, fim_se,
    enquanto, faça, fim_enquanto,
    repetir, vezes, fim_repetir,
    para_cada, em, fim_para_cada,
    
    # Funções
    função, fim_função,
    
    # Estruturas de Dados
    lista,
    
    # Controle de Programa
    parar
}
```

### 3.6 Operadores

#### Aritméticos
```
OP_ARITMETICO = + | - | * | / | %
```

#### Comparação
```
OP_COMPARACAO = = | != | < | > | <= | >=
```

#### Atribuição
```
OP_ATRIBUICAO = = | += | -= | *= | /=
```

### 3.7 Delimitadores

```
DELIMITADOR = ( | ) | [ | ] | { | } | , | ;
```

## 4. Gramática Sintática

### 4.1 Programa

```
PROGRAMA = DECLARACAO*
```

### 4.2 Declarações

```
DECLARACAO = DECLARACAO_VARIAVEL |
             DECLARACAO_FUNCAO |
             COMANDO |
             ESTRUTURA_CONTROLE
```

### 4.3 Declaração de Variável

```
DECLARACAO_VARIAVEL = "declarar" ID "como" EXPRESSAO
```

### 4.4 Expressões

```
EXPRESSAO = EXPRESSAO_LOGICA

EXPRESSAO_LOGICA = EXPRESSAO_COMPARACAO (("e" | "ou") EXPRESSAO_COMPARACAO)*

EXPRESSAO_COMPARACAO = EXPRESSAO_ARITMETICA (OP_COMPARACAO EXPRESSAO_ARITMETICA)*

EXPRESSAO_ARITMETICA = TERMO ((+ | -) TERMO)*

TERMO = FATOR ((* | / | %) FATOR)*

FATOR = NUMERO | ID | STRING | "(" EXPRESSAO ")" | CHAMADA_FUNCAO
```

### 4.5 Estruturas de Controle

#### Condicional
```
ESTRUTURA_CONDICIONAL = "se" EXPRESSAO "então" BLOCO ("senão_se" EXPRESSAO "então" BLOCO)* ("senão" BLOCO)? "fim_se"
```

#### Loop While
```
ESTRUTURA_WHILE = "enquanto" EXPRESSAO "faça" BLOCO "fim_enquanto"
```

#### Loop For
```
ESTRUTURA_FOR = "repetir" NUMERO "vezes" BLOCO "fim_repetir"
```

#### Loop Para Cada
```
ESTRUTURA_PARA_CADA = "para_cada" ID "em" EXPRESSAO "faça" BLOCO "fim_para_cada"
```

### 4.6 Funções

```
DECLARACAO_FUNCAO = "função" ID "(" PARAMETROS ")" BLOCO "fim_função"

PARAMETROS = (ID ("," ID)*)?

CHAMADA_FUNCAO = ID "(" ARGUMENTOS ")"

ARGUMENTOS = (EXPRESSAO ("," EXPRESSAO)*)?
```

### 4.7 Blocos

```
BLOCO = DECLARACAO*
```

## 5. Semântica

### 5.1 Tipos de Dados

- **Inteiro:** Números inteiros (ex: 42, -17)
- **Decimal:** Números de ponto flutuante (ex: 3.14, -2.5)
- **Texto:** Strings (ex: "Olá, mundo!")
- **Lista:** Arrays heterogêneos (ex: [1, "texto", 3.14])
- **Booleano:** Valores lógicos (verdadeiro/falso)

### 5.2 Conversão de Tipos

- Conversão automática entre tipos numéricos
- Strings podem ser concatenadas com o operador `+`
- Conversão implícita de números para strings em concatenação

### 5.3 Escopo

- Escopo léxico
- Variáveis locais em funções
- Variáveis globais no escopo principal

## 6. Tratamento de Erros

### 6.1 Tipos de Erro

1. **Erro Léxico:** Caracteres inválidos, tokens malformados
2. **Erro Sintático:** Estrutura gramatical incorreta
3. **Erro Semântico:** Tipos incompatíveis, variáveis não declaradas
4. **Erro de Execução:** Divisão por zero, índice fora dos limites

### 6.2 Mensagens de Erro

Todas as mensagens de erro são em português brasileiro:

```
Erro léxico: Caractere inválido na linha 5
Erro sintático: Esperado 'então' na linha 10
Erro semântico: Variável 'idade' não declarada
Erro de execução: Divisão por zero
```

## 7. Ambiente de Execução

### 7.1 Funções Built-in

- `mostrar(expressão)`: Exibe texto no console
- `perguntar(mensagem)`: Solicita entrada do usuário
- `lista(...)`: Cria uma nova lista

### 7.2 Operações com Listas

- `lista[indice]`: Acesso a elemento
- `lista[indice] = valor`: Atribuição a elemento
- `para_cada`: Iteração sobre elementos

## 8. Considerações de Implementação

### 8.1 Análise Léxica

- Scanner baseado em autômatos finitos
- Reconhecimento de longest match
- Tratamento de comentários e espaços em branco

### 8.2 Análise Sintática

- Parser recursivo descendente
- Tratamento de precedência de operadores
- Recuperação de erros

### 8.3 Interpretação

- Árvore sintática abstrata (AST)
- Execução por interpretação direta
- Ambiente de execução com tabela de símbolos

## 9. Exemplos de Implementação

### 9.1 Scanner (Analisador Léxico)

```python
class BrasilScriptScanner:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []
    
    def scan(self):
        while self.position < len(self.source):
            char = self.source[self.position]
            
            if char.isspace():
                self.skip_whitespace()
            elif char == '#':
                self.skip_comment()
            elif char.isalpha() or char == '_':
                self.scan_identifier()
            elif char.isdigit():
                self.scan_number()
            elif char == '"':
                self.scan_string()
            else:
                self.scan_operator()
        
        return self.tokens
```

### 9.2 Parser (Analisador Sintático)

```python
class BrasilScriptParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    
    def parse_program(self):
        declarations = []
        while self.position < len(self.tokens):
            declarations.append(self.parse_declaration())
        return Program(declarations)
    
    def parse_declaration(self):
        token = self.current_token()
        if token.type == 'DECLARAR':
            return self.parse_variable_declaration()
        elif token.type == 'FUNCAO':
            return self.parse_function_declaration()
        else:
            return self.parse_statement()
```

## 10. Conclusão

Esta especificação técnica fornece a base formal para a implementação da linguagem BrasilScript, garantindo consistência e facilitando o desenvolvimento do compilador/interpretador. A linguagem foi projetada para ser simples de aprender, mas poderosa o suficiente para ensinar conceitos fundamentais de programação.
