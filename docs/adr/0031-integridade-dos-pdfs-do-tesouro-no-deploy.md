# 0031. Integridade dos PDFs do Tesouro no deploy

- **Status:** Proposto
- **Data:** 2026-11-20

## Contexto
O deploy do site (`publicar-site.yml`) baixa da Release pública `tesouro-marina` os PDFs `*-tela` listados em
`app/content/tesouro.json` e os publica junto com o app (ADR 0011 e 0015). Hoje só conferimos nome, cabeçalho
`%PDF-` e número de páginas. Um PDF corrompido no envio, trocado por engano ou enviado pela metade passaria, desde
que ainda parecesse um PDF com a paginação certa. A estória #111 pede verificação de integridade (sha256).
Os PDFs são regenerados a cada merge em `tesouro-marina/`, então o hash não pode ficar fixo no repositório.

## Opções consideradas
1. **Hash fixo no catálogo (`tesouro.json`):** simples, mas muda a cada regeneração e exigiria um commit extra por
   merge; build determinístico dos PDFs não existe hoje.
2. **Manifesto `SHA256SUMS` publicado na própria Release:** gerado pelo mesmo workflow que gera os PDFs, sem commit
   extra. Exige ordem de publicação e um passo a mais no deploy.
3. **Atestado de proveniência (assinatura/attestation do GitHub):** protege também contra quem escreve na Release,
   mas é bem mais trabalho e dependência de serviço.

## Decisão
Opção 2.
- `publicar-tesouro.yml` gera `pdfs/SHA256SUMS` (`sha256sum *.pdf`, formato `<hash>  <arquivo>`) ao juntar os
  PDFs. No job de publicação, envia os PDFs primeiro e o manifesto **por último** (`--clobber`). A limpeza de
  anexos antigos preserva o manifesto, porque ele existe em `pdfs/`.
- O passo "Baixar os PDFs do Tesouro" de `publicar-site.yml` baixa o manifesto **antes** dos PDFs e falha
  (`::error::`) se ele faltar ou vier vazio. Para cada PDF do catálogo exige **exatamente uma** linha
  `^[0-9a-f]{64}  <arquivo>$` (comparação de texto, não regex, para o ponto do nome não virar curinga) e compara
  com o `sha256sum` do arquivo baixado, antes de `%PDF-` e do `pdfinfo`. Sem entrada: `sem entrada no manifesto`;
  hash diferente: `sha256 não confere`.
- O manifesto é **dado externo**: só é lido com `awk`, nunca executado, e o nome já passou pela validação do
  catálogo. Não usamos a verificação em lote do `sha256sum`, que aceitaria linhas extras ou malformadas. Linhas
  que não são do catálogo são ignoradas.
- `app/tests/deploy-site.test.ts` executa o `run:` real, sem rede, cobrindo caso feliz, PDF adulterado, manifesto
  ausente ou vazio, PDF sem entrada e entradas malformadas.

## Consequências
- **Limite honesto:** o manifesto protege contra troca acidental, corrupção e envio parcial. **Não** protege
  contra quem tem escrita na Release: essa pessoa troca PDF e manifesto juntos. Atestado de proveniência (opção 3)
  fica como evolução.
- **Ordem de adoção:** `publicar-tesouro.yml` precisa rodar no `main` (merge ou `workflow_dispatch`) antes do
  próximo deploy do site; senão o deploy falha por manifesto ausente.
- **Mistura de gerações:** se o deploy ler a Release no meio de uma publicação (PDFs novos, manifesto antigo), a
  conferência falha fechada e basta reexecutar o deploy depois que a publicação terminar.
- O envio à Release continua não atômico (ADR 0011); o manifesto por último reduz, mas não elimina, a janela.
