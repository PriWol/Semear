# 0004. Pacote de sessão como HTML + impressão do navegador

- **Status:** Aceito
- **Data:** 2026-10-14

## Contexto

O pacote (roteiro, folhas, ficha) precisa sair em A4 para imprimir e num "modo tablet", gerado
no aparelho e sem servidor (decisão 22 da especificação). Emojis e fontes precisam sair nítidos.

## Opções consideradas

1. **HTML + CSS de impressão + "Imprimir / Salvar como PDF" do navegador**: texto vetorial e nítido,
   zero dependências, funciona offline.
2. **Biblioteca de PDF no navegador (jsPDF, pdf-lib)**: arquivo PDF direto, mas o layout teria de ser
   reescrito em coordenadas, ou rasterizado como imagem (perde nitidez, arquivos grandes).
3. **Servidor gerando PDF**: melhor controle, mas exige backend e deixa de ser offline.

## Decisão

Opção 1. `src/pacote/` gera um **documento HTML completo e autossuficiente** (CSS embutido, barra com
botões de imprimir, modo tablet e troca de letra). O app oferece: pré-visualizar, imprimir/salvar PDF
e **baixar o arquivo HTML** para abrir offline no tablet.

## Segurança (após a revisão do PR #1)

- O documento traz uma **CSP** própria (`default-src 'none'`, sem conexões nem imagens externas):
  mesmo que algum texto escape da proteção, não consegue enviar dados para fora.
- A prévia no app roda num iframe **`sandbox`** sem a origem do app, então o pacote não acessa o
  IndexedDB. Por isso o botão "Imprimir" do app pede a impressão por mensagem (`postMessage`).

## Consequências

- O "Salvar como PDF" depende do diálogo de impressão do navegador (um passo a mais para o pai).
- Fontes vêm do Google Fonts; sem internet, o arquivo baixado usa fontes do sistema.
- Se as famílias pedirem PDF direto, avaliamos a opção 2 num novo ADR.
