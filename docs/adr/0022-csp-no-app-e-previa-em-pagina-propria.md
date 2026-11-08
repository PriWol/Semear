# 0022. CSP no app e prévia do pacote em página própria

- **Status:** Aceito
- **Data:** 2026-11-08

## Contexto
A estória #32 pede uma política de segurança de conteúdo (CSP) no app como segunda camada contra injeção de código. A prévia do pacote roda num `iframe sandbox` com `srcdoc`, e um iframe `srcdoc` **herda a CSP do app**. O pacote tem script inline (modo tablet, impressão), que `script-src 'self'` bloquearia.

## Opções consideradas
1. **Blob URL no iframe** (sugestão da estória): testada e descartada. O iframe com `sandbox` tem origem opaca e não consegue abrir um blob criado pela origem do app (fica em branco); além disso, blob também herda a CSP do criador.
2. **Liberar `unsafe-inline` no app:** anula a proteção.
3. **Página de prévia própria** (`public/previa.html`), com CSP separada, que recebe o pacote por `postMessage` e o escreve com `document.write`.

## Decisão
Opção 3.
- `app/index.html` ganha a CSP por `<meta>`: `script-src 'self'`, `connect-src 'self'`, `style-src 'self' 'unsafe-inline'` + Google Fonts, `font-src` Google Fonts, `img-src 'self' data: blob:`, `object-src 'none'`.
- O iframe carrega `./previa.html` (sandbox `allow-scripts allow-modals`, sem a origem do app). A página só aceita **uma** mensagem, vinda da janela-mãe, e o pacote continua com a CSP própria dele (`connect-src 'none'`, `img-src 'none'`).
- O teste `e2e/csp.spec.ts` percorre o fluxo até a prévia e falha se aparecer qualquer violação de CSP no console, além de conferir que o script do pacote roda.

## Consequências
- O app tem uma camada a mais contra XSS, e a prévia continua isolada e sem rede.
- `previa.html` é um arquivo estático a mais no precache do PWA.
- Sem `unsafe-eval`: qualquer biblioteca nova que use `eval` quebra e é recusada.
- No modo dev do Vite o HMR usa websocket na mesma origem (`connect-src 'self'`); não foi exercitado em teste automático.
