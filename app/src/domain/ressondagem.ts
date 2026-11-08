// Ressondagem das linhas paradas (§5.5, #18). Funções puras: a data de "agora" vem por parâmetro.
import type { IndiceConteudo } from './conteudo';
import { diasEntre } from './datas';
import { chaveMarco, marcosDaPista, type Pista } from './jornada';
import { marcosSondaveis, type Sondagem } from './sondagem';
import type { EstadosCrianca } from './tipos';

/** Tempo sem mudança a partir do qual a linha pede uma ressondagem (decisão 13). */
export const SEMANAS_SEM_MUDAR = 8;
const DIAS_LIMITE = SEMANAS_SEM_MUDAR * 7;

export type MotivoRessondagem = 'parada' | 'sem-observacao';

export interface LinhaParaRessondar {
  pista: Pista;
  motivo: MotivoRessondagem;
}

/**
 * Linhas que pedem uma mini-sondagem, entre as que têm item de sondagem:
 * - **parada**: tem marco em desenvolvimento e nada mudou na linha há 8 semanas ou mais;
 * - **sem observação**: nenhum registro na linha e a família existe há 8 semanas ou mais.
 * Linha toda consolidada não entra.
 */
export function linhasParaRessondar(
  idx: IndiceConteudo,
  pistas: Pista[],
  sondagem: Sondagem,
  estados: EstadosCrianca,
  familiaCriadaEm: string,
  agora: string,
): LinhaParaRessondar[] {
  const resultado: LinhaParaRessondar[] = [];
  for (const pista of pistas) {
    if (marcosSondaveis(idx, pista, sondagem).length === 0) continue;
    const marcos = marcosDaPista(idx, pista);
    const registros = marcos.flatMap((m) => {
      const r = estados[chaveMarco(m.id, pista.idioma)];
      return r ? [r] : [];
    });
    if (registros.length === 0) {
      if (diasEntre(familiaCriadaEm, agora) >= DIAS_LIMITE)
        resultado.push({ pista, motivo: 'sem-observacao' });
      continue;
    }
    const emAndamento = registros.some((r) => r.estado === 'em-desenvolvimento');
    const maisRecente = registros.reduce((a, r) => (r.atualizadoEm > a ? r.atualizadoEm : a), '');
    if (emAndamento && diasEntre(maisRecente, agora) >= DIAS_LIMITE)
      resultado.push({ pista, motivo: 'parada' });
  }
  return resultado;
}
