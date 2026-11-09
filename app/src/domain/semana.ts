// Plano semanal (#8, §6 da especificação). Funções puras e determinísticas: tudo vem por parâmetro.
import type { IndiceConteudo } from './conteudo';
import { dataLocalISO } from './datas';
import { idPista, pistasDaCrianca, posicaoDaLinha } from './jornada';
import { candidatas, atividadesRecentes, proporSessao, proximaAlternativa } from './sessao';
import type { Crianca, EstadosCrianca, Familia, Sessao } from './tipos';

export const DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom'] as const;
export type Dia = (typeof DIAS)[number];

export const NOME_DIA: Record<Dia, string> = {
  seg: 'Segunda',
  ter: 'Terça',
  qua: 'Quarta',
  qui: 'Quinta',
  sex: 'Sexta',
  sab: 'Sábado',
  dom: 'Domingo',
};

/** Dias e duração escolhidos, guardados por criança para não repetir toda semana. */
export interface Rotina {
  dias: Dia[];
  duracaoMin: number;
}

export interface DiaPlano {
  dia: Dia;
  /** AAAA-MM-DD */
  data: string;
  duracaoMin: number;
  atividadeIds: string[];
  livroId: string | null;
  feito: boolean;
  /** sessão registrada para este dia (liga com o registro de progresso, #11) */
  sessaoId?: string;
}

export interface PlanoSemana {
  id: string;
  criancaId: string;
  /** segunda-feira da semana, AAAA-MM-DD */
  inicio: string;
  criadoEm: string;
  rotina: Rotina;
  dias: DiaPlano[];
}

export interface EntradaSemana {
  familia: Familia;
  crianca: Crianca;
  idade: number;
  estados: EstadosCrianca;
  /** sessões já feitas: contam como "recentes" para não repetir e para equilibrar as linhas */
  historico: Sessao[];
  rotina: Rotina;
  agora: string;
  /** id do plano novo (vem de fora para a função continuar pura) */
  id: string;
}

/** Segunda-feira da semana de `data`, no calendário local (domingo fecha a semana). */
export function segundaDaSemana(data: Date): string {
  const d = new Date(data.getFullYear(), data.getMonth(), data.getDate());
  const desde = (d.getDay() + 6) % 7; // segunda = 0 … domingo = 6
  d.setDate(d.getDate() - desde);
  return dataLocalISO(d);
}

function dataDoDia(inicio: string, dia: Dia): string {
  const [a, m, d] = inicio.split('-').map(Number) as [number, number, number];
  const data = new Date(a, m - 1, d + DIAS.indexOf(dia));
  return dataLocalISO(data);
}

/** Sessão fictícia: faz o dia seguinte tratar o que já foi planejado como "feito recentemente". */
function simulada(entrada: EntradaSemana, i: number, atividadeIds: string[], min: number): Sessao {
  return {
    id: `plano-${i}`,
    codigo: `P-${i}`,
    criancaId: entrada.crianca.id,
    criadaEm: entrada.agora,
    duracaoMin: min,
    foco: 'equilibrado',
    atividadeIds,
    livroId: null,
  };
}

/**
 * Distribui as linhas pelos dias reaproveitando o gerador de sessão (§5.6), dia a dia: o que já entrou
 * na semana vira histórico, então nenhuma atividade se repete e as linhas se alternam.
 */
