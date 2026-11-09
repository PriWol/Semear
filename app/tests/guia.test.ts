import { describe, expect, it } from 'vitest';
import { validarGuia } from '../src/domain/guia';
import { carregarGuia, carregarConteudoBruto } from '../src/conteudo';
import { VERTENTES } from '../src/domain/tipos';

const refs = () => carregarConteudoBruto().referencias;

describe('guia das vertentes (#30)', () => {
  it('o guia real passa na validação', () => {
    expect(validarGuia(carregarGuia(), refs())).toEqual([]);
  });
  it('tem uma seção para cada vertente, na ordem do cadastro', () => {
    expect(carregarGuia().vertentes.map((v) => v.vertente)).toEqual([...VERTENTES]);
  });
  it('explica como combinar a principal com inspirações', () => {
    expect(carregarGuia().combinar.texto).toMatch(/principal/);
    expect(carregarGuia().combinar.exemplos.length).toBeGreaterThan(0);
  });
  it('recusa vertente repetida, desconhecida ou faltando', () => {
    const g = carregarGuia();
    const [primeira, ...resto] = g.vertentes;
    expect(
      validarGuia({ ...g, vertentes: [primeira!, primeira!, ...resto] }, refs()).length,
    ).toBeGreaterThan(0);
    expect(validarGuia({ ...g, vertentes: resto }, refs()).some((e) => /falta/.test(e))).toBe(true);
    expect(
      validarGuia(
        { ...g, vertentes: [{ ...primeira!, vertente: 'Outra' as never }, ...resto] },
        refs(),
      ).length,
    ).toBeGreaterThan(0);
  });
  it('recusa referência que não existe no catálogo e campo vazio', () => {
    const g = carregarGuia();
    const [primeira, ...resto] = g.vertentes;
    const ruim = { ...primeira!, referencias: ['nao-existe'], resumo: ' ' };
    const erros = validarGuia({ ...g, vertentes: [ruim, ...resto] }, refs());
    expect(erros.some((e) => /nao-existe/.test(e))).toBe(true);
    expect(erros.some((e) => /resumo/.test(e))).toBe(true);
  });
});
