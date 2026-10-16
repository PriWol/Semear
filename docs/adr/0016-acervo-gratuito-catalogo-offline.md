# 0016. Acervo gratuito como catálogo curado offline

- **Status:** Aceito.
- **Data:** 2026-10-16

## Contexto

A dona do produto quer um acervo gratuito, com busca, de livros em português, inglês, latim e francês para
crianças de 2 a 8 anos. O CLAUDE.md proíbe chamadas externas sem ADR: a busca ao vivo em Internet Archive,
Gutenberg, Wikisource e similares enviaria o termo digitado a serviços de terceiros e exigiria abrir a CSP.

## Opções consideradas

1. **Busca ao vivo nas APIs das fontes:** cobertura ampla, mas envia o que a família digita para fora e
   depende de serviços que mudam.
2. **Catálogo curado em JSON, com busca no aparelho:** nenhuma chamada externa; os links só abrem quando a
   pessoa clica.

## Decisão

Opção 2. `app/content/acervo.json` lista obras de domínio público ou licença aberta, com idioma, faixa etária,
fonte, licença e endereço. A busca (`src/domain/acervo.ts`) é uma função pura. Cada item tem `tipoLink`:
`obra` abre o livro; `busca` abre a busca da própria fonte pelo título (não quebra se a fonte reorganizar os
endereços). A validação recusa endereço que não seja `https` e faixa fora de 2–8 anos.

Os livros da curadoria ganham `editora` e `linkCompra` opcionais, também só `https`.

## Consequências

- Nada muda na privacidade: nenhum dado sai do aparelho; abrir um link é uma ação explícita, em outra aba, com `noopener`.
- O acervo precisa de revisão periódica de links e licenças. A busca ao vivo fica como estória futura, com novo ADR.
