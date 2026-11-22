import { describe, expect, it } from 'vitest';
import { duracaoDoAviso, SEM_PRAZO } from '../src/ui/aviso';

// QA2-12: o aviso flutuante dura de 6 a 8 s, conforme o tamanho do texto; alerta fica até ser fechado.
describe('duracaoDoAviso', () => {
  it('texto curto dura 6 s', () => {
    expect(duracaoDoAviso('Aviso salvo.', 'sucesso')).toBe(6000);
  });

  it('texto longo cresce, mas nunca passa de 8 s', () => {
    const medio = duracaoDoAviso('x'.repeat(80), 'sucesso');
    expect(medio).toBeGreaterThan(6000);
    expect(medio).toBeLessThanOrEqual(8000);
    expect(duracaoDoAviso('x'.repeat(500), 'sucesso')).toBe(8000);
  });

  it('alerta não some sozinho', () => {
    expect(duracaoDoAviso('Atenção: fora da faixa.', 'alerta')).toBe(SEM_PRAZO);
  });
});
