// Imprime um HTML em PDF A4 com o Chromium do Playwright.
// uso: node pdf.js entrada.html saida.pdf
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch {
  console.error('playwright não encontrado: rode "npm ci" em tesouro-marina/editorial (veja o README).');
  process.exit(1);
}

(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // O build é offline: qualquer pedido que não seja file:// é abortado (e conta como problema).
  const externos = [];
  await page.route(/^(?!file:|data:)/, r => { externos.push(r.request().url()); r.abort(); });
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // verificação automática de transbordamento: nenhum bloco pode sair da página
  const problemas = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.pagina').forEach((pg, i) => {
      const r = pg.getBoundingClientRect();
      pg.querySelectorAll('[data-check], img, svg, p, h1, h2, h3, li, td, .carta, .bloco').forEach(el => {
        const e = el.getBoundingClientRect();
        if (e.width === 0) return;
        // camada decorativa que cobre a página inteira (fundo/moldura) sangra de propósito
        if (el.tagName.toLowerCase() === 'svg' && e.width >= r.width * 0.95 && e.height >= r.height * 0.95) return;
        const mm = 96 / 25.4, m = 8 * mm; // nada a menos de 8 mm da borda
        if (e.left < r.left + m - 0.5 || e.right > r.right - m + 0.5 ||
            e.top < r.top + m - 0.5 || e.bottom > r.bottom - m + 0.5)
          out.push(`p${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> fora da área segura`);
        if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden')
          out.push(`p${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> texto cortado`);
      });
    });
    return out;
  });
  externos.forEach(u => problemas.push(`pedido externo bloqueado: ${u}`));
  // Só grava o PDF se a diagramação estiver limpa: um arquivo ruim nunca fica no disco.
  if (problemas.length) {
    await browser.close();
    console.log('PROBLEMAS DE DIAGRAMAÇÃO:\n' + problemas.join('\n'));
    process.exit(2);
  }
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('ok', out);
})();
