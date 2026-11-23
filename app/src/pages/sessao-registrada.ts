import { NaoEncontrado, type FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import {
  contarObservados,
  dentroDoPrazoDeDesfazer,
  observacoesDaSessao,
  observacoesRegistradas,
  pareceProntoPara,
  PRAZO_DESFAZER_MS,
  textoMarcosObservados,
} from '../domain/registro';
import type { Sessao } from '../domain/tipos';
import { dataCurta, NOME_ESTADO } from '../ui/rotulos';

/**
 * O que é preciso para desfazer o registro que acabou de ser salvo: a sessão como era antes e a hora do
 * registro. Fica só na memória da página (não é gravado em lugar nenhum): ao recarregar ou sair, o
 * "Desfazer" simplesmente deixa de existir e o registro vale (ADR 0030, adendo de 22/11/2026).
 */
let desfazivel: { anterior: Sessao; registradaEm: string } | null = null;

export function lembrarParaDesfazer(anterior: Sessao, registradaEm: string): void {
  desfazivel = { anterior, registradaEm };
}

const segundosRestantes = (registradaEm: string, agora: string): number =>
  Math.max(
    0,
    Math.ceil((PRAZO_DESFAZER_MS - (Date.parse(agora) - Date.parse(registradaEm))) / 1000),
  );

/**
 * Resumo depois de registrar (D20): mostra o efeito sem prometer avanço. Registrar NUNCA muda o estado do
 * marco (ADR 0030), então a tela diz "marcos observados" e lembra quem decide: a família, na jornada.
 */
export const paginaSessaoRegistrada: FabricaPagina = async (ctx, params) => {
  const sessao = params.id ? await ctx.repo.sessao(params.id) : null;
  const crianca = sessao ? await ctx.repo.crianca(sessao.criancaId) : null;
  if (!sessao || !crianca) throw new NaoEncontrado('sessão');

  const ficha = observacoesDaSessao(sessao, ctx.idx);
  const historico = await ctx.repo.historico(crianca.id);
  const estados = await ctx.repo.estados(crianca.id);
  const registradas = observacoesRegistradas(sessao.id, historico);
  const observados = ficha.filter((o) => registradas[o.chave] !== undefined);
  const prontos = observados.filter((o) => pareceProntoPara(o.chave, estados, historico));

  const pendente =
    desfazivel &&
    desfazivel.anterior.id === sessao.id &&
    desfazivel.registradaEm === sessao.registradaEm
      ? desfazivel
      : null;
  const restante = pendente ? segundosRestantes(pendente.registradaEm, ctx.agora()) : 0;
  const podeDesfazer = pendente !== null && restante > 0;

  return {
    titulo: `Sessão ${sessao.codigo} registrada`,
    conteudo: html`
      <section class="cartao resumo-registro" aria-labelledby="titulo-resumo">
        <h1 id="titulo-resumo">Sessão registrada</h1>
        <p class="reg-contexto">
          ${sessao.codigo} · ${crianca.nome} · ${dataCurta(sessao.criadaEm)}
        </p>
        <h2 id="resumo-observados">
          ${textoMarcosObservados(contarObservados(ficha, registradas))}
        </h2>
        ${
          observados.length
            ? html`<ul class="resumo-marcos">
                ${observados.map(
                  (o) =>
                    html`<li>
                      <span>${ctx.idx.marco(o.marcoId)?.titulo ?? ''}</span>
                      <span class="nota">${NOME_ESTADO[registradas[o.chave]!]}</span>
                    </li>`,
                )}
              </ul>`
            : ''
        }
        ${
          prontos.length
            ? html`<p class="reg-dica">
                ${prontos.length === 1 ? '1 marco parece pronto' : `${prontos.length} marcos parecem prontos`}:
                você decide se marca como Consolidado, na jornada.
              </p>`
            : ''
        }
        <p class="nota">
          O estado dos marcos na jornada não mudou. Quem decide quando um marco está consolidado é
          você.
        </p>
        <div class="acoes">
          <a class="botao primario" href="#/sessao/nova?crianca=${crianca.id}"
            >Preparar a próxima sessão</a
          >
          <a class="botao" href="#/jornada/${crianca.id}">Ver jornada</a>
          <a class="botao" href="#/">Voltar ao início</a>
        </div>
        ${
          podeDesfazer
            ? html`<p class="resumo-desfazer" id="area-desfazer">
                <button class="botao" type="button" id="desfazer">
                  Desfazer este registro (<span id="segundos">${restante}</span> s)
                </button>
              </p>`
            : ''
        }
      </section>
    `,
    montar(raiz) {
      const area = raiz.querySelector<HTMLElement>('#area-desfazer');
      const botao = raiz.querySelector<HTMLButtonElement>('#desfazer');
      const segundos = raiz.querySelector<HTMLElement>('#segundos');
      if (!pendente || !area || !botao || !segundos) return;
      let temporizador = 0;
      const encerrar = () => {
        window.clearInterval(temporizador);
        area.remove();
      };
      temporizador = window.setInterval(() => {
        if (!raiz.isConnected) return window.clearInterval(temporizador);
        const falta = segundosRestantes(pendente.registradaEm, ctx.agora());
        if (falta <= 0) {
          desfazivel = null;
          return encerrar();
        }
        segundos.textContent = String(falta);
      }, 500);

      botao.addEventListener('click', async () => {
        botao.disabled = true; // um toque duplo não desfaz duas vezes
        // A janela de 10 s vale também no toque, não só na contagem que a tela mostra.
        const dentro = dentroDoPrazoDeDesfazer(pendente.registradaEm, ctx.agora());
        const desfeito = dentro
          ? await ctx.repo.desfazerRegistro(pendente.anterior, pendente.registradaEm)
          : false;
        desfazivel = null;
        encerrar();
        if (desfeito) {
          ctx.avisar('Registro desfeito. A ficha voltou ao que era.');
          ctx.ir(`/sessao/${sessao.id}/registrar`);
        } else {
          ctx.avisar(
            'Não foi possível desfazer: o registro já passou do prazo ou foi alterado.',
            'alerta',
          );
        }
      });
    },
  };
};
