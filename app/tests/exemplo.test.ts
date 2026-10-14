import { beforeEach, describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { idadeInteira } from '../src/domain/datas';
import { criarExemplo } from '../src/domain/exemplo';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import { AGORA, crianca, familia, indiceBase } from './fabricas';

// Usa o conteúdo REAL: se um marco do exemplo sumir de app/content, este teste avisa.
const idx = criarIndice(carregarConteudo());
const HOJE = new Date(2026, 9, 14, 12); // 14/10/2026, horário local

describe('família de exemplo (#39)', () => {
  it('cria Ana com 5 anos e Theo com 7, a partir da data de hoje', () => {
    const { criancas } = criarExemplo(idx, HOJE);
    expect(criancas.map((c) => [c.nome, idadeInteira(c.nascimento, HOJE)])).toEqual([
      ['Ana', 5],
      ['Theo', 7],
    ]);
    // Um ano depois, as idades acompanham: o exemplo não "envelhece".
    const daquiUmAno = criarExemplo(idx, new Date(2027, 9, 14, 12));
    expect(
      daquiUmAno.criancas.map((c) => idadeInteira(c.nascimento, new Date(2027, 9, 14))),
    ).toEqual([5, 7]);
  });

  it('não cai num dia inexistente quando hoje é dia 31', () => {
    // 31/05/2026: Theo (7 anos e 3 meses) nasceria em "31/02/2019", que não existe.
    const { criancas } = criarExemplo(idx, new Date(2026, 4, 31, 12));
    expect(criancas.map((c) => c.nascimento)).toEqual(['2021-01-31', '2019-02-28']);
  });

  it('posiciona a Ana em LG.FON.04 e MA.SEN.06, com os anteriores consolidados', () => {
    const { estados } = criarExemplo(idx, HOJE);
    const ana = estados.find((e) => e.criancaId === 'exemplo-ana')?.estados ?? {};
    expect(ana['LG.FON.04']?.estado).toBe('em-desenvolvimento');
    expect(ana['LG.FON.03']?.estado).toBe('consolidado');
    expect(ana['MA.SEN.06']?.estado).toBe('em-desenvolvimento');
    expect(ana['MA.SEN.05']?.estado).toBe('consolidado');
    // Todos os marcos citados existem no conteúdo.
    for (const e of estados) {
      for (const chave of Object.keys(e.estados)) expect(idx.marco(chave)).toBeDefined();
    }
  });

  it('cria 3 sessões no passado, com atividades publicadas e códigos únicos', () => {
    const { sessoes } = criarExemplo(idx, HOJE);
    expect(sessoes).toHaveLength(3);
    expect(new Set(sessoes.map((s) => s.codigo)).size).toBe(3);
    for (const s of sessoes) {
      expect(s.criadaEm < HOJE.toISOString()).toBe(true);
      for (const id of s.atividadeIds) expect(idx.atividade(id)?.autoria.status).toBe('publicado');
    }
  });

  it('marca todos os registros como exemplo', () => {
    const d = criarExemplo(idx, HOJE);
    expect(d.familia.exemplo).toBe(true);
    expect(d.criancas.every((c) => c.exemplo)).toBe(true);
    expect(d.sessoes.every((s) => s.exemplo)).toBe(true);
  });

  it('não quebra se o conteúdo não tiver os marcos nem atividades do exemplo', () => {
    const d = criarExemplo(indiceBase({ atividades: [] }), HOJE);
    expect(d.criancas).toHaveLength(2);
    expect(d.sessoes).toEqual([]);
    expect(d.estados.find((e) => e.criancaId === 'exemplo-ana')?.estados['LG.FON.04']?.estado).toBe(
      'em-desenvolvimento',
    );
    expect(
      d.estados.find((e) => e.criancaId === 'exemplo-ana')?.estados['MA.SEN.06'],
    ).toBeUndefined();
  });
});

describe('repositório: carregar e apagar o exemplo', () => {
  let repo: Repositorio;
  let n = 0;
  beforeEach(async () => {
    repo = await abrirRepositorio(`exemplo-${++n}`);
  });

  it('carrega família, crianças, jornada (com histórico) e sessões', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE), AGORA);
    expect((await repo.familia())?.exemplo).toBe(true);
    expect((await repo.criancas()).map((c) => c.nome)).toEqual(['Theo', 'Ana']);
    expect((await repo.estados('exemplo-ana'))['LG.FON.04']?.estado).toBe('em-desenvolvimento');
    expect((await repo.historico('exemplo-ana')).length).toBeGreaterThan(0);
    expect(await repo.sessoes()).toHaveLength(3);
    // O exemplo não dispara o lembrete de backup.
    expect(await repo.ultimoBackup()).toBe(AGORA);
  });

  it('recusa carregar o exemplo quando já existe uma família', async () => {
    await repo.salvarFamilia(familia());
    await expect(repo.carregarExemplo(criarExemplo(idx, HOJE), AGORA)).rejects.toThrow(
      /Já existe uma família/,
    );
    expect(await repo.familia()).toEqual(familia());
    expect(await repo.criancas()).toEqual([]);
  });

  it('apagar o exemplo não deixa resto', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE), AGORA);
    await repo.apagarExemplo();
    const backup = await repo.exportar(AGORA);
    expect(backup.familia).toBeNull();
    expect(backup.criancas).toEqual([]);
    expect(backup.estados).toEqual([]);
    expect(backup.historico).toEqual([]);
    expect(backup.sessoes).toEqual([]);
    expect(await repo.ultimoBackup()).toBeNull();
  });

  it('uma criança real cadastrada durante o exemplo sobrevive ao "Apagar exemplo"', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE), AGORA);
    const real = crianca({ id: 'real', nome: 'Lia' });
    await repo.salvarCrianca(real);
    await repo.atualizarEstados('real', {
      'LG.FON.01': { estado: 'consolidado', atualizadoEm: AGORA, origem: 'manual' },
    });
    await repo.salvarSessao({
      id: 's-real',
      codigo: 'S-1014-L1',
      criancaId: 'real',
      criadaEm: AGORA,
      duracaoMin: 20,
      foco: 'equilibrado',
      atividadeIds: [],
      livroId: null,
    });

    await repo.apagarExemplo();

    expect(await repo.criancas()).toEqual([real]);
    expect(Object.keys(await repo.estados('real'))).toEqual(['LG.FON.01']);
    expect((await repo.sessoes()).map((s) => s.id)).toEqual(['s-real']);
    expect(await repo.sessoes('exemplo-ana')).toEqual([]);
  });

  it('não apaga uma família real', async () => {
    await repo.salvarFamilia(familia());
    await repo.apagarExemplo();
    expect(await repo.familia()).toEqual(familia());
  });

  it('o backup de um exemplo continua válido e marcado como exemplo', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE), AGORA);
    const backup = JSON.parse(JSON.stringify(await repo.exportar(AGORA))) as unknown;
    expect(() => validarBackup(backup)).not.toThrow();
    expect((backup as { familia: { exemplo?: boolean } }).familia.exemplo).toBe(true);
  });

  it('recusa um backup com o marcador de exemplo adulterado', async () => {
    const backup = {
      ...(await repo.exportar(AGORA)),
      criancas: [{ ...crianca(), exemplo: 'sim' }],
    };
    expect(() => validarBackup(backup)).toThrow(/marcador de exemplo/);
  });
});
