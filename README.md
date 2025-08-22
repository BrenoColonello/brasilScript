# BrasilScript 📚

## Linguagem de Programação Educacional em Português Brasileiro

**Universidade de Marília - UNIMAR**  
**Projeto Integrador - Ciência da Computação**

---

## 📋 Objetivos da Semana

Aplicar conceitos de alfabetos, palavras e linguagens na definição formal dos elementos básicos da linguagem.

## 🎯 Atividades do Projeto Integrador

Esta semana marca o início da especificação formal da linguagem. Definimos o alfabeto básico da linguagem (quais caracteres são válidos), especificamos os diferentes tipos de tokens (identificadores, números, operadores, palavras-chave), e estabelecemos a estrutura léxica geral.

Utilizamos as operações com linguagens estudadas para especificar conjuntos complexos de tokens. A aplicação prática dos conceitos de fechamento de Kleene é evidente na definição de comentários, strings, e outros elementos que podem ter comprimento variável.

---

## 🏗️ Especificação Formal da Linguagem

### 1. Alfabeto da Linguagem (Σ)

O alfabeto da BrasilScript é definido como:

```
Σ = {a, b, c, ..., z, A, B, C, ..., Z, 0, 1, 2, ..., 9, 
     +, -, *, /, =, <, >, <=, >=, ==, !=, 
     (, ), [, ], {, }, ", ', #, _, ., 
     espaço, tab, quebra_de_linha, 
     ç, ã, õ, é, ê, í, ó, ô, ú, ü}
```

**Características do Alfabeto:**
- **Case-sensitive:** Distingue entre maiúsculas e minúsculas
- **Acentos:** Suporta caracteres acentuados do português
- **Unicode:** Compatível com UTF-8 para caracteres especiais

### 2. Definição Formal dos Tokens

#### 2.1 Identificadores (ID)

```
ID = (letra | _) (letra | dígito | _)*
```

**Onde:**
- `letra = a | b | c | ... | z | A | B | C | ... | Z | ç | ã | õ | é | ê | í | ó | ô | ú | ü`
- `dígito = 0 | 1 | 2 | ... | 9`

**Exemplos válidos:**
- `nome`, `idade_aluno`, `primeiroNome`, `número1`, `_variável`

**Exemplos inválidos:**
- `1nome` (não pode começar com dígito)
- `nome-completo` (hífen não é permitido)

#### 2.2 Literais Numéricos

**Inteiros:**
```
INTEIRO = dígito+
```

**Decimais:**
```
DECIMAL = dígito+ . dígito+
```

**Notação Científica:**
```
CIENTIFICO = (dígito+ | dígito+ . dígito+) [e|E] [+|-]? dígito+
```

**Exemplos:**
- `123`, `3.14`, `1.5e-3`, `2E+10`

#### 2.3 Strings

```
STRING = " (caractere | escape)* "
```

**Onde:**
- `caractere = qualquer_caractere_exceto_aspas`
- `escape = \\ | \" | \n | \t`

**Exemplos:**
- `"Olá, mundo!"`
- `"Linha 1\nLinha 2"`
- `"Caminho: C:\\arquivo.txt"`

#### 2.4 Comentários

```
COMENTARIO = # (caractere)* quebra_de_linha
```

**Exemplos:**
- `# Este é um comentário`
- `# Calcula a média dos números`

#### 2.5 Palavras-Chave

```
PALAVRAS_CHAVE = {
    declarar, como, mostrar, perguntar, guardar_em,
    se, então, senão, senão_se, fim_se,
    enquanto, faça, fim_enquanto,
    repetir, vezes, fim_repetir,
    para_cada, em, fim_para_cada,
    função, fim_função,
    lista, parar
}
```

#### 2.6 Operadores

**Operadores Aritméticos:**
```
OP_ARITMETICO = + | - | * | / | %
```

**Operadores de Comparação:**
```
OP_COMPARACAO = = | != | < | > | <= | >=
```

**Operadores de Atribuição:**
```
OP_ATRIBUICAO = = | += | -= | *= | /=
```

#### 2.7 Delimitadores

```
DELIMITADOR = ( | ) | [ | ] | { | } | , | ;
```

