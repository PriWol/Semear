import type { FabricaPagina } from '../ui/app';
import { lerFormulario, lista, novoId } from '../ui/app';
import { html } from '../ui/html';
import { IDIOMAS, LETRAS, type Crianca, type Idioma } from '../domain/tipos';
import { dataLocalISO, idadeEmAnos } from '../domain/datas';
import { ehLetra } from '../domain/letra';
import { letraPadrao, NOME_LETRA } from '../domain/letra';
import { avisoExemplo, ligarAvisoExemplo } from '../ui/exemplo';

export const paginaCrianca: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  if (!familia)
    return {
      titulo: 'Família',
      conteudo: html`<p>Cadastre a família primeiro. <a href="#/familia">Começar</a></p>`,
    };
  const id = params.id ?? 'nova';
  const existente = id === 'nova' ? null : await ctx.repo.crianca(id);
  if (id !== 'nova' && !existente) throw new Error('Criança não encontrada.');
  const c: Crianca = existente ?? {
    id: novoId(),
    nome: '',
    nascimento: '',
    letra: null,
    trilhas: [],
  };
  const agora = new Date(ctx.agora());
  const hoje = dataLocalISO(agora); // dia do aparelho, não o de UTC
  const letraAuto = c.nascimento
    ? NOME_LETRA[letraPadrao(idadeEmAnos(c.nascimento, agora), familia)]
    : null;
  // Línguas que a criança já tem, mesmo que a família tenha desmarcado depois: não somem sem aviso.
  const idiomasOferecidos = [
    ...familia.idiomasEducador,
    ...c.trilhas.filter((i) => !familia.idiomasEducador.includes(i)),
  ];

  return {
    titulo: existente ? c.nome : 'Nova criança',
    conteudo: html` <h1>${existente ? `Editar ${c.nome}` : 'Adicionar criança'}</h1>
      ${familia.exemplo ? avisoExemplo() : ''}
      <form class="cartao formulario" id="form-crianca">
        <label
          >Nome <input name="nome" required maxlength="40" pattern=".*\\S.*" value="${c.nome}"
        /></label>
        <label>
          Data de nascimento
          <input name="nascimento" type="date" required max="${hoje}" value="${c.nascimento}" />
        </label>
        <label>
          Letra nas folhas
          <select name="letra">
            <option value="">Automática${letraAuto ? ` (hoje: ${letraAuto})` : ''}</option>
            ${LETRAS.map((l) => html`<option value="${l}" ${c.letra === l ? 'selected' : ''}>${NOME_LETRA[l]}</option>`)}
          </select>
          <span class="nota"
            >Automática: bastão → script → cursiva pela idade; Montessori e Waldorf começam na
            cursiva.</span
          >
        </label>
        <fieldset>
          <legend>Línguas estrangeiras</legend>
          ${
            idiomasOferecidos.length
              ? html`<p class="nota">
                    Recomendamos no máximo 2 ao mesmo tempo. Latim a partir dos 6 anos.
                  </p>
                  ${idiomasOferecidos.map(
                    (i) =>
                      html`<label class="opcao">
                        <input
                          type="checkbox"
                          name="trilhas"
                          value="${i}"
                          ${c.trilhas.includes(i) ? 'checked' : ''}
                        />
                        <span
                          >${IDIOMAS[i]}${
                            familia.idiomasEducador.includes(i)
                              ? ''
                              : html` <span class="nota">(não está mais marcada na família)</span>`
                          }</span
                        >
                      </label>`,
                  )}`
              : html`<p class="nota">Nenhuma língua marcada na <a href="#/familia">família</a>.</p>`
          }
        </fieldset>
        <div class="acoes">
          <button class="botao primario" type="submit">Salvar</button>
          ${existente ? html`<button class="botao perigo" type="button" id="remover">Remover criança</button>` : ''}
        </div>
      </form>`,
    montar(raiz) {
      ligarAvisoExemplo(raiz, ctx);
      raiz
        .querySelector<HTMLFormElement>('#form-crianca')
        ?.addEventListener('submit', async (ev) => {
          ev.preventDefault();
          const d = lerFormulario(ev.currentTarget as HTMLFormElement);
          const nome = String(d.nome ?? '').trim();
          if (!nome) return;
          const nova: Crianca = {
            ...c,
            nome,
            nascimento: String(d.nascimento ?? ''),
            letra: ehLetra(d.letra) ? d.letra : null,
            trilhas: lista(d.trilhas) as Idioma[],
          };
          await ctx.repo.salvarCrianca(nova);
          ctx.avisar('Dados salvos.');
          ctx.ir(existente ? '/' : `/jornada/${nova.id}`);
        });
      raiz.querySelector('#remover')?.addEventListener('click', async () => {
        if (!confirm(`Remover ${c.nome} e todo o histórico? Isso não pode ser desfeito.`)) return;
        await ctx.repo.removerCrianca(c.id);
        ctx.avisar('Criança removida.');
        ctx.ir('/');
      });
    },
  };
};
