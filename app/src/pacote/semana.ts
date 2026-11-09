// Documento único com todas as sessões da semana (#9, ADR 0004): mesma CSP e CSS do pacote de sessão.
import type { Crianca } from '../domain/tipos';
import { dataBR } from '../domain/datas';
import { NOME_DIA, type DiaPlano, type MaterialDaSemana, type PlanoSemana } from '../domain/semana';
import { html, type HtmlSeguro } from '../ui/html';
import { montarDocumento, paginasDaSessao, type EntradaPacote } from './gerar';

/** O que imprimir: tudo, só as folhas da criança ou só os roteiros (e fichas) do educador. */
export type ModoSemana = 'tudo' | 'folhas' | 'roteiros';

export interface DiaParaImprimir {
  dia: DiaPlano;
  entrada: EntradaPacote;
}

export interface EntradaSemana {
  crianca: Crianca;
  plano: PlanoSemana;
  dias: DiaParaImprimir[];
  materiais: MaterialDaSemana[];
  modo: ModoSemana;
}

function paginaMateriaisDaSemana(e: EntradaSemana): HtmlSeguro {
  return html`<section class="pagina educador">
    <span class="etiqueta">Prepare antes · semana toda</span>
    <h1>Materiais da semana</h1>
    <p>Separe tudo de uma vez. Ao lado de cada item, os dias em que ele é usado.</p>
    <ul class="check">
      ${e.materiais.map(
        (m) =>
          html`<li>
            ${m.item}${m.deCasa ? html` <b>(de casa)</b>` : ''}
            <span class="nota">· ${m.dias.map((d) => NOME_DIA[d]).join(', ')}</span>
          </li>`,
      )}
      <li>Ficha de registro de cada sessão e uma caneta</li>
    </ul>
  </section>`;
}

function separadorDoDia({ dia, entrada }: DiaParaImprimir): HtmlSeguro {
  return html`<section class="pagina educador">
    <span class="etiqueta">${NOME_DIA[dia.dia]} · ${dataBR(`${dia.data}T12:00:00`)}</span>
    <h1>${NOME_DIA[dia.dia]} · Sessão ${entrada.sessao.codigo}</h1>
    <ul>
      ${entrada.atividades.map((a) => html`<li>${a.titulo} (${a.duracaoMin} min)</li>`)}
    </ul>
  </section>`;
}

export function gerarSemana(e: EntradaSemana): string {
  const partes = e.dias.flatMap((d) => {
    if (d.entrada.atividades.length === 0) return [];
    const p = paginasDaSessao(d.entrada);
    const educador = e.modo !== 'folhas';
    const crianca = e.modo !== 'roteiros';
    const { dia } = d;
    return [
      educador ? separadorDoDia(d) : '',
      educador ? p.roteiro : '',
      crianca ? html`<div class="dia-bloco" data-dia="${dia.dia}">${p.folhas}</div>` : [],
      educador ? p.ficha : '',
    ];
  });
  const corpo = html`${e.modo === 'folhas' ? '' : paginaMateriaisDaSemana(e)}${partes}`;
  const titulo = `Semear · semana de ${dataBR(`${e.plano.inicio}T12:00:00`)} · ${e.crianca.nome}`;
  // No modo tablet, o seletor mostra as folhas de um dia por vez (#9: navegação por dia).
  const diasComFolhas = e.dias.filter((d) => d.entrada.atividades.length > 0);
  const seletor =
    e.modo !== 'roteiros' && diasComFolhas.length > 0
      ? html`<label
          >Dia no tablet:
          <select onchange="mostrarDia(this.value)">
            <option value="todos">Todos os dias</option>
            ${diasComFolhas.map((d) => html`<option value="${d.dia.dia}">${NOME_DIA[d.dia.dia]}</option>`)}
          </select></label
        >`
      : '';
  return montarDocumento(titulo, e.dias[0]?.entrada.letra ?? 'bastao', corpo, seletor);
}

/** semear-semana-<criança>-<data>.html */
export function nomeArquivoSemana(plano: PlanoSemana, crianca: Crianca): string {
  const nome = crianca.nome
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // remove acentos antes de limpar o resto
    .replace(/[^A-Za-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .toLowerCase();
  return `semear-semana-${nome || 'crianca'}-${plano.inicio}.html`;
}
