// Registro de sessão (#11, §5.2 e §5.7 da especificação). Funções puras: a data de "agora" vem de fora.
//
// Regra de ouro (§5.2): a ficha grava a OBSERVAÇÃO da sessão e NUNCA muda o estado do marco.
// Só o pai muda o estado, no mapa da jornada. Por isso nada aqui devolve ou toca em `estados`.
import { linhaDoMarco, marcosVisiveis, revisaVisivel, type IndiceConteudo } from './conteudo';
import { chaveMarco, estadoDe } from './jornada';
import {
  ANOTACOES_MAX,
  DURACAO_REAL_MAX,
  ENGAJAMENTOS,
  ESTADOS,
  type Atividade,
  type Engajamento,
  type EstadoMarco,
  type EstadosCrianca,
  type EventoMarco,
  type Idioma,
  type Sessao,
} from './tipos';

/** Um marco da ficha de registro de uma sessão. */
export interface Observacao {
  /** chave do estado: o id do marco, ou "id@idioma" em Línguas (igual à da jornada) */
  chave: string;
  marcoId: string;
  idioma?: Idioma;
  /** marco de revisão (a atividade o retoma, não é o principal dela) */
  revisao: boolean;
}

/**
 * Os marcos da ficha, a partir das atividades. Fonte única: o pacote impresso lista exatamente
 * isto, na mesma ordem, e a tela de registro mostra o mesmo. Se um marco é principal numa atividade e
 * revisão em outra, vale como principal. `emLinguas` diz se o marco pertence ao domínio de Línguas,
 * onde o estado é guardado por idioma.
 */
export function observacoesDasAtividades(
  atividades: Atividade[],
  emLinguas: (marcoId: string) => boolean,
  idx: Pick<IndiceConteudo, 'marco'>,
): Observacao[] {
  const mapa = new Map<string, Observacao>();
  const incluir = (a: Atividade, marcoId: string, revisao: boolean) => {
    const idioma = a.idioma !== undefined && emLinguas(marcoId) ? a.idioma : undefined;
    const chave = chaveMarco(marcoId, idioma);
    const atual = mapa.get(chave);
    if (atual) {
      if (atual.revisao && !revisao) mapa.set(chave, { ...atual, revisao: false });
      return;
    }
    const obs: Observacao = { chave, marcoId, revisao };
    if (idioma) obs.idioma = idioma;
    mapa.set(chave, obs);
  };
  for (const a of atividades) {
    // Marco em rascunho não entra na ficha: não há o que observar nem título para mostrar.
    for (const id of marcosVisiveis(idx, a)) incluir(a, id, false);
    for (const id of revisaVisivel(idx, a)) incluir(a, id, true);
  }
  return [...mapa.values()];
}

/** Os marcos da ficha de uma sessão. Atividades que sumiram do conteúdo são ignoradas. */
export function observacoesDaSessao(
  sessao: Pick<Sessao, 'atividadeIds'>,
  idx: IndiceConteudo,
): Observacao[] {
  const atividades = sessao.atividadeIds
    .map((id) => idx.atividade(id))
    .filter((a): a is Atividade => a !== undefined);
  return observacoesDasAtividades(
    atividades,
    (marcoId) => idx.dominioDaLinha(linhaDoMarco(marcoId))?.trilhas !== undefined,
    idx,
  );
}

/** O que o educador preencheu na tela de registro. Tudo chega "cru": é validado aqui. */
export interface EntradaRegistro {
  /** chave do marco → estado escolhido; marco ausente ou `undefined` = sem escolha */
  estados: Record<string, string | undefined>;
  duracaoReal?: number;
  engajamento?: string;
  anotacoes?: string;
}

export interface ResultadoRegistro {
  sessao: Sessao;
  eventos: EventoMarco[];
}

const ehEstado = (v: unknown): v is EstadoMarco => (ESTADOS as readonly unknown[]).includes(v);
const ehEngajamento = (v: unknown): v is Engajamento =>
  (ENGAJAMENTOS as readonly unknown[]).includes(v);

/**
 * Monta o registro: a sessão atualizada (com a data do registro e os detalhes) e um evento de histórico
 * por marco que o educador marcou. Marco sem escolha não gera evento. Recusa qualquer valor fora dos
 * conjuntos conhecidos. Ao corrigir (`anteriores`), só emite evento do marco que mudou.
 * Não altera a sessão recebida. Registrar de novo troca os campos da sessão e
 * acrescenta novos eventos: o histórico nunca é apagado (§4.2).
 */
