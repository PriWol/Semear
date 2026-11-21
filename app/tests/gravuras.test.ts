import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CREDITO_GRAVURAS, GRAVURAS, gravura } from '../src/gravuras';
import { figuraGravura } from '../src/ui/gravura';

// ADR 0035 (padrão dos ADR 0019 e 0021): gravura de domínio público com origem, SHA-256 do original e
// do WebP tratado, e falha fechada. O app só mostra imagem registrada, e o arquivo tem de bater com o registro.
const PUBLIC = new URL('../public/gravuras/', import.meta.url);
const SRC = new URL('../src/', import.meta.url);

const sha = (arquivo: string) =>
  createHash('sha256')
    .update(readFileSync(new URL(arquivo, PUBLIC)))
    .digest('hex');

describe('registro das gravuras', () => {
  it('registra as três gravuras escolhidas', () => {
    expect(Object.keys(GRAVURAS).sort()).toEqual(['girassol', 'gladiolo', 'tulipas']);
  });

  for (const g of Object.values(GRAVURAS)) {
    describe(g.id, () => {
      it('o WebP claro e o escuro batem com o SHA-256 registrado', () => {
        expect(sha(g.arquivoClaro)).toBe(g.sha256Claro);
        expect(sha(g.arquivoEscuro)).toBe(g.sha256Escuro);
      });

      it('os arquivos são WebP leves (até 60 KB)', () => {
        for (const arq of [g.arquivoClaro, g.arquivoEscuro]) {
          const bytes = readFileSync(new URL(arq, PUBLIC));
          expect(bytes.subarray(0, 4).toString('latin1')).toBe('RIFF');
          expect(bytes.subarray(8, 12).toString('latin1')).toBe('WEBP');
          expect(statSync(new URL(arq, PUBLIC)).size).toBeLessThanOrEqual(60 * 1024);
        }
      });

      it('traz autoria, obra, licença e crédito não vazios', () => {
        for (const campo of [g.titulo, g.autor, g.livro, g.licenca, g.credito, g.alt]) {
          expect(campo.trim()).not.toBe('');
        }
        expect(g.ano).toBeGreaterThan(1500);
        expect(g.licenca).toMatch(/domínio público/i);
      });

      it('a origem é o Internet Archive e o SHA-256 do original é válido', () => {
        for (const url of [g.urlOrigem, g.urlPagina]) {
          const u = new URL(url);
          expect(u.protocol).toBe('https:');
          expect(u.hostname === 'archive.org' || u.hostname.endsWith('.archive.org')).toBe(true);
          expect(url).toContain(g.item);
        }
        expect(g.urlOrigem).toBe(`https://archive.org/download/${g.item}/page/n${g.pagina}.jpg`);
        expect(g.sha256Original).toMatch(/^[0-9a-f]{64}$/);
      });
    });
  }

  it('o WebP claro e o escuro são arquivos diferentes (tinta diferente)', () => {
    for (const g of Object.values(GRAVURAS)) expect(g.sha256Claro).not.toBe(g.sha256Escuro);
  });

  it('não sobra arquivo em public/gravuras sem registro', () => {
    const registrados = new Set(
      Object.values(GRAVURAS).flatMap((g) => [g.arquivoClaro, g.arquivoEscuro]),
    );
    expect(
      readdirSync(PUBLIC)
        .filter((f) => f.endsWith('.webp'))
        .sort(),
    ).toEqual([...registrados].sort());
  });

  it('o crédito do Sobre cita as duas obras e a digitalização', () => {
    expect(CREDITO_GRAVURAS).toContain('Besler');
    expect(CREDITO_GRAVURAS).toContain('Hortus Eystettensis');
    expect(CREDITO_GRAVURAS).toContain('Redouté');
    expect(CREDITO_GRAVURAS).toContain('Les Liliacées');
    expect(CREDITO_GRAVURAS).toContain('Internet Archive');
    expect(CREDITO_GRAVURAS).toContain('domínio público');
  });
});

describe('figuraGravura (falha fechada)', () => {
  it('sem imagem registrada não mostra nada', () => {
    expect(gravura('inexistente')).toBeUndefined();
    expect(figuraGravura('inexistente').toString()).toBe('');
    expect(figuraGravura('constructor').toString()).toBe('');
  });

  it('com imagem registrada usa <picture> com a variante escura e só arquivos locais', () => {
    const marcacao = figuraGravura('girassol').toString();
    expect(marcacao).toContain('<picture');
    expect(marcacao).toContain('media="(prefers-color-scheme: dark)"');
    expect(marcacao).toContain('srcset="gravuras/girassol-escuro.webp"');
    expect(marcacao).toContain('src="gravuras/girassol.webp"');
    expect(marcacao).toContain('alt=""');
    expect(marcacao).not.toMatch(/https?:/);
  });

  it('a gravura que fica abaixo da dobra carrega sob demanda', () => {
    expect(figuraGravura('tulipas', { abaixoDaDobra: true }).toString()).toContain(
      'loading="lazy"',
    );
    expect(figuraGravura('tulipas').toString()).not.toContain('loading="lazy"');
  });
});

describe('privacidade', () => {
  it('só src/gravuras.ts menciona o archive.org; o app não faz requisição a ele', () => {
    const arquivos = (dir: URL): URL[] =>
      readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
        e.isDirectory()
          ? arquivos(new URL(`${e.name}/`, dir))
          : /\.(ts|css)$/.test(e.name)
            ? [new URL(e.name, dir)]
            : [],
      );
    const mencionam = arquivos(SRC)
      .filter((u) => /archive\.org/.test(readFileSync(u, 'utf8')))
      .map((u) => u.pathname.split('/src/')[1]);
    expect(mencionam).toEqual(['gravuras.ts']);
    const indice = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
    expect(indice).not.toMatch(/archive\.org/);
  });
});
