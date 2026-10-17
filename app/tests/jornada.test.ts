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
import { AGORA, crianca, familia, indiceBase, marco } from './fabricas';
import { marcoVisivel } from '../src/domain/jornada';

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
    const pos = posicaoDaLinha(idx, fon, {}, 5, familia());
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
      familia(),
    );
    expect(pos.ativos).toEqual(['LG.FON.01', 'LG.FON.02']);
  });

  it('a fronteira pula marcos consolidados, mesmo fora de ordem', () => {
    const pos = posicaoDaLinha(
      idx,
      fon,
      estados({ 'LG.FON.01': 'consolidado', 'LG.FON.03': 'consolidado' }),
      5,
      familia(),
    );
    expect(pos.fronteira).toBe('LG.FON.02');
    expect(pos.consolidados).toBe(2);
  });

  it('marco com pré-requisito pendente fica aguardando e não é ativo', () => {
    const e = estados({ 'LG.FON.01': 'consolidado', 'LG.FON.02': 'consolidado' });
    const pos = posicaoDaLinha(idx, fon, e, 5, familia());
    expect(pos.fronteira).toBe('LG.FON.03');
    expect(pos.marcos[2]!.aguardando).toEqual(['MA.SEN.01']);
    expect(pos.ativos).toEqual([]);

    const liberado = posicaoDaLinha(
      idx,
      fon,
      { ...e, ...estados({ 'MA.SEN.01': 'consolidado' }) },
      5,
      familia(),
    );
    expect(liberado.ativos).toEqual(['LG.FON.03']);
  });

  it('pré-requisito na mesma linha não bloqueia o segundo ativo (a ordem já garante a sequência)', () => {
    const e = estados({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'em-desenvolvimento',
      'MA.SEN.01': 'consolidado',
    });
    const pos = posicaoDaLinha(idx, fon, e, 5, familia());
    expect(pos.ativos).toEqual(['LG.FON.03', 'LG.FON.04']);
    expect(pos.marcos[3]!.aguardando).toEqual([]);
  });

  it('o pai pode forçar um marco aguardando marcando-o em desenvolvimento (§5.1)', () => {
    const e = estados({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'em-desenvolvimento',
    });
    const pos = posicaoDaLinha(idx, fon, e, 5, familia());
    expect(pos.marcos[2]!.aguardando).toEqual(['MA.SEN.01']);
    expect(pos.ativos[0]).toBe('LG.FON.03');
  });

  it('o marco seguinte com pré-requisito pendente não entra como segundo ativo', () => {
    const e = estados({ 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' });
    expect(posicaoDaLinha(idx, fon, e, 5, familia()).ativos).toEqual(['LG.FON.02']);
  });

  it('linha completa não tem fronteira nem ativos', () => {
    const tudo = estados({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'consolidado',
      'LG.FON.04': 'consolidado',
    });
    const pos = posicaoDaLinha(idx, fon, tudo, 5, familia());
    expect(pos.fronteira).toBeNull();
    expect(pos.ativos).toEqual([]);
  });

  it('avisa (sem bloquear) quando a vertente introduz o marco mais tarde (§5.3)', () => {
    const waldorf = posicaoDaLinha(idx, fon, {}, 5, familia({ vertentePrincipal: 'Waldorf' }));
    expect(waldorf.marcos[2]!.avisoRitmo).toBe(7);
    expect(
      posicaoDaLinha(idx, fon, {}, 7.5, familia({ vertentePrincipal: 'Waldorf' })).marcos[2]!
        .avisoRitmo,
    ).toBeNull();
    expect(posicaoDaLinha(idx, fon, {}, 5, familia()).marcos[2]!.avisoRitmo).toBeNull();
  });

  it('em Línguas, o pré-requisito é lido no mesmo idioma', () => {
    const voc = idx.linha('LI.VOC')!;
    const e = estados({ [chaveMarco('LI.VOC.01', 'en')]: 'em-desenvolvimento' });
    const pos = posicaoDaLinha(idx, { linha: voc, idioma: 'en' }, e, 5, familia());
    expect(pos.ativos).toEqual(['LI.VOC.01', 'LI.VOC.02']);
  });

  it('no domínio de Línguas o estado é separado por idioma', () => {
    const voc = idx.linha('LI.VOC')!;
    const e = estados({ [chaveMarco('LI.VOC.01', 'en')]: 'consolidado' });
    expect(posicaoDaLinha(idx, { linha: voc, idioma: 'en' }, e, 5, familia()).fronteira).toBe(
      'LI.VOC.02',
    );
    expect(posicaoDaLinha(idx, { linha: voc, idioma: 'fr' }, e, 5, familia()).fronteira).toBe(
      'LI.VOC.01',
    );
  });
});

