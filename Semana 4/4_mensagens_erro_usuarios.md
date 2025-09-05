# Primeiros Esboços de Mensagens de Erro para Usuários

## 1. Mensagens de Erro Léxico

### 1.1 Caractere Inválido

**Formato da Mensagem**:
```
ERRO LÉXICO: Caractere inválido '{caractere}' encontrado na linha {linha}, coluna {coluna}
Sugestão: Verifique se o caractere está correto ou se há erro de digitação
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Caractere inválido '§' encontrado na linha 5, coluna 12
Sugestão: Verifique se o caractere está correto ou se há erro de digitação
Contexto: declarar nome§ como texto
                    ^

ERRO LÉXICO: Caractere inválido '@' encontrado na linha 3, coluna 8
Sugestão: Verifique se o caractere está correto ou se há erro de digitação
Contexto: mostrar "texto"@
                    ^
```

### 1.2 String Não Fechada

**Formato da Mensagem**:
```
ERRO LÉXICO: String não foi fechada na linha {linha}, coluna {coluna}
Sugestão: Adicione aspas de fechamento (") ou (')
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: String não foi fechada na linha 3, coluna 15
Sugestão: Adicione aspas de fechamento (") ou (')
Contexto: mostrar "Olá, mundo
                    ^

ERRO LÉXICO: String não foi fechada na linha 7, coluna 20
Sugestão: Adicione aspas de fechamento (") ou (')
Contexto: declarar nome como 'texto
                    ^
```

### 1.3 Número Malformado

**Formato da Mensagem**:
```
ERRO LÉXICO: Formato de número inválido na linha {linha}, coluna {coluna}
Sugestão: Use formato correto: 123.45 ou 123
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Formato de número inválido na linha 7, coluna 8
Sugestão: Use formato correto: 123.45 ou 123
Contexto: declarar preco como 123.
                    ^

ERRO LÉXICO: Formato de número inválido na linha 2, coluna 15
Sugestão: Use formato correto: 123.45 ou 123
Contexto: declarar valor como 12.34.56
                    ^
```

### 1.4 Identificador Inválido

**Formato da Mensagem**:
```
ERRO LÉXICO: Identificador inválido '{identificador}' na linha {linha}, coluna {coluna}
Sugestão: Identificadores devem começar com letra ou underscore
Contexto: {linha_completa}
^
```

**Exemplos**:
```
ERRO LÉXICO: Identificador inválido '2nome' na linha 4, coluna 1
Sugestão: Identificadores devem começar com letra ou underscore
Contexto: 2nome = "teste"
^
```

## 2. Mensagens de Aviso

### 2.1 Palavra-Chave com Acento

**Formato da Mensagem**:
```
AVISO: Palavra-chave '{palavra}' encontrada na linha {linha}, coluna {coluna}
Sugestão: Use '{palavra_sem_acento}' (sem acento) para compatibilidade
Contexto: {linha_completa}
```

**Exemplos**:
```
AVISO: Palavra-chave 'entao' encontrada na linha 6, coluna 3
Sugestão: Use 'entao' para compatibilidade
Contexto: se idade > 18 entao

AVISO: Palavra-chave 'funcao' encontrada na linha 10, coluna 1
Sugestão: Use 'funcao' para compatibilidade
Contexto: funcao calcular_soma()
```

### 2.2 Identificador com Acentos

**Formato da Mensagem**:
```
AVISO: Identificador '{identificador}' contém acentos na linha {linha}, coluna {coluna}
Sugestão: Considere usar '{identificador_sem_acento}' para melhor compatibilidade
Contexto: {linha_completa}
```

**Exemplos**:
```
AVISO: Identificador 'coração' contém acentos na linha 2, coluna 1
Sugestão: Considere usar 'coracao' para melhor compatibilidade
Contexto: declarar coração como texto

AVISO: Identificador 'preço_do_produto' contém acentos na linha 5, coluna 1
Sugestão: Considere usar 'preco_do_produto' para melhor compatibilidade
Contexto: declarar preço_do_produto como numero
```

## 3. Mensagens de Erro Contextuais

### 3.1 Erro em Declaração de Variável

**Formato da Mensagem**:
```
ERRO LÉXICO: Erro na declaração de variável na linha {linha}, coluna {coluna}
Problema: {problema_especifico}
Sugestão: {sugestao_especifica}
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Erro na declaração de variável na linha 3, coluna 12
Problema: Tipo de dados inválido
Sugestão: Use 'texto', 'numero' ou 'logico'
Contexto: declarar nome como string
                    ^

ERRO LÉXICO: Erro na declaração de variável na linha 5, coluna 8
Problema: Nome de variável inválido
Sugestão: Use apenas letras, números e underscore
Contexto: declarar 2nome como texto
                    ^
```

