import { describe, expect, it } from 'vitest';
import { criarRotas, lerHash, lista } from '../src/ui/app';

describe('rotas por hash (ADR 0008)', () => {
  it('separa caminho e parâmetros de busca', () => {
    expect(lerHash('#/sessao/nova?crianca=abc&x=1')).toEqual({
      caminho: '/sessao/nova',
      query: { crianca: 'abc', x: '1' },
    });
    expect(lerHash('')).toEqual({ caminho: '/', query: {} });
  });
  it('casa rotas com parâmetros nomeados, priorizando a ordem de declaração', async () => {
    const pagina = async () => ({ titulo: '', conteudo: { valor: '' } as never });
    const rotas = criarRotas({ '/sessao/nova': pagina, '/sessao/:id': pagina });
    expect(rotas[0]!.padrao.test('/sessao/nova')).toBe(true);
    const m = rotas[1]!.padrao.exec('/sessao/123');
    expect(m?.[1]).toBe('123');
    expect(rotas[1]!.nomes).toEqual(['id']);
    expect(rotas[1]!.padrao.test('/sessao/1/2')).toBe(false);
  });
  it('lista normaliza campos de formulário', () => {
    expect(lista(undefined)).toEqual([]);
    expect(lista('a')).toEqual(['a']);
    expect(lista(['a', 'b'])).toEqual(['a', 'b']);
  });
});