describe('posicionar aqui', () => {
  it('consolida os anteriores e deixa o escolhido em desenvolvimento', () => {
    const mudancas = posicionarAqui(idx, fon, 'LG.FON.03', {}, AGORA, familia());
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
      {},
      AGORA,
      familia(),
    );
    expect(Object.keys(mudancas)).toEqual(['LI.VOC.01@en', 'LI.VOC.02@en']);
  });
  it('recusa marco de outra linha', () => {
    expect(() => posicionarAqui(idx, fon, 'MA.SEN.01', {}, AGORA, familia())).toThrow(
      /não pertence/,
    );
  });
  it('voltar para um marco anterior limpa os posteriores que tinham registro', () => {
    const antes = estados({
      'LG.FON.01': 'consolidado',
      'LG.FON.02': 'consolidado',
      'LG.FON.03': 'consolidado',
      'LG.FON.04': 'em-desenvolvimento',
    });
    const mudancas = posicionarAqui(idx, fon, 'LG.FON.02', antes, AGORA, familia());
    expect(mudancas['LG.FON.02']!.estado).toBe('em-desenvolvimento');
    expect(mudancas['LG.FON.03']!.estado).toBe('nao-observado');
    expect(mudancas['LG.FON.04']!.estado).toBe('nao-observado');
    const pos = posicaoDaLinha(idx, fon, { ...antes, ...mudancas }, 5, familia());
    expect(pos.fronteira).toBe('LG.FON.02');
  });
});

describe('avisos das trilhas de língua', () => {
  it('avisa quando passa do máximo de trilhas ativas', () => {
    const avisos = avisosTrilhas(
      idx,
      { trilhas: ['en', 'fr', 'la'] },
      7,
      estados({ 'LG.FON.01': 'consolidado' }),
      familia(),
    );
    expect(avisos.some((a) => a.includes('Mais de 2'))).toBe(true);
  });
  it('avisa sobre latim antes dos 6 anos e antes da leitura em andamento', () => {
    const avisos = avisosTrilhas(idx, { trilhas: ['la'] }, 5, {}, familia());
    expect(avisos).toHaveLength(2);
    expect(
      avisosTrilhas(
        idx,
        { trilhas: ['la'] },
        6,
        estados({ 'LG.FON.01': 'em-desenvolvimento' }),
        familia(),
      ),
    ).toEqual([]);
  });
});

