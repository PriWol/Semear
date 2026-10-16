import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { buscarAcervo } from '../domain/acervo';
import type { IdiomaAcervo, ItemAcervo } from '../domain/tipos';

const IDIOMAS: Record<IdiomaAcervo, string> = {
  pt: 'Português',
  en: 'Inglês',
  la: 'Latim',
  fr: 'Francês',
};

function cartaoItem(i: ItemAcervo) {
  return html`<li class="cartao item-acervo">
    <h3>${i.titulo}</h3>
    <p class="nota">
      ${i.autor} · ${IDIOMAS[i.idioma]} · ${i.idade[0]}–${i.idade[1]} anos · ${i.fonte} · ${i.licenca}
    </p>
    <p>${i.sobre}</p>
    <a class="botao" href="${i.url}" target="_blank" rel="noopener noreferrer"
      >${i.tipoLink === 'obra' ? 'Abrir o livro' : 'Buscar nesta fonte'}</a
    >
  </li>`;
}

/** Acervo gratuito: catálogo curado, com busca no aparelho. Os links só abrem quando a pessoa clica (ADR 0016). */
export const paginaAcervo: FabricaPagina = async (ctx) => {
  const itens = ctx.idx.conteudo.acervo;
  const lista = (texto: string, idioma: IdiomaAcervo | '', idade: number | null) => {
    const achados = buscarAcervo(itens, { texto, idioma, idade });
    return achados.length
      ? html`<ul class="lista-acervo">
          ${achados.map(cartaoItem)}
        </ul>`
      : html`<p class="nota">Nenhuma obra encontrada. Tente outro termo ou limpe os filtros.</p>`;
  };

  return {
    titulo: 'Acervo gratuito',
    conteudo: html`<h1>Acervo gratuito</h1>
      <p class="nota">
        ${itens.length} obras de domínio público ou licença aberta, em português, inglês, latim e
        francês. A busca acontece neste aparelho; os links abrem o site de cada fonte.
      </p>
      <form class="cartao" id="filtros" role="search">
        <label>Buscar <input type="search" id="busca-texto" placeholder="título, autor ou tema" /></label>
        <label
          >Idioma
          <select id="busca-idioma">
            <option value="">Todos</option>
            ${(Object.keys(IDIOMAS) as IdiomaAcervo[]).map(
              (k) => html`<option value="${k}">${IDIOMAS[k]}</option>`,
            )}
          </select>
        </label>
        <label
          >Idade
          <select id="busca-idade">
            <option value="">Todas</option>
            ${[2, 3, 4, 5, 6, 7, 8].map((n) => html`<option value="${n}">${n} anos</option>`)}
          </select>
        </label>
      </form>
      <div id="resultado" aria-live="polite">${lista('', '', null)}</div>`,
    montar(raiz) {
      const texto = raiz.querySelector<HTMLInputElement>('#busca-texto');
      const idioma = raiz.querySelector<HTMLSelectElement>('#busca-idioma');
      const idade = raiz.querySelector<HTMLSelectElement>('#busca-idade');
      const resultado = raiz.querySelector<HTMLElement>('#resultado');
      const atualizar = () => {
        if (!texto || !idioma || !idade || !resultado) return;
        resultado.innerHTML = lista(
          texto.value,
          idioma.value as IdiomaAcervo | '',
          idade.value ? Number(idade.value) : null,
        ).valor;
      };
      raiz.querySelector('#filtros')?.addEventListener('submit', (e) => e.preventDefault());
      for (const el of [texto, idioma, idade]) el?.addEventListener('input', atualizar);
    },
  };
};
