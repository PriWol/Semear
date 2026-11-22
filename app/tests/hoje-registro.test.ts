import { beforeEach, describe, expect, it } from 'vitest';
import {
  contarObservados,
  dentroDoPrazoDeDesfazer,
  montarRegistro,
  observacoesDaSessao,
  observacoesRegistradas,
  PRAZO_DESFAZER_MS,
  sugerirTudoFoiBem,
  textoMarcosObservados,
} from '../src/domain/registro';
import { montarSessaoDaProposta, type PropostaSessao } from '../src/domain/sessao';
import { abrirRepositorio, type Repositorio } from '../src/dados/repositorio';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, atividade, crianca, indiceBase } from './fabricas';

// Estórias #142 (D10, D20): "Tudo foi bem" só sugere "Em desenvolvimento"; o resumo diz "observados";
// desfazer só vale logo depois de registrar. Nada disto muda o estado do marco (ADR 0030).
const idx = indiceBase();
const sessao = (extra: Partial<Sessao> = {}): Sessao => ({
  id: 's1',
  codigo: 'S-1014-A1',
  criancaId: 'c1',
  criadaEm: AGORA,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: ['atv-fon-1', 'atv-fon-2'],
  livroId: null,
  ...extra,
});
const ficha = observacoesDaSessao(sessao(), idx);

describe('sugerirTudoFoiBem (D10)', () => {
  it('sugere "em-desenvolvimento" nos marcos sem resposta, nunca "consolidado"', () => {
    const s = sugerirTudoFoiBem(ficha, {});
    expect(Object.values(s)).toEqual(ficha.map(() => 'em-desenvolvimento'));
    expect(Object.values(s)).not.toContain('consolidado');
  });

  it('não sobrescreve o que a pessoa já respondeu', () => {
    const s = sugerirTudoFoiBem(ficha, { [ficha[0]!.chave]: 'consolidado' });
    expect(Object.keys(s)).toEqual([ficha[1]!.chave]);
  });

  it('sem marcos sem resposta devolve vazio', () => {
    const tudo = Object.fromEntries(ficha.map((o) => [o.chave, 'nao-observado']));
    expect(sugerirTudoFoiBem(ficha, tudo)).toEqual({});
  });
});

describe('resumo do registro (D20)', () => {
  it('conta só os marcos da ficha com observação e fala em "observados", nunca "avançou"', () => {
    const { eventos } = montarRegistro(
      sessao(),
      ficha,
      { estados: { [ficha[0]!.chave]: 'em-desenvolvimento' } },
      AGORA,
    );
    const reg = observacoesRegistradas('s1', eventos);
    expect(contarObservados(ficha, reg)).toBe(1);
    expect(textoMarcosObservados(1)).toBe('1 marco observado');
    expect(textoMarcosObservados(3)).toBe('3 marcos observados');
    expect(textoMarcosObservados(0)).toBe('Nenhum marco observado');
    expect(textoMarcosObservados(3)).not.toMatch(/avan/i);
  });
});

describe('dentroDoPrazoDeDesfazer', () => {
  const t0 = '2026-10-15T09:00:00.000Z';
  it('vale por 10 s depois do registro', () => {
    expect(PRAZO_DESFAZER_MS).toBe(10_000);
    expect(dentroDoPrazoDeDesfazer(t0, '2026-10-15T09:00:09.000Z')).toBe(true);
    expect(dentroDoPrazoDeDesfazer(t0, '2026-10-15T09:00:10.000Z')).toBe(true);
    expect(dentroDoPrazoDeDesfazer(t0, '2026-10-15T09:00:10.001Z')).toBe(false);
  });
  it('relógio que andou para trás ou data inválida não permite desfazer', () => {
    expect(dentroDoPrazoDeDesfazer(t0, '2026-10-15T08:59:00.000Z')).toBe(false);
    expect(dentroDoPrazoDeDesfazer('lixo', t0)).toBe(false);
  });
});

