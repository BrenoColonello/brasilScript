# Projeto Integrador - Linguagem de Programação Educacional

## BrasilScript
### Linguagem de Programação Educacional em Português Brasileiro

**Universidade de Marília - UNIMAR**

---

### Equipe de Desenvolvimento

- **Breno** - Gerente de Projeto e Desenvolvedor de Sintaxe
- **Leandro** - Desenvolvedor de Interpretador e Arquitetura
- **Caio** - Documentador e Designer de Interface
- **Gabriel** - Especialista em Testes e Quality Assurance

### Informações do Projeto

- **Período:** 15 semanas (Entrega parcial na 6ª semana)
- **Instituição:** Universidade de Marília - UNIMAR
- **Curso:** Ciência da Computação
- **Data de Início:** Março 2024

---

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

## 3. Cronograma Detalhado e Planejamento do Projeto

### 3.1 Cronograma de 15 Semanas

#### Fase 1: Planejamento e Fundamentos (Semanas 1-3)

##### Semana 1: Formação da Equipe e Proposta Inicial
- Definição de papéis e responsabilidades
- Criação da proposta inicial da linguagem
- Estabelecimento do diário de desenvolvimento
- Pesquisa de linguagens similares e referências

**Entrega:** Proposta Inicial (3 páginas)

##### Semana 2: Especificação Detalhada da Sintaxe
- Definição completa da gramática da linguagem
- Criação de exemplos de código para todas as estruturas
- Especificação de tipos de dados e operadores
- Definição de palavras-chave e convenções

**Entrega:** Especificação da Sintaxe

##### Semana 3: Arquitetura do Interpretador
- Design da arquitetura do interpretador
- Especificação do analisador léxico (tokenização)
- Design do analisador sintático (parser)
- Planejamento da estrutura de dados interna

**Entrega:** Documento de Arquitetura

#### Fase 2: Desenvolvimento Core (Semanas 4-9)

##### Semana 4: Analisador Léxico (Tokenizer)
- Implementação do tokenizer em Python
- Reconhecimento de palavras-chave em português
- Identificação de operadores e delimitadores
- Testes unitários para o tokenizer

##### Semana 5: Analisador Sintático (Parser)
- Implementação do parser recursivo descendente
- Construção da árvore sintática abstrata (AST)
- Tratamento de erros sintáticos
- Testes de parsing para estruturas básicas

##### Semana 6: ENTREGA PARCIAL - Avaliação Intermediária
- Apresentação do progresso para avaliação
- Demonstração do tokenizer e parser funcionais
- Relatório de progresso e dificuldades
- Feedback e ajustes no cronograma

**Entrega:** Protótipo Funcional + Relatório

##### Semana 7: Interpretador - Estruturas Básicas
- Implementação de variáveis e atribuições
- Operações aritméticas e lógicas
- Comandos de entrada e saída (mostrar, perguntar)
- Sistema de tipos básicos (número, texto, lógico)

##### Semana 8: Estruturas de Controle
- Implementação de condicionais (se, senão_se, senão)
- Estruturas de repetição (enquanto, repetir)
- Controle de fluxo e escopo de variáveis
- Testes de integração das estruturas

##### Semana 9: Funções e Estruturas de Dados
- Implementação de funções definidas pelo usuário
- Sistema de parâmetros e valores de retorno
- Implementação de listas (arrays)
- Operações com listas (acesso, modificação, iteração)

#### Fase 3: Interface e Documentação (Semanas 10-12)

##### Semana 10: Interface de Desenvolvimento
- Desenvolvimento de IDE web simples
- Editor de código com highlight de sintaxe
- Console integrado para execução
- Sistema de salvamento de arquivos

##### Semana 11: Documentação e Tutoriais
- Manual completo da linguagem
- Tutoriais passo-a-passo para iniciantes
- Galeria de exemplos práticos
- Guia de referência rápida

##### Semana 12: Sistema de Ajuda e Feedback
- Mensagens de erro claras e educativas
- Sistema de sugestões automáticas
- Help interativo dentro do IDE
- Testes de usabilidade com usuários

#### Fase 4: Testes e Finalização (Semanas 13-15)

