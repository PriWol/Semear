# 0012. Versão visível no app e atualização com aviso

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

Cada merge no `main` publica o app (ADR 0009), mas olhando o site não dava para saber qual versão
estava no ar. Como o app é um PWA, o navegador também pode continuar mostrando a versão guardada
em cache até a próxima abertura. A dona do produto testa cada fase no site publicado (sem prévia
por PR, decisão de 14/10 na #40), então precisa saber exatamente o que está testando. (#38)

## Opções consideradas

1. **Atualização automática (`autoUpdate`, como antes):** o service worker novo assume sozinho. Mas a
   tela aberta continua com o código antigo até recarregar, e não há como avisar.
2. **Atualização com aviso (`prompt`):** o service worker novo fica esperando; o app mostra
   "Nova versão disponível · Atualizar" e troca quando o educador toca. Não interrompe quem está
   no meio de uma tarefa (ex.: preparando uma sessão).
3. Recarregar a página sozinho quando houver versão nova: simples, mas pode perder o que a pessoa
   estava preenchendo.

## Decisão

- Opção 2: `registerType: 'prompt'`, com o registro feito em `src/main.ts` (`virtual:pwa-register`).
- A versão aparece no topo (`v0.2 · 14/10`) e completa em Configurações (número, data do build e
  código curto do commit). O número vem do `package.json`; a data e o commit são embutidos no build
  (`define` no `vite.config.ts`; no CI, o commit vem de `GITHUB_SHA`).
- Cada fase do roteiro (`docs/ROADMAP.md`) sobe a versão "do meio" (Fase 0 = 0.2.0). Correções
  dentro de uma fase sobem o último número (0.2.1).
- A página "Novidades" lê `app/content/novidades.json`. Um teste falha se a versão do `package.json`
  não tiver uma entrada nas novidades: quem sobe a versão precisa contar o que mudou.

## Consequências

- Mais fácil: saber o que está no ar e relatar problemas citando a versão.
- O serviço continua 100% local: nada é consultado num servidor para saber a versão.
- Quem nunca tocar em "Atualizar" continua na versão antiga até fechar todas as abas do app; o
  navegador troca sozinho nesse momento.
- A troca foi verificada simulando duas publicações seguidas num navegador real: a faixa aparece e
  "Atualizar" carrega a versão nova.
