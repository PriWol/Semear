# 0009. Publicação do app no GitHub Pages via GitHub Actions

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
A v1 do app (`app/`) ficou pronta e a dona do produto pediu para substituir o site antigo publicado em
`https://priwol.github.io/Semear/`. O site antigo era publicado direto da raiz do branch `main`.
O app novo precisa de um passo de build (Vite), então não dá para publicar os arquivos-fonte.

## Opções consideradas
1. **GitHub Actions publicando `app/dist` no Pages:** build verificado a cada merge, sem arquivos
   gerados no repositório. Exige mudar uma vez a fonte do Pages para "GitHub Actions".
2. **Commitar o build na raiz ou num branch `gh-pages`:** arquivos gerados no Git, fácil de esquecer de
   atualizar, e diffs enormes nos PRs.
3. **Outro serviço (Netlify, Cloudflare Pages):** prévias por PR, mas exige conta e configuração externa.

## Decisão
Opção 1 (`.github/workflows/publicar-site.yml`). O workflow roda `npm run check` antes do build: nada que
falhe nas verificações chega às famílias. O mesmo endereço continua valendo (`base: './'` no Vite e
rotas por hash funcionam em `/Semear/`).

**Transição do site antigo** (simulada num navegador antes de publicar):
- O site antigo usava endereços como `/Semear/onboarding`, que dariam 404. O app publica um `404.html`
  que redireciona qualquer endereço desconhecido para o início do app.
- O antigo registrava `service-worker.js` e guardava páginas em cache. O service worker do app novo
  (`sw.js`) assume o mesmo escopo; o app apaga os caches antigos (`semear-v*`) ao abrir, e um
  `service-worker.js` de "faxina" faz o mesmo para quem ainda carregar a página antiga. Os dados que famílias tenham salvo no site antigo (localStorage) não
são migrados: o modelo de dados é outro e o site antigo estava em fase de MVP.

## Consequências
- Todo merge que toca `app/` publica automaticamente em ~2 minutos.
- O site antigo (raiz do repositório) deixa de ser publicado. Os arquivos ficam até serem arquivados.
- Prévias por PR não existem; se fizerem falta para testes com famílias, revisitar a opção 3.
