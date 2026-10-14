"""
Biblioteca de páginas da coleção O Grande Tesouro de Marina.
Cada função devolve o HTML de uma página A4 (ou de uma folha recortável).
O estilo está em estilo.css; o conteúdo de cada volume fica em volumeN.py.
"""
import math
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
ARTE = os.path.join(AQUI, "build", "arte")

from motivos import SUBJECTS  # noqa: E402
from motivos2 import MOTIVOS2, contorno  # noqa: E402
from arte_extra import ARTE_EXTRA  # noqa: E402
from motivos3 import MOTIVOS3  # noqa: E402
from motivos4 import MOTIVOS4  # noqa: E402
import fontes_v1  # noqa: E402

TODOS = {**SUBJECTS, **MOTIVOS2, **ARTE_EXTRA, **MOTIVOS3, **MOTIVOS4}
VERSAO = {"atual": "impressao"}   # "impressao" (papel branco) ou "tela" (papel creme)


# ------------------------------------------------------------------ imagens

def arte(nome, para_colorir=False):
    """Motivo procedural (PNG com transparência), pintado uma vez e reaproveitado."""
    os.makedirs(ARTE, exist_ok=True)
    arq = nome + ("_contorno" if para_colorir else "") + ".png"
    p = os.path.join(ARTE, arq)
    if not os.path.exists(p):
        a = contorno(TODOS[nome]) if para_colorir else TODOS[nome]()
        a.rgba().save(p, dpi=(300, 300), optimize=True)
    return "build/arte/" + arq


def img(nome, w, estilo="", colorir=False):
    return f'<img class="aq" src="{arte(nome, colorir)}" style="width:{w};{estilo}" alt="">'


def pd(nome, w, estilo=""):
    """Ilustração de domínio público, na versão de papel certa."""
    suf = "creme" if VERSAO["atual"] == "tela" else "branco"
    return f'<img class="pd" src="dominio_publico/v1/{nome}_{suf}.jpg" style="width:{w};{estilo}" alt="">'


def credito_pd(*nomes):
    return '<div class="credito">Ilustração: ' + " · ".join(fontes_v1.credito(n) for n in nomes) + "</div>"


# ------------------------------------------------------------------ estrutura

class Livro:
    def __init__(self, volume, titulo_volume):
        self.volume = volume
        self.titulo_volume = titulo_volume
        self.paginas = []      # (num, html)
        self.unidade = ""

    @property
    def proximo(self):
        return len(self.paginas) + 1

    def cab(self):
        base = f"Volume {self.volume} · {self.titulo_volume}"
        return base + (f" &nbsp;—&nbsp; {self.unidade}" if self.unidade else "")

    def add(self, conteudo, aba=None, classe="", moldura=True, cabecalho=True, numero=True):
        n = self.proximo
        partes = [f'<section class="pagina {classe}">']
        if moldura:
            partes.append('<div class="moldura"></div>')
        if cabecalho:
            partes.append(f'<div class="cabecalho">{self.cab()}</div>')
        if aba:
            lado = "dir" if n % 2 else "esq"
            partes.append(f'<div class="aba {lado}" style="--aba: var({aba})"></div>')
        partes.append(conteudo)
        if numero:
            partes.append(f'<div class="rodape"><span class="num">{n}</span></div>')
        partes.append("</section>")
        self.paginas.append((n, "\n".join(partes)))
        return n

    def html(self):
        cls = "tela" if VERSAO["atual"] == "tela" else ""
        corpo = "".join(h for _, h in self.paginas)
        return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                f'<title>O Grande Tesouro de Marina — Volume {self.volume}</title>'
                f'<link rel="stylesheet" href="estilo.css"></head><body class="{cls}">{corpo}</body></html>')


def gerar_pdf(html_path, pdf_path):
    env = dict(os.environ, NODE_PATH="/opt/node-tools/node_modules")
    r = subprocess.run(["node", os.path.join(AQUI, "pdf.js"), html_path, pdf_path], env=env,
                       capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[-2000:])
    return r.returncode == 0


# ------------------------------------------------------------------ blocos

def adulto(rotulo, texto, credito="", estilo=""):
    return (f'<div class="adulto" style="{estilo}"><span class="rotulo">Para o adulto · {rotulo}</span><br>'
            f'{texto}{credito}</div>')


def titulo(t, sub=None, tam=None):
    s = f'<h1 class="titulo" style="{f"font-size:{tam}pt" if tam else ""}">{t}</h1>'
    if sub:
        s += f'<div class="subtitulo">{sub}</div>'
    return s


