import type { FabricaPagina } from '../ui/app';
import { lerFormulario } from '../ui/app';
import { html, type HtmlSeguro } from '../ui/html';
import { icone } from '../ui/icones';
import { idadeEmAnos } from '../domain/datas';
import { marcosVisiveis } from '../domain/conteudo';
import { buscarAtividades, dominioDaAtividade } from '../domain/busca';
import {
  TAMANHO_PAGINA,
  fatiarPagina,
  mostrarLimparFiltros,
  proximoLote,
  textoContagem,
} from '../domain/paginacao';
import { imprimirAtividadeAvulsa } from './sessao-avulsa';
import { VERTENTES, type Atividade, type Vertente } from '../domain/tipos';

const DURACOES_MAX = [10, 20, 30, 40, 60];
const CHAVE_FILTROS = 'semear:filtros-atividades';
const IDADES = [2, 3, 4, 5, 6, 7, 8]; // faixa do app (2 a 8 anos)

/**
 * Atividades avulsas (#13): busca uma atividade e imprime só ela, para reforçar uma área fora da
 * sessão planejada. A sessão avulsa entra no histórico como as demais.
 */
export const paginaAtividades: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  const criancas = await ctx.repo.criancas();
  const crianca = criancas.find((c) => c.id === params.crianca) ?? criancas[0] ?? null;
  const publicadas = ctx.idx.conteudo.atividades.filter((a) => a.autoria.status === 'publicado');
  const dominios = ctx.idx.conteudo.dominios.filter((d) =>
    publicadas.some((a) => dominioDaAtividade(a, ctx.idx) === d.id),
  );

  /** Título do marco principal e "+N" (QA3); o código curto só no title. A ficha impressa mantém o código (§5.7). */
  const marcosDoCartao = (a: Atividade): HtmlSeguro | '' => {
    const ids = marcosVisiveis(ctx.idx, a);
    const principal = ids[0];
    if (!principal) return '';
    const titulo = ctx.idx.marco(principal)?.titulo ?? '';
    const mais = ids.length > 1 ? ` +${ids.length - 1}` : '';
    return html`· <span class="marco-cartao" title="${ids.join(', ')}">${titulo}${mais}</span>`;
  };

  const cartao = (a: Atividade): HtmlSeguro => {
    const folha = a.folhas[0];
    return html`<li class="cartao" data-atividade="${a.id}">
      <h2><a href="#/atividade/${a.id}">${a.titulo}</a></h2>
      <p class="nota">
        ${a.duracaoMin} min · ${a.idade[0]} a ${a.idade[1]} anos
        ${marcosDoCartao(a)}
      </p>
      <p>${a.objetivo.replace(/\*+/g, '')}</p>
      ${folha ? html`<p class="nota">Primeira folha: ${folha.titulo}</p>` : ''}
      <button class="botao primario" type="button" data-imprimir="${a.id}"
        ${crianca ? '' : 'disabled'}>
        ${icone('printer')} Imprimir esta atividade
      </button>
    </li>`;
  };
  const cartoes = (itens: Atividade[]): string => itens.map((a) => cartao(a).valor).join('');

  return {
    titulo: 'Atividades',
    conteudo: html`
      <h1>Atividades</h1>
      <p class="nota">
        Procure uma atividade e imprima só ela, para reforçar uma área fora da sessão planejada.
      </p>
      ${
        !familia || !crianca
          ? html`<p class="alerta">
              Cadastre uma criança para imprimir. <a href="#/familia">Começar</a>
            </p>`
          : ''
      }
      <form class="cartao formulario" id="filtros-atividades" role="search">
        <label>Buscar <input type="search" name="texto" placeholder="título, objetivo, marco ou tema" /></label>
        ${
          criancas.length > 1
            ? html`<label
                >Para quem imprimir
                <select name="crianca">
                  ${criancas.map(
                    (c) =>
                      html`<option value="${c.id}" ${c.id === crianca?.id ? 'selected' : ''}>${c.nome}</option>`,
                  )}
                </select></label
              >`
            : ''
        }
        <label
          >Área
          <select name="dominio">
            <option value="">Todas</option>
            ${dominios.map((d) => html`<option value="${d.id}">${d.nome}</option>`)}
          </select></label
        >
        <label
          >Vertente
          <select name="vertente">
            <option value="">Todas</option>
            ${VERTENTES.map((v) => html`<option value="${v}">${v}</option>`)}
          </select></label
        >
        <label
          >Duração
          <select name="duracao">
            <option value="">Qualquer</option>
            ${DURACOES_MAX.map((d) => html`<option value="${d}">até ${d} min</option>`)}
          </select></label
        >
        <label
          >Idade
          <select name="idade">
            <option value="">Qualquer</option>
            ${crianca ? html`<option value="crianca">Idade de ${crianca.nome}</option>` : ''}
            ${IDADES.map((i) => html`<option value="${i}">${i} anos</option>`)}
          </select></label
        >
      </form>
      <p id="contagem-atividades" class="nota" role="status" aria-live="polite"></p>
      <button class="link-botao" type="button" id="limpar-filtros" hidden>Limpar filtros</button>
      <div id="resultado-atividades"></div>
      <button class="botao" type="button" id="ver-mais" hidden></button>
    `,
    montar(raiz) {
      const form = raiz.querySelector<HTMLFormElement>('#filtros-atividades');
      const resultado = raiz.querySelector<HTMLElement>('#resultado-atividades');
      const contagem = raiz.querySelector<HTMLElement>('#contagem-atividades');
      const limpar = raiz.querySelector<HTMLButtonElement>('#limpar-filtros');
      const verMais = raiz.querySelector<HTMLButtonElement>('#ver-mais');
      if (!form || !resultado || !contagem || !limpar || !verMais) return;
      form.addEventListener('submit', (ev) => ev.preventDefault());

      const campo = (n: string) => form.elements.namedItem(n) as HTMLInputElement | null;
      const escolhida = () => criancas.find((c) => c.id === campo('crianca')?.value) ?? crianca;

      // Resultado completo da busca atual e quantos já aparecem (#130): muda busca/filtro, volta a 20.
      let achadas: Atividade[] = [];
      let mostrando = TAMANHO_PAGINA;

      const valoresFiltro = () => ({
        texto: campo('texto')?.value ?? '',
        dominio: campo('dominio')?.value ?? '',
        vertente: campo('vertente')?.value ?? '',
        duracao: campo('duracao')?.value ?? '',
        idade: campo('idade')?.value ?? '',
      });

      const atualizarRodape = () => {
        contagem.textContent = textoContagem(achadas.length, mostrando);
        limpar.hidden = !mostrarLimparFiltros(valoresFiltro());
        const lote = proximoLote(achadas.length, mostrando);
        verMais.hidden = lote === 0;
        verMais.textContent = `Ver mais ${lote}`;
      };

      const atualizar = () => {
        const alvo = escolhida();
        // "Idade de <criança>" usa a idade atual dela; os números escolhem uma idade qualquer (2 a 8).
        const escolhaIdade = campo('idade')?.value ?? '';
        const idade =
          escolhaIdade === 'crianca'
            ? alvo
              ? Math.floor(idadeEmAnos(alvo.nascimento, new Date(ctx.agora())))
              : undefined
            : escolhaIdade
              ? Number(escolhaIdade)
              : undefined;
        achadas = buscarAtividades(
          publicadas,
          {
            texto: campo('texto')?.value ?? '',
            dominio: campo('dominio')?.value || undefined,
            vertente: (campo('vertente')?.value || undefined) as Vertente | undefined,
            duracaoMax: campo('duracao')?.value ? Number(campo('duracao')?.value) : undefined,
            idade,
          },
          ctx.idx,
        ).map((r) => r.atividade);
        mostrando = TAMANHO_PAGINA;
        resultado.innerHTML =
          achadas.length === 0
            ? html`<p class="nota">
                Nenhuma atividade encontrada. Tente outra palavra ou tire um filtro.
              </p>`.valor
            : `<ul class="lista-atividades">${cartoes(fatiarPagina(achadas, mostrando))}</ul>`;
        atualizarRodape();
      };

      const guardarFiltros = () => {
        try {
          sessionStorage.setItem(CHAVE_FILTROS, JSON.stringify(lerFormulario(form)));
        } catch {
          /* sem armazenamento: só não lembra */
        }
      };

      // "Ver mais" acrescenta ao fim da lista, sem redesenhar o que já está na tela (o foco não se perde).
      verMais.addEventListener('click', () => {
        const lista = resultado.querySelector('ul');
        if (!lista) return;
        const antes = mostrando;
        mostrando += proximoLote(achadas.length, mostrando);
        lista.insertAdjacentHTML('beforeend', cartoes(achadas.slice(antes, mostrando)));
        atualizarRodape();
      });

      limpar.addEventListener('click', () => {
        for (const nome of ['texto', 'dominio', 'vertente', 'duracao', 'idade']) {
          const el = campo(nome);
          if (el) el.value = '';
        }
        atualizar();
        guardarFiltros();
        campo('texto')?.focus();
      });
      // Filtros guardados na sessão do navegador: ao voltar da página de uma atividade, a busca continua.
      // Nada sai do aparelho; se o armazenamento falhar, a lista só abre sem filtros.
      try {
        const salvo = JSON.parse(sessionStorage.getItem(CHAVE_FILTROS) ?? '{}') as Record<
          string,
          unknown
        >;
        for (const [nome, valor] of Object.entries(salvo)) {
          const el = campo(nome);
          if (el && typeof valor === 'string' && nome !== 'crianca') el.value = valor;
        }
      } catch {
        /* sem armazenamento: segue sem restaurar */
      }
      atualizar();
      form.addEventListener('input', () => {
        atualizar();
        guardarFiltros();
      });

      let gerando = false;
      raiz.addEventListener('click', async (ev) => {
        const botao = (ev.target as HTMLElement).closest<HTMLButtonElement>('[data-imprimir]');
        const alvo = escolhida();
        if (!botao || !alvo || gerando) return;
        gerando = true; // evita duas sessões com o mesmo código num clique duplo
        botao.disabled = true;
        const atividade = publicadas.find((a) => a.id === botao.dataset.imprimir);
        if (!atividade) {
          gerando = false;
          botao.disabled = false;
          return;
        }
        await imprimirAtividadeAvulsa(ctx, atividade, alvo);
      });
    },
  };
};
