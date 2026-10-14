"""
VOLUME 3 — NÚMEROS, FORMAS E RACIOCÍNIO
uso: python3 volume3.py
"""
import math
import os
import subprocess
import sys

from livro import (Livro, VERSAO, adulto, cabeca_folha, cartoes, credito_pd, gerar_pdf, guia, historia, img, lista,
                   marcas_corte, memoria, observacao, passos, pd, poema, ponto_inicio, pontilhado, rodape_folha,
                   sequencia, texto, titulo, tracado)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume3")

UNIDADES = [
    ("Unidade 1 · Um, nenhum e muitos", "--d-matematica"),
    ("Unidade 2 · Um para cada", "--d-vida"),
    ("Unidade 3 · Contar até cinco (e até nove)", "--d-matematica"),
    ("Unidade 4 · Grande, médio e pequeno", "--d-historias"),
    ("Unidade 5 · As formas", "--d-artes"),
    ("Unidade 6 · Padrões", "--d-memoria"),
    ("Unidade 7 · Onde está?", "--d-natureza"),
    ("Unidade 8 · Medir e ordenar", "--d-matematica"),
]
INICIO = {}


def lado(nome, w, direita=True):
    f = "right" if direita else "left"
    m = "0 0 3mm 5mm" if direita else "0 5mm 3mm 0"
    return pd(nome, w, f"float:{f};clear:both;margin:{m}")


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


def colunas(rotulos, top=46, alt=84):
    n = len(rotulos)
    w = (178 - (n - 1) * 6) / n
    return "".join(f'<div style="position:absolute;left:{16 + i * (w + 6):.1f}mm;top:{top}mm;width:{w:.1f}mm;height:{alt}mm" class="caixa centro">'
                   f'<div style="font-size:16pt;font-weight:600">{r}</div></div>' for i, r in enumerate(rotulos))


def recortes(itens, top, w=30, h=38):
    cel = "".join(f'<div class="carta" style="width:{w}mm;height:{h}mm;display:inline-flex;margin:1mm;vertical-align:top">{html}<div class="peq">{n}</div></div>'
                  for html, n in itens)
    return f'<div class="centro" style="position:absolute;left:0;right:0;top:{top}mm">{cel}</div>'


def fila(motivo, n, w="16mm"):
    return ('<div style="text-align:center;line-height:0;max-width:26mm">'
            + "".join(img(motivo, w, "display:inline-block;margin:.4mm") for _ in range(n)) + "</div>")


# ================================================================== ABERTURA

def capa(L):
    formas = "".join(img(f, "30mm", "display:inline-block;margin:0 3mm") for f in ("circulo_vermelho", "quadrado_azul", "triangulo_amarelo", "retangulo_verde"))
    contas = "".join(img(c, "13mm", "display:inline-block;margin:0 1mm") for c in ["conta_vermelho", "conta_azul"] * 5)
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 3</div>
      <div style="font-weight:500;font-size:28pt;line-height:1.05;margin:2mm 0">Números, formas<br>e raciocínio</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:134mm;left:0;right:0">{pd("crane_porcos_mesa", "70mm", "margin:0 auto")}</div>
    <div class="centro" style="position:absolute;top:226mm;left:0;right:0">{formas}</div>
    <div class="centro" style="position:absolute;top:262mm;left:0;right:0">{contas}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 3</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">Números, formas e raciocínio</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">Os números deste livro são da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:14mm auto 0;width:96mm;height:72mm" class="caixa"><div class="peq" style="margin-top:30mm">a mão dela, contornada a lápis</div></div>
      <div style="margin-top:8mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Matemática com as mãos</h1>
      <p>Antes de ser escrita, a matemática é feita com as mãos e com o corpo: pôr um prato para cada pessoa, ver que uma pilha tem mais que
      a outra, achar a forma redonda da lua no prato, perceber que depois do vermelho vem o azul. Este volume não ensina contas nem
      cobra números escritos. Ele dá à Marina experiências de quantidade, forma, ordem e espaço, com objetos de verdade, que um dia
      vão dar sentido aos símbolos.</p>
      <h2>Três princípios</h2>
      <ul>
        <li><b>Do concreto ao abstrato</b> (Montessori). Primeiro o objeto (três colheres), depois a imagem (três colheres desenhadas),
        só então o símbolo (3). Muitas vezes ela vai ficar no primeiro passo — e está certo.</li>
        <li><b>Contar é tocar.</b> Um número para cada toque, um toque para cada objeto. Recitar “um, dois, três” é diferente de contar;
        as duas coisas vêm, cada uma no seu tempo.</li>
        <li><b>A linguagem da matemática.</b> Mais, menos, igual, muitos, nenhum, primeiro, último, dentro, fora, em cima, embaixo, comprido,
        curto, cheio, vazio. Use essas palavras no dia a dia: elas são tão importantes quanto os números.</li>
      </ul>
      <h2>O que esperar</h2>
      <p>Por volta dos 3 anos, muitas crianças contam até 3 ou 4 com correspondência; recitam mais longe do que conseguem contar; reconhecem
      círculo, quadrado e triângulo; e percebem padrões simples (vermelho, azul, vermelho, azul). Cada criança faz isso no seu ritmo. As
      atividades têm três níveis: escolha o que ela consegue com sucesso e suba um degrau quando ficar fácil.</p>
      <h2>Histórias e números</h2>
      <p>Os números aparecem em rimas e contos: o porquinho que foi ao mercado (as gravuras são de Walter Crane, 1870), a galinha do vizinho,
      os três ursos, um, dois, feijão com arroz. Contar com histórias é como os números entram na vida das crianças há séculos.</p>""")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Uma caixa de matemática</h1>
      <p>Monte, antes de começar, uma <b>caixa de matemática</b>: 10 botões grandes ou tampinhas, 10 feijões grandes (só com o adulto ao lado),
      5 colheres, 5 pratinhos, blocos de montar, uma fita métrica de costura, barbante, três tigelas de tamanhos diferentes, contas grandes de
      madeira e um cordão. Quase todas as atividades usam essas coisas.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Dois encontros por fim de semana, de 15 a 20 minutos. Uma unidade a cada dois fins de semana.</td></tr>
        <tr><th>No dia a dia</th><td>Contar degraus da escada, pratos da mesa, botões da roupa. É ali que a matemática fica.</td></tr>
        <tr><th>Números escritos</th><td>Os cartões de 1 a 9 mostram o numeral junto da quantidade. Ela não precisa escrevê-los. Se mostrar interesse,
        trace o número com o dedo, em tamanho grande, sem cobrar forma.</td></tr>
        <tr><th>Idiomas</th><td>Os números aparecem também em inglês, francês e latim no verso dos cartões: contar em outra língua é uma brincadeira de que
        as crianças gostam.</td></tr>
      </table>
      <h2>Segurança</h2>
      <p>Botões, feijões e contas pequenas só com o adulto ao lado, e guardados depois. Prefira contas de madeira com mais de 3 cm.</p>
      <div class="centro" style="margin-top:6mm">{img("caixa", "40mm", "display:inline-block;margin:0 3mm")}
      {"".join(img(c, "12mm", "display:inline-block;margin:0 1mm") for c in ("conta_vermelho", "conta_azul", "conta_amarelo", "conta_verde"))}</div>""")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio.get(n, "")}</td></tr>' for n, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Meus números, diário e repertório</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Volume 3 · Números, formas e raciocínio", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{"".join(img(f"barra_{k}", f"{k * 10}mm", "margin:1mm auto") for k in range(1, 6))}</div></div>"""