### 3.2 Erro em Estrutura de Controle

**Formato da Mensagem**:
```
ERRO LÉXICO: Erro na estrutura de controle na linha {linha}, coluna {coluna}
Problema: {problema_especifico}
Sugestão: {sugestao_especifica}
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Erro na estrutura de controle na linha 8, coluna 3
Problema: Palavra-chave 'entao' não reconhecida
Sugestão: Use 'entao'
Contexto: se idade > 18 entao
                    ^

ERRO LÉXICO: Erro na estrutura de controle na linha 12, coluna 1
Problema: Estrutura não fechada
Sugestão: Adicione 'fim_se' para fechar a estrutura
Contexto: se condicao então
```

### 3.3 Erro em Expressão

**Formato da Mensagem**:
```
ERRO LÉXICO: Erro na expressão na linha {linha}, coluna {coluna}
Problema: {problema_especifico}
Sugestão: {sugestao_especifica}
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Erro na expressão na linha 6, coluna 15
Problema: Operador inválido
Sugestão: Use operadores válidos: +, -, *, /, %, =, !=, <, >, <=, >=
Contexto: resultado = a + b§
                    ^

ERRO LÉXICO: Erro na expressão na linha 4, coluna 10
Problema: Número malformado
Sugestão: Use formato correto: 123.45 ou 123
Contexto: preco = 123.
                    ^
```

## 4. Mensagens de Erro com Sugestões Inteligentes

### 4.1 Sugestões de Correção Automática

**Formato da Mensagem**:
```
ERRO LÉXICO: {erro} na linha {linha}, coluna {coluna}
Sugestão: {sugestao}
Correção sugerida: {correcao}
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Palavra-chave 'entao' não reconhecida na linha 6, coluna 3
Sugestão: Use 'entao' para compatibilidade
Correção sugerida: se idade > 18 entao
Contexto: se idade > 18 entao
                    ^

ERRO LÉXICO: Número malformado na linha 3, coluna 15
Sugestão: Use formato correto: 123.45 ou 123
Correção sugerida: declarar preco como 123.0
Contexto: declarar preco como 123.
                    ^
```

### 4.2 Sugestões de Palavras Similares

**Formato da Mensagem**:
```
ERRO LÉXICO: Palavra-chave '{palavra}' não reconhecida na linha {linha}, coluna {coluna}
Sugestão: Você quis dizer uma dessas?
  - {palavra1}
  - {palavra2}
  - {palavra3}
Contexto: {linha_completa}
                    ^
```

**Exemplos**:
```
ERRO LÉXICO: Palavra-chave 'declar' não reconhecida na linha 2, coluna 1
Sugestão: Você quis dizer uma dessas?
  - declarar
  - mostrar
  - perguntar
Contexto: declar nome como texto
                    ^
```

## 5. Mensagens de Erro com Contexto Estendido

### 5.1 Erro com Múltiplas Linhas de Contexto

**Formato da Mensagem**:
```
ERRO LÉXICO: {erro} na linha {linha}, coluna {coluna}
Contexto:
  {linha-2}: {codigo_linha-2}
  {linha-1}: {codigo_linha-1}
  {linha}:   {codigo_linha}
                    ^
  {linha+1}: {codigo_linha+1}
  {linha+2}: {codigo_linha+2}
```

**Exemplo**:
```
ERRO LÉXICO: String não foi fechada na linha 5, coluna 15
Contexto:
  3: declarar nome como texto
  4: nome = "João"
  5: mostrar "Olá, " + nome
                    ^
  6: mostrar "Bem-vindo!"
  7: fim_programa
```

### 5.2 Erro com Informações de Arquivo

**Formato da Mensagem**:
```
ERRO LÉXICO: {erro} na linha {linha}, coluna {coluna}
Arquivo: {nome_arquivo}
Timestamp: {timestamp}
Contexto: {linha_completa}
                    ^
```

**Exemplo**:
```
ERRO LÉXICO: Caractere inválido '§' encontrado na linha 5, coluna 12
Arquivo: exemplo.bs
Timestamp: 2024-01-15 14:30:25
Contexto: declarar nome§ como texto
                    ^
```

## 6. Mensagens de Erro com Códigos de Erro

### 6.1 Sistema de Códigos de Erro

**Formato da Mensagem**:
```
ERRO LÉXICO [E001]: {erro} na linha {linha}, coluna {coluna}
Sugestão: {sugestao}
Contexto: {linha_completa}
                    ^
```

**Códigos de Erro**:
- **E001**: Caractere inválido
- **E002**: String não fechada
- **E003**: Número malformado
- **E004**: Identificador inválido
- **E005**: Palavra-chave não reconhecida
- **E006**: Operador inválido
- **E007**: Delimitador inválido

