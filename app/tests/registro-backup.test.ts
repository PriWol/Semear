import { beforeEach, describe, expect, it } from 'vitest';
import { carregarConteudo } from '../src/conteudo';
import { criarIndice } from '../src/domain/conteudo';
import { criarExemplo } from '../src/domain/exemplo';
import { abrirRepositorio, validarBackup, type Repositorio } from '../src/dados/repositorio';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca } from './fabricas';

const sessao = (id: string, extra: Partial<Sessao> = {}): Sessao => ({
  id,
  codigo: `S-${id}`,
  criancaId: 'c1',
  criadaEm: AGORA,
  duracaoMin: 30,
  foco: 'equilibrado',
  atividadeIds: [],
  livroId: null,
  ...extra,
});
const base = {
  app: 'semear',
  versao: 1,
  exportadoEm: AGORA,
  familia: null,
  criancas: [],
  estados: [],
  historico: [],
  sessoes: [sessao('s1')],
};

describe('validarBackup: sessões', () => {
  it('recusa duas sessões com o mesmo id (a segunda apagaria a primeira ao importar)', () => {
    expect(() => validarBackup({ ...base, sessoes: [sessao('s1'), sessao('s1')] })).toThrow(
      /backup inválido.*repetid/,
    );
  });

  it.each(['2026-13-45T10:00:00Z', '2026-02-31T10:00:00Z', 'ontem'])(
    'recusa registradaEm impossível (%s)',
    (d) => {
      expect(() =>
        validarBackup({ ...base, sessoes: [sessao('s1', { registradaEm: d })] }),
      ).toThrow(/backup inválido/);
    },
  );
});

describe('backup com observações do exemplo', () => {
  const idx = criarIndice(carregarConteudo());
  const HOJE = new Date(2026, 9, 14, 12);
  let repo: Repositorio;
  let n = 0;
  beforeEach(async () => {
    repo = await abrirRepositorio(`backup-exemplo-${++n}`);
  });

  it('importar e depois apagar o exemplo remove só o que é do exemplo', async () => {
    await repo.carregarExemplo(criarExemplo(idx, HOJE));
    const real = sessao('s-real', { criancaId: 'real', registradaEm: AGORA });
    const exportado = JSON.parse(JSON.stringify(await repo.exportar(AGORA)));
    exportado.criancas.push(crianca({ id: 'real', nome: 'Lia' }));
    exportado.sessoes.push(real);
    exportado.historico.push({
      criancaId: 'real',
      chave: 'LG.FON.01',
      sessaoId: 's-real',
      registro: { estado: 'consolidado', atualizadoEm: AGORA, origem: 'sessao' },
    });
    validarBackup(exportado);
    await repo.apagarTudo();
    await repo.importar(exportado);
    expect((await repo.exportar(AGORA)).historico.some((e) => e.criancaId === 'exemplo-ana')).toBe(
      true,
    );

    await repo.apagarExemplo();
    const depois = await repo.exportar(AGORA);
    expect(depois.sessoes.map((s) => s.id)).toEqual(['s-real']);
    expect(depois.historico.map((e) => e.sessaoId)).toEqual(['s-real']);
    expect(depois.criancas.map((c) => c.id)).toEqual(['real']);
  });
});
