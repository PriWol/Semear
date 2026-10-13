# Semear · app

App das famílias (Vite + TypeScript + PWA). Regras do projeto: [`../CLAUDE.md`](../CLAUDE.md).
Especificação: [`../docs/JORNADA_SPEC.md`](../docs/JORNADA_SPEC.md). Decisões técnicas: [`../docs/adr/`](../docs/adr/).

```bash
npm ci            # instala
npm run dev       # abre em http://localhost:5173
npm run check     # tipos + lint + formatação + testes
npm run test:e2e  # testes ponta a ponta (desktop e celular)
```

Estrutura: `src/domain` (regras puras) · `src/dados` (IndexedDB) · `src/pacote` (HTML imprimível) ·
`src/pages` e `src/ui` (telas) · `content/` (conteúdo curado) · `tests/` (unitários e integração) · `e2e/`.
