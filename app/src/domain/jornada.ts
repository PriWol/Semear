// Regras da jornada (§5.1 a §5.3 da especificação). Funções puras.
import type {
  Crianca,
  Dominio,
  EstadoMarco,
  EstadosCrianca,
  Familia,
  Idioma,
  Linha,
  Marco,
  RegistroMarco,
} from './tipos';
import { linhaDoMarco, type IndiceConteudo } from './conteudo';

/** Chave do estado de um marco: no domínio de Línguas, o mesmo marco existe por idioma. */
export function chaveMarco(marcoId: string, idioma?: Idioma): string {
  return idioma ? `${marcoId}@${idioma}` : marcoId;
}

export function estadoDe(estados: EstadosCrianca, chave: string): EstadoMarco {
  return estados[chave]?.estado ?? 'nao-observado';
}

/** Vertentes que a família usa: a principal e as inspirações. */
export function vertentesDaFamilia(familia: Pick<Familia, 'vertentePrincipal' | 'inspiracoes'>) {
  return [familia.vertentePrincipal, ...familia.inspiracoes];
}

/** Linhas que aparecem para a família: as comuns e as extras das vertentes que ela usa. */
export function linhasVisiveis(
  dominio: Dominio,
  familia: Pick<Familia, 'vertentePrincipal' | 'inspiracoes'>,
): Linha[] {
  const usadas = vertentesDaFamilia(familia);
  return (dominio.linhas ?? []).filter(
    (l) => l.vertentes === null || l.vertentes.some((v) => usadas.includes(v)),
  );
}

/** Uma "pista" da jornada: uma linha, ou uma linha num idioma (domínio de Línguas). */
export interface Pista {
  linha: Linha;
  dominio: Dominio;
  idioma?: Idioma;
}

export function pistasDaCrianca(
  idx: IndiceConteudo,
  familia: Pick<Familia, 'vertentePrincipal' | 'inspiracoes'>,
  crianca: Pick<Crianca, 'trilhas'>,
): Pista[] {
  const pistas: Pista[] = [];
  for (const dominio of idx.conteudo.dominios) {
    if (!dominio.comJornada) continue;
    for (const linha of linhasVisiveis(dominio, familia)) {
      if (dominio.trilhas) {
        for (const idioma of crianca.trilhas) {
          if (!linha.idiomas || linha.idiomas.includes(idioma))
            pistas.push({ linha, dominio, idioma });
        }
      } else {
        pistas.push({ linha, dominio });
      }
    }
  }
  return pistas;
}

export function idPista(p: Pick<Pista, 'linha' | 'idioma'>): string {
  return p.idioma ? `${p.linha.id}@${p.idioma}` : p.linha.id;
}

export function marcosDaPista(idx: IndiceConteudo, pista: Pick<Pista, 'linha' | 'idioma'>) {
  return idx
    .marcosDaLinha(pista.linha.id)
    .filter((m) => !pista.idioma || !m.idiomas || m.idiomas.includes(pista.idioma));
}

export interface SituacaoMarco {
  marco: Marco;
  chave: string;
  estado: EstadoMarco;
  /** pré-requisitos (existentes no conteúdo) ainda não consolidados */
  aguardando: string[];
  /** idade de introdução da vertente principal, quando maior que a idade da criança */
  avisoRitmo: number | null;
  /** "trabalhando agora" num marco de idade típica muito acima da criança (D6): só avisa, não bloqueia */
  aindaCedo: boolean;
  ativo: boolean;
  fronteira: boolean;
}

export interface PosicaoLinha {
  marcos: SituacaoMarco[];
  fronteira: string | null;
  ativos: string[];
  consolidados: number;
  total: number;
  /** Só na sugestão (D6): a linha não tem registro e o ponto de partida veio da idade; nada é gravado. */
  provisoria?: boolean;
}

/** "Ainda cedo para esta linha": idade típica do marco ativo acima da idade da criança por mais que isto (D6). */
export const ANOS_AINDA_CEDO = 1.5;
/** Ponto de partida pela idade: prefere o último marco com idade típica até este tanto abaixo da idade (D6). */
export const ANOS_ABAIXO_PREFERIDO = 0.5;

