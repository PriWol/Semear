# 0001. Reconstruir o app com Vite + TypeScript, como PWA

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

O Semear original é JavaScript puro, sem tipos e sem testes. A jornada traz regras com consequência
para as famílias (posição da criança, marcos ativos, sugestão de sessão), e o produto vai crescer
(contas, sincronização, portfólio). Precisamos de segurança para mudar o código sem quebrar o que funciona.

## Opções consideradas

1. **Evoluir o JS atual**: começo rápido, mas cada mudança fica mais arriscada conforme o código cresce.
2. **Vite + TypeScript (sem framework de UI)**: tipos pegam erros antes de rodar; build rápido; pouco peso.
3. **React + TypeScript**: ecossistema enorme, mais peso e mais conceitos.

## Decisão

Opção 2. O app novo vive em `app/`, e o site antigo continua no ar até a v1 ficar pronta.
Continua sendo PWA (instalável, funciona offline) via `vite-plugin-pwa`.

## Consequências

- Erros de tipo aparecem no editor e no CI, antes de chegar às famílias.
- Telas são escritas com HTML em template strings (sem framework). Se a interface ficar complexa,
  podemos adotar uma biblioteca de UI depois, porque as regras de negócio estão separadas (ADR 0003).
- Contratar pessoas depois: TypeScript é muito difundido.
