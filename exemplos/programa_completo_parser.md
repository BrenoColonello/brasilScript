# 🎉 Exemplo de Programa BrasilScript Completo

Este arquivo demonstra um programa BrasilScript sendo processado pelo parser.

## Programa Exemplo

```brasilscript
# Calculadora simples em BrasilScript

declarar num1 como numero = 10
declarar num2 como numero = 5
declarar operacao como numero = 1
declarar resultado como numero

# Função para somar
funcao somar(a, b)
    declarar soma como numero
    soma = a + b
    retornar soma
fim_funcao

# Função para subtrair
funcao subtrair(a, b)
    declarar diferenca como numero
    diferenca = a - b
    retornar diferenca
fim_funcao

# Lógica principal
se operacao = 1 entao
    resultado = somar(num1, num2)
senao_se operacao = 2 entao
    resultado = subtrair(num1, num2)
senao
    resultado = 0
fim_se

# Loop para demonstrar
declarar contador como numero = 0
enquanto contador < resultado faca
    contador = contador + 1
fim_enquanto

# Loop repetir
repetir 3 vezes
    resultado = resultado + 1
fim_repetir
```

## AST Gerada

Quando processado pelo parser, este código gera uma AST com:

1. **Declarações**: 4 declarações de variáveis
2. **Função somar**: Com 2 parâmetros e corpo com declaração, atribuição e retorno
3. **Função subtrair**: Similar à função somar
4. **Condicional if-else**: Com múltiplas condições
5. **Loop while**: Com condição e corpo
6. **Loop repeat**: Com contagem fixa

## Estruturas Demonstradas

### ✅ Declarações de Variáveis
- [x] Declaração simples: `declarar x como numero`
- [x] Declaração com inicialização: `declarar x como numero = 10`
- [x] Diferentes tipos: `numero`, `texto`, `logico`

### ✅ Expressões
- [x] Aritméticas: `a + b`, `a - b * c`
- [x] Relacionais: `x > 5`, `a = b`
- [x] Lógicas: `x > 5 e y < 10`
- [x] Precedência correta: `10 + 20 * 2` = `10 + (20 * 2)`

### ✅ Estruturas de Controle
- [x] Condicional if-else com múltiplas condições
- [x] Loop while com condição
- [x] Loop repeat com contagem
- [x] Blocos aninhados

### ✅ Funções
- [x] Declaração com parâmetros
- [x] Corpo com múltiplas instruções
- [x] Retorno de valores
- [x] Chamadas de função

### ✅ Atribuições
- [x] Atribuição simples: `x = 10`
- [x] Atribuição com expressão: `x = a + b`
- [x] Atribuição com chamada de função: `x = somar(1, 2)`

## Limitações Atuais

### ❌ Ainda não implementado
- [ ] Strings (problema no lexer com aspas)
- [ ] Listas e arrays
- [ ] Input/Output (mostrar, perguntar)
- [ ] Comentários inline
- [ ] Operadores lógicos avançados

### ⚠️  Conhecidos
- Lexer não processa strings com aspas corretamente
- Alguns operadores podem não estar completamente implementados
- Falta análise semântica (verificação de tipos)

## Como Testar

```bash
cd /path/to/brasilScript
python test_parser_simple.py
```

Este comando executa vários testes demonstrando que a gramática está funcionando corretamente para as estruturas principais do BrasilScript.
