# Exemplos Práticos de Derivação da Gramática BrasilScript

## Programa de Exemplo: Calculadora Simples

Vamos analisar o programa `calculadora.bs` e mostrar como ele é derivado pela gramática formal:

```brasilscript
# Programa: Calculadora Simples
mostrar "=== CALCULADORA SIMPLES ==="

perguntar "Digite o primeiro número: " guardar_em num1
perguntar "Digite o segundo número: " guardar_em num2
perguntar "Operação (+, -, *, /): " guardar_em operacao

se operacao = "+" então
    declarar resultado como num1 + num2
senão_se operacao = "-" então
    declarar resultado como num1 - num2
senão_se operacao = "*" então
    declarar resultado como num1 * num2
senão_se operacao = "/" então
    se num2 != 0 então
        declarar resultado como num1 / num2
    senão
        mostrar "Erro: Divisão por zero!"
        parar
    fim_se
senão
    mostrar "Operação inválida!"
    parar
fim_se

mostrar "Resultado: " + resultado
```

## 1. Derivação do Programa Principal

```
programa
→ instrucao*
→ instrucao instrucao instrucao instrucao instrucao instrucao
→ comentario instrucao instrucao instrucao instrucao instrucao
→ COMMENT instrucao instrucao instrucao instrucao instrucao
→ # Programa: Calculadora Simples instrucao instrucao instrucao instrucao instrucao
```

## 2. Derivação de Comentários

```
comentario
→ COMMENT
→ #.*
→ # Programa: Calculadora Simples
```

## 3. Derivação de Chamada de Função (mostrar)

```
instrucao
→ chamada_funcao
→ IDENTIFICADOR LPAREN expressao RPAREN
→ mostrar LPAREN expressao RPAREN
→ mostrar LPAREN expressao_logica RPAREN
→ mostrar LPAREN expressao_relacional RPAREN
→ mostrar LPAREN expressao_aritmetica RPAREN
→ mostrar LPAREN termo RPAREN
→ mostrar LPAREN fator RPAREN
→ mostrar LPAREN STRING_LITERAL RPAREN
→ mostrar LPAREN "=== CALCULADORA SIMPLES ===" RPAREN
→ mostrar("=== CALCULADORA SIMPLES ===")
```

## 4. Derivação de Estrutura Condicional

```
estrutura_controle
→ estrutura_condicional
→ SE expressao ENTAO bloco_codigo (SENAO_SE expressao ENTAO bloco_codigo)* (SENAO bloco_codigo)? FIM_SE
→ SE expressao_relacional ENTAO bloco_codigo SENAO_SE expressao_relacional ENTAO bloco_codigo SENAO_SE expressao_relacional ENTAO bloco_codigo SENAO_SE expressao_relacional ENTAO bloco_codigo SENAO bloco_codigo FIM_SE
→ SE IDENTIFICADOR = STRING_LITERAL ENTAO bloco_codigo SENAO_SE IDENTIFICADOR = STRING_LITERAL ENTAO bloco_codigo SENAO_SE IDENTIFICADOR = STRING_LITERAL ENTAO bloco_codigo SENAO_SE IDENTIFICADOR = STRING_LITERAL ENTAO bloco_codigo SENAO bloco_codigo FIM_SE
→ SE operacao = "+" ENTAO bloco_codigo SENAO_SE operacao = "-" ENTAO bloco_codigo SENAO_SE operacao = "*" ENTAO bloco_codigo SENAO_SE operacao = "/" ENTAO bloco_codigo SENAO bloco_codigo FIM_SE
```

## 5. Derivação de Declaração de Variável com Expressão

```
declaracao_variavel
→ DECLARAR IDENTIFICADOR COMO tipo ATRIBUICAO expressao
→ DECLARAR resultado COMO NUMERO = expressao
→ DECLARAR resultado COMO NUMERO = expressao_aritmetica
→ DECLARAR resultado COMO NUMERO = termo + termo
→ DECLARAR resultado COMO NUMERO = fator + fator
→ DECLARAR resultado COMO NUMERO = IDENTIFICADOR + IDENTIFICADOR
→ DECLARAR resultado COMO NUMERO = num1 + num2
→ declarar resultado como num1 + num2
```

## 6. Derivação de Expressão Aritmética Complexa

