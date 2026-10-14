import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { idadeEmAnos } from '../domain/datas';
import { precisaLembreteBackup } from '../domain/backup';
import { pistasDaCrianca, posicaoDaLinha } from '../domain/jornada';
import { anos, dataCurta } from '../ui/rotulos';
import { criarExemplo } from '../domain/exemplo';

export const paginaInicio: FabricaPagina = async (ctx) => {
  const familia = await ctx.repo.familia();
  if (!familia) {
    return {
      titulo: 'Bem-vindo',
      conteudo: html`<section class="cartao boas-vindas">
        <p class="selo">🌱</p>
        <h1>Bem-vindo ao Semear</h1>
        <p>
          Organize a jornada de aprendizado dos seus filhos por domínios e gere, antes de cada
          sessão, um pacote pronto para imprimir ou abrir no tablet. <b>A criança não usa o app</b>:
          só você.
        </p>
        <p class="nota">Seus dados ficam guardados só neste aparelho.</p>
        <div class="acoes">
          <a class="botao primario grande" href="#/familia">Começar</a>
          <button class="botao grande" type="button" id="explorar-exemplo">
            Explorar com uma família de exemplo
          </button>
        </div>
        <p class="nota">
          O exemplo traz duas crianças fictícias já posicionadas, para você ver tudo funcionando.
          Dá para apagar depois com um toque.
        </p>
      </section>`,
      montar(raiz) {
        raiz
          .querySelector<HTMLButtonElement>('#explorar-exemplo')
          ?.addEventListener('click', async (ev) => {
            const botao = ev.currentTarget as HTMLButtonElement;
            botao.disabled = true; // evita carregar duas vezes num toque duplo
            try {
              const agora = ctx.agora();
              await ctx.repo.carregarExemplo(criarExemplo(ctx.idx, new Date(agora)));
              ctx.avisar('Família de exemplo carregada.');
              ctx.ir('/');
            } catch (erro) {
              botao.disabled = false;
              alert(erro instanceof Error ? erro.message : 'Não foi possível carregar o exemplo.');
            }
          });
      },
    };
  }

  const agora = ctx.agora();
  const hoje = new Date(agora);
  const criancas = await ctx.repo.criancas();
  const sessoes = (await ctx.repo.sessoes()).slice(0, 6);
  const ultimoBackup = await ctx.repo.ultimoBackup();
  const precisaBackup = precisaLembreteBackup(criancas, ultimoBackup, agora);

  const cartoes = await Promise.all(
    criancas.map(async (c) => {
      const idade = idadeEmAnos(c.nascimento, hoje);
      const estados = await ctx.repo.estados(c.id);
      const porDominio = new Map<
        string,
        { nome: string; icone: string; cons: number; total: number }
      >();
      const ativos: string[] = [];
      for (const pista of pistasDaCrianca(ctx.idx, familia, c)) {
        const pos = posicaoDaLinha(ctx.idx, pista, estados, idade, familia.vertentePrincipal);
        const d = porDominio.get(pista.dominio.id) ?? {
          nome: pista.dominio.nome,
          icone: pista.dominio.icone,
          cons: 0,
          total: 0,
        };
        d.cons += pos.consolidados;
        d.total += pos.total;
        porDominio.set(pista.dominio.id, d);
        for (const id of pos.ativos) ativos.push(ctx.idx.marco(id)?.titulo ?? id);
      }
      const posicionada = Object.keys(estados).length > 0;
      return html`<article class="cartao crianca-cartao">
        <header>
          <h2>${c.nome}</h2>
          <span class="nota">${anos(idade)}</span>
          <a class="link-discreto" href="#/crianca/${c.id}">editar</a>
        </header>
        ${
          posicionada
            ? html`<ul class="progresso-dominios">
                  ${[...porDominio.values()]
                    .filter((d) => d.total > 0)
                    .map(
                      (d) =>
                        html`<li>
                          <span>${d.icone} ${d.nome}</span>
                          <progress max="${d.total}" value="${d.cons}"></progress>
                          <span class="nota">${d.cons}/${d.total}</span>
                        </li>`,
                    )}
                </ul>
                ${
                  ativos.length
                    ? html`<p class="nota">
                        <b>Trabalhando agora:</b> ${ativos.slice(0, 4).join(' · ')}
                      </p>`
                    : ''
                }`
            : html`<p class="nota">
                Ainda sem posição na jornada. Leva uns 5 minutos por domínio.
              </p>`
        }
        <div class="acoes">
          <a class="botao primario" href="#/sessao/nova?crianca=${c.id}">Preparar sessão</a>
          <a class="botao" href="#/jornada/${c.id}"
            >${posicionada ? 'Ver jornada' : 'Posicionar'}</a
          >
        </div>
      </article>`;
    }),
  );

  return {
    titulo: 'Início',
    conteudo: html`
      <h1>Olá, ${familia.educador}!</h1>
      ${
        precisaBackup
          ? html`<div class="alerta">
              💾
              ${
                ultimoBackup
                  ? `Seu último backup foi em ${dataCurta(ultimoBackup)}.`
                  : 'Você ainda não fez nenhum backup.'
              }
              Os dados ficam só neste aparelho. <a href="#/config">Fazer backup agora</a>
            </div>`
          : ''
      }
      <div class="grade-cartoes">${cartoes}</div>
      <p><a class="botao" href="#/crianca/nova">+ Adicionar criança</a></p>

      <h2>Últimas sessões</h2>
      ${
        sessoes.length
          ? html`<ul class="lista-sessoes">
              ${sessoes.map((s) => {
                const crianca = criancas.find((c) => c.id === s.criancaId);
                const titulos = s.atividadeIds.map((id) => ctx.idx.atividade(id)?.titulo ?? id);
                return html`<li>
                  <a href="#/sessao/${s.id}">
                    <b>${s.codigo}</b> · ${crianca?.nome ?? '—'} · ${dataCurta(s.criadaEm)}
                    <span class="nota">${titulos.join(' + ')}</span>
                  </a>
                </li>`;
              })}
            </ul>`
          : html`<p class="nota">Nenhuma sessão ainda. Prepare a primeira!</p>`
      }
    `,
  };
};
