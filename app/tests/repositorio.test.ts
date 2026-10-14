import { beforeEach, describe, expect, it } from 'vitest';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

// Testes de integração: o repositório real contra um IndexedDB simulado (tests/setup.ts).
let repo: Repositorio;
let n = 0;
beforeEach(async () => {
  repo = await abrirRepositorio(`teste-${++n}`); // banco novo a cada teste
});

const sessao = (id: string, criancaId: string, criadaEm: string): Sessao => ({
  id,
  codigo: `S-${id}`,
  criancaId,
  criadaEm,
  duracaoMin: 40,
  foco: 'equilibrado',
  atividadeIds: [],
  livroId: null,
});

describe('repositório (IndexedDB)', () => {
  it('guarda e lê a família', async () => {
    expect(await repo.familia()).toBeNull();
    await repo.salvarFamilia(familia());
    expect(await repo.familia()).toEqual(familia());
  });

  it('lista crianças da mais velha para a mais nova', async () => {
    await repo.salvarCrianca(crianca({ id: 'b', nascimento: '2022-01-01' }));
    await repo.salvarCrianca(crianca({ id: 'a', nascimento: '2020-01-01' }));
    expect((await repo.criancas()).map((c) => c.id)).toEqual(['a', 'b']);
  });

  it('atualiza estados mesclando e grava cada mudança no histórico', async () => {
    const r = (estado: 'consolidado' | 'em-desenvolvimento') => ({
      estado,
      atualizadoEm: AGORA,
      origem: 'manual' as const,
    });
    await repo.atualizarEstados('c1', { 'LG.FON.01': r('em-desenvolvimento') });
    await repo.atualizarEstados('c1', {
      'LG.FON.01': r('consolidado'),
      'LG.FON.02': r('em-desenvolvimento'),
    });
    const estados = await repo.estados('c1');
    expect(estados['LG.FON.01']!.estado).toBe('consolidado');
    expect(estados['LG.FON.02']!.estado).toBe('em-desenvolvimento');
    expect(await repo.historico('c1')).toHaveLength(3);
    expect(await repo.estados('outra')).toEqual({});
  });

  it('remover criança apaga estados, histórico e sessões dela, e só dela', async () => {
    await repo.salvarCrianca(crianca({ id: 'c1' }));
    await repo.salvarCrianca(crianca({ id: 'c2' }));
    await repo.atualizarEstados('c1', {
      x: { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
    });
    await repo.salvarSessao(sessao('s1', 'c1', AGORA));
    await repo.salvarSessao(sessao('s2', 'c2', AGORA));
    await repo.removerCrianca('c1');
    expect(await repo.crianca('c1')).toBeNull();
    expect(await repo.estados('c1')).toEqual({});
    expect(await repo.historico('c1')).toEqual([]);
    expect((await repo.sessoes()).map((s) => s.id)).toEqual(['s2']);
  });

  it('lista sessões da mais recente para a mais antiga, filtrando por criança', async () => {
    await repo.salvarSessao(sessao('velha', 'c1', '2026-10-01T00:00:00Z'));
    await repo.salvarSessao(sessao('nova', 'c1', '2026-10-10T00:00:00Z'));
    await repo.salvarSessao(sessao('outra', 'c2', '2026-10-05T00:00:00Z'));
    expect((await repo.sessoes('c1')).map((s) => s.id)).toEqual(['nova', 'velha']);
    expect((await repo.sessoes()).map((s) => s.id)).toEqual(['nova', 'outra', 'velha']);
  });

  it('guarda a data do último backup sem confundir com a família', async () => {
    expect(await repo.ultimoBackup()).toBeNull();
    await repo.marcarBackup(AGORA);
    expect(await repo.ultimoBackup()).toBe(AGORA);
    expect(await repo.familia()).toBeNull();
  });

  it('exportar e importar preserva todos os dados (ida e volta)', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.atualizarEstados('c1', {
      x: { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
    });
    await repo.salvarSessao(sessao('s1', 'c1', AGORA));
    const backup = await repo.exportar(AGORA);

    const outro = await abrirRepositorio(`teste-${++n}`);
    await outro.salvarCrianca(crianca({ id: 'sobra' }));
    await outro.importar(JSON.parse(JSON.stringify(backup)));
    expect(await outro.familia()).toEqual(familia());
    expect((await outro.criancas()).map((c) => c.id)).toEqual(['c1']);
    expect(await outro.estados('c1')).toEqual(await repo.estados('c1'));
    expect(await outro.historico('c1')).toHaveLength(1);
    expect((await outro.sessoes()).map((s) => s.id)).toEqual(['s1']);
  });

  it('apagarTudo deixa o banco vazio', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    await repo.apagarTudo();
    expect(await repo.familia()).toBeNull();
    expect(await repo.criancas()).toEqual([]);
  });
});

