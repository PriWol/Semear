import type { FabricaPagina } from '../ui/app';
import { lerFormulario } from '../ui/app';
import { html, textoRico, type HtmlSeguro } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { idPista, pistasDaCrianca } from '../domain/jornada';
import {
  alvoDaSondagem,
  etapaDeAjuste,
  itensBase,
  marcosSondaveis,
  mudancasDaSondagem,
  type Resultados,
} from '../domain/sondagem';
import { carregarSondagem } from '../conteudo';
import { ESTADOS } from '../domain/tipos';
import { NOME_ESTADO } from '../ui/rotulos';

/**
 * Sondagem impressa (#17, §5.4): a etapa base traz três itens por linha; depois que o educador
 * lança os resultados, a etapa de ajuste traz um item novo só nas linhas que ainda não se
 * definiram. Ao terminar, a posição é gravada com origem "sondagem".
 */
export const paginaSondagem: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  const crianca = params.id ? await ctx.repo.crianca(params.id) : null;
  if (!familia || !crianca) throw new Error('Criança não encontrada.');
  const sondagem = carregarSondagem();
  const idade = idadeEmAnos(crianca.nascimento, new Date(ctx.agora()));
  const emRevisao = sondagem.itens.some((i) => i.revisao?.estado === 'rascunho');

  const pistas = pistasDaCrianca(ctx.idx, familia, crianca)
    .map((pista) => ({
      pista,
      id: idPista(pista),
      marcos: marcosSondaveis(ctx.idx, pista, sondagem),
    }))
    .filter((x) => x.marcos.length > 0);

  // Estado da sondagem em andamento: resultados lançados e o que cada linha testa nesta etapa.
  const resultados = new Map<string, Resultados>(pistas.map((p) => [p.id, {}]));
  let atuais = new Map<string, string[]>(pistas.map((p) => [p.id, itensBase(p.marcos, idade)]));
  let etapa = 1;

  const itemDoMarco = (marcoId: string) => sondagem.itens.find((i) => i.marco === marcoId);

  const folha = (): HtmlSeguro => {
    const linhas = pistas.filter((p) => (atuais.get(p.id) ?? []).length > 0);
    if (linhas.length === 0) return html`<p>Nada a aplicar.</p>`;
    return html`<h2>${etapa === 1 ? 'Etapa 1: base' : `Etapa ${etapa}: ajuste`}</h2>
      <form id="form-sondagem" class="formulario">
        ${linhas.map(
          (p) => html`<section class="cartao">
            <h3>${p.pista.dominio.icone} ${p.pista.linha.nome}</h3>
            ${(atuais.get(p.id) ?? []).map((marcoId) => {
              const item = itemDoMarco(marcoId);
              const marco = ctx.idx.marco(marcoId);
              if (!item || !marco) return '';
              return html`<fieldset>
                <legend>${marco.titulo}</legend>
                <p>${textoRico(item.instrucao)}</p>
                <p class="nota">
                  <b>Consolidado:</b> ${textoRico(item.consolidado)}<br />
                  <b>Em desenvolvimento:</b> ${textoRico(item.emDesenvolvimento)}
                </p>
                <div class="linha-opcoes">
                  ${ESTADOS.map(
                    (e) => html`<label class="opcao"
                      ><input type="radio" name="${p.id}|${marcoId}" value="${e}" />
                      ${NOME_ESTADO[e]}</label
                    >`,
                  )}
                </div>
              </fieldset>`;
            })}
          </section>`,
        )}
        <div class="acoes">
          <button class="botao" type="button" id="imprimir-sondagem">🖨️ Imprimir esta etapa</button>
          <button class="botao primario" type="submit">Lançar resultados</button>
        </div>
      </form>`;
  };

  return {
    titulo: `Sondagem de ${crianca.nome}`,
    conteudo: html`
      <h1>Sondagem de ${crianca.nome}</h1>
      <p class="nota">
        Aplique com ${crianca.nome} no papel, sem pressa e sem avisar que é uma prova. Marque o que
        viu em cada item e toque em “Lançar resultados”. Se alguma linha ainda não ficar clara, o
        app traz mais um item só dela. Pode dividir em dias: lance o que já aplicou.
        <a href="#/jornada/${crianca.id}">Voltar à jornada</a>
      </p>
      ${
        emRevisao
          ? html`<p class="alerta" role="note">
              Itens de sondagem em revisão pela dona do produto. Use como ponto de partida.
            </p>`
          : ''
      }
      ${
        pistas.length === 0
          ? html`<p class="alerta">Ainda não há itens de sondagem para as linhas de ${crianca.nome}.</p>`
          : html`<div id="area-sondagem">${folha()}</div>`
      }
    `,
    montar(raiz) {
      const area = raiz.querySelector<HTMLElement>('#area-sondagem');
      if (!area) return;

      const redesenhar = () => {
        area.innerHTML = folha().valor;
        ligar();
      };

      const ligar = () => {
        area.querySelector('#imprimir-sondagem')?.addEventListener('click', () => window.print());
        area
          .querySelector<HTMLFormElement>('#form-sondagem')
          ?.addEventListener('submit', async (ev) => {
            ev.preventDefault();
            const dados = lerFormulario(ev.currentTarget as HTMLFormElement);
            const estados = await ctx.repo.estados(crianca.id);
            const proximas = new Map<string, string[]>();
            let gravadas = 0;
            for (const p of pistas) {
              const res = resultados.get(p.id) ?? {};
              for (const marcoId of atuais.get(p.id) ?? []) {
                const v = dados[`${p.id}|${marcoId}`];
                if (typeof v === 'string' && (ESTADOS as readonly string[]).includes(v))
                  res[marcoId] = v as Resultados[string];
              }
              const ajuste = etapaDeAjuste(p.marcos, res);
              const alvo = alvoDaSondagem(p.marcos, res);
              if (ajuste.length > 0) {
                proximas.set(p.id, ajuste);
              } else if (
                alvo &&
                Object.keys(res).length > 0 &&
                (atuais.get(p.id) ?? []).length > 0
              ) {
                await ctx.repo.atualizarEstados(
                  crianca.id,
                  mudancasDaSondagem(ctx.idx, p.pista, alvo, estados, ctx.agora()),
                );
                gravadas++;
              }
            }
            if (proximas.size === 0) {
              ctx.avisar(
                gravadas > 0 ? 'Sondagem registrada na jornada.' : 'Nenhum resultado lançado.',
              );
              ctx.ir(`/jornada/${crianca.id}`);
              return;
            }
            atuais = proximas;
            etapa++;
            ctx.avisar(
              gravadas > 0
                ? 'Linhas definidas foram gravadas. Faltam alguns itens.'
                : 'Faltam alguns itens.',
            );
            redesenhar();
          });
      };
      ligar();
    },
  };
};
