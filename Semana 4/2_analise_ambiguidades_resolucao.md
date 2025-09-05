# Análise de Ambiguidades e Regras de Resolução

## 1. Conflito entre Identificadores e Palavras-Chave

### 1.1 Problema Identificado

Um identificador pode coincidir com uma palavra-chave, causando ambiguidade na análise léxica.

**Exemplo problemático**:
```brasilscript
declarar mostrar como texto  // 'mostrar' é palavra-chave ou identificador?
```

### 1.2 Solução Implementada

Implementar regras de precedência claras:

1. **Palavras-chave têm precedência** sobre identificadores
2. **Verificação de palavras-chave primeiro** antes de classificar como identificador
3. **Case-sensitive**: `Declarar` ≠ `declarar` (palavra-chave)

### 1.3 Exemplos de Resolução

```brasilscript
# Caso 1: Palavra-chave reconhecida
declarar nome  // 'declarar' é palavra-chave

# Caso 2: Identificador reconhecido
Declarar nome  // 'Declarar' é identificador (maiúscula)

# Caso 3: Contexto determina
mostrar "texto"  // 'mostrar' é palavra-chave
declarar mostrar como texto  // 'mostrar' é identificador
```

### 1.4 Algoritmo de Resolução

```
1. Verificar se token corresponde a palavra-chave exata
2. Se sim: classificar como palavra-chave
3. Se não: verificar se é identificador válido
4. Se válido: classificar como identificador
5. Se não: reportar erro léxico
```

## 2. Conflito entre Operadores

### 2.1 Problema Identificado

Operadores multi-caractere podem ser interpretados como sequência de operadores de caractere único.

**Exemplo problemático**:
```brasilscript
se a != b entao  // '!=' é operador único ou '!' + '='?
```

### 2.2 Solução Implementada

**Operadores multi-caractere têm precedência** sobre operadores de caractere único.

### 2.3 Ordem de Verificação

1. **Operadores de 2 caracteres**: `!=`, `<=`, `>=`
2. **Operadores de 1 caractere**: `=`, `<`, `>`

### 2.4 Exemplos de Resolução

```brasilscript
# Caso 1: Operador multi-caractere
a != b  // '!=' é operador relacional

# Caso 2: Operadores separados
a ! = b  // '!' e '=' são operadores separados

# Caso 3: Contexto determina
a <= b  // '<=' é operador relacional
a < = b  // '<' e '=' são operadores separados
```

### 2.5 Algoritmo de Resolução

```
1. Verificar operadores de 2 caracteres primeiro
2. Se encontrado: classificar como operador multi-caractere
3. Se não: verificar operadores de 1 caractere
4. Se encontrado: classificar como operador simples
5. Se não: reportar erro léxico
```

## 3. Conflito entre Strings e Comentários

### 3.1 Problema Identificado

O caractere `#` dentro de string pode ser interpretado como início de comentário.

**Exemplo problemático**:
```brasilscript
mostrar "Preço: R$ 100#00"  // '#' é parte da string ou início de comentário?
```

### 3.2 Solução Implementada

**Strings são processadas primeiro**, ignorando caracteres especiais dentro delas.

### 3.3 Exemplos de Resolução

```brasilscript
# Caso 1: String com #
mostrar "Preço: R$ 100#00"  // '#' é parte da string

# Caso 2: Comentário real
mostrar "texto"  # Este é um comentário

# Caso 3: String com aspas
mostrar "Ele disse \"Olá\""  // Aspas são parte da string
```

### 3.4 Algoritmo de Resolução

```
1. Verificar se está dentro de string
2. Se sim: tratar '#' como caractere literal
3. Se não: verificar se é início de comentário
4. Se sim: processar como comentário
5. Se não: reportar erro léxico
```

## 4. Conflito entre Números e Ponto Decimal

### 4.1 Problema Identificado

O ponto `.` pode ser interpretado como operador ou parte de número decimal.

**Exemplo problemático**:
```brasilscript
declarar preco como 123.45  // '.' é parte do número ou operador?
```

### 4.2 Solução Implementada

**Contexto determina a interpretação**:
- Após dígito: parte de número decimal
- Em outros contextos: operador ou delimitador

### 4.3 Exemplos de Resolução

```brasilscript
# Caso 1: Número decimal
declarar preco como 123.45  // '.' é parte do número

# Caso 2: Operador de acesso
lista.primeiro  // '.' é operador de acesso

# Caso 3: Delimitador
funcao(a, b, c)  // ',' é delimitador
```

### 4.4 Algoritmo de Resolução

