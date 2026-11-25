---
description: Retro semanal do time de agentes: mede o processo, junta o que cada agente observou e propõe no máximo 3 experimentos
argument-hint: [período, ex.: "7 dias" (padrão)]
---
Faça a retro do período ($ARGUMENTS; padrão: últimos 7 dias). Leia `docs/PROCESSO_AI_SDLC.md` e `docs/APRENDIZADOS.md`.

## 1. Meça (só com dados do GitHub: PRs, issues, revisões, CI)
- **Fluxo:** estórias que chegaram a "Feito", tempo médio entre colunas e onde acumula.
- **Retrabalho:** quantas vezes cartões voltaram de um portão e por quê (estória vaga? critério faltando? prova fraca?).
- **Qualidade:** achados bloqueantes por categoria nos PRs; categorias que **se repetem**; testes que falharam no e2e.
- **Defeitos que escaparam:** problemas achados em produção depois do merge.
- **Testes:** variação do número de testes e, se `npm run check` passar a medir, da cobertura. Diga "não medido" se não houver dado.
- **Lado humano (dona do produto):** tempo de espera em cada coluna dela, coluna que mais acumula, estórias devolvidas e
  motivo, perguntas sem resposta há mais de 3 dias. Sugira janelas de revisão em lote e melhorias no modelo do Backlog.

## 2. Pergunte aos agentes
Peça a cada subagente (pm, designer, dev-senior-a, dev-senior-b, qa, curador-pedagogico, seguranca-privacidade,
devops-release) três linhas: o que funcionou, o erro que mais se repetiu, uma mudança de processo.

## 3. Entregue
Abra uma issue "Retro AAAA-MM-DD" com: números, padrões, **no máximo 3 experimentos** (cada um com hipótese, como medir e
quando revisar) e as perguntas para a dona. Regra: erro que se repete 2 vezes vira **teste ou regra de lint**, não só texto.
Não altere regras do processo, do `CLAUDE.md` nem ADRs sem aprovação dela. O que ela aprovar entra em `docs/APRENDIZADOS.md`.
