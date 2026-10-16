// Índice e validação do conteúdo curado. Funções puras: recebem o conteúdo já carregado.
import {
  VERTENTES,
  type Atividade,
  type Conteudo,
  type Dominio,
  type Folha,
  type Linha,
  type Livro,
  type Marco,
  type OrientacaoPais,
  type Referencia,
} from './tipos';

export interface IndiceConteudo {
  conteudo: Conteudo;
  dominio(id: string): Dominio | undefined;
  linha(id: string): Linha | undefined;
  dominioDaLinha(linhaId: string): Dominio | undefined;
  marco(id: string): Marco | undefined;
  /** marcos da linha, em ordem */
  marcosDaLinha(linhaId: string): Marco[];
  atividade(id: string): Atividade | undefined;
  /** atividades publicadas que trabalham o marco (como principal) */
  atividadesDoMarco(marcoId: string): Atividade[];
  /** atividades complementares publicadas (sem marcos; §3.0) */
  complementares(): Atividade[];
  /** atividades publicadas cujos marcos principais estão na linha */
  atividadesDaLinha(linhaId: string): Atividade[];
  livro(id: string): Livro | undefined;
  referencia(id: string): Referencia | undefined;
}

export function linhaDoMarco(marcoId: string): string {
  return marcoId.split('.').slice(0, 2).join('.');
}

export function criarIndice(conteudo: Conteudo): IndiceConteudo {
  const dominios = new Map(conteudo.dominios.map((d) => [d.id, d]));
  const linhas = new Map<string, Linha>();
  const dominioPorLinha = new Map<string, Dominio>();
  for (const d of conteudo.dominios) {
    for (const l of d.linhas ?? []) {
      linhas.set(l.id, l);
      dominioPorLinha.set(l.id, d);
    }
  }
  const marcos = new Map(conteudo.marcos.map((m) => [m.id, m]));
  const marcosPorLinha = new Map<string, Marco[]>();
  for (const m of conteudo.marcos) {
    const lista = marcosPorLinha.get(m.linha) ?? [];
    lista.push(m);
    marcosPorLinha.set(m.linha, lista);
  }
  for (const lista of marcosPorLinha.values()) lista.sort((a, b) => a.ordem - b.ordem);

  const publicadas = conteudo.atividades.filter((a) => a.autoria.status === 'publicado');
  const atividades = new Map(conteudo.atividades.map((a) => [a.id, a]));
  const livros = new Map(conteudo.livros.map((l) => [l.id, l]));
  const referencias = new Map(conteudo.referencias.map((r) => [r.id, r]));

  return {
    conteudo,
    dominio: (id) => dominios.get(id),
    linha: (id) => linhas.get(id),
    dominioDaLinha: (id) => dominioPorLinha.get(id),
    marco: (id) => marcos.get(id),
    marcosDaLinha: (id) => marcosPorLinha.get(id) ?? [],
    atividade: (id) => atividades.get(id),
    atividadesDoMarco: (marcoId) => publicadas.filter((a) => a.marcos.includes(marcoId)),
    complementares: () => publicadas.filter((a) => a.marcos.length === 0),
    atividadesDaLinha: (linhaId) =>
      publicadas.filter((a) => a.marcos.some((m) => linhaDoMarco(m) === linhaId)),
    livro: (id) => livros.get(id),
    referencia: (id) => referencias.get(id),
  };
}

// ---------- Validação ----------

export interface ResultadoValidacao {
  /** problemas que quebram o app: precisam ser corrigidos antes de publicar */
  erros: string[];
  /** conteúdo incompleto, mas utilizável (ex.: pré-requisito ainda não escrito) */
  avisos: string[];
}

const TIPOS_FOLHA: Folha['tipo'][] = [
  'ligar',
  'marcar',
  'cartas',
  'desenho',
  'contar',
  'quadro-dez',
  'comparar',
];

/** Atividade sem marcos só vale como complementar: domínio sem jornada e categoria conhecida. */
function validarComplementar(a: Atividade, idx: IndiceConteudo, erros: string[]): void {
  const dominio = a.dominio ? idx.dominio(a.dominio) : undefined;
  if (!dominio || dominio.comJornada) {
    erros.push(
      `Atividade ${a.id}: sem marco, precisa de "dominio" de um domínio sem jornada (complementar)`,
    );
  } else if (!a.categoria || !dominio.categorias?.includes(a.categoria)) {
    erros.push(`Atividade ${a.id}: categoria "${a.categoria ?? ''}" não existe em ${dominio.id}`);
  }
}

