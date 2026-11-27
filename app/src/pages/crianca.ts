import { lerFormulario, lista, NaoEncontrado, novoId, type FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { IDIOMAS, LETRAS, type Crianca, type Idioma } from '../domain/tipos';
import { faixaEtaria } from '../domain/faixa';
import { idadeEmAnos, MENSAGEM_NASCIMENTO, problemaDeNascimento } from '../domain/datas';
import { camposAlterados } from '../domain/campos';
import { ehLetra } from '../domain/letra';
import { letraPadrao, NOME_LETRA } from '../domain/letra';
import { avisoExemplo, ligarAvisoExemplo } from '../ui/exemplo';
import { abrirDialogo } from '../ui/dialogo';
import { baixarArquivo } from './sessao';

export const paginaCrianca: FabricaPagina = async (ctx, params) => {
  const familia = await ctx.repo.familia();
  if (!familia)
    return {
      titulo: 'Família',
      conteudo: html`<p>Cadastre a família primeiro. <a href="#/familia">Começar</a></p>`,
    };
  const id = params.id ?? 'nova';
  const existente = id === 'nova' ? null : await ctx.repo.crianca(id);
  if (id !== 'nova' && !existente) throw new NaoEncontrado('criança');
  const c: Crianca = existente ?? {
    id: novoId(),
    nome: '',
    nascimento: '',
    letra: null,
    trilhas: [],
  };
  const agora = new Date(ctx.agora());
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
      <form class="cartao formulario formulario-colunas" id="form-crianca">
        <label
          >Nome <input name="nome" required maxlength="40" pattern=".*\\S.*" value="${c.nome}"
        /></label>
        <label>
          Data de nascimento
          <input name="nascimento" type="date" required value="${c.nascimento}" />
          <span class="nota">O Semear é pensado para crianças de 2 a 8 anos.</span>
        </label>
        <p class="alerta" id="aviso-faixa" role="status" hidden>
          Esta criança está fora da faixa de 2 a 8 anos para a qual o Semear foi pensado. Você pode
          salvar mesmo assim: as atividades podem não servir bem para a idade.
        </p>
        <p class="alerta erro" id="erro-nascimento" role="alert" hidden></p>
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
      const campoNascimento = raiz.querySelector<HTMLInputElement>('[name=nascimento]');
      const avisoFaixa = raiz.querySelector<HTMLElement>('#aviso-faixa');
      const erroNascimento = raiz.querySelector<HTMLElement>('#erro-nascimento');
      const atualizarAvisoFaixa = () => {
        if (!avisoFaixa || !campoNascimento) return;
        const faixa = faixaEtaria(campoNascimento.value, agora);
        avisoFaixa.hidden = !(faixa === 'abaixo' || faixa === 'acima');
        if (erroNascimento) erroNascimento.hidden = true;
      };
      atualizarAvisoFaixa();
      campoNascimento?.addEventListener('input', atualizarAvisoFaixa);
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
          // Bloqueia só o impossível (futuro, mais de 18 anos, data que não existe), com a mensagem na tela.
          const problema = problemaDeNascimento(nova.nascimento, agora);
          if (problema && erroNascimento) {
            erroNascimento.textContent = MENSAGEM_NASCIMENTO[problema];
            erroNascimento.hidden = false;
            campoNascimento?.focus();
            return;
          }
          // Criança existente: grava só o que mudou (QA1-03); a nova entra inteira.
          if (existente) await ctx.repo.atualizarCrianca(c.id, camposAlterados(existente, nova));
          else await ctx.repo.salvarCrianca(nova);
          // Só avisa: um irmão fora da faixa pode usar o app, mas as atividades são feitas para 2 a 8 anos.
          const foraDaFaixa = faixaEtaria(nova.nascimento, agora);
          // Aviso de verdade (a pessoa precisa ler): fica até ser fechado.
          if (foraDaFaixa === 'abaixo' || foraDaFaixa === 'acima') {
            ctx.avisar(
              'Dados salvos. Atenção: o Semear é pensado para crianças de 2 a 8 anos.',
              'alerta',
            );
          } else {
            ctx.avisar('Dados salvos.');
          }
          // Criança nova: tela de próximo passo (D21), não uma jornada de milhares de pixels.
          ctx.ir(existente ? '/' : `/crianca/${nova.id}/pronta`);
        });
      raiz.querySelector('#remover')?.addEventListener('click', async () => {
        // Caixa própria (QA2-04): verbo e nome no botão de perigo, e "guardar uma cópia" antes, sem sair da caixa.
        let guardou = false;
        const escolha = await abrirDialogo({
          titulo: `Remover ${c.nome}?`,
          texto: html`<p>Saem o cadastro e todo o histórico de ${c.nome}. Isso não pode ser desfeito.</p>
            <p>Se quiser ficar com os dados, guarde uma cópia antes.</p>`,
          botoes: [
            {
              valor: 'copia',
              rotulo: 'Guardar uma cópia antes',
              tipo: 'primario',
              mantemAberto: true,
            },
            { valor: 'remover', rotulo: `Remover ${c.nome}`, tipo: 'perigo' },
            { valor: 'cancelar', rotulo: `Manter ${c.nome}`, tipo: 'neutro' },
          ],
          aoEscolher: async () => {
            const agora = ctx.agora();
            const backup = await ctx.repo.exportar(agora);
            baixarArquivo(
              `semear-backup-${agora.slice(0, 10)}.json`,
              JSON.stringify(backup, null, 2),
              'application/json',
            );
            await ctx.repo.marcarBackup(agora);
            guardou = true;
            return 'Cópia guardada. Agora você pode remover, se quiser.';
          },
        });
        if (escolha !== 'remover') return;
        await ctx.repo.removerCrianca(c.id);
        ctx.avisar(guardou ? 'Criança removida. A cópia ficou guardada.' : 'Criança removida.');
        ctx.ir('/');
      });
    },
  };
};
