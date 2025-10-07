

#### 1. Definição do Alfabeto Básico ($\Sigma$)

O **alfabeto ($\Sigma$)** da BrasilScript é o conjunto de todos os caracteres válidos que podem compor um programa. Ele representa o conjunto de símbolos atômicos a partir dos quais todas as "palavras" (tokens) da linguagem são construídas.

*   **Caracteres Alfabéticos:**
    *   Letras minúsculas: `a, b, c, ..., z`
    *   Letras maiúsculas: `A, B, C, ..., Z`
*   **Caracteres Numéricos:**
    *   Dígitos: `0, 1, 2, 3, 4, 5, 6, 7, 8, 9`
*   **Caracteres Especiais e Símbolos:**
    *   Operadores Aritméticos: `+, -, *, /, %`
    *   Operadores Relacionais: `=`, `!=`, `<`, `>`, `<=`, `>=`
    *   Delimitadores: `(, ), [, ], {, }, ,, ., :, ;`
    *   Atribuição: `=`
    *   Comentário: `#`
    *   Aspas: `"`
    *   Ponto decimal: `.`
    *   Espaço em branco: ` ` (representando espaço e tabulação)
        *   Barra invertida: `\` (necessária para sequências de escape como `\n`)

Formalmente, `$\Sigma = \{a-z, A-Z, 0-9, +, -, *, /, %, =, \neq, <, >, \le, \ge, (, ), [, ], {, }, ,, ., :, ;, \#, ", ', \sqcup, \text{\textbackslash n}\}$`.

#### 2. Especificação dos Tipos de Tokens

Utilizaremos Expressões Regulares e notação formal para definir cada tipo de token.

*   **Identificadores (ID):**
    *   Um identificador deve começar com uma letra (minúscula ou maiúscula) ou sublinhado, seguido por zero ou mais letras (minúsculas ou maiúsculas), dígitos ou sublinhados.
    *   Formalmente: `$ID = (Letra \cup \_)(Letra \cup Dígito \cup \_)*$`
    *   Onde `$Letra = \{a-z, A-Z\}$` e `$Dígito = \{0-9\}$`.
    *   **Reflexão:** Identificadores serão *case-sensitive*.

*   **Palavras-Chave (KW):**
    *   São identificadores reservados com significado especial. Todas em minúsculas (conforme decisão anterior).
    *   `$KW = declarar, como, mostrar, perguntar, guardar_em, se, entao, senao, repetir, vezes, enquanto, faca, funcao, lista, para_cada, em, parar, e, ou, nao, retornar, texto, numero, logico, contador, classe`

*   **Literais Numéricos (NUMERO_LITERAL):**
    *   Representa tanto números inteiros quanto números com casas decimais.
    *   Pode ser uma sequência de dígitos (inteiro) ou uma sequência de dígitos seguida por um ponto e outra sequência de dígitos (quebrado/decimal).
    *   Formalmente: `$NUMERO_LITERAL = dígito+ (\text{.} dígito+)?$`
    *   Onde `?` indica que a parte decimal é opcional.

*   **Literais de Texto (STRING):**
    *   Sequência de caracteres delimitada por aspas duplas ou simples.
    *   Formalmente: `$STRING = "(\Sigma \setminus \{"\})"* " \cup '(\Sigma \setminus \{'\})'* '$`
    *   **Reflexão:** Caracteres especiais dentro de strings (como quebras de linha) serão representados por sequências de escape (ex: `\n`).

*   **Literais Lógicos (LOGICO_LITERAL):**
    *   Representam valores booleanos.
    *   `$LOGICO_LITERAL = verdadeiro, falso`

*   **Operadores (OP):**
    *   `OP = +, -, *, /, %, =, \neq, <, >, \le, \ge\`

*   **Delimitadores (DELIM):**
    *   `DELIM = (, ), [, ], {, }, ,, ., :, ;`

*   **Comentários (COMMENT):**
    *   Iniciam com `#` e vão até o final da linha (marcado por `\n`).
    *   Formalmente: `COMMENT = # (\Sigma \setminus \{\text{\textbackslash n}\})* \text{\textbackslash n}$`
    *   **Aplicação de Fechamento de Kleene:** O uso de `*` permite que o comentário tenha comprimento variável, incluindo comentários vazios após o `#`.

*   **Espaços em Branco (WHITESPACE):**
    *   Sequência de um ou mais espaços ou tabulações. Quebras de linha (`\n`) serão tratadas separadamente como delimitadores de linha para comentários e fim de instrução (se aplicável).
    *   Formalmente: `$WHITESPACE = (\sqcup \cup \text{tab})+$`
    *   **Reflexão:** Espaços em branco serão ignorados pelo analisador léxico, exceto dentro de strings.

#### Exemplo de Criação de função 

{nome funcao} {tipo retorno} {corpo funcao}
Declarar um nome, colocar o tipo dela e montar o corpo

#### 3. Exemplos Concretos de Programas Válidos

```brasilscript
# este e um programa simples
declarar MeuNome como texto
declarar MinhaIdade como numero
declarar EstaAtivo como logico

MeuNome = "brasilscript"
MinhaIdade = 10 # numero inteiro
EstaAtivo = verdadeiro

mostrar "ola, mundo da " + MeuNome + "!\n"
mostrar "idade: " + MinhaIdade + "\n"
mostrar "ativo: " + EstaAtivo + "\n"

declarar PrecoProduto como numero
PrecoProduto = 99.99 # numero quebrado/decimal
mostrar "preco: " + PrecoProduto + "\n"

## Integração com Semana 5 — Autômatos (AFD)

Observação: as expressões regulares definidas nesta especificação foram convertidas em autômatos finitos determinísticos na semana 5. A implementação e os diagramas estão em `Semana 5/`.

- Diagrama (Mermaid): `Semana 5/automata.md` — contém diagramas para comentários, whitespace, strings, números, literais lógicos, keywords, identificadores, operadores e delimitadores.
- Implementações AFD (módulos): `Semana 5/afds/` — cada função `accepts_*` tenta corresponder uma lexema e retorna o tipo de token quando casa; por exemplo:
    - `number_afd.py` → `NUMERO_LITERAL`
    - `string_afd.py` → `STRING_LITERAL`
    - `identifier_afd.py` → `IDENTIFICADOR` / `IDENTIFICADOR_INVALIDO`
    - `logical_afd.py` → `LOGICO_LITERAL`
    - `keywords_afd.py` → `PALAVRA_CHAVE`
    - `operators_afd.py` → `OP` (aritmético/relacional)
    - `delimiters_afd.py` → `LPAREN`, `RPAREN`, `COMMA`, `DOT`, etc.
    - `comment_afd.py`, `whitespace_afd.py`, `newline_afd.py` — tratamento apropriado

Status atual e recomendações rápidas:
- Diagramas: existentes e alinhados com as regex da especificação.
- AFDs: implementados como funções independentes e cobertos por `Semana 5/test_afds.py`.
- Minimização de AFD: ainda não implementada — recomendo adicionar `afds/minimization.py` (Hopcroft) como próxima tarefa.
- Lexer determinístico unificado: atualmente o `lexer.py` usa uma master-regex; para completar o objetivo da semana (converter regex em AFDs e usar DFAs em produção) recomenda-se implementar um `dfa_lexer.py` que utilize as AFDs ou as tabelas de transição construídas a partir delas e que execute longest-match respeitando prioridades.

Como testar rapidamente (PowerShell):
```powershell
# rodar testes dos AFDs
python -m pytest -q "Semana 5/test_afds.py"

# rodar os testes do lexer atual (regex-based)
python -m pytest -q "Semana 5/test_lexer.py"
```

Próximos passos sugeridos para entrega final da semana:
1. Implementar o lexer baseado em DFA (`dfa_lexer.py`) que consuma as AFDs e passe na suíte de testes atual.
2. Implementar minimização (Hopcroft) e documentar ganhos (tamanho de DFA antes/depois).
3. Adicionar um script de comparação que valide equivalência (tokens) entre `lexer.py` e `dfa_lexer.py` em um conjunto de casos de teste.

Com isso a Semana 5 ficará coerente com os objetivos: diagramas, AFDs funcionais, testes unitários e plano para minimização/integração.