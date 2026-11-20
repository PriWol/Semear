import { describe, expect, it } from 'vitest';
import type { Ponte } from '../src/nativo/lembretes';
import { apagarTudoECancelarLembretes } from '../src/nativo/sincronizar';
import type { Repositorio } from '../src/dados/repositorio';

// #25: "Apagar tudo" promete remover tudo neste aparelho. Os lembretes já agendados podem mostrar o nome
// da criança na tela bloqueada, então precisam ser cancelados também (ADR 0028).
function ponteFalsa(falhaNoCancelar = false) {
  const chamadas: string[] = [];
  const ponte: Ponte = {
    checkPermissions: async () => ({ display: 'granted' }),
    requestPermissions: async () => ({ display: 'granted' }),
    getPending: async () => ({ notifications: [{ id: 1 }, { id: 2 }] }),
    cancel: async (o) => {
      chamadas.push(`cancel:${o.notifications.map((n) => n.id).join(',')}`);
      if (falhaNoCancelar) throw new Error('plugin quebrou');
    },
    schedule: async () => {
      chamadas.push('schedule');
    },
  };
  return { ponte, chamadas };
}

function repoFalso(chamadas: string[]) {
  return {
    apagarTudo: async () => {
      chamadas.push('apagarTudo');
    },
  } as unknown as Repositorio;
}

describe('apagar tudo cancela os lembretes agendados (#25)', () => {
  it('apaga o banco e depois cancela todos os lembretes, sem agendar nenhum', async () => {
    const { ponte, chamadas } = ponteFalsa();
    expect(await apagarTudoECancelarLembretes(repoFalso(chamadas), ponte)).toBe('ok');
    expect(chamadas).toEqual(['apagarTudo', 'cancel:1,2']);
  });

  it('se a ponte falhar, o banco já foi limpo, nenhum erro sobe e o resultado avisa', async () => {
    const { ponte, chamadas } = ponteFalsa(true);
    await expect(apagarTudoECancelarLembretes(repoFalso(chamadas), ponte)).resolves.toBe(
      'lembretes-nao-cancelados',
    );
    expect(chamadas[0]).toBe('apagarTudo');
  });

  it('no navegador (sem ponte) só apaga o banco', async () => {
    const chamadas: string[] = [];
    expect(await apagarTudoECancelarLembretes(repoFalso(chamadas), null)).toBe('ok');
    expect(chamadas).toEqual(['apagarTudo']);
  });
});
