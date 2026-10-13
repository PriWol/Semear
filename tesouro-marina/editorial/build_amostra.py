"""
Gera a AMOSTRA EDITORIAL do Volume 1 (páginas reais, A4) em duas versões:
  amostra/amostra-v1-impressao.pdf  — fundo branco (imprimir em papel creme/marfim)
  amostra/amostra-v1-tela.pdf       — fundo creme, para leitura na tela
e renderiza PNGs de inspeção em amostra/inspecao/.

uso: python3 build_amostra.py
"""
import os
import subprocess
import sys
import math

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ARTE = os.path.join(AQUI, "build", "arte")
SAIDA = os.path.join(RAIZ, "amostra")
sys.path.insert(0, AQUI)

from motivos import SUBJECTS  # noqa: E402
from arte_extra import ARTE_EXTRA  # noqa: E402

TODOS = {**SUBJECTS, **ARTE_EXTRA}


def arte(nome):
    """Pinta (ou reaproveita) o motivo e devolve o caminho relativo ao HTML."""
    os.makedirs(ARTE, exist_ok=True)
    p = os.path.join(ARTE, nome + ".png")
    if not os.path.exists(p):
        TODOS[nome]().rgba().save(p, dpi=(300, 300), optimize=True)
    return "build/arte/" + nome + ".png"


def img(nome, w, extra=""):
    return f'<img class="aq" src="{arte(nome)}" style="width:{w};{extra}" alt="">'


def pagina(conteudo, num=None, cab=None, aba=None, classe="", moldura=True):
    """moldura=False nas folhas de recorte: a moldura cruzaria as marcas de corte."""
    partes = [f'<section class="pagina {classe}">'] + (['<div class="moldura"></div>'] if moldura else [])
    if cab:
        partes.append(f'<div class="cabecalho">{cab}</div>')
    if aba:
        partes.append(f'<div class="aba" style="--aba: var({aba})"></div>')
    partes.append(conteudo)
    if num:
        partes.append(f'<div class="rodape"><span class="num">{num}</span></div>')
    partes.append("</section>")
    return "\n".join(partes)


CAB = "Volume 1 · O mundo ao meu redor &nbsp;—&nbsp; Unidade 3 · O jardim e o pomar"

# ------------------------------------------------------------------ capa