def lista(itens, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"


def marcas_corte(gx, gy, cols, rows, cw, ch):
    s = []
    for i in range(cols + 1):
        x = gx + i * cw
        s.append(f'<line x1="{x}" y1="{gy - 6}" x2="{x}" y2="{gy - 1.5}"/>')
        s.append(f'<line x1="{x}" y1="{gy + rows * ch + 1.5}" x2="{x}" y2="{gy + rows * ch + 6}"/>')
    for j in range(rows + 1):
        y = gy + j * ch
        s.append(f'<line x1="{gx - 6}" y1="{y}" x2="{gx - 1.5}" y2="{y}"/>')
        s.append(f'<line x1="{gx + cols * cw + 1.5}" y1="{y}" x2="{gx + cols * cw + 6}" y2="{y}"/>')
    return ('<svg class="svgpag" viewBox="0 0 210 297" stroke="#6f6a62" stroke-width="0.25">'
            + "".join(s) + "</svg>")


def cabeca_folha(t, sub, top=12):
    return (f'<div style="position:absolute;top:{top}mm;left:0;right:0;text-align:center">'
            f'<div class="tit-folha">{t}</div><div class="peq">{sub}</div></div>')


def rodape_folha(txt):
    return f'<div class="rodape-folha peq">{txt}</div>'


# ------------------------------------------------------------------ tipos de página

def guia(L, u):
    """Guia do adulto de uma unidade. u: dict com as chaves usadas abaixo."""
    etapas = "".join(
        f'<div class="etapa"><h4>{nome}</h4><div class="verbo">{verbo}</div>{lista(u["etapas"][i])}</div>'
        for i, (nome, verbo) in enumerate((("Descobrir", "observar · escutar · nomear"),
                                            ("Relacionar", "comparar · parear · ordenar"),
                                            ("Criar", "narrar · imaginar · expressar"))))
    alerta = f'<div class="alerta">{u["alerta"]}</div>' if u.get("alerta") else ""
    c = f"""
    <div class="miolo guia">
      <div class="centro peq versal" style="letter-spacing:.2em">Guia do adulto</div>
      {titulo(u["titulo"], u["pergunta"], 24)}
      <div class="ficha">
        <div>
          <h3>Duração e ritmo</h3><p>{u["duracao"]}</p>
          <h3>Objetivos</h3>{lista(u["objetivos"])}
        </div>
        <div>
          <h3>Repertório</h3><p>{u["repertorio"]}</p>
          <h3>Materiais</h3><p>{u["materiais"]}</p>
          <h3>Vida prática</h3><p>{u["vida"]}</p>
        </div>
      </div>
      <div class="etapas">{etapas}</div>
      <h3>Indicadores observáveis <span class="peq it" style="font-weight:400">— sinais para observar, não metas nem prova</span></h3>
      {lista(u["indicadores"], "duas")}
      <p style="margin-top:1.5mm"><b>Se o interesse crescer:</b> {u["interesse"]} <b>Se o dia estiver difícil:</b> {u["dificil"]}</p>
      {alerta}
    </div>"""
    return L.add(c, aba=u.get("aba", "--d-natureza"), classe="guia")


def historia(L, t, sub, corpo, adulto_html="", aba="--d-historias", tam=None):
    c = f'<div class="miolo historia">{titulo(t, sub, tam) if t else ""}{corpo}</div>{adulto_html}'
    return L.add(c, aba=aba)


def poema(L, t, autor, estrofes, imagem_html, adulto_html="", aba="--d-historias", original=None):
    est = "".join(f'<p class="estrofe">{e}</p>' for e in estrofes)
    orig = f'<div class="original">{original}</div>' if original else ""
    c = f"""<div class="miolo poema">{titulo(t, autor, 30)}
      <div class="centro" style="margin:4mm 0">{imagem_html}</div>{est}{orig}</div>{adulto_html}"""
    return L.add(c, aba=aba)


def observacao(L, t, sub, imagem_html, perguntas, adulto_html="", aba="--d-natureza"):
    pq = "".join(f'<li>{p}</li>' for p in perguntas)
    c = f"""<div class="miolo">{titulo(t, sub, 28)}
      <div class="centro" style="margin:4mm 0 3mm">{imagem_html}</div>
      <ol class="perguntas">{pq}</ol></div>{adulto_html}"""
    return L.add(c, aba=aba)


CW, CH, GX, GY = 60, 78, 15, 34


def cartoes(L, t, itens, rodape, sub_frente=None):
    """Folha de 9 cartões (frente) e verso espelhado. itens: dicts pt, mot|pd, en, fr, la, sci, dica."""
    def img_de(it):
        if it.get("html"):
            return it["html"]
        return pd(it["pd"], "50mm", "max-height:52mm;object-fit:contain") if it.get("pd") else img(it["mot"], "44mm")
    frente = "".join(f'<div class="carta"><div class="borda"></div>{img_de(it)}<div class="palavra">{it["pt"]}</div></div>'
                     for it in itens)
    sub = sub_frente or "frente · imprimir frente e verso (virar pela borda longa) em papel de 180 g ou mais · cortar nas linhas tracejadas"
    c1 = f"""{cabeca_folha("Cartões · " + t, sub)}
    <div class="grade" style="left:{GX}mm;top:{GY}mm;grid-template-columns:repeat(3,{CW}mm);grid-template-rows:repeat(3,{CH}mm)">{frente}</div>
    {marcas_corte(GX, GY, 3, 3, CW, CH)}"""
    n1 = L.add(c1 + rodape_folha(f"{L.proximo} · {rodape}"), moldura=False, cabecalho=False, numero=False)
    ordem = []
    for r in range(3):
        ordem += [itens[r * 3 + 2], itens[r * 3 + 1], itens[r * 3]]
    verso = []
    for it in ordem:
        la = it.get("la") or "<span class='peq'>sem palavra clássica</span>"
        linhas = [("inglês", it["en"]), ("francês", it["fr"]), ("latim", la)]
        if it.get("sci"):
            linhas.append(("ciência", f'<span class="it">{it["sci"]}</span>'))
        if it.get("som"):
            linhas = [("som", it["som"])] + linhas
        ls = "".join(f'<div class="linha-idioma"><span>{a}</span><span>{b}</span></div>' for a, b in linhas)
        verso.append(f'<div class="carta verso"><div class="borda"></div><div class="pt">{it["pt"]}</div>{ls}'
                     f'<div class="dica">{it["dica"]}</div></div>')
    c2 = f"""{cabeca_folha("Cartões · " + t, "verso · para o adulto · colunas espelhadas para coincidir com a frente")}
    <div class="grade" style="left:{GX}mm;top:{GY}mm;grid-template-columns:repeat(3,{CW}mm);grid-template-rows:repeat(3,{CH}mm)">{''.join(verso)}</div>
    {marcas_corte(GX, GY, 3, 3, CW, CH)}"""
    L.add(c2 + rodape_folha(f"{L.proximo} · Latim: vogal com traço (ā, ē, ī, ō, ū) é longa · “sem palavra clássica”: os romanos não conheciam"),
          moldura=False, cabecalho=False, numero=False)
    return n1


def memoria(L, t, itens, ordem, adulto_html, verso_motivo="raminho"):
    """12 cartas (6 pares) + verso. itens: lista de (rótulo, html_img)."""
    MW = MH = 52
    MX, MY = 27, 33
    cartas = "".join(f'<div class="carta"><div class="borda"></div>{itens[i][1]}'
                     f'<div class="peq" style="margin-top:.5mm">{itens[i][0]}</div></div>' for i in ordem)
    c = f"""{cabeca_folha("Jogo da memória · " + t, "6 pares · imprimir em papel de 180 g ou colar sobre papelão · verso na página seguinte", 11)}
    <div class="grade" style="left:{MX}mm;top:{MY}mm;grid-template-columns:repeat(3,{MW}mm);grid-template-rows:repeat(4,{MH}mm)">{cartas}</div>
    {marcas_corte(MX, MY, 3, 4, MW, MH)}{adulto_html}"""
    n = L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)
    versos = "".join(f'<div class="carta"><div class="borda"></div>{img(verso_motivo, "41mm", "transform:rotate(-20deg)")}</div>'
                     for _ in range(12))
    c2 = f"""{cabeca_folha("Jogo da memória · verso", f"imprimir no verso da página {n} (virar pela borda longa) · desenho igual em todas as cartas", 11)}
    <div class="grade" style="left:{MX}mm;top:{MY}mm;grid-template-columns:repeat(3,{MW}mm);grid-template-rows:repeat(4,{MH}mm)">{versos}</div>
    {marcas_corte(MX, MY, 3, 4, MW, MH)}"""
    L.add(c2 + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)
    return n


