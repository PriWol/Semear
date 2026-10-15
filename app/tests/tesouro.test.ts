import { describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { enderecoDoMaterial, enderecoDoPdf, VOLUMES } from '../src/tesouro';
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

  it('os volumes 1 a 4 estão no catálogo, em ordem', () => {
    expect(VOLUMES.map((v) => v.numero)).toEqual([1, 2, 3, 4]);
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
