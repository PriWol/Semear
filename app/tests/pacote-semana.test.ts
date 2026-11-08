import { describe, expect, it } from 'vitest';
import { gerarSemana, nomeArquivoSemana, type ModoSemana } from '../src/pacote/semana';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { materiaisDaSemana, type PlanoSemana } from '../src/domain/semana';
import { crianca, familia } from './fabricas';

const idx = criarIndice(carregarConteudo());
const c = crianca({ id: 'c1', nome: 'Ana Lúcia' });
const plano: PlanoSemana = {
  id: 'p',
  criancaId: 'c1',
  inicio: '2026-11-09',
  criadoEm: '2026-11-09T12:00:00.000Z',
  rotina: { dias: ['seg', 'qua'], duracaoMin: 40 },
  dias: [
    {
      dia: 'seg',
      data: '2026-11-09',
      duracaoMin: 40,
      atividadeIds: ['atv-caca-silabas'],
      livroId: null,
      feito: false,
    },
    {
      dia: 'qua',
      data: '2026-11-11',
      duracaoMin: 40,
      atividadeIds: ['atv-feira-numeros'],
      livroId: null,
      feito: false,
    },
  ],
};

function doc(modo: ModoSemana) {
  const dias = plano.dias.map((dia, i) => ({
    dia,
    entrada: {
      sessao: {
        id: `s${i}`,
        codigo: `S-110${i}-A1`,
        criancaId: 'c1',
        criadaEm: dia.data,
        duracaoMin: 40,
        foco: 'equilibrado' as const,
        atividadeIds: dia.atividadeIds,
        livroId: null,
      },
      familia: familia(),
      crianca: c,
      idade: 5.6,
      letra: 'script' as const,
      atividades: dia.atividadeIds.map((id) => idx.atividade(id)!),
      livro: null,
      marco: (id: string) => idx.marco(id),
    },
  }));
  return gerarSemana({ crianca: c, plano, dias, materiais: materiaisDaSemana(idx, plano), modo });
}

const contar = (d: string, t: string) => d.split(t).length - 1;

describe('pacote da semana (#9)', () => {
  const tudo = doc('tudo');
  it('é um documento só, com a mesma CSP e CSS embutidos', () => {
    expect(tudo.startsWith('<!doctype html>')).toBe(true);
    expect(tudo).toContain('Content-Security-Policy');
    expect(contar(tudo, '<!doctype html>')).toBe(1);
  });
  it('começa pelos materiais da semana, com os dias de cada item', () => {
    expect(tudo.indexOf('Materiais da semana')).toBeLessThan(tudo.indexOf('Segunda · Sessão'));
    expect(tudo).toMatch(/feij[^<]*[\s\S]{0,200}Quarta/);
  });
  it('separa por dia, em ordem, e traz uma ficha por sessão', () => {
    expect(tudo.indexOf('Segunda · Sessão S-1100-A1')).toBeLessThan(
      tudo.indexOf('Quarta · Sessão S-1101-A1'),
    );
    expect(contar(tudo, 'Ficha de registro rápido')).toBe(2);
  });
  it('"folhas" não traz roteiros, materiais nem ficha; "roteiros" não traz folhas da criança', () => {
    const folhas = doc('folhas');
    expect(folhas).not.toContain('Roteiro do educador');
    expect(folhas).not.toContain('Materiais da semana');
    expect(folhas).not.toContain('Ficha de registro rápido');
    expect(contar(folhas, 'class="pagina crianca"')).toBeGreaterThan(0);
    const roteiros = doc('roteiros');
    expect(contar(roteiros, 'class="pagina crianca"')).toBe(0);
    expect(contar(roteiros, 'Roteiro do educador')).toBe(2);
  });
  it('o nome do arquivo tem a criança sem acento e a data da segunda', () => {
    expect(nomeArquivoSemana(plano, c)).toBe('semear-semana-ana-lucia-2026-11-09.html');
  });
});
