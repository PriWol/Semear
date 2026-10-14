import './estilos.css';
import { abrirRepositorio } from './dados/repositorio';
import { conteudo } from './conteudo';
import { limparCachesAntigos } from './legado';
import { criarRotas, iniciarApp, type FabricaPagina } from './ui/app';
import { html } from './ui/html';
import { paginaInicio } from './pages/inicio';
import { paginaFamilia } from './pages/familia';
import { paginaCrianca } from './pages/crianca';
import { paginaJornada } from './pages/jornada';
import { paginaSessaoNova } from './pages/sessao-nova';
import { paginaSessao } from './pages/sessao';
import { paginaConfig } from './pages/config';
import { paginaConteudo } from './pages/conteudo';

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
  iniciarApp(
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
      '/conteudo': paginaConteudo,
    }),
    naoEncontrada,
  );
}

void iniciar();
void limparCachesAntigos('caches' in window ? caches : undefined);
