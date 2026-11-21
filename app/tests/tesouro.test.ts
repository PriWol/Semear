import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { CADERNOS, enderecoDoMaterial, enderecoDoPdf, VOLUMES } from '../src/tesouro';
import { cartaoDoCaderno, rotuloAcompanha } from '../src/pages/biblioteca';
import type { CadernoTesouro } from '../src/tesouro';
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

  it('os volumes 1 a 8 estão no catálogo, em ordem', () => {
    expect(VOLUMES.map((v) => v.numero)).toEqual([1, 2, 3, 4, 5, 6, 7, 8]);
  });

  it('o volume 8 aponta para o PDF de tela de 32 páginas e abre cada bloco na página do sumário', () => {
    const v8 = VOLUMES.find((v) => v.numero === 8)!;
    expect(v8.titulo).toBe('Jogos e descobertas');
    expect(v8.arquivo).toBe('tesouro/volume8-tela.pdf');
    expect(v8.paginas).toBe(32);
    expect(v8.unidades.map((u) => u.paginas[0])).toEqual([7, 15, 20, 25, 29]);
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

  it('o endereço do material de caderno vem do arquivo do catálogo; id desconhecido dá null (#118)', () => {
    const c = CADERNOS[0]!;
    expect(enderecoDoMaterial({ caderno: c.id, unidade: 8, paginas: [30, 35] })).toBe(
      `${c.arquivo}#page=30`,
    );
    expect(enderecoDoMaterial({ caderno: 'nao-existe', unidade: 1, paginas: [1, 2] })).toBeNull();
  });

  it('o rótulo do caderno usa título e subtítulo do catálogo, sem texto fixo por id (#118)', () => {
    const c = CADERNOS[0]!;
    const rotulo = rotuloDoMaterial({ caderno: c.id, unidade: 8, paginas: [30, 35] }, CADERNOS);
    expect(rotulo).toBe(`${c.titulo} · ${c.subtitulo}, Unidade 8 (p. 30–35)`);
    const outro = [{ id: c.id, titulo: 'Caderno novo', subtitulo: '3 anos' }];
    expect(rotuloDoMaterial({ caderno: c.id, unidade: 1, paginas: [2, 3] }, outro)).toBe(
      'Caderno novo · 3 anos, Unidade 1 (p. 2–3)',
    );
    // sem o catálogo, não inventa título
    expect(rotuloDoMaterial({ caderno: 'x', unidade: 1, paginas: [2, 3] })).toBe(
      'Caderno do Tesouro · Unidade 1 (p. 2–3)',
    );
  });

  it('todo material impresso do conteúdo aponta para uma unidade do catálogo', () => {
    const comMaterial = carregarConteudo().atividades.filter((a) => a.materialImpresso);
    expect(comMaterial.length).toBeGreaterThan(0);
    for (const a of comMaterial) {
      const m = a.materialImpresso!;
      const fonte =
        m.caderno !== undefined
          ? CADERNOS.find((c) => c.id === m.caderno)
          : VOLUMES.find((v) => v.numero === m.volume);
      const unidade = fonte?.unidades.find((u) => u.numero === m.unidade);
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

  it('só as 8 unidades do caderno de atividades têm `volume`', () => {
    for (const v of VOLUMES)
      for (const u of v.unidades) expect(u.volume, `V${v.numero}`).toBeUndefined();
    const ingles = CADERNOS.find((x) => x.id === 'ingles-2-anos')!;
    for (const u of ingles.unidades) expect(u.volume).toBeUndefined();
    const ativ = CADERNOS.find((x) => x.id === 'atividades-2-anos')!;
    expect(ativ.unidades.every((u) => Number.isInteger(u.volume))).toBe(true);
  });

  it('páginas totais são inteiros positivos e os cadernos são de 2 anos', () => {
    for (const x of TODOS) {
      expect(Number.isInteger(x.paginas) && x.paginas > 0, x.arquivo).toBe(true);
    }
    for (const c of CADERNOS) {
      expect(c.titulo.trim(), c.id).not.toBe('');
      expect(c.subtitulo, c.id).toContain('2 anos');
    }
  });

  it('o rótulo "acompanha" avisa quando o volume ainda não está no catálogo', () => {
    const existentes = VOLUMES.map((v) => v.numero);
    expect(rotuloAcompanha(7, existentes)).toBe('acompanha o Volume 7');
    expect(rotuloAcompanha(8, existentes)).toBe('acompanha o Volume 8');
    // Volume fora do catálogo continua avisando (o 9 ainda não existe).
    expect(rotuloAcompanha(9, [1, 2, 3, 4, 5, 6, 7, 8])).toBe(
      'acompanha o Volume 9 (ainda não disponível no app)',
    );
  });

  it('rótulo "acompanha": volume 0, 9 e não inteiro', () => {
    const existentes = VOLUMES.map((v) => v.numero);
    expect(rotuloAcompanha(0, existentes)).toBe('');
    expect(rotuloAcompanha(1.5, existentes)).toBe('');
    expect(rotuloAcompanha(-1, existentes)).toBe('');
    expect(rotuloAcompanha(9, existentes)).toBe(
      'acompanha o Volume 9 (ainda não disponível no app)',
    );
  });

  it('caderno sem unidades não gera lista vazia', () => {
    const saida = cartaoDoCaderno({
      id: 'vazio',
      titulo: 'Caderno vazio',
      subtitulo: '2 anos',
      aviso: 'Fale com o pediatra.',
      arquivo: 'tesouro/vazio-tela.pdf',
      paginas: 5,
      unidades: [],
    }).toString();
    expect(saida).toContain('Caderno vazio · 2 anos');
    expect(saida).toContain('Abrir o caderno');
    expect(saida).not.toContain('<ul');
    expect(saida).not.toContain('<li');
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

describe('cadernos: título e aviso vêm do próprio catálogo (estória #109)', () => {
  it('todo caderno tem título, subtítulo e um aviso de saúde que cita o pediatra', () => {
    for (const c of CADERNOS) {
      expect(c.titulo.trim(), c.id).not.toBe('');
      expect(c.subtitulo.trim(), c.id).not.toBe('');
      expect(c.aviso.trim(), c.id).not.toBe('');
      expect(c.aviso, c.id).toContain('pediatra');
    }
  });

  it('um caderno de id desconhecido aparece com o título e o aviso dele, não de outro', () => {
    const novo: CadernoTesouro = {
      id: 'matematica-3-anos',
      titulo: 'Caderno de contas',
      subtitulo: '3 anos',
      aviso: 'Aviso próprio do caderno novo, fale com o pediatra.',
      arquivo: 'tesouro/caderno-contas-tela.pdf',
      paginas: 10,
      unidades: [{ numero: 1, titulo: 'Somar', paginas: [2, 5] }],
    };
    const saida = cartaoDoCaderno(novo).toString();
    expect(saida).toContain('Caderno de contas · 3 anos');
    expect(saida).toContain('Aviso próprio do caderno novo, fale com o pediatra.');
    expect(saida).toContain('tesouro/caderno-contas-tela.pdf#page=2');
    expect(saida).not.toContain('Caderno de atividades');
    expect(saida).not.toContain('fonoaudióloga');
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

describe('pacote com material de caderno (#118)', () => {
  it('mostra o rótulo do caderno e escapa o texto vindo do catálogo', () => {
    const c = CADERNOS[0]!;
    const a = atividade('comp-caderno', [], {
      dominio: 'AR',
      categoria: 'Escuta musical',
      folhas: [],
      materialImpresso: { caderno: c.id, unidade: 8, paginas: [30, 35] },
    });
    const maliciosos = [{ id: c.id, titulo: '<img src=x onerror=alert(1)>', subtitulo: 'a&b' }];
    const gerar = (cadernos: typeof maliciosos) =>
      gerarPacote({
        sessao: {
          id: 's',
          codigo: 'S-1',
          criancaId: 'c1',
          criadaEm: '2026-01-01T10:00:00Z',
          duracaoMin: 20,
          foco: 'equilibrado',
          atividadeIds: ['comp-caderno'],
          livroId: null,
        },
        familia: familia(),
        crianca: crianca(),
        idade: 2,
        letra: 'bastao',
        atividades: [a],
        livro: null,
        marco: () => undefined,
        cadernos,
      });
    expect(gerar(CADERNOS)).toContain(`${c.titulo} · ${c.subtitulo}, Unidade 8`);
    const doc = gerar(maliciosos);
    expect(doc).not.toContain('<img src=x');
    expect(doc).toContain('&lt;img src=x onerror=alert(1)&gt;');
  });
});
