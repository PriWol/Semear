// Sondagem adaptativa por linha (§5.4, #17). Funções puras: recebem os marcos já ordenados e os
// resultados lançados pelo educador. Só marcos que têm item de sondagem entram na conta.
import type { IndiceConteudo } from './conteudo';
import { marcosDaPista, posicionarAqui, type Pista } from './jornada';
import type { EstadoMarco, EstadosCrianca, Marco, RegistroMarco, Revisao } from './tipos';
import { validarRevisao } from './revisao';

export interface ItemSondagem {
  id: string;
  marco: string;
  /** o que o educador faz e diz */
  instrucao: string;
  /** como é a resposta de quem já domina o marco */
  consolidado: string;
  /** como é a resposta de quem está aprendendo */
  emDesenvolvimento: string;
  revisao?: Revisao;
}

export interface Sondagem {
  itens: ItemSondagem[];
}

/** Resultado por id do marco; marco sem entrada ainda não foi testado. */
export type Resultados = Record<string, EstadoMarco>;

/** Máximo de itens por linha (3 a 5 na estória): a etapa base traz 3, o ajuste completa até 5. */
export const MAX_ITENS_POR_LINHA = 5;

export interface AnaliseLinha {
  /** achamos o primeiro marco ainda não consolidado (ou os limites da linha) */
  definida: boolean;
  /** marco onde a criança "está" (em desenvolvimento); null enquanto nada foi testado */
  alvo: string | null;
  /** próximo marco a testar, se a linha ainda não foi definida */
  proximo: string | null;
}

/** Marcos da pista que têm item de sondagem, na ordem da linha. */
export function marcosSondaveis(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  sondagem: Sondagem,
): Marco[] {
  const comItem = new Set(sondagem.itens.map((i) => i.marco));
  return marcosDaPista(idx, pista).filter((m) => comItem.has(m.id));
}

/** Índice do marco cuja idade típica é a mais próxima; em empate, o mais baixo. */
function indiceInicial(marcos: Marco[], idade: number): number {
  let melhor = 0;
  marcos.forEach((m, i) => {
    if (Math.abs(m.idadeTipica - idade) < Math.abs(marcos[melhor]!.idadeTipica - idade)) melhor = i;
  });
  return melhor;
}

/**
 * Etapa base: o marco mais próximo da idade da criança e seus vizinhos. Os três são impressos de
 * uma vez, porque a folha sai antes de haver resultado (a adaptação acontece na etapa de ajuste).
 */
export function itensBase(marcos: Marco[], idade: number): string[] {
  if (marcos.length === 0) return [];
  const i = indiceInicial(marcos, idade);
  return marcos.slice(Math.max(0, i - 1), i + 2).map((m) => m.id);
}

export function analisarLinha(marcos: Marco[], resultados: Resultados): AnaliseLinha {
  const n = marcos.length;
  const testado = (i: number) => resultados[marcos[i]!.id] !== undefined;
  let alto = -1; // maior índice consolidado (resultado incoerente abaixo dele é ignorado)
  let baixo = -1; // menor índice testado
  marcos.forEach((m, i) => {
    if (resultados[m.id] === undefined) return;
    if (baixo < 0) baixo = i;
    if (resultados[m.id] === 'consolidado') alto = i;
  });
  if (n === 0 || baixo < 0) return { definida: false, alvo: null, proximo: null };
  if (alto >= 0) {
    if (alto === n - 1) return { definida: true, alvo: marcos[alto]!.id, proximo: null };
    const acima = alto + 1;
    return testado(acima)
      ? { definida: true, alvo: marcos[acima]!.id, proximo: null }
      : { definida: false, alvo: marcos[acima]!.id, proximo: marcos[acima]!.id };
  }
  if (baixo === 0) return { definida: true, alvo: marcos[0]!.id, proximo: null };
  return { definida: false, alvo: marcos[baixo]!.id, proximo: marcos[baixo - 1]!.id };
}

/** Etapa de ajuste: um item novo só para a linha ainda indefinida, até o limite de itens. */
export function etapaDeAjuste(marcos: Marco[], resultados: Resultados): string[] {
  const testados = marcos.filter((m) => resultados[m.id] !== undefined).length;
  const a = analisarLinha(marcos, resultados);
  if (a.definida || a.proximo === null || testados >= MAX_ITENS_POR_LINHA) return [];
  return [a.proximo];
}

/** Marco onde posicionar: o resultado da análise, ou o melhor palpite se o limite de itens acabou. */
export function alvoDaSondagem(marcos: Marco[], resultados: Resultados): string | null {
  return analisarLinha(marcos, resultados).alvo;
}

/** Posiciona como o "Está aqui", mas com origem "sondagem". */
export function mudancasDaSondagem(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  alvo: string,
  estados: EstadosCrianca,
  agora: string,
): Record<string, RegistroMarco> {
  const mudancas = posicionarAqui(idx, pista, alvo, estados, agora);
  return Object.fromEntries(
    Object.entries(mudancas).map(([k, v]) => [k, { ...v, origem: 'sondagem' as const }]),
  );
}

/** Erros dos itens de sondagem (lista vazia = válido). Dado de fora: confere antes de usar. */
export function validarSondagem(sondagem: Sondagem, marcos: Marco[]): string[] {
  const erros: string[] = [];
  const ids = new Set<string>();
  const existentes = new Set(marcos.map((m) => m.id));
  const vazio = (t: unknown) => typeof t !== 'string' || t.trim() === '';
  for (const i of sondagem.itens) {
    const onde = `Sondagem ${String(i.id)}`;
    if (ids.has(i.id)) erros.push(`${onde}: id repetido`);
    ids.add(i.id);
    if (!existentes.has(i.marco)) erros.push(`${onde}: marco ${String(i.marco)} não existe`);
    for (const campo of ['instrucao', 'consolidado', 'emDesenvolvimento'] as const) {
      if (vazio(i[campo])) erros.push(`${onde}: "${campo}" vazio`);
    }
    if (i.revisao !== undefined) validarRevisao(i.revisao, onde, erros);
  }
  return erros;
}
