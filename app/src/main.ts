import './estilos.css';
import { registerSW } from 'virtual:pwa-register';
import { VERSAO } from './versao';
import { rotuloVersao } from './ui/versao';
import { paginaNovidades } from './pages/novidades';
import './tokens.css';
import { abrirRepositorio } from './dados/repositorio';
import { conteudo } from './conteudo';
import { limparCachesAntigos } from './legado';
import { atualizarFaixaExemplo, ligarFaixaExemplo } from './ui/exemplo';
import { criarRotas, iniciarApp, type FabricaPagina } from './ui/app';
import { html } from './ui/html';
import { paginaInicio } from './pages/inicio';
import { paginaFamilia } from './pages/familia';
import { paginaCrianca } from './pages/crianca';
import { paginaJornada } from './pages/jornada';
import { paginaSessaoNova } from './pages/sessao-nova';
import { paginaSessao } from './pages/sessao';
import { paginaConfig } from './pages/config';
import { paginaBiblioteca } from './pages/biblioteca';
import { paginaConteudo } from './pages/conteudo';
import { paginaAcervo } from './pages/acervo';

const naoEncontrada: FabricaPagina = async () => ({
  titulo: 'Não encontrada',
  conteudo: html`<section class="cartao">
    <h1>Página não encontrada</h1>
    <p><a href="#/">Voltar ao início</a></p>
  </section>`,
});

async function iniciar() {
  const raiz = document.getElementById('app');
  if (!raiz) return;
  const repo = await abrirRepositorio();
  const ctx = iniciarApp(
    raiz,
    { repo, idx: conteudo(), agora: () => new Date().toISOString() },
    criarRotas({
      '/': paginaInicio,
      '/familia': paginaFamilia,
      '/crianca/:id': paginaCrianca,
      '/jornada/:id': paginaJornada,
      '/sessao/nova': paginaSessaoNova,
      '/sessao/:id': paginaSessao,
      '/config': paginaConfig,
      '/biblioteca': paginaBiblioteca,
      '/acervo': paginaAcervo,
      '/conteudo': paginaConteudo,
      '/novidades': paginaNovidades,
    }),
    naoEncontrada,
    atualizarFaixaExemplo,
  );
  ligarFaixaExemplo(ctx);
  mostrarVersao();
  // Depois da primeira renderização, para não disputar a abertura do app (ADR 0009).
  void limparCachesAntigos('caches' in window ? caches : undefined);
}

/** Versão no topo e aviso de versão nova (#38). */
function mostrarVersao() {
  const rotulo = document.getElementById('versao');
  if (rotulo) rotulo.textContent = rotuloVersao(VERSAO);

  const faixa = document.getElementById('faixa-atualizar');
  // Com registerType "prompt", a versão nova fica esperando: o educador escolhe a hora de trocar.
  const atualizar = registerSW({
    onNeedRefresh() {
      if (faixa) faixa.hidden = false;
    },
    // Um app aberto por dias só procuraria versão nova quando o navegador quisesse: conferimos de hora em hora.
    onRegisteredSW(_url, registro) {
      if (!registro) return;
      setInterval(
        () => {
          if (navigator.onLine) void registro.update().catch(() => undefined);
        },
        60 * 60 * 1000,
      );
    },
    onRegisterError(erro) {
      console.error('Não foi possível registrar o service worker.', erro);
    },
  });
  document.getElementById('atualizar-app')?.addEventListener('click', () => void atualizar(true));
}

void iniciar();