const CAMPOS_DA_ORIENTACAO = ['porQueImporta', 'comoParticipar', 'sinaisDeAtencao'] as const;

/** Orientação para os pais: texto preenchido, vertentes conhecidas e referências que existem. */
function validarOrientacao(
  m: Marco,
  o: OrientacaoPais,
  idx: IndiceConteudo,
  erros: string[],
): void {
  for (const campo of CAMPOS_DA_ORIENTACAO) {
    if (typeof o[campo] !== 'string' || o[campo].trim() === '')
      erros.push(`Marco ${m.id}: orientação para os pais com "${campo}" vazio`);
  }
  const citadas = [...(o.referencias ?? [])];
  for (const [vertente, texto] of Object.entries(o.porVertente ?? {})) {
    if (!(VERTENTES as readonly string[]).includes(vertente)) {
      erros.push(`Marco ${m.id}: vertente "${vertente}" desconhecida na orientação para os pais`);
      continue;
    }
    if (!texto.comoParticipar?.trim())
      erros.push(`Marco ${m.id}: texto da vertente ${vertente} com "comoParticipar" vazio`);
    citadas.push(...(texto.referencias ?? []));
  }
  for (const id of new Set(citadas)) {
    if (!idx.referencia(id)) erros.push(`Marco ${m.id}: referência "${id}" não existe no catálogo`);
  }
}

/** Dado de fora: confere o formato antes de usar. O link vira `href`, então só aceita https. */
function validarReferencia(r: Referencia, erros: string[]): void {
  const vazio = (t: unknown) => typeof t !== 'string' || t.trim() === '';
  if (vazio(r.autores) || vazio(r.titulo) || vazio(r.veiculo))
    erros.push(`Referência ${r.id}: autores, título e veículo são obrigatórios`);
  else if (!Number.isInteger(r.ano) || r.ano < 1000 || r.ano > 2100)
    erros.push(`Referência ${r.id}: ano inválido`);
  else if (r.link !== undefined && !/^https:\/\/\S+$/.test(r.link))
    erros.push(`Referência ${r.id}: o link precisa começar com https://`);
}

