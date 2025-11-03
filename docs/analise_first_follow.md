# 📚 Análise FIRST e FOLLOW da Gramática BrasilScript

## 🎯 Objetivo

Este documento apresenta a análise dos conjuntos FIRST e FOLLOW para cada produção da gramática BrasilScript, e determina se a gramática é LL(1).

## 📝 Gramática BrasilScript (BNF)

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

## 🔍 Conjuntos FIRST

### Terminais
```
FIRST("declarar") = {"declarar"}
FIRST("como") = {"como"}
FIRST("numero") = {"numero"}
FIRST("texto") = {"texto"}
FIRST("logico") = {"logico"}
FIRST("lista") = {"lista"}
FIRST("=") = {"="}
FIRST("funcao") = {"funcao"}
FIRST("fim_funcao") = {"fim_funcao"}
FIRST("se") = {"se"}
FIRST("entao") = {"entao"}
FIRST("senao_se") = {"senao_se"}
FIRST("senao") = {"senao"}
FIRST("fim_se") = {"fim_se"}
FIRST("enquanto") = {"enquanto"}
FIRST("faca") = {"faca"}
FIRST("fim_enquanto") = {"fim_enquanto"}
FIRST("repetir") = {"repetir"}
FIRST("vezes") = {"vezes"}
FIRST("fim_repetir") = {"fim_repetir"}
FIRST("para_cada") = {"para_cada"}
FIRST("em") = {"em"}
FIRST("fim_para_cada") = {"fim_para_cada"}
FIRST("mostrar") = {"mostrar"}
FIRST("perguntar") = {"perguntar"}
FIRST("guardar_em") = {"guardar_em"}
FIRST("retornar") = {"retornar"}
FIRST("parar") = {"parar"}
FIRST("ou") = {"ou"}
FIRST("e") = {"e"}
FIRST("nao") = {"nao"}
FIRST("==") = {"=="}
FIRST("!=") = {"!="}
FIRST("<") = {"<"}
FIRST("<=") = {"<="}
FIRST(">") = {">"}
FIRST(">=") = {">="}
FIRST("+") = {"+"}
FIRST("-") = {"-"}
FIRST("*") = {"*"}
FIRST("/") = {"/"}
FIRST("%") = {"%"}
FIRST("(") = {"("}
FIRST(")") = {")"}
FIRST("[") = {"["}
FIRST("]") = {"]"}
FIRST(",") = {","}
FIRST("verdadeiro") = {"verdadeiro"}
FIRST("falso") = {"falso"}
FIRST(NUMERO_LITERAL) = {NUMERO_LITERAL}
FIRST(STRING_LITERAL) = {STRING_LITERAL}
FIRST(IDENTIFICADOR) = {IDENTIFICADOR}
```

### Não-terminais

#### Nível Superior
```
FIRST(<Program>) = FIRST(<StatementList>)
                 = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                    "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar", ε}

FIRST(<StatementList>) = FIRST(<Statement>) ∪ {ε}
                       = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                          "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar", ε}

FIRST(<Statement>) = FIRST(<Declaration>) ∪ FIRST(<Assignment>) ∪ FIRST(<IfStmt>) ∪
                     FIRST(<WhileStmt>) ∪ FIRST(<RepeatStmt>) ∪ FIRST(<ForStmt>) ∪ 
                     FIRST(<PrintStmt>) ∪ FIRST(<InputStmt>) ∪ FIRST(<ReturnStmt>) ∪
                     FIRST(<FuncCall>) ∪ FIRST(<FuncDecl>) ∪ {"parar"}
                   = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                      "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar"}
```

#### Declarações
```
FIRST(<Declaration>) = {"declarar"}

FIRST(<InitOpt>) = {"=", ε}

FIRST(<Type>) = {"numero", "texto", "logico", "lista"}

FIRST(<TypeOpt>) = {"[", ε}

FIRST(<Assignment>) = {IDENTIFICADOR}
```

#### Funções
```
FIRST(<FuncDecl>) = {"funcao"}

FIRST(<FormalParamsOpt>) = {IDENTIFICADOR, ε}

FIRST(<FormalParams>) = {IDENTIFICADOR}

FIRST(<FormalParamsTail>) = {",", ε}

FIRST(<FuncCall>) = {IDENTIFICADOR}

FIRST(<ActualParamsOpt>) = FIRST(<Expression>) ∪ {ε}
                         = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                            "verdadeiro", "falso", "(", "[", ε}

FIRST(<ActualParams>) = FIRST(<Expression>)
                      = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                         "verdadeiro", "falso", "(", "["}

FIRST(<ActualParamsTail>) = {",", ε}
```

