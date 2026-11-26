# 0039. Teste e2e instável fica visível no resumo do CI

- **Status:** Proposto (arquivo em `.github/`: só a dona do produto mescla, ADR 0038)
- **Data:** 2026-11-26

## Contexto
O CI repete uma vez o teste e2e que falha (`retries: 1`). Teste que só passa na repetição deixa o job verde e ninguém vê.
O problema real é o teste agir antes de a tela estar pronta. Medido: `app/e2e/` não tem esperas fixas (`waitForTimeout`,
`setTimeout`, `networkidle`), então a dívida é de espera por estado, não por tempo. Estória #172.

## Opções consideradas
1. Tirar a repetição: o e2e fica vermelho por ruído e o cartão trava em "Pronto para mesclar".
2. Manter a repetição como está: o instável continua invisível.
3. Manter a repetição e **mostrar** o instável no resumo da execução, com trace guardado: custo baixo e o job segue verde.

## Decisão
Opção 3.
- Em CI, o Playwright grava também `app/playwright-report/resultados.json` e o trace na repetição (`on-first-retry`).
  Local não muda (`retries: 0`, `retain-on-failure`).
- O script `.github/scripts/resumo-e2e-instaveis.mjs` (Node, sem dependência) lê o JSON e escreve no `GITHUB_STEP_SUMMARY`
  só nome do teste, aparelho (desktop ou celular) e arquivo. Sem instáveis, diz que nenhum foi encontrado.
- O artefato `relatorio-playwright` sobe sempre (`if: always()`), com retenção de 7 dias.
- Regra: o e2e espera por elemento ou estado visível, nunca por tempo. Cada teste instável vira **uma issue com o rótulo
  `e2e-instavel`**, com a causa.
- Os tetos de 40 s em `tela-cheia.spec.ts` e `csp.spec.ts` ficam, comentados: seguram o carregamento das fontes do Google no
  iframe do pacote; não há medição do tempo típico.

## Consequências
Mais fácil: ver o instável sem abrir logs, com trace para achar a causa. Mais difícil: o artefato sobe em toda execução
(7 dias de retenção, pequeno custo de armazenamento). O resumo não bloqueia a mescla; a triagem é por issue.