# ================================================================== U1 UM, NENHUM, MUITOS

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · Um, nenhum e muitos", aba="--d-matematica",
        pergunta="Quantos? Um, nenhum, alguns, muitos — as primeiras palavras da quantidade.",
        duracao="Dois fins de semana · dois encontros · 15 minutos. Comece no dia a dia: “um biscoito ou muitos?”.",
        objetivos=["Distinguir um, nenhum e muitos.", "Recitar uma parlenda numérica com gestos.", "Associar cada dedo a uma parte da rima (correspondência).",
                   "Separar cartões em três grupos: um, muitos, nenhum.", "Ouvir e produzir “um som” e “muitos sons”."],
        repertorio="<b>Parlenda:</b> <i>Um, dois, feijão com arroz</i> (tradicional). <b>Rima de dedos:</b> <i>Este porquinho foi à feira</i> "
                   "(tradução da coleção de <i>This little pig went to market</i>). <b>Imagens:</b> Walter Crane (c. 1870). <b>Línguas:</b> <i>one · un · ūnus</i>.",
        materiais="Uma tigela com feijões grandes; uma cesta vazia; botões; os cartões da unidade.",
        vida="Servir: “pegue <i>um</i> guardanapo”, “pegue <i>muitos</i> morangos”, “não sobrou <i>nenhum</i>”.",
        etapas=[["Parlenda com palmas.", "Rima do porquinho nos dedos dos pés.", "Um e muitos na mesa."],
                ["Separar: um, muitos, nenhum.", "Contar os porquinhos de Crane.", "Um som, muitos sons."],
                ["Ela pede: “quero um”, “quero muitos”.", "Inventar o sexto porquinho.", "Esconder todos: nenhum!"]],
        indicadores=["Diz “um” e “muitos” corretamente.", "Entende “nenhum” (mostra a cesta vazia).", "Acompanha a parlenda com gestos.",
                     "Toca um dedo por verso.", "Separa os cartões com poucos erros.", "Usa “mais” espontaneamente."],
        interesse="conte na rua: uma porta, muitas janelas; um sol, muitas nuvens.",
        dificil="só a rima do porquinho nos dedos.",
        alerta="<b>Feijões e botões</b> só com o adulto ao lado."))

    poema(L, "Um, dois, feijão com arroz", "parlenda tradicional brasileira",
          ["Um, dois, feijão com arroz;<br>três, quatro, feijão no prato;",
           "cinco, seis, chegou minha vez;<br>sete, oito, comer biscoito;",
           "nove, dez, comer pastéis!"],
          img("tigela", "36mm", "display:inline-block;margin:0 3mm") + img("colher", "22mm", "display:inline-block;margin:0 3mm") + img("prato", "40mm", "display:inline-block;margin:0 3mm"),
          adulto("recitar e contar",
                 "Recite batendo palmas no ritmo; nos números, mostre os dedos (um dedo, dois dedos…). Aos 2 ou 3 anos, recitar até dez é uma "
                 "<b>música</b>, não uma contagem: ela pode recitar bem e ainda contar só até três. As duas coisas são boas. "
                 "Há versões regionais da parlenda (“cinco, seis, falar inglês”); use a que vocês conhecem."),
          aba="--d-historias")

    historia(L, "Este porquinho foi à feira", "rima de dedos inglesa · tradução da coleção", f"""
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:3mm 0 4mm">
        <div class="centro">{pd("crane_porco_mercado", "52mm")}<div class="legenda-q">1 · foi à feira</div></div>
        <div class="centro">{pd("crane_porco_casa", "52mm")}<div class="legenda-q">2 · ficou em casa</div></div>
        <div class="centro">{pd("crane_porco_nada", "52mm")}<div class="legenda-q">4 · não comeu nada</div></div></div>
      <p style="font-size:16pt;line-height:1.6;text-align:center;font-style:italic">Este porquinho foi à feira,<br>este porquinho ficou em casa,<br>
      este porquinho comeu um bolinho,<br>este porquinho não comeu nada,<br>e este porquinho chorou: “uí, uí, uí!”<br>todo o caminho até em casa.</p>""",
             adulto("rima de dedos",
                    "Pegue o pé (ou a mão) dela e toque um dedo a cada verso, do dedão ao mindinho. No “uí, uí, uí”, os seus dedos sobem correndo pela "
                    "perna dela até a barriga — e cócegas. É uma correspondência um a um: <b>um verso para cada dedo</b>. Depois de muitas vezes, ela vai "
                    "fazer nos seus dedos. Crane pintou o terceiro porquinho comendo rosbife; na tradução, ele come um bolinho.",
                    credito_pd("crane_porco_mercado", "crane_porco_casa", "crane_porco_nada")),
             aba="--d-historias")

    observacao(L, "A família porquinho à mesa", "Walter Crane · <i>This Little Pig Went to Market</i> (c. 1870)", pd("crane_porcos_mesa", "104mm"),
               ["Quantos porquinhos estão à mesa? Vamos contar tocando.", "E quem está servindo? Ele é <b>um</b> só.",
                "Há <b>muitos</b> pratos ou só um?", "Ache a colher que caiu no chão.", "Tem algum gato na sala? (<b>nenhum</b>!)"],
               adulto("um, muitos e nenhum numa cena",
                      "Há quatro porquinhos sentados e um (o pai) servindo: cinco ao todo. Na mesa, quatro pratinhos azuis, quatro colheres e uma travessa; "
                      "no chão, mais um prato com colher. Para ela, basta perceber “um que serve” e “muitos que comem”. Contar até quatro é ótimo; não precisa acertar o total.",
                      credito_pd("crane_porcos_mesa")),
               aba="--d-matematica")

    itens = [(fila("maca", 1, "18mm"), "uma maçã"), (fila("uva", 1, "24mm"), "um cacho"), (fila("estrela", 7, "6mm"), "estrelas"),
             (fila("peixe", 1, "22mm"), "um peixe"), (fila("bolhas", 3, "9mm"), "bolhas"), (fila("florzinha_rosa", 4, "6mm"), "flores")]
    c = f"""<div class="miolo">{titulo("Um, muitos ou nenhum?", "separar em três cestas", 28)}</div>
    {colunas(["um", "muitos", "nenhum"], 46, 70)}
    <div style="position:absolute;left:142mm;top:72mm;width:52mm" class="centro">{img("cesta", "40mm", "margin:0 auto;opacity:.6")}</div>
    {recortes(itens, 126)}
    <div class="centro peq" style="position:absolute;left:0;right:0;top:172mm">recortar os seis cartões e pôr cada um na cesta certa</div>
    {adulto("classificar quantidades",
            "A terceira coluna, “nenhum”, fica vazia de propósito: nenhum cartão vai para lá — e isso é a ideia de zero. Pergunte: “o que tem na cesta do nenhum?” — "
            "“nada!”. <b>Com objetos:</b> três pratos na mesa; ponha um feijão num, muitos noutro, nenhum no terceiro. "
            "<b>Criar:</b> ela arruma os pratos e você adivinha qual é o “um”, o “muitos” e o “nenhum”.",
            estilo="top:186mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Um som, muitos sons", "escutar quantidades", 28)}
      <table class="tab" style="font-size:13pt;margin-top:8mm">
        <tr><td style="width:40mm">{img("sino", "26mm")}</td><td><b>um</b> — uma badalada do sino: <i>dlém!</i></td></tr>
        <tr><td>{img("tambor", "28mm")}</td><td><b>muitos</b> — muitas batidinhas no tambor: <i>tum-tum-tum-tum-tum…</i></td></tr>
        <tr><td>{img("bolhas", "26mm", "opacity:.4")}</td><td><b>nenhum</b> — silêncio: as mãos param no ar.</td></tr></table>
      <p class="centro" style="font-size:14pt;font-style:italic;margin-top:8mm">E se eu tocar duas vezes? <i>dlém, dlém!</i> E três?</p></div>
    {adulto("quantidade sonora",
            "De olhos fechados, ela escuta: você toca uma vez, muitas vezes ou nenhuma. Ela responde com a palavra ou com o dedo (um dedo, mãos abertas, mãos fechadas). "
            "Quando ficar fácil, toque duas e três vezes e peça que ela conte as batidas — contar sons é mais difícil que contar objetos, porque eles desaparecem.")}"""
    L.add(c, aba="--d-musica")

    passos(L, "Um para mim, um para você", "repartir na mesa",
           [(fila("morango", 2, "18mm"), "Dois morangos: um para mim, um para você"),
            (fila("maca", 1, "22mm") + img("maca_cortada", "22mm", "display:inline-block"), "Uma maçã cortada: um pedaço para cada um"),
            (fila("bolota", 4, "12mm"), "Quatro biscoitos para duas pessoas"),
            (img("cesta", "28mm"), "Sobrou algum? Nenhum!"),
            (fila("xicara", 2, "20mm"), "Uma xícara para cada um"),
            (img("ratinho", "26mm"), "E para o ratinho? Um farelinho!")],
           adulto("vida prática e quantidade",
                  "Repartir é o começo da divisão — sem nome nem conta. Deixe que ela distribua: “um para você, um para mim”, até acabar. "
                  "Pergunte depois: “quem ficou com mais? ficou igual?”. Os biscoitos da imagem são bolotas de carvalho; use biscoitos de verdade."),
           aba="--d-vida")