#### Estruturas de Controle
```
FIRST(<IfStmt>) = {"se"}

FIRST(<ElseIfSeq>) = {"senao_se", ε}

FIRST(<ElseOpt>) = {"senao", ε}

FIRST(<WhileStmt>) = {"enquanto"}

FIRST(<RepeatStmt>) = {"repetir"}

FIRST(<ForStmt>) = {"para_cada"}
```

#### I/O
```
FIRST(<PrintStmt>) = {"mostrar"}

FIRST(<PrintTail>) = {",", ε}

FIRST(<InputStmt>) = {"perguntar"}

FIRST(<ReturnStmt>) = {"retornar"}

FIRST(<ExprOpt>) = FIRST(<Expression>) ∪ {ε}
                 = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                    "verdadeiro", "falso", "(", "[", ε}
```

#### Expressões e Condições
```
FIRST(<Condition>) = FIRST(<OrCondition>)
                   = FIRST(<AndCondition>)
                   = FIRST(<NotCondition>)
                   = {"nao"} ∪ FIRST(<PrimaryCondition>)
                   = {"nao", IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                      "verdadeiro", "falso", "(", "["}

FIRST(<OrCondition>) = FIRST(<AndCondition>)
                     = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                        "verdadeiro", "falso", "(", "[", "nao"}

FIRST(<OrConditionTail>) = {"ou", ε}

FIRST(<AndCondition>) = FIRST(<NotCondition>)
                      = {"nao", IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                         "verdadeiro", "falso", "(", "["}

FIRST(<AndConditionTail>) = {"e", ε}

FIRST(<NotCondition>) = {"nao"} ∪ FIRST(<PrimaryCondition>)
                      = {"nao", IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                         "verdadeiro", "falso", "(", "["}

FIRST(<PrimaryCondition>) = FIRST(<Expression>) ∪ {"("}
                          = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                             "verdadeiro", "falso", "(", "["}

FIRST(<RelOpOpt>) = {"==", "!=", "<", "<=", ">", ">=", "=", ε}

FIRST(<Expression>) = FIRST(<Term>)
                    = FIRST(<Factor>)
                    = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                       "verdadeiro", "falso", "(", "["}

FIRST(<ExpressionTail>) = {"+", "-", ε}

FIRST(<Term>) = FIRST(<Factor>)
              = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                 "verdadeiro", "falso", "(", "["}

FIRST(<TermTail>) = {"*", "/", "%", ε}

FIRST(<Factor>) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                   "verdadeiro", "falso", "(", "["}

FIRST(<ListLiteralOpt>) = FIRST(<ActualParams>) ∪ {ε}
                        = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                           "verdadeiro", "falso", "(", "[", ε}
```

#### Operadores
```
FIRST(<RelOp>) = {"==", "!=", "<", "<=", ">", ">=", "="}

FIRST(<ArithOp>) = {"+", "-"}

FIRST(<MulOp>) = {"*", "/", "%"}
```

#### Literais
```
FIRST(<Literal>) = {NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso"}

FIRST(<Identifier>) = {IDENTIFICADOR}
```

## 📤 Conjuntos FOLLOW

### Cálculo dos conjuntos FOLLOW

