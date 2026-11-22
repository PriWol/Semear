// Gerador de sessão (§5.6 da especificação). Determinístico: mesma entrada, mesma sugestão.
import type {
  Atividade,
  Crianca,
  EstadosCrianca,
  Familia,
  Livro,
  Marco,
  Sessao,
  Vertente,
} from './tipos';
import type { IndiceConteudo } from './conteudo';
import { linhaDoMarco, marcosVisiveis, revisaVisivel } from './conteudo';
import { diasEntre } from './datas';
import { idPista, pistasDaCrianca, posicaoParaSugestao, type Pista } from './jornada';
import { adequacaoDeIdade, filtrarForaDaFaixa, type AdequacaoIdade } from './idade-sugestao';

export const DURACOES = [20, 30, 40, 60] as const;
/** Sessão padrão: 30 minutos de atividade; a preparação do adulto é contada à parte (#71). */
export const DURACAO_PADRAO = 30;
/** Folga sobre a duração escolhida (10%), para não descartar uma atividade por poucos minutos. */
const FOLGA = 1.1;
const JANELA_DIAS = 14;

/**
 * Teto suave de duração de UMA atividade, por idade inteira (ADR 0036, D5 da estória #138). Vale como
 * regra prática de rotina para a atenção da criança, sem fonte citável. 2 anos segue o ADR 0021 (até 10 min).
 * Acima do teto a atividade só entra se for a única possível, com aviso.
 */
export const TETOS_DURACAO_POR_IDADE: Readonly<Record<number, number>> = {
  2: 10,
  3: 12,
  4: 15,
  5: 20,
  6: 20,
  7: 25,
  8: 25,
};
/** Charlotte Mason pede lições curtas (10 a 20 min, §3): o teto nunca passa disso, em nenhuma idade. */
export const TETO_CHARLOTTE_MASON = 20;
/** Uma atividade ocupa no máximo metade da sessão, quando há alternativa (critério da estória #145). */
export const FRACAO_MAXIMA_ATIVIDADE = 0.5;
/** Para menores de 4 anos a parcela é menor: 4 a 5 blocos curtos em 30 min, em vez de 2 grandes. */
export const FRACAO_MAXIMA_ATIVIDADE_PEQUENOS = 0.3;
const IDADE_BLOCOS_CURTOS = 4;
/** Meta de mistura de áreas na sessão equilibrada (§5.6): pelo menos 2 domínios, quando o conteúdo permitir. */
const MIN_DOMINIOS = 2;

/** Teto de duração de uma atividade para a idade (inteira, limitada a 2..8) e a vertente principal. */
export function tetoDeDuracao(idade: number, vertente: Vertente): number {
  const inteira = Math.min(8, Math.max(2, Math.floor(idade)));
  const teto = TETOS_DURACAO_POR_IDADE[inteira] ?? 20;
  return vertente === 'Charlotte Mason' ? Math.min(teto, TETO_CHARLOTTE_MASON) : teto;
}

/**
 * Número estável (FNV-1a) a partir do dia e da linha: gira a ordem das linhas empatadas de um dia para o
 * outro sem sorteio, então a mesma entrada dá sempre a mesma sessão (§5.6). Só usa a data, não a hora.
 */