# ================================================================== U2 UM PARA CADA

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · Um para cada", aba="--d-vida",
        pergunta="Tem para todo mundo? Sobra ou falta? — a correspondência um a um.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos, sempre com objetos da mesa.",
        objetivos=["Fazer correspondência um a um (um prato para cada pessoa).", "Perceber quando sobra e quando falta.",
                   "Ligar pares com uma linha.", "Associar objetos que vão juntos (colher e tigela, luva e mão).", "Pôr a mesa para quatro pessoas."],
        repertorio="<b>História:</b> <i>A mesa dos porquinhos</i> (texto da coleção, a partir da gravura de Crane). <b>Imagens:</b> Walter Crane (c. 1870). "
                   "<b>Línguas:</b> <i>two · deux · duo</i>; <i>pair · la paire · pār</i>.",
        materiais="Pratos, xícaras e colheres (4 de cada); bichinhos de pelúcia; lápis grosso; os cartões da unidade.",
        vida="Pôr a mesa da família: contar as pessoas e pegar um prato para cada uma.",
        etapas=[["História da mesa dos porquinhos.", "Um prato para cada bichinho.", "Ver os pares: colher e tigela."],
                ["Ligar com linhas.", "Sobrou ou faltou?", "Memória dos pares que combinam."],
                ["Pôr a mesa da família.", "Inventar pares novos.", "Festa de bichinhos para cinco."]],
        indicadores=["Põe um objeto para cada lugar sem pular.", "Diz “falta um” ou “sobrou um”.", "Liga pares com o dedo ou com a linha.",
                     "Encontra o par que combina.", "Conta as pessoas da família.", "Põe a mesa com pouca ajuda."],
        interesse="calçar os sapatos aos pares, guardar as meias aos pares, tampar potes: pares estão por toda parte.",
        dificil="só pôr a mesa juntas."))

    historia(L, "A mesa dos porquinhos", "uma história da coleção", f"""
      {lado("crane_porcos_mesa", "76mm")}
      <p class="capitular" style="margin-top:4mm">Na casa dos porquinhos, o jantar estava quase pronto.</p>
      <p>O papai porco contou os filhos: um, dois, três, quatro.</p>
      <p class="fala">— Quatro porquinhos, quatro pratos!</p>
      <p>Pôs um prato para cada um. Depois uma colher para cada prato.</p>
      <p>Mas… <i>toc, toc!</i> Chegou a vovó porca para jantar.</p>
      <p class="fala">— Oh! Agora somos mais um. Falta um prato!</p>
      <p>O porquinho menor correu à cozinha e trouxe mais um prato e mais uma colher. E todos jantaram juntos.</p>""",
             adulto("contar e corresponder",
                    "Conte os porquinhos da imagem com ela. Depois, com bichinhos de pelúcia e pratos de verdade, repitam a história: quatro bichinhos, "
                    "quatro pratos; chega mais um — falta um! Deixe que ela descubra sozinha que falta.",
                    credito_pd("crane_porcos_mesa")),
             aba="--d-historias")

    def linha(esq, dir_, n_esq, n_dir, y):
        e = "".join(img(esq, "20mm", f"position:absolute;left:24mm;top:{y + k * 24}mm") for k in range(n_esq))
        d = "".join(img(dir_, "20mm", f"position:absolute;left:160mm;top:{y + k * 24}mm") for k in range(n_dir))
        pts = "".join(f'<circle cx="46" cy="{y + 10 + k * 24}" r="1.6" fill="var(--sepia)"/>' for k in range(n_esq))
        pts += "".join(f'<circle cx="158" cy="{y + 10 + k * 24}" r="1.6" fill="var(--sepia)"/>' for k in range(n_dir))
        return e + d, pts
    h1, p1 = linha("xicara", "colher", 3, 3, 46)
    c = f"""<div class="miolo">{titulo("Uma colher para cada xícara", "ligar com o dedo, depois com o lápis", 26)}</div>
    {h1}<svg class="svgpag" viewBox="0 0 210 297">{p1}</svg>
    {adulto("ligar pares",
            "Cada xícara ganha uma colher: com o dedo, ela vai do pontinho da xícara até o pontinho de uma colher. Qualquer colher serve — o que importa é "
            "<b>uma para cada</b>. Depois, com lápis grosso, ela traça as linhas. Não precisam ser retas. Pergunte no fim: “sobrou alguma colher?” (nenhuma). "
            "<b>Com objetos:</b> três xícaras e três colheres de verdade na mesa.",
            estilo="top:132mm;bottom:auto")}
    <div class="miolo" style="top:178mm">{titulo("E agora?", "", 20)}</div>"""
    h2, p2 = linha("tigela", "colher", 3, 2, 196)
    c += h2 + f'<svg class="svgpag" viewBox="0 0 210 297">{p2}</svg>'
    c += '<div class="peq it" style="position:absolute;left:62mm;right:62mm;top:212mm;text-align:center">três tigelas, duas colheres… faltou uma!</div>'
    L.add(c, aba="--d-matematica")

    memoria(L, "Coisas que combinam", [("tigela", img("tigela", "30mm")), ("colher", img("colher", "30mm")), ("luva", img("luva", "30mm")),
                                       ("mão", img("palma", "30mm")), ("guarda-chuva", img("guarda_chuva", "30mm")), ("bota", img("bota", "30mm"))],
            [0, 2, 4, 1, 3, 5, 5, 1, 0, 3, 4, 2],
            adulto("pares que combinam",
                   "Diferente da memória comum: aqui o par não é igual, é <b>o que vai junto</b> — tigela e colher, luva e mão, guarda-chuva e bota de chuva. "
                   "Primeiro com as cartas viradas para cima: “o que combina com a tigela?”. Ela pode inventar outros pares (bota e luva, porque são de vestir): "
                   "se ela explicar, vale.",
                   estilo="bottom:19mm;top:auto"))

    lugares = ""
    for k, (x, y) in enumerate(((40, 60), (130, 60), (40, 140), (130, 140))):
        lugares += (f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:60mm;height:62mm" class="caixa centro">'
                    f'<svg viewBox="0 0 60 60" style="width:44mm;height:44mm;margin-top:4mm"><circle cx="30" cy="30" r="20" fill="none" stroke="var(--sepia-claro)" stroke-dasharray="1.5 1.5" stroke-width=".6"/>'
                    f'<rect x="54" y="12" width="3" height="36" rx="1.5" fill="none" stroke="var(--sepia-claro)" stroke-dasharray="1.5 1.5" stroke-width=".6"/></svg>'
                    f'<div class="peq">lugar {k + 1}</div></div>')
    c = f"""<div class="miolo">{titulo("Mesa para quatro", "um prato e uma colher em cada lugar", 26)}</div>{lugares}
    {adulto("pôr a mesa",
            "Imprima (ou desenhe) e ponha sobre a mesa. Ela traz quatro pratinhos e quatro colheres de verdade e põe um em cada lugar. "
            "<b>Relacionar:</b> entregue cinco pratos — sobra um! — ou três — falta um. <b>Criar:</b> quantas pessoas vão jantar hoje? Ela conta a família e põe a mesa.",
            estilo="top:212mm;bottom:auto")}"""
    L.add(c, aba="--d-vida")

    pares = [("meias", "pegada", "pegada_esq"), ("luvas", "luva", "luva"), ("cerejas", "cereja", "cereja"), ("botas", "bota", "bota")]
    linhas = "".join(f'<tr><td style="width:50mm;font-size:13pt">um par de {n}</td><td>{img(a, "22mm", "display:inline-block;margin:0 2mm")}'
                     f'{img(b, "22mm", "display:inline-block;margin:0 2mm" + (";transform:scaleX(-1)" if a == b else ""))}</td></tr>' for n, a, b in pares)
    c = f"""<div class="miolo">{titulo("Os pares", "dois que andam juntos", 28)}<table class="tab" style="margin-top:8mm">{linhas}</table></div>
    {adulto("o número dois",
            "Par é o primeiro “dois” da vida: dois pés, duas mãos, duas meias. Ao guardar a roupa, peça que ela junte as meias aos pares. "
            "“Um par de sapatos tem quantos sapatos?” — dois. Mostre também as duas cerejas presas pelo cabinho (Volume 1). "
            "Em inglês: <i>a pair</i>; em francês: <i>une paire</i>; em latim: <i>pār</i>, de onde vem a palavra “par”.")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Um passo para cada batida", "marcha e pulso", 28)}
      <div class="centro" style="margin:6mm 0">{img("tambor", "50mm")}</div>
      <p class="centro" style="font-size:22pt;letter-spacing:.3em;color:var(--d-musica)">● ● ● ● ● ● ● ●</p>
      <p class="centro" style="font-size:12pt;font-style:italic">um passo · um passo · um passo · um passo…</p>
      <p class="centro" style="font-size:14pt;margin-top:8mm;line-height:1.6">Marcha, soldado, cabeça de papel;<br>se não marchar direito,<br>vai preso no quartel!</p>
      <p class="centro peq">cantiga tradicional</p></div>
    {adulto("correspondência no tempo",
            "Você bate o tambor (ou a panela) num pulso regular; ela dá <b>um passo para cada batida</b> — correspondência um a um, só que no tempo. "
            "Comece devagar. Depois mude o andamento: batidas rápidas, passos rápidos; batidas lentas, passos de gigante. Quando você para, ela para.")}"""
    L.add(c, aba="--d-musica")


# ================================================================== U3 CONTAR

NUMEROS = [
    (1, "um", "maca", "one", "un", "ūnus"), (2, "dois", "cereja", "two", "deux", "duo"), (3, "três", "pera", "three", "trois", "trēs"),
    (4, "quatro", "morango", "four", "quatre", "quattuor"), (5, "cinco", "estrela", "five", "cinq", "quīnque"),
    (6, "seis", "florzinha_rosa", "six", "six", "sex"), (7, "sete", "bolota", "seven", "sept", "septem"),
    (8, "oito", "folha", "eight", "huit", "octō"), (9, "nove", "conta_azul", "nine", "neuf", "novem"),
]


def cartao_numero(n, mot):
    w = 13 if n <= 4 else (10 if n <= 6 else 8.5)
    objs = "".join(img(mot, f"{w}mm", "display:inline-block;margin:.4mm") for _ in range(n))
    return (f'<div style="font-size:44pt;line-height:1;font-weight:500;color:var(--rosa)">{n}</div>'
            f'<div style="width:46mm;text-align:center;line-height:0">{objs}</div>')


