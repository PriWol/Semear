import { beforeEach, describe, expect, it } from 'vitest';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import type { EventoMarco, Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

// Registro de sessão (#11) no repositório: a sessão e as observações entram juntas, sem mexer nos estados.
let repo: Repositorio;
let n = 0;
beforeEach(async () => {
  repo = await abrirRepositorio(`registro-${++n}`);
});

const sessao = (id: string, criancaId = 'c1'): Sessao => ({
  id,
  codigo: `S-${id}`,
  criancaId,
  criadaEm: AGORA,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: [],
  livroId: null,
});

const OBS = '2026-10-15T09:00:00.000Z';

const evento = (
  chave: string,
  estado: 'consolidado' | 'em-desenvolvimento',
  sessaoId: string,
  criancaId = 'c1',
): EventoMarco => ({
  criancaId,
  chave,
  sessaoId,
  registro: { estado, atualizadoEm: OBS, origem: 'sessao' },
});

const registrada = (id = 's1'): Sessao => ({
  ...sessao(id),
  registradaEm: OBS,
  duracaoReal: 35,
  engajamento: 'bom',
  anotacoes: 'Gostou.',
});

describe('registrarSessao: grava a observação sem mexer nos estados', () => {
  it('grava a sessão e os eventos juntos, e não toca nos estados', async () => {
    await repo.salvarCrianca(crianca());
    await repo.atualizarEstados('c1', {
      'LG.FON.01': { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'manual' },
    });
    await repo.salvarSessao(sessao('s1'));
    const estadosAntes = await repo.estados('c1');

    await repo.registrarSessao(registrada(), [evento('LG.FON.01', 'consolidado', 's1')]);

    expect(await repo.sessao('s1')).toEqual(registrada());
    expect(await repo.estados('c1')).toEqual(estadosAntes); // §5.2: só o pai muda o estado
    expect((await repo.estados('c1'))['LG.FON.01']?.estado).toBe('em-desenvolvimento');
    const h = await repo.historico('c1');
    expect(h).toHaveLength(2); // o evento antigo continua lá: o histórico só cresce
    expect(h[1]).toEqual(evento('LG.FON.01', 'consolidado', 's1'));
  });

  it('é atômico: se um evento não pode ser gravado, nada é gravado', async () => {
    await repo.salvarSessao(sessao('s1'));
    const estragado = {
      ...evento('LG.FON.02', 'consolidado', 's1'),
      registro: { estado: 'consolidado', atualizadoEm: () => 1, origem: 'sessao' },
    };
    await expect(
      repo.registrarSessao(registrada(), [
        evento('LG.FON.01', 'consolidado', 's1'),
        estragado as never,
      ]),
    ).rejects.toThrow();
    expect((await repo.sessao('s1'))?.registradaEm).toBeUndefined();
    expect(await repo.historico('c1')).toEqual([]);
  });

  it('recusa sessão que não existe e não grava os eventos', async () => {
    await expect(
      repo.registrarSessao(registrada('nao-existe'), [
        evento('LG.FON.01', 'consolidado', 'nao-existe'),
      ]),
    ).rejects.toThrow(/Sessão não encontrada/);
    expect(await repo.sessao('nao-existe')).toBeNull();
    expect(await repo.historico('c1')).toEqual([]);
  });

  it('recusa evento que aponta para outra sessão ou outra criança', async () => {
    await repo.salvarSessao(sessao('s1'));
    await expect(
      repo.registrarSessao(registrada(), [evento('LG.FON.01', 'consolidado', 'outra')]),
    ).rejects.toThrow(/evento/i);
    await expect(
      repo.registrarSessao(registrada(), [evento('LG.FON.01', 'consolidado', 's1', 'c2')]),
    ).rejects.toThrow(/evento/i);
    expect((await repo.sessao('s1'))?.registradaEm).toBeUndefined();
    expect(await repo.historico('c1')).toEqual([]);
  });

  it('registrar de novo troca os campos da sessão e acrescenta eventos', async () => {
    await repo.salvarSessao(sessao('s1'));
    await repo.registrarSessao(registrada(), [evento('LG.FON.01', 'em-desenvolvimento', 's1')]);
    const corrigida: Sessao = { ...sessao('s1'), registradaEm: '2026-10-16T08:00:00.000Z' };
    await repo.registrarSessao(corrigida, [evento('LG.FON.01', 'consolidado', 's1')]);
    expect(await repo.sessao('s1')).toEqual(corrigida); // duração, engajamento e anotações saíram
    expect((await repo.historico('c1')).map((e) => e.registro.estado)).toEqual([
      'em-desenvolvimento',
      'consolidado',
    ]);
  });

  it('os dados continuam lá depois de abrir o banco de novo', async () => {
    const nome = `registro-reabrir-${++n}`;
    const a = await abrirRepositorio(nome);
    await a.salvarSessao(sessao('s1'));
    await a.registrarSessao(registrada(), [evento('LG.FON.01', 'consolidado', 's1')]);
    const b = await abrirRepositorio(nome);
    expect(await b.sessao('s1')).toEqual(registrada());
    expect(await b.historico('c1')).toEqual([evento('LG.FON.01', 'consolidado', 's1')]);
  });

  it('excluir a sessão leva junto as observações dela, e só as dela', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.salvarSessao(sessao('s1'));
    await repo.salvarSessao(sessao('s2'));
    await repo.registrarSessao(registrada('s1'), [evento('LG.FON.01', 'consolidado', 's1')]);
    await repo.registrarSessao(registrada('s2'), [evento('LG.FON.01', 'consolidado', 's2')]);
    await repo.atualizarEstados('c1', {
      'LG.FON.01': { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'manual' },
    });
    await repo.removerSessao('s1');
    const h = await repo.historico('c1');
    expect(h.map((e) => [e.sessaoId, e.registro.origem])).toEqual([
      ['s2', 'sessao'],
      [undefined, 'manual'],
    ]);
    // o backup segue importável: nenhum evento fica apontando para uma sessão que não existe
    const arquivo: unknown = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    expect(() => validarBackup(arquivo)).not.toThrow();
  });
});

