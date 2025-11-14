# Análise Semântica e Inferência de Tipos - BrasilScript

Este documento descreve a implementação simples de análise semântica e inferência de tipos adicionada ao projeto.

Objetivos e escopo
- Verificação de declarações: detectar uso de identificadores não declarados.
- Verificação de tipos em atribuições e inicializações.
- Inferência de tipos para expressões, literais, listas, operações aritméticas, lógicas e relacionais.
- Verificações básicas em acesso por índice de listas e chamadas de função (existência apenas).

Regras resumidas
- Tipos suportados: `numero`, `texto`, `logico`, `lista[T]`, `funcao`, `any`.
- Literais numéricos inferem `numero`; strings inferem `texto`; `verdadeiro`/`falso` inferem `logico`.
- Operadores aritméticos (`+, -, *, /, %`) requerem `numero` (com `+` também suportando concatenação de `texto`).
- Operadores lógicos (`e`, `ou`, `nao`) requerem `logico`.
- Operadores relacionais retornam `logico` e exigem tipos compatíveis.
- Listas exigem elementos do mesmo tipo (ou `any` para listas vazias).

Como usar
- Após gerar a AST com `parser.brasilscript_parser.parse_brasilscript`, instancie `parser.semantic.SemanticAnalyzer` e chame `analyze(ast)`.
- A função retorna uma lista de mensagens de erro (vazia se tudo OK).

Exemplo

    from parser.brasilscript_parser import parse_brasilscript
    from parser.semantic import SemanticAnalyzer

    ast = parse_brasilscript('''
    declarar x como numero = 10
    declarar nome como texto
    nome = "BrasilScript"
    mostrar "Ola, " + nome
    ''')

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    if errors:
        for e in errors:
            print(e)
    else:
        print('Análise semântica: OK')

Limitações
- Escopos reduzidos: símbolo global apenas; funções não criam escopo próprio neste analisador simples.
- Assinaturas de funções não verificadas (apenas existência).
- Inferência conservadora para operações mais avançadas.

O objetivo foi implementar uma análise semântica objetiva e simples, suficiente para testes e para detectar os erros mais comuns durante o desenvolvimento do parser e do interpretador.
