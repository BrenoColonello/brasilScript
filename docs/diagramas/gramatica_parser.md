# 📝 Gramática Formal do BrasilScript

## 💡 Definição Formal da Gramática

G = (V, Σ, P, S)

onde:

* **V** (variáveis / não-terminais):
  `{Program, Statement, StatementList, Declaration, VarDecl, FuncDecl, Assignment,
   Expression, Term, Factor, Condition, Block, IfStmt, WhileStmt, ForStmt, RepeatStmt,
   PrintStmt, InputStmt, ReturnStmt, FuncCall, ActualParams, FormalParams, Type,
   Identifier, Literal, RelOp, ArithOp, MulOp, LogicalOp}`

* **Σ** (terminais):
  Palavras reservadas, símbolos e identificadores do BrasilScript:
  `{declarar, como, mostrar, perguntar, guardar_em, se, entao, senao, senao_se, fim_se,
   enquanto, faca, fim_enquanto, repetir, vezes, fim_repetir, para_cada, em, fim_para_cada,
   funcao, fim_funcao, retornar, parar, e, ou, nao, lista, numero, texto, logico,
   verdadeiro, falso, IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, =, ==, !=, <, <=,
   >, >=, +, -, *, /, %, (, ), [, ], {, }, ,, ., :, ;, \n}`

* **S** (símbolo inicial):
  `Program`

* **P** (regras de produção):
  O conjunto de produções segue abaixo, no formato EBNF.

---

## 📘 Gramática em EBNF (Extended Backus–Naur Form)

```ebnf
Program       = StatementList .

StatementList = { Statement } .

Statement     = Declaration
              | Assignment  
              | IfStmt
              | WhileStmt
              | RepeatStmt
              | ForStmt
              | PrintStmt
              | InputStmt
              | ReturnStmt
              | FuncCall
              | FuncDecl
              | "parar" .

Declaration   = "declarar" Identifier "como" Type [ "=" Expression ] .

Type          = "numero" | "texto" | "logico" 
              | "lista" [ "[" Type "]" ] .

Assignment    = Identifier "=" Expression .

FuncDecl      = "funcao" Identifier "(" [ FormalParams ] ")" 
                StatementList 
                "fim_funcao" .

FormalParams  = Identifier { "," Identifier } .

IfStmt        = "se" Condition "entao" 
                StatementList 
                { "senao_se" Condition "entao" StatementList }
                [ "senao" StatementList ]
                "fim_se" .

WhileStmt     = "enquanto" Condition "faca" 
                StatementList 
                "fim_enquanto" .

RepeatStmt    = "repetir" Expression "vezes" 
                StatementList 
                "fim_repetir" .

ForStmt       = "para_cada" Identifier "em" Expression "faca" 
                StatementList 
                "fim_para_cada" .

PrintStmt     = "mostrar" Expression { "," Expression } .

InputStmt     = "perguntar" Expression "guardar_em" Identifier .

ReturnStmt    = "retornar" [ Expression ] .

FuncCall      = Identifier "(" [ ActualParams ] ")" .

ActualParams  = Expression { "," Expression } .

Condition     = Expression RelOp Expression 
              | Expression
              | "nao" Condition
              | Condition LogicalOp Condition .

Expression    = Term { ArithOp Term } .

Term          = Factor { MulOp Factor } .

Factor        = Identifier
              | Literal
              | FuncCall
              | "(" Expression ")"
              | "[" [ ActualParams ] "]"  (* Lista literal *)
              | Identifier "[" Expression "]" . (* Acesso a lista *)

RelOp         = "==" | "!=" | "<" | "<=" | ">" | ">=" | "=" .

ArithOp       = "+" | "-" .

MulOp         = "*" | "/" | "%" .

LogicalOp     = "e" | "ou" .

Literal       = NUMERO_LITERAL | STRING_LITERAL | "verdadeiro" | "falso" .

Identifier    = IDENTIFICADOR .
```

---

## 📘 Gramática em BNF (Backus–Naur Form)

