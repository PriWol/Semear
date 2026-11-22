// Gerador de sessão (§5.6 da especificação). Determinístico: mesma entrada, mesma sugestão.
import type { Atividade, Crianca, EstadosCrianca, Familia, Livro, Sessao, Vertente } from './tipos';
import type { IndiceConteudo } from './conteudo';
import { linhaDoMarco, marcosVisiveis, revisaVisivel } from './conteudo';
import { diasEntre } from './datas';
import { idPista, pistasDaCrianca, posicaoDaLinha, type Pista } from './jornada';

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
}

export interface Lacuna {
  pista: string;
  nomeLinha: string;
  marcos: string[];
}

export interface PropostaSessao {
  escolhas: Escolha[];
  /** pistas com marcos ativos mas sem atividade publicada: avisa a curadoria */
  lacunas: Lacuna[];
  livro: Livro | null;
  minutos: number;
  avisos: string[];
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
): { pontos: number; motivos: string[] } {
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
  if (idade >= atividade.idade[0] && idade <= atividade.idade[1]) {
    pontos += 2;
    motivos.push('idade adequada');
  }
  if (!recentes.has(atividade.id)) {
    pontos += 2;
    motivos.push('não feita nas últimas 2 semanas');
  }
  return { pontos, motivos };
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

/** Atividades candidatas de uma pista: as que trabalham algum marco ativo, melhor pontuadas primeiro. */
export function candidatas(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'idioma'>,
  ativos: string[],
  familia: Familia,
  idade: number,
  recentes: Set<string>,
): Escolha[] {
  const vistas = new Set<string>();
  const lista: Escolha[] = [];
  for (const marcoId of ativos) {
    for (const atividade of idx.atividadesDoMarco(marcoId)) {
      if (vistas.has(atividade.id)) continue;
      if ((atividade.idioma ?? undefined) !== pista.idioma) continue;
      vistas.add(atividade.id);
      lista.push({ atividade, pista: '', ...pontuar(atividade, familia, idade, recentes) });
    }
  }
  return lista.sort((a, b) => b.pontos - a.pontos || a.atividade.id.localeCompare(b.atividade.id));
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
  return (
    idx
      .complementares()
      // Atividade de idioma pertence a uma trilha de Línguas (com jornada), nunca é complementar.
      .filter((a) => a.idioma === undefined && idade >= a.idade[0] && idade <= a.idade[1])
      .map((atividade) => ({
        atividade,
        pista: PISTA_COMPLEMENTAR,
        ...pontuar(atividade, familia, idade, recentes),
      }))
      .sort((a, b) => b.pontos - a.pontos || a.atividade.id.localeCompare(b.atividade.id))
  );
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
  pistas.forEach((pista, ordem) => {
    const pos = posicaoDaLinha(idx, pista, estados, idade, familia.vertentePrincipal);
    if (pos.ativos.length === 0) return;
    const id = idPista(pista);
    const fila = candidatas(idx, pista, pos.ativos, familia, idade, recentes).map((e) => ({
      ...e,
      pista: id,
    }));
    if (fila.length === 0) {
      lacunas.push({ pista: id, nomeLinha: pista.linha.nome, marcos: pos.ativos });
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

  const nivel = (e: Escolha) =>
    nivelDaAtividade(e.atividade.duracaoMin, limite - minutos, teto, parcela);
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
    for (const { fila } of ordenado) {
      const e = fila.find((c) => !usadas.has(c.atividade.id) && nivel(c) <= nivelMax);
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

  return { escolhas, lacunas, livro: sugerirLivro(idx, escolhas, familia, idade), minutos, avisos };
}

/**
 * Próxima atividade para o botão "Trocar": percorre as candidatas da pista em ciclo, a partir da atual,
 * pulando as que já estão em outra posição da sessão. Devolve null se não houver outra opção.
 */
export function proximaAlternativa(
  candidatasDaPista: Escolha[],
  atualId: string,
  ocupadas: Set<string>,
): Escolha | null {
  const lista = candidatasDaPista.filter(
    (c) => c.atividade.id === atualId || !ocupadas.has(c.atividade.id),
  );
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
