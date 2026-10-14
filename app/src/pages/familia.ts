import type { FabricaPagina } from '../ui/app';
import { lerFormulario, lista } from '../ui/app';
import { html } from '../ui/html';
import { IDIOMAS, VERTENTES, type Familia, type Idioma, type Vertente } from '../domain/tipos';
import { avisoExemplo, ligarAvisoExemplo } from '../ui/exemplo';

export const DESCRICAO_VERTENTE: Record<Vertente, string> = {
  Montessori: 'autonomia, materiais concretos, vida prática',
  Waldorf: 'ritmo, arte, imaginação, alfabetização mais tardia',
  Clássico: 'memorização, recitação, Trivium',
  Religioso: 'formação na fé e nas virtudes',
  'Charlotte Mason': 'livros vivos, narração, lições curtas, natureza',
};

export const paginaFamilia: FabricaPagina = async (ctx) => {
  const atual = await ctx.repo.familia();
  const primeiraVez = !atual;
  const f: Familia = atual ?? {
    educador: '',
    vertentePrincipal: 'Montessori',
    inspiracoes: [],
    idiomasEducador: [],
    criadaEm: ctx.agora(),
  };

  return {
    titulo: 'Família',
    conteudo: html` <h1>${primeiraVez ? 'Vamos conhecer sua família' : 'Família'}</h1>
      ${atual?.exemplo ? avisoExemplo() : ''}
      <form class="cartao formulario" id="form-familia">
        <label>
          Seu nome (educador)
          <input
            name="educador"
            required
            maxlength="60"
            value="${f.educador}"
            autocomplete="given-name"
          />
        </label>

        <fieldset>
          <legend>Vertente principal</legend>
          <p class="nota">Define o ritmo e os marcos extras. Dá para mudar depois.</p>
          ${VERTENTES.map(
            (v) =>
              html`<label class="opcao">
                <input
                  type="radio"
                  name="vertentePrincipal"
                  value="${v}"
                  ${v === f.vertentePrincipal ? 'checked' : ''}
                />
                <span><b>${v}</b> <span class="nota">${DESCRICAO_VERTENTE[v]}</span></span>
              </label>`,
          )}
        </fieldset>

        <fieldset>
          <legend>Inspirações (opcional)</legend>
          <p class="nota">Ampliam as atividades e os livros sugeridos.</p>
          ${VERTENTES.map(
            (v) =>
              html`<label class="opcao">
                <input
                  type="checkbox"
                  name="inspiracoes"
                  value="${v}"
                  ${f.inspiracoes.includes(v) ? 'checked' : ''}
                />
                <span>${v}</span>
              </label>`,
          )}
        </fieldset>

        <fieldset>
          <legend>Línguas estrangeiras que você domina</legend>
          <p class="nota">Só oferecemos trilhas de línguas que você fala (decisão do produto).</p>
          ${(Object.keys(IDIOMAS) as Idioma[]).map(
            (i) =>
              html`<label class="opcao">
                <input
                  type="checkbox"
                  name="idiomasEducador"
                  value="${i}"
                  ${f.idiomasEducador.includes(i) ? 'checked' : ''}
                />
                <span>${IDIOMAS[i]}</span>
              </label>`,
          )}
        </fieldset>

        <button class="botao primario" type="submit">
          ${primeiraVez ? 'Continuar' : 'Salvar'}
        </button>
      </form>`,
    montar(raiz) {
      ligarAvisoExemplo(raiz, ctx);
      raiz
        .querySelector<HTMLFormElement>('#form-familia')
        ?.addEventListener('submit', async (ev) => {
          ev.preventDefault();
          const d = lerFormulario(ev.currentTarget as HTMLFormElement);
          const principal = d.vertentePrincipal as Vertente;
          const nova: Familia = {
            ...f,
            educador: String(d.educador ?? '').trim(),
            vertentePrincipal: principal,
            // a principal não conta como inspiração
            inspiracoes: (lista(d.inspiracoes) as Vertente[]).filter((v) => v !== principal),
            idiomasEducador: lista(d.idiomasEducador) as Idioma[],
          };
          await ctx.repo.salvarFamilia(nova);
          void navigator.storage?.persist?.();
          const temCriancas = (await ctx.repo.criancas()).length > 0;
          ctx.avisar('Família salva.');
          ctx.ir(temCriancas ? '/' : '/crianca/nova');
        });
    },
  };
};
