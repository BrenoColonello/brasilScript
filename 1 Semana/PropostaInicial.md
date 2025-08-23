## 1. Introdução e Visão Geral do Projeto

### 1.1 Contexto e Motivação

O ensino de programação no Brasil enfrenta desafios significativos, especialmente no que se refere à barreira linguística. A maioria das linguagens de programação utiliza palavras-chave em inglês, criando uma camada adicional de complexidade para estudantes brasileiros que estão iniciando sua jornada na programação. Este projeto surge da necessidade de criar uma ferramenta educacional que seja verdadeiramente acessível e inclusiva.

> **Problema Identificado:** Segundo pesquisas do IBGE, apenas 5% da população brasileira possui fluência em inglês, criando uma barreira significativa no aprendizado de programação tradicional.

A **BrasilScript** foi concebida como uma linguagem de programação que combina a simplicidade do Python com a naturalidade do português brasileiro, oferecendo uma ponte acessível entre o pensamento lógico humano e a programação de computadores.

### 1.2 Objetivos do Projeto

#### Objetivos Principais
- ✓ Desenvolver uma linguagem 100% em português brasileiro
- ✓ Criar sintaxe mais simples que Python
- ✓ Facilitar o aprendizado de lógica de programação
- ✓ Promover inclusão digital no Brasil

#### Objetivos Específicos
- ✓ Implementar interpretador funcional
- ✓ Criar documentação educacional completa
- ✓ Desenvolver ambiente de desenvolvimento integrado
- ✓ Estabelecer base para futuras expansões

### 1.3 Público-Alvo

#### Estudantes (12-18 anos)
Ensino fundamental e médio, primeira experiência com programação

#### Educadores
Professores buscando ferramentas pedagógicas acessíveis

#### Iniciantes Adultos
Pessoas em transição de carreira ou interesse pessoal

---

## 2. Especificação da Linguagem BrasilScript

### 2.1 Filosofia e Princípios de Design

#### Princípios Fundamentais

- **Simplicidade:** Código legível como português natural
- **Clareza:** Intenção do código óbvia à primeira vista
- **Acessibilidade:** Sem barreiras linguísticas
- **Progressividade:** Crescimento gradual de complexidade

### 2.2 Sintaxe e Estruturas Básicas

#### Declaração de Variáveis

```brasilscript
# BrasilScript
declarar nome como "João"
declarar idade como 15
declarar altura como 1.75
```
*Comparação Python: name = "João"*

#### Entrada e Saída

```brasilscript
# Saída de dados
mostrar "Olá, mundo!"

# Entrada de dados
perguntar "Seu nome:" guardar_em nome
```
*Comparação Python: print() / input()*

#### Estruturas Condicionais

```brasilscript
se idade >= 18 então
    mostrar "Maior de idade"
senão_se idade >= 16 então
    mostrar "Pode votar"
senão
    mostrar "Menor de idade"
fim_se
```

#### Estruturas de Repetição

```brasilscript
# Laço com contador
repetir 5 vezes
    mostrar "Repetição"
fim_repetir

# Laço condicional
enquanto idade < 18 faça
    idade = idade + 1
fim_enquanto
```

### 2.3 Funcionalidades Avançadas

#### Funções e Procedimentos

```brasilscript
função saudacao(nome, idade)
    declarar mensagem como "Olá " + nome
    mostrar mensagem + ", você tem " + idade + " anos"
fim_função

# Chamada da função
saudacao("Maria", 16)
```

#### Listas (Arrays)

```brasilscript
declarar numeros como lista[1, 2, 3, 4, 5]
declarar nomes como lista["Ana", "João", "Maria"]

# Acessar elementos
mostrar numeros[0] # Primeiro elemento

# Percorrer lista
para_cada nome em nomes faça
    mostrar "Nome: " + nome
fim_para_cada
```

### 2.4 Exemplo Completo: Calculadora Simples

```brasilscript
# Programa: Calculadora Simples em BrasilScript

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
    se num2 ≠ 0 então
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

---