describe('marcos extras por vertente (§2, marcos extras)', () => {
  // LG.FON.02 e LG.FON.04 são extras de Charlotte Mason; LG.FON.03 pede o extra .02 como pré-requisito.
  const cm = ['Charlotte Mason' as const];
  const idxExtra = indiceBase({
    marcos: [
      marco('LG.FON.01', 1),
      marco('LG.FON.02', 2, { vertentes: cm }),
      marco('LG.FON.03', 3, { preRequisitos: ['LG.FON.02', 'MA.SEN.02'] }),
      marco('LG.FON.04', 4, { vertentes: cm }),
      marco('MA.SEN.01', 1),
      marco('MA.SEN.02', 2, { vertentes: cm }),
    ],
  });
  const linha = { linha: idxExtra.linha('LG.FON')! };
  const cmFamilia = familia({ vertentePrincipal: 'Charlotte Mason' });
  const inspirada = familia({ inspiracoes: ['Charlotte Mason'] });
  const ids = (f: ReturnType<typeof familia>) =>
    posicaoDaLinha(idxExtra, linha, {}, 5, f).marcos.map((s) => s.marco.id);

  it('marcoVisivel: sem vertentes (null ou ausente) vale para todas', () => {
    expect(marcoVisivel(marco('LG.FON.01', 1), familia())).toBe(true);
    expect(marcoVisivel(marco('LG.FON.01', 1, { vertentes: null }), familia())).toBe(true);
    expect(marcoVisivel(marco('LG.FON.02', 2, { vertentes: cm }), familia())).toBe(false);
    expect(marcoVisivel(marco('LG.FON.02', 2, { vertentes: cm }), inspirada)).toBe(true);
  });

  it('família Montessori não vê o marco extra; Charlotte Mason (principal ou inspiração) vê', () => {
    expect(ids(familia())).toEqual(['LG.FON.01', 'LG.FON.03']);
    expect(ids(cmFamilia)).toEqual(['LG.FON.01', 'LG.FON.02', 'LG.FON.03', 'LG.FON.04']);
    expect(ids(inspirada)).toEqual(ids(cmFamilia));
  });

  it('total e consolidados contam só os marcos visíveis', () => {
    const e = estados({ 'LG.FON.01': 'consolidado' });
    const pos = posicaoDaLinha(idxExtra, linha, e, 5, familia());
    expect([pos.consolidados, pos.total]).toEqual([1, 2]);
  });

  it('marco escondido não vira fronteira nem segundo ativo', () => {
    const e = estados({ 'LG.FON.01': 'em-desenvolvimento' });
    const pos = posicaoDaLinha(idxExtra, linha, e, 5, familia());
    expect(pos.ativos).toEqual(['LG.FON.01', 'LG.FON.03']);
    const cheia = posicaoDaLinha(idxExtra, linha, e, 5, cmFamilia);
    expect(cheia.ativos).toEqual(['LG.FON.01', 'LG.FON.02']);
  });

  it('pré-requisito que aponta para marco extra invisível é ignorado', () => {
    const e = estados({ 'LG.FON.01': 'consolidado' });
    const pos = posicaoDaLinha(idxExtra, linha, e, 5, familia());
    const m3 = pos.marcos.find((s) => s.marco.id === 'LG.FON.03')!;
    expect(m3.aguardando).toEqual([]);
    expect(pos.fronteira).toBe('LG.FON.03');
    const cheia = posicaoDaLinha(idxExtra, { linha: idxExtra.linha('LG.FON')! }, e, 5, cmFamilia);
    expect(cheia.marcos.find((s) => s.marco.id === 'LG.FON.03')!.aguardando).toEqual(['MA.SEN.02']);
  });

  it('"posicionar aqui" não grava estado de marco invisível', () => {
    const m = posicionarAqui(idxExtra, linha, 'LG.FON.03', {}, AGORA, familia());
    expect(Object.keys(m)).toEqual(['LG.FON.01', 'LG.FON.03']);
    expect(() => posicionarAqui(idxExtra, linha, 'LG.FON.02', {}, AGORA, familia())).toThrow(
      /não pertence/,
    );
  });

  it('o aviso de trilha ignora pré-requisito invisível', () => {
    const idxLa = indiceBase({
      marcos: [marco('LG.FON.01', 1, { vertentes: cm }), marco('LG.FON.02', 2)],
    });
    const semAviso = (f: ReturnType<typeof familia>) =>
      avisosTrilhas(idxLa, { trilhas: ['la'] }, 6, {}, f).some((a) => a.includes('leitura'));
    expect(semAviso(familia())).toBe(false);
    expect(semAviso(cmFamilia)).toBe(true);
  });
});
