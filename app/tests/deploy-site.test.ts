// Este teste lê o workflow de deploy do site (.github/workflows/publicar-site.yml) de propósito: só a dona
// do produto mescla mudanças ali, e as garantias abaixo (baixar volumes E cadernos, recusar nome inválido,
// conferir %PDF-, páginas e sha256 contra o manifesto da Release) foram aprovadas por ela. Se alguém reverter uma delas, o `npm run check` falha.
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const workflow = readFileSync(
  resolve(__dirname, '../../.github/workflows/publicar-site.yml'),
  'utf8',
);
const workflowTesouro = readFileSync(
  resolve(__dirname, '../../.github/workflows/publicar-tesouro.yml'),
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

  it('confere o sha256 contra o manifesto SHA256SUMS, sem sha256sum -c', () => {
    expect(passo).toContain('SHA256SUMS');
    expect(passo).toContain('sha256sum');
    expect(passo).not.toMatch(/sha256sum\s+(-c|--check)/);
    expect(passo).toContain('::error::$arquivo sem entrada no manifesto');
    expect(passo).toContain('::error::$arquivo: sha256 não confere');
  });
});

describe('publicação do Tesouro: manifesto SHA256SUMS (ADR 0031)', () => {
  it('gera o manifesto ao juntar os PDFs', () => {
    expect(workflowTesouro).toMatch(/sha256sum \*\.pdf > SHA256SUMS/);
  });

  it('envia o manifesto à Release depois dos PDFs', () => {
    const pdfs = workflowTesouro.indexOf('gh release upload tesouro-marina pdfs/*.pdf --clobber');
    const manifesto = workflowTesouro.indexOf(
      'gh release upload tesouro-marina pdfs/SHA256SUMS --clobber',
    );
    expect(pdfs).toBeGreaterThan(-1);
    expect(manifesto).toBeGreaterThan(pdfs);
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
  /** Conteúdo que o manifesto registrou; por padrão, o mesmo do PDF servido (hash confere). */
  cabecalhoManifestado?: string;
  /** Texto do manifesto; `null` = a Release não tem o SHA256SUMS (curl --fail falha). */
  manifesto?: string | null;
}

const sha = (texto: string) => createHash('sha256').update(texto).digest('hex');

function rodarPasso({
  catalogo,
  paginasReais = 3,
  cabecalho = '%PDF-1.4',
  cabecalhoManifestado = cabecalho,
  manifesto,
}: Caso) {
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
  const arquivos = [...catalogo.volumes, ...catalogo.cadernos].map((v) =>
    v.arquivo.replace('tesouro/', ''),
  );
  const texto =
    manifesto === undefined
      ? arquivos.map((a) => `${sha(cabecalhoManifestado)}  ${a}`).join('\n') + '\n'
      : manifesto;
  // O curl falso serve o manifesto por URL e o PDF para as demais; sem manifesto, imita o 404 do --fail.
  falso(
    'curl',
    [
      'while [ $# -gt 0 ]; do [ "$1" = --output ] && saida="$2"; url="$1"; shift; done',
      'case "$url" in',
      '  */SHA256SUMS) [ -n "${FAKE_SEM_MANIFESTO:-}" ] && exit 22; printf "%s" "$FAKE_MANIFESTO" > "$saida" ;;',
      '  *) printf "%s" "$FAKE_CABECALHO" > "$saida" ;;',
      'esac',
    ].join('\n'),
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
      FAKE_MANIFESTO: texto ?? '',
      ...(texto === null ? { FAKE_SEM_MANIFESTO: '1' } : {}),
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

  it('PDF adulterado (hash diferente do manifesto): falha com a mensagem', () => {
    const r = rodarPasso({
      catalogo: comArquivos('volume1-tela.pdf'),
      cabecalho: '%PDF-1.4 adulterado',
      cabecalhoManifestado: '%PDF-1.4',
    });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toContain('::error::volume1-tela.pdf: sha256 não confere');
  });

  it('manifesto ausente na Release: falha com a mensagem do manifesto', () => {
    const r = rodarPasso({ catalogo: comArquivos('volume1-tela.pdf'), manifesto: null });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toMatch(/::error::.*SHA256SUMS/);
  });

  it('manifesto vazio: falha com a mensagem do manifesto', () => {
    const r = rodarPasso({ catalogo: comArquivos('volume1-tela.pdf'), manifesto: '' });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toMatch(/::error::.*SHA256SUMS/);
  });

  it('PDF do catálogo sem entrada no manifesto: falha com a mensagem', () => {
    const r = rodarPasso({
      catalogo: comArquivos('volume1-tela.pdf'),
      manifesto: `${sha('%PDF-1.4')}  outro.pdf\n`,
    });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toContain('::error::volume1-tela.pdf sem entrada no manifesto');
  });

  const bom = sha('%PDF-1.4');
  it.each([
    ['hash curto', `${bom.slice(0, 63)}  volume1-tela.pdf\n`],
    ['hash em maiúsculas', `${bom.toUpperCase()}  volume1-tela.pdf\n`],
    ['um espaço só entre hash e nome', `${bom} volume1-tela.pdf\n`],
    ['nome com prefixo parecido', `${bom}  xvolume1-tela.pdf\n`],
    ['nome com sufixo parecido', `${bom}  volume1-tela.pdf.bak\n`],
    ['ponto coringa no nome', `${bom}  volumeX-tela.pdf\n`],
  ])('entrada malformada (%s): tratada como sem entrada', (_nome, manifesto) => {
    const r = rodarPasso({ catalogo: comArquivos('volume1-tela.pdf'), manifesto });
    expect(r.codigo).not.toBe(0);
    expect(r.saida).toContain('::error::volume1-tela.pdf sem entrada no manifesto');
  });

  it('linhas extras no manifesto são ignoradas (só o catálogo manda)', () => {
    const r = rodarPasso({
      catalogo: comArquivos('volume1-tela.pdf'),
      manifesto: `${sha('qualquer')}  sobra.pdf\n${bom}  volume1-tela.pdf\n`,
    });
    expect(r.saida).not.toContain('::error::');
    expect(r.codigo).toBe(0);
  });
});
