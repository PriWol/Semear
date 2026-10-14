# ADRs: registros de decisão de arquitetura

Um ADR (*Architecture Decision Record*) é uma página curta que responde: **"por que fizemos assim?"**.
Cada um tem contexto, opções consideradas, decisão e consequências. ADRs não são apagados:
quando uma decisão muda, cria-se um novo ADR que **substitui** o anterior.

| # | Decisão | Status |
|---|---|---|
| [0001](0001-vite-typescript-pwa.md) | Reconstruir o app com Vite + TypeScript, como PWA | Aceito |
| [0002](0002-local-first-indexeddb.md) | Dados no aparelho com IndexedDB (`idb`) atrás de um repositório | Aceito |
| [0003](0003-camadas-nucleo-funcional.md) | Camadas com núcleo funcional (domínio puro) | Aceito |
| [0004](0004-pacote-html-impressao.md) | Pacote de sessão como HTML + impressão do navegador | Aceito |
| [0005](0005-conteudo-json-versionado.md) | Conteúdo curado em JSON versionado e validado por testes | Aceito |
| [0006](0006-piramide-de-testes-e-ci.md) | Pirâmide de testes e CI obrigatória | Aceito |
| [0007](0007-revisao-por-agentes.md) | Revisão por dois agentes + aprovação humana; PR único da v1 | Aceito |
| [0008](0008-roteamento-por-hash.md) | Roteamento por hash (`#/`) | Aceito |
| [0009](0009-publicacao-github-pages.md) | Publicação do app no GitHub Pages via GitHub Actions | Aceito |
| [0010](0010-modelo-de-negocio-livre-familia.md) | Modelo de negócio: plano Livre + assinatura por família | Aceito |
| [0011](0011-colecao-editorial-tesouro-marina.md) | Coleção editorial impressa em `tesouro-marina/`, fora do app | Aceito |
| [0012](0012-versao-visivel-e-atualizacao-com-aviso.md) | Versão visível no app e atualização com aviso | Aceito |
| [0013](0013-familia-de-exemplo-com-marcador-por-registro.md) | Família de exemplo com marcador por registro | Aceito |

Modelo para um novo ADR: copie `0000-modelo.md`.