Para a expressão `num1 + num2`:

```
expressao
→ expressao_logica
→ expressao_relacional
→ expressao_aritmetica
→ expressao_aritmetica + termo
→ termo + termo
→ fator + fator
→ IDENTIFICADOR + IDENTIFICADOR
→ num1 + num2
```

## 7. Derivação de Estrutura Condicional Aninhada

Para o bloco interno `se num2 != 0 então`:

```
estrutura_condicional
→ SE expressao ENTAO bloco_codigo FIM_SE
→ SE expressao_relacional ENTAO bloco_codigo FIM_SE
→ SE expressao_aritmetica != expressao_aritmetica ENTAO bloco_codigo FIM_SE
→ SE termo != termo ENTAO bloco_codigo FIM_SE
→ SE fator != fator ENTAO bloco_codigo FIM_SE
→ SE IDENTIFICADOR != NUMERO_LITERAL ENTAO bloco_codigo FIM_SE
→ SE num2 != 0 ENTAO bloco_codigo FIM_SE
→ se num2 != 0 então bloco_codigo fim_se
```

## 8. Derivação de Bloco de Código

```
bloco_codigo
→ instrucao*
→ instrucao instrucao
→ declaracao_variavel instrucao
→ DECLARAR IDENTIFICADOR COMO tipo ATRIBUICAO expressao instrucao
→ declarar resultado como num1 + num2 instrucao
```

## 9. Árvore Sintática Abstrata (AST) Simplificada

```
programa
├── comentario
├── chamada_funcao (mostrar)
├── chamada_funcao (perguntar)
├── chamada_funcao (perguntar)
├── chamada_funcao (perguntar)
├── estrutura_condicional
│   ├── condicao: operacao = "+"
│   ├── bloco_verdadeiro: declarar resultado como num1 + num2
│   ├── condicao: operacao = "-"
│   ├── bloco_verdadeiro: declarar resultado como num1 - num2
│   ├── condicao: operacao = "*"
│   ├── bloco_verdadeiro: declarar resultado como num1 * num2
│   ├── condicao: operacao = "/"
│   ├── bloco_verdadeiro:
│   │   └── estrutura_condicional
│   │       ├── condicao: num2 != 0
│   │       ├── bloco_verdadeiro: declarar resultado como num1 / num2
│   │       └── bloco_falso:
│   │           ├── chamada_funcao (mostrar)
│   │           └── parar
│   └── bloco_falso:
│       ├── chamada_funcao (mostrar)
│       └── parar
└── chamada_funcao (mostrar)
```

## 10. Análise de Precedência de Operadores

Para a expressão `num1 + num2`:

1. **Análise Léxica**: `num1` (IDENTIFICADOR), `+` (OP_ARITMETICO), `num2` (IDENTIFICADOR)
2. **Análise Sintática**:
   - `num1` é um fator (IDENTIFICADOR)
   - `num2` é um fator (IDENTIFICADOR)
   - `+` é um operador aritmético
   - A regra `expressao_aritmetica → expressao_aritmetica + termo` aplica associatividade à esquerda

## 11. Verificação de Ambiguidades

### 11.1 Precedência de Operadores
A expressão `num1 + num2 * num3` seria interpretada como:
```
expressao_aritmetica
→ expressao_aritmetica + termo
→ termo + termo
→ fator + termo * fator
→ num1 + (num2 * num3)  // Multiplicação tem precedência
```

### 11.2 Estrutura Condicional Aninhada
O `senão` sempre pertence ao `se` mais próximo:
```brasilscript
se condicao1 então
    se condicao2 então
        instrucao1
    senão  // Pertence ao se condicao2
        instrucao2
    fim_se
fim_se
```

## 12. Conclusão

Este exemplo demonstra como a gramática formal da BrasilScript:

1. **Define estruturas claras** para todos os elementos da linguagem
2. **Resolve ambiguidades** através de regras de precedência
3. **Suporta estruturas aninhadas** como condicionais dentro de condicionais
4. **Mantém consistência** com a sintaxe em português brasileiro
5. **Permite análise determinística** através de parsers LL(1) ou LR(1)

A gramática garante que programas como a calculadora sejam interpretados de forma única e previsível, facilitando a implementação do compilador.