export function validarConteudo(conteudo: Conteudo): ResultadoValidacao {
  const erros: string[] = [];
  const avisos: string[] = [];
  const idx = criarIndice(conteudo);

  const vistos = new Set<string>();
  const unico = (id: string, tipo: string) => {
    if (vistos.has(id)) erros.push(`${tipo} com id repetido: ${id}`);
    vistos.add(id);
  };

  for (const d of conteudo.dominios) {
    unico(d.id, 'Domínio');
    for (const l of d.linhas ?? []) {
      unico(l.id, 'Linha');
      if (!l.id.startsWith(`${d.id}.`))
        erros.push(`Linha ${l.id} não começa com o domínio ${d.id}`);
    }
    for (const t of d.trilhas ?? []) {
      for (const p of t.preRequisitos ?? []) {
        if (!idx.marco(p)) avisos.push(`Trilha ${t.id}: pré-requisito ${p} ainda não existe`);
      }
    }
  }

  // O catálogo tem seu próprio espaço de ids (não concorre com marcos nem atividades).
  const idsDeReferencia = new Set<string>();
  for (const r of conteudo.referencias) {
    if (idsDeReferencia.has(r.id)) erros.push(`Referência com id repetido: ${r.id}`);
    idsDeReferencia.add(r.id);
    validarReferencia(r, erros);
  }

  const ordensPorLinha = new Map<string, Set<number>>();
  for (const m of conteudo.marcos) {
    unico(m.id, 'Marco');
    const linha = idx.linha(m.linha);
    if (!linha) {
      erros.push(`Marco ${m.id}: linha ${m.linha} não existe`);
      continue;
    }
    if (!m.id.startsWith(`${m.linha}.`))
      erros.push(`Marco ${m.id} não começa com a linha ${m.linha}`);
    if (!idx.dominioDaLinha(m.linha)?.comJornada) {
      avisos.push(`Marco ${m.id}: o domínio da linha ${m.linha} ainda não tem jornada`);
    }
    const ordens = ordensPorLinha.get(m.linha) ?? new Set<number>();
    if (ordens.has(m.ordem)) erros.push(`Linha ${m.linha}: ordem ${m.ordem} repetida (${m.id})`);
    ordens.add(m.ordem);
    ordensPorLinha.set(m.linha, ordens);
    // Dado de fora: o JSON pode não ter o campo, apesar do tipo.
    const orientacao = m.orientacaoPais as OrientacaoPais | undefined;
    if (orientacao) validarOrientacao(m, orientacao, idx, erros);
    else erros.push(`Marco ${m.id}: falta a orientação para os pais (obrigatória em todo marco)`);
    for (const p of m.preRequisitos) {
      if (p === m.id) erros.push(`Marco ${m.id} é pré-requisito de si mesmo`);
      else if (!idx.marco(p)) avisos.push(`Marco ${m.id}: pré-requisito ${p} ainda não existe`);
    }
  }

  for (const a of conteudo.atividades) {
    unico(a.id, 'Atividade');
    if (a.marcos.length === 0) validarComplementar(a, idx, erros);
    if (a.materialImpresso) {
      // Dado de fora: confere o formato antes de usar (nunca lança, sempre reporta).
      const { volume, unidade, paginas } = a.materialImpresso;
      const inteiro = (n: unknown): n is number => Number.isInteger(n) && (n as number) >= 1;
      if (!inteiro(volume) || !inteiro(unidade))
        erros.push(`Atividade ${a.id}: material impresso com volume ou unidade inválidos`);
      else if (
        !Array.isArray(paginas) ||
        paginas.length !== 2 ||
        !inteiro(paginas[0]) ||
        !inteiro(paginas[1]) ||
        paginas[1] < paginas[0]
      )
        erros.push(`Atividade ${a.id}: material impresso com páginas inválidas`);
    }
    for (const m of [...a.marcos, ...(a.revisa ?? [])]) {
      if (!idx.marco(m)) erros.push(`Atividade ${a.id}: marco ${m} não existe`);
    }
    if (a.idade[0] > a.idade[1]) erros.push(`Atividade ${a.id}: faixa de idade invertida`);
    if (a.duracaoMin <= 0) erros.push(`Atividade ${a.id}: duração precisa ser maior que zero`);
    if (a.folhas.length === 0) avisos.push(`Atividade ${a.id}: não tem folhas para a criança`);
    a.folhas.forEach((f, i) => {
      const onde = `Atividade ${a.id}, folha ${i + 1}`;
      if (!TIPOS_FOLHA.includes(f.tipo)) {
        erros.push(`${onde}: tipo de folha desconhecido "${(f as { tipo: string }).tipo}"`);
        return;
      }
      if (f.tipo === 'contar') {
        for (const item of f.itens) {
          if (!item.opcoes.includes(item.quantidade)) {
            erros.push(
              `${onde}: as opções de ${item.emoji} não incluem a resposta ${item.quantidade}`,
            );
          }
        }
      }
      if (f.tipo === 'quadro-dez' || f.tipo === 'cartas') {
        const numeros =
          f.tipo === 'quadro-dez'
            ? f.numeros
            : f.cartas.flatMap((c) => ('quadroDez' in c ? [c.quadroDez] : []));
        for (const n of numeros) {
          if (n < 0 || n > 20)
            erros.push(`${onde}: quadro de dez só representa de 0 a 20 (recebeu ${n})`);
        }
      }
      if (f.tipo === 'cartas' && f.cartas.length > 12) {
        avisos.push(`${onde}: mais de 12 cartas não cabem em uma página`);
      }
    });
    if (a.autoria.status !== 'publicado') {
      avisos.push(`Atividade ${a.id}: status "${a.autoria.status}" (não aparece para as famílias)`);
    }
  }

  for (const l of conteudo.livros) {
    unico(l.id, 'Livro');
    for (const m of l.marcos) {
      if (!idx.marco(m)) avisos.push(`Livro ${l.id}: marco ${m} ainda não existe`);
    }
  }

  return { erros, avisos };
}
