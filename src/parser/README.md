# 🚀 Parser do BrasilScript

Este diretório contém a implementação do analisador sintático (parser) para a linguagem BrasilScript.

## 📁 Estrutura

- `brasilscript_parser.py` - Implementação do parser recursivo descendente
- `test_parser.py` - Testes unitários para o parser
- `../docs/gramatica_parser.md` - Documentação da gramática formal

## 🎯 Características

### Parser Recursivo Descendente
- **Técnica**: Recursive Descent Parser (RDP)
- **Gramática**: LL(1) - sem recursão à esquerda
- **AST**: Geração de Árvore Sintática Abstrata
- **Tratamento de erros**: Mensagens descritivas de erro

### Estruturas Suportadas

#### ✅ Declarações
```brasilscript
declarar nome como texto
declarar idade como numero = 25
declarar ativo como logico = verdadeiro
declarar numeros como lista[numero]
```

#### ✅ Atribuições
```brasilscript
nome = "Maria"
idade = idade + 1
```

#### ✅ Estruturas de Controle
```brasilscript
# Condicional
se idade >= 18 entao
    mostrar "Maior de idade"
senao_se idade >= 16 entao
    mostrar "Pode votar"
senao
    mostrar "Menor de idade"
fim_se

# Loop while
enquanto contador < 10 faca
    contador = contador + 1
fim_enquanto

# Loop repeat
repetir 5 vezes
    mostrar "Repetindo..."
fim_repetir

# Loop for-each
para_cada item em lista faca
    mostrar item
fim_para_cada
```

#### ✅ Funções
```brasilscript
funcao somar(a, b)
    declarar resultado como numero
    resultado = a + b
    retornar resultado
fim_funcao

# Chamada de função
resultado = somar(10, 20)
```

#### ✅ I/O
```brasilscript
mostrar "Olá, mundo!"
mostrar "Nome: " + nome + ", Idade: " + idade

perguntar "Digite seu nome: " guardar_em nome
```

#### ✅ Expressões
```brasilscript
# Aritméticas (com precedência correta)
resultado = a + b * 2 - c / d

# Lógicas
condicao = x > 5 e y < 10 ou nao z

# Com parênteses
resultado = (a + b) * (c - d)
```

#### ✅ Listas
```brasilscript
# Literal de lista
numeros = [1, 2, 3, 4, 5]

# Acesso por índice
primeiro = numeros[0]
```

## 🔧 Como Usar

### Exemplo Básico
```python
from src.parser.brasilscript_parser import parse_brasilscript

code = '''
declarar nome como texto = "BrasilScript"
declarar versao como numero = 1.0

mostrar "Linguagem: " + nome
mostrar "Versão: " + versao

se versao >= 1.0 entao
    mostrar "Versão estável!"
fim_se
'''

try:
    ast = parse_brasilscript(code)
    print("✅ Parse realizado com sucesso!")
    print(f"Statements encontrados: {len(ast.statements)}")
except ParseError as e:
    print(f"❌ Erro de sintaxe: {e}")
```

### Analisando a AST
```python
from src.parser.brasilscript_parser import *

# Parse do código
ast = parse_brasilscript("declarar x como numero = 42")

# Primeira declaração
decl = ast.statements[0]
print(f"Tipo: {type(decl).__name__}")  # Declaration
print(f"Variável: {decl.identifier}")   # x
print(f"Tipo: {decl.type_name}")        # numero
print(f"Valor: {decl.initial_value.value}")  # 42
```

## 🧪 Executando Testes

### Testes Básicos
```bash
cd /path/to/brasilScript
python src/parser/test_parser.py
```

### Com pytest (se disponível)
```bash
cd /path/to/brasilScript
python -m pytest src/parser/test_parser.py -v
```

### Teste Manual
```python
from src.parser.test_parser import TestBrasilScriptParser

test = TestBrasilScriptParser()
test.test_simple_declaration()
test.test_arithmetic_expression()
print("✅ Testes passaram!")
```

## 📊 Hierarquia da AST

```
Program
├── Statement*
    ├── Declaration (identificador, tipo, valor_inicial?)
    ├── Assignment (identificador, valor)
    ├── IfStatement (condição, bloco_then, senao_ses[], bloco_else?)
    ├── WhileStatement (condição, corpo)
    ├── RepeatStatement (contagem, corpo)
    ├── ForEachStatement (variável, iterável, corpo)
    ├── FunctionDecl (nome, parâmetros[], corpo[])
    ├── PrintStatement (expressões[])
    ├── InputStatement (prompt, variável)
    ├── ReturnStatement (valor?)
    └── FunctionCall (nome, argumentos[])

Expression
├── BinaryOperation (esquerda, operador, direita)
├── UnaryOperation (operador, operando)
├── Literal (valor, tipo)
├── Identifier (nome)
├── ListLiteral (elementos[])
├── IndexAccess (objeto, índice)
└── FunctionCall (nome, argumentos[])
```

## 🔧 Precedência de Operadores

1. **Parênteses**: `( )`
2. **Acesso/Chamada**: `[index]`, `func()`
3. **Unário**: `-`, `nao`
4. **Multiplicativo**: `*`, `/`, `%`
5. **Aditivo**: `+`, `-`
6. **Relacional**: `<`, `<=`, `>`, `>=`, `==`, `!=`
7. **Lógico E**: `e`
8. **Lógico OU**: `ou`
9. **Atribuição**: `=`

## ⚠️ Limitações Atuais

- **Não implementado**: Classes, módulos, importações
- **Simplificado**: Tratamento de erros (apenas ParseError básico)
- **Pendente**: Análise semântica (tipos, escopo)
- **Faltando**: Otimizações (tail call, constant folding)

## 🚧 Próximos Passos

1. **Análise Semântica**: Verificação de tipos e escopo
2. **Geração de Código**: Tradução para Python/bytecode
3. **Melhor tratamento de erros**: Recuperação de erros, múltiplos erros
4. **Otimizações**: Constant folding, dead code elimination
5. **Debugging**: Source maps, stack traces

## 🤝 Contribuindo

Para adicionar novas features à gramática:

1. Atualize a gramática formal em `docs/gramatica_parser.md`
2. Adicione os novos nós AST em `brasilscript_parser.py`
3. Implemente os métodos de parse correspondentes
4. Adicione testes em `test_parser.py`
5. Atualize esta documentação

## 📚 Referências

- **Teoria**: "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- **Técnica**: Recursive Descent Parsing
- **Gramática**: Extended Backus-Naur Form (EBNF)
- **AST**: Abstract Syntax Tree design patterns