def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · Contar até cinco (e até nove)", aba="--d-matematica",
        pergunta="Quantos são? Um número para cada toque, e o último diz quantos há.",
        duracao="Três fins de semana · dois encontros · 15 a 20 minutos. Fique no 1 a 3 enquanto for preciso; o 4 e o 5 vêm depois; 6 a 9 é para mais tarde.",
        objetivos=["Contar objetos tocando um de cada vez.", "Entender que o último número dito é a quantidade (cardinalidade).",
                   "Reconhecer pequenas quantidades sem contar (1, 2, 3 de uma olhada).", "Associar quantidade e numeral, quando houver interesse.",
                   "Recitar uma rima de contar até dez."],
        repertorio="<b>Rima:</b> <i>A galinha do vizinho</i> (tradicional). <b>Imagens:</b> Kate Greenaway (1878). "
                   "<b>Línguas:</b> os números de 1 a 9 em inglês, francês e latim, no verso dos cartões.",
        materiais="Botões ou tampinhas; 9 pratinhos ou forminhas de papel; os cartões de números; giz grosso.",
        vida="Contar os degraus da escada, os pratos da mesa, as pessoas no almoço.",
        etapas=[["Rima da galinha com os dedos.", "Contar 1, 2, 3 objetos.", "Cartões 1 a 3."],
                ["Pôr a quantidade certa no pratinho.", "Contar os gansos de Greenaway.", "Ver 1, 2, 3 sem contar."],
                ["Ela é a professora: conta para o ratinho.", "Esconder e contar quantos sobraram.", "Traçar o número com o dedo (se quiser)."]],
        indicadores=["Conta 3 objetos tocando cada um.", "Responde “quantos?” com o último número.", "Põe 3 botões quando pedido.",
                     "Reconhece 2 e 3 de uma olhada.", "Recita até 5 ou mais.", "Liga numeral e quantidade de 1 a 3."],
        interesse="conte em inglês e francês no carro; conte as estrelas de uma noite clara.",
        dificil="só contar os degraus subindo a escada."))

    cartoes(L, "Números de 1 a 9", [dict(pt=pt, html=cartao_numero(n, mot), en=en, fr=fr, la=la,
                                         dica=f"Ponha {pt} botões no pratinho. Conte tocando.") for n, pt, mot, en, fr, la in NUMEROS],
            "Unidade 3 · Contar", sub_frente="frente · numeral e quantidade · imprimir frente e verso (borda longa) · cortar nas linhas")

    poema(L, "A galinha do vizinho", "rima tradicional de contar",
          ["A galinha do vizinho<br>bota ovo amarelinho;",
           "bota um, bota dois, bota três,<br>bota quatro, bota cinco, bota seis,",
           "bota sete, bota oito, bota nove,<br>bota dez!"],
          pd("cartao_galo", "40mm", "display:inline-block"),
          adulto("rima de contar",
                 "Mostre um dedo a cada número. Aos poucos, vá parando antes do número: “bota um, bota…” — e ela completa. "
                 "Contar ovos de verdade (de uma caixa de ovos, com cuidado) é a melhor continuação: a caixa tem lugares, e cada ovo ocupa um.",
                 credito_pd("cartao_galo")),
          aba="--d-historias")

    observacao(L, "Quantos gansos?", "Kate Greenaway · <i>Under the Window</i> (1878)", pd("greenaway_gansos", "160mm"),
               ["Conte os gansos tocando cada um: um, dois…", "Quantos são? (o último número que você disse!)",
                "Para que lado eles andam?", "Qual é o primeiro da fila? E o último?"],
               adulto("contar numa imagem",
                      "São cinco gansos, todos andando para a direita. O desafio de contar numa imagem é não contar o mesmo duas vezes: mostre como "
                      "tocar da esquerda para a direita. Se ela errar, conte de novo junto, devagar, sem dizer que errou.",
                      credito_pd("greenaway_gansos")),
               aba="--d-matematica")

    pratos = "".join(f'<div style="position:absolute;left:{18 + (k % 3) * 60}mm;top:{50 + (k // 3) * 76}mm;width:54mm;height:68mm" class="caixa centro">'
                     f'<div style="font-size:34pt;color:var(--rosa);line-height:1.1">{k + 1}</div>'
                     f'<svg viewBox="0 0 50 40" style="width:46mm;height:36mm"><ellipse cx="25" cy="20" rx="22" ry="16" fill="none" stroke="var(--sepia-claro)" stroke-width=".6" stroke-dasharray="1.4 1.4"/></svg></div>'
                     for k in range(6))
    c = f"""<div class="miolo">{titulo("Ponha tantos quanto diz", "um botão para cada número", 26)}</div>{pratos}
    {adulto("quantidade e numeral",
            "Em cada prato desenhado, ela põe a quantidade de botões que o número diz — tocando e contando. Comece só com 1, 2 e 3 (cubra os outros com papel). "
            "<b>Conferir:</b> depois, conte junto com ela. <b>Criar:</b> ela põe botões num prato e você diz o número — e às vezes erra de propósito para ela corrigir.",
            estilo="top:206mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    quadros = [(1, (50, 50)), (2, (40, 60)), (3, (30, 60)), (2, (60, 40)), (3, (40, 40)), (1, (60, 60))]
    cel = ""
    for k, (n, _) in enumerate(quadros):
        x, y = 18 + (k % 3) * 60, 50 + (k // 3) * 64
        pts = {1: [(25, 25)], 2: [(15, 15), (35, 35)], 3: [(12, 38), (25, 25), (38, 12)]}[n]
        dots = "".join(f'<circle cx="{px}" cy="{py}" r="5.5" fill="#c0716b"/>' for px, py in pts)
        cel += (f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:54mm;height:56mm" class="caixa centro">'
                f'<svg viewBox="0 0 50 50" style="width:42mm;height:42mm;margin-top:6mm">{dots}</svg></div>')
    c = f"""<div class="miolo">{titulo("De uma olhada só", "quantos pontos? sem contar!", 26)}</div>{cel}
    {adulto("subitização",
            "Até três, o olho reconhece a quantidade de uma vez, sem contar — é o que fazemos com os dados. Cubra a página com uma folha, "
            "mostre um quadro por um segundo e esconda de novo: “quantos você viu?”. Depois, confiram contando. A disposição muda de quadro para quadro "
            "de propósito: três pontos em linha e três em diagonal são o mesmo três.",
            estilo="top:186mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    svg = ""
    for k, (x, d) in enumerate(((45, "M 38 95 L 50 80 L 50 170"),
                                 (105, "M 88 98 C 88 78 122 78 122 100 C 122 120 88 150 86 170 L 124 170"),
                                 (165, "M 148 90 C 152 76 182 78 180 98 C 178 114 160 118 156 120 C 176 120 186 136 182 152 C 176 174 148 172 144 160"))):
        svg += pontilhado(d, w=3.2)
        start = d.split()[1:3]
        svg += ponto_inicio(float(start[0]), float(start[1]))
    imgs = "".join(img("conta_vermelho", "10mm", f"position:absolute;left:{x}mm;top:186mm") for x in (40,)) + \
        "".join(img("conta_azul", "10mm", f"position:absolute;left:{x}mm;top:186mm") for x in (94, 106)) + \
        "".join(img("conta_amarelo", "10mm", f"position:absolute;left:{x}mm;top:186mm") for x in (148, 160, 172))
    tracado(L, "1 · 2 · 3", "traçar com o dedo, só se ela quiser", svg, imgs,
            adulto("o numeral (opcional)",
                   "Esta página é para quando ela mostrar interesse pelos números escritos — não antes. Com o dedo, do círculo verde até o fim, dizendo o nome do número; "
                   "depois, conte as contas embaixo. Não peça que ela escreva números. Traçar na areia ou no ar, com o braço inteiro, é ainda melhor."),
            aba="--d-memoria")


# ================================================================== U4 GRANDE MÉDIO PEQUENO

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · Grande, médio e pequeno", aba="--d-historias",
        pergunta="Maior que, menor que, do mesmo tamanho — comparar e pôr em ordem.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos.",
        objetivos=["Usar grande, médio, pequeno, maior, menor.", "Ordenar três objetos e depois cinco.", "Comparar alturas e comprimentos lado a lado.",
                   "Recontar a casa dos ursos (Volume 2) como problema de tamanhos.", "Mover o corpo em tamanhos: passos de gigante e de formiga."],
        repertorio="<b>Retomada:</b> <i>Cachinhos Dourados</i> (Volume 2), com as cadeiras de L. Leslie Brooke (1905), e a versão da família, com o Lobo. "
                   "<b>Línguas:</b> <i>big, small · grand, petit · magnus, parvus</i>.",
        materiais="Três tigelas, três almofadas, copos de encaixar ou potes de tamanhos diferentes; fita crepe; bichinhos.",
        vida="Guardar os potes um dentro do outro (do maior para o menor).",
        etapas=[["As três cadeiras dos ursos.", "Comparar dois: qual é maior?", "Passos de gigante e de formiga."],
                ["Ordenar três círculos.", "Torre de potes.", "Quem é mais alto na família?"],
                ["Ordenar cinco.", "Inventar uma família de cinco lobos.", "Medir os bichinhos e pôr em fila."]],
        indicadores=["Diz qual é maior entre dois.", "Ordena três sem ajuda.", "Usa “médio”.", "Encaixa potes do maior ao menor.",
                     "Ordena cinco com uma ou duas correções.", "Compara alturas lado a lado."],
        interesse="a família de bonecas russas (matrioscas) é o material perfeito para esta unidade.",
        dificil="só as três tigelas e as três almofadas."))

    observacao(L, "As cadeiras dos ursos", "L. Leslie Brooke · <i>The Golden Goose Book</i> (1905)", pd("brooke_cadeiras", "110mm"),
               ["Quem são os três ursos? Aponte o grande, o médio e o pequeno.", "Ache a cadeira <b>grande</b>. E a pequenina?",
                "Qual urso está mais perto? E mais longe?", "Na nossa história, se fossem três lobos: o Lobão, a Loba e o Lobinho…"],
               adulto("tamanhos numa cena",
                      "Brooke pinta os três ursos descobrindo as cadeiras mexidas. Na versão da família, com o Lobo, a mesma cena tem três tamanhos de lobo. "
                      "Pergunte: “e se chegasse um quarto urso, ainda menor? onde ele sentaria?”.",
                      credito_pd("brooke_cadeiras")),
               aba="--d-historias")

    tam = [(20, "circulo_vermelho"), (34, "circulo_azul"), (48, "circulo_amarelo")]
    misturados = [tam[1], tam[2], tam[0]]
    cel = "".join(f'<td style="vertical-align:bottom;text-align:center"><div class="carta" style="display:inline-flex;width:{w + 6}mm;height:{w + 6}mm">{img(m, f"{w}mm")}</div></td>'
                  for w, m in misturados)
    c = f"""{cabeca_folha("Do pequeno ao grande", "recortar os três círculos e pôr em ordem · depois, uns sobre os outros", 12)}
    <table style="position:absolute;left:16mm;top:36mm;width:178mm"><tr>{cel}</tr></table>
    <div class="centro" style="position:absolute;left:0;right:0;top:108mm;font-size:13pt">pequeno &nbsp; · &nbsp; médio &nbsp; · &nbsp; grande</div>
    <div style="position:absolute;left:30mm;right:30mm;top:118mm;height:60mm;display:flex;align-items:flex-end;justify-content:space-around">
      <div class="caixa" style="width:26mm;height:26mm"></div><div class="caixa" style="width:40mm;height:40mm"></div><div class="caixa" style="width:54mm;height:54mm"></div></div>
    {adulto("seriação",
            "Recorte os três círculos (cole sobre papelão para durar). <b>Descobrir:</b> “qual é o maior?”. <b>Relacionar:</b> ela põe cada um no quadro do seu tamanho, "
            "do pequeno ao grande. <b>Criar:</b> empilhar o pequeno sobre o médio sobre o grande — um alvo — e depois ao contrário: “por que o grande não cabe em cima?”.",
            estilo="top:200mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    barras = "".join(f'<div style="margin:3mm 0">{img(f"barra_{k}", f"{k * 22 + 3}mm")}</div>' for k in (3, 1, 5, 2, 4))
    c = f"""{cabeca_folha("A escada de cinco barras", "recortar as barras e montar uma escada, da mais curta à mais comprida", 12)}
    <div style="position:absolute;left:18mm;top:36mm">{barras}</div>
    {adulto("ordenar cinco",
            "Inspiradas nas barras vermelhas de Montessori: cada barra tem o tamanho de uma, duas, três, quatro ou cinco barras pequenas. "
            "Recorte (cole sobre papelão). <b>Relacionar:</b> alinhe todas pela esquerda e deixe que ela as ponha em ordem, formando uma escada. "
            "Comece com três (1, 3, 5), que são bem diferentes. <b>Criar:</b> quantas barras pequenas cabem na maior? Coloque-as lado a lado — cinco!",
            estilo="top:200mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    linhas = "".join(f'<tr><td style="height:12mm;width:60mm">{p}</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>'
                     for p in ("Marina", "Mamãe", "Papai", "o ratinho de pelúcia", "", ""))
    c = f"""<div class="miolo">{titulo("Quem é mais alto?", "a fita da família", 28)}
      <div class="texto" style="margin-top:4mm"><p>Cole uma tira de papel comprida na parede, do chão para cima. Cada pessoa encosta as costas na parede e
      faz-se uma marca na altura da cabeça, com o nome e a data.</p></div>
      <table class="tab" style="font-size:12pt;margin-top:4mm"><tr><th>quem</th><th>a altura, medida em palmos da Marina (ou em barras)</th></tr>{linhas}</table></div>
    {adulto("comparar alturas",
            "Comparar lado a lado é o primeiro jeito de medir: “quem é mais alto, você ou o papai?”. Na fita, as marcas ficam em ordem sozinhas — uma escada "
            "de alturas. Volte à fita daqui a alguns meses: ela vai adorar ver que cresceu. Medir em palmos da mão dela vem na Unidade 8.")}"""
    L.add(c, aba="--d-matematica")

    passos(L, "Passos de gigante, passos de formiga", "o tamanho no corpo",
           [(img("barra_5", "40mm"), "Passo de gigante: bem comprido"),
            (img("barra_1", "10mm"), "Passo de formiga: bem curtinho"),
            (img("circulo_amarelo", "28mm"), "Ficar grande: braços abertos, na ponta dos pés"),
            (img("circulo_azul", "12mm"), "Ficar pequenininha: encolhida no chão"),
            (img("tambor", "26mm"), "Tambor forte: gigante · tambor fraco: formiga"),
            (img("ratinho", "24mm"), "E o ratinho? Passo de rato!")],
           adulto("movimento e tamanho",
                  "Brincadeira tradicional: “Mamãe, posso ir?” — “Pode: dois passos de gigante!”. Marque a chegada com fita crepe. "
                  "Contar os passos também é medir: quantos passos de gigante até a porta? E de formiga?"),
           aba="--d-vida")

    c = f"""<div class="miolo">{titulo("Os três lobos", "a versão da família, para contar com tamanhos", 26)}
      <p style="font-size:15pt;line-height:1.5;margin-top:6mm">Era uma vez três lobos: o <b>Lobão</b>, grande; a <b>Loba</b>, média; e o <b>Lobinho</b>, pequenininho.</p>
      <p style="font-size:15pt;line-height:1.5">Tinham três tigelas: uma grande, uma média e uma pequenininha. Três cadeiras: uma grande, uma média e uma pequenininha.
      E três camas: uma grande, uma média e uma pequenininha…</p>
      <p style="font-size:15pt;line-height:1.5;font-style:italic">— E o que aconteceu, Marina?</p>
      <div class="centro" style="margin:6mm 0">{img("tigela", "44mm", "display:inline-block;margin:0 3mm;vertical-align:bottom")}{img("tigela", "32mm", "display:inline-block;margin:0 3mm;vertical-align:bottom")}{img("tigela", "20mm", "display:inline-block;margin:0 3mm;vertical-align:bottom")}</div>
      <div class="caixa" style="height:52mm"><div class="peq centro" style="margin-top:2mm">o que a Marina contou</div></div></div>
    {adulto("criar: contar com tamanhos",
            "Comece a história e deixe que ela continue. A estrutura de três tamanhos é o que importa: cada coisa da casa vem em grande, médio e pequeno. "
            "Escreva aqui as palavras dela. Se ela quiser cinco lobos, ótimo — use a escada de barras para mostrar os cinco tamanhos.")}"""
    L.add(c, aba="--d-historias")


# ================================================================== U5 FORMAS

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · As formas", aba="--d-artes",
        pergunta="Redondo, quadrado, triângulo, retângulo — onde estão as formas no mundo?",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos.",
        objetivos=["Reconhecer e nomear círculo, quadrado, triângulo e retângulo.", "Encontrar formas em objetos e imagens.",
                   "Encaixar formas nos seus contornos.", "Compor figuras com formas (casa, sol, árvore).", "Contornar formas com o dedo."],
        repertorio="<b>Imagem:</b> Kate Greenaway (1878). <b>Línguas:</b> <i>circle · le cercle · circulus</i>; <i>square · le carré · quadrātum</i>; "
                   "<i>triangle · le triangle · triangulum</i>.",
        materiais="Formas recortadas em papel cartão (as desta unidade); blocos de montar; objetos da casa (prato, livro, guardanapo dobrado).",
        vida="Dobrar guardanapos: um quadrado vira retângulo (ao meio) ou triângulo (na diagonal).",
        etapas=[["Cartões das formas.", "Contornar com o dedo.", "Caça às formas na casa."],
                ["Tabuleiro de encaixe.", "Formas na imagem de Greenaway.", "Separar por forma e por cor."],
                ["Compor uma casa com formas.", "Dobrar o guardanapo.", "Inventar um bicho de formas."]],
        indicadores=["Nomeia o círculo.", "Nomeia mais duas formas.", "Encaixa as quatro formas.", "Acha uma forma num objeto da casa.",
                     "Separa por forma, ignorando a cor.", "Compõe uma figura com três formas."],
        interesse="pinturas de Kandinsky e de Paul Klee são feitas de formas; procure-as em livros de arte (Volume 5).",
        dificil="só o círculo: procurar coisas redondas pela casa."))

    cartoes(L, "As formas", [
        dict(pt="círculo", mot="circulo_vermelho", en="circle", fr="le cercle", la="circulus", dica="Contorne com o dedo: não tem pontas!"),
        dict(pt="quadrado", mot="quadrado_azul", en="square", fr="le carré", la="quadrātum", dica="Quatro lados iguais. Conte as pontas."),
        dict(pt="triângulo", mot="triangulo_amarelo", en="triangle", fr="le triangle", la="triangulum", dica="Três lados, três pontas."),
        dict(pt="retângulo", mot="retangulo_verde", en="rectangle", fr="le rectangle", la=None, dica="Comprido como um livro deitado."),
        dict(pt="sol", mot="sol", en="sun", fr="le soleil", la="sōl", dica="O sol parece um círculo. E a lua cheia?"),
        dict(pt="prato", mot="prato", en="plate", fr="l’assiette (fem.)", la="patella", dica="Que forma tem o nosso prato?"),
        dict(pt="livro", mot="livro", en="book", fr="le livre", la="liber", dica="Retângulo ou quadrado? Meça os lados com as mãos."),
        dict(pt="vela", mot="vela", en="candle", fr="la bougie", la="candēla", dica="De lado, um retângulo; a chama, quase um triângulo."),
        dict(pt="estrela", mot="estrela", en="star", fr="l’étoile (fem.)", la="stēlla", dica="Cinco pontas! Uma forma diferente."),
    ], "Unidade 5 · As formas")

    slots = [("circulo", 52, 70), ("quadrado", 150, 70), ("triangulo", 52, 150), ("retangulo", 150, 150)]
    svg = ""
    for t, cx, cy in slots:
        st = 'fill="none" stroke="var(--sepia)" stroke-width="0.8" stroke-dasharray="2 1.6"'
        if t == "circulo":
            svg += f'<circle cx="{cx}" cy="{cy}" r="24" {st}/>'
        elif t == "quadrado":
            svg += f'<rect x="{cx - 22}" y="{cy - 22}" width="44" height="44" {st}/>'
        elif t == "triangulo":
            svg += f'<path d="M {cx} {cy - 26} L {cx + 26} {cy + 20} L {cx - 26} {cy + 20} Z" {st}/>'
        else:
            svg += f'<rect x="{cx - 34}" y="{cy - 14}" width="68" height="28" {st}/>'
    pecas = "".join(img(m, w, f"display:inline-block;margin:0 2mm;vertical-align:middle") for m, w in
                    (("triangulo_vermelho", "40mm"), ("circulo_azul", "40mm"), ("retangulo_amarelo", "56mm"), ("quadrado_verde", "38mm")))
    c = f"""{cabeca_folha("O tabuleiro de encaixe", "recortar as quatro peças de baixo e encaixar cada uma no seu contorno", 12)}
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>
    <div class="centro" style="position:absolute;left:0;right:0;top:186mm">{pecas}</div>
    {adulto("encaixe e forma",
            "As cores das peças não combinam com nada de propósito: a pista é só a forma. Recorte as peças (cole sobre papelão). <b>Descobrir:</b> contorne "
            "cada peça com o dedo dela. <b>Relacionar:</b> ela encaixa cada peça no contorno certo — o triângulo só cabe no triângulo. <b>Criar:</b> com as peças, "
            "monte uma casa (quadrado e triângulo).",
            estilo="top:236mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    observacao(L, "Formas no jardim", "Kate Greenaway · <i>Under the Window</i> (1878)", pd("greenaway_cha", "134mm"),
               ["Ache coisas <b>redondas</b>: os pratos, as xícaras…", "Ache um <b>retângulo</b>: a mesa, a janela da casa…",
                "Tem algum <b>triângulo</b>? Olhe o telhado.", "E na nossa casa, onde há círculos?"],
               adulto("formas em imagens",
                      "Na pintura, as formas não aparecem sozinhas como nos cartões: estão escondidas nas coisas. A mesa vista de cima seria um retângulo; "
                      "os pratos são círculos vistos de lado (parecem ovais) — se ela disser “oval”, aceite e elogie. Saiam depois numa caça às formas pela casa.",
                      credito_pd("greenaway_cha")),
               aba="--d-artes")

    casa = (img("quadrado_azul", "60mm", "position:absolute;left:40mm;top:96mm") + img("triangulo_vermelho", "70mm", "position:absolute;left:35mm;top:42mm")
            + img("circulo_amarelo", "34mm", "position:absolute;left:146mm;top:46mm") + img("retangulo_verde", "34mm", "position:absolute;left:62mm;top:132mm;transform:rotate(90deg)"))
    c = f"""<div class="miolo">{titulo("Uma casa de formas", "triângulo, quadrado, retângulo e o sol redondo", 26)}</div>{casa}
    <div style="position:absolute;left:112mm;top:96mm;width:80mm;height:84mm" class="caixa"><div class="peq centro" style="margin-top:2mm">a casa da Marina</div></div>
    {adulto("compor com formas",
            "O modelo da esquerda é feito só de formas: telhado triângulo, parede quadrado, porta retângulo, sol círculo. Com as peças do tabuleiro (ou formas novas "
            "recortadas em papel colorido), ela monta e cola a casa dela no quadro da direita. Qualquer composição vale: um bicho, um carro, uma flor.",
            estilo="top:200mm;bottom:auto")}"""
    L.add(c, aba="--d-artes")

    svg = pontilhado("M 40 80 A 26 26 0 1 1 39.9 80") + ponto_inicio(40, 80)
    svg += pontilhado("M 110 54 L 160 54 L 160 104 L 110 104 Z") + ponto_inicio(110, 54)
    svg += pontilhado("M 60 130 L 92 186 L 28 186 Z") + ponto_inicio(60, 130)
    svg += pontilhado("M 108 150 L 180 150 L 180 186 L 108 186 Z") + ponto_inicio(108, 150)
    tracado(L, "Contornar as formas", "com o dedo, depois com o giz", svg, "",
            adulto("contornar",
                   "Começando no círculo verde, ela percorre cada contorno com o dedo, dizendo o nome da forma. Nas pontas, parar e virar: é o que diferencia "
                   "o quadrado do círculo. Com o giz, pode sair da linha à vontade. Este movimento prepara o desenho e, mais tarde, a escrita."),
            aba="--d-memoria")


# ================================================================== U6 PADRÕES

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · Padrões", aba="--d-memoria",
        pergunta="O que vem depois? Descobrir a regra que se repete.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos.",
        objetivos=["Continuar um padrão AB (vermelho, azul, vermelho, azul…).", "Reconhecer padrões de som e de movimento.",
                   "Observar padrões na natureza.", "Criar um padrão próprio (colar de contas).", "Chegar ao padrão AAB e ABC (mais tarde)."],
        repertorio="<b>Observação:</b> girassol, margarida, folhas (motivos da coleção). <b>Música:</b> palma e perna. <b>Línguas:</b> <i>red, blue · rouge, bleu · ruber, caeruleus</i>.",
        materiais="Contas grandes de madeira de duas cores e um cordão grosso; blocos de duas cores; guache.",
        vida="Arrumar a mesa alternando: prato, copo, prato, copo.",
        etapas=[["Palma, perna, palma, perna.", "Ver o padrão das contas.", "Pétalas da margarida."],
                ["O que vem depois?", "Cartões de padrão.", "Padrão de blocos."],
                ["Colar de contas.", "Faixa decorada.", "Inventar um padrão de sons."]],
        indicadores=["Continua um padrão AB com objetos.", "Continua um padrão de palmas.", "Diz o que vem depois em AB.",
                     "Faz um colar alternando duas cores.", "Percebe um padrão numa roupa ou no chão.", "Continua AAB."],
        interesse="procure padrões em azulejos, tecidos, cercas, escadas, no chão da cozinha.",
        dificil="só palma-perna, palma-perna."))

    linhas_padrao = [["conta_vermelho", "conta_azul"] * 3, ["conta_amarelo", "conta_verde"] * 3, ["conta_vermelho", "conta_vermelho", "conta_azul"] * 2]
    blocos = ""
    for k, p in enumerate(linhas_padrao):
        mostra = p[:5]
        blocos += (f'<div class="caixa" style="margin-bottom:6mm;padding:4mm 4mm;display:flex;align-items:center;gap:2mm">'
                   + "".join(img(m, "20mm") for m in mostra)
                   + '<div style="width:20mm;height:20mm;border:0.8pt dashed var(--sepia);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18pt;color:var(--sepia)">?</div></div>')
    soltas = "".join(img(f"conta_{c}", "16mm", "display:inline-block;margin:0 2mm") for c in ("vermelho", "azul", "amarelo", "verde", "vermelho", "azul"))
    c = f"""<div class="miolo">{titulo("O que vem depois?", "continuar o colar", 28)}<div style="margin-top:6mm">{blocos}</div>
      <div class="centro peq" style="margin-top:2mm">contas para recortar e pôr no lugar do “?”</div>
      <div class="centro" style="margin-top:2mm">{soltas}</div></div>
    {adulto("padrão AB e AAB",
            "Leia o colar em voz alta, tocando: “vermelho, azul, vermelho, azul, vermelho…” — e espere: “…azul!”. A voz ajuda a ouvir o padrão. "
            "A terceira fileira é mais difícil (vermelho, vermelho, azul): deixe para quando as duas primeiras estiverem fáceis. "
            "<b>Com contas de verdade:</b> você começa o colar; ela continua.")}"""
    L.add(c, aba="--d-memoria")

    c = f"""<div class="miolo">{titulo("Padrões de som e de corpo", "palma, perna, palma, perna…", 26)}
      <table class="tab" style="font-size:13pt;margin-top:6mm">
        <tr><td style="width:30mm">{img("palma", "18mm", "display:inline-block")}{img("tambor", "18mm", "display:inline-block")}</td><td>palma · perna · palma · perna · <b>?</b></td><td class="peq">AB</td></tr>
        <tr><td>{img("palma", "18mm", "display:inline-block")}{img("sino", "16mm", "display:inline-block")}</td><td>palma · palma · <i>dlém</i> · palma · palma · <i>dlém</i> · <b>?</b></td><td class="peq">AAB</td></tr>
        <tr><td>{img("pegada", "10mm", "display:inline-block")}{img("pegada_esq", "10mm", "display:inline-block")}</td><td>pé · pé · pulo · pé · pé · pulo · <b>?</b></td><td class="peq">AAB</td></tr>
        <tr><td>{img("tambor", "18mm", "display:inline-block")}</td><td>forte · fraco · forte · fraco · <b>?</b></td><td class="peq">AB</td></tr></table></div>
    {adulto("padrão no tempo",
            "Padrões de som e de movimento são os mesmos das contas, mas no tempo: é o ritmo, a base da música. Faça um padrão algumas vezes e pare: ela continua. "
            "Depois ela inventa um padrão e você continua. Se ela mudar a regra no meio, diga “ah, mudou!” — perceber a mudança também é entender o padrão.")}"""
    L.add(c, aba="--d-musica")

    c = f"""<div class="miolo">{titulo("Padrões na natureza", "olhar de perto", 28)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:6mm">
        <div class="centro">{img("girassol", "60mm", "margin:0 auto")}<div class="legenda-q">pétalas em volta, sementes no meio</div></div>
        <div class="centro">{img("margarida", "60mm", "margin:0 auto")}<div class="legenda-q">pétala, pétala, pétala…</div></div>
        <div class="centro">{img("folha", "56mm", "margin:0 auto")}<div class="legenda-q">nervuras dos dois lados</div></div>
        <div class="centro">{img("tartaruga", "60mm", "margin:0 auto")}<div class="legenda-q">o casco de placas</div></div></div></div>
    {adulto("observação",
            "A natureza é cheia de repetições: pétalas iguais em volta da flor, nervuras dos dois lados da folha, placas no casco da tartaruga. "
            "Leve uma lupa ao jardim e procurem padrões de verdade: num abacaxi, numa pinha, numa concha, na casca de uma árvore. "
            "Não é preciso nomear; basta dizer “olha, se repete!”.")}"""
    L.add(c, aba="--d-natureza")

    cartas = []
    pads = [("vermelho", "azul"), ("amarelo", "verde"), ("azul", "amarelo"), ("verde", "vermelho")]
    for a, b in pads:
        seq = "".join(img(f"conta_{c}", "10mm", "display:inline-block;margin:0 .5mm") for c in (a, b, a, b, a))
        cartas.append(f'<div class="carta" style="width:86mm;height:28mm;display:inline-flex;flex-direction:row;margin:1mm">{seq}'
                      f'<span style="display:inline-block;width:10mm;height:10mm;border:0.6pt dashed var(--sepia);border-radius:50%;margin-left:2mm"></span></div>')
    respostas = "".join(img(f"conta_{c}", "14mm", "display:inline-block;margin:0 2mm") for c in ("azul", "verde", "amarelo", "vermelho"))
    c = f"""{cabeca_folha("Cartões de padrão", "recortar as tiras e as contas soltas · ela completa cada tira", 12)}
    <div class="centro" style="position:absolute;left:0;right:0;top:36mm">{''.join(cartas)}</div>
    <div class="centro" style="position:absolute;left:0;right:0;top:110mm">{respostas}</div>
    <div style="position:absolute;left:18mm;right:18mm;top:136mm;height:52mm" class="caixa centro"><div class="peq">a faixa da Marina: pinte ou cole um padrão inventado por ela</div></div>
    {adulto("completar e inventar",
            "Cada tira mostra cinco contas e um lugar vazio. Ela escolhe, entre as contas soltas, a que completa o padrão. Respostas: azul, verde, amarelo, vermelho. "
            "Na faixa de baixo, ela inventa um padrão com carimbos de dedo em duas cores de guache.",
            estilo="top:200mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    passos(L, "O colar da Marina", "um padrão para usar no pescoço",
           [(img("conta_vermelho", "22mm") , "Separar contas de duas cores"),
            (img("conta_azul", "22mm"), "Dar um nó grande na ponta do cordão"),
            (img("conta_vermelho", "16mm", "display:inline-block") + img("conta_azul", "16mm", "display:inline-block"), "Uma vermelha, uma azul…"),
            (img("conta_vermelho", "12mm", "display:inline-block") + img("conta_azul", "12mm", "display:inline-block") + img("conta_vermelho", "12mm", "display:inline-block"), "…e o que vem depois?"),
            (img("caixa", "26mm"), "O adulto amarra as pontas"),
            (img("estrela", "24mm"), "Usar o colar e mostrar o padrão a alguém")],
           adulto("vida prática e padrão",
                  "Enfiar contas é ótimo para a coordenação fina. Use contas grandes (mais de 3 cm) e um cordão com a ponta endurecida com fita adesiva. "
                  "Fique ao lado o tempo todo. O padrão é dela: se ela quiser vermelho, vermelho, azul, ótimo — pergunte só qual é a regra."),
           aba="--d-vida")

    c = f"""<div class="miolo">{titulo("Padrão nos azulejos", "continuar pintando", 28)}
      <table style="margin:8mm auto;border-collapse:collapse">{''.join('<tr>' + ''.join(f'<td style="width:22mm;height:22mm;border:0.6pt solid var(--linha);background:{("#c0716b" if (i + j) % 2 == 0 else "#ffffff") if (i < 2 or j < 2) else "transparent"}"></td>' for j in range(7)) + '</tr>' for i in range(6))}</table></div>
    {adulto("padrão no plano",
            "Como um tabuleiro de xadrez: as duas primeiras linhas e colunas mostram o padrão (pintado, branco, pintado…). Ela continua pintando os quadrados "
            "com giz ou guache, ou cobrindo-os com papel colorido picado. É difícil: muitas crianças só conseguem por volta dos 4 anos. Fique com a fileira de cima, se for o caso.")}"""
    L.add(c, aba="--d-artes")


# ================================================================== U7 ONDE ESTÁ

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · Onde está?", aba="--d-natureza",
        pergunta="Dentro, fora, em cima, embaixo, atrás, na frente, perto, longe — as palavras do espaço.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos, com muito movimento.",
        objetivos=["Compreender e usar dentro, fora, em cima, embaixo, ao lado, atrás, na frente.", "Seguir uma ordem com duas palavras de lugar.",
                   "Distinguir perto e longe.", "Desenhar um mapa simples do quarto (com ajuda).", "Retomar <i>O Coelho Pedro</i> como mapa de esconderijos."],
        repertorio="<b>Imagens:</b> Beatrix Potter (1902) e Randolph Caldecott (1880). <b>Línguas:</b> <i>in, on, under · dans, sur, sous · in, super, sub</i>.",
        materiais="Uma caixa de sapato; o ratinho de pelúcia; uma cadeira; uma cesta; papel grande para o mapa.",
        vida="Guardar: “os sapatos vão <i>embaixo</i> da cama; o livro vai <i>em cima</i> da mesa; o urso vai <i>dentro</i> da cesta”.",
        etapas=[["Pedro na horta: onde ele está?", "O ratinho e a caixa.", "Esconde-esconde de objetos."],
                ["Ordens de lugar.", "Perto e longe na imagem.", "Cartões: dentro ou fora?"],
                ["Ela dá as ordens ao adulto.", "Mapa do quarto.", "Esconder o ratinho e dar pistas."]],
        indicadores=["Põe um objeto dentro, em cima e embaixo, quando pedido.", "Diz onde algo está usando uma palavra de lugar.",
                     "Entende atrás e na frente.", "Segue uma ordem com duas partes.", "Diz o que está perto e o que está longe.", "Encontra um objeto escondido com pistas."],
        interesse="esconde-esconde com pistas: “está embaixo de algo macio” (o travesseiro).",
        dificil="só dentro e fora com a caixa e o ratinho."))

    figs = [("dentro", "potter_regador", "Pedro está <b>dentro</b> do regador."), ("embaixo", "potter_pedro_porteira", "Pedro passa por <b>baixo</b> da porteira."),
            ("em cima", "potter_portao", "Pedro olha de <b>cima</b> do carrinho."), ("atrás", "potter_rato_ervilha", "A ratinha está <b>atrás</b> da porta.")]
    cel = "".join(f'<div class="estacao">{pd(n, "62mm", "max-height:66mm;object-fit:contain")}<div style="font-size:13pt;margin-top:1mm">{t}</div></div>' for _, n, t in figs)
    c = f"""<div class="miolo">{titulo("Onde está o Pedro?", "Beatrix Potter · <i>The Tale of Peter Rabbit</i> (1902)", 26)}<div class="grade4">{cel}</div></div>
    {adulto("palavras de lugar",
            "Retome <i>O Coelho Pedro</i> (Volume 2). Para cada imagem, pergunte “onde está o Pedro?” e espere que ela use a palavra de lugar. "
            "Na quarta imagem, a ratinha (com uma ervilha na boca) está junto da porta, e o Pedro atrás dela: aceite “perto” e “do lado”.",
            credito_pd("potter_regador", "potter_pedro_porteira", "potter_portao", "potter_rato_ervilha"))}"""
    L.add(c, aba="--d-natureza")

    pos = [("dentro", "left:16mm;top:7mm;width:18mm", 1), ("fora", "left:-6mm;top:22mm;width:16mm", 0), ("em cima", "left:14mm;top:-12mm;width:18mm", 0),
           ("ao lado", "left:44mm;top:16mm;width:16mm", 0)]
    cel = ""
    for k, (nome, st, dentro) in enumerate(pos):
        x, y = 22 + (k % 2) * 90, 52 + (k // 2) * 76
        z_caixa, z_rato = (2, 1) if dentro else (1, 2)
        cel += (f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:80mm;height:68mm" class="caixa">'
                f'<div style="position:absolute;left:14mm;top:16mm;width:50mm;height:46mm">'
                f'{img("caixa", "50mm", f"position:absolute;left:0;top:0;z-index:{z_caixa}")}'
                f'{img("ratinho", "18mm", f"position:absolute;{st};z-index:{z_rato}")}</div>'
                f'<div style="position:absolute;bottom:2mm;left:0;right:0;text-align:center;font-size:14pt;font-weight:600">{nome}</div></div>')
    c = f"""<div class="miolo">{titulo("O ratinho e a caixa", "onde está o ratinho?", 26)}</div>{cel}
    {adulto("brincar de lugar",
            "Com uma caixa de sapato e o ratinho de pelúcia, repitam as quatro posições e acrescentem outras: embaixo (caixa por cima), atrás, na frente. "
            "<b>Relacionar:</b> você diz, ela faz. <b>Criar:</b> ela põe o ratinho e você diz onde ele está — erre às vezes, para ela corrigir. "
            "No quadro “dentro”, só a cabeça do ratinho aparece por cima da borda.",
            estilo="top:212mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    ordens = ["Ponha o urso <b>em cima</b> da cadeira.", "Esconda a bola <b>embaixo</b> da almofada.", "Fique <b>atrás</b> da porta.",
              "Ponha o livro <b>dentro</b> da cesta.", "Sente-se <b>ao lado</b> do papai.", "Fique <b>na frente</b> do espelho.",
              "Ponha a colher <b>dentro</b> da xícara e a xícara <b>em cima</b> da mesa.", "Leve o ratinho para <b>perto</b> da janela."]
    cel = "".join(f'<div class="carta" style="width:86mm;height:28mm;display:inline-flex;margin:1mm;padding:0 6mm;font-size:13pt;text-align:center">{o}</div>' for o in ordens)
    c = f"""{cabeca_folha("Cartões de ordens", "recortar · o adulto lê, a Marina faz (e depois trocam)", 12)}
    <div class="centro" style="position:absolute;left:0;right:0;top:34mm">{cel}</div>
    {adulto("seguir ordens",
            "Embaralhe os cartões; tire um, leia em voz alta, e ela faz. A penúltima ordem tem duas partes — é mais difícil; guarde-a para quando as outras estiverem fáceis. "
            "Depois troquem: ela “lê” (inventa) uma ordem para você. Errar de propósito (pôr o urso embaixo em vez de em cima) faz rir e ensina.",
            estilo="top:166mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    observacao(L, "Perto e longe", "Randolph Caldecott · <i>R. Caldecott’s Picture Book</i> (1880)", pd("caldecott_vaca", "104mm"),
               ["O que está <b>perto</b> de nós? (a vaca grande, as plantinhas)", "O que está <b>longe</b>? (a casa, os morros)",
                "Por que as vacas lá de trás parecem pequenas?", "O gato está mais perto da vaca ou da casa?"],
               adulto("perspectiva",
                      "O que está longe parece pequeno: é a ideia mais difícil desta página, e não precisa ser explicada. Experimente na janela: “aquele carro lá longe "
                      "parece pequenininho; e aqui perto?”. Depois, brinquem de andar para longe e voltar para perto, acenando.",
                      credito_pd("caldecott_vaca")),
               aba="--d-artes")

    c = f"""<div class="miolo">{titulo("O mapa do meu quarto", "visto de cima, como um passarinho", 26)}
      <div class="caixa" style="height:150mm;margin-top:6mm;position:relative">
        <div class="peq" style="position:absolute;left:3mm;top:2mm">porta</div>
        <div style="position:absolute;left:0;top:10mm;width:2mm;height:24mm;background:var(--sepia-claro)"></div></div></div>
    {adulto("primeiro mapa",
            "Desenhe você o contorno do quarto e a porta (já marcada). Depois pergunte: “onde fica a cama?” — e desenhe um retângulo onde ela mostrar. "
            "Faça o mesmo com o armário, a janela, o tapete. Por fim, esconda o ratinho no quarto e marque um X no mapa: ela usa o mapa para encontrá-lo. "
            "É a mesma ideia do caminho do Pedro (Volume 2), agora com o espaço dela.")}"""
    L.add(c, aba="--d-matematica")

    passos(L, "Esconde-esconde com pistas", "achar pelo lugar",
           [(img("ratinho", "26mm"), "O adulto esconde o ratinho"),
            (img("caixa", "26mm"), "Pista 1: está dentro de alguma coisa"),
            (img("mesa", "28mm"), "Pista 2: perto da mesa"),
            (img("cesta", "28mm"), "Pista 3: embaixo de algo leve"),
            (img("estrela", "22mm"), "Achou!"),
            (img("palma", "22mm"), "Agora é ela quem esconde e dá as pistas")],
           adulto("raciocínio espacial",
                  "As pistas vão do geral ao específico. No começo, uma pista basta (“está embaixo da almofada”). Quando ela for a que esconde, ajude-a a "
                  "dizer as pistas com palavras de lugar."),
           aba="--d-vida")


# ================================================================== U8 MEDIR E ORDENAR

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · Medir e ordenar", aba="--d-matematica",
        pergunta="Quanto mede? Quanto cabe? Quanto pesa? — medir com o corpo e com as coisas.",
        duracao="Dois fins de semana · dois encontros · 20 minutos.",
        objetivos=["Medir comprimentos com a mão e com o pé (medidas do corpo).", "Comparar cheio e vazio, pesado e leve.",
                   "Ordenar do menor ao maior.", "Contar unidades de medida (quantas mãos?).", "Usar mais, menos, igual."],
        repertorio="<b>História do medir:</b> o palmo, o pé e o passo eram medidas usadas por todos os povos antes do metro. "
                   "<b>Línguas:</b> <i>hand, foot · la main, le pied · manus, pēs</i>.",
        materiais="Um cabide e dois saquinhos (balança caseira); copos e uma jarra; fita métrica de costura; os cartões da unidade.",
        vida="Encher e esvaziar na pia: meio copo, copo cheio, vazio.",
        etapas=[["Medir a mesa em mãos.", "Cheio e vazio.", "Pesado e leve, segurando."],
                ["Quantos pés até a porta?", "Balança de cabide.", "Ordenar do menor ao maior."],
                ["Medir o papai em mãos da Marina.", "Prever: qual pesa mais?", "Medir com o próprio passo a casa toda."]],
        indicadores=["Coloca a mão uma depois da outra, sem espaço.", "Conta as mãos com ajuda.", "Diz cheio, vazio, metade.",
                     "Diz qual é mais pesado segurando os dois.", "Lê a balança de cabide (o lado que desce).", "Ordena três ou mais por tamanho."],
        interesse="cozinhem juntas com medidas: uma xícara de farinha, duas colheres de açúcar.",
        dificil="só cheio e vazio na pia."))

    linhas = "".join(f'<tr><td style="width:62mm;font-size:13pt">{o}</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>'
                     for o in ("a mesa da cozinha", "a cama da Marina", "a porta", "o papai deitado", "o ratinho de pelúcia"))
    c = f"""<div class="miolo">{titulo("Medir com as mãos", "quantos palmos?", 28)}
      <div class="centro" style="margin:5mm 0">{"".join(img("palma", "26mm", "display:inline-block;margin:0 -2mm") for _ in range(5))}</div>
      <table class="tab" style="margin-top:4mm"><tr><th>o que medimos</th><th>quantas mãos da Marina? (e quantas do adulto?)</th></tr>{linhas}</table></div>
    {adulto("medida não padronizada",
            "Mostre como pôr uma mão depois da outra, sem deixar espaço e sem sobrepor; conte cada mão. Depois meça a mesma coisa com a sua mão: dá menos mãos! "
            "“Por quê?” — porque a mão do adulto é maior. Essa é a razão de existirem o metro e a régua: todo mundo medir igual. "
            "Escreva os números que ela contar.")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Quantos pés até a porta?", "medir com os pés e com os passos", 26)}
      <div class="centro" style="margin:8mm 0">{"".join(img("pegada" if k % 2 else "pegada_esq", "14mm", "display:inline-block;margin:0 1mm;transform:rotate(90deg)") for k in range(8))}</div>
      <table class="tab" style="font-size:12pt"><tr><th>de onde até onde</th><th>pés (um encostado no outro)</th><th>passos</th></tr>
        <tr><td style="height:14mm">da cama até a porta</td><td></td><td></td></tr><tr><td style="height:14mm">do sofá até a janela</td><td></td><td></td></tr>
        <tr><td style="height:14mm">de um lado do tapete ao outro</td><td></td><td></td></tr></table></div>
    {adulto("medir com o corpo",
            "Pé ante pé (o calcanhar encostado na ponta do outro pé) é uma medida pequena; o passo é uma medida maior. A mesma distância dá mais pés do que passos. "
            "Em muitas línguas, “pé” ainda é nome de medida: em inglês, <i>foot</i>; os romanos mediam em <i>pedēs</i> e em <i>passūs</i> (mil passos = uma milha).")}"""
    L.add(c, aba="--d-matematica")

    copos = ""
    for k, (frac, nome) in enumerate(((0, "vazio"), (0.5, "metade"), (1, "cheio"))):
        h = 50 * frac
        copos += (f'<div style="display:inline-block;margin:0 8mm;text-align:center;vertical-align:bottom">'
                  f'<svg viewBox="0 0 40 60" style="width:30mm;height:45mm"><rect x="{6}" y="{58 - h}" width="28" height="{h}" fill="#a7c2d8"/>'
                  f'<path d="M 4 4 L 6 58 L 34 58 L 36 4" fill="none" stroke="var(--sepia)" stroke-width="1"/></svg>'
                  f'<div style="font-size:14pt">{nome}</div></div>')
    c = f"""<div class="miolo">{titulo("Cheio, vazio e pesado, leve", "encher, esvaziar, segurar", 26)}
      <div class="centro" style="margin-top:6mm">{copos}</div>
      <div style="display:flex;justify-content:center;gap:16mm;align-items:center;margin-top:10mm">
        <div class="centro">{img("pedra", "36mm")}<div style="font-size:13pt">pesado</div></div>
        <svg viewBox="0 0 80 50" style="width:60mm;height:38mm"><path d="M 40 4 L 40 10 M 6 22 L 74 10" stroke="var(--sepia)" stroke-width="1.4" fill="none"/>
          <path d="M 6 22 L 6 34 M 74 10 L 74 22" stroke="var(--sepia)" stroke-width=".6"/><rect x="0" y="34" width="12" height="10" fill="#9a948a"/>
          <rect x="68" y="22" width="12" height="10" fill="#c9d6e0"/><circle cx="40" cy="4" r="2" fill="none" stroke="var(--sepia)"/></svg>
        <div class="centro">{img("pena", "36mm")}<div style="font-size:13pt">leve</div></div></div></div>
    {adulto("capacidade e peso",
            "<b>Cheio e vazio:</b> na pia, com um copo transparente: encher, esvaziar, encher até a metade (marque a metade com fita). "
            "<b>Pesado e leve:</b> ela segura um objeto em cada mão e diz qual pesa mais. <b>Balança de cabide:</b> pendure dois saquinhos nas pontas de um cabide; "
            "o lado mais pesado desce, como no desenho. Antes de pôr, ela adivinha. Uma pedrinha ou uma pena? Uma maçã ou um morango?")}"""
    L.add(c, aba="--d-matematica")

    tam = [(14, "estrela"), (22, "estrela"), (30, "estrela"), (38, "estrela"), (46, "estrela")]
    ordem = [2, 4, 0, 3, 1]
    cel = "".join(f'<td style="vertical-align:bottom;text-align:center"><div class="carta" style="display:inline-flex;width:{tam[i][0] + 4}mm;height:{tam[i][0] + 4}mm">{img(tam[i][1], f"{tam[i][0]}mm")}</div></td>' for i in ordem)
    c = f"""{cabeca_folha("Do menor ao maior", "recortar as cinco estrelas e pôr em fila", 12)}
    <table style="position:absolute;left:16mm;top:40mm;width:178mm"><tr>{cel}</tr></table>
    <div style="position:absolute;left:16mm;right:16mm;top:110mm;height:60mm" class="caixa centro"><div class="peq">a fila da Marina: da menor à maior</div></div>
    {adulto("ordenar cinco",
            "As estrelas estão misturadas. Ela as põe em fila, da menor para a maior, no quadro. Se ficar difícil, tire duas e ordene três. "
            "Depois, ao contrário: da maior para a menor. Para conferir, ponha uma estrela sobre a seguinte — a menor sempre cabe dentro da maior.",
            estilo="top:186mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    passos(L, "Cozinhar com medidas", "um bolinho de caneca",
           [(img("tigela", "28mm"), "Uma tigela grande"),
            (img("colher", "24mm"), "Contar colheres de farinha: uma, duas, três"),
            (img("xicara", "26mm"), "Uma xícara de leite: cheia, sem derramar"),
            (img("colher", "22mm", "transform:rotate(40deg)"), "Mexer: dez voltas, contando"),
            (img("vela", "24mm"), "O adulto leva ao forno"),
            (img("prato", "30mm"), "Repartir: um pedaço para cada um")],
           adulto("matemática na cozinha",
                  "Escolha uma receita simples que vocês já fazem e deixe que ela conte as colheres, encha a xícara e conte as voltas da colher. "
                  "O forno e o fogão são sempre do adulto. Medir na cozinha junta tudo deste volume: contar, um para cada, cheio e vazio, ordem."),
           aba="--d-vida")

    c = f"""<div class="miolo">{titulo("Mais, menos ou igual?", "comparar duas pilhas", 26)}
      <div style="display:flex;justify-content:space-around;margin-top:10mm">
        <div class="centro"><div style="display:flex;flex-direction:column-reverse;align-items:center">{"".join(img("conta_vermelho", "16mm", "margin-top:-2mm") for _ in range(4))}</div><div style="font-size:13pt">mais</div></div>
        <div class="centro"><div style="display:flex;flex-direction:column-reverse;align-items:center">{"".join(img("conta_azul", "16mm", "margin-top:-2mm") for _ in range(2))}</div><div style="font-size:13pt">menos</div></div>
        <div class="centro"><div style="display:flex;gap:4mm"><div style="display:flex;flex-direction:column-reverse">{"".join(img("conta_amarelo", "16mm", "margin-top:-2mm") for _ in range(3))}</div>
        <div style="display:flex;flex-direction:column-reverse">{"".join(img("conta_verde", "16mm", "margin-top:-2mm") for _ in range(3))}</div></div><div style="font-size:13pt">igual</div></div></div></div>
    {adulto("comparar quantidades",
            "Com blocos ou botões, faça duas pilhas e pergunte: “qual tem mais?”. Em pilhas, a resposta se vê pela altura — sem contar. Depois, contem para conferir. "
            "<b>Igual:</b> duas pilhas da mesma altura. <b>Criar:</b> “faça uma pilha igual à minha”; “faça uma com mais”. "
            "Mais e menos são as palavras que, mais tarde, vão dar sentido a somar e tirar.")}"""
    L.add(c, aba="--d-matematica")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo
    c = f"""<div class="miolo">{titulo("Meus números", "o que eu já sei contar", 28)}
      <table class="tab" style="font-size:12pt;margin-top:4mm">
        <tr><td style="width:66mm">Eu tenho … anos.</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Na minha casa moram … pessoas.</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Minha forma preferida:</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Eu sei contar até:</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr></table>
      <div class="caixa" style="height:140mm;margin-top:6mm"><div class="peq centro" style="margin-top:2mm">a mão dela carimbada com guache, e quantos dedos tem</div></div></div>"""
    L.add(c, aba="--d-artes")

    for metade, unidades in enumerate((UNIDADES[:4], UNIDADES[4:])):
        linhas = "".join(f'<tr><td style="width:44mm"><b>{n.split(" · ", 1)[1]}</b><div class="peq">{n.split(" · ")[0]}</div></td>'
                         f'<td style="height:50mm"></td></tr>' for n, _ in unidades)
        c = f"""<div class="miolo">{titulo("Diário de observação", "para o adulto · contagens, comparações e descobertas — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Unidade</th><th>O que ela contou, comparou ou descobriu (com data)</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    import fontes_v1
    usados = ["crane_porco", "crane_porcos", "brooke_cadeiras", "greenaway_gansos", "greenaway_cha", "caldecott_vaca", "cartao_galo",
              "potter_regador", "potter_pedro_porteira", "potter_portao", "potter_rato_ervilha"]
    por_livro = {}
    for n, (item, pg, *_r) in fontes_v1.ITENS.items():
        if any(n.startswith(u) for u in usados):
            por_livro.setdefault(item, set()).add(pg)
    cred = "".join(f"<li>{fontes_v1.LIVROS[i]} — Internet Archive, <i>{i}</i>, páginas {', '.join('n' + str(p) for p in sorted(ps))}.</li>" for i, ps in por_livro.items())
    c = f"""<div class="miolo texto">{titulo("Repertório e créditos", "Volume 3", 26)}
      <h2>Rimas e histórias</h2><p style="font-size:9.6pt">Parlendas e cantigas tradicionais: <i>Um, dois, feijão com arroz</i>, <i>A galinha do vizinho</i>, <i>Marcha, soldado</i>.
      Tradução da coleção: <i>This little pig went to market</i> (rima inglesa tradicional). Textos originais da coleção: <i>A mesa dos porquinhos</i>, <i>Os três lobos</i>.</p>
      <h2>Fundamentos</h2><p style="font-size:9.6pt">As barras de comprimento, o tabuleiro de encaixe e o saco de formas inspiram-se nos materiais de Maria Montessori
      (barras vermelhas, encaixes geométricos); os padrões e a correspondência, na tradição da educação matemática infantil. Nenhum material reproduz produtos comerciais.</p>
      <h2>Ilustrações em domínio público</h2><p style="font-size:9pt">Digitalizações do Internet Archive, com recorte e ajuste do tom do papel; nenhuma pintura foi retocada.
      Nas gravuras de Walter Crane, os títulos em inglês impressos nas pranchas foram recortados.</p>
      <ul style="font-size:8.6pt;line-height:1.35">{cred}</ul>
      <p style="font-size:9pt">Formas, contas, barras e demais motivos: aquarela digital procedural da coleção. Tipografia: EB Garamond (licença OFL).</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 3</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">o pulso, o forte e o fraco, o rápido e o lento,<br>os instrumentos da orquestra,<br>
      e Vivaldi, Bach, Mozart, Saint-Saëns e Debussy.</p>
      <div style="margin-top:12mm">{img("sino", "34mm", "margin:0 auto")}</div>
      <p class="peq" style="margin-top:8mm">Volume 4 · O mundo da música</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

def montar():
    L = Livro(3, "Números, formas e raciocínio")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8):
        u(L)
    encerramento(L)
    num, _ = L.paginas[n_sum - 1]
    L.paginas[n_sum - 1] = (num, f'<section class="pagina"><div class="moldura"></div>{sumario(INICIO)}'
                                 f'<div class="rodape"><span class="num">{num}</span></div></section>')
    return L


def main():
    os.makedirs(SAIDA, exist_ok=True)
    ok = True
    for versao, nome in (("impressao", "volume3-impressao"), ("tela", "volume3-tela")):
        VERSAO["atual"] = versao
        L = montar()
        h = os.path.join(AQUI, f"{nome}.html")
        open(h, "w", encoding="utf-8").write(L.html())
        ok &= gerar_pdf(h, os.path.join(SAIDA, f"{nome}.pdf"))
        print(versao, len(L.paginas), "páginas")
    insp = os.path.join(SAIDA, "inspecao")
    os.makedirs(insp, exist_ok=True)
    for f in os.listdir(insp):
        os.remove(os.path.join(insp, f))
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume3-tela.pdf"), os.path.join(insp, "p")], check=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
