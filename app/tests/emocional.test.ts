import { describe, expect, it } from 'vitest';
import { carregarConteudo, carregarConteudoBruto } from '../src/conteudo';
import { validarConteudo } from '../src/domain/conteudo';
import { IDADE_MAXIMA, IDADE_MINIMA } from '../src/domain/faixa';

// Domínio "Formação e regulação emocional" (#72): vale de 2 a 8 anos e é rascunho até a dona do
// produto revisar (#77). Estes testes seguram o que não pode mudar sem ela perceber.
const LINHAS = ['EM.NOM', 'EM.REG', 'EM.CON', 'EM.VAL'];
const marcosEM = () => carregarConteudoBruto().marcos.filter((m) => m.id.startsWith('EM.'));

describe('domínio de formação e regulação emocional', () => {
  it('é um domínio com jornada e quatro linhas', () => {
    const d = carregarConteudoBruto().dominios.find((x) => x.id === 'EM');
    expect(d?.comJornada).toBe(true);
    expect(d?.linhas?.map((l) => l.id)).toEqual(LINHAS);
  });
  it('passa na validação do conteúdo (inclui o texto para os pais de cada marco)', () => {
    expect(validarConteudo(carregarConteudoBruto()).erros).toEqual([]);
  });
  it.each(LINHAS)(
    '%s tem marcos na ordem 1..N, começando aos 2 anos e sem passar dos 8',
    (linha) => {
      const marcos = marcosEM()
        .filter((m) => m.linha === linha)
        .sort((a, b) => a.ordem - b.ordem);
      expect(marcos.length).toBeGreaterThanOrEqual(4);
      expect(marcos.map((m) => m.ordem)).toEqual(marcos.map((_, i) => i + 1));
      expect(marcos[0]?.idadeTipica).toBe(IDADE_MINIMA);
      for (const [i, m] of marcos.entries()) {
        expect(m.idadeTipica).toBeLessThanOrEqual(IDADE_MAXIMA);
        if (i > 0) expect(m.idadeTipica).toBeGreaterThanOrEqual(marcos[i - 1]!.idadeTipica);
      }
    },
  );
  it('todo marco avisa que o texto é orientação, não diagnóstico', () => {
    for (const m of marcosEM())
      expect(m.orientacaoPais.sinaisDeAtencao, m.id).toMatch(/não um diagnóstico/);
  });
  it('fica escondido das famílias enquanto estiver em rascunho', () => {
    expect(marcosEM().every((m) => m.revisao?.estado === 'rascunho')).toBe(true);
    expect(carregarConteudo().marcos.some((m) => m.id.startsWith('EM.'))).toBe(false);
  });
  it('tem atividades em rascunho que cobrem as quatro linhas, sem material de risco nas de 2 anos', () => {
    const c = carregarConteudoBruto();
    const doEM = c.atividades.filter((a) => a.marcos.some((m) => m.startsWith('EM.')));
    expect(doEM.length).toBeGreaterThanOrEqual(5);
    const linhas = new Set(
      doEM.flatMap((a) => a.marcos.map((m) => m.split('.').slice(0, 2).join('.'))),
    );
    expect([...linhas].sort()).toEqual([...LINHAS].sort());
    for (const a of doEM) {
      expect(a.revisao?.estado, a.id).toBe('rascunho');
      if (a.idade[0] < 3) expect(a.cuidados, a.id).toMatch(/peça pequena|boca/);
    }
    expect(carregarConteudo().atividades.some((a) => a.id.startsWith('atv-em-'))).toBe(false);
  });
});
