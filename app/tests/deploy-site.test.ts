// Este teste lê o workflow de deploy do site (.github/workflows/publicar-site.yml) de propósito: só a dona
// do produto mescla mudanças ali, e as garantias abaixo (baixar volumes E cadernos, recusar nome inválido,
// conferir %PDF- e páginas) foram aprovadas por ela. Se alguém reverter uma delas, o `npm run check` falha.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const workflow = readFileSync(
  resolve(__dirname, '../../.github/workflows/publicar-site.yml'),
  'utf8',
);
const passo = (() => {
  const inicio = workflow.indexOf('- name: Baixar os PDFs do Tesouro');
  const fim = workflow.indexOf('- uses: actions/upload-pages-artifact', inicio);
  expect(inicio, 'passo de download existe').toBeGreaterThan(-1);
  return workflow.slice(inicio, fim);
})();

describe('deploy do site: PDFs do Tesouro (ADR 0015, adendo)', () => {
  it('baixa os volumes e os cadernos do catálogo', () => {
    expect(passo).toContain('...c.volumes');
    expect(passo).toContain('...c.cadernos');
  });

  it('recusa nome de arquivo inválido e falha o job', () => {
    expect(passo).toContain('::error::nome de arquivo inválido');
    expect(passo).toMatch(/nome de arquivo inválido[^\n]*exit 1/);
  });

  it('confere o cabeçalho %PDF-', () => {
    expect(passo).toContain("grep -q '^%PDF-'");
  });

  it('garante o pdfinfo e falha se as páginas divergirem do catálogo', () => {
    expect(passo).toContain('pdfinfo');
    expect(passo).toContain('poppler-utils');
    expect(passo).toMatch(/::error::não foi possível instalar o pdfinfo/);
    expect(passo).toMatch(/::error::\$arquivo tem \$reais páginas/);
  });
});
