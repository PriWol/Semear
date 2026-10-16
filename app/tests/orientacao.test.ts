import { describe, expect, it } from 'vitest';
import { formatarReferencia, orientacaoParaFamilia } from '../src/domain/orientacao';
import type { OrientacaoPais, Referencia } from '../src/domain/tipos';
import { familia, indiceBase, marco } from './fabricas';

const ref = (id: string, extra: Partial<Referencia> = {}): Referencia => ({
  id,
  autores: 'AUTORA, Ana',
  titulo: `Obra ${id}`,
  ano: 2000,
  veiculo: 'São Paulo: Editora',
  ...extra,
});

const orientacao = (extra: Partial<OrientacaoPais> = {}): OrientacaoPais => ({
  porQueImporta: 'Porque sim.',
  comoParticipar: 'Brinquem juntos.',
  sinaisDeAtencao: 'Converse com a escola.',
  referencias: ['geral'],
  ...extra,
});

function indiceComOrientacao(o: OrientacaoPais | undefined, idadeIntroducao = {}) {
  return indiceBase({
    marcos: [marco('LG.FON.01', 1, { ...(o ? { orientacaoPais: o } : {}), idadeIntroducao })],
    referencias: [ref('geral'), ref('mont'), ref('wal'), ref('cm')],
  });
}

describe('formatarReferencia (ABNT)', () => {
  it('formata autores, título em itálico, local/editora e ano', () => {
    expect(formatarReferencia(ref('x'))).toBe('AUTORA, Ana. *Obra x*. São Paulo: Editora, 2000.');
  });

  it('acrescenta o link quando a fonte é de acesso livre', () => {
    expect(formatarReferencia(ref('x', { link: 'https://exemplo.gov.br' }))).toBe(
      'AUTORA, Ana. *Obra x*. São Paulo: Editora, 2000. Disponível em: https://exemplo.gov.br.',
    );
  });
});

describe('orientacaoParaFamilia', () => {
  it('devolve null quando o marco ainda não tem orientação', () => {
    const idx = indiceComOrientacao(undefined);
    expect(orientacaoParaFamilia(idx, 'LG.FON.01', familia())).toBeNull();
  });

  it('devolve null para marco inexistente', () => {
    const idx = indiceComOrientacao(orientacao());
    expect(orientacaoParaFamilia(idx, 'LG.FON.99', familia())).toBeNull();
  });

  it('sem texto da vertente, mostra só o geral e as referências gerais', () => {
    const idx = indiceComOrientacao(orientacao());
    const r = orientacaoParaFamilia(idx, 'LG.FON.01', familia({ vertentePrincipal: 'Religioso' }));
    expect(r?.geral.porQueImporta).toBe('Porque sim.');
    expect(r?.vertentes).toEqual([]);
    expect(r?.referencias.map((x) => x.id)).toEqual(['geral']);
  });

  it('mostra a vertente principal primeiro e depois as inspirações, só as que têm texto', () => {
    const idx = indiceComOrientacao(
      orientacao({
        porVertente: {
          Montessori: { comoParticipar: 'Jogos de som.', referencias: ['mont'] },
          Waldorf: { comoParticipar: 'Versos e ritmo.', referencias: ['wal'] },
          'Charlotte Mason': { comoParticipar: 'Poesia.', referencias: ['cm'] },
        },
      }),
    );
    const f = familia({
      vertentePrincipal: 'Waldorf',
      inspiracoes: ['Clássico', 'Montessori'],
    });
    const r = orientacaoParaFamilia(idx, 'LG.FON.01', f);
    expect(r?.vertentes).toEqual([
      { vertente: 'Waldorf', principal: true, comoParticipar: 'Versos e ritmo.' },
      { vertente: 'Montessori', principal: false, comoParticipar: 'Jogos de som.' },
    ]);
    // referências: geral, depois as das vertentes exibidas (Charlotte Mason não aparece)
    expect(r?.referencias.map((x) => x.id)).toEqual(['geral', 'wal', 'mont']);
  });

  it('não repete a mesma referência', () => {
    const idx = indiceComOrientacao(
      orientacao({
        porVertente: { Montessori: { comoParticipar: 'Jogos.', referencias: ['geral', 'mont'] } },
      }),
    );
    const r = orientacaoParaFamilia(idx, 'LG.FON.01', familia());
    expect(r?.referencias.map((x) => x.id)).toEqual(['geral', 'mont']);
  });

  it('troca {idade} pela idade de introdução da própria vertente, no formato brasileiro', () => {
    const idx = indiceComOrientacao(
      orientacao({
        porVertente: {
          Waldorf: { comoParticipar: 'Costuma vir por volta dos {idade} anos.', referencias: [] },
          Montessori: { comoParticipar: 'Pode ser antes, até aos {idade}.', referencias: [] },
        },
      }),
      { Waldorf: 6.5, Montessori: 4 },
    );
    const f = familia({ vertentePrincipal: 'Waldorf', inspiracoes: ['Montessori'] });
    const r = orientacaoParaFamilia(idx, 'LG.FON.01', f);
    expect(r?.vertentes.map((v) => v.comoParticipar)).toEqual([
      'Costuma vir por volta dos 6,5 anos.',
      'Pode ser antes, até aos 4.',
    ]);
  });

  it('a idade aparece mesmo quando a família tem a vertente só como inspiração', () => {
    const idx = indiceComOrientacao(
      orientacao({
        porVertente: {
          Waldorf: { comoParticipar: 'Por volta dos {idade} anos.', referencias: [] },
        },
      }),
      { Waldorf: 7 },
    );
    const f = familia({ vertentePrincipal: 'Montessori', inspiracoes: ['Waldorf'] });
    expect(orientacaoParaFamilia(idx, 'LG.FON.01', f)?.vertentes[0]?.comoParticipar).toBe(
      'Por volta dos 7 anos.',
    );
  });
});
