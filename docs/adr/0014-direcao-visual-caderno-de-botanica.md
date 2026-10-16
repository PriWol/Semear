# 0014. Direção visual "Caderno de botânica" e tokens compartilhados

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

O app usava a paleta "Mata Atlântica" (verdes e terracota), a fonte Nunito e muitos emojis. A estória #14
pediu uma identidade moderna e clássica. O protótipo `prototipos/design/direcoes-visuais.html` apresentou duas
direções: A (Caderno de botânica) e B (Biblioteca clássica). A dona do produto escolheu a **A** e pediu
ilustrações clássicas no app e nas folhas.

## Opções consideradas

1. **Tokens CSS num arquivo único (`app/src/tokens.css`)**, carregado pelo app e embutido no pacote impresso.
2. Tokens duplicados em `estilos.css` e `pacote.css`: mais simples, mas os nomes e valores divergem com o tempo.
3. Biblioteca de design em pacote npm separado: custo alto para um app deste tamanho.

## Decisão

Direção A, com a opção 1. Os tokens usam o prefixo `--s-` para não colidir com as variáveis antigas, que saem
do app (#41) e do pacote (#42) nas próximas entregas. O contraste AA é conferido por teste automatizado.
Regras completas em `docs/DESIGN.md`.

## Consequências

- Mudar a identidade passa a ser trocar valores num lugar só.
- Os pacotes baixados continuam autônomos (o CSS é embutido), e as fontes seguem vindo do Google Fonts (única
  chamada externa permitida, `CLAUDE.md`). Fraunces e Inter entram junto na aplicação das telas (#41).
- Enquanto #41 e #42 não entram, os tokens existem mas ainda não mudam a aparência.
