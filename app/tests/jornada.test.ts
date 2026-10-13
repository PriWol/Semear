import { describe, expect, it } from 'vitest';
import {
  avisosTrilhas,
  chaveMarco,
  idPista,
  linhasVisiveis,
  pistasDaCrianca,
  posicaoDaLinha,
  posicionarAqui,
} from '../src/domain/jornada';
import type { EstadoMarco, EstadosCrianca } from '../src/domain/tipos';
import { AGORA, crianca, familia, indiceBase } from './fabricas';

const idx = indiceBase();
const fon = { linha: idx.linha('LG.FON')! };

function estados(mapa: Record<string, EstadoMarco>): EstadosCrianca {
  return Object.fromEntries(
    Object.entries(mapa).map(([k, estado]) => [
      k,
      { estado, atualizadoEm: AGORA, origem: 'manual' },
    ]),
  );
}

describe('linhas visíveis', () => {
  it('mostra linhas extras só para as vertentes da família', () => {
    const lg = idx.dominio('LG')!;
    expect(linhasVisiveis(lg, familia()).map((l) => l.id)).toEqual(['LG.FON']);
    expect(linhasVisiveis(lg, familia({ inspiracoes: ['Clássico'] })).map((l) => l.id)).toEqual([
      'LG.FON',
      'LG.MEM',
    ]);
  });
});

describe('pistas da criança', () => {
  it('ignora domínios sem jornada e cria uma pista por idioma em Línguas', () => {
    const pistas = pistasDaCrianca(idx, familia(), crianca({ trilhas: ['en', 'la'] }));
    expect(pistas.map(idPista)).toEqual(['LG.FON', 'MA.SEN', 'LI.VOC@en', 'LI.VOC@la']);
  });
  it('sem trilhas, Línguas não aparece', () => {
    expect(pistasDaCrianca(idx, familia(), crianca()).map(idPista)).toEqual(['LG.FON', 'MA.SEN']);
  });
});

describe('posição na linha (§5.1)', () => {
  it('sem registros: a fronteira é o primeiro marco e é o único ativo', () => {
    const pos = posicaoDaLinha(idx, fon, {}, 5, 'Montessori');
    expect(pos.fronteira).toBe('LG.FON.01');
    expect(pos.ativos).toEqual(['LG.FON.01']);
    expect(pos.consolidados).toBe(0);
    expect(pos.total).toBe(4);
  });

  it('fronteira em desenvolvimento libera o marco seguinte (máx. 2 ativos)', () => {
    const pos = posicaoDaLinha(
      idx,
      fon,
      estados({ 'LG.FON.01': 'em-desenvolvimento' }),
      5,
      'Montessori',
    );
    expect(pos.ativos).toEqual(['LG.FON.01', 'LG.FON.02']);
  });

  it('a fronteira pula marcos consolidados, mesmo fora de ordem', () => {
    const pos = posicaoDaLinha(
      idx,
      fon,
      estados({ 'LG.FON.01': 'consolidado', 'LG.FON.03': 'consolidado' }),
      5,
      'Montessori',
    );
    expect(pos.fronteira).toBe('LG.FON.02');
    expect(pos.consolidados).toBe(2);
  });

  it('marco com pré-requisito pendente fica aguardando e não é ativo', () => {
    const e = estados({ 'LG.FON.01': 'consolidado', 'LG.FON.02': 'consolidado' });
    const pos = posicaoDaLinha(idx, fon, e, 5, 'Montessori');
    expect(pos.fronteira).toBe('LG.FON.03');
    expect(pos.marcos[2]!.aguardando).toEqual(['MA.SEN.01']);
    expect(pos.ativos).toEqual([]);

    const liberado = posicaoDaLinha(
      idx,
      fon,
      { ...e, ...estados({ 'MA.SEN.01': 'consolidado' }) },
      5,
      'Montessori',
    );
    expect(liberado.ativos).toEqual(['LG.FON.03']);
  });

  it('o marco seguinte com pré-requisito pendente não entra como segundo ativo', () => {
    const e = estados({ 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' });
    expect(posicaoDaLinha(idx, fon, e, 5, 'Montessori').ativos).toEqual(['LG.FON.02']);
  });

  it('linha completa não tem fronteira nem ativos', () => {
    const tudo = estados({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'consolidado',
      'LG.FON.04': 'consolidado',
    });
    const pos = posicaoDaLinha(idx, fon, tudo, 5, 'Montessori');
    expect(pos.fronteira).toBeNull();
    expect(pos.ativos).toEqual([]);
  });

  it('avisa (sem bloquear) quando a vertente introduz o marco mais tarde (§5.3)', () => {
    const waldorf = posicaoDaLinha(idx, fon, {}, 5, 'Waldorf');
    expect(waldorf.marcos[2]!.avisoRitmo).toBe(7);
    expect(posicaoDaLinha(idx, fon, {}, 7.5, 'Waldorf').marcos[2]!.avisoRitmo).toBeNull();
    expect(posicaoDaLinha(idx, fon, {}, 5, 'Montessori').marcos[2]!.avisoRitmo).toBeNull();
  });

  it('no domínio de Línguas o estado é separado por idioma', () => {
    const voc = idx.linha('LI.VOC')!;
    const e = estados({ [chaveMarco('LI.VOC.01', 'en')]: 'consolidado' });
    expect(posicaoDaLinha(idx, { linha: voc, idioma: 'en' }, e, 5, 'Montessori').fronteira).toBe(
      'LI.VOC.02',
    );
    expect(posicaoDaLinha(idx, { linha: voc, idioma: 'fr' }, e, 5, 'Montessori').fronteira).toBe(
      'LI.VOC.01',
    );
  });
});

describe('posicionar aqui', () => {
  it('consolida os anteriores e deixa o escolhido em desenvolvimento', () => {
    const mudancas = posicionarAqui(idx, fon, 'LG.FON.03', AGORA);
    expect(Object.fromEntries(Object.entries(mudancas).map(([k, v]) => [k, v.estado]))).toEqual({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'em-desenvolvimento',
    });
    expect(mudancas['LG.FON.01']!.origem).toBe('posicionamento');
  });
  it('usa a chave com idioma em Línguas', () => {
    const mudancas = posicionarAqui(
      idx,
      { linha: idx.linha('LI.VOC')!, idioma: 'en' },
      'LI.VOC.02',
      AGORA,
    );
    expect(Object.keys(mudancas)).toEqual(['LI.VOC.01@en', 'LI.VOC.02@en']);
  });
  it('recusa marco de outra linha', () => {
    expect(() => posicionarAqui(idx, fon, 'MA.SEN.01', AGORA)).toThrow(/não pertence/);
  });
});

describe('avisos das trilhas de língua', () => {
  it('avisa quando passa do máximo de trilhas ativas', () => {
    const avisos = avisosTrilhas(
      idx,
      { trilhas: ['en', 'fr', 'la'] },
      7,
      estados({ 'LG.FON.01': 'consolidado' }),
    );
    expect(avisos.some((a) => a.includes('Mais de 2'))).toBe(true);
  });
  it('avisa sobre latim antes dos 6 anos e antes da leitura em andamento', () => {
    const avisos = avisosTrilhas(idx, { trilhas: ['la'] }, 5, {});
    expect(avisos).toHaveLength(2);
    expect(
      avisosTrilhas(idx, { trilhas: ['la'] }, 6, estados({ 'LG.FON.01': 'em-desenvolvimento' })),
    ).toEqual([]);
  });
});
