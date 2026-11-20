import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { CADERNOS, enderecoDoMaterial, enderecoDoPdf, VOLUMES } from '../src/tesouro';
import { rotuloDoMaterial } from '../src/domain/material';
import { gerarPacote } from '../src/pacote/gerar';
import { atividade, crianca, familia } from './fabricas';

describe('catálogo do Tesouro (ADR 0015)', () => {
  it('unidades em ordem, sem sobreposição e dentro do volume', () => {
    for (const v of VOLUMES) {
      let anterior = 0;
      for (const u of v.unidades) {
        expect(u.paginas[0], `U${u.numero}`).toBeGreaterThan(anterior);
        expect(u.paginas[1]).toBeGreaterThanOrEqual(u.paginas[0]);
        expect(u.paginas[1]).toBeLessThanOrEqual(v.paginas);
        anterior = u.paginas[1];
      }
    }
  });

  it('os volumes 1 a 7 estão no catálogo, em ordem', () => {
    expect(VOLUMES.map((v) => v.numero)).toEqual([1, 2, 3, 4, 5, 6, 7]);
  });

  it('o volume 5 aponta para o PDF de tela e abre cada unidade na página do sumário do livro', () => {
    const v5 = VOLUMES.find((v) => v.numero === 5)!;
    expect(v5.arquivo).toBe('tesouro/volume5-tela.pdf');
    expect(v5.paginas).toBe(67);
    expect(v5.unidades.map((u) => u.paginas[0])).toEqual([6, 13, 20, 28, 35, 43, 51, 56]);
  });

  it('o arquivo é caminho relativo ao app (nada de endereço externo)', () => {
    for (const v of VOLUMES) expect(v.arquivo).toMatch(/^tesouro\/[\w-]+\.pdf$/);
    expect(
      enderecoDoPdf(
        VOLUMES.find((v) => v.numero === 4)!,
        42,
      ),
    ).toBe('tesouro/volume4-tela.pdf#page=42');
  });

  it('o endereço do material abre na primeira página do trecho', () => {
    expect(enderecoDoMaterial({ volume: 4, unidade: 5, paginas: [42, 47] })).toBe(
      'tesouro/volume4-tela.pdf#page=42',
    );
    expect(enderecoDoMaterial({ volume: 9, unidade: 1, paginas: [1, 2] })).toBeNull();
  });

  it('todo material impresso do conteúdo aponta para uma unidade do catálogo', () => {
    const comMaterial = carregarConteudo().atividades.filter((a) => a.materialImpresso);
    expect(comMaterial.length).toBeGreaterThan(0);
    for (const a of comMaterial) {
      const m = a.materialImpresso!;
      const unidade = VOLUMES.find((v) => v.numero === m.volume)?.unidades.find(
        (u) => u.numero === m.unidade,
      );
      expect(unidade?.paginas, a.id).toEqual(m.paginas);
    }
  });

  it('atividades do Tesouro são rascunho até a revisão da dona do produto', () => {
    for (const a of carregarConteudo().atividades.filter((x) => x.materialImpresso)) {
      expect(a.autoria.status, a.id).toBe('rascunho');
    }
  });
});

// Cadernos para 2 anos (ADR 0015, adendo; ADR 0021 e 0026): não são volumes da coleção.
const TODOS = [...VOLUMES, ...CADERNOS];

