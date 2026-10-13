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

Modelo para um novo ADR: copie `0000-modelo.md`.
