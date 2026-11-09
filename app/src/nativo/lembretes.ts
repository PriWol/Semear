// Ponte com as notificações locais do aplicativo (Capacitor, ADR 0027). No navegador não faz nada.
import type { Lembrete } from '../domain/lembretes';

/** O pedaço do plugin LocalNotifications que usamos. */
export interface Ponte {
  checkPermissions(): Promise<{ display: string }>;
  requestPermissions(): Promise<{ display: string }>;
  getPending(): Promise<{ notifications: { id: number }[] }>;
  cancel(opcoes: { notifications: { id: number }[] }): Promise<void>;
  schedule(opcoes: {
    notifications: { id: number; title: string; body: string; schedule: { at: Date } }[];
  }): Promise<unknown>;
}

interface JanelaComCapacitor {
  Capacitor?: {
    isNativePlatform?: () => boolean;
    Plugins?: { LocalNotifications?: Ponte };
  };
}

/** A ponte só existe dentro do aplicativo instalado; no navegador devolve null. */
export function ponteDoAparelho(janela: JanelaComCapacitor): Ponte | null {
  const cap = janela.Capacitor;
  if (!cap?.isNativePlatform?.()) return null;
  return cap.Plugins?.LocalNotifications ?? null;
}

export type ResultadoSincronia = 'ok' | 'sem-permissao' | 'indisponivel';

/**
 * Cancela os lembretes agendados e agenda os novos. Só pede a permissão quando a família acabou
 * de ligar o lembrete (`pedirPermissao`); na abertura do app apenas confere.
 */
export async function sincronizarLembretes(
  ponte: Ponte | null,
  lembretes: Lembrete[],
  opcoes: { pedirPermissao: boolean },
): Promise<ResultadoSincronia> {
  if (!ponte) return 'indisponivel';
  const pendentes = (await ponte.getPending()).notifications;
  if (pendentes.length > 0)
    await ponte.cancel({ notifications: pendentes.map((n) => ({ id: n.id })) });
  if (lembretes.length === 0) return 'ok';
  let permissao = (await ponte.checkPermissions()).display;
  if (permissao !== 'granted' && opcoes.pedirPermissao) {
    permissao = (await ponte.requestPermissions()).display;
  }
  if (permissao !== 'granted') return 'sem-permissao';
  await ponte.schedule({
    notifications: lembretes.map((l) => ({
      id: l.id,
      title: l.titulo,
      body: l.texto,
      schedule: { at: l.quando },
    })),
  });
  return 'ok';
}
