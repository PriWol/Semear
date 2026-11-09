import { describe, expect, it } from 'vitest';
import { estaPublicavel, validarRevisao } from '../src/domain/revisao';
import { validarConteudo } from '../src/domain/conteudo';
import { publicavel } from '../src/conteudo';
import type { Livro } from '../src/domain/tipos';
import { atividade, conteudoBase, marco } from './fabricas';

const livro = (extra: Partial<Livro> = {}): Livro => ({
  id: 'liv-1',
  titulo: 'Livro',
  autor: 'Autora',
  vertentes: ['Montessori'],
  marcos: [],
  idade: [3, 8],
  uso: 'leitura-em-voz-alta',
  porQue: 'Porque sim.',
  ...extra,
});

function erros(revisao: unknown): string[] {
  const lista: string[] = [];
  validarRevisao(revisao, 'Marco X', lista);
  return lista;
}

describe('validarRevisao (#77)', () => {
  it('aceita rascunho sem revisor e revisado/aprovado com quem e quando', () => {
    expect(erros({ estado: 'rascunho' })).toEqual([]);
    expect(erros({ estado: 'revisado', por: 'Priscila', em: '2026-11-08' })).toEqual([]);
    expect(erros({ estado: 'aprovado', por: 'Priscila', em: '2026-11-08' })).toEqual([]);
  });
  it('recusa estado fora do conjunto', () => {
    expect(erros({ estado: 'publicado', por: 'x', em: '2026-11-08' })).toHaveLength(1);
    expect(erros({})).toHaveLength(1);
    expect(erros('aprovado')).toHaveLength(1);
  });
  it('exige quem revisou e a data quando já foi revisado', () => {
    expect(erros({ estado: 'revisado' })).toHaveLength(2);
    expect(erros({ estado: 'aprovado', por: ' ', em: '2026-11-08' })).toHaveLength(1);
    expect(erros({ estado: 'aprovado', por: 'P', em: '08/11/2026' })).toHaveLength(1);
    expect(erros({ estado: 'aprovado', por: 'P', em: '2026-02-31' })).toHaveLength(1);
  });
});

describe('estaPublicavel', () => {
  it('sem revisão é conteúdo anterior à #77 e continua publicado', () => {
    expect(estaPublicavel({})).toBe(true);
  });
  it('só o aprovado é publicado', () => {
    expect(estaPublicavel({ revisao: { estado: 'aprovado', por: 'P', em: '2026-11-08' } })).toBe(
      true,
    );
    expect(estaPublicavel({ revisao: { estado: 'revisado', por: 'P', em: '2026-11-08' } })).toBe(
      false,
    );
    expect(estaPublicavel({ revisao: { estado: 'rascunho' } })).toBe(false);
  });
});

describe('validação do conteúdo com revisão', () => {
  it('recusa revisão inválida em marco, atividade e livro', () => {
    const ruim = { estado: 'ok' } as never;
    const c = conteudoBase();
    const base = c.marcos[0]!;
    const r = validarConteudo({
      ...c,
      marcos: [{ ...base, revisao: ruim }, ...c.marcos.slice(1)],
      atividades: [atividade('atv-r', [base.id], { revisao: ruim })],
      livros: [livro({ revisao: ruim })],
    });
    expect(r.erros.filter((e) => /revis/i.test(e))).toHaveLength(3);
  });
});

describe('publicavel: o app só carrega o que está aprovado', () => {
  it('tira rascunhos e revisados, mas mantém o que não tem revisão', () => {
    const c = conteudoBase();
    const rasc = { estado: 'rascunho' } as const;
    const m1 = marco('LG.FON.07', 7, { revisao: rasc });
    const filtrado = publicavel({
      ...c,
      marcos: [...c.marcos, m1],
      livros: [livro({ id: 'a' }), livro({ id: 'b', revisao: rasc })],
    });
    expect(filtrado.marcos.map((m) => m.id)).not.toContain('LG.FON.07');
    expect(filtrado.livros.map((l) => l.id)).toEqual(['a']);
  });
});
