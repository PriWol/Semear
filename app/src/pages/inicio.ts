import { novoId, type FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { icone } from '../ui/icones';
import { idadeEmAnos } from '../domain/datas';
import { precisaLembreteBackup } from '../domain/backup';
import { pistasDaCrianca, posicaoDaLinha } from '../domain/jornada';
import { linhasParaRessondar } from '../domain/ressondagem';
import { carregarSondagem } from '../conteudo';
import { anos, dataCurta, ROTULO_FEITA, textoProgresso } from '../ui/rotulos';
import { sessaoRegistrada } from '../domain/registro';
import { criarExemplo } from '../domain/exemplo';
import { figuraGravura } from '../ui/gravura';
import { familiaSemNome } from '../domain/pendencias';
import { criancaPadrao } from '../domain/criancas';
import {
  DURACAO_PADRAO,
  montarSessaoDaProposta,
  proporSessao,
  type PropostaSessao,
} from '../domain/sessao';

export const paginaInicio: FabricaPagina = async (ctx) => {
  const familia = await ctx.repo.familia();
  if (!familia) {
    return {
      titulo: 'Bem-vindo',
      conteudo: html`<section class="cartao boas-vindas">
        ${figuraGravura('girassol')}
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
      </section>
      <section class="cartao como-funciona" aria-labelledby="como-funciona">
        <h2 id="como-funciona">Como funciona</h2>
        <ol>
          <li><b>Cadastre</b> a família e as crianças (de 2 a 8 anos).</li>
          <li>
            <b>Posicione</b> cada criança na jornada: em cada linha, toque no marco em que ela está.
          </li>
          <li>
            <b>Imprima a sessão</b>: roteiro para você, folhas para a criança e uma ficha de
            registro. Também abre no tablet, sem internet.
          </li>
        </ol>
        <p>
          Escolha a pedagogia da sua família: Montessori, Waldorf, Clássica, Religiosa ou Charlotte
          Mason. <a href="#/guia">Conheça as vertentes</a>.
        </p>
        <p class="nota">
          Privacidade: os dados das crianças ficam só neste aparelho, e o app não usa anúncios nem
          análise de uso. <a href="#/privacidade">Leia a política de privacidade</a> e os
          <a href="#/termos">Termos de uso</a>.
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
  const todasSessoes = await ctx.repo.sessoes();
  const sessoes = todasSessoes.slice(0, 6);
  // "Hoje com X" (D19): a criança da sessão mais recente, derivada das sessões (nada novo é guardado).
  const padrao = criancaPadrao(criancas, todasSessoes);
  const ultimoBackup = await ctx.repo.ultimoBackup();
  const precisaBackup = precisaLembreteBackup(criancas, ultimoBackup, agora);

  let propostaHoje: PropostaSessao | null = null;
  // A criança de hoje vem primeiro; as outras seguem na ordem de sempre.
  const ordenadas = padrao ? [padrao, ...criancas.filter((c) => c.id !== padrao.id)] : criancas;
  const cartoes = await Promise.all(
    ordenadas.map(async (c) => {
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
      // A sugestão de hoje é gerada ao abrir e não é gravada: só o toque em "Preparar sessão de hoje" cria a sessão.
      const proposta: PropostaSessao | null =
        c.id === padrao?.id
          ? proporSessao(ctx.idx, {
              familia,
              crianca: c,
              idade,
              estados,
              historico: todasSessoes.filter((x) => x.criancaId === c.id),
              duracaoMin: DURACAO_PADRAO,
              foco: 'equilibrado',
              agora,
            })
          : null;
      const sugestao = proposta !== null && proposta.escolhas.length > 0 ? proposta : null;
      if (sugestao) propostaHoje = sugestao;
      const paraRessondar = linhasParaRessondar(
        ctx.idx,
        pistasDaCrianca(ctx.idx, familia, c),
        carregarSondagem(),
        estados,
        familia.criadaEm,
        agora,
      );
      return html`<article class="cartao crianca-cartao ${c.id === padrao?.id ? 'hoje' : ''}">
        <header>
          <h2>${c.id === padrao?.id ? `Hoje com ${c.nome}` : c.nome}</h2>
          <span class="nota">${anos(idade)}</span>
          <a class="link-discreto" href="#/crianca/${c.id}" aria-label="Editar ${c.nome}">editar</a>
        </header>
        ${
          paraRessondar.length > 0
            ? html`<p class="alerta" role="note">
                ${paraRessondar.length === 1 ? '1 linha' : `${paraRessondar.length} linhas`} de
                ${c.nome} pedem uma ressondagem.
                <a href="#/sondagem/${c.id}?ressondagem=1">Fazer a ressondagem</a>
              </p>`
            : ''
        }
        ${
          posicionada
            ? html`<ul class="progresso-dominios">
                  ${[...porDominio.values()]
                    .filter((d) => d.total > 0)
                    .map(
                      (d) =>
                        html`<li>
                          <span>${icone(d.icone)} ${d.nome}</span>
                          <progress
                            max="${d.total}"
                            value="${d.cons}"
                            aria-label="${d.nome}: ${textoProgresso(d.cons, d.total)}"
                          ></progress>
                          <span class="nota">${textoProgresso(d.cons, d.total)}</span>
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
        ${
          sugestao
            ? html`<div class="hoje-sugestao">
                <p class="nota">Sugestão de hoje · cerca de ${sugestao.minutos} min</p>
                <ul>
                  ${sugestao.escolhas.map(
                    (e) =>
                      html`<li>${e.atividade.titulo} <span class="nota">${e.atividade.duracaoMin} min</span></li>`,
                  )}
                </ul>
              </div>`
            : ''
        }
        <div class="acoes">
          ${
            sugestao
              ? html`<button
                    class="botao primario grande"
                    type="button"
                    id="preparar-hoje"
                    data-crianca="${c.id}"
                  >
                    Preparar sessão de hoje
                  </button>
                  <a
                    class="botao"
                    href="#/sessao/nova?crianca=${c.id}"
                    aria-label="Mudar a sessão de ${c.nome} (duração e foco)"
                    >Mudar</a
                  >`
              : html`<a
                  class="botao primario"
                  href="#/sessao/nova?crianca=${c.id}"
                  aria-label="Preparar sessão de ${c.nome}"
                  >Preparar sessão</a
                >`
          }
          <a
            class="botao"
            href="#/sessao/registrar?crianca=${c.id}"
            aria-label="Registrar sessão de ${c.nome}"
            >Registrar sessão</a
          >
          <a class="botao" href="#/semana/${c.id}" aria-label="Planejar semana de ${c.nome}"
            >Planejar semana</a
          >
          <a
            class="botao"
            href="#/jornada/${c.id}"
            aria-label="${posicionada ? 'Ver jornada' : 'Posicionar'} de ${c.nome}"
            >${posicionada ? 'Ver jornada' : 'Posicionar'}</a
          >
        </div>
      </article>`;
    }),
  );

  return {
    titulo: 'Início',
    conteudo: html`
      <h1>${familiaSemNome(familia) ? 'Olá!' : `Olá, ${familia.educador}!`}</h1>
      ${
        familiaSemNome(familia)
          ? html`<p class="alerta" id="pendencia-nome" role="note">
              <b>Complete o nome da família.</b> <a href="#/familia">Completar agora</a>
            </p>`
          : ''
      }
      ${
        precisaBackup
          ? html`<div class="alerta">
              ${icone('floppy-disk')}
              ${
                ultimoBackup
                  ? `Seu último backup foi em ${dataCurta(ultimoBackup)}.`
                  : 'Você ainda não fez nenhum backup.'
              }
              Os dados ficam só neste aparelho. <a href="#/config">Fazer backup agora</a>
            </div>`
          : ''
      }
      ${
        criancas.length === 0
          ? html`<section class="cartao vazio-criancas">
              ${figuraGravura('gladiolo')}
              <h2>Ainda não há crianças por aqui</h2>
              <p>Cadastre a primeira para posicioná-la na jornada e preparar a sessão.</p>
              <a class="botao primario" href="#/crianca/nova">Adicionar a primeira criança</a>
            </section>`
          : html`<div class="grade-cartoes">${cartoes}</div>`
      }
      <div class="acoes" id="atalhos-inicio">
        <a class="botao" href="#/crianca/nova">+ Adicionar criança</a>
        <a class="botao" href="#/biblioteca">${icone('books')} Biblioteca</a>
        <a class="botao" href="#/acervo">${icone('gift')} Acervo gratuito</a>
        <a class="botao" href="#/guia">${icone('compass')} Guia das vertentes</a>
      </div>

      <h2>Últimas sessões</h2>
      ${
        sessoes.length
          ? html`<ul class="lista-sessoes">
              ${sessoes.map((s) => {
                const crianca = criancas.find((c) => c.id === s.criancaId);
                const titulos = s.atividadeIds.map((id) => ctx.idx.atividade(id)?.titulo ?? id);
                return html`<li>
                  <a href="#/sessao/${s.id}">
                    <span
                      ><b>${s.codigo}</b> · ${crianca?.nome ?? '—'} · ${dataCurta(s.criadaEm)}
                      ${sessaoRegistrada(s) ? html`<span class="selo-feita">${ROTULO_FEITA}</span>` : ''}</span
                    >
                    <span class="nota">${titulos.join(' + ')}</span>
                  </a>
                </li>`;
              })}
            </ul>`
          : html`<p class="nota">Nenhuma sessão ainda. Prepare a primeira!</p>`
      }
    `,
    montar(raiz) {
      const botao = raiz.querySelector<HTMLButtonElement>('#preparar-hoje');
      const proposta = propostaHoje;
      const crianca = criancas.find((c) => c.id === botao?.dataset.crianca);
      if (!botao || !proposta || !crianca) return;
      botao.addEventListener('click', async () => {
        botao.disabled = true; // um toque duplo não cria duas sessões
        try {
          const existentes = (await ctx.repo.sessoes()).map((s) => s.codigo);
          const sessao = montarSessaoDaProposta({
            id: novoId(),
            crianca,
            proposta,
            foco: 'equilibrado',
            agora: ctx.agora(), // a hora do toque, não a de quando a tela abriu
            codigosExistentes: existentes,
          });
          await ctx.repo.salvarSessao(sessao);
          // A prévia continua antes de imprimir: a mãe confere idade, atividades e tempo na página da sessão.
          ctx.ir(`/sessao/${sessao.id}`);
        } catch (erro) {
          console.error(erro);
          botao.disabled = false;
          ctx.avisar('Não foi possível preparar a sessão. Tente de novo.', 'alerta');
        }
      });
    },
  };
};
