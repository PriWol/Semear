// Gera o documento HTML completo do pacote de uma sessão (ADR 0004, especificação §5.7).
import type {
  Atividade,
  Crianca,
  Familia,
  Letra,
  Livro,
  Marco,
  Sessao,
  Vertente,
} from '../domain/tipos';
import { ehLetra, NOME_LETRA } from '../domain/letra';
import { dataBR } from '../domain/datas';
import { rotuloDoMaterial } from '../domain/material';
import { escapar, html, textoRico, type HtmlSeguro } from '../ui/html';
import { paginaDaFolha } from './folhas';
import tokens from '../tokens.css?raw';
import estilos from './pacote.css?raw';

export interface EntradaPacote {
  sessao: Sessao;
  familia: Familia;
  crianca: Crianca;
  idade: number;
  letra: Letra;
  atividades: Atividade[];
  livro: Livro | null;
  /** busca de marcos para mostrar os títulos na ficha */
  marco: (id: string) => Marco | undefined;
}

const USO_LIVRO: Record<Livro['uso'], string> = {
  'leitura-em-voz-alta': 'leitura em voz alta',
  'leitura-pela-crianca': 'leitura pela criança',
  'apoio-ao-educador': 'apoio ao educador',
};

function rodapeEducador(texto: string, pagina: string): HtmlSeguro {
  return html`<div class="rodape"><span>${texto}</span><span>${pagina}</span></div>`;
}

function cabecalhoMeta(e: EntradaPacote): HtmlSeguro {
  const vertentes = [e.familia.vertentePrincipal, ...e.familia.inspiracoes].join(' + ');
  const minutos = e.atividades.reduce((t, a) => t + a.duracaoMin, 0);
  return html`<div class="meta">
    <div><b>Criança</b>${e.crianca.nome}, ${Math.floor(e.idade)} anos</div>
    <div><b>Duração</b>~${minutos} min</div>
    <div><b>Vertente</b>${vertentes}</div>
    <div><b>Código</b>${e.sessao.codigo}</div>
  </div>`;
}

function roteiroDaAtividade(a: Atividade, e: EntradaPacote, primeira: boolean): HtmlSeguro {
  const nomeMarco = (id: string) => `${id} · ${e.marco(id)?.titulo ?? ''}`;
  return html`<div class="${primeira ? '' : 'atividade-sep'}">
    <h1>${a.titulo}</h1>
    <p>
      ${
        a.marcos.length
          ? html`<b>Marco principal:</b> ${a.marcos.map(nomeMarco).join(' · ')}`
          : html`<b>Atividade complementar:</b> ${a.categoria ?? ''}`
      }
      ${a.revisa?.length ? html` &nbsp;·&nbsp; <b>Revisão:</b> ${a.revisa.map(nomeMarco).join(' · ')}` : ''}
    </p>
    ${a.materialImpresso ? html`<p>📖 <b>Material impresso:</b> ${rotuloDoMaterial(a.materialImpresso)}</p>` : ''}
    ${primeira ? cabecalhoMeta(e) : ''}
    <h2>🎯 Objetivo</h2>
    <p>${textoRico(a.objetivo)}</p>
    <h2>🧭 Passo a passo</h2>
    <ol>
      ${a.passos.map(
        (p) =>
          html`<li>
            <b>${p.titulo}${p.minutos ? ` (${p.minutos} min)` : ''}.</b> ${textoRico(p.texto)}
            ${p.fala ? html`<p class="fala">“${p.fala}”</p>` : ''}
          </li>`,
      )}
    </ol>
    <h2>👀 O que observar (para a ficha de registro)</h2>
    <div class="duas-col">
      <div class="caixa">
        <p><b>✅ Consolidado</b> se…</p>
        <ul>
          ${a.observar.consolidado.map((t) => html`<li>${textoRico(t)}</li>`)}
        </ul>
      </div>
      <div class="caixa">
        <p><b>🌱 Em desenvolvimento</b> se…</p>
        <ul>
          ${a.observar.emDesenvolvimento.map((t) => html`<li>${textoRico(t)}</li>`)}
        </ul>
      </div>
    </div>
    ${
      a.ajustes?.dificil || a.ajustes?.facil
        ? html`<h2>🔁 Ajustes na hora</h2>
            <p>
              ${a.ajustes.dificil ? html`<b>Está difícil?</b> ${textoRico(a.ajustes.dificil)} ` : ''}
              ${a.ajustes.facil ? html`<b>Está fácil?</b> ${textoRico(a.ajustes.facil)}` : ''}
            </p>`
        : ''
    }
  </div>`;
}

