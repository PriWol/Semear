// Tela de Ajustes (antes "Configurações"; a rota #/config continua para não quebrar links e favoritos).
// Seis grupos, na ordem do que se usa: Família, Aviso diário, Cópia de segurança, Material de apoio,
// Sobre o Semear e, por último, Cuidado (ações sem volta). Tudo fica neste aparelho (ADR 0002).
import './ajustes.css';
import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { validarBackup } from '../dados/repositorio';
import { dataCurta } from '../ui/rotulos';
import { horaDe24h, LEMBRETE_PADRAO } from '../domain/lembretes';
import { arquivoGrandeDemais, MENSAGEM_ARQUIVO_GRANDE, resumoUltimaCopia } from '../domain/backup';
import { confirmacaoApagarTudo, PALAVRA_APAGAR } from '../domain/confirmacao';
import { ponteDoAparelho } from '../nativo/lembretes';
import {
  apagarTudoECancelarLembretes,
  AVISO_LEMBRETES_NAO_CANCELADOS,
  sincronizarComOAparelho,
} from '../nativo/sincronizar';
import { baixarArquivo } from './sessao';
import { VERSAO } from '../versao';
import { numeroCurto } from '../ui/versao';
import { CREDITO_GRAVURAS } from '../gravuras';
import { abrirDialogo, paragrafo } from '../ui/dialogo';
import { sairDoExemplo } from '../ui/exemplo';

const plural = (n: number, um: string, varios: string) => `${n} ${n === 1 ? um : varios}`;