```
FOLLOW(<Program>) = {$}

FOLLOW(<StatementList>) = FOLLOW(<Program>) ∪ {"fim_se", "fim_enquanto", "fim_repetir", 
                                               "fim_para_cada", "fim_funcao", "senao_se", "senao"}
                        = {$, "fim_se", "fim_enquanto", "fim_repetir", 
                           "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Statement>) = FIRST(<StatementList>) - {ε} ∪ FOLLOW(<StatementList>)
                    = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                       "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                       $, "fim_se", "fim_enquanto", "fim_repetir", 
                       "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Declaration>) = FOLLOW(<Statement>)
                      = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                         "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                         $, "fim_se", "fim_enquanto", "fim_repetir", 
                         "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<InitOpt>) = FOLLOW(<Declaration>)
                  = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                     "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                     $, "fim_se", "fim_enquanto", "fim_repetir", 
                     "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Type>) = {"=", IDENTIFICADOR} ∪ FOLLOW(<InitOpt>) ∪ {"]"}
               = {"=", IDENTIFICADOR, "]", "declarar", "se", "enquanto", "repetir", 
                  "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                  $, "fim_se", "fim_enquanto", "fim_repetir", 
                  "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<TypeOpt>) = FOLLOW(<Type>)
                  = {"=", IDENTIFICADOR, "]", "declarar", "se", "enquanto", "repetir", 
                     "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                     $, "fim_se", "fim_enquanto", "fim_repetir", 
                     "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Assignment>) = FOLLOW(<Statement>)
                     = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                        "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                        $, "fim_se", "fim_enquanto", "fim_repetir", 
                        "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<FuncDecl>) = FOLLOW(<Statement>)
                   = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                      "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                      $, "fim_se", "fim_enquanto", "fim_repetir", 
                      "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<FormalParamsOpt>) = {")"}

FOLLOW(<FormalParams>) = FOLLOW(<FormalParamsOpt>)
                       = {")"}

FOLLOW(<FormalParamsTail>) = FOLLOW(<FormalParams>)
                           = {")"}

FOLLOW(<IfStmt>) = FOLLOW(<Statement>)
                 = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                    "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                    $, "fim_se", "fim_enquanto", "fim_repetir", 
                    "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<ElseIfSeq>) = FIRST(<ElseOpt>) ∪ {"fim_se"}
                    = {"senao", "fim_se"}

FOLLOW(<ElseOpt>) = {"fim_se"}

FOLLOW(<WhileStmt>) = FOLLOW(<Statement>)
                    = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                       "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                       $, "fim_se", "fim_enquanto", "fim_repetir", 
                       "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<RepeatStmt>) = FOLLOW(<Statement>)
                     = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                        "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                        $, "fim_se", "fim_enquanto", "fim_repetir", 
                        "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<ForStmt>) = FOLLOW(<Statement>)
                  = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                     "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                     $, "fim_se", "fim_enquanto", "fim_repetir", 
                     "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<PrintStmt>) = FOLLOW(<Statement>)
                    = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                       "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                       $, "fim_se", "fim_enquanto", "fim_repetir", 
                       "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<PrintTail>) = FOLLOW(<PrintStmt>)
                    = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                       "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                       $, "fim_se", "fim_enquanto", "fim_repetir", 
                       "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<InputStmt>) = FOLLOW(<Statement>)
                    = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                       "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                       $, "fim_se", "fim_enquanto", "fim_repetir", 
                       "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<ReturnStmt>) = FOLLOW(<Statement>)
                     = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                        "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                        $, "fim_se", "fim_enquanto", "fim_repetir", 
                        "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<ExprOpt>) = FOLLOW(<ReturnStmt>)
                  = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                     "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                     $, "fim_se", "fim_enquanto", "fim_repetir", 
                     "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<FuncCall>) = FOLLOW(<Statement>) ∪ FOLLOW(<Factor>)
                   = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", 
                      "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar",
                      $, "fim_se", "fim_enquanto", "fim_repetir", 
                      "fim_para_cada", "fim_funcao", "senao_se", "senao",
                      "+", "-", "*", "/", "%", ")", "]", ",", "==", "!=", 
                      "<", "<=", ">", ">=", "=", "e", "ou"}

FOLLOW(<ActualParamsOpt>) = {")"}

FOLLOW(<ActualParams>) = FOLLOW(<ActualParamsOpt>) ∪ FOLLOW(<ListLiteralOpt>)
                       = {")", "]"}

FOLLOW(<ActualParamsTail>) = FOLLOW(<ActualParams>)
                           = {")", "]"}

FOLLOW(<Condition>) = {"entao", ")"}

FOLLOW(<OrCondition>) = FOLLOW(<Condition>)
                      = {"entao", ")"}

FOLLOW(<OrConditionTail>) = FOLLOW(<OrCondition>)
                          = {"entao", ")"}

FOLLOW(<AndCondition>) = FIRST(<OrConditionTail>) - {ε} ∪ FOLLOW(<OrCondition>)
                       = {"ou", "entao", ")"}

FOLLOW(<AndConditionTail>) = FOLLOW(<AndCondition>)
                           = {"ou", "entao", ")"}

FOLLOW(<NotCondition>) = FIRST(<AndConditionTail>) - {ε} ∪ FOLLOW(<AndCondition>)
                       = {"e", "ou", "entao", ")"}

FOLLOW(<PrimaryCondition>) = FOLLOW(<NotCondition>)
                           = {"e", "ou", "entao", ")"}

FOLLOW(<RelOpOpt>) = FOLLOW(<PrimaryCondition>)
                   = {"e", "ou", "entao", ")"}

FOLLOW(<Expression>) = FIRST(<RelOpOpt>) - {ε} ∪ FOLLOW(<RelOpOpt>) ∪ 
                       {",", ")", "]", "vezes", "guardar_em"} ∪ 
                       FOLLOW(<ExprOpt>) ∪ FOLLOW(<PrintTail>)
                     = {"==", "!=", "<", "<=", ">", ">=", "=", "e", "ou", "entao", ")",
                        ",", "]", "vezes", "guardar_em", "declarar", IDENTIFICADOR, 
                        "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", 
                        "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", 
                        "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<ExpressionTail>) = FOLLOW(<Expression>)
                         = {"==", "!=", "<", "<=", ">", ">=", "=", "e", "ou", "entao", ")",
                            ",", "]", "vezes", "guardar_em", "declarar", IDENTIFICADOR, 
                            "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", 
                            "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", 
                            "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Term>) = FIRST(<ExpressionTail>) - {ε} ∪ FOLLOW(<Expression>)
               = {"+", "-", "==", "!=", "<", "<=", ">", ">=", "=", "e", "ou", "entao", ")",
                  ",", "]", "vezes", "guardar_em", "declarar", IDENTIFICADOR, 
                  "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", 
                  "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", 
                  "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<TermTail>) = FOLLOW(<Term>)
                   = {"+", "-", "==", "!=", "<", "<=", ">", ">=", "=", "e", "ou", "entao", ")",
                      ",", "]", "vezes", "guardar_em", "declarar", IDENTIFICADOR, 
                      "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", 
                      "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", 
                      "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}

FOLLOW(<Factor>) = FIRST(<TermTail>) - {ε} ∪ FOLLOW(<Term>)
                 = {"*", "/", "%", "+", "-", "==", "!=", "<", "<=", ">", ">=", "=", 
                    "e", "ou", "entao", ")", ",", "]", "vezes", "guardar_em", 
                    "declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", 
                    "mostrar", "perguntar", "retornar", "funcao", "parar", $, 
                    "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", 
                    "fim_funcao", "senao_se", "senao"}

FOLLOW(<ListLiteralOpt>) = {"]"}

FOLLOW(<RelOp>) = FIRST(<Expression>)
                = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                   "verdadeiro", "falso", "(", "["}

FOLLOW(<ArithOp>) = FIRST(<Term>)
                  = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                     "verdadeiro", "falso", "(", "["}

FOLLOW(<MulOp>) = FIRST(<Factor>)
                = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, 
                   "verdadeiro", "falso", "(", "["}

FOLLOW(<Literal>) = FOLLOW(<Factor>)
                  = {"*", "/", "%", "+", "-", "==", "!=", "<", "<=", ">", ">=", "=", 
                     "e", "ou", "entao", ")", ",", "]", "vezes", "guardar_em", 
                     "declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", 
                     "mostrar", "perguntar", "retornar", "funcao", "parar", $, 
                     "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", 
                     "fim_funcao", "senao_se", "senao"}

FOLLOW(<Identifier>) = FOLLOW(<Factor>) ∪ {"como", "=", "(", "[", ",", ")", "em", "guardar_em"}
                     = {"*", "/", "%", "+", "-", "==", "!=", "<", "<=", ">", ">=", "=", 
                        "e", "ou", "entao", ")", ",", "]", "vezes", "guardar_em", 
                        "declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", 
                        "mostrar", "perguntar", "retornar", "funcao", "parar", $, 
                        "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", 
                        "fim_funcao", "senao_se", "senao", "como", "(", "[", "em"}
```