```bnf
<Program>        ::= <StatementList>

<StatementList>  ::= <Statement> <StatementList>
                   | ε

<Statement>      ::= <Declaration>
                   | <Assignment>
                   | <IfStmt>
                   | <WhileStmt>
                   | <RepeatStmt>
                   | <ForStmt>
                   | <PrintStmt>
                   | <InputStmt>
                   | <ReturnStmt>
                   | <FuncCall>
                   | <FuncDecl>
                   | "parar"

<Declaration>    ::= "declarar" <Identifier> "como" <Type> <InitOpt>

<InitOpt>        ::= "=" <Expression>
                   | ε

<Type>           ::= "numero"
                   | "texto"
                   | "logico"
                   | "lista" <TypeOpt>

<TypeOpt>        ::= "[" <Type> "]"
                   | ε

<Assignment>     ::= <Identifier> "=" <Expression>

<FuncDecl>       ::= "funcao" <Identifier> "(" <FormalParamsOpt> ")" 
                     <StatementList> 
                     "fim_funcao"

<FormalParamsOpt> ::= <FormalParams>
                    | ε

<FormalParams>   ::= <Identifier> <FormalParamsTail>

<FormalParamsTail> ::= "," <Identifier> <FormalParamsTail>
                     | ε

<IfStmt>         ::= "se" <Condition> "entao" 
                     <StatementList> 
                     <ElseIfSeq>
                     <ElseOpt>
                     "fim_se"

<ElseIfSeq>      ::= "senao_se" <Condition> "entao" <StatementList> <ElseIfSeq>
                   | ε

<ElseOpt>        ::= "senao" <StatementList>
                   | ε

<WhileStmt>      ::= "enquanto" <Condition> "faca" 
                     <StatementList> 
                     "fim_enquanto"

<RepeatStmt>     ::= "repetir" <Expression> "vezes" 
                     <StatementList> 
                     "fim_repetir"

<ForStmt>        ::= "para_cada" <Identifier> "em" <Expression> "faca" 
                     <StatementList> 
                     "fim_para_cada"

<PrintStmt>      ::= "mostrar" <Expression> <PrintTail>

<PrintTail>      ::= "," <Expression> <PrintTail>
                   | ε

<InputStmt>      ::= "perguntar" <Expression> "guardar_em" <Identifier>

<ReturnStmt>     ::= "retornar" <ExprOpt>

<ExprOpt>        ::= <Expression>
                   | ε

<FuncCall>       ::= <Identifier> "(" <ActualParamsOpt> ")"

<ActualParamsOpt> ::= <ActualParams>
                    | ε

<ActualParams>   ::= <Expression> <ActualParamsTail>

<ActualParamsTail> ::= "," <Expression> <ActualParamsTail>
                     | ε

<Condition>      ::= <OrCondition>

<OrCondition>    ::= <AndCondition> <OrConditionTail>

<OrConditionTail> ::= "ou" <AndCondition> <OrConditionTail>
                    | ε

<AndCondition>   ::= <NotCondition> <AndConditionTail>

<AndConditionTail> ::= "e" <NotCondition> <AndConditionTail>
                     | ε

<NotCondition>   ::= "nao" <PrimaryCondition>
                   | <PrimaryCondition>

<PrimaryCondition> ::= <Expression> <RelOpOpt>
                     | "(" <Condition> ")"

<RelOpOpt>       ::= <RelOp> <Expression>
                   | ε

<Expression>     ::= <Term> <ExpressionTail>

<ExpressionTail> ::= <ArithOp> <Term> <ExpressionTail>
                   | ε

<Term>           ::= <Factor> <TermTail>

<TermTail>       ::= <MulOp> <Factor> <TermTail>
                   | ε

<Factor>         ::= <Identifier>
                   | <Literal>
                   | <FuncCall>
                   | "(" <Expression> ")"
                   | "[" <ListLiteralOpt> "]"
                   | <Identifier> "[" <Expression> "]" 

<ListLiteralOpt> ::= <ActualParams>
                   | ε

<RelOp>          ::= "=="
                   | "!="
                   | "<"
                   | "<="
                   | ">"
                   | ">="
                   | "="

<ArithOp>        ::= "+"
                   | "-"

<MulOp>          ::= "*"
                   | "/"
                   | "%"

<Literal>        ::= NUMERO_LITERAL
                   | STRING_LITERAL
                   | "verdadeiro"
                   | "falso"

<Identifier>     ::= IDENTIFICADOR
```

---

## 🧩 Características da Gramática

* **Livre de contexto (CFL)**: Adequada para análise sintática.
* **Recursão descendente**: Evita recursão à esquerda, facilitando implementação de parsers recursivos.
* **Precedência de operadores**: Implementada através da hierarquia Factor → Term → Expression.
* **Estruturas de controle**: Suporte completo para condicionais, loops e funções.
* **Tipos de dados**: Suporte para números, texto, lógico e listas.
* **Expressões lógicas**: Operadores `e`, `ou` e `nao` com precedência adequada.

---

## 🎯 Características Específicas do BrasilScript

### Palavras-chave em Português

* Declarações: `declarar`, `como`
* Controle de fluxo: `se`, `entao`, `senao`, `senao_se`, `fim_se`
* Loops: `enquanto`, `faca`, `fim_enquanto`, `repetir`, `vezes`, `fim_repetir`
* Funções: `funcao`, `fim_funcao`, `retornar`
* I/O: `mostrar`, `perguntar`, `guardar_em`
* Operadores lógicos: `e`, `ou`, `nao`
* Tipos: `numero`, `texto`, `logico`, `lista`
* Literais: `verdadeiro`, `falso`

### Estruturas Sintáticas Únicas

1. **Declaração com inicialização**: `declarar x como numero = 10`
2. **Input com destino**: `perguntar "Nome:" guardar_em nome`
3. **Blocos delimitados por palavras**: `se...fim_se`, `funcao...fim_funcao`
4. **Loop com contagem**: `repetir 5 vezes`
5. **For-each**: `para_cada item em lista faca`

### Precedência de Operadores

1. **Parênteses**: `( )`
2. **Acesso a array**: `[index]`
3. **Chamada de função**: `func()`
4. **Unário**: `-`, `nao`
5. **Multiplicativo**: `*`, `/`, `%`
6. **Aditivo**: `+`, `-`
7. **Relacional**: `<`, `<=`, `>`, `>=`, `==`, `!=`
8. **Lógico E**: `e`
9. **Lógico OU**: `ou`
10. **Atribuição**: `=`

---

## 🔧 Implementação Sugerida

Esta gramática pode ser implementada usando:

* **Parser recursivo descendente** (mais simples)
* **Parser LL(1)** (com tabela de análise)
* **Parser LR(1)** (mais poderoso, mas complexo)

A gramática foi projetada para ser **LL(1)**, facilitando a implementação de um parser recursivo descendente manual ou usando geradores como ANTLR4.
