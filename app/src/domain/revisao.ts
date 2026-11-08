// Status de revisão do conteúdo (#77): o conteúdo é rascunhado por IA, revisado pela dona do
// produto e, mais tarde, por preceptores. O app precisa saber o que já foi revisado.
import { ESTADOS_REVISAO, type EstadoRevisao, type Revisao } from './tipos';

const DATA_ISO = /^(\d{4})-(\d{2})-(\d{2})$/;

function dataReal(texto: string): boolean {
  const m = DATA_ISO.exec(texto);
  if (!m) return false;
  const [ano, mes, dia] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const d = new Date(Date.UTC(ano, mes - 1, dia));
  return d.getUTCFullYear() === ano && d.getUTCMonth() === mes - 1 && d.getUTCDate() === dia;
}

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
  if (r.estado === 'rascunho') return;
  if (typeof r.por !== 'string' || r.por.trim() === '') {
    erros.push(`${onde}: revisão "${r.estado}" precisa de "por" (quem revisou)`);
  }
  if (typeof r.em !== 'string' || !dataReal(r.em)) {
    erros.push(`${onde}: revisão "${r.estado}" precisa de "em" no formato AAAA-MM-DD`);
  }
}

/**
 * Só o aprovado chega às famílias. Item sem `revisao` é o conteúdo anterior à #77 (já revisado
 * antes de existir o campo) e continua publicado; a regra vale para o conteúdo novo.
 */
export function estaPublicavel(item: { revisao?: Revisao }): boolean {
  return item.revisao === undefined || item.revisao.estado === 'aprovado';
}