## 🔍 Análise LL(1)

### Condições para uma gramática ser LL(1):

1. **Para cada produção A → α | β**, deve-se ter:
   - FIRST(α) ∩ FIRST(β) = ∅

2. **Para cada não-terminal A que possui ε-produções**:
   - FIRST(A) ∩ FOLLOW(A) = ∅

### Verificação das Condições

#### 1. Verificação de FIRST disjuntos

Vamos verificar os não-terminais com múltiplas produções:

**<StatementList>**:
- Produção 1: `<Statement> <StatementList>`
- Produção 2: `ε`
- FIRST(Statement StatementList) = FIRST(Statement) = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar"} ∩ {ε} = ∅

**<Statement>**:
- FIRST(<Declaration>) = {"declarar"}
- FIRST(<Assignment>) = {IDENTIFICADOR}
- FIRST(<IfStmt>) = {"se"}
- FIRST(<WhileStmt>) = {"enquanto"}
- FIRST(<RepeatStmt>) = {"repetir"}
- FIRST(<ForStmt>) = {"para_cada"}
- FIRST(<PrintStmt>) = {"mostrar"}
- FIRST(<InputStmt>) = {"perguntar"}
- FIRST(<ReturnStmt>) = {"retornar"}
- FIRST(<FuncCall>) = {IDENTIFICADOR}
- FIRST(<FuncDecl>) = {"funcao"}
- FIRST("parar") = {"parar"}