def sequencia(L, t, sub, quadros, adulto_html, aba="--d-memoria"):
    """4 cartões grandes para ordenar (2 × 2), recortáveis, com o número da ordem só no verso do adulto."""
    QW, QH, QX, QY = 86, 86, 19, 44
    cel = "".join(f'<div class="carta"><div class="borda"></div>{q[1]}<div class="legenda-q">{q[0]}</div></div>'
                  for q in quadros)
    c = f"""{cabeca_folha(t, sub, 13)}
    <div class="grade" style="left:{QX}mm;top:{QY}mm;grid-template-columns:repeat(2,{QW}mm);grid-template-rows:repeat(2,{QH}mm)">{cel}</div>
    {marcas_corte(QX, QY, 2, 2, QW, QH)}{adulto_html}"""
    return L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)


def tracado(L, t, sub, svg, imagens_html, adulto_html, aba="--d-memoria"):
    c = f"""<div class="miolo">{titulo(t, sub)}</div>{imagens_html}
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>{adulto_html}"""
    return L.add(c, aba=aba)


def ponto_inicio(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="3.3" fill="none" stroke="var(--oliva)" stroke-width="0.9"/>'
            f'<circle cx="{x}" cy="{y}" r="1.2" fill="var(--oliva)"/>')


def pontilhado(d, cor="var(--tracejado)", w=2.6):
    return (f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-dasharray="0.1 6"/>')


def passos(L, t, sub, itens, adulto_html, aba="--d-vida"):
    """Sequência ilustrada de vida prática: itens = [(imagem_html, texto)]."""
    cel = "".join(f'<div class="passo"><div class="n">{i + 1}</div>{im}<div class="txt">{tx}</div></div>'
                  for i, (im, tx) in enumerate(itens))
    c = f"""<div class="miolo">{titulo(t, sub)}<div class="passos">{cel}</div></div>{adulto_html}"""
    return L.add(c, aba=aba)


def texto(L, conteudo, aba=None, classe=""):
    return L.add(f'<div class="miolo texto">{conteudo}</div>', aba=aba, classe=classe)
