// Gerador de sessão (§5.6 da especificação). Determinístico: mesma entrada, mesma sugestão.
import type { Atividade, Crianca, EstadosCrianca, Familia, Livro, Sessao } from './tipos';
import type { IndiceConteudo } from './conteudo';
import { linhaDoMarco } from './conteudo';
import { diasEntre } from './datas';
import { idPista, pistasDaCrianca, posicaoDaLinha, type Pista } from './jornada';

export const DURACOES = [20, 40, 60] as const;
/** Folga sobre a duração escolhida (10%), para não descartar uma atividade por poucos minutos. */
const FOLGA = 1.1;
const JANELA_DIAS = 14;

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
      const linhas = new Set(a.marcos.map(linhaDoMarco));
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
  return idx
    .complementares()
    .filter((a) => idade >= a.idade[0] && idade <= a.idade[1])
    .map((atividade) => ({
      atividade,
      pista: PISTA_COMPLEMENTAR,
      ...pontuar(atividade, familia, idade, recentes),
    }))
    .sort((a, b) => b.pontos - a.pontos || a.atividade.id.localeCompare(b.atividade.id));
}

export function proporSessao(idx: IndiceConteudo, pedido: PedidoSessao): PropostaSessao {
  const { familia, crianca, idade, estados, historico, duracaoMin, foco, agora } = pedido;
  const recentes = atividadesRecentes(historico, crianca.id, agora);
  const todas = pistasDaCrianca(idx, familia, crianca);

  // 1. Pistas candidatas: o foco do pai, ou as menos trabalhadas nas últimas 2 semanas.
  let pistas: Pista[];
  if (foco === 'equilibrado') {
    const minutos = minutosPorLinha(idx, historico, crianca.id, agora);
    pistas = todas
      .map((p, ordem) => ({ p, ordem, min: minutos.get(p.linha.id) ?? 0 }))
      .sort((a, b) => a.min - b.min || a.ordem - b.ordem)
      .map((x) => x.p);
  } else {
    pistas = foco
      .map((id) => todas.find((p) => idPista(p) === id))
      .filter((p): p is Pista => p !== undefined);
  }

  // 2. Candidatas por pista, a partir dos marcos ativos.
  const filas: { pista: Pista; fila: Escolha[] }[] = [];
  const lacunas: Lacuna[] = [];
  for (const pista of pistas) {
    const pos = posicaoDaLinha(idx, pista, estados, idade, familia.vertentePrincipal);
    if (pos.ativos.length === 0) continue;
    const fila = candidatas(idx, pista, pos.ativos, familia, idade, recentes).map((e) => ({
      ...e,
      pista: idPista(pista),
    }));
    if (fila.length === 0) {
      lacunas.push({ pista: idPista(pista), nomeLinha: pista.linha.nome, marcos: pos.ativos });
    } else {
      filas.push({ pista, fila });
    }
  }

  // 3-4. Preenche a duração alternando entre as pistas (uma atividade por pista a cada rodada).
  const escolhas: Escolha[] = [];
  const usadas = new Set<string>();
  let minutos = 0;
  const limite = duracaoMin * FOLGA;
  let adicionou = true;
  while (adicionou) {
    adicionou = false;
    for (const { fila } of filas) {
      const proxima = fila.find((e) => !usadas.has(e.atividade.id));
      if (!proxima) continue;
      const cabe = minutos + proxima.atividade.duracaoMin <= limite;
      if (cabe || escolhas.length === 0) {
        escolhas.push(proxima);
        usadas.add(proxima.atividade.id);
        minutos += proxima.atividade.duracaoMin;
        adicionou = true;
      }
    }
  }

  // 5. No máximo uma complementar, só se couber na duração escolhida. Com linhas de foco
  // escolhidas à mão, a educadora pediu essas linhas: não acrescenta nada por conta própria.
  const comp =
    foco === 'equilibrado'
      ? complementares(idx, familia, idade, recentes).find(
          (e) => !usadas.has(e.atividade.id) && minutos + e.atividade.duracaoMin <= limite,
        )
      : undefined;
  if (comp) {
    escolhas.push(comp);
    minutos += comp.atividade.duracaoMin;
  }

  const avisos: string[] = [];
  if (escolhas.length > 0 && minutos > limite) {
    avisos.push(
      `A atividade sugerida tem ${minutos} min, mais do que os ${duracaoMin} min escolhidos. Você pode fazê-la em duas partes.`,
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
    escolhas.flatMap((e) => [...e.atividade.marcos, ...(e.atividade.revisa ?? [])]),
  );
  const candidatos = idx.conteudo.livros
    .filter((l) => l.marcos.some((m) => marcos.has(m)))
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