describe('importar com falha (revisão de segurança, achado 2)', () => {
  it('um item inválido no meio do backup não apaga os dados atuais', async () => {
    await repo.salvarFamilia(familia());
    await repo.salvarCrianca(crianca());
    const backup = await repo.exportar(AGORA);
    // O IndexedDB recusa a gravação no meio da transação (chave ausente), depois de já ter limpado as lojas.
    // Simula um arquivo que passou por uma validação incompleta.
    const ruim = { ...backup, estados: [{ estados: {} }] };
    await expect(repo.importar(ruim as never)).rejects.toThrow();
    expect(await repo.familia()).toEqual(familia());
    expect((await repo.criancas()).map((c) => c.id)).toEqual(['c1']);
  });
});

describe('validarBackup', () => {
  const valido = {
    app: 'semear',
    versao: 1,
    exportadoEm: AGORA,
    familia: null,
    criancas: [],
    estados: [],
    historico: [],
    sessoes: [],
  };
  it('aceita um backup válido', () => {
    expect(() => validarBackup(valido)).not.toThrow();
  });
  it('aceita um backup completo exportado pelo próprio app', async () => {
    await repo.salvarFamilia(familia({ inspiracoes: ['Waldorf'], idiomasEducador: ['en', 'fr'] }));
    await repo.salvarCrianca(crianca({ letra: 'cursiva', trilhas: ['en'] }));
    await repo.atualizarEstados('c1', {
      'LI.VOC.01@en': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'posicionamento' },
    });
    await repo.salvarSessao({
      ...sessao('s1', 'c1', AGORA),
      foco: ['LG.FON'],
      atividadeIds: ['a'],
      livroId: 'l',
    });
    const exportado: unknown = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    expect(() => validarBackup(exportado)).not.toThrow();
  });
  it.each([
    ['nulo', null],
    ['de outro app', { ...valido, app: 'outro' }],
    ['de versão futura', { ...valido, versao: 99 }],
    ['sem crianças', { ...valido, criancas: undefined }],
    ['com criança sem nome', { ...valido, criancas: [{ id: 'x' }] }],
    [
      'com letra adulterada',
      {
        ...valido,
        criancas: [{ id: 'x', nome: 'A', nascimento: '2021-01-01', letra: '"><img>', trilhas: [] }],
      },
    ],
    [
      'com nascimento inválido',
      { ...valido, criancas: [{ id: 'x', nome: 'A', nascimento: 5, letra: null, trilhas: [] }] },
    ],
    [
      'com vertente desconhecida',
      { ...valido, familia: { ...familia(), vertentePrincipal: 'constructor' } },
    ],
    ['com sessão sem id', { ...valido, sessoes: [{ ...sessao('s', 'c', AGORA), id: 1 }] }],
    [
      'com estado desconhecido',
      {
        ...valido,
        estados: [
          {
            criancaId: 'c',
            estados: { m: { estado: 'hackeado', atualizadoEm: AGORA, origem: 'manual' } },
          },
        ],
      },
    ],
  ])('recusa backup %s', (_, dado) => {
    expect(() => validarBackup(dado)).toThrow(/backup inválido/);
  });
});
