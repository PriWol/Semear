// Este teste lê o workflow de deploy do site (.github/workflows/publicar-site.yml) de propósito: só a dona
// do produto mescla mudanças ali, e as garantias abaixo (baixar volumes E cadernos, recusar nome inválido,
// conferir %PDF- e páginas) foram aprovadas por ela. Se alguém reverter uma delas, o `npm run check` falha.
import { spawnSync } from 'node:child_process';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
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

// Executa de verdade o `run:` do passo, com curl e pdfinfo falsos: os testes de texto acima não pegam
// lógica quebrada (por exemplo, uma comparação de páginas que nunca falha).
const script = (() => {
  const linhas = passo.split('\n');
  const i = linhas.findIndex((l) => l.trim() === 'run: |');
  const corpo = linhas.slice(i + 1).filter((l) => l.trim() !== '');
  const recuo = corpo[0]!.length - corpo[0]!.trimStart().length;
  return corpo.map((l) => l.slice(recuo)).join('\n');
})();

interface Caso {
  catalogo: {
    volumes: { arquivo: string; paginas: number }[];
    cadernos: { arquivo: string; paginas: number }[];
  };
  paginasReais?: number;
  cabecalho?: string;
}

function rodarPasso({ catalogo, paginasReais = 3, cabecalho = '%PDF-1.4' }: Caso) {
  const cwd = mkdtempSync(join(tmpdir(), 'deploy-cwd-'));
  const runnerTemp = mkdtempSync(join(tmpdir(), 'deploy-rt-'));
  const bin = join(cwd, 'bin');
  mkdirSync(bin);
  mkdirSync(join(cwd, 'content'));
  writeFileSync(join(cwd, 'content/tesouro.json'), JSON.stringify(catalogo));
  const falso = (nome: string, corpoScript: string) => {
    writeFileSync(join(bin, nome), `#!/bin/bash\n${corpoScript}\n`);
    chmodSync(join(bin, nome), 0o755);
  };
  falso(
    'curl',
    'while [ $# -gt 0 ]; do [ "$1" = --output ] && saida="$2"; shift; done\nprintf "%s" "$FAKE_CABECALHO" > "$saida"',
  );
  falso('pdfinfo', 'echo "Pages:          $FAKE_PAGINAS"');
  const r = spawnSync('/bin/bash', ['-e', '-c', script], {
    cwd,
    encoding: 'utf8',
    env: {
      PATH: `${bin}:${process.env.PATH ?? ''}`,
      RUNNER_TEMP: runnerTemp,
      REPO: 'dono/repo',
      FAKE_CABECALHO: cabecalho,
      FAKE_PAGINAS: String(paginasReais),
    },
  });
  return { codigo: r.status, saida: `${r.stdout}${r.stderr}` };
}

const comArquivos = (...arquivos: string[]): Caso['catalogo'] => ({
  volumes: arquivos.map((a) => ({ arquivo: `tesouro/${a}`, paginas: 3 })),
  cadernos: [],
});

describe('deploy do site: o passo roda de verdade (sem rede)', () => {
  it('catálogo válido, volumes e cadernos: sai com 0', () => {
    const r = rodarPasso({
      catalogo: {
        volumes: [{ arquivo: 'tesouro/volume1-tela.pdf', paginas: 3 }],
        cadernos: [{ arquivo: 'tesouro/caderno-tela.pdf', paginas: 3 }],
      },
    });
    expect(r.saida).not.toContain('::error::');
    expect(r.codigo).toBe(0);
  });

  it.each(['../x.pdf', 'a;b.pdf', 'x.txt'])('nome inválido %s: falha com a mensagem', (nome) => {
    const r = rodarPasso({ catalogo: comArquivos(nome) });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toContain('::error::nome de arquivo inválido');
  });

  it('páginas diferentes do catálogo: falha com a mensagem', () => {
    const r = rodarPasso({ catalogo: comArquivos('volume1-tela.pdf'), paginasReais: 4 });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toMatch(/::error::.*páginas/);
  });

  it('arquivo sem %PDF-: falha', () => {
    const r = rodarPasso({ catalogo: comArquivos('volume1-tela.pdf'), cabecalho: '<html>' });
    expect(r.codigo).not.toBe(0);
  });
});
