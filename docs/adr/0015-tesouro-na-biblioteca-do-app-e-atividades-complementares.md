# 0015. Tesouro na biblioteca do app e atividades complementares

- **Status:** Aceito (piloto com o Volume 4). Complementa o ADR 0011.
- **Data:** 2026-10-15

## Contexto

O ADR 0011 manteve _O Grande Tesouro de Marina_ fora do app. Agora a dona do produto quer que o material
alimente a jornada Clássica (piloto: Volume 4, música). Os domínios AR, NM e DI não têm marcos
(especificação §3.0); suas atividades devem entrar nas sessões como "complementares", mas o gerador de sessão
(§5.6) e a validação (ADR 0005) só conheciam atividades com marco.

## Opções consideradas

1. **PDFs no Git / no app:** pesa o repositório e o cache offline (cerca de 29 MB por volume).
2. **Link para o arquivo na Release:** a Release entrega o PDF como download, sem abrir no navegador nem na página.
3. **Baixar os PDFs da Release no deploy do site e servi-los na mesma origem:** abre inline, aceita `#page=N`,
   não envia nada para fora e não aumenta o Git.

## Decisão

Opção 3, mais as mudanças de modelo abaixo.

- **Complementar** é uma atividade com `marcos: []`, `dominio` (domínio sem jornada) e `categoria` (uma das
  categorias do domínio). A validação recusa atividade sem marco que não cumpra isso.
- **`materialImpresso`** (`volume`, `unidade`, `paginas`) liga a atividade ao trecho do volume. A ficha e o
  roteiro mostram o trecho; a Biblioteca abre o PDF direto na unidade.
- **Gerador de sessão:** depois de preencher a duração com a jornada, entra **no máximo uma** complementar,
  só se couber na duração, adequada à idade, publicada e pontuada como as demais (vertente, inspiração, novidade).
  O "Trocar" percorre as outras complementares.
- **Catálogo** `app/content/tesouro.json`: volumes, arquivo e unidades com páginas. Um teste confere que cada
  `materialImpresso` aponta para uma unidade do catálogo.
- **Site:** o workflow `publicar-site.yml` baixa, para `dist/tesouro/`, os PDFs `*-tela` listados no catálogo,
  a partir da Release pública `tesouro-marina`, e confere o cabeçalho `%PDF-`. O service worker não os guarda
  no cache offline nem responde por eles (`navigateFallbackDenylist`). É preciso estar online ou ter baixado o arquivo.
- **Rascunho:** as 8 atividades do Volume 4 entram como `rascunho` (origem `ia`). Só aparecem para as famílias
  quando a dona do produto revisar e publicar.

## Consequências

- O site depende da Release existir no momento do deploy; sem ela o deploy falha (melhor que publicar link quebrado).
- Privacidade inalterada: nenhum dado da família sai do aparelho, e o PDF vem do mesmo domínio do app.
- O catálogo é mantido à mão neste piloto; se os volumes mudarem de paginação, atualize o catálogo e rode `npm run check`.
- Atividades complementares ainda não têm "tema"; a escolha usa idade, vertente e novidade.