export function montarRegistro(
  sessao: Sessao,
  ficha: Observacao[],
  entrada: EntradaRegistro,
  agora: string,
  /** o que já estava registrado nesta sessão (`observacoesRegistradas`); vazio no primeiro registro */
  anteriores: Record<string, EstadoMarco> = {},
): ResultadoRegistro {
  const chavesDaFicha = new Set(ficha.map((o) => o.chave));
  for (const chave of Object.keys(entrada.estados)) {
    if (!chavesDaFicha.has(chave))
      throw new Error(`O marco ${chave} não está na ficha desta sessão.`);
  }

  const escolhas: { chave: string; estado: EstadoMarco }[] = [];
  for (const o of ficha) {
    const valor = Object.hasOwn(entrada.estados, o.chave) ? entrada.estados[o.chave] : undefined;
    if (valor === undefined) continue;
    if (!ehEstado(valor)) throw new Error(`Estado desconhecido para o marco ${o.chave}.`);
    escolhas.push({ chave: o.chave, estado: valor });
  }

  const { duracaoReal, engajamento } = entrada;
  if (
    duracaoReal !== undefined &&
    !(Number.isInteger(duracaoReal) && duracaoReal >= 1 && duracaoReal <= DURACAO_REAL_MAX)
  ) {
    throw new Error(
      `A duração real deve ser um número inteiro de minutos, de 1 a ${DURACAO_REAL_MAX}.`,
    );
  }
  if (engajamento !== undefined && !ehEngajamento(engajamento)) {
    throw new Error('Engajamento desconhecido.');
  }
  const anotacoes = entrada.anotacoes?.trim();
  if (anotacoes !== undefined && anotacoes.length > ANOTACOES_MAX) {
    throw new Error(`As anotações podem ter no máximo ${ANOTACOES_MAX} caracteres.`);
  }

  // Os detalhes opcionais são SUBSTITUÍDOS (não mesclados): quem corrige o registro pode apagar um campo.
  const registrada: Sessao = { ...sessao, registradaEm: agora };
  delete registrada.duracaoReal;
  delete registrada.engajamento;
  delete registrada.anotacoes;
  if (duracaoReal !== undefined) registrada.duracaoReal = duracaoReal;
  if (engajamento !== undefined) registrada.engajamento = engajamento;
  if (anotacoes) registrada.anotacoes = anotacoes;

  // Ao corrigir, só o marco cujo estado observado MUDOU gera evento. Reemitir tudo poria observações
  // velhas depois de um "Está aqui" no histórico e faria o selo voltar sozinho.
  const eventos: EventoMarco[] = escolhas
    .filter(({ chave, estado }) => anteriores[chave] !== estado)
    .map(({ chave, estado }) => ({
      criancaId: sessao.criancaId,
      chave,
      registro: { estado, atualizadoEm: agora, origem: 'sessao' },
      sessaoId: sessao.id,
    }));
  return { sessao: registrada, eventos };
}

/** O que já foi marcado numa sessão, para corrigir: vale o último evento de cada marco. */
export function observacoesRegistradas(
  sessaoId: string,
  historico: EventoMarco[],
): Record<string, EstadoMarco> {
  const saida: Record<string, EstadoMarco> = {};
  for (const e of historico) {
    if (e.sessaoId === sessaoId && e.registro.origem === 'sessao') {
      saida[e.chave] = e.registro.estado;
    }
  }
  return saida;
}

/** Mínimo de sessões diferentes com a observação "Consolidado" para o selo aparecer (§5.2). */
export const SESSOES_PARA_PARECER_PRONTO = 2;

/**
 * Selo "parece pronto" (§5.2): o marco AINDA NÃO está Consolidado e teve a observação Consolidado em 2
 * sessões DIFERENTES. É só uma dica: o pai confirma no mapa.
 * - De cada sessão vale só o último registro do marco (corrigir a ficha troca a observação).
 * - Conta sessões com Consolidado, não só a mais recente: uma terceira "Em desenvolvimento" não apaga o selo.
 * - Um "Está aqui" (evento de posicionamento) zera o que veio antes DELE, pela ORDEM do histórico
 *   (a ordem de gravação, não a data). Como o "Está aqui" só grava eventos dos marcos que mudam de
 *   estado, ele zera só os marcos que ele tocou.
 * - Evento sem sessaoId, ou de outra origem que não "sessao", nunca conta.
 */
export function pareceProntoPara(
  chave: string,
  estados: EstadosCrianca,
  historico: EventoMarco[],
): boolean {
  if (estadoDe(estados, chave) === 'consolidado') return false;
  let ultimaPorSessao = new Map<string, EstadoMarco>();
  for (const e of historico) {
    if (e.chave !== chave) continue;
    if (e.registro.origem === 'posicionamento') ultimaPorSessao = new Map();
    else if (e.registro.origem === 'sessao' && e.sessaoId) {
      ultimaPorSessao.set(e.sessaoId, e.registro.estado);
    }
  }
  let consolidadas = 0;
  for (const estado of ultimaPorSessao.values()) if (estado === 'consolidado') consolidadas++;
  return consolidadas >= SESSOES_PARA_PARECER_PRONTO;
}

/** Normaliza o que a pessoa digitou: sem espaços nem hífens, em maiúsculas. */
const normalizarCodigo = (texto: string) => texto.replace(/[\s-]/g, '').toUpperCase();

/**
 * Acha a sessão pelo código impresso na folha (ex.: "S-1014-A1"). Aceita minúsculas, espaços e hífens
 * a mais ou a menos. A comparação é de código inteiro: "A1" não casa com "A10".
 */
export function acharSessaoPorCodigo(texto: string, sessoes: Sessao[]): Sessao | null {
  const procurado = normalizarCodigo(texto);
  if (procurado === '') return null;
  return sessoes.find((s) => normalizarCodigo(s.codigo) === procurado) ?? null;
}

/** As sessões mais recentes primeiro, no máximo `limite`. Não altera a lista recebida. */
export function ultimasSessoes(sessoes: Sessao[], limite: number): Sessao[] {
  return [...sessoes].sort((a, b) => b.criadaEm.localeCompare(a.criadaEm)).slice(0, limite);
}

export const sessaoRegistrada = (sessao: Pick<Sessao, 'registradaEm'>): boolean =>
  sessao.registradaEm !== undefined;
