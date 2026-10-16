// Carrega o conteúdo curado de app/content (embutido no build pelo Vite; ADR 0005).
import type { Atividade, Conteudo, Dominio, Livro, Marco, Referencia } from './domain/tipos';
import { criarIndice, type IndiceConteudo } from './domain/conteudo';
import dominiosJson from '../content/dominios.json';
import livrosJson from '../content/livros.json';
import referenciasJson from '../content/referencias.json';

const arquivosMarcos = import.meta.glob<{ marcos: Marco[] }>('../content/marcos/*.json', {
  eager: true,
  import: 'default',
});
const arquivosAtividades = import.meta.glob<Atividade>('../content/atividades/*.json', {
  eager: true,
  import: 'default',
});

export function carregarConteudo(): Conteudo {
  return {
    dominios: (dominiosJson as { dominios: Dominio[] }).dominios,
    marcos: Object.values(arquivosMarcos).flatMap((a) => a.marcos),
    atividades: Object.values(arquivosAtividades),
    livros: (livrosJson as { livros: Livro[] }).livros,
    referencias: (referenciasJson as { referencias: Referencia[] }).referencias,
  };
}

let indice: IndiceConteudo | null = null;
export function conteudo(): IndiceConteudo {
  indice ??= criarIndice(carregarConteudo());
  return indice;
}
