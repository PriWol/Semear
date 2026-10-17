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
| [0014](0014-direcao-visual-caderno-de-botanica.md) | Direção visual "Caderno de botânica" e tokens compartilhados | Aceito |
| [0015](0015-tesouro-na-biblioteca-do-app-e-atividades-complementares.md) | Tesouro na biblioteca do app e atividades complementares | Aceito |
| [0016](0016-acervo-gratuito-catalogo-offline.md) | Acervo gratuito como catálogo curado offline | Aceito |
| [0017](0017-orientacao-para-os-pais-obrigatoria-em-todo-marco.md) | Orientação para os pais é obrigatória em todo marco | Aceito |
| [0018](0018-reproducoes-de-obras-de-arte-no-volume-5.md) | Reproduções de obras de arte no Volume 5 (Commons e acervos abertos) | Aceito |
| [0019](0019-pranchas-de-naturalistas-no-volume-6.md) | Pranchas de naturalistas no Volume 6 (Commons e desenho próprio) | Aceito |

Modelo para um novo ADR: copie `0000-modelo.md`.