/** Toques das vertentes que a família usa, sem repetir a mesma vertente de atividades diferentes. */
function toquesDaVertente(
  e: EntradaPacote,
): { vertente: Vertente; texto: string; principal: boolean }[] {
  const usadas = [e.familia.vertentePrincipal, ...e.familia.inspiracoes];
  const lista: { vertente: Vertente; texto: string; principal: boolean }[] = [];
  for (const v of usadas) {
    const texto = e.atividades.map((a) => a.toqueVertente?.[v]).find((t) => t);
    if (texto) lista.push({ vertente: v, texto, principal: v === e.familia.vertentePrincipal });
  }
  return lista;
}

function paginaMateriais(e: EntradaPacote): HtmlSeguro {
  const materiais = [
    ...new Map(e.atividades.flatMap((a) => a.materiais).map((m) => [m.item, m])).values(),
  ];
  const toques = toquesDaVertente(e);
  return html`<section class="pagina educador">
    <span class="etiqueta">Prepare antes · 5 min</span>
    <h1>Materiais e livro</h1>
    <div class="duas-col">
      <div>
        <h2>🧺 Separe</h2>
        <ul class="check">
          ${materiais.map((m) => html`<li>${m.item}${m.deCasa ? html` <b>(de casa)</b>` : ''}</li>`)}
          <li>Folhas da criança impressas, ou o tablet no modo tablet</li>
          <li>Ficha de registro e uma caneta</li>
        </ul>
      </div>
      <div>
        <h2>📚 Livro sugerido</h2>
        ${
          e.livro
            ? html`<div class="livro">
                <div class="capa">${e.livro.titulo}</div>
                <div>
                  <p><b>${e.livro.titulo}</b><br />${e.livro.autor}</p>
                  <p><b>Uso:</b> ${USO_LIVRO[e.livro.uso]}.</p>
                  <p><b>Por quê:</b> ${textoRico(e.livro.porQue)}</p>
                </div>
              </div>`
            : html`<p class="aviso-capa">Ainda não há livro da curadoria ligado a estes marcos.</p>`
        }
      </div>
    </div>
    ${
      toques.length
        ? html`<h2>🌿 Toque da vertente</h2>
            <div class="duas-col">
              ${toques.map(
                (t) =>
                  html`<div class="caixa">
                    <p>
                      <b>${t.vertente}${t.principal ? '' : ' (inspiração)'}:</b>
                      ${textoRico(t.texto)}
                    </p>
                  </div>`,
              )}
            </div>`
        : ''
    }
    <h2>📸 Depois da sessão</h2>
    <p>
      Preencha a ficha de registro (2 min). Se quiser guardar evidência para o portfólio, fotografe
      <b>a folha preenchida</b>, não o rosto da criança.
    </p>
    ${rodapeEducador('Semear · Pacote de sessão · Materiais', 'Educador')}
  </section>`;
}

function paginaFicha(e: EntradaPacote): HtmlSeguro {
  const linhasMarco: { id: string; revisao: boolean }[] = [];
  for (const a of e.atividades) {
    for (const id of a.marcos) linhasMarco.push({ id, revisao: false });
    for (const id of a.revisa ?? []) linhasMarco.push({ id, revisao: true });
  }
  const unicos = [...new Map(linhasMarco.map((l) => [l.id, l])).values()];
  const evidencias = e.atividades.flatMap((a) => a.evidencias);
  const pergunta =
    e.atividades.map((a) => a.perguntaFicha).find((p) => p) ??
    'Anotações: o que a criança disse, o que surpreendeu, o que repetir';

  return html`<section class="pagina educador">
    <span class="etiqueta">Ficha de registro rápido · 2 min</span>
    <h1>Como foi a sessão?</h1>
    <div class="meta">
      <div><b>Criança</b>${e.crianca.nome}</div>
      <div><b>Data</b>___/___/______</div>
      <div><b>Duração real</b>_____ min</div>
      <div><b>Código</b>${e.sessao.codigo}</div>
    </div>
    ${unicos.length === 0 ? html`<p>Atividade complementar: não há marcos para registrar. Anote abaixo o que a criança fez.</p>` : ''}
    <h2>Marcos trabalhados</h2>
    <table class="registro">
      <tr>
        <th>Marco</th>
        <th>Não observado</th>
        <th>Em desenvolvimento</th>
        <th>Consolidado</th>
      </tr>
      ${unicos.map(
        (l) =>
          html`<tr>
            <td>
              <b>${l.id}</b>${l.revisao ? ' (revisão)' : ''}<br />${e.marco(l.id)?.titulo ?? ''}
            </td>
            <td class="c">☐</td>
            <td class="c">☐</td>
            <td class="c">☐</td>
          </tr>`,
      )}
    </table>
    ${
      evidencias.length
        ? html`<h2>Evidências</h2>
            <table class="registro">
              ${evidencias.map(
                (ev) =>
                  html`<tr>
                    <td>${ev.texto}</td>
                    <td>${ev.resposta}</td>
                  </tr>`,
              )}
              <tr>
                <td>Foto da folha para o portfólio</td>
                <td>☐ tirei &nbsp; ☐ não precisa</td>
              </tr>
            </table>`
        : ''
    }
    <h2>Engajamento</h2>
    <p style="font-size:16pt">
      😴 &nbsp; 🙂 &nbsp; 😄 &nbsp; 🤩 &nbsp;&nbsp;<span style="font-size:10pt">(circule)</span>
    </p>
    <h2>${pergunta}</h2>
    <div class="linhas-nota">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
    ${rodapeEducador(`Sessão ${e.sessao.codigo} · gerada em ${dataBR(e.sessao.criadaEm)}`, 'Educador · ficha')}
  </section>`;
}

