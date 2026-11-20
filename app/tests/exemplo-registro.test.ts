import { beforeEach, describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { criarExemplo } from '../src/domain/exemplo';
import {
  montarRegistro,
  observacoesDaSessao,
  pareceProntoPara,
  sessaoRegistrada,
} from '../src/domain/registro';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import { AGORA, crianca } from './fabricas';

// Família de exemplo com registro de sessão (#11, ADR 0013): conteúdo REAL, como em tests/exemplo.test.ts.
const idx = criarIndice(carregarConteudo());
const HOJE = new Date(2026, 9, 14, 12);

describe('família de exemplo: sessões registradas e uma por registrar', () => {
  const d = criarExemplo(idx, HOJE);
  const registradas = d.sessoes.filter((s) => sessaoRegistrada(s));
  const abertas = d.sessoes.filter((s) => !sessaoRegistrada(s));

  it('traz uma sessão ainda não registrada e as demais já registradas', () => {
    expect(abertas).toHaveLength(1);
    expect(registradas.length).toBeGreaterThanOrEqual(1);
    for (const s of registradas) {
      expect(s.registradaEm! <= HOJE.toISOString()).toBe(true);
      expect(s.duracaoReal).toBeGreaterThan(0);
      expect(s.engajamento).toBeDefined();
    }
  });

  it('cada sessão registrada tem eventos "sessao" ligados a ela, e a aberta não tem nenhum', () => {
    expect(d.historico.length).toBeGreaterThan(0);
    expect(d.historico.every((e) => e.registro.origem === 'sessao' && e.sessaoId)).toBe(true);
    for (const s of registradas) {
      const chaves = d.historico.filter((e) => e.sessaoId === s.id).map((e) => e.chave);
      expect(chaves).toEqual(observacoesDaSessao(s, idx).map((o) => o.chave));
    }
    for (const s of abertas) expect(d.historico.some((e) => e.sessaoId === s.id)).toBe(false);
    for (const e of d.historico) expect(idx.marco(e.chave)).toBeDefined();
  });

  it('o registro não muda o estado de nenhum marco do exemplo (§5.2)', () => {
    for (const { estados } of d.estados) {
      expect(Object.values(estados).every((r) => r.origem === 'posicionamento')).toBe(true);
    }
  });

  it('o selo só aparece depois de uma segunda sessão: nenhum marco já o mostra, e mais uma ficha o acende', () => {
    for (const { criancaId, estados } of d.estados) {
      const h = d.historico.filter((e) => e.criancaId === criancaId);
      for (const chave of Object.keys(estados)) {
        expect(pareceProntoPara(chave, estados, h)).toBe(false);
      }
    }
    // A Ana registra uma nova sessão com o marco que já tinha uma observação Consolidado.
    const ana = d.estados.find((e) => e.criancaId === 'exemplo-ana')!;
    const primeira = registradas.find((s) => s.criancaId === 'exemplo-ana')!;
    const nova = { ...primeira, id: 'nova', codigo: 'S-NOVA' };
    delete nova.registradaEm;
    const ficha = observacoesDaSessao(nova, idx);
    const r = montarRegistro(
      nova,
      ficha,
      { estados: Object.fromEntries(ficha.map((o) => [o.chave, 'consolidado'])) },
      HOJE.toISOString(),
    );
    const h = [...d.historico.filter((e) => e.criancaId === 'exemplo-ana'), ...r.eventos];
    expect(pareceProntoPara('LG.FON.04', ana.estados, h)).toBe(true);
  });
});

describe('repositório: o registro do exemplo', () => {
  let repo: Repositorio;
  let k = 0;
  beforeEach(async () => {
    repo = await abrirRepositorio(`exemplo-registro-${++k}`);
  });

  it('carregar grava as observações depois do posicionamento, na ordem que o selo lê', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE));
    const h = await repo.historico('exemplo-ana');
    const primeiraDeSessao = h.findIndex((e) => e.registro.origem === 'sessao');
    expect(primeiraDeSessao).toBeGreaterThan(0);
    expect(h.slice(primeiraDeSessao).every((e) => e.registro.origem === 'sessao')).toBe(true);
    expect(h.slice(0, primeiraDeSessao).every((e) => e.registro.origem === 'posicionamento')).toBe(
      true,
    );
  });

  it('"Apagar exemplo" remove também as observações, mesmo as de uma sessão registrada depois', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE));
    const aberta = (await repo.sessoes('exemplo-ana')).find((s) => !sessaoRegistrada(s))!;
    const ficha = observacoesDaSessao(aberta, idx);
    const r = montarRegistro(
      aberta,
      ficha,
      { estados: Object.fromEntries(ficha.map((o) => [o.chave, 'consolidado'])) },
      HOJE.toISOString(),
    );
    await repo.registrarSessao(r.sessao, r.eventos);
    await repo.apagarExemplo();
    expect((await repo.exportar(AGORA)).historico).toEqual([]);
  });

  it('"Apagar exemplo" não toca nas observações de uma sessão real', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE));
    await repo.salvarCrianca(crianca({ id: 'real', nome: 'Lia' }));
    await repo.salvarSessao({
      id: 's-real',
      codigo: 'S-1014-L1',
      criancaId: 'real',
      criadaEm: AGORA,
      duracaoMin: 20,
      foco: 'equilibrado',
      atividadeIds: [],
      livroId: null,
      registradaEm: AGORA,
    });
    const obs = {
      criancaId: 'real',
      chave: 'LG.FON.01',
      sessaoId: 's-real',
      registro: { estado: 'consolidado' as const, atualizadoEm: AGORA, origem: 'sessao' as const },
    };
    await repo.registrarSessao((await repo.sessao('s-real'))!, [obs]);
    await repo.apagarExemplo();
    expect(await repo.historico('real')).toEqual([obs]);
    expect((await repo.exportar(AGORA)).historico).toEqual([obs]);
  });

  it('o backup do exemplo com as observações continua válido', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE));
    const arquivo: unknown = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    expect(() => validarBackup(arquivo)).not.toThrow();
  });
});
