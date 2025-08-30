# Gramática Formal da BrasilScript

## 1. Classificação na Hierarquia de Chomsky

A gramática da BrasilScript é classificada como **Gramática Livre de Contexto (Tipo 2)** na hierarquia de Chomsky. Esta escolha é justificada pelos seguintes motivos:

- **Expressividade adequada**: Gramáticas livres de contexto são capazes de expressar a estrutura sintática de linguagens de programação modernas
- **Simplicidade de implementação**: Permitem o uso de parsers eficientes como LL(k) ou LR(k)
- **Clareza de definição**: As regras de produção são intuitivas e fáceis de entender
- **Capacidade de expressar estruturas aninhadas**: Essencial para expressões, blocos de código e estruturas de controle

## 2. Gramática Formal (BNF - Backus-Naur Form)

### 2.1 Símbolos Terminais
```
# Palavras-chave
DECLARAR, COMO, MOSTRAR, PERGUNTAR, GUARDAR_EM, SE, ENTAO, SENAO, SENAO_SE, FIM_SE
REPETIR, VEZES, ENQUANTO, FACA, FIM_ENQUANTO, FIM_REPETIR
FUNCAO, FIM_FUNCAO, RETORNAR, PARA_CADA, EM, FIM_PARA_CADA
PARAR, E, OU, NAO, LISTA, TEXTO, NUMERO, LOGICO

# Operadores
OP_ARITMETICO: + | - | * | / | %
OP_RELACIONAL: = | != | < | > | <= | >=
OP_ATRIBUICAO: =
OP_LOGICO: E | OU | NAO

# Delimitadores
LPAREN: (
RPAREN: )
LBRACKET: [
RBRACKET: ]
LBRACE: {
RBRACE: }
COMMA: ,
SEMICOLON: ;
COLON: :
DOT: .

# Literais
NUMERO_LITERAL: [0-9]+(\.[0-9]+)?
STRING_LITERAL: "([^"]|\\.)*" | '([^']|\\.)*'
LOGICO_LITERAL: verdadeiro | falso

# Identificadores
IDENTIFICADOR: [a-zA-Z_][a-zA-Z0-9_]*

# Comentários e espaços
COMMENT: #.*
WHITESPACE: [ \t\n\r]+
```

### 2.2 Símbolos Não-Terminais e Regras de Produção

```
// Programa principal
programa ::= instrucao*

// Instruções
instrucao ::= declaracao_variavel
           | atribuicao
           | chamada_funcao
           | estrutura_controle
           | retorno
           | comentario

// Declaração de variáveis
declaracao_variavel ::= DECLARAR IDENTIFICADOR COMO tipo
                      | DECLARAR IDENTIFICADOR COMO tipo ATRIBUICAO expressao

tipo ::= TEXTO | NUMERO | LOGICO | LISTA | LISTA LBRACKET tipo RBRACKET

// Atribuição
atribuicao ::= IDENTIFICADOR OP_ATRIBUICAO expressao

// Expressões
expressao ::= expressao_logica

expressao_logica ::= expressao_relacional
                  | expressao_logica OP_LOGICO expressao_relacional

expressao_relacional ::= expressao_aritmetica
                      | expressao_aritmetica OP_RELACIONAL expressao_aritmetica

expressao_aritmetica ::= termo
                      | expressao_aritmetica OP_ARITMETICO termo

termo ::= fator
       | termo OP_ARITMETICO fator

fator ::= LPAREN expressao RPAREN
       | literal
       | IDENTIFICADOR
       | chamada_funcao
       | acesso_lista

// Literais
literal ::= NUMERO_LITERAL | STRING_LITERAL | LOGICO_LITERAL | lista_literal

lista_literal ::= LBRACKET (expressao (COMMA expressao)*)? RBRACKET

// Chamada de função
chamada_funcao ::= IDENTIFICADOR LPAREN (expressao (COMMA expressao)*)? RPAREN

// Acesso a lista
acesso_lista ::= IDENTIFICADOR LBRACKET expressao RBRACKET

// Estruturas de controle
estrutura_controle ::= estrutura_condicional
                    | estrutura_repeticao
                    | estrutura_para_cada

// Estrutura condicional
estrutura_condicional ::= SE expressao ENTAO bloco_codigo (SENAO_SE expressao ENTAO bloco_codigo)* (SENAO bloco_codigo)? FIM_SE

// Estruturas de repetição
estrutura_repeticao ::= loop_enquanto | loop_repetir

loop_enquanto ::= ENQUANTO expressao FACA bloco_codigo FIM_ENQUANTO

loop_repetir ::= REPETIR expressao VEZES bloco_codigo FIM_REPETIR

loop_para_cada ::= PARA_CADA IDENTIFICADOR EM expressao FACA bloco_codigo FIM_PARA_CADA

// Bloco de código
bloco_codigo ::= instrucao*

// Definição de função
definicao_funcao ::= FUNCAO IDENTIFICADOR LPAREN (parametro (COMMA parametro)*)? RPAREN bloco_codigo FIM_FUNCAO

parametro ::= IDENTIFICADOR COMO tipo

// Instruções especiais
retorno ::= RETORNAR expressao?
parar ::= PARAR

// Comentários
comentario ::= COMMENT
```