describe('catálogo: volumes 6 e 7 e cadernos (estória #109)', () => {
  it('os cadernos são o de atividades e o de inglês, nesta ordem', () => {
    expect(CADERNOS.map((c) => c.id)).toEqual(['atividades-2-anos', 'ingles-2-anos']);
  });

  it('unidades sem buracos na numeração, em ordem, sem sobreposição e dentro do total', () => {
    for (const c of TODOS) {
      const nome = 'id' in c ? c.id : `volume ${c.numero}`;
      c.unidades.forEach((u, i) => expect(u.numero, `${nome} posição ${i}`).toBe(i + 1));
      let anterior = 0;
      for (const u of c.unidades) {
        expect(u.paginas[0], `${nome} U${u.numero}`).toBeGreaterThan(anterior);
        expect(u.paginas[1]).toBeGreaterThanOrEqual(u.paginas[0]);
        expect(u.paginas[1]).toBeLessThanOrEqual(c.paginas);
        anterior = u.paginas[1];
      }
    }
  });

  it('nenhum arquivo se repete e todos casam a regra do deploy (caminho relativo)', () => {
    const arquivos = TODOS.map((x) => x.arquivo);
    expect(new Set(arquivos).size).toBe(arquivos.length);
    for (const a of arquivos) {
      expect(a).toMatch(/^tesouro\/[A-Za-z0-9._-]+\.pdf$/);
      expect(a).not.toMatch(/^https?:|\.\./);
    }
  });

  it('páginas totais e primeiras páginas das unidades conferem com os sumários', () => {
    const total = (a: string) => TODOS.find((x) => x.arquivo === a)!;
    const inicios = (a: string) => total(a).unidades.map((u) => u.paginas[0]);
    expect(total('tesouro/volume6-tela.pdf').paginas).toBe(90);
    expect(total('tesouro/volume7-tela.pdf').paginas).toBe(64);
    expect(total('tesouro/caderno-tela.pdf').paginas).toBe(84);
    expect(total('tesouro/caderno-ingles-tela.pdf').paginas).toBe(90);
    expect(inicios('tesouro/volume6-tela.pdf')).toEqual([6, 14, 22, 31, 39, 48, 56, 66, 76]);
    expect(inicios('tesouro/volume7-tela.pdf')).toEqual([6, 12, 18, 24, 30, 36, 42, 48, 54]);
    expect(inicios('tesouro/caderno-tela.pdf')).toEqual([10, 20, 29, 38, 47, 56, 65, 73]);
    expect(inicios('tesouro/caderno-ingles-tela.pdf')).toEqual([8, 18, 28, 38, 48, 58, 68, 78]);
  });

  it('a unidade 9 do volume 7 é a seção de latim, com título explícito', () => {
    const u9 = VOLUMES.find((v) => v.numero === 7)!.unidades[8]!;
    expect(u9.titulo).toBe('Latim · De onde vêm as palavras');
    expect(u9.paginas).toEqual([54, 59]);
  });

  it('o caderno de atividades acompanha os volumes 1 a 8, um por unidade', () => {
    const c = CADERNOS.find((x) => x.id === 'atividades-2-anos')!;
    expect(c.unidades.map((u) => u.volume)).toEqual([1, 2, 3, 4, 5, 6, 7, 8]);
    for (const u of TODOS.flatMap((x) => x.unidades))
      if (u.volume !== undefined) {
        expect(u.volume).toBeGreaterThanOrEqual(1);
        expect(u.volume).toBeLessThanOrEqual(8);
      }
  });

  it('o endereço do caderno abre na página pedida', () => {
    const ingles = CADERNOS.find((x) => x.id === 'ingles-2-anos')!;
    expect(enderecoDoPdf(ingles, 58)).toBe('tesouro/caderno-ingles-tela.pdf#page=58');
  });

  it('os geradores e o workflow ainda produzem os nomes publicados (sem rede)', () => {
    const raiz = resolve(__dirname, '../..');
    const le = (p: string) => readFileSync(resolve(raiz, p), 'utf8');
    const workflow = le('.github/workflows/publicar-tesouro.yml');
    for (const [script, nome] of [
      ['volume6.py', 'volume6'],
      ['volume7.py', 'volume7'],
      ['caderno.py', 'caderno'],
      ['caderno_ingles.py', 'caderno-ingles'],
    ] as const) {
      const fonte = le(`tesouro-marina/editorial/${script}`);
      expect(fonte, script).toContain(`"${nome}-impressao"`);
      expect(fonte, script).toContain(`"${nome}-tela"`);
      expect(workflow, script).toContain(`python3 ${script}`);
    }
  });
});

describe('pacote com atividade complementar', () => {
  const a = atividade('comp', [], {
    dominio: 'AR',
    categoria: 'Escuta musical',
    folhas: [],
    materialImpresso: { volume: 4, unidade: 5, paginas: [42, 47] },
  });
  const doc = gerarPacote({
    sessao: {
      id: 's',
      codigo: 'S-1',
      criancaId: 'c1',
      criadaEm: '2026-01-01T10:00:00Z',
      duracaoMin: 20,
      foco: 'equilibrado',
      atividadeIds: ['comp'],
      livroId: null,
    },
    familia: familia(),
    crianca: crianca(),
    idade: 5,
    letra: 'bastao',
    atividades: [a],
    livro: null,
    marco: () => undefined,
  });

  it('mostra a categoria e o trecho do livro, sem marco', () => {
    expect(doc).toContain('Atividade complementar:');
    expect(doc).toContain('Escuta musical');
    expect(doc).toContain(rotuloDoMaterial(a.materialImpresso!));
    expect(doc).not.toContain('Marco principal');
  });
});