function sementeDoDia(agora: string, linhaId: string): number {
  let h = 0x811c9dc5;
  for (const c of `${agora.slice(0, 10)}|${linhaId}`) {
    h ^= c.charCodeAt(0);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h;
}

export interface PedidoSessao {
  familia: Familia;
  crianca: Crianca;
  idade: number;
  estados: EstadosCrianca;
  historico: Sessao[];
  duracaoMin: number;
  /** ids de pista ("LG.FON" ou "LI.VOC@en"), ou equilibrado */
  foco: string[] | 'equilibrado';
  agora: string;
  /** atividades que não podem entrar (ex.: já planejadas em outro dia da semana, #8) */
  excluir?: string[];
}

export interface Escolha {
  atividade: Atividade;
  pista: string;
  pontos: number;
  motivos: string[];
  /** avisos da escolha para a tela: fora da faixa de idade ("versão mais simples"), vertente (§5.3) */
  notas?: string[];
  /** a idade da criança está fora da faixa da atividade (D4); ela só entra depois das que servem à idade */
  foraDaFaixa?: boolean;
}

export interface Lacuna {
  pista: string;
  nomeLinha: string;
  marcos: string[];
  /** `idade`: havia atividade, mas nenhuma adequada à idade da criança (D4); a linha não é forçada */
  motivo?: 'idade';
}

export interface PropostaSessao {
  escolhas: Escolha[];
  /** pistas com marcos ativos mas sem atividade publicada: avisa a curadoria */
  lacunas: Lacuna[];
  livro: Livro | null;
  minutos: number;
  avisos: string[];
  /** nomes das linhas em que a criança não tinha registro e o ponto de partida veio da idade (D6) */
  linhasPelaIdade: string[];
}

/** Atividades feitas pela criança nas últimas 2 semanas (usadas na pontuação "novidade"). */
export function atividadesRecentes(
  historico: Sessao[],
  criancaId: string,
  agora: string,
): Set<string> {
  return new Set(
    historico
      .filter((s) => s.criancaId === criancaId && diasEntre(s.criadaEm, agora) <= JANELA_DIAS)
      .flatMap((s) => s.atividadeIds),
  );
}

/** Pontuação da atividade (§5.6, passo 3). Exportada para os testes e para a tela explicar a escolha. */
export function pontuar(
  atividade: Atividade,
  familia: Familia,
  idade: number,
  recentes: Set<string>,
): { pontos: number; motivos: string[]; notas: string[] } {
  let pontos = 0;
  const motivos: string[] = [];
  if (atividade.vertentes.includes(familia.vertentePrincipal)) {
    pontos += 3;
    motivos.push(`combina com ${familia.vertentePrincipal}`);
  }
  const insp = familia.inspiracoes.find((v) => atividade.vertentes.includes(v));
  if (insp) {
    pontos += 1;
    motivos.push(`inspiração ${insp}`);
  }
  // A idade é peso graduado, não filtro (D4; ver idade-sugestao.ts). A exclusão dura é de `candidatas`.
  const adequacao = adequacaoDeIdade(atividade, idade);
  pontos += adequacao.pontos;
  motivos.push(...adequacao.motivos);
  if (!recentes.has(atividade.id)) {
    pontos += 2;
    motivos.push('não feita nas últimas 2 semanas');
  }
  return { pontos, motivos, notas: adequacao.notas };
}

/** Penalidade por marco ativo antes da idade de introdução da vertente principal (Waldorf etc., §5.3, F). */
export const PENALIDADE_ANTES_DA_INTRODUCAO = 4;

/**
 * Ajuste pela vertente (§5.3): se TODOS os marcos ativos que levam à atividade são anteriores à idade de
 * introdução da vertente principal, ela perde pontos e ganha uma nota. Um marco que a vertente já aceita
 * basta para a atividade não ser penalizada.
 */
function ajusteDeVertente(
  marcos: Marco[],
  vertente: Vertente,
  idade: number,
): { pontos: number; notas: string[] } {
  const intros = marcos.map((m) => m.idadeIntroducao[vertente]);
  if (intros.length === 0 || intros.some((i) => i === undefined || i <= idade)) {
    return { pontos: 0, notas: [] };
  }
  const intro = Math.min(...intros.filter((i): i is number => i !== undefined));
  return {
    pontos: -PENALIDADE_ANTES_DA_INTRODUCAO,
    notas: [
      `Na pedagogia ${vertente}, este marco costuma ser introduzido por volta dos ${intro} anos.`,
    ],
  };
}

/** Minutos trabalhados por pista nas últimas 2 semanas, para o modo equilibrado. */
function minutosPorLinha(
  idx: IndiceConteudo,
  historico: Sessao[],
  criancaId: string,
  agora: string,
): Map<string, number> {
  const mapa = new Map<string, number>();
  for (const s of historico) {
    if (s.criancaId !== criancaId || diasEntre(s.criadaEm, agora) > JANELA_DIAS) continue;
    for (const id of s.atividadeIds) {
      const a = idx.atividade(id);
      if (!a) continue;
      const linhas = new Set(marcosVisiveis(idx, a).map(linhaDoMarco));
      for (const l of linhas) mapa.set(l, (mapa.get(l) ?? 0) + a.duracaoMin);
    }
  }
  return mapa;
}

/** Candidatas de uma pista e quantas foram excluídas só pela regra de idade (para a linha virar lacuna). */
export interface CandidatasDaPista {
  escolhas: Escolha[];
  excluidasPorIdade: number;
}

/**
 * Atividades candidatas de uma pista: as que trabalham algum marco ativo, melhor pontuadas primeiro, já com
 * a regra de idade (D4: exclusão dura, e "mais de 1 ano fora só sem alternativa dentro da faixa") e o ajuste
 * pela vertente (F).
 */
export function candidatasDaPista(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'idioma'>,
  ativos: string[],
  familia: Familia,
  idade: number,
  recentes: Set<string>,
): CandidatasDaPista {
  const porAtividade = new Map<string, { atividade: Atividade; marcos: Marco[] }>();
  for (const marcoId of ativos) {
    const marco = idx.marco(marcoId);
    for (const atividade of idx.atividadesDoMarco(marcoId)) {
      if ((atividade.idioma ?? undefined) !== pista.idioma) continue;
      const item = porAtividade.get(atividade.id) ?? { atividade, marcos: [] };
      if (marco) item.marcos.push(marco);
      porAtividade.set(atividade.id, item);
    }
  }
  const todas = [...porAtividade.values()].map(({ atividade, marcos }) => {
    const adequacao = adequacaoDeIdade(atividade, idade);
    const vertente = ajusteDeVertente(marcos, familia.vertentePrincipal, idade);
    const base = pontuar(atividade, familia, idade, recentes);
    const escolha: Escolha = {
      atividade,
      pista: '',
      pontos: base.pontos + vertente.pontos,
      motivos: base.motivos,
      notas: [...base.notas, ...vertente.notas],
      ...(adequacao.lado !== 'dentro' ? { foraDaFaixa: true } : {}),
    };
    return { escolha, adequacao };
  });
  const aceitas = todas.filter((c) => !c.adequacao.excluida);
  const escolhas = filtrarForaDaFaixa(aceitas)
    .map((c) => c.escolha)
    .sort((a, b) => b.pontos - a.pontos || a.atividade.id.localeCompare(b.atividade.id));
  return { escolhas, excluidasPorIdade: todas.length - aceitas.length };
}

export function candidatas(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'idioma'>,
  ativos: string[],
  familia: Familia,
  idade: number,
  recentes: Set<string>,
): Escolha[] {
  return candidatasDaPista(idx, pista, ativos, familia, idade, recentes).escolhas;
}

/** Id de "pista" das complementares: elas não pertencem a nenhuma linha da jornada. */
export const PISTA_COMPLEMENTAR = 'complementar';

/** Complementares adequadas à idade (§3.0), melhor pontuadas primeiro. Rascunhos nunca chegam aqui. */
export function complementares(
  idx: IndiceConteudo,
  familia: Familia,
  idade: number,
  recentes: Set<string>,
): Escolha[] {
  // Atividade de idioma pertence a uma trilha de Línguas (com jornada), nunca é complementar. A idade segue
  // a mesma regra graduada das candidatas das linhas (D4), em vez do filtro rígido de antes.
  const aceitas = idx
    .complementares()
    .filter((a) => a.idioma === undefined)
    .map((atividade) => ({ atividade, adequacao: adequacaoDeIdade(atividade, idade) }))
    .filter((c) => !c.adequacao.excluida);
  return filtrarForaDaFaixa<{ atividade: Atividade; adequacao: AdequacaoIdade }>(aceitas)
    .map(({ atividade }) => ({
      atividade,
      pista: PISTA_COMPLEMENTAR,
      ...pontuar(atividade, familia, idade, recentes),
    }))
    .sort((a, b) => b.pontos - a.pontos || a.atividade.id.localeCompare(b.atividade.id));
}

/** Fila de candidatas de uma pista, com a posição dela na ordem do dia (para desempates estáveis). */
interface FilaPista {
  pista: Pista;
  id: string;
  ordem: number;
  fila: Escolha[];
}

/** Pistas em ordem de "quem merece abrir a sessão": menos tempo trabalhado, depois a semente do dia. */
function ordenarEquilibrado(todas: Pista[], minutos: Map<string, number>, agora: string): Pista[] {
  return todas
    .map((p, ordem) => ({
      p,
      ordem,
      min: minutos.get(p.linha.id) ?? 0,
      semente: sementeDoDia(agora, idPista(p)),
    }))
    .sort((a, b) => a.min - b.min || a.semente - b.semente || a.ordem - b.ordem)
    .map((x) => x.p);
}

/** Agrupa as pistas por domínio, na ordem em que cada domínio aparece pela primeira vez. */
function agruparPorDominio(filas: FilaPista[]): FilaPista[][] {
  const grupos = new Map<string, FilaPista[]>();
  for (const f of filas) {
    const g = grupos.get(f.pista.dominio.id);
    if (g) g.push(f);
    else grupos.set(f.pista.dominio.id, [f]);
  }
  return [...grupos.values()];
}

const idDominio = (grupo: FilaPista[]) => grupo[0]?.pista.dominio.id ?? '';

/** Quão bem a atividade serve agora: 0 = ideal; 1 = cabe, mas passa da parcela; 2 = passa do teto; 3 = não cabe. */
function nivelDaAtividade(
  minutosAtividade: number,
  restante: number,
  teto: number,
  parcela: number,
): 0 | 1 | 2 | 3 {
  if (minutosAtividade > restante) return 3;
  if (minutosAtividade > teto) return 2;
  return minutosAtividade > parcela ? 1 : 0;
}

/** Nome da linha para a tela: "Fonologia" ou "Vocabulário (en)". */
function nomeDaPista(p: Pista): string {
  return p.idioma ? `${p.linha.nome} (${p.idioma})` : p.linha.nome;
}

export function proporSessao(idx: IndiceConteudo, pedido: PedidoSessao): PropostaSessao {
  const { familia, crianca, idade, estados, historico, duracaoMin, foco, agora } = pedido;
  const recentes = atividadesRecentes(historico, crianca.id, agora);
  const todas = pistasDaCrianca(idx, familia, crianca);

  // 1. Pistas candidatas: o foco do pai, ou as menos trabalhadas nas últimas 2 semanas. Quando várias
  // empatam (criança sem histórico), a semente do dia gira a ordem, em vez de a ordem do arquivo.
  let pistas: Pista[];
  if (foco === 'equilibrado') {
    pistas = ordenarEquilibrado(todas, minutosPorLinha(idx, historico, crianca.id, agora), agora);
  } else {
    pistas = foco
      .map((id) => todas.find((p) => idPista(p) === id))
      .filter((p): p is Pista => p !== undefined);
  }

  // 2. Candidatas por pista, a partir dos marcos ativos.
  const filas: FilaPista[] = [];
  const lacunas: Lacuna[] = [];
  // Linha sem nenhum registro: o ponto de partida é provisório, pela idade (D6); nada é gravado.
  const pelaIdade = new Map<string, string>();
  pistas.forEach((pista, ordem) => {
    const pos = posicaoParaSugestao(idx, pista, estados, idade, familia.vertentePrincipal);
    if (pos.ativos.length === 0) return;
    const id = idPista(pista);
    if (pos.provisoria) pelaIdade.set(id, nomeDaPista(pista));
    const { escolhas: candidatas, excluidasPorIdade } = candidatasDaPista(
      idx,
      pista,
      pos.ativos,
      familia,
      idade,
      recentes,
    );
    const fila = candidatas.map((e) => ({ ...e, pista: id }));
    if (fila.length === 0) {
      lacunas.push({
        pista: id,
        nomeLinha: pista.linha.nome,
        marcos: pos.ativos,
        ...(excluidasPorIdade > 0 ? { motivo: 'idade' as const } : {}),
      });
    } else {
      filas.push({ pista, id, ordem, fila });
    }
  });

  // 3-4. Preenche a duração em rodadas por DOMÍNIO (no máximo uma atividade por domínio por rodada).
  // Dentro do domínio, vem primeiro a linha com menos atividades já escolhidas. A próxima atividade é a
  // melhor pontuada que caiba no tempo que resta (ver nivelDaAtividade).
  const escolhas: Escolha[] = [];
  const usadas = new Set<string>(pedido.excluir ?? []);
  const porPista = new Map<string, number>();
  const porDominio = new Map<string, number>();
  const dominioDaPista = new Map(filas.map((f) => [f.id, f.pista.dominio.id]));
  const dominios = agruparPorDominio(filas);
  const limite = duracaoMin * FOLGA;
  const teto = tetoDeDuracao(idade, familia.vertentePrincipal);
  const parcela =
    duracaoMin *
    (idade < IDADE_BLOCOS_CURTOS ? FRACAO_MAXIMA_ATIVIDADE_PEQUENOS : FRACAO_MAXIMA_ATIVIDADE);
  let minutos = 0;

  // Fora da faixa de idade não é "ideal" (nível 0): entra na segunda passada, depois de quem serve à idade.
  // Exceção: enquanto a sessão tem menos de 2 domínios, um domínio ainda sem atividade pode usá-la, para
  // não perder a mistura de áreas (§5.6, meta de 30 min).
  const nivel = (e: Escolha, dominioVazio = false) => {
    const n = nivelDaAtividade(e.atividade.duracaoMin, limite - minutos, teto, parcela);
    return e.foraDaFaixa && n === 0 && !dominioVazio ? 1 : n;
  };
  const adicionar = (e: Escolha) => {
    escolhas.push(e);
    usadas.add(e.atividade.id);
    minutos += e.atividade.duracaoMin;
    porPista.set(e.pista, (porPista.get(e.pista) ?? 0) + 1);
    const dominio = dominioDaPista.get(e.pista);
    if (dominio) porDominio.set(dominio, (porDominio.get(dominio) ?? 0) + 1);
  };
  const escolherNoDominio = (grupo: FilaPista[], nivelMax: 0 | 1): Escolha | undefined => {
    const ordenado = [...grupo].sort(
      (a, b) => (porPista.get(a.id) ?? 0) - (porPista.get(b.id) ?? 0) || a.ordem - b.ordem,
    );
    const vazio =
      (porDominio.get(idDominio(grupo)) ?? 0) === 0 &&
      porDominio.size < MIN_DOMINIOS &&
      dominios.length >= MIN_DOMINIOS;
    for (const { fila } of ordenado) {
      const e = fila.find((c) => !usadas.has(c.atividade.id) && nivel(c, vazio) <= nivelMax);
      if (e) return e;
    }
    return undefined;
  };
  const preencher = (nivelMax: 0 | 1) => {
    let adicionou = true;
    while (adicionou) {
      adicionou = false;
      // Rodízio: quem tem menos atividades na sessão vai primeiro, para um domínio não consumir o tempo
      // antes de os outros terem a vez. O sort é estável, então o empate segue a ordem do dia.
      const vez = [...dominios].sort(
        (a, b) => (porDominio.get(idDominio(a)) ?? 0) - (porDominio.get(idDominio(b)) ?? 0),
      );
      for (const grupo of vez) {
        const e = escolherNoDominio(grupo, nivelMax);
        if (e) {
          adicionar(e);
          adicionou = true;
        }
      }
    }
  };

  preencher(0);
  // Atividade que ocupa mais que a parcela só entra depois de outra: sozinha, só como último recurso.
  if (escolhas.length > 0) preencher(1);

  // 5. No máximo uma complementar, só se couber na duração escolhida e no teto da idade. Com linhas de
  // foco escolhidas à mão, a educadora pediu essas linhas: não acrescenta nada por conta própria.
  const comp =
    foco === 'equilibrado'
      ? complementares(idx, familia, idade, recentes).find(
          (e) => !usadas.has(e.atividade.id) && nivel(e) <= 1,
        )
      : undefined;
  if (comp) adicionar(comp);

  // Último recurso (sessão ainda vazia): a primeira também precisa caber. Escolhe a mais curta que
  // caiba no tempo e no teto; se nenhuma serve, a mais curta de todas, e o aviso explica.
  if (escolhas.length === 0) {
    const sobra = filas
      .flatMap((f) => f.fila.map((e) => ({ e, ordem: f.ordem })))
      .filter((x) => !usadas.has(x.e.atividade.id))
      .map((x) => ({ ...x, n: nivel(x.e) }));
    sobra.sort(
      (a, b) =>
        Number(a.n === 3) - Number(b.n === 3) ||
        Number(a.n >= 2) - Number(b.n >= 2) ||
        Number(a.e.foraDaFaixa === true) - Number(b.e.foraDaFaixa === true) ||
        a.e.atividade.duracaoMin - b.e.atividade.duracaoMin ||
        a.ordem - b.ordem ||
        b.e.pontos - a.e.pontos ||
        a.e.atividade.id.localeCompare(b.e.atividade.id),
    );
    const primeira = sobra[0];
    if (primeira) {
      adicionar(primeira.e);
      // Acima do teto ou do tempo, a atividade fica sozinha; dentro dos dois, a sessão continua.
      if (primeira.n <= 1) {
        preencher(0);
        preencher(1);
      }
    }
  }

  const avisos: string[] = [];
  if (escolhas.length > 0 && minutos > limite) {
    avisos.push(
      `A atividade sugerida tem ${minutos} min, mais do que os ${duracaoMin} min escolhidos. Você pode fazê-la em duas partes.`,
    );
  }
  const acima = escolhas.find((e) => e.atividade.duracaoMin > teto);
  if (acima) {
    avisos.push(
      `A atividade sugerida tem ${acima.atividade.duracaoMin} min, mais do que o recomendado para ${Math.floor(idade)} anos (até ${teto} min). Você pode fazê-la em duas partes.`,
    );
  }
  if (pistas.length === 0 && foco !== 'equilibrado')
    avisos.push('Escolha pelo menos uma linha de foco.');
  const porIdade = lacunas.filter((l) => l.motivo === 'idade');
  if (porIdade.length > 0) {
    avisos.push(
      `Sem atividade adequada para ${Math.floor(idade)} anos em: ${porIdade.map((l) => l.nomeLinha).join(', ')}. Preferimos não sugerir uma atividade que não serve à idade.`,
    );
  }
  // D6: só avisa das linhas que de fato deram atividade à sessão.
  const linhasPelaIdade = [
    ...new Set(escolhas.flatMap((e) => (pelaIdade.has(e.pista) ? [pelaIdade.get(e.pista)!] : []))),
  ];
  if (linhasPelaIdade.length > 0) {
    avisos.push(
      `${crianca.nome} ainda não foi posicionada em ${linhasPelaIdade.join(', ')}: usamos a idade (${Math.floor(idade)} anos) como ponto de partida. Marque "Está aqui" na jornada ou faça a sondagem para acertar.`,
    );
  }

  return {
    escolhas,
    lacunas,
    livro: sugerirLivro(idx, escolhas, familia, idade),
    minutos,
    avisos,
    linhasPelaIdade,
  };
}

/**
 * Opções do botão "Trocar" para a atividade `atualId` (a atual fica na lista, para o ciclo): as candidatas da
 * pista que não estão em outra posição da sessão e respeitam o teto de duração da idade (ADR 0036). Se a atual
 * já passa do teto e nenhuma outra cabe nele, a pista só tem atividades longas (o gerador entrou com a mais
 * curta e avisou): então o teto deixa de valer, e a família ainda pode trocar entre elas, com o mesmo aviso.
 * As candidatas já vêm com a regra de idade (D4).
 */
export function opcoesDeTroca(
  candidatasDaPista: Escolha[],
  atualId: string,
  ocupadas: Set<string>,
  teto?: number,
): Escolha[] {
  const livres = candidatasDaPista.filter(
    (c) => c.atividade.id === atualId || !ocupadas.has(c.atividade.id),
  );
  if (teto === undefined) return livres;
  const dentro = livres.filter((c) => c.atividade.duracaoMin <= teto);
  const atual = livres.find((c) => c.atividade.id === atualId);
  const soLongas = atual !== undefined && atual.atividade.duracaoMin > teto && dentro.length === 0;
  return soLongas ? livres : dentro.concat(atual && !dentro.includes(atual) ? [atual] : []);
}

/**
 * Próxima atividade para o botão "Trocar": percorre as opções (ver `opcoesDeTroca`) em ciclo, a partir da
 * atual. Devolve null se não houver outra.
 */
export function proximaAlternativa(
  candidatasDaPista: Escolha[],
  atualId: string,
  ocupadas: Set<string>,
  teto?: number,
): Escolha | null {
  const lista = opcoesDeTroca(candidatasDaPista, atualId, ocupadas, teto);
  const i = lista.findIndex((c) => c.atividade.id === atualId);
  for (let passo = 1; passo < lista.length; passo++) {
    const c = lista[(i + passo) % lista.length];
    if (c && c.atividade.id !== atualId) return c;
  }
  return null;
}

/** Livro da curadoria ligado aos marcos da sessão (§5.6, passo 6). */
export function sugerirLivro(
  idx: IndiceConteudo,
  escolhas: Pick<Escolha, 'atividade'>[],
  familia: Familia,
  idade: number,
): Livro | null {
  const marcos = new Set(
    escolhas.flatMap((e) => [
      ...marcosVisiveis(idx, e.atividade),
      ...revisaVisivel(idx, e.atividade),
    ]),
  );
  // A indicação liga por marco ou pela linha do marco (#73): obra e música costumam servir a uma linha toda.
  const linhas = new Set([...marcos].map(linhaDoMarco));
  const candidatos = idx.conteudo.livros
    .filter(
      (l) => l.marcos.some((m) => marcos.has(m)) || (l.linhas ?? []).some((x) => linhas.has(x)),
    )
    .map((l) => ({
      l,
      pontos:
        (l.vertentes.includes(familia.vertentePrincipal) ? 2 : 0) +
        (idade >= l.idade[0] && idade <= l.idade[1] ? 1 : 0),
    }))
    .sort((a, b) => b.pontos - a.pontos || a.l.id.localeCompare(b.l.id));
  return candidatos[0]?.l ?? null;
}

/**
 * Código curto da sessão, impresso na ficha (ex.: S-1013-A1):
 * mês+dia, inicial da criança e um número sequencial do dia.
 */
export function gerarCodigoSessao(nomeCrianca: string, agora: Date, existentes: string[]): string {
  const mm = String(agora.getMonth() + 1).padStart(2, '0');
  const dd = String(agora.getDate()).padStart(2, '0');
  const inicial =
    nomeCrianca
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // remove acentos antes de limpar o resto
      .replace(/[^A-Za-z]/g, '')
      .charAt(0)
      .toUpperCase() || 'X';
  const base = `S-${mm}${dd}-${inicial}`;
  let n = 1;
  while (existentes.includes(`${base}${n}`)) n++;
  return `${base}${n}`;
}