⚠️ **PROBLEMA**: FIRST(<Assignment>) ∩ FIRST(<FuncCall>) = {IDENTIFICADOR} ≠ ∅

**<InitOpt>**:
- FIRST("=" Expression) = {"="}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"="} ∩ {ε} = ∅

**<Type>**:
- FIRST("numero") = {"numero"}
- FIRST("texto") = {"texto"}
- FIRST("logico") = {"logico"}
- FIRST("lista" TypeOpt) = {"lista"}
- ✅ Todos disjuntos

**<TypeOpt>**:
- FIRST("[" Type "]") = {"["}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"["} ∩ {ε} = ∅

**<FormalParamsOpt>**:
- FIRST(FormalParams) = {IDENTIFICADOR}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {IDENTIFICADOR} ∩ {ε} = ∅

**<FormalParamsTail>**:
- FIRST("," Identifier FormalParamsTail) = {","}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {","} ∩ {ε} = ∅

**<ElseIfSeq>**:
- FIRST("senao_se" Condition "entao" StatementList ElseIfSeq) = {"senao_se"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"senao_se"} ∩ {ε} = ∅

**<ElseOpt>**:
- FIRST("senao" StatementList) = {"senao"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"senao"} ∩ {ε} = ∅

**<PrintTail>**:
- FIRST("," Expression PrintTail) = {","}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {","} ∩ {ε} = ∅

