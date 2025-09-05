# Estratégia para Tratamento de Erros Léxicos

## 1. Tipos de Erros Léxicos

### 1.1 Caracteres Inválidos

**Definição**: Caracteres que não fazem parte do alfabeto da linguagem.

**Expressão Regular**:
```regex
# Caracteres não reconhecidos
CARACTERE_INVALIDO: [^\w\s+\-*/%=!<>()[\]{},.;:#"'áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]
```

**Exemplos**:
```brasilscript
declarar nome§ como texto  # '§' é caractere inválido
mostrar "texto"@  # '@' é caractere inválido
```

### 1.2 Strings Não Fechadas

**Definição**: Strings que não foram fechadas até o final da linha.

**Expressão Regular**:
```regex
# String que não foi fechada até o final da linha
STRING_NAO_FECHADA: "(?:[^"\\]|\\.)*$|'(?:[^'\\]|\\.)*$
```

**Exemplos**:
```brasilscript
mostrar "Olá, mundo  # String não fechada
declarar nome como 'texto  # String não fechada
```

### 1.3 Números Malformados

**Definição**: Números com formato inválido.

**Expressão Regular**:
```regex
# Números com formato inválido
NUMERO_MALFORMADO: \d+\.\d*\.|\d*\.\d+\.|\d+\.\d*[eE]\d*\.|\d*\.\d+[eE]\d*\.
```

**Exemplos**:
```brasilscript
declarar preco como 123.  # Número malformado
declarar valor como 12.34.56  # Número malformado
```

### 1.4 Identificadores Inválidos

**Definição**: Identificadores que não seguem as regras de formação.

**Exemplos**:
```brasilscript
2nome = "teste"  # Identificador não pode começar com dígito
nome@ = "teste"  # Identificador contém caractere inválido
```

### 1.5 Comentários Malformados

**Definição**: Comentários que não seguem o formato correto.

**Exemplos**:
```brasilscript
# Comentário sem quebra de linha no final do arquivo
declarar nome como texto
```

## 2. Estratégias de Recuperação

### 2.1 Modo Pânico

**Quando usar**: Caractere inválido encontrado.

**Ação**: Pular caracteres até encontrar delimitador conhecido.

**Delimitadores de recuperação**: `\n`, `;`, `}`, `)`

**Algoritmo**:
```
1. Detectar caractere inválido
2. Reportar erro
3. Pular caracteres até encontrar delimitador
4. Continuar análise a partir do delimitador
```

**Exemplo**:
```brasilscript
declarar nome§ como texto
# Erro: caractere inválido '§'
# Recuperação: pular até encontrar 'como'
# Continuar: como texto
```

### 2.2 Modo Tolerante

**Quando usar**: Erro menor (ex: número malformado).

**Ação**: Tentar corrigir automaticamente.

**Exemplos de correção**:
- `123.` → `123.0`
- `12.34.56` → `12.34` (truncar)
- `12e` → `12e0`

**Algoritmo**:
```
1. Detectar erro menor
2. Tentar correção automática
3. Se bem-sucedida: continuar
4. Se falhar: aplicar modo pânico
```

**Exemplo**:
```brasilscript
declarar preco como 123.
# Erro: número malformado
# Correção: 123. → 123.0
# Continuar: como 123.0
```

### 2.3 Modo Restritivo

**Quando usar**: Erro crítico (ex: string não fechada).

**Ação**: Parar análise e reportar erro.

**Algoritmo**:
```
1. Detectar erro crítico
2. Reportar erro
3. Parar análise
4. Não continuar até correção manual
```

**Exemplo**:
```brasilscript
mostrar "Olá, mundo
# Erro: string não fechada
# Ação: parar análise
# Não continuar até correção
```

## 3. Algoritmo de Tratamento de Erros

### 3.1 Algoritmo Principal

```
1. Tentar reconhecer token normal
2. Se falhar:
   a. Verificar se é caractere inválido
   b. Se sim: aplicar modo pânico
   c. Se não: verificar se é erro recuperável
   d. Se recuperável: aplicar modo tolerante
   e. Se não: aplicar modo restritivo
3. Continuar análise a partir do ponto de recuperação
```

### 3.2 Implementação em Pseudocódigo

```python
def analisar_token():
    try:
        token = reconhecer_token()
        return token
    except CaractereInvalido as e:
        return aplicar_modo_panico(e)
    except ErroRecuperavel as e:
        return aplicar_modo_tolerante(e)
    except ErroCritico as e:
        return aplicar_modo_restritivo(e)

def aplicar_modo_panico(erro):
    reportar_erro(erro)
    pular_ate_delimitador()
    return continuar_analise()

def aplicar_modo_tolerante(erro):
    correcao = tentar_correcao(erro)
    if correcao:
        return criar_token_corrigido(correcao)
    else:
        return aplicar_modo_panico(erro)

def aplicar_modo_restritivo(erro):
    reportar_erro(erro)
    parar_analise()
    return None
```

## 4. Estratégias de Recuperação por Tipo de Erro

### 4.1 Caracteres Inválidos

**Estratégia**: Modo Pânico

**Implementação**:
```python
def tratar_caractere_invalido(caractere, posicao):
    erro = ErroLexico(
        tipo="CARACTERE_INVALIDO",
        mensagem=f"Caractere inválido '{caractere}'",
        linha=posicao.linha,
        coluna=posicao.coluna
    )
    reportar_erro(erro)
    pular_ate_delimitador()
    return continuar_analise()
```

### 4.2 Strings Não Fechadas

**Estratégia**: Modo Restritivo

