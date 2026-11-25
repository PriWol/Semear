---
description: Roda o ciclo AI-SDLC de uma ideia ou estória (#N), parando em cada coluna que é uma verificação da dona do produto
argument-hint: <ideia em texto ou número da estória, ex.: #42>
---
Conduza o ciclo descrito em `docs/PROCESSO_AI_SDLC.md` (quadro, regras do acordo e rótulos) para: $ARGUMENTS

Leia antes `docs/APRENDIZADOS.md`. Use os subagentes na ordem abaixo e **pare** em cada coluna ★ (apresente o resumo de
3 linhas, aplique o rótulo da coluna e encerre o turno):

1. **pm** (Detalhando): escreva a estória com critérios de aceite **e o "Como testar"** (o `qa` redige o rascunho).
   ★ **Aprovar estória**: rótulo `aguardando-aprovacao`; só a dona aplica `aprovada`.
2. **Em desenvolvimento**: **dev-senior-b** (plano), **designer** (se `ui`), **qa** (casos de teste), **curador-pedagogico**
   (se `conteudo`) e **dev-senior-a** (testes primeiro, código, `npm run check` e `npm run test:e2e` verdes, PR com `Closes #N`).
   Revisão em paralelo: dev-senior-b, qa, seguranca-privacidade e designer (se `ui`). Pergunta que só a dona responde:
   rótulo `quadro:pergunta`, a pergunta em uma linha, e pare. Com revisões sem bloqueio e e2e verde: `quadro:testando`.
3. **qa** (Testando): valida o PR e escreve o relatório com **a prova de cada critério** (tabela critério, teste, resultado,
   link do artefato `relatorio-playwright`). ★ **Aprovar entrega**: rótulo `quadro:aprovar-entrega` (máx. 3 cartões ali).
4. ★ **Pronto para mesclar** (`quadro:pronto`): só a dona mescla. **devops-release** só prepara; nunca mescla.
5. ★ **Em produção**: depois do merge, **qa** publica o roteiro de teste do site publicado; a dona confere e aplica `quadro:feito`.

Nunca mesclar nem aprovar em nome da dona do produto. Resuma cada etapa em linguagem simples.
