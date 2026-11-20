---
description: Roda o ciclo AI-SDLC de uma ideia ou estória (#N), parando nos portões da dona do produto
argument-hint: <ideia em texto ou número da estória, ex.: #42>
---
Conduza o ciclo descrito em `docs/PROCESSO_AI_SDLC.md` para: $ARGUMENTS

Use os subagentes na ordem abaixo e **pare** nos portões ★ (peça aprovação à dona do produto e encerre o turno):

1. **pm**: se for ideia, escreva a estória com critérios de aceite. ★ **Portão 1**: aprovação da estória (rótulo `aprovada`).
2. **dev-senior-b** (plano técnico) e, se a estória tem `ui`, **designer** (desenho). **qa** deriva os casos de teste dos critérios. Sem portão humano: Dev B e Designer aprovam o plano; você só mostra um resumo.
3. Se a estória tem `conteudo`: **curador-pedagogico** prepara o conteúdo. ★ **Portão 2**: aprovação pedagógica (a dona do produto mescla o PR).
4. **dev-senior-a**: testes primeiro, código, `npm run check` e `npm run test:e2e` verdes, abre o PR com `Closes #N`.
5. Revisão em paralelo: **dev-senior-b** (correção/arquitetura), **qa**, **seguranca-privacidade**, **designer** (se `ui`). Achado bloqueante volta ao dev-senior-a.
6. **devops-release**: avalia se o PR é elegível a mesclagem automática; se não, deixa para a dona do produto.
7. Depois do merge, **qa** publica o roteiro de teste manual na estória.

Nunca mesclar nem aprovar em nome da dona do produto. Resuma cada etapa em linguagem simples.