describe('banco e backup anteriores ao registro: sem subir a versão', () => {
  it('um banco que já tem sessão e evento antigos reabre e aceita o registro', async () => {
    const nome = `registro-antigo-${++n}`;
    const antes = await abrirRepositorio(nome);
    await antes.salvarCrianca(crianca());
    await antes.salvarSessao(sessao('s1')); // sem nenhum campo novo
    await antes.atualizarEstados('c1', {
      'LG.FON.01': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
    });
    const depois = await abrirRepositorio(nome);
    expect((await depois.sessao('s1'))?.registradaEm).toBeUndefined();
    await depois.registrarSessao({ ...sessao('s1'), registradaEm: AGORA }, [
      evento('LG.FON.02', 'consolidado', 's1'),
    ]);
    const h = await depois.historico('c1');
    expect(h).toHaveLength(2);
    expect(h[0]?.sessaoId).toBeUndefined(); // o evento antigo segue como estava
  });

  it('um backup antigo, sem os campos novos, importa e depois aceita registro', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.salvarSessao(sessao('s1'));
    const antigo: unknown = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    await repo.apagarTudo();
    validarBackup(antigo);
    await repo.importar(antigo);
    expect((await repo.sessao('s1'))?.registradaEm).toBeUndefined();
    await repo.registrarSessao({ ...sessao('s1'), registradaEm: AGORA }, []);
    expect((await repo.sessao('s1'))?.registradaEm).toBe(AGORA);
  });

  it('o registro vai e volta no backup', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.salvarSessao(sessao('s1'));
    await repo.registrarSessao({ ...registrada(), anotacoes: '<b>x</b>' }, [
      evento('LG.FON.01', 'consolidado', 's1'),
    ]);
    const arquivo: unknown = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    validarBackup(arquivo);
    await repo.apagarTudo();
    await repo.importar(arquivo);
    expect(await repo.sessao('s1')).toMatchObject({
      duracaoReal: 35,
      engajamento: 'bom',
      anotacoes: '<b>x</b>',
    });
    expect((await repo.historico('c1'))[0]?.sessaoId).toBe('s1');
  });
});