/**
 * Posição numa linha (§5.1):
 * - fronteira = primeiro marco (na ordem) que não está consolidado;
 * - ativos = a fronteira, mais o marco seguinte se a fronteira já está em desenvolvimento (máx. 2);
 * - marcos com pré-requisito não consolidado ficam "aguardando" e não são ativos.
 */
export function posicaoDaLinha(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  estados: EstadosCrianca,
  idade: number,
  vertentePrincipal: Familia['vertentePrincipal'],
): PosicaoLinha {
  const marcos = marcosDaPista(idx, pista);
  const situacoes: SituacaoMarco[] = marcos.map((marco) => {
    const chave = chaveMarco(marco.id, pista.idioma);
    // Pré-requisitos da mesma linha não contam: a ordem da linha já garante a sequência.
    // Em Línguas, o pré-requisito de outra linha de Línguas é lido no mesmo idioma.
    const aguardando = marco.preRequisitos.filter((p) => {
      if (!idx.marco(p) || linhaDoMarco(p) === pista.linha.id) return false;
      const mesmoIdioma = pista.idioma && idx.dominioDaLinha(linhaDoMarco(p))?.trilhas;
      return estadoDe(estados, mesmoIdioma ? chaveMarco(p, pista.idioma) : p) !== 'consolidado';
    });
    const intro = marco.idadeIntroducao[vertentePrincipal];
    return {
      marco,
      chave,
      estado: estadoDe(estados, chave),
      aguardando,
      avisoRitmo: intro !== undefined && intro > idade ? intro : null,
      aindaCedo: false,
      ativo: false,
      fronteira: false,
    };
  });

  // O pai pode "forçar" um marco aguardando: marcá-lo em desenvolvimento o torna ativo (§5.1).
  const podeSerAtivo = (s: SituacaoMarco) =>
    s.aguardando.length === 0 || s.estado === 'em-desenvolvimento';

  const iFronteira = situacoes.findIndex((s) => s.estado !== 'consolidado');
  const ativos: string[] = [];
  if (iFronteira >= 0) {
    const f = situacoes[iFronteira]!;
    f.fronteira = true;
    if (podeSerAtivo(f)) {
      f.ativo = true;
      ativos.push(f.marco.id);
      if (f.estado === 'em-desenvolvimento') {
        const prox = situacoes.slice(iFronteira + 1).find((s) => s.estado !== 'consolidado');
        if (prox && podeSerAtivo(prox)) {
          prox.ativo = true;
          ativos.push(prox.marco.id);
        }
      }
    }
  }

  for (const s of situacoes) s.aindaCedo = s.ativo && s.marco.idadeTipica > idade + ANOS_AINDA_CEDO;

  return {
    marcos: situacoes,
    fronteira: iFronteira >= 0 ? situacoes[iFronteira]!.marco.id : null,
    ativos,
    consolidados: situacoes.filter((s) => s.estado === 'consolidado').length,
    total: situacoes.length,
  };
}

/**
 * Ponto de partida pela idade (§5.4, D6): o marco com `idadeTipica` mais próxima da idade da criança, errando
 * para o lado fácil. Se há marco com idade típica até meio ano ABAIXO da idade (ou igual a ela), vale o último
 * deles; senão vale o mais próximo, e no empate o mais fácil (o anterior).
 */
export function marcoDePartidaPelaIdade(marcos: Marco[], idade: number): Marco | null {
  const recentes = marcos.filter(
    (m) => m.idadeTipica <= idade && idade - m.idadeTipica <= ANOS_ABAIXO_PREFERIDO,
  );
  const ultimo = recentes[recentes.length - 1];
  if (ultimo) return ultimo;
  let melhor: Marco | null = null;
  for (const m of marcos) {
    if (!melhor || Math.abs(m.idadeTipica - idade) < Math.abs(melhor.idadeTipica - idade))
      melhor = m;
  }
  return melhor;
}