export const paginaConfig: FabricaPagina = async (ctx) => {
  const ultimo = await ctx.repo.ultimoBackup();
  const persistente = (await navigator.storage?.persisted?.()) ?? false;
  const familia = await ctx.repo.familia();
  const criancas = await ctx.repo.criancas();
  const lembrete = familia?.lembrete ?? LEMBRETE_PADRAO;
  const noAplicativo = ponteDoAparelho(window as never) !== null;
  const copia = resumoUltimaCopia(ultimo, ctx.agora());
  const [horaAviso = '08', minutoAviso = '00'] = lembrete.hora.split(':');
  const ultimaCopiaTexto =
    copia.dias === null
      ? 'nunca'
      : copia.dias === 0
        ? 'hoje'
        : `há ${plural(copia.dias, 'dia', 'dias')}`;

  return {
    titulo: 'Ajustes',
    conteudo: html`
      <div class="ajustes">
        <h1>Ajustes</h1>
        <p class="ajustes-sub">
          Seus dados, avisos e cópias de segurança. Tudo fica neste aparelho.
        </p>

        <section class="cartao" aria-labelledby="aj-familia">
          <h2 id="aj-familia">Família</h2>
          ${
            familia
              ? html`<p class="ajustes-resumo">
                  Família ${familia.educador} · ${plural(criancas.length, 'criança', 'crianças')}
                </p>
                <a class="botao" href="#/familia">Dados da família e das crianças</a>`
              : html`<p>Você ainda não cadastrou a família.</p>
                <a class="botao primario" href="#/familia">Cadastrar a família</a>`
          }
        </section>

        <section class="cartao" aria-labelledby="aj-aviso">
          <h2 id="aj-aviso">Aviso diário</h2>
          ${
            familia
              ? html`
                ${
                  noAplicativo
                    ? ''
                    : html`<p class="nota ajustes-so-app">
                      Os avisos só funcionam no aplicativo de celular. Aqui no navegador você já pode
                      deixar a escolha feita.
                    </p>`
                }
                <p>
                  Todo dia, na hora que você escolher, o aviso lembra das atividades do plano da
                  semana que são de hoje. Ele é criado <b>neste aparelho</b>: nada é enviado a
                  servidor.
                </p>
                <p class="nota">
                  O aviso aparece na tela bloqueada. Por isso, o nome da criança só aparece se você
                  marcar a última opção.
                </p>
                <form class="formulario" id="form-lembrete" novalidate>
                  <label class="opcao"
                    ><input type="checkbox" name="ativo" ${lembrete.ativo ? 'checked' : ''} /> Me
                    avisar das atividades do dia</label
                  >
                  <fieldset class="ajustes-hora">
                    <legend>Hora do aviso (24 horas)</legend>
                    <label
                      >Hora
                      <input
                        type="text"
                        inputmode="numeric"
                        name="hora"
                        maxlength="2"
                        autocomplete="off"
                        value="${horaAviso}"
                        aria-describedby="erro-hora"
                      />
                    </label>
                    <span class="ajustes-dois-pontos" aria-hidden="true">:</span>
                    <label
                      >Minutos
                      <input
                        type="text"
                        inputmode="numeric"
                        name="minuto"
                        maxlength="2"
                        autocomplete="off"
                        value="${minutoAviso}"
                        aria-describedby="erro-hora"
                      />
                    </label>
                  </fieldset>
                  <p class="alerta erro" id="erro-hora" role="alert" hidden></p>
                  <label class="opcao"
                    ><input
                      type="checkbox"
                      name="incluirNome"
                      ${lembrete.incluirNome ? 'checked' : ''}
                    />
                    Mostrar o nome da criança no aviso (na tela bloqueada)</label
                  >
                  <div class="acoes">
                    <button class="botao primario" type="submit">Salvar aviso</button>
                  </div>
                </form>
              `
              : html`<p class="nota">Cadastre a família para escolher o aviso diário.</p>`
          }
        </section>

        <section class="cartao" aria-labelledby="aj-copia">
          <h2 id="aj-copia">Cópia de segurança</h2>
          <p class="ajustes-ultima${copia.alerta ? ' ajustes-ultima-alerta' : ''}">
            <b>Última cópia: ${ultimaCopiaTexto}</b>${ultimo ? ` (${dataCurta(ultimo)})` : ''}
          </p>
          ${
            copia.estado === 'antiga'
              ? html`<p class="alerta" role="note">
                Faz ${copia.dias} dias que você não guarda uma cópia. Guarde uma agora: se o aparelho
                se perder, os dados também.
              </p>`
              : ''
          }
          ${
            copia.estado === 'nunca'
              ? html`<p class="alerta" role="note">
                Você ainda não guardou nenhuma cópia. Guarde uma: se o aparelho se perder, os dados
                também.
              </p>`
              : ''
          }
          <div class="acoes">
            <button class="botao primario" type="button" id="exportar">
              Guardar uma cópia dos meus dados
            </button>
            <button class="botao" type="button" id="importar-botao">Trazer uma cópia guardada</button>
            <input
              type="file"
              accept="application/json,.json"
              id="importar"
              hidden
              tabindex="-1"
              aria-hidden="true"
            />
          </div>
          <p class="alerta erro" id="erro-copia" role="alert" hidden></p>
          <details class="ajustes-detalhe">
            <summary>O que tem na cópia?</summary>
            <p>
              Os nomes, as datas de nascimento, a jornada das crianças e as anotações das sessões. O
              arquivo <b>não é protegido por senha</b>: guarde num lugar seguro (e-mail, nuvem,
              pendrive) e não compartilhe com outras pessoas.
            </p>
            <p>
              Para passar para outro celular: guarde a cópia aqui e use “Trazer uma cópia guardada”
              no outro aparelho.
            </p>
            <p class="nota">
              ${
                persistente
                  ? 'O armazenamento deste aparelho está protegido contra limpeza automática.'
                  : 'O navegador pode limpar os dados se faltar espaço; uma cópia guardada resolve.'
              }
            </p>
          </details>
        </section>

        <section class="cartao" aria-labelledby="aj-material">
          <h2 id="aj-material">Material de apoio</h2>
          <ul class="ajustes-lista">
            <li>
              <a href="#/biblioteca">Biblioteca</a>
              <span class="nota">O Grande Tesouro de Marina: o material para imprimir ou ler na tela.</span>
            </li>
            <li>
              <a href="#/acervo">Acervo gratuito</a>
              <span class="nota">Obras de domínio público ou licença aberta, com busca neste aparelho.</span>
            </li>
          </ul>
        </section>

        <section class="cartao" id="sobre" aria-labelledby="aj-sobre">
          <h2 id="aj-sobre">Sobre o Semear</h2>
          <p>
            Versão <b>${numeroCurto(VERSAO.numero)}</b> · ${dataCurta(VERSAO.data)}. Seus dados ficam
            só neste aparelho.
          </p>
          <ul class="ajustes-links">
            <li><a href="#/novidades">Novidades</a></li>
            <li><a href="#/privacidade">Privacidade</a></li>
            <li><a href="#/termos">Termos de uso</a></li>
            <li><a href="#/conteudo">Cobertura do conteúdo</a></li>
          </ul>
          <details class="ajustes-detalhe" id="creditos-gravuras">
            <summary>Créditos das gravuras</summary>
            <p>${CREDITO_GRAVURAS}</p>
          </details>
          <details class="ajustes-detalhe">
            <summary>Detalhes técnicos</summary>
            <p>
              Versão completa <b>${VERSAO.numero}</b> · publicada em ${dataCurta(VERSAO.data)} ·
              código <code>${VERSAO.commit}</code>
            </p>
          </details>
        </section>

        <section class="cartao ajustes-cuidado" aria-labelledby="aj-cuidado">
          <h2 id="aj-cuidado">Cuidado</h2>
          <p>
            Estas ações não têm volta. Antes, guarde uma cópia dos seus dados. Há duas: uma tira só a
            família de exemplo; a outra tira tudo.
          </p>
          ${
            familia?.exemplo
              ? html`<div class="ajustes-acao">
                <p>
                  <b>Apagar o exemplo</b> remove só a família de exemplo e as sessões dela. O que você
                  cadastrou fica.
                </p>
                <button class="botao perigo" type="button" id="apagar-exemplo-ajustes">
                  Apagar o exemplo
                </button>
              </div>`
              : ''
          }
          <div class="ajustes-acao">
            <p>
              <b>Apagar todos os dados</b> remove a família, as crianças, as sessões e os avisos deste
              aparelho, inclusive o que você cadastrou.
            </p>
            <button class="botao perigo" type="button" id="apagar">
              Apagar todos os dados deste aparelho
            </button>
          </div>
        </section>
      </div>
    `,
    montar(raiz) {
      const erroCopia = raiz.querySelector<HTMLElement>('#erro-copia');
      const mostrarErroCopia = (msg: string) => {
        if (!erroCopia) return;
        erroCopia.textContent = msg;
        erroCopia.hidden = false;
      };

      /** Gera o arquivo, baixa e anota a data. Usada pelo botão e pela caixa de "Apagar tudo". */
      const guardarCopia = async () => {
        const agora = ctx.agora();
        const backup = await ctx.repo.exportar(agora);
        baixarArquivo(
          `semear-backup-${agora.slice(0, 10)}.json`,
          JSON.stringify(backup, null, 2),
          'application/json',
        );
        await ctx.repo.marcarBackup(agora);
      };

      raiz.querySelector('#exportar')?.addEventListener('click', async () => {
        await guardarCopia();
        await ctx.atualizar();
        ctx.avisar('Cópia guardada.');
      });

      // Botão real (alcançável por teclado e leitor de tela) que abre o seletor do campo de arquivo.
      const campoArquivo = raiz.querySelector<HTMLInputElement>('#importar');
      raiz.querySelector('#importar-botao')?.addEventListener('click', () => campoArquivo?.click());
      campoArquivo?.addEventListener('change', async (ev) => {
        const campo = ev.target as HTMLInputElement;
        const arquivo = campo.files?.[0];
        campo.value = ''; // permite escolher o mesmo arquivo de novo se esta tentativa falhar
        if (!arquivo) return;
        if (erroCopia) erroCopia.hidden = true;
        try {
          // D23: o tamanho vem de `File.size`, então nada é lido (nem JSON.parse) de um arquivo enorme.
          if (arquivoGrandeDemais(arquivo.size)) throw new Error(MENSAGEM_ARQUIVO_GRANDE);
          let dados: unknown;
          try {
            dados = JSON.parse(await arquivo.text());
          } catch {
            throw new Error('Este arquivo não parece ser uma cópia do Semear: não consegui lê-lo.');
          }
          // Todo dado de fora é validado antes de qualquer uso (privacidade, CLAUDE.md).
          validarBackup(dados);
          const escolha = await abrirDialogo({
            titulo: 'Trazer esta cópia?',
            texto: paragrafo(
              'Os dados atuais deste aparelho serão substituídos pelos da cópia. Não dá para desfazer.',
            ),
            botoes: [
              { valor: 'trazer', rotulo: 'Substituir os dados', tipo: 'perigo' },
              { valor: 'cancelar', rotulo: 'Cancelar', tipo: 'neutro' },
            ],
          });
          if (escolha !== 'trazer') return;
          await ctx.repo.importar(dados);
          ctx.avisar('Cópia trazida.');
          ctx.ir('/');
        } catch (erro) {
          mostrarErroCopia(
            erro instanceof Error ? erro.message : 'Não foi possível ler o arquivo.',
          );
        }
      });

      raiz
        .querySelector<HTMLFormElement>('#form-lembrete')
        ?.addEventListener('submit', async (ev) => {
          ev.preventDefault();
          const dados = new FormData(ev.currentTarget as HTMLFormElement);
          const erroHora = raiz.querySelector<HTMLElement>('#erro-hora');
          const hora = horaDe24h(
            String(dados.get('hora') ?? ''),
            String(dados.get('minuto') ?? ''),
          );
          if (!hora || !familia) {
            if (erroHora) {
              erroHora.textContent =
                'Escolha uma hora de 0 a 23 e minutos de 0 a 59. Exemplo: hora 7, minutos 30.';
              erroHora.hidden = false;
            }
            return;
          }
          if (erroHora) erroHora.hidden = true;
          // Só o lembrete: a família lida ao abrir a tela pode estar velha (QA1-03).
          await ctx.repo.atualizarFamilia({
            lembrete: {
              ativo: dados.get('ativo') !== null,
              hora,
              incluirNome: dados.get('incluirNome') !== null,
            },
          });
          const r = await sincronizarComOAparelho(ctx, { pedirPermissao: true });
          if (r === 'sem-permissao') {
            ctx.avisar(
              'Preferência salva, mas as notificações estão bloqueadas nas configurações do celular.',
              'alerta',
            );
          } else {
            ctx.avisar('Aviso salvo.');
          }
        });

      raiz.querySelector('#apagar-exemplo-ajustes')?.addEventListener('click', () =>
        // Confirmação simples: o que a pessoa cadastrou continua (ADR 0013).
        sairDoExemplo(ctx, '/', async () => {
          const escolha = await abrirDialogo({
            titulo: 'Apagar o exemplo?',
            texto: paragrafo(
              'Saem a família de exemplo, a Ana, o Theo e as sessões deles. O que você cadastrou continua neste aparelho.',
            ),
            botoes: [
              { valor: 'apagar', rotulo: 'Apagar o exemplo', tipo: 'perigo' },
              { valor: 'cancelar', rotulo: 'Cancelar', tipo: 'neutro' },
            ],
          });
          return escolha === 'apagar';
        }),
      );

      raiz.querySelector('#apagar')?.addEventListener('click', async () => {
        let guardou = false;
        const escolha = await abrirDialogo({
          titulo: 'Apagar tudo neste aparelho?',
          texto: html`<p>
              Saem a família, as crianças, as sessões e os avisos. Não dá para desfazer.
            </p>
            <p>Se quiser ficar com os dados, guarde uma cópia antes.</p>`,
          palavra: {
            rotulo: `Para confirmar, digite ${PALAVRA_APAGAR}`,
            valida: confirmacaoApagarTudo,
          },
          botoes: [
            {
              valor: 'copia',
              rotulo: 'Guardar uma cópia primeiro',
              tipo: 'primario',
              mantemAberto: true,
            },
            {
              valor: 'apagar',
              rotulo: 'Apagar mesmo assim',
              tipo: 'perigo',
              soComPalavra: true,
            },
            { valor: 'cancelar', rotulo: 'Cancelar', tipo: 'neutro' },
          ],
          aoEscolher: async () => {
            await guardarCopia();
            guardou = true;
            return 'Cópia guardada. Agora você pode apagar, se quiser.';
          },
        });
        if (escolha !== 'apagar') {
          if (guardou) await ctx.atualizar(); // mostra a nova data da última cópia
          return;
        }
        const resultado = await apagarTudoECancelarLembretes(ctx.repo);
        ctx.ir('/');
        // Os dados já foram apagados; se os lembretes (que podem mostrar o nome da criança) seguirem
        // agendados, a pessoa precisa saber (#25).
        if (resultado === 'lembretes-nao-cancelados')
          ctx.avisar(AVISO_LEMBRETES_NAO_CANCELADOS, 'alerta');
      });
    },
  };
};
