import { describe, expect, it } from 'vitest';
import {
  alvoDaSondagem,
  analisarLinha,
  etapaDeAjuste,
  itensBase,
  mudancasDaSondagem,
  validarSondagem,
} from '../src/domain/sondagem';
import { carregarConteudoBruto, carregarSondagem } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import type { EstadoMarco } from '../src/domain/tipos';
import { marco } from './fabricas';

// Linha com 7 marcos de 3 a 6 anos (idade típica sobe de meio em meio ano).
const marcos = Array.from({ length: 7 }, (_, i) =>
  marco(`LG.FON.0${i + 1}`, i + 1, { idadeTipica: 3 + i / 2 }),
);
const r = (...pares: [number, EstadoMarco][]) =>
  Object.fromEntries(pares.map(([i, e]) => [marcos[i]!.id, e]));
const C = 'consolidado';
const D = 'em-desenvolvimento';
const N = 'nao-observado';

describe('sondagem adaptativa (§5.4, #17)', () => {
  it('a etapa base cobre o marco de idade típica mais próxima e os vizinhos', () => {
    expect(itensBase(marcos, 4.6)).toEqual(['LG.FON.03', 'LG.FON.04', 'LG.FON.05']);
  });
  it('em empate de idade, começa pelo marco mais baixo', () => {
    // 3.25 está entre 3 e 3.5: fica com o mais baixo (índice 0), e os vizinhos cortam o que não existe
    expect(itensBase(marcos, 3.25)).toEqual(['LG.FON.01', 'LG.FON.02']);
  });
  it('sobe quando está consolidado e para quando acha o primeiro não consolidado', () => {
    const a = analisarLinha(marcos, r([3, C], [4, D]));
    expect(a.definida).toBe(true);
    expect(a.alvo).toBe('LG.FON.05');
  });
  it('sobe mais um quando o último testado está consolidado', () => {
    const a = analisarLinha(marcos, r([2, C], [3, C], [4, C]));
    expect(a).toMatchObject({ definida: false, proximo: 'LG.FON.06' });
  });
  it('desce quando o primeiro testado não foi observado', () => {
    const a = analisarLinha(marcos, r([4, N], [5, N]));
    expect(a).toMatchObject({ definida: false, proximo: 'LG.FON.04' });
  });
  it('se nada está consolidado e o primeiro marco falhou, posiciona no primeiro', () => {
    const a = analisarLinha(marcos, r([0, N]));
    expect(a).toMatchObject({ definida: true, alvo: 'LG.FON.01' });
  });
  it('tudo consolidado até o topo posiciona no último marco', () => {
    const a = analisarLinha(marcos, r([5, C], [6, C]));
    expect(a).toMatchObject({ definida: true, alvo: 'LG.FON.07' });
  });
  it('resultado incoerente (consolidado acima de um não observado) vale o mais alto consolidado', () => {
    const a = analisarLinha(marcos, r([1, N], [3, C], [4, N]));
    expect(a).toMatchObject({ definida: true, alvo: 'LG.FON.05' });
  });
  it('a etapa de ajuste só traz um item novo para a linha indefinida, até 5 itens', () => {
    expect(etapaDeAjuste(marcos, r([2, C], [3, C], [4, C]))).toEqual(['LG.FON.06']);
    expect(etapaDeAjuste(marcos, r([3, C], [4, D]))).toEqual([]);
    // 5 itens já testados e ainda indefinida: para e fica com o melhor palpite
    const cinco = r([0, C], [1, C], [2, C], [3, C], [4, C]);
    expect(etapaDeAjuste(marcos, cinco)).toEqual([]);
    expect(alvoDaSondagem(marcos, cinco)).toBe('LG.FON.06');
  });
});

describe('gravação da sondagem', () => {
  it('grava os estados com origem "sondagem"', () => {
    const idx = criarIndice(carregarConteudoBruto());
    const pista = {
      linha: { id: 'LG.FON', nome: 'x', vertentes: null },
      dominio: idx.conteudo.dominios[0]!,
    };
    const m = mudancasDaSondagem(idx, pista, 'LG.FON.03', {}, '2026-11-08T10:00:00.000Z');
    expect(Object.values(m).every((x) => x.origem === 'sondagem')).toBe(true);
    expect(m['LG.FON.02']?.estado).toBe('consolidado');
    expect(m['LG.FON.03']?.estado).toBe('em-desenvolvimento');
  });
});

describe('itens de sondagem (conteúdo)', () => {
  it('passam na validação e cobrem LG.FON e MA.SEN', () => {
    const c = carregarConteudoBruto();
    const s = carregarSondagem();
    expect(validarSondagem(s, c.marcos)).toEqual([]);
    for (const linha of ['LG.FON', 'MA.SEN']) {
      const doMarcos = c.marcos.filter((m) => m.linha === linha);
      const cobertos = s.itens.filter((i) => i.marco.startsWith(linha));
      expect(cobertos.length, linha).toBe(doMarcos.length);
    }
  });
  it('recusa item de marco que não existe, texto vazio e id repetido', () => {
    const c = carregarConteudoBruto();
    const [a] = carregarSondagem().itens;
    const erros = validarSondagem(
      {
        itens: [
          { ...a!, marco: 'XX.YYY.99' },
          { ...a!, instrucao: ' ' },
        ],
      },
      c.marcos,
    );
    expect(erros.some((e) => /não existe/.test(e))).toBe(true);
    expect(erros.some((e) => /instrucao/.test(e))).toBe(true);
    expect(erros.some((e) => /repetido/.test(e))).toBe(true);
  });
});