### 3. Gramática Léxica Completa

```
TOKEN = PALAVRA_CHAVE | ID | INTEIRO | DECIMAL | CIENTIFICO | 
        STRING | OP_ARITMETICO | OP_COMPARACAO | OP_ATRIBUICAO | 
        DELIMITADOR | COMENTARIO

PROGRAMA = TOKEN*
```

### 4. Regras de Análise Léxica

1. **Longest Match:** Sempre reconhecer o token mais longo possível
2. **Case Sensitivity:** Identificadores são case-sensitive
3. **Espaços em Branco:** Ignorados entre tokens, exceto em strings
4. **Comentários:** Ignorados durante a análise léxica
5. **Quebras de Linha:** Significativas para estrutura de blocos

---

## 💡 Reflexões Importantes

### Experiência do Usuário

- **Case-sensitive:** Decidimos manter case-sensitivity para preparar os estudantes para linguagens profissionais
- **Caracteres Especiais:** Permitimos acentos em identificadores para naturalidade
- **Espaços em Branco:** Ignorados entre tokens, mas significativos para indentação de blocos
- **Mensagens de Erro:** Desenvolvidas em português para facilitar debugging

### Resolução de Ambiguidades

- **Identificadores vs Números:** Identificadores não podem começar com dígitos
- **Operadores vs Atribuições:** Contexto determina se `=` é comparação ou atribuição
- **Strings vs Comentários:** Aspas duplas sempre iniciam strings, `#` sempre inicia comentários

---

## 📊 Exemplos de Programas Válidos

### Exemplo 1: Hello World
```brasilscript
# Programa: Olá, Mundo!
mostrar "Olá, mundo!"
```

### Exemplo 2: Calculadora Simples
```brasilscript
# Programa: Calculadora
declarar num1 como 10
declarar num2 como 5
declarar resultado como num1 + num2
mostrar "Resultado: " + resultado
```

### Exemplo 3: Estruturas Condicionais
```brasilscript
# Programa: Verificação de Idade
declarar idade como 18

se idade >= 18 então
    mostrar "Maior de idade"
senão
    mostrar "Menor de idade"
fim_se
```

### Exemplo 4: Estruturas de Repetição
```brasilscript
# Programa: Contador
declarar contador como 0

enquanto contador < 5 faça
    mostrar "Contador: " + contador
    contador = contador + 1
fim_enquanto
```

### Exemplo 5: Funções e Listas
```brasilscript
# Programa: Lista de Nomes
declarar nomes como lista["Ana", "João", "Maria"]

função saudar(nome)
    mostrar "Olá, " + nome + "!"
fim_função

para_cada nome em nomes faça
    saudar(nome)
fim_para_cada
```

---

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8+
- Git

### Instalação
```bash
git clone https://github.com/seu-usuario/brasilscript.git
cd brasilscript
pip install -r requirements.txt
```

### Execução
```bash
python brasilscript.py arquivo.bs
```

---

## 👥 Equipe de Desenvolvimento

- **Breno** - Gerente de Projeto e Desenvolvedor de Sintaxe
- **Leandro** - Desenvolvedor de Interpretador e Arquitetura  
- **Caio** - Documentador e Designer de Interface
- **Gabriel** - Especialista em Testes e Quality Assurance

---

## 📅 Cronograma

- **Semana 1-2:** Especificação formal da linguagem ✅
- **Semana 3-4:** Implementação do analisador léxico
- **Semana 5-6:** Implementação do analisador sintático
- **Semana 7-8:** Implementação do interpretador
- **Semana 9-10:** Desenvolvimento do ambiente de desenvolvimento
- **Semana 11-12:** Testes e documentação
- **Semana 13-15:** Refinamentos e entrega final

---

## 📝 Licença

Este projeto é desenvolvido para fins educacionais na Universidade de Marília - UNIMAR.

---

## 🔗 Links Úteis

- [Proposta Inicial](PropostaInicial.md)
- [Diário de Desenvolvimento](DiariodeDesenvolvimento.md)
- [Cronograma](Cronograma.md)
- [Membros da Equipe](Membros.md)

---

**Universidade de Marília - UNIMAR | Ciência da Computação | 2024**
