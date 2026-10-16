# 0016. Orientação para os pais é obrigatória em todo marco

- **Status:** Aceito. Complementa o ADR 0005.
- **Data:** 2026-10-16

## Contexto

Cada marco ganhou um texto pedagógico para os pais ("Para os pais"): por que o marco importa, como participar,
sinais de atenção, trechos por vertente e referências bibliográficas. No começo o campo `orientacaoPais` era
opcional e a falta dele só gerava um aviso, para que o conteúdo entrasse aos poucos. Agora que as linhas
`LG.FON` e `MA.SEN` estão completas, a dona do produto definiu que **todo marco novo inclui a orientação**.

## Opções consideradas

1. **Manter como aviso:** o conteúdo entra rápido, mas marcos sem texto se acumulam e a família vê uma jornada
   desigual, com apoio em alguns marcos e nenhum em outros.
2. **Tornar obrigatório (erro de validação):** nenhum marco chega à família sem o texto, e o custo de escrevê-lo
   fica junto do custo de escrever o marco.

## Decisão

Opção 2. `Marco.orientacaoPais` é obrigatório no tipo, e a validação do conteúdo (`validarConteudo`) acusa
**erro** em marco sem ele, o que faz o CI falhar (ADR 0005). Continuam opcionais `porVertente` e o link das
referências. A "Definição de pronto" do `CLAUDE.md` passa a incluir o item.

## Consequências

- Escrever um marco novo exige escrever também a orientação (texto geral, referências do catálogo e, onde
  houver algo a acrescentar, trechos por vertente). É mais trabalho por marco, mas a revisão pedagógica acontece
  no mesmo PR.
- As referências precisam existir no catálogo `referencias.json`; a validação recusa id inexistente.
- O texto continua sendo rascunho até a revisão da dona do produto: a obrigatoriedade garante que existe, não que
  foi revisado.
- Se o ritmo de produção de conteúdo (estória #21) pedir entrada em etapas, a regra pode voltar a ser aviso por um
  novo ADR que substitua este.
