import type { FabricaPagina } from '../ui/app';
import { lerFormulario, lista, novoId } from '../ui/app';
import { html } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { letraDaCrianca } from '../domain/letra';
import { DURACAO_PADRAO, DURACOES, gerarCodigoSessao } from '../domain/sessao';
import {
  DIAS,
  marcarFeito,
  materiaisDaSemana,
  NOME_DIA,
  planejarSemana,
  removerAtividade,
  segundaDaSemana,
  trocarAtividade,
  type Dia,
  type EntradaSemana,
  type PlanoSemana,
} from '../domain/semana';
import type { Atividade, Sessao } from '../domain/tipos';
import { gerarSemana, nomeArquivoSemana, type ModoSemana } from '../pacote/semana';
import { baixarArquivo } from './sessao';
import { sincronizarComOAparelho } from '../nativo/sincronizar';

const DIAS_PADRAO: Dia[] = ['seg', 'qua', 'sex'];

/** Plano da semana de uma criança (#8) e impressão da semana inteira (#9). */
export const paginaSemana: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  const crianca = params.id ? await ctx.repo.crianca(params.id) : null;
  if (!familia || !crianca) throw new Error('Criança não encontrada.');
  const agora = ctx.agora();
  const idade = idadeEmAnos(crianca.nascimento, new Date(agora));
  const inicio = segundaDaSemana(new Date(agora));
  const plano = (await ctx.repo.planos(crianca.id)).find((p) => p.inicio === inicio) ?? null;
  const rotina = crianca.rotina ?? { dias: DIAS_PADRAO, duracaoMin: DURACAO_PADRAO };

  const atividadeDe = (id: string): Atividade | undefined => ctx.idx.atividade(id);

  const base = async (): Promise<Omit<EntradaSemana, 'id' | 'rotina'>> => ({
    familia,
    crianca,
    idade,
    estados: await ctx.repo.estados(crianca.id),
    historico: (await ctx.repo.sessoes(crianca.id)).filter(
      (s) => !plano?.dias.some((d) => d.sessaoId === s.id), // sessões do próprio plano não pesam
    ),
    agora,
  });

  const formulario = html`<form class="cartao formulario" id="form-semana">
    <fieldset>
      <legend>Dias da semana</legend>
      <div class="linha-opcoes">
        ${DIAS.map(
          (d) =>
            html`<label class="opcao"
              ><input type="checkbox" name="dias" value="${d}" ${rotina.dias.includes(d) ? 'checked' : ''} />
              ${NOME_DIA[d]}</label
            >`,
        )}
      </div>
    </fieldset>
    <fieldset>
      <legend>Duração de cada sessão</legend>
      <div class="linha-opcoes">
        ${DURACOES.map(
          (m) =>
            html`<label class="opcao"
              ><input type="radio" name="duracao" value="${m}" ${m === rotina.duracaoMin ? 'checked' : ''} />
              ${m} min</label
            >`,
        )}
      </div>
    </fieldset>
    <button class="botao primario" type="submit">Planejar semana</button>
  </form>`;

  const diaCard = (
    d: PlanoSemana['dias'][number],
  ) => html`<section class="cartao dia-plano ${d.feito ? 'feito' : ''}" data-dia="${d.dia}">
    <h2>${NOME_DIA[d.dia]} <span class="nota">${d.data.split('-').reverse().slice(0, 2).join('/')}${d.feito ? ' · feito ✓' : ''}</span></h2>
    ${
      d.atividadeIds.length === 0
        ? html`<p class="nota">Sem atividade neste dia.</p>`
        : html`<ul>
            ${d.atividadeIds.map((id) => {
              const a = atividadeDe(id);
              if (!a) return '';
              return html`<li>
                ${a.titulo} <span class="nota">${a.duracaoMin} min</span>
                <button class="link-botao" type="button" data-acao="trocar" data-dia="${d.dia}" data-atividade="${id}">Trocar</button>
                <button class="link-botao" type="button" data-acao="remover" data-dia="${d.dia}" data-atividade="${id}">Remover</button>
              </li>`;
            })}
          </ul>`
    }
    <button class="botao ${d.feito ? '' : 'primario'}" type="button" data-acao="feito" data-dia="${d.dia}">
      ${d.feito ? 'Desmarcar' : 'Marcar como feito'}
    </button>
  </section>`;

  return {
    titulo: `Semana de ${crianca.nome}`,
    conteudo: html`
      <h1>Semana de ${crianca.nome}</h1>
      <p class="nota">
        Escolha os dias e a duração e o app distribui as linhas, sem repetir atividade na semana.
        <a href="#/jornada/${crianca.id}">Voltar à jornada</a>
      </p>
      ${
        plano
          ? html`<div class="acoes">
                <button class="botao" type="button" data-acao="replanejar">Planejar de novo</button>
              </div>
              ${plano.dias.map(diaCard)}
              <section class="cartao">
                <h2>Imprimir a semana</h2>
                <label
                  >O que imprimir
                  <select id="modo-semana">
                    <option value="tudo">Tudo (roteiros, folhas e fichas)</option>
                    <option value="folhas">Só as folhas da criança</option>
                    <option value="roteiros">Só os roteiros e as fichas</option>
                  </select></label
                >
                <div class="acoes">
                  <button class="botao primario" type="button" id="abrir-semana">🖨️ Abrir para imprimir</button>
                  <button class="botao" type="button" id="baixar-semana">⬇️ Baixar arquivo</button>
                </div>
              </section>`
          : formulario
      }
    `,
    montar(raiz) {
      const entradaDoPlano = async (p: PlanoSemana) => {
        const b = await base();
        return { ...b, id: p.id, rotina: p.rotina } satisfies EntradaSemana;
      };

      raiz
        .querySelector<HTMLFormElement>('#form-semana')
        ?.addEventListener('submit', async (ev) => {
          ev.preventDefault();
          const d = lerFormulario(ev.currentTarget as HTMLFormElement);
          const dias = lista(d.dias) as Dia[];
          if (dias.length === 0) {
            ctx.avisar('Escolha pelo menos um dia.');
            return;
          }
          const nova = { dias, duracaoMin: Number(d.duracao ?? DURACAO_PADRAO) };
          await ctx.repo.salvarCrianca({ ...crianca, rotina: nova });
          const novo = planejarSemana(ctx.idx, { ...(await base()), id: novoId(), rotina: nova });
          await ctx.repo.salvarPlano(novo);
          void sincronizarComOAparelho(ctx, { pedirPermissao: false });
          await ctx.atualizar();
        });

      raiz.addEventListener('click', async (ev) => {
        const alvo = (ev.target as HTMLElement).closest<HTMLElement>('[data-acao]');
        if (!alvo || !plano) return;
        const dia = alvo.dataset.dia as Dia | undefined;
        const acao = alvo.dataset.acao;
        let novo: PlanoSemana | null = plano;
        if (acao === 'replanejar') {
          if (!confirm('Planejar de novo apaga o plano desta semana. Continuar?')) return;
          await ctx.repo.removerPlano(plano.id);
          void sincronizarComOAparelho(ctx, { pedirPermissao: false });
          await ctx.atualizar();
          return;
        }
        if (!dia) return;
        if (acao === 'remover') novo = removerAtividade(plano, dia, alvo.dataset.atividade ?? '');
        else if (acao === 'trocar') {
          novo = trocarAtividade(
            ctx.idx,
            await entradaDoPlano(plano),
            plano,
            dia,
            alvo.dataset.atividade ?? '',
          );
          if (!novo) {
            ctx.avisar('Não há outra atividade para trocar nesta linha.');
            return;
          }
        } else if (acao === 'feito') {
          const d = plano.dias.find((x) => x.dia === dia);
          if (!d) return;
          if (d.feito) {
            if (d.sessaoId) await ctx.repo.removerSessao(d.sessaoId);
            novo = marcarFeito(plano, dia, false);
          } else {
            // Registra a sessão do dia no histórico, como se tivesse sido preparada pelo gerador.
            const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
            const [a, m, dd] = d.data.split('-').map(Number) as [number, number, number];
            const sessao: Sessao = {
              id: novoId(),
              codigo: gerarCodigoSessao(crianca.nome, new Date(a, m - 1, dd), existentes),
              criancaId: crianca.id,
              criadaEm: agora,
              duracaoMin: d.atividadeIds.reduce(
                (t, id) => t + (atividadeDe(id)?.duracaoMin ?? 0),
                0,
              ),
              foco: 'equilibrado',
              atividadeIds: d.atividadeIds,
              livroId: d.livroId,
            };
            await ctx.repo.salvarSessao(sessao);
            novo = marcarFeito(plano, dia, true, sessao.id);
          }
        }
        if (novo) await ctx.repo.salvarPlano(novo);
        void sincronizarComOAparelho(ctx, { pedirPermissao: false });
        await ctx.atualizar();
      });

      const documento = async () => {
        if (!plano) return null;
        const modo = (raiz.querySelector<HTMLSelectElement>('#modo-semana')?.value ??
          'tudo') as ModoSemana;
        const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
        const usados = [...existentes];
        const dias = plano.dias.map((dia) => {
          const [a, m, dd] = dia.data.split('-').map(Number) as [number, number, number];
          const codigo = gerarCodigoSessao(crianca.nome, new Date(a, m - 1, dd), usados);
          usados.push(codigo);
          return {
            dia,
            entrada: {
              sessao: {
                id: `${plano.id}-${dia.dia}`,
                codigo,
                criancaId: crianca.id,
                criadaEm: agora,
                duracaoMin: dia.duracaoMin,
                foco: 'equilibrado' as const,
                atividadeIds: dia.atividadeIds,
                livroId: dia.livroId,
              },
              familia,
              crianca,
              idade,
              letra: letraDaCrianca(crianca, idade, familia),
              atividades: dia.atividadeIds
                .map(atividadeDe)
                .filter((x): x is Atividade => x !== undefined),
              livro: dia.livroId ? (ctx.idx.livro(dia.livroId) ?? null) : null,
              marco: (id: string) => ctx.idx.marco(id),
            },
          };
        });
        return gerarSemana({
          crianca,
          plano,
          dias,
          materiais: materiaisDaSemana(ctx.idx, plano),
          modo,
        });
      };
      raiz.querySelector('#abrir-semana')?.addEventListener('click', async () => {
        const doc = await documento();
        if (!doc) return;
        const url = URL.createObjectURL(new Blob([doc], { type: 'text/html;charset=utf-8' }));
        window.open(url, '_blank', 'noopener');
        setTimeout(() => URL.revokeObjectURL(url), 60_000);
      });
      raiz.querySelector('#baixar-semana')?.addEventListener('click', async () => {
        const doc = await documento();
        if (doc && plano)
          baixarArquivo(nomeArquivoSemana(plano, crianca), doc, 'text/html;charset=utf-8');
      });
    },
  };
};
