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
import type { IndiceConteudo } from './conteudo';

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
  ativo: boolean;
  fronteira: boolean;
}

export interface PosicaoLinha {
  marcos: SituacaoMarco[];
  fronteira: string | null;
  ativos: string[];
  consolidados: number;
  total: number;
}

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
    const aguardando = marco.preRequisitos.filter(
      (p) => idx.marco(p) && estadoDe(estados, p) !== 'consolidado',
    );
    const intro = marco.idadeIntroducao[vertentePrincipal];
    return {
      marco,
      chave,
      estado: estadoDe(estados, chave),
      aguardando,
      avisoRitmo: intro !== undefined && intro > idade ? intro : null,
      ativo: false,
      fronteira: false,
    };
  });

  const iFronteira = situacoes.findIndex((s) => s.estado !== 'consolidado');
  const ativos: string[] = [];
  if (iFronteira >= 0) {
    const f = situacoes[iFronteira]!;
    f.fronteira = true;
    if (f.aguardando.length === 0) {
      f.ativo = true;
      ativos.push(f.marco.id);
      if (f.estado === 'em-desenvolvimento') {
        const prox = situacoes.slice(iFronteira + 1).find((s) => s.estado !== 'consolidado');
        if (prox && prox.aguardando.length === 0) {
          prox.ativo = true;
          ativos.push(prox.marco.id);
        }
      }
    }
  }

  return {
    marcos: situacoes,
    fronteira: iFronteira >= 0 ? situacoes[iFronteira]!.marco.id : null,
    ativos,
    consolidados: situacoes.filter((s) => s.estado === 'consolidado').length,
    total: situacoes.length,
  };
}

/**
 * "Posicionar aqui": o pai indica onde a criança está numa linha.
 * Todos os marcos anteriores viram consolidados e o escolhido fica em desenvolvimento.
 * Devolve só as mudanças, para o armazenamento gravar.
 */
export function posicionarAqui(
  idx: IndiceConteudo,
  pista: Pick<Pista, 'linha' | 'idioma'>,
  marcoId: string,
  agora: string,
): Record<string, RegistroMarco> {
  const marcos = marcosDaPista(idx, pista);
  const alvo = marcos.findIndex((m) => m.id === marcoId);
  if (alvo < 0) throw new Error(`Marco ${marcoId} não pertence à linha ${pista.linha.id}`);
  const mudancas: Record<string, RegistroMarco> = {};
  marcos.forEach((m, i) => {
    if (i > alvo) return;
    mudancas[chaveMarco(m.id, pista.idioma)] = {
      estado: i < alvo ? 'consolidado' : 'em-desenvolvimento',
      atualizadoEm: agora,
      origem: 'posicionamento',
    };
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