**Implementação**:
```python
def tratar_string_nao_fechada(posicao):
    erro = ErroLexico(
        tipo="STRING_NAO_FECHADA",
        mensagem="String não foi fechada",
        linha=posicao.linha,
        coluna=posicao.coluna
    )
    reportar_erro(erro)
    parar_analise()
    return None
```

### 4.3 Números Malformados

**Estratégia**: Modo Tolerante

**Implementação**:
```python
def tratar_numero_malformado(numero, posicao):
    correcao = tentar_corrigir_numero(numero)
    if correcao:
        return criar_token(NUMERO_LITERAL, correcao, posicao)
    else:
        return aplicar_modo_panico(posicao)

def tentar_corrigir_numero(numero):
    if numero.endswith('.'):
        return numero + '0'
    elif '..' in numero:
        return numero.split('..')[0]
    else:
        return None
```

### 4.4 Identificadores Inválidos

**Estratégia**: Modo Pânico

**Implementação**:
```python
def tratar_identificador_invalido(identificador, posicao):
    erro = ErroLexico(
        tipo="IDENTIFICADOR_INVALIDO",
        mensagem=f"Identificador inválido '{identificador}'",
        linha=posicao.linha,
        coluna=posicao.coluna
    )
    reportar_erro(erro)
    pular_ate_delimitador()
    return continuar_analise()
```

## 5. Estratégias de Recuperação Contextual

### 5.1 Recuperação por Contexto

**Definição**: A estratégia de recuperação depende do contexto onde o erro ocorre.

**Exemplos**:
```brasilscript
# Contexto: declaração de variável
declarar nome§ como texto
# Estratégia: modo pânico (pular até 'como')

# Contexto: string
mostrar "texto§"
# Estratégia: modo tolerante (tratar como caractere literal)

# Contexto: expressão
resultado = a + b§
# Estratégia: modo pânico (pular até fim da linha)
```

### 5.2 Recuperação por Frequência

**Definição**: A estratégia de recuperação depende da frequência do erro.

**Exemplos**:
```brasilscript
# Erro único: modo tolerante
declarar preco como 123.

# Múltiplos erros: modo restritivo
declarar nome§ como texto@
```

### 5.3 Recuperação por Severidade

**Definição**: A estratégia de recuperação depende da severidade do erro.

**Classificação de Severidade**:
- **Baixa**: Números malformados, espaços extras
- **Média**: Caracteres inválidos, identificadores inválidos
- **Alta**: Strings não fechadas, comentários malformados

## 6. Implementação de Recuperação

### 6.1 Estrutura de Erro

```python
class ErroLexico:
    def __init__(self, tipo, mensagem, linha, coluna, contexto=None):
        self.tipo = tipo
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        self.contexto = contexto
        self.timestamp = datetime.now()
```

### 6.2 Gerenciador de Erros

```python
class GerenciadorErros:
    def __init__(self):
        self.erros = []
        self.avisos = []
        self.modo_recuperacao = "TOLERANTE"
    
    def reportar_erro(self, erro):
        self.erros.append(erro)
        self.aplicar_estrategia_recuperacao(erro)
    
    def aplicar_estrategia_recuperacao(self, erro):
        if erro.tipo in ERROS_CRITICOS:
            self.modo_recuperacao = "RESTRITIVO"
        elif erro.tipo in ERROS_RECUPERAVEIS:
            self.modo_recuperacao = "TOLERANTE"
        else:
            self.modo_recuperacao = "PANICO"
```

### 6.3 Analisador com Recuperação

```python
class AnalisadorLexico:
    def __init__(self):
        self.gerenciador_erros = GerenciadorErros()
        self.posicao_atual = Posicao(1, 1)
        self.tokens = []
    
    def analisar(self, codigo):
        while self.posicao_atual < len(codigo):
            try:
                token = self.reconhecer_token(codigo)
                self.tokens.append(token)
            except ErroLexico as e:
                self.gerenciador_erros.reportar_erro(e)
                self.recuperar_erro(e)
        
        return self.tokens
    
    def recuperar_erro(self, erro):
        if self.gerenciador_erros.modo_recuperacao == "PANICO":
            self.aplicar_modo_panico(erro)
        elif self.gerenciador_erros.modo_recuperacao == "TOLERANTE":
            self.aplicar_modo_tolerante(erro)
        else:
            self.aplicar_modo_restritivo(erro)
```

## 7. Testes de Recuperação

### 7.1 Casos de Teste

```brasilscript
# Teste 1: Caractere inválido
declarar nome§ como texto
# Esperado: erro reportado, análise continua

# Teste 2: String não fechada
mostrar "Olá, mundo
# Esperado: erro reportado, análise para

# Teste 3: Número malformado
declarar preco como 123.
# Esperado: correção automática para 123.0

# Teste 4: Identificador inválido
2nome = "teste"
# Esperado: erro reportado, análise continua
```

### 7.2 Resultados Esperados

| Erro | Estratégia | Ação | Continua? |
|------|------------|------|-----------|
| Caractere inválido | Pânico | Pular até delimitador | Sim |
| String não fechada | Restritivo | Parar análise | Não |
| Número malformado | Tolerante | Corrigir automaticamente | Sim |
| Identificador inválido | Pânico | Pular até delimitador | Sim |

## 8. Conclusão

A estratégia de tratamento de erros léxicos:

1. **Classifica erros** por tipo e severidade
2. **Aplica estratégias** apropriadas para cada tipo
3. **Recupera automaticamente** quando possível
4. **Reporta erros** de forma clara e útil
5. **Mantém análise** funcionando quando possível
6. **Para análise** apenas em erros críticos

Esta estratégia garante que o analisador léxico seja robusto e útil para desenvolvedores.
