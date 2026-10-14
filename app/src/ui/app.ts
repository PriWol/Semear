// Casca do app: rotas por hash (ADR 0008), contexto compartilhado e renderização das páginas.
import type { Repositorio } from '../dados/repositorio';
import type { IndiceConteudo } from '../domain/conteudo';
import { html, type HtmlSeguro } from './html';

export interface Contexto {
  repo: Repositorio;
  idx: IndiceConteudo;
  /** data/hora atual em ISO; injetável para facilitar testes */
  agora: () => string;
  ir: (rota: string) => void;
  /** renderiza de novo a página atual (após uma ação) */
  atualizar: () => Promise<void>;
  avisar: (mensagem: string) => void;
}

export interface Pagina {
  titulo: string;
  conteudo: HtmlSeguro;
  /** liga eventos depois que o HTML está na tela */
  montar?: (raiz: HTMLElement) => void;
}

export type FabricaPagina = (ctx: Contexto, params: Record<string, string>) => Promise<Pagina>;

interface Rota {
  padrao: RegExp;
  nomes: string[];
  fabrica: FabricaPagina;
}

export function criarRotas(defs: Record<string, FabricaPagina>): Rota[] {
  return Object.entries(defs).map(([caminho, fabrica]) => {
    const nomes: string[] = [];
    const padrao = new RegExp(
      '^' +
        caminho.replace(/:([a-z]+)/g, (_, nome: string) => {
          nomes.push(nome);
          return '([^/?]+)';
        }) +
        '$',
    );
    return { padrao, nomes, fabrica };
  });
}

/** Separa "#/sessao/nova?crianca=x" em caminho e parâmetros. */
export function lerHash(hash: string): { caminho: string; query: Record<string, string> } {
  const semHash = hash.replace(/^#/, '') || '/';
  const [caminho = '/', busca = ''] = semHash.split('?');
  return { caminho, query: Object.fromEntries(new URLSearchParams(busca)) };
}

export function iniciarApp(
  raiz: HTMLElement,
  base: Omit<Contexto, 'ir' | 'atualizar' | 'avisar'>,
  rotas: Rota[],
  naoEncontrada: FabricaPagina,
  /** roda depois de cada página (ex.: atualizar a faixa do exemplo, #39) */
  depoisDeRenderizar?: (ctx: Contexto) => Promise<void>,
): Contexto {
  const aviso = document.getElementById('aviso');
  let timer: number | undefined;

  const ctx: Contexto = {
    ...base,
    ir: (rota) => {
      if (location.hash === `#${rota}`) void renderizar();
      else location.hash = rota;
    },
    atualizar: () => renderizar(),
    avisar: (mensagem) => {
      if (!aviso) return;
      aviso.textContent = mensagem;
      aviso.hidden = false;
      clearTimeout(timer);
      timer = window.setTimeout(() => (aviso.hidden = true), 3500);
    },
  };

  async function renderizar() {
    const { caminho, query } = lerHash(location.hash);
    let fabrica = naoEncontrada;
    const params: Record<string, string> = { ...query };
    for (const r of rotas) {
      const m = r.padrao.exec(caminho);
      if (m) {
        fabrica = r.fabrica;
        r.nomes.forEach((n, i) => (params[n] = decodeURIComponent(m[i + 1]!)));
        break;
      }
    }
    try {
      const pagina = await fabrica(ctx, params);
      document.title = `${pagina.titulo} · Semear`;
      const el = document.createElement('div');
      el.className = 'pagina-app';
      el.innerHTML = pagina.conteudo.valor;
      raiz.replaceChildren(el);
      pagina.montar?.(el);
      marcarNavegacao(caminho);
      await depoisDeRenderizar?.(ctx);
    } catch (erro) {
      console.error(erro);
      raiz.innerHTML = html`<div class="cartao erro">
        <h1>Algo deu errado</h1>
        <p>${erro instanceof Error ? erro.message : String(erro)}</p>
        <p><a href="#/">Voltar ao início</a></p>
      </div>`.valor;
    }
  }

  window.addEventListener('hashchange', () => {
    void renderizar();
    window.scrollTo(0, 0);
  });
  void renderizar();
  return ctx;
}

function marcarNavegacao(caminho: string) {
  document.querySelectorAll<HTMLAnchorElement>('nav a[data-rota]').forEach((a) => {
    const rota = a.dataset.rota ?? '';
    const ativo = rota === '/' ? caminho === '/' : caminho.startsWith(rota);
    a.classList.toggle('ativo', ativo);
    if (ativo) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
}

/** Lê um formulário como objeto de strings; campos repetidos (checkbox) viram listas. */
export function lerFormulario(form: HTMLFormElement): Record<string, string | string[]> {
  const dados: Record<string, string | string[]> = {};
  for (const [k, v] of new FormData(form)) {
    const valor = String(v);
    const atual = dados[k];
    if (atual === undefined) dados[k] = valor;
    else dados[k] = Array.isArray(atual) ? [...atual, valor] : [atual, valor];
  }
  return dados;
}

export const lista = (v: string | string[] | undefined): string[] =>
  v === undefined ? [] : Array.isArray(v) ? v : [v];

export function novoId(): string {
  return crypto.randomUUID();
}