**<ExprOpt>**:
- FIRST(Expression) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["}
- FIRST(ε) = {ε}
- ✅ Disjuntos

**<ActualParamsOpt>**:
- FIRST(ActualParams) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["}
- FIRST(ε) = {ε}
- ✅ Disjuntos

**<ActualParamsTail>**:
- FIRST("," Expression ActualParamsTail) = {","}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {","} ∩ {ε} = ∅

**<OrConditionTail>**:
- FIRST("ou" AndCondition OrConditionTail) = {"ou"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"ou"} ∩ {ε} = ∅

**<AndConditionTail>**:
- FIRST("e" NotCondition AndConditionTail) = {"e"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"e"} ∩ {ε} = ∅

**<NotCondition>**:
- FIRST("nao" PrimaryCondition) = {"nao"}
- FIRST(PrimaryCondition) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["}
- ✅ Disjuntos: {"nao"} ∩ {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["} = ∅

**<PrimaryCondition>**:
- FIRST(Expression RelOpOpt) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["}
- FIRST("(" Condition ")") = {"("}
- ✅ Disjuntos (todos os primeiros já incluem "(")

**<RelOpOpt>**:
- FIRST(RelOp Expression) = {"==", "!=", "<", "<=", ">", ">=", "="}
- FIRST(ε) = {ε}
- ✅ Disjuntos

**<ExpressionTail>**:
- FIRST(ArithOp Term ExpressionTail) = {"+", "-"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"+", "-"} ∩ {ε} = ∅

**<TermTail>**:
- FIRST(MulOp Factor TermTail) = {"*", "/", "%"}
- FIRST(ε) = {ε}
- ✅ Disjuntos: {"*", "/", "%"} ∩ {ε} = ∅

**<Factor>**:
- FIRST(Identifier) = {IDENTIFICADOR}
- FIRST(Literal) = {NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso"}
- FIRST(FuncCall) = {IDENTIFICADOR}
- FIRST("(" Expression ")") = {"("}
- FIRST("[" ListLiteralOpt "]") = {"["}
- FIRST(Identifier "[" Expression "]") = {IDENTIFICADOR}

⚠️ **PROBLEMA**: FIRST(Identifier) ∩ FIRST(FuncCall) ∩ FIRST(Identifier "[" Expression "]") = {IDENTIFICADOR} ≠ ∅

**<ListLiteralOpt>**:
- FIRST(ActualParams) = {IDENTIFICADOR, NUMERO_LITERAL, STRING_LITERAL, "verdadeiro", "falso", "(", "["}
- FIRST(ε) = {ε}
- ✅ Disjuntos

**<RelOp>**, **<ArithOp>**, **<MulOp>**:
- ✅ Todos têm conjuntos FIRST disjuntos

**<Literal>**:
- FIRST(NUMERO_LITERAL) = {NUMERO_LITERAL}
- FIRST(STRING_LITERAL) = {STRING_LITERAL}
- FIRST("verdadeiro") = {"verdadeiro"}
- FIRST("falso") = {"falso"}
- ✅ Todos disjuntos

#### 2. Verificação de ε-produções

Para não-terminais com ε-produções, verificar se FIRST ∩ FOLLOW = ∅:

**<StatementList>**:
- FIRST(<StatementList>) = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar", ε}
- FOLLOW(<StatementList>) = {$, "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}
- ✅ FIRST ∩ FOLLOW = ∅ (sem considerar ε)

**<InitOpt>**:
- FIRST(<InitOpt>) = {"=", ε}
- FOLLOW(<InitOpt>) = {"declarar", IDENTIFICADOR, "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}
- ✅ FIRST ∩ FOLLOW = ∅ (sem considerar ε)

**<TypeOpt>**:
- FIRST(<TypeOpt>) = {"[", ε}
- FOLLOW(<TypeOpt>) = {"=", IDENTIFICADOR, "]", "declarar", "se", "enquanto", "repetir", "para_cada", "mostrar", "perguntar", "retornar", "funcao", "parar", $, "fim_se", "fim_enquanto", "fim_repetir", "fim_para_cada", "fim_funcao", "senao_se", "senao"}
- ✅ FIRST ∩ FOLLOW = ∅ (sem considerar ε)

**Outras ε-produções**: Similar análise mostra que são disjuntos.

## ❌ Conclusão: A Gramática NÃO é LL(1)

### Problemas Identificados:

1. **Ambiguidade em <Statement>**:
   - `<Assignment>` e `<FuncCall>` ambos começam com IDENTIFICADOR
   - Não é possível decidir qual produção usar apenas olhando o primeiro token

2. **Ambiguidade em <Factor>**:
   - `<Identifier>`, `<FuncCall>` e `<Identifier> "[" <Expression> "]"` todos começam com IDENTIFICADOR
   - Requer lookahead além de 1 token para distinguir entre:
     - `id` (identifier simples)
     - `id(...)` (function call)
     - `id[...]` (array access)

### Soluções Possíveis:

#### Opção 1: Refatoração da Gramática
```bnf
<Statement> ::= <DeclarationStmt>
              | <IdentifierStmt>
              | <IfStmt>
              | <WhileStmt>
              | <RepeatStmt>
              | <ForStmt>
              | <PrintStmt>
              | <InputStmt>
              | <ReturnStmt>
              | <FuncDecl>
              | "parar"

<IdentifierStmt> ::= <Identifier> <IdentifierSuffix>

<IdentifierSuffix> ::= "=" <Expression>        # Assignment
                     | "(" <ActualParamsOpt> ")" # FuncCall
                     | "[" <Expression> "]" "=" <Expression> # Array assignment

<Factor> ::= <Identifier> <FactorSuffix>
           | <Literal>
           | "(" <Expression> ")"
           | "[" <ListLiteralOpt> "]"

<FactorSuffix> ::= "(" <ActualParamsOpt> ")"   # Function call
                 | "[" <Expression> "]"        # Array access
                 | ε                           # Simple identifier
```

#### Opção 2: Parser com Backtracking
Manter a gramática atual mas usar um parser com capacidade de backtracking (não LL(1) puro).

#### Opção 3: Lookahead Estendido
Usar um parser LL(k) com k > 1, ou LR(1) que pode lidar com essas ambiguidades.

### Recomendação:

**A gramática atual não é LL(1)** devido às ambiguidades identificadas. Para torná-la LL(1), seria necessário refatorar as produções conforme a Opção 1 acima, ou utilizar uma técnica de parsing mais poderosa como LR(1) ou um parser recursivo descendente com backtracking limitado.
