import { describe, expect, it } from 'vitest';
import { atividadePublicada, leituraDaAtividade } from '../src/domain/leitura';
import type { Atividade } from '../src/domain/tipos';

const marcos = new Map([['LG-1', { titulo: 'Reconhece rimas' }]]);
const idx = { marco: (id: string) => marcos.get(id) as never };
const base = {
  marcos: ['LG-1', 'XX-9'],
  revisa: ['LG-1'],
  cuidados: '  Peças pequenas.  ',
  toqueVertente: { Montessori: 'Use a bandeja.', Clássico: 'Leia em voz alta.' },
  autoria: { origem: 'humano', status: 'publicado' },
} as unknown as Atividade;

describe('leitura da atividade', () => {
  it('mostra título do marco (nunca o id cru) e ignora marco desconhecido', () => {
    const l = leituraDaAtividade(base, idx, []);
    expect(l.marcos).toEqual([{ id: 'LG-1', titulo: 'Reconhece rimas' }]);
    expect(l.revisao).toEqual([{ id: 'LG-1', titulo: 'Reconhece rimas' }]);
  });
  it('apara os cuidados e devolve null quando não há', () => {
    expect(leituraDaAtividade(base, idx, []).cuidados).toBe('Peças pequenas.');
    expect(leituraDaAtividade({ ...base, cuidados: '  ' }, idx, []).cuidados).toBeNull();
  });
  it('toques só das vertentes da família, a principal primeiro', () => {
    const l = leituraDaAtividade(base, idx, ['Clássico', 'Montessori', 'Waldorf']);
    expect(l.toques.map((t) => [t.vertente, t.principal])).toEqual([
      ['Clássico', true],
      ['Montessori', false],
    ]);
  });
  it('só atividade publicada é exibida', () => {
    expect(atividadePublicada(base)).toBe(true);
    expect(atividadePublicada({ ...base, autoria: { origem: 'ia', status: 'rascunho' } })).toBe(
      false,
    );
    expect(atividadePublicada(undefined)).toBe(false);
  });
});