##### Semana 13: Testes e Validação
- Testes extensivos com casos reais
- Correção de bugs e otimizações
- Validação com educadores e estudantes
- Benchmarks de performance

##### Semana 14: Preparação da Apresentação
- Criação de slides e material de apresentação
- Preparação de demonstrações ao vivo
- Ensaios da apresentação final
- Finalização da documentação técnica

##### Semana 15: ENTREGA FINAL
- Apresentação final do projeto
- Demonstração completa da linguagem
- Entrega de todo o código e documentação
- Avaliação final e feedback

**Entrega:** Projeto Completo + Apresentação

### 3.2 Divisão de Responsabilidades

#### Breno - Gerente de Projeto e Desenvolvedor de Sintaxe
- ✓ Coordenação geral do projeto
- ✓ Definição da sintaxe da linguagem
- ✓ Criação de exemplos de código
- ✓ Controle de cronograma e entregas
- ✓ Comunicação com orientadores

#### Caio - Desenvolvedor de Interpretador e Arquitetura
- ✓ Implementação do interpretador
- ✓ Design da arquitetura do sistema
- ✓ Desenvolvimento do parser e tokenizer
- ✓ Otimização de performance
- ✓ Testes técnicos e debugging

#### Leandro - Documentador e Designer de Interface
- ✓ Criação da documentação completa
- ✓ Design da interface do IDE
- ✓ Desenvolvimento de tutoriais
- ✓ Testes de usabilidade
- ✓ Material de apresentação

#### Gabriel - Documentador e Designer de Interface
- ✓ Criação da documentação completa
- ✓ Design da interface do IDE
- ✓ Desenvolvimento de tutoriais
- ✓ Testes de usabilidade
- ✓ Material de apresentação

### 3.3 Ferramentas e Tecnologias

#### Desenvolvimento
- **Python 3.9+:** Linguagem base para o interpretador
- **PLY (Python Lex-Yacc):** Para parser e tokenizer
- **Flask:** Framework web para o IDE
- **HTML/CSS/JavaScript:** Interface do usuário
- **Git/GitHub:** Controle de versão

#### Documentação e Design
- **Markdown:** Documentação técnica
- **Figma:** Design de interface
- **Canva:** Material de apresentação
- **Draw.io:** Diagramas e fluxogramas
- **Notion:** Diário de desenvolvimento

### Riscos e Mitigações

#### Risco: Complexidade técnica alta
**Mitigação:** Começar com MVP simples e expandir gradualmente

#### Risco: Divergência na equipe
**Mitigação:** Reuniões semanais e comunicação constante

---

## 4. Diário de Desenvolvimento

O Diário de Desenvolvimento será mantido colaborativamente pela equipe utilizando a plataforma Notion, permitindo registro em tempo real do progresso, decisões e reflexões sobre o projeto.

### Semana 1 - Dia 1: Formação da Equipe
**Data:** [Data da primeira reunião]

Realizamos nossa primeira reunião de equipe para definir os papéis e discutir a proposta inicial. Decidimos que a BrasilScript deve focar na simplicidade extrema, sendo ainda mais acessível que o Python.

**Decisões:** Uso do português brasileiro, sintaxe natural, foco educacional

### Semana 1 - Dia 3: Pesquisa de Referências
**Data:** [Data da pesquisa]

Estudamos linguagens como Scratch, Logo e Python para entender diferentes abordagens educacionais. Identificamos que a barreira linguística é realmente um fator limitante no Brasil.

**Insights:** Necessidade de syntax highlighting, mensagens de erro claras

### Semana 1 - Dia 5: Definição da Sintaxe Base
**Data:** [Data da definição]

Estabelecemos as primeiras palavras-chave: declarar, mostrar, perguntar, se, senão, enquanto. A equipe está animada com a naturalidade da sintaxe proposta.

**Próximos passos:** Finalizar especificação completa da gramática

---

**Nota:** Este diário será atualizado diariamente durante todo o projeto, documentando progressos, dificuldades e soluções encontradas pela equipe.

---

## Projeto Integrador - BrasilScript
**Universidade de Marília - UNIMAR | Ciência da Computação | 2024**