## 3. Exemplos de Derivações

### 3.1 Declaração de Variável
```
programa
→ instrucao*
→ declaracao_variavel
→ DECLARAR IDENTIFICADOR COMO tipo
→ DECLARAR idade COMO NUMERO
```

### 3.2 Expressão Aritmética
```
expressao
→ expressao_logica
→ expressao_relacional
→ expressao_aritmetica
→ expressao_aritmetica + termo
→ termo + termo
→ fator + fator
→ IDENTIFICADOR + IDENTIFICADOR
→ a + b
```

### 3.3 Estrutura Condicional
```
estrutura_controle
→ estrutura_condicional
→ SE expressao ENTAO bloco_codigo FIM_SE
→ SE expressao_relacional ENTAO bloco_codigo FIM_SE
→ SE expressao_aritmetica > expressao_aritmetica ENTAO bloco_codigo FIM_SE
→ SE IDENTIFICADOR > NUMERO_LITERAL ENTAO bloco_codigo FIM_SE
→ SE idade > 18 ENTAO bloco_codigo FIM_SE
```

## 4. Análise de Ambiguidades e Estratégias de Resolução

### 4.1 Ambiguidade de Precedência de Operadores

**Problema**: A expressão `a + b * c` pode ser interpretada como `(a + b) * c` ou `a + (b * c)`.

**Solução**: Implementação de regras de precedência através da estrutura hierárquica da gramática:
- Operadores de multiplicação (`*`, `/`, `%`) têm maior precedência
- Operadores de adição (`+`, `-`) têm menor precedência
- Uso de parênteses para controle explícito da precedência

### 4.2 Ambiguidade do "else" pendente

**Problema**: Em estruturas condicionais aninhadas, pode haver ambiguidade sobre qual `se` o `senão` pertence.

**Solução**: Regra de associatividade à direita - o `senão` sempre pertence ao `se` mais próximo.

### 4.3 Estratégias de Resolução

1. **Precedência de Operadores**: Definida pela hierarquia de regras de produção
2. **Associatividade**: 
   - Operadores aritméticos: associatividade à esquerda
   - Operadores lógicos: associatividade à esquerda
3. **Delimitadores Explícitos**: Uso de palavras-chave como `fim_se`, `fim_enquanto` para delimitar blocos
4. **Parsing Determinístico**: Implementação de parser LL(1) ou LR(1) para evitar ambiguidades

## 5. Considerações sobre Paradigmas

### 5.1 Paradigma Imperativo
A gramática atual suporta o paradigma imperativo com:
- Declaração e atribuição de variáveis
- Estruturas de controle sequenciais
- Funções com efeitos colaterais

### 5.2 Extensões Funcionais Futuras
Para suportar programação funcional, a gramática pode ser estendida com:
- Expressões lambda
- Funções de primeira classe
- Avaliação lazy
- Imutabilidade de dados

### 5.3 Equilíbrio Expressividade-Simplicidade
A gramática atual prioriza:
- **Simplicidade**: Sintaxe intuitiva em português
- **Legibilidade**: Estruturas claras e bem delimitadas
- **Extensibilidade**: Base sólida para futuras expansões