def capa():
    cx, cy, rx, ry = 105, 168, 74, 82  # mm, centro da guirlanda
    itens = ["maca", "folha", "margarida", "pera", "raminho", "morango", "tulipa", "uva", "folha",
             "laranja", "florzinha_azul", "cereja", "girassol", "bolota", "raminho", "jabuticaba",
             "florzinha_rosa", "banana"]
    html = []
    for i, nome in enumerate(itens):
        t = -math.pi / 2 + 2 * math.pi * i / len(itens)
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        w = 33 if nome not in ("raminho", "jabuticaba") else 46
        rot = math.degrees(t) + 90 if nome in ("raminho", "folha") else (i % 3 - 1) * 9
        html.append(f'<img class="aq" src="{arte(nome)}" style="position:absolute;width:{w}mm;'
                    f'left:{x - w / 2:.1f}mm;top:{y - w / 2:.1f}mm;transform:rotate({rot:.0f}deg)">')
    texto = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-family:'Cormorant Garamond';font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:64pt;line-height:.95;color:var(--tinta);letter-spacing:.02em">Marina</div>
      <div style="font-size:11.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div>
    </div>
    <div style="position:absolute;top:{cy - 30}mm;left:{cx - 42}mm;width:84mm;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 1</div>
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:27pt;line-height:1.05;margin:2mm 0">O mundo<br>ao meu redor</div>
      <div class="vinheta-sep">❦</div>
      <div style="font-size:10.5pt;font-style:italic;color:var(--sepia);line-height:1.4">sentidos · casa · jardim e pomar<br>animais · céu · água · estações</div>
    </div>
    {img('ratinho', '26mm', f'position:absolute;left:{cx - 13}mm;top:{cy + 34}mm')}
    <div style="position:absolute;bottom:22mm;left:0;right:0;text-align:center;font-size:10pt;color:var(--sepia);font-style:italic">
      “Grandes coisas começam com pequenos olhares atentos.”</div>
    <div style="position:absolute;bottom:15mm;left:0;right:0;text-align:center" class="peq">AMOSTRA EDITORIAL · páginas selecionadas para aprovação</div>
    """
    return pagina("".join(html) + texto, classe="capa")

# ------------------------------------------------------------------ guia

def guia():
    c = f"""
    <div class="miolo guia">
      <div class="centro peq versal" style="letter-spacing:.2em">Guia do adulto</div>
      <h1 class="titulo">Unidade 3 · O jardim e o pomar</h1>
      <div class="subtitulo">De onde vêm os frutos? Olhar, cheirar, nomear, separar, contar até três e contar histórias.</div>

      <div class="ficha">
        <div>
          <h3>Duração e ritmo</h3>
          <p>Três fins de semana · dois encontros por fim de semana · de 15 a 25 minutos cada, em blocos curtos.
          Pare enquanto o interesse ainda está alto: o desejo de voltar ensina mais que a insistência.</p>
          <h3>Objetivos</h3>
          <ul>
            <li>Nomear e reconhecer de 6 a 9 frutas e 4 flores do cotidiano.</li>
            <li>Comparar por cor, tamanho e cheiro; separar em dois grupos.</li>
            <li>Acompanhar uma história cumulativa e antecipar a frase repetida.</li>
            <li>Correspondência um a um e quantidades até 3, com objetos reais.</li>
            <li>Primeiro traço controlado: linha vertical, de cima para baixo.</li>
            <li>Escutar música descritiva e reconhecer um tema que volta.</li>
          </ul>
        </div>
        <div>
          <h3>Repertório</h3>
          <p><b>História:</b> <i>A cesta do pomar</i> (texto original da coleção, p. 30–31).<br>
          <b>Cantiga:</b> <i>Alecrim dourado</i> (tradicional, domínio público).<br>
          <b>Música:</b> Vivaldi, <i>A Primavera</i>, 1º movimento (p. 39).<br>
          <b>Arte:</b> Albrecht Dürer, <i>O grande tufo de relva</i> (1503) — olhar de perto as folhinhas.<br>
          <b>Línguas</b> (no máximo três palavras por semana): <i>apple · la pomme · mālum</i>.</p>
          <h3>Materiais</h3>
          <p>Cesta pequena; 3 ou 4 frutas de verdade; pano de prato; faca sem ponta;
          giz de cera grosso; papel cartão (180 g ou mais) para cartas; gravação de <i>As Quatro Estações</i>.</p>
          <h3>Vida prática</h3>
          <p>Lavar a fruta na bacia, enxugar, descascar a banana (o adulto inicia, ela termina), pôr a fruta na cesta e levar à mesa com as duas mãos.</p>
        </div>
      </div>

      <div class="etapas">
        <div class="etapa"><h4>Descobrir</h4><div class="verbo">observar · escutar · nomear</div>
          <ul><li>Cesta real: tocar, cheirar, nomear (dia 1).</li><li>História, primeira escuta (p. 30–31).</li>
          <li>Flashcards: 3 por vez, mostrar e dizer (p. 35).</li><li>Ouvir <i>A Primavera</i> no colo.</li></ul></div>
        <div class="etapa"><h4>Relacionar</h4><div class="verbo">comparar · parear · ordenar</div>
          <ul><li>“Qual é a vermelha?” — duas frutas reais.</li><li>Pôr as frutas na ordem da história.</li>
          <li>Memória com cartas viradas para cima (p. 37).</li><li>Um morango para cada prato (1 a 1).</li></ul></div>
        <div class="etapa"><h4>Criar</h4><div class="verbo">narrar · imaginar · expressar</div>
          <ul><li>Recontar com a cesta e as cartas.</li><li>“O que mais caberia na cesta?”</li>
          <li>Chuva no jardim: traço e som (p. 33).</li><li>Dançar o tema, os pássaros e o trovão.</li></ul></div>
      </div>

      <h3>Indicadores observáveis <span class="peq it" style="font-weight:400">— sinais para observar, não metas nem prova</span></h3>
      <ul style="columns:2;column-gap:7mm">
        <li>Aponta ou nomeia frutas espontaneamente fora da hora da atividade.</li>
        <li>Completa a frase “— Uma maçã para a…” antes do adulto.</li>
        <li>Junta duas cartas iguais com as cartas à vista.</li>
        <li>Separa frutas em dois grupos por um critério que ela mesma escolhe.</li>
        <li>Faz o traço de cima para baixo com o dedo, depois com o giz.</li>
        <li>Reage com o movimento combinado quando o tema de Vivaldi volta.</li>
      </ul>
      <p style="margin-top:1.5mm"><b>Se o interesse crescer:</b> visite uma feira e procure as frutas das cartas; abra uma maçã ao meio (a estrela de sementes).
      <b>Se o dia estiver difícil:</b> só a história e a cesta; o resto espera.</p>

      <div class="alerta"><b>Segurança à mesa.</b> Uvas, cerejas e jabuticabas inteiras são risco de engasgo antes dos 4 anos: corte as uvas ao comprido,
      retire caroços e sementes, e ofereça sempre com a criança sentada.</div>
    </div>"""
    return pagina(c, num="29", cab=CAB, aba="--d-natureza", classe="guia")

# ------------------------------------------------------------------ história

def historia1():
    frutas = "".join(img(n, "33mm", "display:inline-block;margin:0 1.5mm") for n in ("maca", "pera", "banana", "laranja"))
    c = f"""
    <div class="miolo historia">
      <h1 class="titulo" style="font-size:34pt">A cesta do pomar</h1>
      <div class="subtitulo">uma história para contar e recontar</div>
      <div class="centro" style="margin:4mm 0 3mm">{frutas}</div>
      <p class="capitular" style="margin-top:6mm">Era uma manhã de sol. Marina pegou a cesta de vime e foi ao pomar.</p>
      <p>Debaixo da macieira, encontrou uma maçã vermelha.</p>
      <p class="fala">— Uma maçã para a cesta!</p>
      <p>Perto do muro, a pereira deixou cair uma pera.</p>
      <p class="fala">— Uma pera para a cesta! Uma pera e uma maçã.</p>
      <p>Na bananeira, um cacho de bananas amarelas esperava.</p>
      <p class="fala">— Uma banana para a cesta! Uma banana, uma pera e uma maçã.</p>
      <p>E lá no fundo, a laranjeira estava cheia de laranjas redondas.</p>
      <p class="fala">— Uma laranja para a cesta! Uma laranja, uma banana, uma pera e uma maçã.</p>
    </div>"""
    return pagina(c, num="30", cab=CAB, aba="--d-historias")


def historia2():
    c = f"""
    <div class="miolo historia">
      {img('cesta', '48mm', 'float:right;margin:0 0 2mm 4mm')}
      <p style="margin-top:6mm">A cesta ficou pesada. Marina sentou-se debaixo da jabuticabeira para descansar.</p>
      <p>Então, de mansinho, saiu da grama um ratinho de bigodes finos. Ele olhou para a cesta… e olhou para Marina.</p>
      <p class="fala">— Você está com fome, ratinho?</p>
      <p>O ratinho mexeu os bigodes.</p>
      {img('jabuticaba', '62mm', 'margin:1mm auto 2mm')}
      <p>Marina esticou a mão até o tronco da jabuticabeira e colheu uma jabuticaba bem pretinha.</p>
      <p class="fala">— Esta é para você.</p>
      <p>Marina voltou para casa com a cesta cheia.<br>E o ratinho voltou para a toca… com a barriga cheia.</p>
      {img('ratinho', '30mm', 'position:absolute;right:4mm;bottom:52mm')}
    </div>
    <div class="adulto"><span class="rotulo">Para o adulto · contar e narrar</span><br>
      <b>Antes:</b> mostre uma cesta com frutas de verdade e deixe que ela segure e cheire cada uma.
      <b>Durante:</b> pare antes da frase repetida e espere: “— Uma maçã para a…”. Mexa o nariz quando o ratinho mexer os bigodes.
      <b>Depois</b> (narração): “O que Marina achou primeiro?” · tire as frutas da cesta e peça que ela as devolva na ordem da história ·
      “O ratinho estava com fome. O que ele ganhou?” · “Se você encontrasse o ratinho, o que daria a ele?”.
      Não corrija: repita a fala dela, ampliando-a (“Maçã! Uma maçã vermelha e redonda”).
    </div>"""
    return pagina(c, num="31", cab=CAB, aba="--d-historias")

# ------------------------------------------------------------------ traçado

def tracado():
    # cinco linhas verticais pontilhadas, de cada gota até uma flor
    xs = [38, 72, 105, 138, 172]  # mm
    y0, y1 = 88, 208
    svg = [f'<svg style="position:absolute;left:0;top:0" width="210mm" height="297mm" viewBox="0 0 210 297">']
    for x in xs:
        svg.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="var(--tracejado)" stroke-width="2.6" '
                   f'stroke-linecap="round" stroke-dasharray="0.1 6"/>')
        svg.append(f'<circle cx="{x}" cy="{y0 - 1}" r="3.3" fill="none" stroke="var(--oliva)" stroke-width="0.9"/>')
        svg.append(f'<circle cx="{x}" cy="{y0 - 1}" r="1.2" fill="var(--oliva)"/>')
        svg.append(f'<path d="M {x} {y0 + 10} l -2.4 -3.4 M {x} {y0 + 10} l 2.4 -3.4" stroke="var(--oliva)" '
                   f'stroke-width="0.8" fill="none" stroke-linecap="round"/>')
    svg.append("</svg>")
    flores = ["florzinha_rosa", "florzinha_azul", "florzinha_amarela", "florzinha_rosa", "florzinha_azul"]
    fl = "".join(f'<img class="aq" src="{arte(n)}" style="position:absolute;width:22mm;left:{x - 11}mm;top:{y1 + 2}mm">'
                 for x, n in zip(xs, flores))
    nuv = (f'<img class="aq" src="{arte("nuvem")}" style="position:absolute;width:92mm;left:12mm;top:42mm">'
           f'<img class="aq" src="{arte("nuvem")}" style="position:absolute;width:92mm;left:104mm;top:40mm;transform:scaleX(-1)">')
    c = f"""
    <div class="miolo"><h1 class="titulo">A chuva no jardim</h1>
      <div class="subtitulo">Plim, plim, plim, a chuva cai — do céu pra flor a gota vai.</div></div>
    {nuv}{''.join(svg)}{fl}
    <div class="adulto"><span class="rotulo">Para o adulto · traçado vertical</span><br>
      <b>Primeiro com o corpo:</b> de pé, braços no alto, “a chuva cai” até tocar o chão. <b>Depois com o dedo</b> sobre cada linha,
      começando no círculo verde e dizendo “plim” a cada pontinho. <b>Só então</b> o giz de cera grosso, seguro como ela conseguir.
      Por volta dos 2 anos a linha vertical é o primeiro traço controlado: não espere precisão nem exija “ficar na linha”.
      Observe se o movimento vai de cima para baixo e se ela para na flor. Uma ou duas linhas já bastam num dia.
    </div>"""
    return pagina(c, num="33", cab=CAB, aba="--d-memoria")

# ------------------------------------------------------------------ flashcards

FRUTAS = [
    # pt, motivo, inglês, francês, latim clássico, nome científico, dica
    ("maçã", "maca", "apple", "la pomme", "mālum", "Malus domestica",
     "Corte ao meio, atravessado: aparece uma estrela de sementes."),
    ("pera", "pera", "pear", "la poire", "pirum", "Pyrus communis",
     "Ponha ao lado da maçã: qual é mais comprida?"),
    ("banana", "banana", "banana", "la banane", None, "Musa sp.",
     "O adulto começa a descascar; ela termina."),
    ("laranja", "laranja", "orange", "l’orange (fem.)", None, "Citrus × sinensis",
     "Role na mesa. A pera também rola?"),
    ("morango", "morango", "strawberry", "la fraise", "frāgum", "Fragaria × ananassa",
     "As sementinhas ficam do lado de fora. Toque e sinta."),
    ("uva", "uva", "grapes", "le raisin", "ūva", "Vitis vinifera",
     "Corte cada uva ao comprido antes de oferecer."),
    ("jabuticaba", "jabuticaba", "jabuticaba", "jaboticaba", None, "Plinia cauliflora",
     "Nasce grudada no tronco! Procure uma jabuticabeira."),
    ("cereja", "cereja", "cherry", "la cerise", "cerasum", "Prunus avium",
     "Duas cerejas, um cabinho: um par."),
    ("melancia", "melancia", "watermelon", "la pastèque", None, "Citrullus lanatus",
     "É quase toda água: aperte um pedaço e veja o suco."),
]

CW, CH = 60, 78  # mm por carta (3 × 3 = 180 × 234 mm)
GX, GY = 15, 34  # origem da grade


def marcas_corte(gx, gy, cols, rows, cw, ch):
    """Marcas de corte fora da grade, alinhadas a cada linha de corte."""
    s = []
    for i in range(cols + 1):
        x = gx + i * cw
        s.append(f'<line x1="{x}" y1="{gy - 6}" x2="{x}" y2="{gy - 1.5}"/>')
        s.append(f'<line x1="{x}" y1="{gy + rows * ch + 1.5}" x2="{x}" y2="{gy + rows * ch + 6}"/>')
    for j in range(rows + 1):
        y = gy + j * ch
        s.append(f'<line x1="{gx - 6}" y1="{y}" x2="{gx - 1.5}" y2="{y}"/>')
        s.append(f'<line x1="{gx + cols * cw + 1.5}" y1="{y}" x2="{gx + cols * cw + 6}" y2="{y}"/>')
    return ('<svg style="position:absolute;left:0;top:0" width="210mm" height="297mm" viewBox="0 0 210 297" '
            'stroke="#6f6a62" stroke-width="0.25">' + "".join(s) + "</svg>")


def flash_frente():
    cartas = []
    for pt, mot, *_ in FRUTAS:
        cartas.append(f'<div class="carta"><div class="borda"></div>{img(mot, "44mm")}'
                      f'<div class="palavra">{pt}</div></div>')
    c = f"""
    <div style="position:absolute;top:13mm;left:0;right:0;text-align:center">
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:19pt">Cartões · Frutas do pomar</div>
      <div class="peq">frente · imprimir frente e verso (virar pela borda longa) em papel de 180 g ou mais · cortar nas linhas tracejadas</div></div>
    <div class="grade" style="left:{GX}mm;top:{GY}mm;grid-template-columns:repeat(3,{CW}mm);grid-template-rows:repeat(3,{CH}mm)">
      {''.join(cartas)}</div>
    {marcas_corte(GX, GY, 3, 3, CW, CH)}
    <div style="position:absolute;bottom:13mm;left:0;right:0;text-align:center" class="peq">35 · Unidade 3 · O jardim e o pomar</div>"""
    return pagina(c, moldura=False)


def flash_verso():
    cartas = []
    # espelha as colunas para coincidir com a frente na impressão frente e verso (borda longa)
    ordem = []
    for r in range(3):
        ordem += [FRUTAS[r * 3 + 2], FRUTAS[r * 3 + 1], FRUTAS[r * 3]]
    for pt, mot, en, fr, la, sci, dica in ordem:
        la_txt = la if la else "<span class='peq'>sem palavra clássica</span>"
        cartas.append(f"""<div class="carta verso"><div class="borda"></div>
          <div class="pt">{pt}</div>
          <div class="linha-idioma"><span>inglês</span><span>{en}</span></div>
          <div class="linha-idioma"><span>francês</span><span>{fr}</span></div>
          <div class="linha-idioma"><span>latim</span><span>{la_txt}</span></div>
          <div class="linha-idioma"><span>ciência</span><span class="it">{sci}</span></div>
          <div class="dica">{dica}</div></div>""")
    c = f"""
    <div style="position:absolute;top:13mm;left:0;right:0;text-align:center">
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:19pt">Cartões · Frutas do pomar</div>
      <div class="peq">verso · para o adulto · colunas espelhadas para coincidir com a frente</div></div>
    <div class="grade" style="left:{GX}mm;top:{GY}mm;grid-template-columns:repeat(3,{CW}mm);grid-template-rows:repeat(3,{CH}mm)">
      {''.join(cartas)}</div>
    {marcas_corte(GX, GY, 3, 3, CW, CH)}
    <div style="position:absolute;bottom:13mm;left:0;right:0;text-align:center" class="peq">36 · Latim: ā, ū = vogais longas · “sem palavra clássica”: fruta desconhecida dos romanos</div>"""
    return pagina(c, moldura=False)

# ------------------------------------------------------------------ jogo da memória

MEMO = [("tulipa", "tulipa"), ("margarida", "margarida"), ("girassol", "girassol"),
        ("folha", "folha"), ("cogumelo", "cogumelo"), ("bolota", "bolota")]
MW, MH = 52, 52
MX, MY = 27, 33


def memoria():
    ordem = [0, 3, 1, 4, 2, 5, 3, 0, 5, 1, 4, 2]
    cartas = "".join(f'<div class="carta"><div class="borda"></div>{img(MEMO[i][1], "35mm")}'
                     f'<div class="peq" style="margin-top:.5mm">{MEMO[i][0]}</div></div>' for i in ordem)
    c = f"""
    <div style="position:absolute;top:11mm;left:0;right:0;text-align:center">
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:19pt">Jogo da memória · Achados do jardim</div>
      <div class="peq">6 pares · imprimir em papel de 180 g ou colar sobre papelão · o verso está na página seguinte</div></div>
    <div class="grade" style="left:{MX}mm;top:{MY}mm;grid-template-columns:repeat(3,{MW}mm);grid-template-rows:repeat(4,{MH}mm)">
      {cartas}</div>
    {marcas_corte(MX, MY, 3, 4, MW, MH)}
    <div class="adulto" style="bottom:19mm;top:auto"><span class="rotulo">Para o adulto · três níveis do mesmo jogo</span><br>
      <b>Descobrir:</b> 3 pares, cartas viradas para cima; ela acha a carta igual e diz o nome.
      <b>Relacionar:</b> 2 ou 3 pares virados para baixo; vire uma de cada vez e espere que ela lembre onde estava a outra.
      <b>Criar:</b> “Qual sumiu?” — mostre 4 cartas, esconda uma, e peça que ela descubra qual falta.
      Comece sempre um nível abaixo do que ela consegue: o jogo precisa terminar em sucesso.
    </div>
    <div style="position:absolute;bottom:13mm;left:0;right:0;text-align:center" class="peq">37</div>"""
    return pagina(c, moldura=False)


def memoria_verso():
    cartas = "".join(f'<div class="carta"><div class="borda" style="background:none"></div>'
                     f'{img("raminho", "41mm", "transform:rotate(-20deg)")}</div>' for _ in range(12))
    c = f"""
    <div style="position:absolute;top:11mm;left:0;right:0;text-align:center">
      <div style="font-family:'Cormorant Garamond';font-weight:600;font-size:19pt">Jogo da memória · verso</div>
      <div class="peq">imprimir no verso da página 37 (virar pela borda longa) · desenho simétrico: não precisa espelhar</div></div>
    <div class="grade" style="left:{MX}mm;top:{MY}mm;grid-template-columns:repeat(3,{MW}mm);grid-template-rows:repeat(4,{MH}mm)">
      {cartas}</div>
    {marcas_corte(MX, MY, 3, 4, MW, MH)}
    <div style="position:absolute;bottom:13mm;left:0;right:0;text-align:center" class="peq">38</div>"""
    return pagina(c, moldura=False)

# ------------------------------------------------------------------ música

def musica():
    estacoes = [("m_tema", "Tema", "marchar e bater palmas leves"),
                ("m_passaros", "Pássaros", "dedinhos voando · “piu, piu”"),
                ("m_tema", "Tema", "palmas"),
                ("m_riacho", "Riacho", "braços em onda, devagar"),
                ("m_tema", "Tema", "palmas"),
                ("m_trovao", "Trovoada", "tambor nas pernas, forte!"),
                ("m_tema", "Tema", "palmas"),
                ("m_passaros", "Os pássaros voltam", "dedinhos voando de novo"),
                ("m_tema", "Tema", "palmas e… fim!")]
    # caminho em S: 3 linhas de 3 estações
    cel = []
    for i, (m, nome, mov) in enumerate(estacoes):
        r, k = divmod(i, 3)
        col = k if r % 2 == 0 else 2 - k
        x, y = 22 + col * 58, 78 + r * 50
        cel.append(f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:50mm;text-align:center">'
                   f'{img(m, "40mm", "margin:0 auto")}'
                   f'<div style="font-family:Cormorant Garamond;font-weight:700;font-size:12.5pt;margin-top:-1mm">'
                   f'<span style="color:var(--rosa)">{i + 1}</span> · {nome}</div>'
                   f'<div class="peq it" style="font-size:8.6pt;color:var(--sepia)">{mov}</div></div>')
    # trilha tracejada ligando as estações
    pts = []
    for i in range(9):
        r, k = divmod(i, 3)
        col = k if r % 2 == 0 else 2 - k
        pts.append((47 + col * 58, 91 + r * 50))
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    trilha = (f'<svg style="position:absolute;left:0;top:0" width="210mm" height="297mm" viewBox="0 0 210 297">'
              f'<path d="{d}" fill="none" stroke="var(--linha)" stroke-width="0.7" stroke-dasharray="1.6 2.2"/></svg>')
    c = f"""
    <div class="miolo"><h1 class="titulo">Ouvir com o corpo</h1>
      <div class="subtitulo">Antonio Vivaldi · <i>A Primavera</i> · Concerto em mi maior, RV 269 · 1º movimento, Allegro</div>
      <p class="centro" style="font-size:10pt;margin-top:2.5mm;color:var(--sepia)"><i>Giunt’è la Primavera e festosetti / la salutan gl’augei con lieto canto…</i><br>
      “Chegou a Primavera, e os passarinhos a saúdam, em festa, com alegre canto…” — do soneto que acompanha a partitura.</p>
    </div>
    {trilha}{''.join(cel)}
    <div class="adulto"><span class="rotulo">Para o adulto · escuta ativa (musicograma)</span><br>
      O movimento é um <b>ritornelo</b>: um tema alegre que sempre volta, com episódios entre uma volta e outra — os pássaros, o riacho,
      a trovoada. <b>1ª escuta:</b> no colo, só ouvindo; aponte cada desenho quando a música chegar nele. <b>2ª escuta:</b> faça os
      movimentos juntos. <b>Depois:</b> “Quando veio o trovão, a música ficou forte ou fraquinha?”. Os números marcam a ordem; os desenhos são
      sinais de som, não figuras para colorir. Vivaldi (1678–1741) era padre em Veneza, apelidado de “o Padre Ruivo”, e ensinava música às
      meninas do Ospedale della Pietà. O 1º movimento dura cerca de três minutos e meio, conforme a gravação.
    </div>"""
    return pagina(c, num="39", cab=CAB, aba="--d-musica")

# ------------------------------------------------------------------ página-modelo de cena

def modelo_cena():
    c = f"""
    <div style="position:absolute;left:18mm;right:18mm;top:20mm;height:150mm;border:0.8pt dashed var(--sepia-claro);
                display:flex;flex-direction:column;justify-content:center;align-items:center;padding:10mm;text-align:center;background:repeating-linear-gradient(135deg,transparent 0 6mm,rgba(191,174,143,.12) 6mm 12mm)" data-check>
      <div style="font-size:9pt;letter-spacing:.2em;text-transform:uppercase;color:var(--rosa)">Ilustração pendente · área 174 × 150 mm · 2055 × 1772 px a 300 dpi</div>
      <div style="font-family:'Cormorant Garamond';font-size:17pt;font-weight:600;margin:3mm 0">Cena: a casinha do Lobo no bosque</div>
      <p style="font-size:10pt;max-width:130mm;color:var(--sepia)">Aquarela tradicional, luz de fim de tarde. Interior de uma casinha de madeira entre faias; porta entreaberta.
      Uma menina de cachos dourados (5–6 anos, vestido azul-claro, avental creme) espia da porta. Mesa rústica com três tigelas de tamanhos
      claramente diferentes (grande, média, pequena), três cadeiras e, ao fundo, três camas. Nenhum lobo em cena. Espaço calmo no terço superior
      esquerdo. Paleta da coleção: verdes-musgo, ocres, azul-acinzentado, creme. Sem texto na imagem.</p>
      <p class="peq" style="margin-top:3mm">Esta página demonstra a diagramação de uma narrativa com cena pintada.
      A cena não pode ser pintada com qualidade neste ambiente — ver docs/03-ilustracao.md.</p>
    </div>
    <div class="historia" style="position:absolute;left:18mm;right:18mm;top:176mm">
      <h2 style="font-family:'Cormorant Garamond';font-weight:600;font-size:20pt;margin-bottom:2mm">Cachinhos Dourados e o Lobo</h2>
      <p class="capitular" style="font-size:15pt">No meio do bosque havia uma casinha. Ali morava um lobo — não o lobo das outras histórias,
      mas um lobo grande, um lobo médio e um lobo pequenino, que gostavam muito de mingau.</p>
      <p style="font-size:15pt">Numa manhã, o mingau estava quente demais, e os três foram passear enquanto ele esfriava…</p>
    </div>
    """
    return pagina(c, num="(modelo)", cab="Volume 2 · Histórias, memória e imaginação — página-modelo de narrativa", aba="--d-historias")


# ------------------------------------------------------------------ montagem

def montar(tela=False):
    paginas = [capa(), guia(), historia1(), historia2(), tracado(), flash_frente(), flash_verso(),
               memoria(), memoria_verso(), musica(), modelo_cena()]
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
    <title>O Grande Tesouro de Marina — Amostra editorial</title>
    <link rel="stylesheet" href="estilo.css"></head>
    <body class="{'tela' if tela else ''}">{''.join(paginas)}</body></html>"""
    nome = "amostra-tela.html" if tela else "amostra.html"
    p = os.path.join(AQUI, nome)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    return p


def main():
    os.makedirs(SAIDA, exist_ok=True)
    env = dict(os.environ, NODE_PATH="/opt/node-tools/node_modules")
    falhou = False
    for tela, pdf in ((False, "amostra-v1-impressao.pdf"), (True, "amostra-v1-tela.pdf")):
        h = montar(tela)
        r = subprocess.run(["node", os.path.join(AQUI, "pdf.js"), h, os.path.join(SAIDA, pdf)], env=env,
                           capture_output=True, text=True)
        print(r.stdout.strip(), r.stderr.strip())
        falhou |= r.returncode != 0
    insp = os.path.join(SAIDA, "inspecao")
    os.makedirs(insp, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", os.path.join(SAIDA, "amostra-v1-tela.pdf"),
                    os.path.join(insp, "pagina")], check=True)
    sys.exit(1 if falhou else 0)


if __name__ == "__main__":
    main()
