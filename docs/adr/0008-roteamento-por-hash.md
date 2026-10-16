# 0008. Roteamento por hash (`#/`)

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto
O app é publicado como arquivos estáticos (GitHub Pages), sem servidor. O app antigo usava caminhos
como `/weekly-plan`, que davam erro 404 ao recarregar a página (exigiam o truque do `404.html`).

## Decisão
Rotas no formato `#/jornada/<id>`. O servidor sempre entrega `index.html`, e o app lê o que vem depois do `#`.

## Consequências
- Recarregar e compartilhar links funciona em qualquer hospedagem estática, inclusive offline.
- URLs ficam com `#` (estética, sem impacto para as famílias).
