# CLAUDE.md: regras do projeto Semear

Este arquivo é lido automaticamente por agentes de IA (Claude Code) no início de cada sessão.
Ele vale também para pessoas. Se uma regra daqui mudar, registre o motivo num ADR (`docs/adr/`).

## O que é o Semear
App para famílias que educam em casa (homeschooling e afterschooling), para crianças de 3 a 8 anos.
O educador cadastra a família e as crianças, posiciona cada criança numa **jornada por domínios**
(domínio → linha → marco) e gera **pacotes de sessão** para imprimir ou abrir num tablet.
**A criança nunca usa o app.** Especificação completa: `docs/JORNADA_SPEC.md`.

## Mapa do repositório
| Caminho | O que é |
|---|---|
| `app/` | **App novo** (Vite + TypeScript + PWA), publicado no GitHub Pages a cada merge no `main` que altere `app/` (ADR 0009). |
| `app/content/` | Conteúdo curado (marcos, atividades, livros) em JSON. Ver `app/content/README.md`. |
| `docs/` | Especificação, identidade visual (`DESIGN.md`), roteiro por fases (`ROADMAP.md`), ADRs e guia de aprendizado. |
| `tesouro-marina/` | Coleção editorial impressa *O Grande Tesouro de Marina* (PDFs A4 gerados em Python + Playwright). Fora do `app/` e sem dados de família (ADR 0011). |
| `prototipos/` | Mocks dos pacotes de sessão e das direções visuais (`design/`); referência visual, não é código do app. |
| raiz (`index.html`, `assets/`, `data/`) | **Site antigo**, não é mais publicado (ADR 0009). Será arquivado; não alterar sem pedido explícito. |

## Comandos (rodar dentro de `app/`)
```bash
npm ci               # instala dependências exatas do package-lock
npm run dev          # app em modo desenvolvimento
npm run check        # typecheck + lint + formatação + testes unitários/integração (rodar antes de todo commit)
npm run test:e2e     # testes ponta a ponta (Playwright, desktop e celular)
npm run build        # build de produção em app/dist
```

## Arquitetura (ver ADR 0003)
```
pages/ (telas) ──► domain/ (regras puras)
   │                 ▲
   ├──► dados/ (IndexedDB) ─┘ tipos
   └──► pacote/ (gera o HTML do pacote) ──► domain/
```
- `src/domain/`: **regras de negócio puras**. Sem acesso a `window`, `document`, banco ou rede.
  Recebem tudo por parâmetro (inclusive a data de "agora"). O ESLint bloqueia imports proibidos.
- `src/dados/`: único lugar que fala com o IndexedDB, por meio de um **repositório** (ADR 0002).
- `src/pacote/`: transforma uma sessão em um documento HTML imprimível (ADR 0004). Usa o helper de
  escape `src/ui/html.ts` (o único import de `ui/` permitido fora das telas).
- `src/pages/` e `src/ui/`: telas. Toda interpolação de texto em HTML passa pelo `html```
  de `src/ui/html.ts`, que escapa o conteúdo (proteção contra injeção de HTML).

## Convenções
- **Português** para nomes do domínio (`marco`, `linha`, `fronteira`, `pacote`), igual ao glossário
  em `docs/GUIA_APRENDIZADO.md`. Termos técnicos genéricos podem ficar em inglês.
- TypeScript estrito: sem `any`, sem `!` desnecessário, sem desligar regras do lint sem comentário explicando.
- Funções pequenas, com um propósito. Prefira dados imutáveis e funções puras.
- Comentários explicam **por quê**, não o quê. Referencie a seção da especificação quando aplicável (ex.: `§5.6`).
- Nada de dependências novas sem justificar no PR (e num ADR, se for estrutural).

## Visual (obrigatório para telas e folhas)
Siga `docs/DESIGN.md` (direção A, "Caderno de botânica"; ADR 0014). Cores, fontes e medidas vêm dos tokens
`--s-*` de `app/src/tokens.css`; não escreva valores soltos. Ilustrações só de domínio público, com fonte registrada.

## Privacidade (inegociável)
- Dados da criança (nome, nascimento, marcos, sessões) **ficam no aparelho**. Nenhum envio para servidor,
  analytics ou serviço externo sem um ADR aprovado.
- Fontes do Google são a única chamada externa permitida hoje (não enviam dados da família).
- Todo dado vindo de fora (backup importado, conteúdo) é **validado antes de usar**: valores fora dos
  conjuntos conhecidos (vertentes, letras, estados) são recusados ou trocados pelo padrão.
- O pacote gerado tem CSP própria e a prévia roda num iframe `sandbox` sem a origem do app.

## Fluxo de trabalho com IA (ADR 0006 e 0007)
1. **Spec**: descreva a funcionalidade (o quê e por quê) ou aponte a seção da especificação.
2. **Plano**: a IA propõe o plano e a pessoa aprova antes de codar.
3. **Testes**: escreva/atualize os testes que descrevem o comportamento esperado.
4. **Código**: implemente até os testes passarem.
5. **Revisão**: `npm run check` e `npm run test:e2e` verdes; PR revisado por dois agentes
   (correção e segurança/privacidade) e aprovado pela dona do produto.

## Estórias (issues) e pull requests
- Todo PR que **entrega** uma estória traz, no corpo, uma linha `Closes #N` por estória (também vale
  `Fixes`/`Resolves`). Palavras como "Fecha" ou "Entrega" **não** fecham a estória no GitHub.
- PR que só **avança** uma estória usa `Refs #N` e não a fecha.
- Estória com critério de aceite que depende de decisão da dona do produto (rótulo `decisao`) só fecha
  depois que a decisão é registrada na própria estória.
- Ao abrir o PR, confira se a estória aparece como ligada; ao mergear, a estória fecha sozinha.

## Definição de pronto
- [ ] Testes cobrindo as regras novas (unitários no domínio; integração no `dados/`; e2e se mudou um fluxo de tela).
- [ ] `npm run check` e `npm run test:e2e` passando.
- [ ] Conteúdo novo passa na validação (`tests/conteudo.test.ts`).
- [ ] Todo marco novo traz `orientacaoPais` (por que importa, como participar, sinais de atenção e referências); sem ela a validação falha (ADR 0017).
- [ ] Decisão técnica relevante registrada em `docs/adr/`.
- [ ] Conceito técnico novo explicado no `docs/GUIA_APRENDIZADO.md`.
- [ ] Especificação atualizada se o comportamento mudou.
