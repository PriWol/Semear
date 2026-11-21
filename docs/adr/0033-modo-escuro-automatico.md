# 0033. Modo escuro automático em arquivo de tokens separado

- **Status:** Aceito (decisão 4 da dona do produto, estória #130)
- **Data:** 2026-11-21

## Contexto
O app usa só tokens `--s-*` (ADR 0014). A dona do produto quer o modo escuro seguindo o aparelho, sem botão de tema (temas escolhíveis ficam para depois).
O pacote impresso embute `tokens.css` no próprio HTML (`pacote/gerar.ts`), e a folha precisa ser sempre clara (papel).

## Decisão
- Segundo conjunto dos mesmos nomes de token em `app/src/tokens-escuro.css`, dentro de `@media screen and (prefers-color-scheme: dark)`; carregado só pelo app (`main.ts`). Assim `estilos.css` e `ajustes.css` não ganham valores novos, o pacote não muda e a impressão do app (`print`) fica clara. Desvio consciente da ideia de pôr o bloco em `tokens.css`: ali ele vazaria para o pacote.
- Paleta: grafite-esverdeado quente no lugar do marfim, verde-musgo e ocre clareados, sem preto nem branco puros. Contraste AA (4,5:1 texto, 3:1 componentes) testado em `tests/tokens.test.ts` para os dois temas.
- Tokens novos para o que era fixo claro: `--s-topo*` (barra do topo vira verde-grafite no escuro), `--s-veu` (fundo das caixas de confirmação), `--s-folha` (papel da moldura da prévia).
- `color-scheme: light dark` no app; `theme-color` com `media` para claro e escuro (o manifest mantém o verde-musgo); o ícone SVG clareia o verde no escuro.
- A prévia do pacote: o iframe declara `color-scheme: light` e `previa.html` tem `<meta name="color-scheme" content="light">`, então não herda o escuro.

## Consequências
- Quem editar cor em `tokens.css` deve revisar o par em `tokens-escuro.css`; o teste de contraste cobre os dois.
- Temas escolhíveis, se vierem, podem reaproveitar este arquivo (trocar o gatilho `@media` por atributo).
