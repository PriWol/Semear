# 0018. Marcos extras filtrados por vertente

- **Status:** Aceito.
- **Data:** 2026-10-17

## Contexto

A especificação prevê marcos extras por vertente (ex.: ditado preparado, Charlotte Mason, em `LG.ESC`). O campo
`vertentes` do marco existia, mas só as linhas eram filtradas; um marco extra apareceria para todas as famílias.

## Decisão

`marcoVisivel` (`src/domain/jornada.ts`) decide se a família vê o marco, reaproveitando `vertentesDaFamilia`.
`marcosDaPista` aplica o filtro e é a base de `posicaoDaLinha`, `posicionarAqui` e do gerador de sessão,
então fronteira, ativos, totais e "Aguardando" só consideram marcos visíveis. Por isso `posicaoDaLinha`,
`posicionarAqui` e `avisosTrilhas` recebem a família (vertentes) em vez de só a vertente principal.

**Pré-requisito para marco extra escondido é ignorado**: a família não vê aquele marco, então ele não pode
bloquear nem avisar. O mesmo vale para pré-requisitos das trilhas de língua.

A tela de cobertura (`/conteudo`) não filtra: é uma visão de curadoria, independente de família.

## Consequências

- Dá para criar marcos extras sem afetar famílias de outras vertentes.
- Se a família trocar de vertente, estados já registrados de marcos agora escondidos ficam guardados, mas não aparecem nem contam.
