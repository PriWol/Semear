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