/** A criança não tem NENHUM registro nesta linha (nem "não observado" marcado de propósito). */
export function linhaSemRegistro(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  estados: EstadosCrianca,
): boolean {
  return marcosDaPista(idx, pista).every((m) => !estados[chaveMarco(m.id, pista.idioma)]);
}

/**
 * Posição para a SUGESTÃO de sessão (§5.4, D6). Igual a `posicaoDaLinha`, exceto numa linha sem nenhum
 * registro: aí parte do marco típico da idade, como se os anteriores estivessem consolidados. É só um
 * cálculo em memória (`provisoria: true`): nada é gravado e a jornada continua mostrando "próximo" no
 * primeiro marco até a família posicionar a criança.
 */
export function posicaoParaSugestao(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  estados: EstadosCrianca,
  idade: number,
  vertentePrincipal: Familia['vertentePrincipal'],
): PosicaoLinha {
  const marcos = marcosDaPista(idx, pista);
  const partida = linhaSemRegistro(idx, pista, estados)
    ? marcoDePartidaPelaIdade(marcos, idade)
    : null;
  if (!partida) return posicaoDaLinha(idx, pista, estados, idade, vertentePrincipal);
  const virtual: EstadosCrianca = { ...estados };
  for (const m of marcos) {
    if (m.id === partida.id) break;
    virtual[chaveMarco(m.id, pista.idioma)] = {
      estado: 'consolidado',
      atualizadoEm: '',
      origem: 'posicionamento',
    };
  }
  return { ...posicaoDaLinha(idx, pista, virtual, idade, vertentePrincipal), provisoria: true };
}

/**
 * "Posicionar aqui": o pai indica onde a criança está numa linha.
 * Os anteriores viram consolidados, o escolhido fica em desenvolvimento e os posteriores que tinham
 * registro voltam a "não observado" (senão a tela e a sugestão de sessão discordariam).
 * Devolve só as mudanças, para o armazenamento gravar.
 */
export function posicionarAqui(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  marcoId: string,
  estados: EstadosCrianca,
  agora: string,
): Record<string, RegistroMarco> {
  const marcos = marcosDaPista(idx, pista);
  const alvo = marcos.findIndex((m) => m.id === marcoId);
  if (alvo < 0) throw new Error(`Marco ${marcoId} não pertence à linha ${pista.linha.id}`);
  const mudancas: Record<string, RegistroMarco> = {};
  marcos.forEach((m, i) => {
    const chave = chaveMarco(m.id, pista.idioma);
    let estado: EstadoMarco;
    if (i < alvo) estado = 'consolidado';
    else if (i === alvo) estado = 'em-desenvolvimento';
    else if (estadoDe(estados, chave) !== 'nao-observado') estado = 'nao-observado';
    else return;
    mudancas[chave] = { estado, atualizadoEm: agora, origem: 'posicionamento' };
  });
  return mudancas;
}

/** Avisos sobre as trilhas de língua de uma criança (§3, regras das trilhas). */
export function avisosTrilhas(
  idx: IndiceConteudo,
  crianca: Pick<Crianca, 'trilhas'>,
  idade: number,
  estados: EstadosCrianca,
): string[] {
  const li = idx.conteudo.dominios.find((d) => d.trilhas);
  if (!li?.trilhas) return [];
  const avisos: string[] = [];
  const max = li.maxTrilhasAtivas ?? Infinity;
  if (crianca.trilhas.length > max) {
    avisos.push(
      `Mais de ${max} línguas ao mesmo tempo costuma diluir o progresso. Você pode manter, mas considere focar.`,
    );
  }
  for (const id of crianca.trilhas) {
    const t = li.trilhas.find((x) => x.id === id);
    if (!t) continue;
    if (idade < t.idadeInicio)
      avisos.push(`${t.nome} costuma começar por volta dos ${t.idadeInicio} anos.`);
    const pendentes = (t.preRequisitos ?? []).filter(
      (p) => idx.marco(p) && estadoDe(estados, p) === 'nao-observado',
    );
    if (pendentes.length) {
      avisos.push(
        `${t.nome}: o ideal é começar quando a leitura em português já estiver em andamento (${pendentes.join(', ')}).`,
      );
    }
  }
  return avisos;
}
