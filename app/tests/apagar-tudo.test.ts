import { describe, expect, it } from 'vitest';
import { openDB } from 'idb';
import { abrirRepositorio } from '../src/dados/repositorio';
import type { Sessao } from '../src/domain/tipos';
import { AGORA, crianca, familia } from './fabricas';

// #25: a política diz que "Apagar tudo" remove família, crianças, jornada e histórico, sessões, planos da
// semana e a data do último backup. Se alguém tirar uma loja de LOJAS, este teste falha e o texto deixaria
// de ser verdadeiro. Conferimos pelo banco cru, loja por loja, e não só pela API.
describe('apagarTudo e a política de privacidade (#25)', () => {
  it('deixa vazias todas as lojas, inclusive a data do último backup', async () => {
    const nome = 'teste-apagar-tudo';
    const repo = await abrirRepositorio(nome);
    await repo.salvarFamilia(familia());
    await repo.marcarBackup(AGORA);
    await repo.salvarCrianca(crianca({ id: 'c1' }));
    await repo.atualizarEstados('c1', {
      'LG.FON.01': { estado: 'em-desenvolvimento', atualizadoEm: AGORA, origem: 'manual' },
    });
    const sessao: Sessao = {
      id: 's1',
      codigo: 'S-1',
      criancaId: 'c1',
      criadaEm: AGORA,
      duracaoMin: 40,
      foco: 'equilibrado',
      atividadeIds: [],
      livroId: null,
      anotacoes: 'texto livre',
    };
    await repo.salvarSessao(sessao);
    await repo.salvarPlano({
      id: 'p1',
      criancaId: 'c1',
      inicio: '2026-10-12',
      criadoEm: AGORA,
      rotina: { dias: ['seg'], duracaoMin: 40 },
      dias: [],
    });

    const bruto = await openDB(nome);
    const lojas = [...bruto.objectStoreNames];
    expect([...lojas].sort()).toEqual([
      'config',
      'criancas',
      'estados',
      'historico',
      'planos',
      'sessoes',
    ]);
    for (const loja of lojas) expect(await bruto.count(loja), loja).toBeGreaterThan(0);

    await repo.apagarTudo();

    for (const loja of lojas) expect(await bruto.count(loja), loja).toBe(0);
    expect(await repo.familia()).toBeNull();
    expect(await repo.ultimoBackup()).toBeNull();
    bruto.close();
  });
});
