// Status de revisão do conteúdo (#77): o conteúdo é rascunhado por IA, revisado pela dona do
// produto e, mais tarde, por preceptores. O app precisa saber o que já foi revisado.
import { dataValida } from './datas';
import {
  ESTADOS_CONFERENCIA,
  ESTADOS_REVISAO,
  type EstadoConferencia,
  type EstadoRevisao,
  type Revisao,
} from './tipos';

/** Acrescenta a `erros` o que estiver errado em `revisao`; `onde` identifica o item na mensagem. */
export function validarRevisao(revisao: unknown, onde: string, erros: string[]): void {
  if (typeof revisao !== 'object' || revisao === null) {
    erros.push(`${onde}: revisão inválida (esperado { estado, por, em })`);
    return;
  }
  const r = revisao as Partial<Record<keyof Revisao, unknown>>;
  if (!ESTADOS_REVISAO.includes(r.estado as EstadoRevisao)) {
    erros.push(
      `${onde}: estado de revisão "${String(r.estado)}" fora de ${ESTADOS_REVISAO.join(', ')}`,
    );
    return;
  }
  if (r.estado !== 'rascunho') {
    if (typeof r.por !== 'string' || r.por.trim() === '') {
      erros.push(`${onde}: revisão "${r.estado}" precisa de "por" (quem revisou)`);
    }
    if (typeof r.em !== 'string' || !dataValida(r.em)) {
      erros.push(`${onde}: revisão "${r.estado}" precisa de "em" no formato AAAA-MM-DD`);
    }
  }
  if (r.conferenciaProfissional !== undefined) {
    validarConferencia(r.conferenciaProfissional, onde, erros);
  }
}

/** Conferência profissional (ADR 0037): estado conhecido; "conferida" diz quem e quando. */
function validarConferencia(conferencia: unknown, onde: string, erros: string[]): void {
  if (typeof conferencia !== 'object' || conferencia === null || Array.isArray(conferencia)) {
    erros.push(`${onde}: conferência profissional inválida (esperado { estado, por, em })`);
    return;
  }
  const c = conferencia as { estado?: unknown; por?: unknown; em?: unknown };
  if (!ESTADOS_CONFERENCIA.includes(c.estado as EstadoConferencia)) {
    erros.push(
      `${onde}: estado de conferência profissional "${String(c.estado)}" fora de ${ESTADOS_CONFERENCIA.join(', ')}`,
    );
    return;
  }
  if (c.estado !== 'conferida') return;
  if (typeof c.por !== 'string' || c.por.trim() === '') {
    erros.push(`${onde}: conferência "conferida" precisa de "por" (quem conferiu)`);
  }
  if (typeof c.em !== 'string' || !dataValida(c.em)) {
    erros.push(`${onde}: conferência "conferida" precisa de "em" no formato AAAA-MM-DD`);
  }
}

/**
 * Só o aprovado chega às famílias. Item sem `revisao` é o conteúdo anterior à #77 (já revisado
 * antes de existir o campo) e continua publicado; a regra vale para o conteúdo novo.
 */
export function estaPublicavel(item: { revisao?: Revisao }): boolean {
  return item.revisao === undefined || item.revisao.estado === 'aprovado';
}

/** Texto do selo único por tela (#138 D2). A parte "Não substitui o pediatra" nunca sai (ADR 0037). */
export const TEXTO_NAO_SUBSTITUI = 'Não substitui o pediatra.';
export const TEXTO_SELO_CONFERENCIA = `Orientação em conferência por profissional de saúde. ${TEXTO_NAO_SUBSTITUI}`;

/** true se algum item da tela tem a conferência profissional pendente; some quando é conferida. */
export function precisaAvisoDeConferencia(itens: readonly { revisao?: Revisao }[]): boolean {
  return itens.some((i) => i.revisao?.conferenciaProfissional?.estado === 'pendente');
}