**Exemplos**:
```
ERRO LÉXICO [E001]: Caractere inválido '§' encontrado na linha 5, coluna 12
Sugestão: Verifique se o caractere está correto ou se há erro de digitação
Contexto: declarar nome§ como texto
                    ^

ERRO LÉXICO [E002]: String não foi fechada na linha 3, coluna 15
Sugestão: Adicione aspas de fechamento (") ou (')
Contexto: mostrar "Olá, mundo
                    ^
```

## 7. Mensagens de Erro com Links de Ajuda

### 7.1 Mensagens com Referências

**Formato da Mensagem**:
```
ERRO LÉXICO: {erro} na linha {linha}, coluna {coluna}
Sugestão: {sugestao}
Documentação: {link_documentacao}
Contexto: {linha_completa}
                    ^
```

**Exemplo**:
```
ERRO LÉXICO: Palavra-chave 'então' não reconhecida na linha 6, coluna 3
Sugestão: Use 'entao' (sem acento) para compatibilidade
Documentação: https://brasilscript.dev/docs/palavras-chave
Contexto: se idade > 18 então
                    ^
```

## 8. Mensagens de Erro com Estatísticas

### 8.1 Mensagens com Informações de Frequência

**Formato da Mensagem**:
```
ERRO LÉXICO: {erro} na linha {linha}, coluna {coluna}
Sugestão: {sugestao}
Frequência: Este erro ocorreu {frequencia} vezes neste arquivo
Contexto: {linha_completa}
                    ^
```

**Exemplo**:
```
ERRO LÉXICO: Palavra-chave 'então' não reconhecida na linha 6, coluna 3
Sugestão: Use 'entao' (sem acento) para compatibilidade
Frequência: Este erro ocorreu 3 vezes neste arquivo
Contexto: se idade > 18 então
                    ^
```

## 9. Implementação das Mensagens

### 9.1 Classe de Mensagem de Erro

```python
class MensagemErro:
    def __init__(self, tipo, codigo, mensagem, linha, coluna, contexto, sugestao=None):
        self.tipo = tipo
        self.codigo = codigo
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        self.contexto = contexto
        self.sugestao = sugestao
        self.timestamp = datetime.now()
    
    def formatar(self):
        return f"""
ERRO LÉXICO [{self.codigo}]: {self.mensagem} na linha {self.linha}, coluna {self.coluna}
Sugestão: {self.sugestao}
Contexto: {self.contexto}
                    ^
"""
```

### 9.2 Gerador de Mensagens

```python
class GeradorMensagens:
    def __init__(self):
        self.codigos_erro = {
            'CARACTERE_INVALIDO': 'E001',
            'STRING_NAO_FECHADA': 'E002',
            'NUMERO_MALFORMADO': 'E003',
            'IDENTIFICADOR_INVALIDO': 'E004',
            'PALAVRA_CHAVE_NAO_RECONHECIDA': 'E005',
            'OPERADOR_INVALIDO': 'E006',
            'DELIMITADOR_INVALIDO': 'E007'
        }
    
    def gerar_mensagem(self, tipo, linha, coluna, contexto, sugestao=None):
        codigo = self.codigos_erro.get(tipo, 'E000')
        mensagem = self.obter_mensagem(tipo)
        return MensagemErro(tipo, codigo, mensagem, linha, coluna, contexto, sugestao)
    
    def obter_mensagem(self, tipo):
        mensagens = {
            'CARACTERE_INVALIDO': 'Caractere inválido',
            'STRING_NAO_FECHADA': 'String não foi fechada',
            'NUMERO_MALFORMADO': 'Formato de número inválido',
            'IDENTIFICADOR_INVALIDO': 'Identificador inválido',
            'PALAVRA_CHAVE_NAO_RECONHECIDA': 'Palavra-chave não reconhecida',
            'OPERADOR_INVALIDO': 'Operador inválido',
            'DELIMITADOR_INVALIDO': 'Delimitador inválido'
        }
        return mensagens.get(tipo, 'Erro desconhecido')
```

## 10. Conclusão

As mensagens de erro para usuários:

1. **São claras e informativas** sobre o problema
2. **Fornecem sugestões úteis** para correção
3. **Incluem contexto** para facilitar localização
4. **Usam códigos de erro** para referência
5. **Oferecem correções automáticas** quando possível
6. **Mantêm consistência** no formato
7. **São amigáveis** para desenvolvedores iniciantes

Estas mensagens garantem que os desenvolvedores possam corrigir erros léxicos de forma eficiente e aprender sobre a linguagem BrasilScript.
