// Imprime um HTML em PDF A4 com o Chromium do Playwright.
// uso: node pdf.js entrada.html saida.pdf
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // verificação automática de transbordamento: nenhum bloco pode sair da página
  const problemas = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.pagina').forEach((pg, i) => {
      const r = pg.getBoundingClientRect();
      pg.querySelectorAll('[data-check], p, h1, h2, h3, li, td, .carta, .bloco').forEach(el => {
        const e = el.getBoundingClientRect();
        if (e.width === 0) return;
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
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  if (problemas.length) { console.log('PROBLEMAS DE DIAGRAMAÇÃO:\n' + problemas.join('\n')); process.exit(2); }
  console.log('ok', out);
})();
