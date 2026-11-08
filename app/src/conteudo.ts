// Carrega o conteúdo curado de app/content (embutido no build pelo Vite; ADR 0005).
import type {
  Atividade,
  Conteudo,
  Dominio,
  ItemAcervo,
  Livro,
  Marco,
  Referencia,
} from './domain/tipos';
import { estaPublicavel } from './domain/revisao';
import { criarIndice, type IndiceConteudo } from './domain/conteudo';
import dominiosJson from '../content/dominios.json';
import livrosJson from '../content/livros.json';
import acervoJson from '../content/acervo.json';
import referenciasJson from '../content/referencias.json';

const arquivosMarcos = import.meta.glob<{ marcos: Marco[] }>('../content/marcos/*.json', {
  eager: true,
  import: 'default',
});
const arquivosAtividades = import.meta.glob<Atividade>('../content/atividades/*.json', {
  eager: true,
  import: 'default',
});

/** Tudo o que está nos JSON, inclusive rascunhos: é o que a validação precisa conferir. */
export function carregarConteudoBruto(): Conteudo {
  return {
    dominios: (dominiosJson as { dominios: Dominio[] }).dominios,
    marcos: Object.values(arquivosMarcos).flatMap((a) => a.marcos),
    atividades: Object.values(arquivosAtividades),
    livros: (livrosJson as { livros: Livro[] }).livros,
    acervo: (acervoJson as { itens: ItemAcervo[] }).itens,
    referencias: (referenciasJson as { referencias: Referencia[] }).referencias,
  };
}

/** Só o conteúdo aprovado (ou anterior à #77, sem revisão) chega às famílias. */
export function publicavel(c: Conteudo): Conteudo {
  return {
    ...c,
    marcos: c.marcos.filter(estaPublicavel),
    atividades: c.atividades.filter(estaPublicavel),
    livros: c.livros.filter(estaPublicavel),
  };
}

export function carregarConteudo(): Conteudo {
  return publicavel(carregarConteudoBruto());
}

let indice: IndiceConteudo | null = null;
export function conteudo(): IndiceConteudo {
  indice ??= criarIndice(carregarConteudo());
  return indice;
}
