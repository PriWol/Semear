import type { FabricaPagina } from '../ui/app';
import { html, textoRico } from '../ui/html';
import { atividadePublicada, leituraDaAtividade } from '../domain/leitura';
import { rotuloDoMaterial } from '../domain/material';
import { CADERNOS, enderecoDoMaterial } from '../tesouro';
import { imprimirAtividadeAvulsa } from './sessao-avulsa';

/**
 * Uma atividade para LER (#13): quem só quer ver o que fazer não cria sessão. A impressão é um botão à
 * parte e só ela grava a sessão avulsa no histórico.
 */
export const paginaAtividade: FabricaPagina = async (ctx, params) => {
  const encontrada = params.id ? ctx.idx.atividade(params.id) : undefined;
  if (!atividadePublicada(encontrada)) {
    return {
      titulo: 'Atividade não encontrada',
      conteudo: html`<h1>Atividade não encontrada</h1>
        <p>Não achamos essa atividade. Ela pode ter sido retirada ou o endereço está incorreto.</p>
        <p><a href="#/atividades">Voltar às atividades</a></p>`,
    };
  }
  const a = encontrada;
  const familia = await ctx.repo.familia();
  const criancas = await ctx.repo.criancas();
  const crianca = criancas.find((c) => c.id === params.crianca) ?? criancas[0] ?? null;
  const leitura = leituraDaAtividade(
    a,
    ctx.idx,
    familia ? [familia.vertentePrincipal, ...familia.inspiracoes] : [],
  );
  const endereco = a.materialImpresso ? enderecoDoMaterial(a.materialImpresso) : null;

  return {
    titulo: a.titulo,
    conteudo: html`
      <p><a href="#/atividades">← Voltar às atividades</a></p>
      <article class="atividade-leitura" data-atividade-leitura="${a.id}">
        <h1>${a.titulo}</h1>
        <p class="nota">${a.duracaoMin} min · ${a.idade[0]} a ${a.idade[1]} anos</p>
        ${
          leitura.marcos.length
            ? html`<p>
                <b>Marcos que trabalha:</b>
                ${leitura.marcos.map((m) => m.titulo).join(' · ')}
              </p>`
            : a.marcos.length === 0 && a.categoria
              ? html`<p><b>Atividade complementar:</b> ${a.categoria}</p>`
              : ''
        }
        ${
          leitura.revisao.length
            ? html`<p><b>Revisão:</b> ${leitura.revisao.map((m) => m.titulo).join(' · ')}</p>`
            : ''
        }

        <section class="cartao imprimir-atividade" aria-label="Imprimir">
          ${
            criancas.length > 1
              ? html`<label
                  >Para quem imprimir
                  <select id="crianca-imprimir">
                    ${criancas.map(
                      (c) =>
                        html`<option value="${c.id}" ${c.id === crianca?.id ? 'selected' : ''}>${c.nome}</option>`,
                    )}
                  </select></label
                >`
              : ''
          }
          <button class="botao primario" type="button" id="imprimir-atividade" ${crianca ? '' : 'disabled'}>
            🖨️ Imprimir esta atividade
          </button>
          ${
            crianca
              ? ''
              : html`<p class="alerta">
                  Cadastre uma criança para imprimir. <a href="#/familia">Começar</a>
                </p>`
          }
        </section>

        ${
          leitura.cuidados
            ? html`<p class="alerta cuidados" role="note"><b>⚠️ Cuidados:</b> ${leitura.cuidados}</p>`
            : ''
        }

        <h2>🎯 Objetivo</h2>
        <p>${textoRico(a.objetivo)}</p>

        <h2>🧺 Materiais</h2>
        <ul>
          ${a.materiais.map((m) => html`<li>${m.item}${m.deCasa ? html` <b>(de casa)</b>` : ''}</li>`)}
        </ul>

        <h2>🧭 Passo a passo</h2>
        <ol class="passos-leitura">
          ${a.passos.map(
            (p) =>
              html`<li>
                <b>${p.titulo}${p.minutos ? ` (${p.minutos} min)` : ''}.</b> ${textoRico(p.texto)}
                ${p.fala ? html`<p class="fala">“${p.fala}”</p>` : ''}
              </li>`,
          )}
        </ol>

        <h2>👀 O que observar</h2>
        <h3>✅ Consolidado se…</h3>
        <ul>
          ${a.observar.consolidado.map((t) => html`<li>${textoRico(t)}</li>`)}
        </ul>
        <h3>🌱 Em desenvolvimento se…</h3>
        <ul>
          ${a.observar.emDesenvolvimento.map((t) => html`<li>${textoRico(t)}</li>`)}
        </ul>

        ${
          a.ajustes?.facil || a.ajustes?.dificil
            ? html`<h2>🔁 Ajustes na hora</h2>
                <ul>
                  ${a.ajustes.facil ? html`<li><b>Está fácil?</b> ${textoRico(a.ajustes.facil)}</li>` : ''}
                  ${a.ajustes.dificil ? html`<li><b>Está difícil?</b> ${textoRico(a.ajustes.dificil)}</li>` : ''}
                </ul>`
            : ''
        }

        ${
          leitura.toques.length
            ? html`<h2>🌿 Toque da vertente</h2>
                <ul>
                  ${leitura.toques.map(
                    (t) =>
                      html`<li>
                        <b>${t.vertente}${t.principal ? '' : ' (inspiração)'}:</b> ${textoRico(t.texto)}
                      </li>`,
                  )}
                </ul>`
            : ''
        }

        ${
          a.materialImpresso
            ? html`<h2>📖 Material impresso</h2>
                <p>
                  ${rotuloDoMaterial(a.materialImpresso, CADERNOS)}
                  ${
                    endereco
                      ? html`· <a href="${endereco}" target="_blank" rel="noopener">Abrir o PDF</a>`
                      : ''
                  }
                </p>`
            : ''
        }
      </article>
      <p><a href="#/atividades">← Voltar às atividades</a></p>
    `,
    montar(raiz) {
      const botao = raiz.querySelector<HTMLButtonElement>('#imprimir-atividade');
      const seletor = raiz.querySelector<HTMLSelectElement>('#crianca-imprimir');
      let gerando = false;
      botao?.addEventListener('click', async () => {
        const alvo = criancas.find((c) => c.id === seletor?.value) ?? crianca;
        if (!alvo || gerando) return;
        gerando = true; // evita duas sessões com o mesmo código num clique duplo
        botao.disabled = true;
        await imprimirAtividadeAvulsa(ctx, a, alvo);
      });
    },
  };
};
