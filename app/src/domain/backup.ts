// Lembrete de backup (decisão 49): avisa quando passam mais de 30 dias sem backup.
import { diasEntre } from './datas';
import type { Crianca } from './tipos';

export const DIAS_LEMBRETE_BACKUP = 30;

/**
 * Só crianças de verdade pedem backup: a família de exemplo (#39) é fictícia e some com um toque.
 * Assim, uma criança cadastrada durante o exemplo já conta, sem depender de nenhuma data gravada.
 */
export function precisaLembreteBackup(
  criancas: Pick<Crianca, 'exemplo'>[],
  ultimoBackup: string | null,
  agora: string,
): boolean {
  if (!criancas.some((c) => !c.exemplo)) return false;
  return !ultimoBackup || diasEntre(ultimoBackup, agora) > DIAS_LEMBRETE_BACKUP;
}

export interface ResumoUltimaCopia {
  estado: 'nunca' | 'recente' | 'antiga';
  /** dias inteiros desde a última cópia; null quando nunca houve */
  dias: number | null;
  /** a tela de Ajustes destaca quando nunca houve cópia ou quando faz 30 dias ou mais */
  alerta: boolean;
}

/**
 * Estado da cópia de segurança para a tela de Ajustes. O alerta vale a partir de 30 dias (>=) e não
 * olha as crianças: é só informação, ao contrário do lembrete do Início (`precisaLembreteBackup`).
 * Data no futuro (o relógio do aparelho mudou) conta como hoje.
 */
export function resumoUltimaCopia(ultimoBackup: string | null, agora: string): ResumoUltimaCopia {
  if (!ultimoBackup) return { estado: 'nunca', dias: null, alerta: true };
  const futuro = new Date(ultimoBackup).getTime() > new Date(agora).getTime();
  const dias = futuro ? 0 : Math.floor(diasEntre(ultimoBackup, agora));
  const antiga = dias >= DIAS_LEMBRETE_BACKUP;
  return { estado: antiga ? 'antiga' : 'recente', dias, alerta: antiga };
}
