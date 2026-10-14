import { dataLocalISO } from '../domain/datas';
import type { InfoVersao } from '../versao';

/** "0.2.0" vira "v0.2"; uma correção como "0.2.1" aparece inteira, para dar para distinguir. */
export function numeroCurto(numero: string): string {
  const [maior = '0', menor = '0', correcao = '0'] = numero.split('.');
  return correcao === '0' ? `v${maior}.${menor}` : `v${numero}`;
}

/** Rótulo discreto do topo: "v0.2 · 14/10". */
export function rotuloVersao(v: Pick<InfoVersao, 'numero' | 'data'>): string {
  const [, mes, dia] = dataLocalISO(new Date(v.data)).split('-');
  return `${numeroCurto(v.numero)} · ${dia}/${mes}`;
}
