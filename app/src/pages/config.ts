import type { FabricaPagina } from '../ui/app';
import { html } from '../ui/html';
import { validarBackup } from '../dados/repositorio';
import { dataCurta } from '../ui/rotulos';
import { baixarArquivo } from './sessao';

export const paginaConfig: FabricaPagina = async (ctx) => {
  const ultimo = await ctx.repo.ultimoBackup();
  const persistente = (await navigator.storage?.persisted?.()) ?? false;

  return {
    titulo: 'Configurações',
    conteudo: html`
      <h1>Configurações</h1>
      <section class="cartao">
        <h2>💾 Backup</h2>
        <p>
          Seus dados ficam <b>só neste aparelho</b>. Faça backup com frequência e guarde o arquivo
          num lugar seguro (e-mail, nuvem, pendrive).
        </p>
        <p class="nota">
          Último backup: ${ultimo ? dataCurta(ultimo) : 'nunca'}.
          ${persistente ? 'Armazenamento persistente ativado.' : 'O navegador pode limpar os dados se faltar espaço.'}
        </p>
        <div class="acoes">
          <button class="botao primario" type="button" id="exportar">Baixar backup</button>
          <label class="botao">
            Restaurar backup
            <input type="file" accept="application/json,.json" id="importar" hidden />
          </label>
        </div>
      </section>
      <section class="cartao">
        <h2>Família e conteúdo</h2>
        <div class="acoes">
          <a class="botao" href="#/familia">Editar família</a>
          <a class="botao" href="#/conteudo">Ver cobertura do conteúdo</a>
        </div>
      </section>
      <section class="cartao">
        <h2>Apagar dados</h2>
        <p class="nota">Remove família, crianças, jornada e sessões deste aparelho.</p>
        <button class="botao perigo" type="button" id="apagar">Apagar tudo</button>
      </section>
    `,
    montar(raiz) {
      raiz.querySelector('#exportar')?.addEventListener('click', async () => {
        const agora = ctx.agora();
        const backup = await ctx.repo.exportar(agora);
        baixarArquivo(
          `semear-backup-${agora.slice(0, 10)}.json`,
          JSON.stringify(backup, null, 2),
          'application/json',
        );
        await ctx.repo.marcarBackup(agora);
        await ctx.atualizar();
        ctx.avisar('Backup baixado.');
      });
      raiz.querySelector<HTMLInputElement>('#importar')?.addEventListener('change', async (ev) => {
        const arquivo = (ev.target as HTMLInputElement).files?.[0];
        if (!arquivo) return;
        try {
          const dados: unknown = JSON.parse(await arquivo.text());
          validarBackup(dados);
          if (!confirm('Restaurar este backup? Os dados atuais deste aparelho serão substituídos.'))
            return;
          await ctx.repo.importar(dados);
          ctx.avisar('Backup restaurado.');
          ctx.ir('/');
        } catch (erro) {
          alert(erro instanceof Error ? erro.message : 'Não foi possível ler o arquivo.');
        }
      });
      raiz.querySelector('#apagar')?.addEventListener('click', async () => {
        if (!confirm('Apagar TODOS os dados deste aparelho? Faça um backup antes.')) return;
        await ctx.repo.apagarTudo();
        ctx.ir('/');
      });
    },
  };
};