describe('validarBackup com os campos do registro', () => {
  const base = {
    app: 'semear',
    versao: 1,
    exportadoEm: AGORA,
    familia: {
      educador: 'M',
      vertentePrincipal: 'Montessori' as const,
      inspiracoes: [],
      idiomasEducador: [],
      criadaEm: '2026-10-01T10:00:00.000Z',
    },
    criancas: [{ id: 'c1', nome: 'Ana', nascimento: '2021-03-15', letra: null, trilhas: [] }],
    estados: [],
    historico: [],
    sessoes: [sessao('s1')],
  };
  const registro = (extra = {}) => ({
    estado: 'consolidado',
    atualizadoEm: AGORA,
    origem: 'sessao',
    ...extra,
  });
  const ev = (extra = {}) => ({
    criancaId: 'c1',
    chave: 'LG.FON.01',
    registro: registro(),
    sessaoId: 's1',
    ...extra,
  });
  const comSessao = (extra: object) => ({ ...base, sessoes: [{ ...sessao('s1'), ...extra }] });

  it('aceita uma sessão registrada completa e um evento ligado a ela', () => {
    expect(() =>
      validarBackup({
        ...comSessao({
          registradaEm: AGORA,
          duracaoReal: 240,
          engajamento: 'baixo',
          anotacoes: 'a'.repeat(500),
        }),
        historico: [ev()],
      }),
    ).not.toThrow();
  });

  it.each([
    ['data do registro inválida', { registradaEm: 'ontem' }],
    ['data do registro que não é texto', { registradaEm: 5 }],
    ['duração zero', { duracaoReal: 0 }],
    ['duração acima de 240', { duracaoReal: 241 }],
    ['duração fracionada', { duracaoReal: 12.5 }],
    ['duração em texto', { duracaoReal: '30' }],
    ['engajamento desconhecido', { engajamento: 'otimo' }],
    ['engajamento de protótipo', { engajamento: '__proto__' }],
    ['anotação longa demais', { anotacoes: 'a'.repeat(501) }],
    ['anotação que não é texto', { anotacoes: { x: 1 } }],
  ])('recusa sessão com %s', (_, extra) => {
    expect(() => validarBackup(comSessao(extra))).toThrow(/backup inválido/);
  });

  it.each([
    ['evento órfão (sessão inexistente)', ev({ sessaoId: 'sumiu' })],
    ['evento com sessaoId que não é texto', ev({ sessaoId: 7 })],
    ['evento de outra criança que a da sessão', ev({ criancaId: 'c2' })],
    ['evento com sessaoId e origem manual', ev({ registro: registro({ origem: 'manual' }) })],
    ['evento com estado inválido', ev({ registro: registro({ estado: 'pronto' }) })],
    ['evento com origem inválida', ev({ registro: registro({ origem: 'robo' }) })],
    ['evento com chave __proto__', ev({ chave: '__proto__' })],
    ['evento com chave constructor', ev({ chave: 'constructor' })],
    ['evento com chave prototype', ev({ chave: 'prototype' })],
  ])('recusa %s', (_, e) => {
    expect(() => validarBackup({ ...base, historico: [e] })).toThrow(/backup inválido/);
  });

  it('recusa estados com chave __proto__, constructor ou prototype', () => {
    for (const chave of ['__proto__', 'constructor', 'prototype']) {
      const estados: unknown = JSON.parse(
        `{"${chave}":{"estado":"consolidado","atualizadoEm":"${AGORA}","origem":"manual"}}`,
      );
      expect(() => validarBackup({ ...base, estados: [{ criancaId: 'c1', estados }] })).toThrow(
        /backup inválido/,
      );
    }
  });

  it('um backup inválido não apaga nada do que já está no aparelho', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.salvarSessao(sessao('s1'));
    await repo.registrarSessao(registrada(), [evento('LG.FON.01', 'consolidado', 's1')]);
    const antes = JSON.stringify(await repo.exportar(AGORA));
    await expect(
      repo.importar({ ...base, historico: [ev({ sessaoId: 'sumiu' })] } as never),
    ).rejects.toThrow(/backup inválido/);
    expect(JSON.stringify(await repo.exportar(AGORA))).toBe(antes);
  });
});