// O app pede a impressão por mensagem: a prévia roda num iframe isolado (sandbox), sem acesso ao app.
const SCRIPT = `
window.addEventListener('message',function(e){if(e.source===window.parent&&e.data==='semear:imprimir'){window.print();}});
function alternarTablet(){var on=document.body.classList.toggle('tablet');document.getElementById('btnTablet').setAttribute('aria-pressed',String(on));}
function trocarLetra(v){document.body.classList.remove('letra-bastao','letra-script','letra-cursiva');document.body.classList.add('letra-'+v);}
`;

/** Documento HTML completo e autossuficiente (CSS e script embutidos): pode ser baixado e aberto offline. */
/**
 * Política de segurança do documento: sem conexões, imagens ou formulários externos. Mesmo que algum
 * texto escape da proteção, ele não consegue enviar os dados da família para fora.
 */
const CSP = [
  "default-src 'none'",
  "style-src 'unsafe-inline' https://fonts.googleapis.com",
  'font-src https://fonts.gstatic.com',
  "script-src 'unsafe-inline'",
  "connect-src 'none'",
  "img-src 'none'",
  "form-action 'none'",
  "base-uri 'none'",
].join('; ');

export function gerarPacote(e: EntradaPacote): string {
  // A letra vem dos dados da criança (que podem vir de um backup): só valores conhecidos entram no HTML.
  const letra = ehLetra(e.letra) ? e.letra : 'bastao';
  const titulo = `Semear · ${e.sessao.codigo} · ${e.crianca.nome}`;
  const roteiro = html`<section class="pagina educador">
    <span class="etiqueta">Roteiro do educador · leia antes da sessão</span>
    ${e.atividades.map((a, i) => roteiroDaAtividade(a, e, i === 0))}
    ${rodapeEducador('Semear · Pacote de sessão · Roteiro', 'Educador')}
  </section>`;

  const folhas = e.atividades.flatMap((a) =>
    a.folhas.map((f, i) =>
      paginaDaFolha(f, `${a.marcos.join(' · ') || a.categoria || ''} · Folha ${i + 1}`),
    ),
  );

  const opcoesLetra = (Object.keys(NOME_LETRA) as Letra[])
    .map(
      (l) =>
        `<option value="${l}"${l === letra ? ' selected' : ''}>${escapar(NOME_LETRA[l])}</option>`,
    )
    .join('');

  const corpo = html`${roteiro}${paginaMateriais(e)}${folhas}${paginaFicha(e)}`;

  return `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="${CSP}">
<title>${escapar(titulo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Playwrite+BR:wght@400&display=swap" rel="stylesheet">
<style>${tokens}
${estilos}</style>
</head>
<body class="letra-${letra}">
<div class="barra" role="toolbar" aria-label="Controles do pacote">
  <strong>🌱 Semear</strong>
  <button class="primario" onclick="window.print()">🖨️ Imprimir / salvar PDF</button>
  <button id="btnTablet" aria-pressed="false" onclick="alternarTablet()">📱 Modo tablet (só folhas da criança)</button>
  <label>Letra da criança: <select onchange="trocarLetra(this.value)">${opcoesLetra}</select></label>
</div>
<main class="paginas">${corpo}</main>
<script>${SCRIPT}</script>
</body>
</html>
`;
}

export function nomeArquivoPacote(sessao: Sessao, crianca: Crianca): string {
  const nome = crianca.nome
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // remove acentos antes de limpar o resto
    .replace(/[^A-Za-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .toLowerCase();
  return `semear-${sessao.codigo.toLowerCase()}-${nome || 'crianca'}.html`;
}
