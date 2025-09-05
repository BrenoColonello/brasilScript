# Especificação Completa usando Expressões Regulares

## 1. Expressões Regulares para Tokens

### 1.1 Palavras-Chave (Keywords)

```regex
# Palavras-chave principais
DECLARAR: \bdeclarar\b
COMO: \bcomo\b
MOSTRAR: \bmostrar\b
PERGUNTAR: \bperguntar\b
GUARDAR_EM: \bguardar_em\b
SE: \bse\b
ENTAO: \bentao\b
SENAO: \bsenao\b
SENAO_SE: \bsenao_se\b
FIM_SE: \bfim_se\b
REPETIR: \brepetir\b
VEZES: \bvezes\b
ENQUANTO: \benquanto\b
FACA: \bfaca\b
FIM_ENQUANTO: \bfim_enquanto\b
FIM_REPETIR: \bfim_repetir\b
FUNCAO: \bfuncao\b
FIM_FUNCAO: \bfim_funcao\b
RETORNAR: \bretornar\b
PARA_CADA: \bpara_cada\b
EM: \bem\b
FIM_PARA_CADA: \bfim_para_cada\b
PARAR: \bparar\b
E: \be\b
OU: \bou\b
NAO: \bnao\b
LISTA: \blista\b
TEXTO: \btexto\b
NUMERO: \bnumero\b
LOGICO: \blogico\b
```

### 1.2 Operadores

```regex
# Operadores aritméticos
OP_ARITMETICO: [+\-*/%]

# Operadores relacionais
OP_RELACIONAL: =|!=|<=|>=|<|>

# Operador de atribuição
OP_ATRIBUICAO: =

# Operadores lógicos
OP_LOGICO: \b(e|ou|nao)\b
```

### 1.3 Delimitadores

```regex
# Parênteses
LPAREN: \(
RPAREN: \)

# Colchetes
LBRACKET: \[
RBRACKET: \]

# Chaves
LBRACE: \{
RBRACE: \}

# Outros delimitadores
COMMA: ,
SEMICOLON: ;
COLON: :
DOT: \.
```

### 1.4 Literais

```regex
# Números (inteiros e decimais)
NUMERO_LITERAL: \d+(\.\d+)?([eE][+-]?\d+)?

# Strings (aspas duplas e simples)
STRING_LITERAL: "(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'

# Valores lógicos
LOGICO_LITERAL: \b(verdadeiro|falso)\b
```

### 1.5 Identificadores

```regex
# Identificadores (letras, números, underscore)
IDENTIFICADOR: [a-zA-Z_][a-zA-Z0-9_]*
```

### 1.6 Comentários e Espaços

```regex
# Comentários de linha
COMMENT: #[^\r\n]*

# Espaços em branco
WHITESPACE: [ \t\r\n]+
```

## 2. Implementação do Analisador Léxico

### 2.1 Estrutura do Token

```python
class Token:
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo      # Tipo do token (IDENTIFICADOR, NUMERO_LITERAL, etc.)
        self.valor = valor    # Valor literal do token
        self.linha = linha    # Número da linha
        self.coluna = coluna  # Número da coluna
```

### 2.2 Algoritmo de Análise Léxica

```
1. Inicializar posição atual (linha=1, coluna=1)
2. Enquanto houver caracteres:
   a. Pular espaços em branco
   b. Tentar reconhecer cada tipo de token na ordem:
      - Comentários
      - Palavras-chave
      - Operadores multi-caractere
      - Operadores de caractere único
      - Literais (números, strings, booleanos)
      - Identificadores
      - Delimitadores
   c. Se token reconhecido: criar Token e avançar posição
   d. Se não reconhecido: tratar erro
3. Retornar lista de tokens
```

### 2.3 Otimizações

#### 2.3.1 Compilação de Expressões Regulares
- **Compilar regex uma vez** e reutilizar
- **Usar flags otimizadas** (re.IGNORECASE para palavras-chave)

#### 2.3.2 Cache de Tokens
- **Manter cache** de tokens frequentes
- **Evitar recriação** de objetos Token

#### 2.3.3 Análise Incremental
- **Processar arquivo em chunks** para arquivos grandes
- **Manter estado** entre chunks

## 3. Testes da Especificação Léxica

### 3.1 Casos de Teste Positivos

```brasilscript
# Teste 1: Palavras-chave
declarar mostrar perguntar se então senão

# Teste 2: Números
123 45.67 1e5 2.5e-3

# Teste 3: Strings
"Olá, mundo!" 'BrasilScript' "com \"aspas\""

# Teste 4: Identificadores
nome idade_do_usuario preço_do_produto

# Teste 5: Operadores
+ - * / % = != <= >= < >
```

### 3.2 Casos de Teste Negativos

```brasilscript
# Teste 1: Caracteres inválidos
nome§ = "teste"  # ERRO: caractere inválido

# Teste 2: String não fechada
mostrar "Olá, mundo  # ERRO: string não fechada

# Teste 3: Número malformado
preco = 123.  # ERRO: número malformado

# Teste 4: Identificador inválido
2nome = "teste"  # ERRO: identificador inválido
```

## 4. Considerações de Internacionalização

### 4.1 Suporte a Caracteres Especiais

A especificação atual suporta:
- **Letras básicas**: a-z, A-Z
- **Números**: 0-9
- **Underscore**: _

### 4.2 Extensões Futuras

Para suportar mais caracteres no futuro:
```regex
# Unicode básico para português (futuro)
IDENTIFICADOR: [\w\u00C0-\u017F][\w\u00C0-\u017F0-9_]*

# Unicode completo (futuro)
IDENTIFICADOR: [\p{L}_][\p{L}\p{N}_]*
```

### 4.3 Impacto na Performance

- **Caracteres básicos**: Performance otimizada
- **Unicode futuro**: Pode impactar performance
- **Recomendação**: Manter suporte básico atual

## 5. Conclusão

Esta especificação de expressões regulares:

1. **Define padrões precisos** para todos os tokens da linguagem
2. **Mantém simplicidade** com caracteres básicos
3. **Otimiza performance** através de técnicas eficientes
4. **Facilita implementação** do analisador léxico
5. **Mantém compatibilidade** com ferramentas de parsing existentes

A especificação está pronta para implementação automática do analisador léxico.