```
1. Verificar contexto anterior
2. Se após dígito: tratar como parte de número
3. Se após identificador: tratar como operador de acesso
4. Se em outros contextos: tratar como delimitador
5. Se não reconhecido: reportar erro léxico
```

## 5. Conflito entre Aspas Simples e Duplas

### 5.1 Problema Identificado

Strings podem usar aspas simples ou duplas, mas podem causar confusão.

**Exemplo problemático**:
```brasilscript
mostrar 'Ele disse "Olá"'  // Aspas aninhadas
```

### 5.2 Solução Implementada

**Strings são processadas com escape de caracteres**:
- Aspas duplas dentro de string com aspas simples: literais
- Aspas simples dentro de string com aspas duplas: literais
- Escape com `\` para caracteres especiais

### 5.3 Exemplos de Resolução

```brasilscript
# Caso 1: Aspas simples
mostrar 'Olá, mundo!'  // String com aspas simples

# Caso 2: Aspas duplas
mostrar "Olá, mundo!"  // String com aspas duplas

# Caso 3: Aspas aninhadas
mostrar 'Ele disse "Olá"'  // Aspas duplas dentro de aspas simples
mostrar "Ele disse 'Olá'"  // Aspas simples dentro de aspas duplas

# Caso 4: Escape
mostrar "Ele disse \"Olá\""  // Escape de aspas
```

## 6. Conflito entre Espaços e Delimitadores

### 6.1 Problema Identificado

Espaços em branco podem ser significativos ou não, dependendo do contexto.

**Exemplo problemático**:
```brasilscript
declarar nome como texto  // Espaços são significativos?
```

### 6.2 Solução Implementada

**Espaços em branco são ignorados** exceto dentro de strings:
- Fora de strings: ignorados
- Dentro de strings: preservados
- Quebras de linha: delimitadores de comentários

### 6.3 Exemplos de Resolução

```brasilscript
# Caso 1: Espaços ignorados
declarar nome como texto
declarar  nome   como   texto  // Equivalente ao anterior

# Caso 2: Espaços preservados em string
mostrar "Olá,   mundo!"  // Espaços são preservados

# Caso 3: Quebra de linha
# Comentário
declarar nome como texto  // Quebra de linha termina comentário
```

## 7. Regras de Precedência Gerais

### 7.1 Ordem de Verificação

1. **Comentários** (maior precedência)
2. **Strings** (com escape)
3. **Palavras-chave**
4. **Operadores multi-caractere**
5. **Operadores de caractere único**
6. **Literais** (números, booleanos)
7. **Identificadores**
8. **Delimitadores**
9. **Espaços em branco** (menor precedência)

### 7.2 Algoritmo de Resolução Geral

```
1. Verificar se está dentro de string ou comentário
2. Se sim: processar como literal
3. Se não: aplicar ordem de precedência
4. Para cada tipo de token:
   a. Tentar reconhecer padrão
   b. Se reconhecido: classificar e avançar
   c. Se não: tentar próximo tipo
5. Se nenhum tipo reconhece: reportar erro
```

## 8. Testes de Resolução de Ambiguidades

### 8.1 Casos de Teste

```brasilscript
# Teste 1: Palavras-chave vs Identificadores
declarar mostrar como texto
Declarar Mostrar como Texto

# Teste 2: Operadores multi-caractere
a != b
a ! = b
a <= b
a < = b

# Teste 3: Strings com caracteres especiais
mostrar "Preço: R$ 100#00"
mostrar 'Ele disse "Olá"'
mostrar "Ele disse \"Olá\""

# Teste 4: Números vs Operadores
123.45
lista.primeiro
funcao(a, b, c)

# Teste 5: Espaços e delimitadores
declarar nome como texto
declarar  nome   como   texto
```

### 8.2 Resultados Esperados

| Entrada | Token 1 | Token 2 | Token 3 | Token 4 |
|---------|---------|---------|---------|---------|
| `declarar mostrar` | DECLARAR | IDENTIFICADOR | | |
| `a != b` | IDENTIFICADOR | OP_RELACIONAL | IDENTIFICADOR | |
| `"Preço: R$ 100#00"` | STRING_LITERAL | | | |
| `123.45` | NUMERO_LITERAL | | | |
| `lista.primeiro` | IDENTIFICADOR | DOT | IDENTIFICADOR | |

## 9. Conclusão

As regras de resolução de ambiguidades:

1. **Definem precedência clara** entre tipos de tokens
2. **Resolvem conflitos** de forma determinística
3. **Mantêm consistência** na análise léxica
4. **Facilitam implementação** do analisador
5. **Garantem comportamento previsível** da linguagem

A implementação dessas regras garante que o analisador léxico funcione de forma consistente e previsível.
