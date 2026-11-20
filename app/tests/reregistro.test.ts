import { describe, expect, it } from 'vitest';
import { abrirRepositorio } from '../src/dados/repositorio';
import {
  montarRegistro,
  observacoesDaSessao,
  observacoesRegistradas,
  pareceProntoPara,
} from '../src/domain/registro';
import type { EstadosCrianca, EventoMarco, Sessao } from '../src/domain/tipos';
import { AGORA, crianca, indiceBase } from './fabricas';

// Corrigir um registro (#11): só o marco cujo estado observado MUDOU gera evento novo. Reemitir tudo
// colocaria observações velhas DEPOIS de um "Está aqui" e faria o selo voltar sozinho.
const idx = indiceBase();
const sessao = (id: string): Sessao => ({
  id,
  codigo: `S-${id}`,
  criancaId: 'c1',
  criadaEm: AGORA,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: ['atv-fon-1', 'atv-fon-2'],
  livroId: null,
});
const T1 = '2026-10-15T09:00:00.000Z';
const T2 = '2026-10-16T09:00:00.000Z';

function registrar(
  s: Sessao,
  estados: Record<string, string>,
  historico: EventoMarco[],
  extras = {},
  agora = T1,
) {
  const anteriores = observacoesRegistradas(s.id, historico);
  return montarRegistro(s, observacoesDaSessao(s, idx), { estados, ...extras }, agora, anteriores);
}

describe('reregistro só emite o que mudou', () => {
  const s = sessao('s1');
  const primeira = registrar(
    s,
    { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' },
    [],
  );

  it('o primeiro registro emite um evento por marco escolhido', () => {
    expect(primeira.eventos).toHaveLength(2);
  });

  it('salvar de novo sem mudar nenhum marco não gera evento', () => {
    const r = registrar(
      primeira.sessao,
      { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' },
      primeira.eventos,
      { anotacoes: 'só uma nota' },
      T2,
    );
    expect(r.eventos).toEqual([]);
    expect(r.sessao.anotacoes).toBe('só uma nota');
    expect(r.sessao.registradaEm).toBe(T2);
  });

  it('corrigir só duração e anotação não gera evento', () => {
    const r = registrar(
      primeira.sessao,
      { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'em-desenvolvimento' },
      primeira.eventos,
      { duracaoReal: 20 },
      T2,
    );
    expect(r.eventos).toEqual([]);
    expect(r.sessao.duracaoReal).toBe(20);
  });

  it('com mudança, gera só o evento do marco mudado', () => {
    const r = registrar(
      primeira.sessao,
      { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'consolidado' },
      primeira.eventos,
      {},
      T2,
    );
    expect(r.eventos.map((e) => [e.chave, e.registro.estado])).toEqual([
      ['LG.FON.02', 'consolidado'],
    ]);
  });

  it('marco que ainda não tinha escolha e agora tem gera evento', () => {
    const parcial = registrar(s, { 'LG.FON.01': 'consolidado' }, []);
    const r = registrar(
      parcial.sessao,
      { 'LG.FON.01': 'consolidado', 'LG.FON.02': 'consolidado' },
      parcial.eventos,
      {},
      T2,
    );
    expect(r.eventos.map((e) => e.chave)).toEqual(['LG.FON.02']);
  });
});

describe('selo depois de "Está aqui" e de reabrir uma sessão antiga', () => {
  const K = 'LG.FON.01';
  const estados: EstadosCrianca = {
    [K]: { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'posicionamento' },
  };
  const aqui: EventoMarco = {
    criancaId: 'c1',
    chave: K,
    registro: { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'posicionamento' },
  };

  it('S1 e S2 Consolidado, Está aqui, reabrir S1 e salvar só a anotação: o selo continua zerado', () => {
    const s1 = registrar(sessao('s1'), { [K]: 'consolidado' }, []);
    const s2 = registrar(sessao('s2'), { [K]: 'consolidado' }, s1.eventos);
    let h = [...s1.eventos, ...s2.eventos];
    expect(pareceProntoPara(K, estados, h)).toBe(true);
    h = [...h, aqui];
    expect(pareceProntoPara(K, estados, h)).toBe(false);
    const reaberta = registrar(s1.sessao, { [K]: 'consolidado' }, h, { anotacoes: 'depois' }, T2);
    h = [...h, ...reaberta.eventos];
    expect(reaberta.eventos).toEqual([]);
    expect(pareceProntoPara(K, estados, h)).toBe(false);
  });
});

describe('repositório com reregistro', () => {
  it('reabrir e salvar sem mudança deixa o histórico igual', async () => {
    const repo = await abrirRepositorio('reregistro-1');
    await repo.salvarCrianca(crianca());
    const s = sessao('s1');
    await repo.salvarSessao(s);
    const a = registrar(s, { 'LG.FON.01': 'consolidado' }, []);
    await repo.registrarSessao(a.sessao, a.eventos);
    const b = registrar(
      a.sessao,
      { 'LG.FON.01': 'consolidado' },
      await repo.historico('c1'),
      { anotacoes: 'x' },
      T2,
    );
    await repo.registrarSessao(b.sessao, b.eventos);
    expect(await repo.historico('c1')).toHaveLength(1);
    expect((await repo.sessao('s1'))?.anotacoes).toBe('x');
  });
});
