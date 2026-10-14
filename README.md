# 🌱 Semear

App para famílias que educam os filhos em casa (homeschooling e afterschooling), de 3 a 8 anos.
O educador posiciona cada criança numa **jornada por domínios** (domínio → linha → marco) e, antes de
cada sessão, gera um **pacote para imprimir ou abrir no tablet**: roteiro, materiais, folhas da criança
e ficha de registro. **A criança nunca usa o app.**

**🌐 Acesse:** https://priwol.github.io/Semear/

## ✨ O que dá para fazer

- Cadastrar a família (vertente principal e inspirações: Montessori, Waldorf, Clássico, Religioso, Charlotte Mason) e as crianças.
- Posicionar cada criança na jornada de Linguagem, Matemática e Línguas, marco a marco.
- Preparar uma sessão: o app sugere atividades para os marcos que a criança está trabalhando.
- Imprimir, salvar em PDF ou baixar o pacote (funciona offline no tablet).
- Backup e restauração dos dados, que ficam **só no aparelho**.

## 📚 Documentação

| Documento | Para quê |
|---|---|
| [`docs/JORNADA_SPEC.md`](docs/JORNADA_SPEC.md) | Especificação do produto e decisões |
| [`CLAUDE.md`](CLAUDE.md) | Regras do projeto (para pessoas e para a IA) |
| [`docs/adr/`](docs/adr/) | Decisões técnicas e seus porquês |
| [`docs/GUIA_APRENDIZADO.md`](docs/GUIA_APRENDIZADO.md) | Conceitos técnicos explicados para gestão |
| [`app/content/README.md`](app/content/README.md) | Como escrever conteúdo (marcos, atividades, livros) |

## 💻 Rodar localmente

```bash
cd app
npm ci
npm run dev        # http://localhost:5173
npm run check      # tipos, lint, formatação e testes
npm run test:e2e   # testes ponta a ponta (desktop e celular)
```

## 🛠️ Tecnologias

Vite + TypeScript (PWA), IndexedDB (`idb`) para os dados locais, Vitest e Playwright para testes,
GitHub Actions para CI, revisão por agentes e publicação no GitHub Pages.

> Os arquivos na raiz (`index.html`, `assets/`, `data/` e os `.md` antigos) são do **site antigo**,
> que não é mais publicado. O arquivamento está na issue #32.

## 📝 Licença

MIT