export function planejarSemana(idx: IndiceConteudo, entrada: EntradaSemana): PlanoSemana {
  const inicio = segundaDaSemana(new Date(entrada.agora));
  const dias = DIAS.filter((d) => entrada.rotina.dias.includes(d));
  const simuladas: Sessao[] = [];
  const plano: DiaPlano[] = [];
  dias.forEach((dia, i) => {
    const proposta = proporSessao(idx, {
      familia: entrada.familia,
      crianca: entrada.crianca,
      idade: entrada.idade,
      estados: entrada.estados,
      historico: [...entrada.historico, ...simuladas],
      duracaoMin: entrada.rotina.duracaoMin,
      foco: 'equilibrado',
      agora: entrada.agora,
      excluir: simuladas.flatMap((x) => x.atividadeIds), // nenhuma atividade se repete na semana
    });
    const ids = proposta.escolhas.map((e) => e.atividade.id);
    simuladas.push(simulada(entrada, i, ids, proposta.minutos));
    plano.push({
      dia,
      data: dataDoDia(inicio, dia),
      duracaoMin: entrada.rotina.duracaoMin,
      atividadeIds: ids,
      livroId: proposta.livro?.id ?? null,
      feito: false,
    });
  });
  return {
    id: entrada.id,
    criancaId: entrada.crianca.id,
    inicio,
    criadoEm: entrada.agora,
    rotina: { dias, duracaoMin: entrada.rotina.duracaoMin },
    dias: plano,
  };
}

const mudarDia = (plano: PlanoSemana, dia: Dia, mudar: (d: DiaPlano) => DiaPlano): PlanoSemana => ({
  ...plano,
  dias: plano.dias.map((d) => (d.dia === dia ? mudar(d) : d)),
});

export function removerAtividade(plano: PlanoSemana, dia: Dia, atividadeId: string): PlanoSemana {
  return mudarDia(plano, dia, (d) => ({
    ...d,
    atividadeIds: d.atividadeIds.filter((id) => id !== atividadeId),
  }));
}

export function marcarFeito(
  plano: PlanoSemana,
  dia: Dia,
  feito: boolean,
  sessaoId?: string,
): PlanoSemana {
  return mudarDia(plano, dia, (d) => {
    const resto: DiaPlano = { ...d, feito };
    delete resto.sessaoId; // desmarcar solta a sessão; marcar com sessão a liga de novo
    if (feito && sessaoId) resto.sessaoId = sessaoId;
    return resto;
  });
}

/**
 * Troca uma atividade do dia pela próxima candidata da mesma linha que ainda não está na semana.
 * Devolve null se a linha não tem outra opção.
 */
export function trocarAtividade(
  idx: IndiceConteudo,
  entrada: EntradaSemana,
  plano: PlanoSemana,
  dia: Dia,
  atividadeId: string,
): PlanoSemana | null {
  const ocupadas = new Set(plano.dias.flatMap((d) => d.atividadeIds));
  const recentes = atividadesRecentes(entrada.historico, entrada.crianca.id, entrada.agora);
  for (const pista of pistasDaCrianca(idx, entrada.familia, entrada.crianca)) {
    const pos = posicaoDaLinha(
      idx,
      pista,
      entrada.estados,
      entrada.idade,
      entrada.familia.vertentePrincipal,
    );
    const fila = candidatas(idx, pista, pos.ativos, entrada.familia, entrada.idade, recentes).map(
      (e) => ({ ...e, pista: idPista(pista) }),
    );
    if (!fila.some((e) => e.atividade.id === atividadeId)) continue;
    const outra = proximaAlternativa(fila, atividadeId, ocupadas);
    if (!outra) return null;
    return mudarDia(plano, dia, (d) => ({
      ...d,
      atividadeIds: d.atividadeIds.map((id) => (id === atividadeId ? outra.atividade.id : id)),
    }));
  }
  return null;
}

export interface MaterialDaSemana {
  item: string;
  deCasa: boolean;
  /** dias da semana em que o material é usado */
  dias: Dia[];
}

/** Lista de materiais da semana toda: o mesmo item em dois dias aparece uma vez, com os dias. */
export function materiaisDaSemana(idx: IndiceConteudo, plano: PlanoSemana): MaterialDaSemana[] {
  const mapa = new Map<string, MaterialDaSemana>();
  for (const d of plano.dias) {
    for (const id of d.atividadeIds) {
      for (const m of idx.atividade(id)?.materiais ?? []) {
        const atual = mapa.get(m.item) ?? { item: m.item, deCasa: m.deCasa, dias: [] };
        if (!atual.dias.includes(d.dia)) atual.dias.push(d.dia);
        mapa.set(m.item, atual);
      }
    }
  }
  return [...mapa.values()];
}
