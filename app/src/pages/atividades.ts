import type { FabricaPagina } from '../ui/app';
import { novoId } from '../ui/app';
import { html, type HtmlSeguro } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { buscarAtividades, dominioDaAtividade } from '../domain/busca';
import { gerarCodigoSessao } from '../domain/sessao';
import { VERTENTES, type Atividade, type Sessao, type Vertente } from '../domain/tipos';

const DURACOES_MAX = [10, 20, 30, 40, 60];

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
    publicadas.some((a) => dominioDaAtividade(a) === d.id),
  );

  const lista = (itens: Atividade[]): HtmlSeguro =>
    itens.length === 0
      ? html`<p class="nota">Nenhuma atividade encontrada. Tente outra palavra ou tire um filtro.</p>`
      : html`<ul class="lista-atividades">
          ${itens.map((a) => {
            const folha = a.folhas[0];
            return html`<li class="cartao" data-atividade="${a.id}">
              <h3>${a.titulo}</h3>
              <p class="nota">
                ${a.duracaoMin} min · ${a.idade[0]} a ${a.idade[1]} anos
                ${a.marcos.length ? html`· ${a.marcos.join(', ')}` : ''}
              </p>
              <p>${a.objetivo.replace(/\*+/g, '')}</p>
              ${folha ? html`<p class="nota">Primeira folha: ${folha.titulo}</p>` : ''}
              <button class="botao primario" type="button" data-imprimir="${a.id}"
                ${crianca ? '' : 'disabled'}>
                🖨️ Imprimir esta atividade
              </button>
            </li>`;
          })}
        </ul>`;

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
            ${dominios.map((d) => html`<option value="${d.id}">${d.icone} ${d.nome}</option>`)}
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
        ${
          crianca
            ? html`<label class="opcao"
                ><input type="checkbox" name="idade" /> Só para a idade de ${crianca.nome}</label
              >`
            : ''
        }
      </form>
      <div id="resultado-atividades" aria-live="polite">${lista(buscarAtividades(publicadas, { texto: '' }).map((r) => r.atividade))}</div>
    `,
    montar(raiz) {
      const form = raiz.querySelector<HTMLFormElement>('#filtros-atividades');
      const resultado = raiz.querySelector<HTMLElement>('#resultado-atividades');
      if (!form || !resultado) return;
      form.addEventListener('submit', (ev) => ev.preventDefault());

      const campo = (n: string) => form.elements.namedItem(n) as HTMLInputElement | null;
      const escolhida = () => criancas.find((c) => c.id === campo('crianca')?.value) ?? crianca;

      const atualizar = () => {
        const alvo = escolhida();
        const idade =
          campo('idade')?.checked && alvo
            ? Math.floor(idadeEmAnos(alvo.nascimento, new Date(ctx.agora())))
            : undefined;
        const achadas = buscarAtividades(publicadas, {
          texto: campo('texto')?.value ?? '',
          dominio: campo('dominio')?.value || undefined,
          vertente: (campo('vertente')?.value || undefined) as Vertente | undefined,
          duracaoMax: campo('duracao')?.value ? Number(campo('duracao')?.value) : undefined,
          idade,
        });
        resultado.innerHTML = lista(achadas.map((r) => r.atividade)).valor;
      };
      form.addEventListener('input', atualizar);

      let gerando = false;
      raiz.addEventListener('click', async (ev) => {
        const botao = (ev.target as HTMLElement).closest<HTMLButtonElement>('[data-imprimir]');
        const alvo = escolhida();
        if (!botao || !alvo || gerando) return;
        gerando = true; // evita duas sessões com o mesmo código num clique duplo
        botao.disabled = true;
        const criadaEm = ctx.agora();
        const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
        const atividade = publicadas.find((a) => a.id === botao.dataset.imprimir);
        if (!atividade) return;
        const sessao: Sessao = {
          id: novoId(),
          codigo: gerarCodigoSessao(alvo.nome, new Date(criadaEm), existentes),
          criancaId: alvo.id,
          criadaEm,
          duracaoMin: atividade.duracaoMin,
          foco: 'equilibrado',
          atividadeIds: [atividade.id],
          livroId: null,
          tipo: 'avulsa',
        };
        await ctx.repo.salvarSessao(sessao);
        ctx.ir(`/sessao/${sessao.id}`);
      });
    },
  };
};
