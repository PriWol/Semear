import { beforeEach, describe, expect, it } from 'vitest';
import { abrirRepositorio, type Repositorio } from '../src/dados/repositorio';
import { AGORA, crianca, familia } from './fabricas';

// SEG-4 / QA1-03: duas abas abertas não desfazem uma à outra, porque cada gravação mexe só nos campos
// que mudaram, dentro de uma única transação.
describe('gravação por campos alterados', () => {
  let nome: string;
  let abaA: Repositorio;
  let abaB: Repositorio;
  beforeEach(async () => {
    nome = `atomico-${Math.random()}`;
    abaA = await abrirRepositorio(nome);
    abaB = await abrirRepositorio(nome);
  });

  it('o aviso diário salvo pela aba B sobrevive ao salvar a família na aba A', async () => {
    await abaA.salvarFamilia(familia());
    const lidaPelaA = await abaA.familia(); // a tela da A guarda isto ao abrir
    await abaB.atualizarFamilia({ lembrete: { ativo: true, hora: '07:30', incluirNome: false } });
    expect(lidaPelaA?.lembrete).toBeUndefined();

    await abaA.atualizarFamilia({ educador: 'Priscila' });

    const final = await abaB.familia();
    expect(final?.educador).toBe('Priscila');
    expect(final?.lembrete).toEqual({ ativo: true, hora: '07:30', incluirNome: false });
  });

  it('a aba que ficou aberta não devolve o marcador de exemplo apagado pela outra', async () => {
    await abaA.salvarFamilia(familia({ exemplo: true }));
    await abaA.salvarCrianca(crianca({ id: 'real' }));
    await abaB.apagarExemplo(); // família mantida, sem marcador
    await abaA.atualizarFamilia({ educador: 'Priscila' });
    expect((await abaB.familia())?.exemplo).toBeUndefined();
  });

  it('atualizarFamilia sem família no aparelho recusa em vez de criar uma incompleta', async () => {
    await expect(abaA.atualizarFamilia({ educador: 'X' })).rejects.toThrow(/família/);
    expect(await abaA.familia()).toBeNull();
  });

  it('criança: a aba A muda o nome sem desfazer a rotina gravada pela B', async () => {
    await abaA.salvarCrianca(crianca());
    await abaB.atualizarCrianca('c1', { rotina: { dias: ['seg'], duracaoMin: 30 } });
    await abaA.atualizarCrianca('c1', { nome: 'Aninha' });
    const final = await abaB.crianca('c1');
    expect(final?.nome).toBe('Aninha');
    expect(final?.rotina).toEqual({ dias: ['seg'], duracaoMin: 30 });
  });

  it('criança removida em outra aba não é recriada pela edição que ficou aberta', async () => {
    await abaA.salvarCrianca(crianca());
    await abaB.removerCrianca('c1');
    await expect(abaA.atualizarCrianca('c1', { nome: 'Fantasma' })).rejects.toThrow(/removida/);
    expect(await abaB.criancas()).toEqual([]);
  });
});

describe('nascimento na gravação (D18)', () => {
  it('salvarCrianca e atualizarCrianca recusam o impossível; o relógio é injetável', async () => {
    const repo = await abrirRepositorio(`nasc-${Math.random()}`, () => new Date(AGORA));
    await expect(repo.salvarCrianca(crianca({ nascimento: '2099-01-01' }))).rejects.toThrow(
      /futuro/,
    );
    await expect(repo.salvarCrianca(crianca({ nascimento: '0001-01-01' }))).rejects.toThrow(
      /calendário/,
    );
    await expect(repo.salvarCrianca(crianca({ nascimento: '1999-01-01' }))).rejects.toThrow(
      /18 anos/,
    );
    expect(await repo.criancas()).toEqual([]);
    await repo.salvarCrianca(crianca({ nascimento: '2016-01-01' })); // 10 anos: só avisa
    await expect(repo.atualizarCrianca('c1', { nascimento: '2099-01-01' })).rejects.toThrow(
      /futuro/,
    );
    expect((await repo.crianca('c1'))?.nascimento).toBe('2016-01-01');
  });
});
