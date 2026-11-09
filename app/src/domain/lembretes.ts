// Lembretes diários das atividades de hoje (#95, ADR 0027). Função pura: "agora" vem por parâmetro.
import type { PlanoSemana } from './semana';

/** Preferência da família. O nome da criança fica de fora por padrão: a notificação aparece na tela bloqueada. */
export interface PreferenciaLembrete {
  ativo: boolean;
  /** HH:MM, no horário do aparelho */
  hora: string;
  incluirNome: boolean;
}

export const LEMBRETE_PADRAO: PreferenciaLembrete = {
  ativo: false,
  hora: '08:00',
  incluirNome: false,
};

/** O iPhone guarda no máximo 64 notificações agendadas. */
const MAX_LEMBRETES = 64;

export interface Lembrete {
  id: number;
  quando: Date;
  titulo: string;
  texto: string;
}

export interface PlanoParaLembrar {
  plano: PlanoSemana;
  nomeDaCrianca: string;
  tituloDaAtividade: (id: string) => string | undefined;
}

export const horaValida = (h: string): boolean => /^([01]\d|2[0-3]):[0-5]\d$/.test(h);

/** Id estável (a mesma semana e dia dão o mesmo número), para cancelar e reagendar sem duplicar. */
function idDoLembrete(planoId: string, dia: string): number {
  let h = 0;
  for (const c of `${planoId}|${dia}`) h = (h * 31 + c.charCodeAt(0)) | 0;
  return Math.abs(h) % 2_000_000_000 || 1;
}

/**
 * Um lembrete por dia do plano que tem atividade, ainda não foi feito e cujo horário está no futuro.
 * Atividade que não existe mais no conteúdo é ignorada.
 */
export function planejarLembretes(
  itens: PlanoParaLembrar[],
  preferencia: PreferenciaLembrete,
  agora: string,
): Lembrete[] {
  if (!preferencia.ativo || !horaValida(preferencia.hora)) return [];
  const [hh, mm] = preferencia.hora.split(':').map(Number) as [number, number];
  const limite = new Date(agora).getTime();
  const lista: Lembrete[] = [];
  for (const { plano, nomeDaCrianca, tituloDaAtividade } of itens) {
    for (const dia of plano.dias) {
      if (dia.feito) continue;
      const titulos = dia.atividadeIds.flatMap((id) => tituloDaAtividade(id) ?? []);
      if (titulos.length === 0) continue;
      const [a, m, d] = dia.data.split('-').map(Number) as [number, number, number];
      const quando = new Date(a, m - 1, d, hh, mm);
      if (quando.getTime() <= limite) continue;
      const resumo = titulos.join(' · ');
      lista.push({
        id: idDoLembrete(plano.id, dia.dia),
        quando,
        titulo: 'Semear: atividades de hoje',
        texto: preferencia.incluirNome ? `${nomeDaCrianca}: ${resumo}` : resumo,
      });
    }
  }
  return lista.sort((x, y) => x.quando.getTime() - y.quando.getTime()).slice(0, MAX_LEMBRETES);
}