describe('montarSessaoDaProposta (Preparar sessão de hoje)', () => {
  const proposta: PropostaSessao = {
    escolhas: [
      { atividade: atividade('a1', []), pista: 'LG.FON', pontos: 1, motivos: [] },
      { atividade: atividade('a2', []), pista: 'LG.FON', pontos: 1, motivos: [] },
    ],
    lacunas: [],
    livro: null,
    minutos: 40,
    avisos: [],
  };
  it('monta a sessão com código, duração real e atividades da proposta', () => {
    const s = montarSessaoDaProposta({
      id: 'x',
      crianca: crianca(),
      proposta,
      foco: 'equilibrado',
      agora: '2026-10-14T10:00:00.000Z',
      codigosExistentes: ['S-1014-C1'],
    });
    expect(s).toMatchObject({
      id: 'x',
      criancaId: 'c1',
      duracaoMin: 40,
      atividadeIds: ['a1', 'a2'],
      livroId: null,
      foco: 'equilibrado',
    });
    expect(s.codigo).toMatch(/^S-\d{4}-[A-Z]\d+$/);
    expect(s.registradaEm).toBeUndefined();
  });

  it('não repete um código já usado', () => {
    const base = {
      id: 'x',
      crianca: crianca(),
      proposta,
      foco: 'equilibrado' as const,
      agora: AGORA,
    };
    const a = montarSessaoDaProposta({ ...base, codigosExistentes: [] });
    const b = montarSessaoDaProposta({ ...base, codigosExistentes: [a.codigo] });
    expect(b.codigo).not.toBe(a.codigo);
  });
});

describe('repositório: desfazerRegistro (só o registro recém-feito)', () => {
  let repo: Repositorio;
  let n = 0;
  beforeEach(async () => {
    repo = await abrirRepositorio(`desfazer-${++n}`);
    await repo.salvarCrianca(crianca());
    await repo.salvarSessao(sessao());
  });

  const registrar = async (agora: string, estado: 'em-desenvolvimento' | 'consolidado') => {
    const anteriores = observacoesRegistradas('s1', await repo.historico('c1'));
    const atual = (await repo.sessao('s1'))!;
    const r = montarRegistro(
      atual,
      ficha,
      { estados: { [ficha[0]!.chave]: estado } },
      agora,
      anteriores,
    );
    await repo.registrarSessao(r.sessao, r.eventos);
    return { anterior: atual, registradaEm: agora };
  };

  it('devolve a sessão ao que era e remove só as observações desse registro', async () => {
    const t = '2026-10-15T09:00:00.000Z';
    const { anterior, registradaEm } = await registrar(t, 'em-desenvolvimento');
    expect((await repo.historico('c1')).length).toBe(1);
    expect(await repo.desfazerRegistro(anterior, registradaEm)).toBe(true);
    expect(await repo.sessao('s1')).toEqual(anterior);
    expect(await repo.historico('c1')).toEqual([]);
    expect(await repo.estados('c1')).toEqual({}); // nunca toca nos estados (ADR 0030)
  });

  it('ao desfazer uma correção, mantém as observações do registro anterior', async () => {
    await registrar('2026-10-15T09:00:00.000Z', 'em-desenvolvimento');
    const { anterior, registradaEm } = await registrar('2026-10-15T09:30:00.000Z', 'consolidado');
    expect((await repo.historico('c1')).length).toBe(2);
    expect(await repo.desfazerRegistro(anterior, registradaEm)).toBe(true);
    const h = await repo.historico('c1');
    expect(h.map((e) => e.registro.estado)).toEqual(['em-desenvolvimento']);
    expect((await repo.sessao('s1'))?.registradaEm).toBe('2026-10-15T09:00:00.000Z');
  });

  it('recusa se a sessão foi registrada de novo depois (outra aba): não apaga o que é mais novo', async () => {
    const { anterior } = await registrar('2026-10-15T09:00:00.000Z', 'em-desenvolvimento');
    await registrar('2026-10-15T09:00:05.000Z', 'consolidado');
    expect(await repo.desfazerRegistro(anterior, '2026-10-15T09:00:00.000Z')).toBe(false);
    expect((await repo.historico('c1')).length).toBe(2);
  });

  it('recusa sessão que não existe mais', async () => {
    const { anterior, registradaEm } = await registrar('2026-10-15T09:00:00.000Z', 'consolidado');
    await repo.removerSessao('s1');
    expect(await repo.desfazerRegistro(anterior, registradaEm)).toBe(false);
    expect(await repo.sessao('s1')).toBeNull();
  });
});
