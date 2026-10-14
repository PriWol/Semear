"""
VOLUME 1 — O MUNDO AO MEU REDOR
Gera volume1/volume1-impressao.pdf e volume1/volume1-tela.pdf e as páginas de inspeção.
uso: python3 volume1.py
"""
import math
import os
import subprocess
import sys

from livro import (Livro, VERSAO, adulto, arte, cabeca_folha, cartoes, credito_pd, gerar_pdf, guia, historia,
                   img, lista, marcas_corte, memoria, observacao, passos, pd, poema, ponto_inicio, pontilhado,
                   rodape_folha, sequencia, texto, titulo, tracado)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume1")

UNIDADES = [
    ("Abertura", None),
    ("Unidade 1 · Eu e meus sentidos", "--d-memoria"),
    ("Unidade 2 · Minha casa e meus objetos", "--d-vida"),
    ("Unidade 3 · O jardim e o pomar", "--d-natureza"),
    ("Unidade 4 · Os animais da fazenda e do bosque", "--d-historias"),
    ("Unidade 5 · O céu: sol, lua, nuvens e chuva", "--d-ingles"),
    ("Unidade 6 · Água, lago e patos", "--d-matematica"),
    ("Unidade 7 · As estações", "--d-artes"),
    ("Encerramento", None),
]
INICIO = {}   # unidade -> primeira página (preenchido na montagem)


# ================================================================== ABERTURA

def capa(L):
    cx, cy, rx, ry = 105, 168, 74, 82
    itens = ["maca", "folha", "margarida", "pera", "raminho", "morango", "tulipa", "uva", "folha",
             "laranja", "florzinha_azul", "cereja", "girassol", "bolota", "raminho", "jabuticaba",
             "florzinha_rosa", "banana"]
    h = []
    for i, nome in enumerate(itens):
        t = -math.pi / 2 + 2 * math.pi * i / len(itens)
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        w = 33 if nome not in ("raminho", "jabuticaba") else 46
        rot = math.degrees(t) + 90 if nome in ("raminho", "folha") else (i % 3 - 1) * 9
        h.append(f'<img class="aq" src="{arte(nome)}" style="position:absolute;width:{w}mm;'
                 f'left:{x - w / 2:.1f}mm;top:{y - w / 2:.1f}mm;transform:rotate({rot:.0f}deg)">')
    h.append(f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div>
    </div>
    <div style="position:absolute;top:{cy - 30}mm;left:{cx - 42}mm;width:84mm;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 1</div>
      <div style="font-weight:500;font-size:26pt;line-height:1.05;margin:2mm 0">O mundo<br>ao meu redor</div>
      <div class="vinheta-sep">❦</div>
      <div style="font-size:10.5pt;font-style:italic;color:var(--sepia);line-height:1.4">sentidos · casa · jardim e pomar<br>animais · céu · água · estações</div>
    </div>
    {img('ratinho', '26mm', f'position:absolute;left:{cx - 13}mm;top:{cy + 34}mm')}
    <div style="position:absolute;bottom:20mm;left:0;right:0;text-align:center;font-size:10pt;color:var(--sepia);font-style:italic">
      “Grandes coisas começam com pequenos olhares atentos.”</div>""")
    L.add("".join(h), cabecalho=False, numero=False)


def rosto(L):
    c = f"""
    <div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 1</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O mundo ao meu redor</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">Este livro é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:16mm auto 0;width:96mm;height:72mm" class="caixa">
        <div class="peq" style="margin-top:30mm">cole aqui uma foto ou um desenho dela</div></div>
      <div style="margin-top:8mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div>
    </div>
    {img('ratinho', '28mm', 'position:absolute;right:26mm;bottom:28mm')}"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Antes de começar</h1>
      <p>Este volume foi feito para os fins de semana da Marina, como um tempo bom em família: ele não substitui a escola
      nem corre na frente dela. O que pedimos é pouco e precioso — vinte minutos de atenção inteira, algumas vezes por semana,
      com objetos de verdade, livros bonitos e música boa.</p>
      <p>A ideia que atravessa a coleção é simples: <b>respeitar a infância sem subestimar a inteligência da criança</b>.
      Por isso não há provas, notas nem folhas repetidas. Há histórias para contar e recontar, coisas para cheirar e separar,
      cartões para nomear, jogos que crescem com ela, obras de arte e música para escutar com o corpo.</p>
      <h2>Três gestos que se repetem</h2>
      <ul>
        <li><b>Descobrir</b> — olhar, escutar, tocar e ganhar palavras para o que se encontra.</li>
        <li><b>Relacionar</b> — comparar, separar, pôr em ordem, lembrar.</li>
        <li><b>Criar</b> — recontar, imaginar, inventar uma variação, resolver um pequeno problema.</li>
      </ul>
      <p>Os três estão em todas as unidades, desde já. Observe onde a Marina está e ofereça o próximo passo; se ela não quiser,
      volte um passo. Uma atividade que termina com vontade de repetir valeu mais do que três que terminam em cansaço.</p>
      <h2>De onde vêm as imagens</h2>
      <p>As aquarelas das histórias e das cenas são de grandes ilustradores ingleses — Beatrix Potter, Kate Greenaway,
      Randolph Caldecott —, em edições originais que já são de domínio público. Os motivos dos cartões e dos jogos foram pintados
      para esta coleção. Cada ilustração antiga traz o seu crédito.</p>
      <p style="margin-top:6mm;font-style:italic;text-align:right">Com carinho, para a Marina e para quem lê com ela.</p>
    """)


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Um fim de semana, uma unidade em pedaços</h1>
      <p>Cada unidade abre com um <b>guia do adulto</b>: objetivos, repertório, materiais, o que fazer em cada um dos três
      níveis e os sinais que vale observar. Depois vêm as páginas da criança. Instruções para o adulto ficam sempre numa faixa
      separada, no pé da página, atrás de um filete.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Dois encontros por fim de semana, de 15 a 25 minutos, em blocos de 5 a 10 minutos (uma história,
        um objeto, um jogo, uma música). Cada unidade dura de dois a três fins de semana.</td></tr>
        <tr><th>Repetição</th><td>Repetir a mesma história e a mesma música é o método. Aos 2 anos, a décima vez é quando ela
        começa a antecipar, completar e corrigir você.</td></tr>
        <tr><th>Idiomas</th><td>No máximo três palavras novas por semana, sempre ditas junto do objeto real ou da imagem. O verso
        dos cartões traz inglês, francês e latim; use só o que fizer sentido para vocês.</td></tr>
        <tr><th>Abas coloridas</th><td>A cor na borda da página indica o domínio principal: <span style="color:var(--d-historias)">■</span> histórias
        · <span style="color:var(--d-memoria)">■</span> memória e traçado · <span style="color:var(--d-natureza)">■</span> natureza
        · <span style="color:var(--d-musica)">■</span> música · <span style="color:var(--d-vida)">■</span> vida prática
        · <span style="color:var(--d-matematica)">■</span> número e experiência · <span style="color:var(--d-artes)">■</span> arte e observação.</td></tr>
      </table>
      <h2>Impressão</h2>
      <ul>
        <li>Páginas de leitura: papel creme, marfim ou pólen, 90 a 120 g. O arquivo <i>impressão</i> tem fundo branco de propósito:
        o tom creme vem do papel, sem gastar tinta.</li>
        <li>Cartões e jogos: papel de 180 a 240 g, frente e verso, virando pela <b>borda longa</b>. Os versos já vêm espelhados.</li>
        <li>Nada importante fica a menos de 9 mm da borda; a impressora doméstica pode cortar a margem sem perder conteúdo.</li>
        <li>Para durar, plastifique os cartões ou cole-os em papelão. Guarde cada jogo num envelope com o nome.</li>
      </ul>
      <h2>Segurança</h2>
      <p>Peças pequenas, frutas com caroço e potinhos com grãos são sempre usados com o adulto ao lado. Os avisos específicos
      aparecem nos guias das unidades.</p>
      {img('cesta', '40mm', 'margin:3mm auto 0')}
    """)


def sumario(L, inicio):
    linhas = []
    for nome, cor in UNIDADES[1:-1]:
        p = inicio.get(nome, "")
        num, tit = nome.split(" · ", 1)
        linhas.append(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{num}</td>'
                      f'<td style="font-size:13pt">{tit}</td><td class="pg">{p}</td></tr>')
    linhas.append(f'<tr><td></td><td style="font-size:13pt">Encerramento · Meu livro do mundo, diário de observação e repertório</td>'
                  f'<td class="pg">{inicio.get("Encerramento", "")}</td></tr>')
    c = f"""<div class="miolo">
      {titulo("Sumário", "Volume 1 · O mundo ao meu redor", 30)}
      <table class="sumario">{''.join(linhas)}</table>
      <div class="centro" style="margin-top:10mm">
        {img('sol', '22mm', 'display:inline-block;margin:0 3mm')}{img('maca', '22mm', 'display:inline-block;margin:0 3mm')}
        {img('ratinho', '24mm', 'display:inline-block;margin:0 3mm')}{img('gota', '12mm', 'display:inline-block;margin:0 3mm')}
        {img('arvore_primavera', '22mm', 'display:inline-block;margin:0 3mm')}</div>
    </div>"""
    return c


# ================================================================== UNIDADE 1

def unidade1(L):
    L.unidade = "Unidade 1 · Eu e meus sentidos"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 1 · Eu e meus sentidos", aba="--d-memoria",
        pergunta="Como eu conheço o mundo? Olhando, escutando, cheirando, provando e tocando.",
        duracao="Dois fins de semana · dois encontros por fim de semana · 15 a 20 minutos. Comece pelo que ela já ama: o som de um sino, o cheiro de uma fruta.",
        objetivos=["Nomear olhos, ouvidos, nariz, boca e mãos e o que cada um faz.",
                   "Prestar atenção a uma só qualidade por vez (um som, um cheiro, uma textura).",
                   "Parear sons iguais na caixa de sons.",
                   "Ampliar vocabulário sensorial: macio, áspero, doce, azedo, alto, baixinho.",
                   "Traço circular amplo (as bolhas)."],
        repertorio="<b>Poema:</b> <i>As cinco janelinhas</i> (texto da coleção, p. seguinte). <b>Imagem:</b> Kate Greenaway, <i>Under the Window</i> (1878). "
                   "<b>Música:</b> Saint-Saëns, <i>O Aquário</i> (<i>O Carnaval dos Animais</i>, 1886). <b>Línguas:</b> <i>eyes · les yeux · oculī</i>.",
        materiais="Sino pequeno, pena, mel, sabonete, uma flor perfumada, lupa; 6 potinhos opacos iguais com tampa; arroz, feijão e sal grosso; fita adesiva; giz de cera grosso.",
        vida="Lavar as mãos com a sequência ilustrada; secar com a própria toalha; pendurar a toalha no gancho baixo.",
        etapas=[["Brincar de “o que é?” de olhos fechados.", "Cartões: tocar a pena, balançar o sino.", "Ouvir <i>O Aquário</i> no colo."],
                ["Achar os pares da caixa de sons.", "“Qual é mais macio?” — pena ou pedra.", "Procurar na casa coisas que fazem som."],
                ["Dizer o poema com gestos.", "Inventar um som para a chuva.", "Bolhas de sabão e o traço circular."]],
        indicadores=["Aponta a parte do corpo quando o adulto diz o sentido.", "Fica atenta a um som baixinho por alguns segundos.",
                     "Encontra pelo menos um par na caixa de sons.", "Usa espontaneamente uma palavra nova (macio, cheiroso…).",
                     "Faz movimentos circulares contínuos com o giz.", "Lava as mãos seguindo dois ou três passos sozinha."],
        interesse="cozinhe algo com cheiro marcante (canela, laranja) e descreva junto; caminhe descalça na grama e na areia.",
        dificil="só o poema com gestos e o sino.",
        alerta="<b>Segurança.</b> Os potinhos da caixa de sons precisam estar bem fechados com fita; grãos e sal grosso só com o adulto ao lado. "
               "Mel não deve ser oferecido a bebês com menos de 1 ano (a Marina já pode provar)."))

    poema(L, "As cinco janelinhas", "poema da coleção, para dizer com gestos",
          ["Duas janelas para olhar,<br>duas conchinhas para escutar,",
           "um narizinho para cheirar,<br>uma boquinha para provar,",
           "e dez dedinhos, devagarinho,<br>para tocar o mundo inteirinho."],
          pd("greenaway_janela", "120mm"),
          adulto("dizer e mostrar",
                 "Diga devagar, apontando em você e depois nela: olhos (“janelas”), orelhas (“conchinhas”), nariz, boca, dedos. "
                 "Na terceira vez, pare antes da última palavra de cada verso e espere: “para olhar…”. "
                 "Na imagem: “Quantas crianças estão na janela? O que elas estão olhando?” (três; deixe que ela imagine o que veem).",
                 credito_pd("greenaway_janela")),
          aba="--d-historias")

    observacao(L, "Hora do chá no jardim", "olhar com calma, um sentido de cada vez",
               pd("greenaway_cha", "150mm"),
               ["<b>Olhar:</b> onde está a menina de vestido azul? E a de rosa?",
                "<b>Escutar:</b> que barulho fazem as xícaras? E os passarinhos da árvore?",
                "<b>Cheirar:</b> há flores no jardim. Que cheiro elas têm?",
                "<b>Provar:</b> o que será que tem no bule? Chá, leite, suco?",
                "<b>Tocar:</b> a mesa é lisa ou áspera? E a grama?"],
               adulto("observação dirigida",
                      "Não faça todas as perguntas no mesmo dia: escolha uma ou duas. Deixe o dedo dela passear pela imagem e nomeie o que ela "
                      "apontar. Depois, faça um “chá” de verdade com xícaras pequenas e repita as mesmas perguntas com objetos reais.",
                      credito_pd("greenaway_cha")),
               aba="--d-artes")

    # caixa de sons: material sensorial com controle do erro
    rot = [("maca", "arroz"), ("estrela", "feijão"), ("folha", "sal grosso")]
    etiquetas = ""
    for k, (mot, grao) in enumerate(rot):
        for j in range(2):
            x = 30 + (k * 2 + j) * 26
            etiquetas += (f'<div style="position:absolute;left:{x - 4}mm;top:186mm;width:30mm;height:30mm;border:0.4pt dashed #a9a39a;'
                          f'border-radius:50%;display:flex;align-items:center;justify-content:center">{img(mot, "20mm")}</div>')
    c = f"""<div class="miolo">{titulo("A caixa de sons", "um material para escutar com atenção", 28)}
      <div class="texto" style="margin-top:4mm">
      <p><b>Para montar (adulto):</b> seis potinhos opacos iguais. Encha dois com um pouco de arroz, dois com feijão e dois com
      sal grosso — a mesma quantidade nos dois de cada par. Feche bem e passe fita adesiva em volta da tampa.</p>
      <p><b>As etiquetas</b> vão <i>no fundo</i> dos potinhos, onde ela não vê enquanto brinca: o desenho igual mostra que os dois
      formam um par. É o “controle do erro”: ela mesma confere, virando o potinho, sem precisar que o adulto diga se acertou.</p>
      </div>
      <div class="caixa" style="margin-top:3mm;font-size:10.5pt;line-height:1.4">
      <b>Descobrir</b> — sacuda um potinho perto do ouvido dela, depois outro: “este faz <i>chhh</i>, este faz <i>toc-toc</i>”.<br>
      <b>Relacionar</b> — com só dois pares na mesa, ela sacode e procura o som igual. Depois, os três pares.<br>
      <b>Criar</b> — ela sacode um potinho num ritmo e você imita; depois vocês trocam.</div>
    </div>
    {etiquetas}
    <div style="position:absolute;left:0;right:0;top:220mm;text-align:center" class="peq">recortar os círculos e colar no fundo dos potinhos ·
    {' · '.join(f'{g}' for _, g in rot)}</div>
    {adulto("segurança", "Os potinhos devem ficar bem vedados; grãos e sal grosso nunca ficam ao alcance sem o adulto por perto. Guarde a caixa fora da altura dela.", estilo="top:236mm;bottom:auto")}"""
    L.add(c, aba="--d-memoria")

    cartoes(L, "Coisas para sentir", [
        dict(pt="sino", mot="sino", en="bell", fr="la cloche", la="tintinnābulum", dica="<b>Escutar:</b> balance perto e longe. Alto ou baixinho?"),
        dict(pt="pena", mot="pena", en="feather", fr="la plume", la="pinna", dica="<b>Tocar:</b> passe no braço dela. Faz cócegas?"),
        dict(pt="lupa", mot="lupa", en="magnifying glass", fr="la loupe", la=None, dica="<b>Olhar:</b> uma folha de perto. O que aparece?"),
        dict(pt="mel", mot="mel", en="honey", fr="le miel", la="mel", dica="<b>Provar:</b> uma pontinha na colher. Doce!"),
        dict(pt="sabonete", mot="sabonete", en="soap", fr="le savon", la=None, dica="<b>Cheirar</b> e <b>tocar:</b> seco e molhado são diferentes?"),
        dict(pt="flor", mot="florzinha_rosa", en="flower", fr="la fleur", la="flōs", dica="<b>Cheirar:</b> procure uma flor de verdade."),
        dict(pt="laranja", mot="laranja", en="orange", fr="l’orange (fem.)", la=None, dica="<b>Cheirar</b> a casca, <b>provar</b> um gomo."),
        dict(pt="pedra", mot="pedra", en="stone", fr="la pierre", la="lapis", dica="<b>Tocar:</b> pesada e fria. E a pena?"),
        dict(pt="bolhas", mot="bolhas", en="bubbles", fr="les bulles", la="bullae", dica="<b>Olhar:</b> faça bolhas de sabão. Para onde vão?"),
    ], "Unidade 1 · Eu e meus sentidos")

    c = f"""<div class="miolo">{titulo("Ouvir de olhos fechados", "Camille Saint-Saëns · <i>O Aquário</i>, de <i>O Carnaval dos Animais</i> (1886)", 28)}
      <div class="centro" style="margin:8mm 0 4mm">
        {img('peixe', '52mm', 'display:inline-block;margin:0 4mm;transform:rotate(-6deg)')}
        {img('bolhas', '38mm', 'display:inline-block;margin:0 4mm')}
        {img('peixe_azul', '48mm', 'display:inline-block;margin:0 4mm;transform:scaleX(-1) rotate(-8deg)')}
      </div>
      <p class="centro" style="font-size:15pt;font-style:italic;line-height:1.5;margin-top:6mm">A água balança devagar.<br>
      Os peixinhos passam brilhando.<br>As bolhas sobem… plim… plim…</p>
      <div class="centro" style="margin-top:6mm">{img('bolhas', '30mm', 'display:inline-block')}</div>
    </div>
    {adulto("escuta calma",
            "Uma escuta curta (cerca de dois minutos e meio), deitadas ou no colo, com a luz baixa. Peça que ela feche os olhos e "
            "“veja” o aquário. Os pianos fazem a água ondular; as flautas e as cordas desenham os peixes; uma celesta (ou harmônica de vidro) "
            "faz os brilhos — “plim”. Depois pergunte: “a música era rápida ou devagar? alta ou baixinha?”. Não precisa explicar mais: "
            "repita a mesma escuta em outros dias. Saint-Saëns escreveu <i>O Carnaval dos Animais</i> como uma brincadeira musical; "
            "cada parte é um bicho, e ela vai reencontrar a coleção no Volume 4.")}"""
    L.add(c, aba="--d-musica")

    # traçado circular: bolhas
    centros = [(60, 105, 22), (140, 95, 26), (100, 160, 30), (52, 205, 18), (150, 200, 22)]
    svg = ""
    for (x, y, r) in centros:
        svg += pontilhado(f"M {x} {y - r} A {r} {r} 0 1 1 {x - 0.1} {y - r}")
        svg += ponto_inicio(x, y - r)
        svg += f'<path d="M {x + 3} {y - r - 2.4} l 3 2.4 l -3 2.4" fill="none" stroke="var(--oliva)" stroke-width="0.8"/>'
    tracado(L, "Bolhas de sabão", "Roda, roda, a bolha vai — sobe, sobe, e não cai!", svg,
            img("sabonete", "26mm", "position:absolute;left:18mm;top:238mm") + img("bolhas", "22mm", "position:absolute;left:44mm;top:232mm"),
            adulto("traço circular",
                   "Antes, faça bolhas de sabão de verdade e desenhe círculos no ar com o dedo. Depois, com o dedo sobre cada bolha, começando no "
                   "círculo verde e seguindo a setinha. Só então o giz grosso. Círculos fechados não são esperados aos 2 anos: o que importa é o "
                   "movimento contínuo e a mudança de direção. Se ela preferir rabiscar dentro das bolhas, ótimo — é o mesmo gesto.",
                   estilo="left:80mm"))

    passos(L, "Lavar as mãos", "uma rotina em cinco passos",
           [(img("jarra", "30mm"), "Molhar as mãos"),
            (img("sabonete", "30mm"), "Pegar o sabonete"),
            (img("bolhas", "30mm"), "Esfregar: palmas, costas e dedinhos"),
            (img("gota", "16mm", "margin:5mm auto 7mm"), "Enxaguar até sair a espuma"),
            (img("toalha", "30mm"), "Secar e pendurar a toalha"),
            ('<div style="font-size:12pt;font-style:italic;line-height:1.45;padding-top:2mm">Esfrega, esfrega,<br>mão com mão;<br>'
             'sai a sujeira,<br>fica o sabão!<br>Água, água,<br>leva a espuma…<br>e não sobra<br>coisa nenhuma!</div>', "Cantar enquanto esfrega")],
           adulto("vida prática",
                  "Recorte os cinco quadros (ou deixe a página inteira) e cole na altura dos olhos dela, perto da pia. Um banquinho firme e uma "
                  "toalha só dela, num gancho baixo, ajudam mais do que qualquer explicação. Mostre devagar, sem falar, e depois deixe que ela "
                  "faça; ajude só no passo em que ela parar. A cantiga dura o tempo certo de esfregar (cerca de 20 segundos se cantada duas vezes)."))


# ================================================================== UNIDADE 2

def unidade2(L):
    L.unidade = "Unidade 2 · Minha casa e meus objetos"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 2 · Minha casa e meus objetos", aba="--d-vida",
        pergunta="Cada coisa tem um nome, um uso e um lugar — e eu sei cuidar delas.",
        duracao="Dois fins de semana · dois encontros · 15 a 25 minutos, sempre terminando com algo de verdade: pôr a mesa, guardar.",
        objetivos=["Nomear nove objetos da casa e dizer para que servem.",
                   "Correspondência um a um: um prato para cada pessoa, uma colher para cada prato.",
                   "Parear objeto real e contorno (o jogo americano).",
                   "Acompanhar uma história de duas páginas e recontá-la com objetos.",
                   "Manter um pulso regular batendo colher na tigela."],
        repertorio="<b>História:</b> <i>Cada coisa no seu lugar</i> (texto da coleção). <b>Imagens:</b> Beatrix Potter, <i>The Tailor of Gloucester</i> (1903) "
                   "e <i>Cecily Parsley's Nursery Rhymes</i> (1922). <b>Música:</b> a orquestra da cozinha. <b>Cantiga:</b> <i>Pirulito que bate bate</i> (tradicional). "
                   "<b>Línguas:</b> <i>cup · la tasse · pōculum</i>.",
        materiais="Xícara, colher, prato, tigela de verdade, de preferência inquebráveis e do tamanho dela; uma cesta para guardar brinquedos; "
                  "papel cartão para o jogo americano.",
        vida="Pôr a mesa com o jogo americano; levar o prato à pia com as duas mãos; guardar cada brinquedo no seu cesto.",
        etapas=[["Passear pela casa nomeando objetos.", "História com a xícara de verdade na mão.", "Cartões: três por vez."],
                ["Jogo americano: pôr cada objeto no contorno.", "Um prato para cada pessoa da família.", "“Onde mora a colher?”"],
                ["Recontar com os objetos.", "Orquestra da cozinha: forte e fraquinho.", "Arrumar a casinha do ratinho."]],
        indicadores=["Busca o objeto pedido em outro cômodo.", "Põe um item em cada lugar sem sobrar nem faltar (até 3).",
                     "Usa o objeto pelo nome ao pedir (“quero a colher”).", "Completa frases da história.",
                     "Bate um pulso regular por alguns tempos.", "Guarda um brinquedo no lugar sem ser lembrada."],
        interesse="dê a ela uma “gaveta só dela” na cozinha com seus utensílios; deixe que lave uma xícara de plástico na bacia.",
        dificil="só pôr a mesa juntas, nomeando cada coisa."))

    historia(L, "Cada coisa no seu lugar", "uma história da coleção",
             f"""{pd("potter_rato_xicara", "78mm", "float:right;margin:0 0 3mm 5mm")}
             <p class="capitular" style="margin-top:4mm">Numa casinha pequena, embaixo do armário da cozinha, morava uma ratinha muito arrumadeira.</p>
             <p>Todo dia de manhã ela dizia:</p>
             <p class="fala">— Cada coisa no seu lugar!</p>
             <p>A xícara ia para a prateleira. A colher ia para a gaveta. O prato ia para o escorredor.</p>
             <p>Mas um dia a ratinha procurou, procurou… e não achou a sua xícara de chá!</p>""",
             adulto("contar com objetos",
                    "Tenha à mão uma xícara, uma colher e um prato. Quando a história disser “a xícara ia para a prateleira”, ponha a xícara "
                    "num lugar alto; a colher, numa gaveta. Ela vai querer fazer isso sozinha na segunda vez.",
                    credito_pd("potter_rato_xicara")),
             aba="--d-historias")

    historia(L, None, None,
             f"""<p style="margin-top:6mm">Então chamou as irmãs ratinhas, e todas vieram ajudar.</p>
             {pd("potter_ratos_costura", "118mm", "margin:3mm auto 4mm")}
             <p>Olharam embaixo da mesa. Não estava.<br>Olharam dentro da tigela. Não estava.</p>
             <p>Até que a menorzinha gritou:</p>
             <p class="fala">— Achei!</p>
             <p>A xícara estava no chão, de cabeça para baixo, servindo de banquinho! A ratinha riu, lavou a xícara e guardou na prateleira:</p>
             <p class="fala">— Cada coisa no seu lugar!</p>""",
             adulto("narrar",
                    "Depois de contar: “O que a ratinha perdeu?” · “Onde elas procuraram?” · “Onde estava a xícara?”. "
                    "Brinque de esconder a xícara de verdade pela casa e procurem juntas, dizendo “não está… não está… achei!”. "
                    "Na imagem, conte as ratinhas com ela, tocando cada uma.",
                    credito_pd("potter_ratos_costura")),
             aba="--d-historias")

    cartoes(L, "Coisas da casa", [
        dict(pt="xícara", mot="xicara", en="cup", fr="la tasse", la="pōculum", dica="Segure com as duas mãos. Quente ou fria?"),
        dict(pt="colher", mot="colher", en="spoon", fr="la cuillère", la="cochleāre", dica="Bata de leve na tigela: tim, tim!"),
        dict(pt="prato", mot="prato", en="plate", fr="l’assiette (fem.)", la="patella", dica="Um prato para cada pessoa da mesa."),
        dict(pt="tigela", mot="tigela", en="bowl", fr="le bol", la="catīnus", dica="O que cabe dentro? Mingau, fruta, água…"),
        dict(pt="vela", mot="vela", en="candle", fr="la bougie", la="candēla", dica="Só o adulto acende. Assopre junto!"),
        dict(pt="chave", mot="chave", en="key", fr="la clé", la="clāvis", dica="Abra e feche uma porta com ela."),
        dict(pt="livro", mot="livro", en="book", fr="le livre", la="liber", dica="Virar a página bem devagar, pela ponta."),
        dict(pt="cesta", mot="cesta", en="basket", fr="le panier", la="corbis", dica="Guardar os brinquedos: cada um no seu lugar."),
        dict(pt="mesa", mot="mesa", en="table", fr="la table", la="mēnsa", dica="Passar o pano depois de comer."),
    ], "Unidade 2 · Minha casa e meus objetos")

    # jogo americano em tamanho real
    svg = (f'<rect x="22" y="40" width="166" height="118" rx="6" fill="none" stroke="var(--linha)" stroke-width="0.6"/>'
           f'<circle cx="105" cy="102" r="40" fill="none" stroke="var(--sepia)" stroke-width="0.8" stroke-dasharray="2 1.6"/>'
           f'<circle cx="105" cy="102" r="27" fill="none" stroke="var(--sepia-claro)" stroke-width="0.5" stroke-dasharray="1.4 1.4"/>'
           f'<path d="M 161 68 m -3.5 0 a 3.5 7 0 1 0 7 0 a 3.5 7 0 1 0 -7 0 M 161 75 L 161 134" fill="none" stroke="var(--sepia)" stroke-width="0.8" stroke-dasharray="2 1.6"/>'
           f'<circle cx="160" cy="54" r="11" fill="none" stroke="var(--sepia)" stroke-width="0.8" stroke-dasharray="2 1.6"/>'
           f'<rect x="34" y="66" width="22" height="70" rx="2" fill="none" stroke="var(--sepia)" stroke-width="0.8" stroke-dasharray="2 1.6"/>')
    c = f"""<div class="miolo">{titulo("Pôr a mesa", "o jogo americano — cada coisa no seu contorno", 28)}</div>
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>
    <div style="position:absolute;top:140mm;left:32mm;width:30mm;text-align:center" class="peq">guardanapo</div>
    <div style="position:absolute;top:144mm;left:90mm;width:30mm;text-align:center" class="peq">prato</div>
    <div style="position:absolute;top:137mm;left:150mm;width:22mm;text-align:center" class="peq">colher</div>
    <div style="position:absolute;top:43mm;left:140mm;width:40mm;text-align:center" class="peq">copo</div>
    <div class="centro" style="position:absolute;top:166mm;left:0;right:0">
      {img('prato', '34mm', 'display:inline-block;margin:0 3mm')}{img('colher', '24mm', 'display:inline-block;margin:0 3mm')}
      {img('xicara', '30mm', 'display:inline-block;margin:0 3mm')}</div>
    {adulto("vida prática e correspondência",
            "Imprima em papel grosso (ou cole sobre papelão) e plastifique: vira o jogo americano dela. Os contornos têm o tamanho de um prato "
            "infantil de cerca de 20 cm, um copo pequeno e uma colher de sobremesa; se os seus objetos forem diferentes, contorne-os à mão sobre "
            "a folha. <b>Descobrir:</b> ponha um objeto de cada vez no contorno, nomeando. <b>Relacionar:</b> entregue os quatro objetos misturados e "
            "deixe que ela encontre o lugar de cada um. <b>Criar:</b> monte jogos americanos para a família e pergunte quantos pratos faltam.",
            estilo="top:206mm;bottom:auto")}"""
    L.add(c, aba="--d-vida")

    observacao(L, "Na cozinha da coelha", "o que tem numa cozinha?", pd("potter_cozinha", "140mm"),
               ["O que a coelha está fazendo? Ela está despejando alguma coisa do avental.",
                "Aponte a <b>tigela</b> vermelha. O que tem dentro? (florezinhas amarelas)",
                "Quantas garrafas você vê no chão? Vamos contar juntas.",
                "O que fica na prateleira, lá no alto?",
                "E na nossa cozinha: onde ficam as tigelas? E as colheres?"],
               adulto("observar e comparar",
                      "Na imagem há quatro garrafas no chão, à direita, e a coelha despeja flores amarelas numa tigela vermelha. Não corrija a contagem: conte de novo, devagar, "
                      "tocando cada uma. Depois vá até a cozinha de vocês e repita as perguntas com as coisas de verdade.",
                      credito_pd("potter_cozinha")),
               aba="--d-artes")

    linhas = ""
    padroes = [("Pulso", "● ● ● ● ● ● ● ●", "colher na tigela, sempre igual, como um relógio"),
               ("Forte e fraquinho", "● · ● · ● · ● ·", "uma batida forte, uma de leve — tum, tim, tum, tim"),
               ("Rápido e devagar", "●●●● ● ● ● ●", "quatro batidinhas rápidas, depois quatro bem devagar"),
               ("Silêncio", "● ● ● ⁀ ● ● ● ⁀", "três batidas e… psiu! As mãos param no ar")]
    for nome, pat, desc in padroes:
        linhas += (f'<tr><td style="font-weight:600;font-size:12pt;width:38mm">{nome}</td>'
                   f'<td style="font-size:20pt;letter-spacing:.12em;color:var(--d-musica)">{pat}</td>'
                   f'<td style="font-size:10pt;font-style:italic;color:var(--sepia)">{desc}</td></tr>')
    c = f"""<div class="miolo">{titulo("A orquestra da cozinha", "pulso, forte e fraco, rápido e devagar", 28)}
      <div class="centro" style="margin:6mm 0">
        {img('tigela', '42mm', 'display:inline-block;margin:0 3mm')}{img('colher', '26mm', 'display:inline-block;margin:0 2mm;transform:rotate(30deg)')}
        {img('xicara', '38mm', 'display:inline-block;margin:0 3mm')}{img('prato', '40mm', 'display:inline-block;margin:0 3mm')}</div>
      <table class="tab" style="margin-top:4mm">{linhas}</table>
      <p class="centro" style="font-size:13pt;font-style:italic;margin-top:7mm;line-height:1.45">Pirulito que bate bate,<br>pirulito que já bateu;<br>
      quem gosta de mim é ela,<br>quem gosta dela sou eu.</p>
      <p class="centro peq">cantiga tradicional — bata o pulso na tigela enquanto canta</p>
    </div>
    {adulto("música e corpo",
            "Use colheres de pau e uma tigela de plástico ou metal. Leia os padrões da esquerda para a direita, tocando cada bolinha: o ponto grande "
            "é uma batida forte, o pequeno é de leve, e o arco é um silêncio. Aos 2 anos, manter o pulso por alguns tempos já é uma conquista; "
            "a alternância forte-fraco e o silêncio combinado são o próximo passo. Deixe que ela seja a regente às vezes: você toca, ela mostra a mão "
            "aberta para parar.")}"""
    L.add(c, aba="--d-musica")


# ================================================================== UNIDADE 3

FRUTAS = [
    dict(pt="maçã", mot="maca", en="apple", fr="la pomme", la="mālum", sci="Malus domestica",
         dica="Corte ao meio, atravessado: aparece uma estrela de sementes."),
    dict(pt="pera", mot="pera", en="pear", fr="la poire", la="pirum", sci="Pyrus communis",
         dica="Ponha ao lado da maçã: qual é mais comprida?"),
    dict(pt="banana", mot="banana", en="banana", fr="la banane", la=None, sci="Musa sp.",
         dica="O adulto começa a descascar; ela termina."),
    dict(pt="laranja", mot="laranja", en="orange", fr="l’orange (fem.)", la=None, sci="Citrus × sinensis",
         dica="Role na mesa. A pera também rola?"),
    dict(pt="morango", mot="morango", en="strawberry", fr="la fraise", la="frāgum", sci="Fragaria × ananassa",
         dica="As sementinhas ficam do lado de fora. Toque e sinta."),
    dict(pt="uva", mot="uva", en="grapes", fr="le raisin", la="ūva", sci="Vitis vinifera",
         dica="Corte cada uva ao comprido antes de oferecer."),
    dict(pt="jabuticaba", mot="jabuticaba", en="jabuticaba", fr="jaboticaba", la=None, sci="Plinia cauliflora",
         dica="Nasce grudada no tronco! Procure uma jabuticabeira."),
    dict(pt="cereja", mot="cereja", en="cherry", fr="la cerise", la="cerasum", sci="Prunus avium",
         dica="Duas cerejas, um cabinho: um par."),
    dict(pt="melancia", mot="melancia", en="watermelon", fr="la pastèque", la=None, sci="Citrullus lanatus",
         dica="É quase toda água: aperte um pedaço e veja o suco."),
]


def unidade3(L):
    L.unidade = "Unidade 3 · O jardim e o pomar"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 3 · O jardim e o pomar", aba="--d-natureza",
        pergunta="De onde vêm os frutos? Olhar, cheirar, nomear, separar, contar até três e contar histórias.",
        duracao="Três fins de semana · dois encontros por fim de semana · de 15 a 25 minutos, em blocos curtos. Pare enquanto o interesse ainda está alto.",
        objetivos=["Nomear e reconhecer de 6 a 9 frutas e 4 flores do cotidiano.", "Comparar por cor, tamanho e cheiro; separar em dois grupos.",
                   "Acompanhar uma história cumulativa e antecipar a frase repetida.", "Correspondência um a um e quantidades até 3, com objetos reais.",
                   "Primeiro traço controlado: linha vertical, de cima para baixo.", "Escutar música descritiva e reconhecer um tema que volta."],
        repertorio="<b>História:</b> <i>A cesta do pomar</i> (texto da coleção). <b>Cantiga:</b> <i>Alecrim dourado</i> (tradicional). "
                   "<b>Música:</b> Vivaldi, <i>A Primavera</i>, 1º movimento. <b>Imagem:</b> Kate Greenaway, girassóis (1878). "
                   "<b>Línguas</b> (no máximo três palavras por semana): <i>apple · la pomme · mālum</i>.",
        materiais="Cesta pequena; 3 ou 4 frutas de verdade; pano de prato; faca sem ponta; duas cestinhas ou pratos (vermelho e amarelo); "
                  "giz de cera grosso; papel cartão (180 g ou mais); gravação de <i>As Quatro Estações</i>.",
        vida="Lavar a fruta na bacia, enxugar, descascar a banana (o adulto inicia, ela termina), pôr a fruta na cesta e levar à mesa com as duas mãos.",
        etapas=[["Cesta real: tocar, cheirar, nomear.", "História, primeira escuta.", "Cartões: 3 por vez, mostrar e dizer.", "Ouvir <i>A Primavera</i> no colo."],
                ["“Qual é a vermelha?” — duas frutas reais.", "Separar por cor nas duas cestas.", "Memória com cartas viradas para cima.", "Um morango para cada prato."],
                ["Recontar com a cesta e os cartões.", "“O que mais caberia na cesta?”", "Chuva no jardim: traço e som.", "Dançar o tema, os pássaros e o trovão."]],
        indicadores=["Aponta ou nomeia frutas espontaneamente.", "Completa a frase “— Uma maçã para a…”.", "Junta duas cartas iguais com as cartas à vista.",
                     "Separa frutas por um critério que ela mesma escolhe.", "Faz o traço de cima para baixo com o dedo e com o giz.",
                     "Reage com o movimento combinado quando o tema de Vivaldi volta."],
        interesse="visite uma feira e procure as frutas dos cartões; abra uma maçã atravessada (página de observação).",
        dificil="só a história e a cesta; o resto espera.",
        alerta="<b>Segurança à mesa.</b> Uvas, cerejas e jabuticabas inteiras são risco de engasgo antes dos 4 anos: corte as uvas ao comprido, "
               "retire caroços e sementes, e ofereça sempre com a criança sentada."))

    frutas = "".join(img(n, "33mm", "display:inline-block;margin:0 1.5mm") for n in ("maca", "pera", "banana", "laranja"))
    historia(L, "A cesta do pomar", "uma história para contar e recontar", f"""
      <div class="centro" style="margin:4mm 0 3mm">{frutas}</div>
      <p class="capitular" style="margin-top:6mm">Era uma manhã de sol. Marina pegou a cesta de vime e foi ao pomar.</p>
      <p>Debaixo da macieira, encontrou uma maçã vermelha.</p>
      <p class="fala">— Uma maçã para a cesta!</p>
      <p>Perto do muro, a pereira deixou cair uma pera.</p>
      <p class="fala">— Uma pera para a cesta! Uma pera e uma maçã.</p>
      <p>Na bananeira, um cacho de bananas amarelas esperava.</p>
      <p class="fala">— Uma banana para a cesta! Uma banana, uma pera e uma maçã.</p>
      <p>E lá no fundo, a laranjeira estava cheia de laranjas redondas.</p>
      <p class="fala">— Uma laranja para a cesta! Uma laranja, uma banana, uma pera e uma maçã.</p>""", tam=34)

    historia(L, None, None, f"""
      {img('cesta', '48mm', 'float:right;margin:0 0 2mm 4mm')}
      <p style="margin-top:6mm">A cesta ficou pesada. Marina sentou-se debaixo da jabuticabeira para descansar.</p>
      <p>Então, de mansinho, saiu da grama um ratinho de bigodes finos. Ele olhou para a cesta… e olhou para Marina.</p>
      <p class="fala">— Você está com fome, ratinho?</p>
      <p>O ratinho mexeu os bigodes.</p>
      {img('jabuticaba', '62mm', 'margin:1mm auto 2mm')}
      <p>Marina esticou a mão até o tronco da jabuticabeira e colheu uma jabuticaba bem pretinha.</p>
      <p class="fala">— Esta é para você.</p>
      <p>Marina voltou para casa com a cesta cheia.<br>E o ratinho voltou para a toca… com a barriga cheia.</p>
      {img('ratinho', '30mm', 'position:absolute;right:4mm;bottom:52mm')}""",
             adulto("contar e narrar",
                    "<b>Antes:</b> mostre uma cesta com frutas de verdade e deixe que ela segure e cheire cada uma. "
                    "<b>Durante:</b> pare antes da frase repetida e espere: “— Uma maçã para a…”. Mexa o nariz quando o ratinho mexer os bigodes. "
                    "<b>Depois</b> (narração): “O que Marina achou primeiro?” · tire as frutas da cesta e peça que ela as devolva na ordem da história · "
                    "“O ratinho estava com fome. O que ele ganhou?” · “Se você encontrasse o ratinho, o que daria a ele?”. "
                    "Não corrija: repita a fala dela, ampliando-a (“Maçã! Uma maçã vermelha e redonda”)."))

    observacao(L, "Abrir uma maçã", "o que tem por dentro?",
               img("maca", "58mm", "display:inline-block;margin:0 6mm;vertical-align:middle") +
               img("maca_cortada", "70mm", "display:inline-block;margin:0 6mm;vertical-align:middle"),
               ["Por fora: de que cor é a <b>casca</b>? Lisa ou áspera?",
                "O adulto corta a maçã <b>atravessada</b>, pelo meio da barriga.",
                "Por dentro: a <b>polpa</b> é clara. Que cheiro tem?",
                "No meio, uma <b>estrela</b>! Quantas pontas? Vamos contar.",
                "As <b>sementes</b> ficam escondidas na estrela. Uma maçã nova pode nascer de uma semente."],
               adulto("observação e vocabulário preciso",
                      "Cortada no sentido do “equador” (não de cima para baixo), a maçã mostra cinco compartimentos de sementes em forma de estrela. "
                      "Nomeie as partes com as palavras certas — casca, polpa, semente, cabinho —, mostrando cada uma. "
                      "Guarde algumas sementes num algodão úmido: em alguns dias, talvez germinem (o Volume 6 volta a isso). "
                      "Depois, faça o mesmo com uma pera e compare: a pera também tem estrela?"),
               aba="--d-natureza")

    xs = [38, 72, 105, 138, 172]
    y0, y1 = 88, 208
    svg = ""
    for x in xs:
        svg += pontilhado(f"M {x} {y0} L {x} {y1}") + ponto_inicio(x, y0 - 1)
        svg += (f'<path d="M {x} {y0 + 10} l -2.4 -3.4 M {x} {y0 + 10} l 2.4 -3.4" stroke="var(--oliva)" '
                f'stroke-width="0.8" fill="none" stroke-linecap="round"/>')
    flores = ["florzinha_rosa", "florzinha_azul", "florzinha_amarela", "florzinha_rosa", "florzinha_azul"]
    imgs = "".join(img(n, "22mm", f"position:absolute;left:{x - 11}mm;top:{y1 + 2}mm") for x, n in zip(xs, flores))
    imgs += img("nuvem", "92mm", "position:absolute;left:12mm;top:42mm") + img("nuvem", "92mm", "position:absolute;left:104mm;top:40mm;transform:scaleX(-1)")
    tracado(L, "A chuva no jardim", "Plim, plim, plim, a chuva cai — do céu pra flor a gota vai.", svg, imgs,
            adulto("traçado vertical",
                   "<b>Primeiro com o corpo:</b> de pé, braços no alto, “a chuva cai” até tocar o chão. <b>Depois com o dedo</b> sobre cada linha, "
                   "começando no círculo verde e dizendo “plim” a cada pontinho. <b>Só então</b> o giz de cera grosso, seguro como ela conseguir. "
                   "Por volta dos 2 anos a linha vertical é o primeiro traço controlado: não espere precisão nem exija “ficar na linha”. "
                   "Uma ou duas linhas já bastam num dia."))

    c = f"""<div class="miolo">{titulo("Vermelhas e amarelas", "separar por cor", 28)}</div>
    <div style="position:absolute;left:16mm;top:52mm;width:84mm;height:120mm" class="caixa centro">
      <div style="font-size:16pt;color:#b8352e;font-weight:600;margin-top:2mm">vermelhas</div>
      {img('cesta', '70mm', 'margin:68mm auto 0')}</div>
    <div style="position:absolute;left:110mm;top:52mm;width:84mm;height:120mm" class="caixa centro">
      <div style="font-size:16pt;color:#c99a1f;font-weight:600;margin-top:2mm">amarelas</div>
      {img('cesta', '70mm', 'margin:68mm auto 0')}</div>
    <div class="centro" style="position:absolute;left:0;right:0;top:178mm">
      {img('morango', '18mm', 'display:inline-block;margin:0 2mm')}{img('cereja', '18mm', 'display:inline-block;margin:0 2mm')}
      {img('maca', '18mm', 'display:inline-block;margin:0 2mm')}<span style="display:inline-block;width:12mm"></span>
      {img('banana', '18mm', 'display:inline-block;margin:0 2mm')}{img('pera', '18mm', 'display:inline-block;margin:0 2mm')}
      {img('laranja', '18mm', 'display:inline-block;margin:0 2mm')}</div>
    {adulto("classificar por um atributo",
            "Use os cartões de frutas (próximas páginas) ou, melhor ainda, frutas de verdade. <b>Descobrir:</b> mostre uma fruta vermelha e uma amarela; "
            "nomeie a cor de cada uma. <b>Relacionar:</b> ponha uma fruta de modelo em cada cesta e entregue as outras uma a uma: “onde mora esta?”. "
            "A laranja e a pera podem gerar boa conversa (“é amarela ou laranja?”): aceite a escolha dela se ela explicar. "
            "<b>Criar:</b> ela inventa outro jeito de separar — grandes e pequenas, as que rolam e as que não rolam.",
            estilo="top:206mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    cartoes(L, "Frutas do pomar", FRUTAS, "Unidade 3 · O jardim e o pomar")

    MEMO = [("tulipa", "tulipa"), ("margarida", "margarida"), ("girassol", "girassol"),
            ("folha", "folha"), ("cogumelo", "cogumelo"), ("bolota", "bolota")]
    memoria(L, "Achados do jardim", [(r, img(m, "35mm")) for r, m in MEMO], [0, 3, 1, 4, 2, 5, 3, 0, 5, 1, 4, 2],
            adulto("três níveis do mesmo jogo",
                   "<b>Descobrir:</b> 3 pares, cartas viradas para cima; ela acha a carta igual e diz o nome. <b>Relacionar:</b> 2 ou 3 pares virados "
                   "para baixo; vire uma de cada vez e espere que ela lembre onde estava a outra. <b>Criar:</b> “Qual sumiu?” — mostre 4 cartas, "
                   "esconda uma, e peça que ela descubra qual falta. Comece sempre um nível abaixo do que ela consegue: o jogo precisa terminar em sucesso. "
                   "<b>Atenção:</b> o cogumelo da carta é de livro de histórias; cogumelos do quintal nunca se põem na boca.",
                   estilo="bottom:19mm;top:auto"))

    musica_primavera(L)


def musica_primavera(L):
    estacoes = [("m_tema", "Tema", "marchar e bater palmas leves"), ("m_passaros", "Pássaros", "dedinhos voando · “piu, piu”"),
                ("m_tema", "Tema", "palmas"), ("m_riacho", "Riacho", "braços em onda, devagar"), ("m_tema", "Tema", "palmas"),
                ("m_trovao", "Trovoada", "tambor nas pernas, forte!"), ("m_tema", "Tema", "palmas"),
                ("m_passaros", "Os pássaros voltam", "dedinhos voando de novo"), ("m_tema", "Tema", "palmas e… fim!")]
    cel, pts = [], []
    for i, (m, nome, mov) in enumerate(estacoes):
        r, k = divmod(i, 3)
        col = k if r % 2 == 0 else 2 - k
        x, y = 22 + col * 58, 78 + r * 50
        pts.append((47 + col * 58, 91 + r * 50))
        cel.append(f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:50mm;text-align:center">{img(m, "40mm", "margin:0 auto")}'
                   f'<div style="font-weight:600;font-size:12.5pt;margin-top:-1mm"><span style="color:var(--rosa)">{i + 1}</span> · {nome}</div>'
                   f'<div class="peq it" style="font-size:8.6pt;color:var(--sepia)">{mov}</div></div>')
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    c = f"""<div class="miolo">{titulo("Ouvir com o corpo", "Antonio Vivaldi · <i>A Primavera</i> · Concerto em mi maior, RV 269 · 1º movimento, Allegro")}
      <p class="centro" style="font-size:10pt;margin-top:2.5mm;color:var(--sepia)"><i>Giunt’è la Primavera e festosetti / la salutan gl’augei con lieto canto…</i><br>
      “Chegou a Primavera, e os passarinhos a saúdam, em festa, com alegre canto…” — do soneto que acompanha a partitura.</p></div>
    <svg class="svgpag" viewBox="0 0 210 297"><path d="{d}" fill="none" stroke="var(--linha)" stroke-width="0.7" stroke-dasharray="1.6 2.2"/></svg>
    {''.join(cel)}
    {adulto("escuta ativa (musicograma)",
            "O movimento é um <b>ritornelo</b>: um tema alegre que sempre volta, com episódios entre uma volta e outra — os pássaros, o riacho, a trovoada. "
            "<b>1ª escuta:</b> no colo, só ouvindo; aponte cada desenho quando a música chegar nele. <b>2ª escuta:</b> façam os movimentos juntas. "
            "<b>Depois:</b> “Quando veio o trovão, a música ficou forte ou fraquinha?”. Os desenhos são sinais de som, não figuras para colorir. "
            "Vivaldi (1678–1741) era padre em Veneza, apelidado de “o Padre Ruivo”, e ensinava música às meninas do Ospedale della Pietà. "
            "O 1º movimento dura cerca de três minutos e meio, conforme a gravação.")}"""
    L.add(c, aba="--d-musica")


# ================================================================== UNIDADE 4

ANIMAIS = [
    dict(pt="galo", pd="cartao_galo", som="cocoricó!", en="rooster · <i>cock-a-doodle-doo</i>", fr="le coq · <i>cocorico</i>",
         la="gallus", dica="Ele canta quando o sol nasce."),
    dict(pt="vaca", pd="cartao_vaca", som="muuu!", en="cow · <i>moo</i>", fr="la vache · <i>meuh</i>", la="vacca",
         dica="Dá o leite do café da manhã."),
    dict(pt="porco", pd="potter_porco", som="oinc, oinc!", en="pig · <i>oink</i>", fr="le cochon · <i>groin groin</i>", la="porcus",
         dica="Gosta de lama para se refrescar."),
    dict(pt="ganso", pd="potter_gansos", som="quén, quén!", en="goose · <i>honk</i>", fr="l’oie (fem.)", la="ānser",
         dica="Anda em fila, um atrás do outro."),
    dict(pt="cavalo", pd="cartao_cavalo", som="iiirrrí!", en="horse · <i>neigh</i>", fr="le cheval", la="equus",
         dica="Faça o trote com a língua: tloc, tloc."),
    dict(pt="gato", pd="potter_gato_cesto", som="miau!", en="cat · <i>meow</i>", fr="le chat · <i>miaou</i>", la="fēlēs",
         dica="Dorme enroladinho. Faça um carinho de leve."),
    dict(pt="coelho", pd="potter_benjamin", som="(silêncio…)", en="rabbit", fr="le lapin", la="cunīculus",
         dica="Quase não faz barulho. Mexe o nariz!"),
    dict(pt="rato", pd="potter_rato_xicara", som="cuim, cuim!", en="mouse · <i>squeak</i>", fr="la souris · <i>couic</i>", la="mūs",
         dica="Pequenininho. Cabe numa xícara!"),
    dict(pt="sapo", pd="potter_sapo_lago", som="croac!", en="frog · <i>ribbit</i>", fr="la grenouille · <i>coâ</i>", la="rāna",
         dica="Pula e nada. Mora perto da água."),
]


def unidade4(L):
    L.unidade = "Unidade 4 · Os animais da fazenda e do bosque"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 4 · Os animais da fazenda e do bosque", aba="--d-historias",
        pergunta="Quem mora na fazenda e no bosque? Como cada um fala, anda e vive?",
        duracao="Três fins de semana · dois encontros · 15 a 25 minutos. Se possível, uma visita a um sítio, fazendinha ou zoológico.",
        objetivos=["Reconhecer e nomear nove animais em ilustrações e imitar o som de cada um.",
                   "Comparar grande e pequeno com pares de animais.", "Contar até 3 (e conferir até 5 com ajuda) numa cena.",
                   "Acompanhar uma história cumulativa e antecipar quem vem depois.", "Mover-se com contraste: galinha ciscando, galo de peito estufado."],
        repertorio="<b>História:</b> <i>Quem acordou primeiro?</i> (texto da coleção). <b>Cantiga:</b> <i>O sapo não lava o pé</i> (tradicional). "
                   "<b>Imagens:</b> Randolph Caldecott (1880) e Beatrix Potter (1903–1922). <b>Música:</b> Saint-Saëns, <i>Galinhas e Galos</i>. "
                   "<b>Línguas:</b> <i>cat · le chat · fēlēs</i> — e como os animais “falam” em cada língua.",
        materiais="Bichinhos de brinquedo (vaca, porco, cavalo, galo, gato), uma caixa de sapato como “estábulo”, cartões da unidade.",
        vida="Dar água a um animal ou a uma planta: encher o potinho, carregar sem derramar, servir devagar.",
        etapas=[["Nomear e imitar os sons dos cartões.", "História no colo.", "Ouvir <i>Galinhas e Galos</i>."],
                ["Grande e pequeno: pares de animais.", "“Quem faz cocoricó?” — achar o cartão.", "Contar as vacas da cena."],
                ["Recontar com os bichinhos de brinquedo.", "Inventar um animal novo e o som dele.", "Dançar como cada bicho."]],
        indicadores=["Faz o som certo ao ver o cartão.", "Encontra o cartão quando o adulto faz o som.", "Diz “grande” e “pequeno” comparando dois animais.",
                     "Antecipa o próximo animal da história.", "Conta 3 objetos tocando um de cada vez.", "Imita o movimento de um animal com o corpo todo."],
        interesse="leia o original de <i>O Coelho Pedro</i> (Volume 2) e procure coelhos, sapos e gatos nos livros da casa.",
        dificil="só os cartões e os sons.",
        alerta="<b>Animais de verdade.</b> Em visitas, a criança toca animais só com o adulto e com a permissão do dono; mãos lavadas depois."))

    historia(L, "Quem acordou primeiro?", "uma história da coleção, para contar com sons", f"""
      {pd("caldecott_galo", "70mm", "float:right;margin:0 0 3mm 5mm")}
      <p class="capitular" style="margin-top:4mm">O sol ainda estava escondido atrás do morro quando o galo subiu no muro e cantou:</p>
      <p class="fala">— Cocoricó!</p>
      <p>A vaca abriu um olho e disse:</p>
      <p class="fala">— Muuu! Já é de manhã?</p>
      <p>O porco virou para o outro lado:</p>
      <p class="fala">— Oinc, oinc… mais um pouquinho…</p>
      <p>Os gansos saíram em fila, um atrás do outro:</p>
      <p class="fala">— Quén, quén, quén!</p>""",
             credito_pd("caldecott_galo").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'),
             aba="--d-historias")

    historia(L, None, None, f"""
      <p style="margin-top:6mm">O cavalo bateu o casco no chão:</p>
      <p class="fala">— Iiirrrí! Bom dia, fazenda!</p>
      {pd("potter_gansos", "100mm", "margin:2mm auto 3mm")}
      <p>Só o gato continuava dormindo, enroladinho no cesto. O galo cantou de novo, mais forte: <i>— Cocoricó!</i></p>
      <p>E o gato, sem abrir os olhos, respondeu baixinho:</p>
      <p class="fala">— Miau… Quem acordou primeiro foi o galo. Quem dorme mais… sou eu.</p>""",
             adulto("sons e sequência",
                    "Na primeira vez, faça você todos os sons. Na segunda, faça só o começo de cada fala (“O porco virou para o outro lado…”) e espere "
                    "que ela faça o som. <b>Relacionar:</b> com os cartões de animais na mesa, ela põe em ordem quem acordou: galo, vaca, porco, gansos, "
                    "cavalo — e o gato por último. <b>Criar:</b> “E na nossa casa, quem acorda primeiro?”.",
                    credito_pd("potter_gansos")),
             aba="--d-historias")

    poema(L, "O sapo não lava o pé", "cantiga tradicional brasileira",
          ["O sapo não lava o pé,<br>não lava porque não quer.",
           "Ele mora lá na lagoa,<br>não lava o pé porque não quer.",
           "Mas que chulé!"],
          pd("potter_sapo_lago", "92mm"),
          adulto("cantar e brincar com os sons",
                 "Cante algumas vezes do jeito tradicional. Depois brinque de trocar todas as vogais por uma só, como se faz há gerações: "
                 "“U supu nu luvu u pu…”, “I sipi ni livi i pi…”. Ela não precisa acertar: a graça é perceber que as palavras têm sons que mudam — "
                 "é o começo da consciência fonológica. Na imagem de Beatrix Potter, o sapo (o Sr. Jeremy Fisher) pesca sentado numa folha de ninfeia.",
                 credito_pd("potter_sapo_lago")),
          aba="--d-historias")

    cartoes(L, "Animais da fazenda e do bosque", ANIMAIS, "Unidade 4 · Os animais",
            sub_frente="frente · imprimir frente e verso (borda longa) em papel de 180 g · no verso: o som de cada animal em português, inglês e francês")

    pares = [("cartao_vaca", "vaca", "potter_gato_cesto", "gato"), ("cartao_cavalo", "cavalo", "potter_rato_xicara", "rato"),
             ("potter_porco", "porco", "potter_sapo_lago", "sapo")]
    linhas = ""
    for gde, ng, peq, np_ in pares:
        linhas += (f'<div class="par"><div>{pd(gde, "54mm", "max-height:46mm;object-fit:contain")}<div class="legenda-q">{ng}</div></div>'
                   f'<div class="ou">ou</div><div>{pd(peq, "40mm", "max-height:34mm;object-fit:contain")}<div class="legenda-q">{np_}</div></div></div>')
    c = f"""<div class="miolo">{titulo("Grande e pequeno", "qual é o maior? qual é o menor?", 28)}<div class="pares">{linhas}</div></div>
    {adulto("comparar tamanhos",
            "As imagens não estão na escala real — por isso a pergunta é sobre os animais de verdade: “Quem é maior, a vaca ou o gato?”. "
            "Aos 2 anos, comparar dois é o certo; ordenar três (gato, porco, vaca) é o desafio seguinte. Use as mãos para mostrar o tamanho: "
            "braços abertos para a vaca, dois dedinhos para o rato.",
            credito_pd("cartao_vaca", "potter_gato_cesto", "cartao_cavalo", "potter_rato_xicara", "potter_porco", "potter_sapo_lago"))}"""
    L.add(c, aba="--d-matematica")

    observacao(L, "Encontre e conte", "um dia na fazenda", pd("caldecott_vaca", "118mm"),
               ["Onde está a <b>vaca grande</b>? O que ela está fazendo?",
                "Ache o <b>gato</b>. Ele está perto ou longe da vaca?",
                "E a <b>menina</b>? Ela está correndo para onde?",
                "Quantas <b>vacas</b> há no pasto, lá atrás? Uma… duas… três…",
                "Ache a <b>casa</b>, a <b>porteira</b> e a <b>árvore</b> grande."],
               adulto("observar e contar",
                      "Há cinco vacas na cena: a grande, na frente, e quatro no pasto ao fundo (uma escura, quase escondida atrás das outras). "
                      "Para ela, contar três já é ótimo: toque cada vaca e diga um número por toque. Não faça disso uma prova; se ela disser “muitas”, "
                      "responda “muitas! vamos ver quantas?” e contem juntas.",
                      credito_pd("caldecott_vaca")),
               aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Galinhas e galos", "Camille Saint-Saëns · <i>O Carnaval dos Animais</i> (1886)", 28)}
      <div class="centro" style="margin:6mm 0">{pd("caldecott_galo", "76mm")}</div>
      <table class="tab" style="font-size:12pt;margin-top:3mm">
        <tr><th style="width:48mm">Quando ouvir…</th><th>…a gente faz</th></tr>
        <tr><td>o <b>piano</b> e os <b>violinos</b> picadinhos</td><td>galinha ciscando: cabeça para a frente e para trás, passinhos curtos</td></tr>
        <tr><td>o <b>clarinete</b> cantando alto</td><td>galo de peito estufado, braços dobrados como asas</td></tr>
        <tr><td>o <b>fim</b></td><td>todos param… e sentam no ninho!</td></tr>
      </table>
    </div>
    {adulto("escuta e movimento",
            "A peça dura menos de um minuto: repita várias vezes no mesmo dia. Saint-Saëns imita o cacarejar com notas curtas e repetidas, "
            "e um clarinete faz o canto do galo. Brinque de contraste: ciscar baixinho e devagar, cantar alto como o galo. Na próxima unidade de música "
            "(Volume 4), ela vai reencontrar outros animais do mesmo <i>Carnaval</i>.",
            credito_pd("caldecott_galo"))}"""
    L.add(c, aba="--d-musica")

    passos(L, "Dar água", "cuidar de quem tem sede",
           [(img("jarra", "30mm"), "Encher a jarra até a marca"),
            (img("tigela", "30mm"), "Pôr o potinho no chão, firme"),
            (img("jarra", "30mm", "transform:rotate(-25deg)"), "Servir devagar, sem derramar"),
            (img("toalha", "30mm"), "Se molhou, secar com o pano"),
            (pd("potter_gato_cesto", "40mm"), "O gato agradece!"),
            (img("florzinha_azul", "22mm"), "Também as plantas têm sede")],
           adulto("vida prática: transferir água",
                  "Marque na jarra uma linha com fita até onde ela deve encher: é o controle do erro. Uma jarra pequena e leve, com bico, e um pano "
                  "sempre por perto. Derramar faz parte — o passo 4 está aqui de propósito. Se não houver animal em casa, regue uma planta.",
                  credito_pd("potter_gato_cesto")),
           aba="--d-vida")


# ================================================================== UNIDADE 5

def unidade5(L):
    L.unidade = "Unidade 5 · O céu: sol, lua, nuvens e chuva"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 5 · O céu: sol, lua, nuvens e chuva", aba="--d-ingles",
        pergunta="O que acontece lá em cima? O dia e a noite, a chuva e o sol.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos. Aproveite o céu de verdade: um fim de tarde, uma noite de lua, um dia de chuva.",
        objetivos=["Nomear sol, lua, estrela, nuvem e chuva.", "Ordenar quatro momentos do dia (amanhecer, meio-dia, entardecer, noite).",
                   "Comparar <i>um</i> e <i>muitos</i>; contar até 3.", "Escutar e dizer dois poemas curtos, completando palavras.",
                   "Traço radial (os raios do sol): do centro para fora."],
        repertorio="<b>Poemas:</b> Robert Louis Stevenson, <i>Rain</i> e <i>The Moon</i>, de <i>A Child's Garden of Verses</i> (1885), em tradução da coleção. "
                   "<b>Imagens:</b> Kate Greenaway (1878) e Beatrix Potter (1906). <b>Música:</b> Debussy, <i>Clair de lune</i>. "
                   "<b>Parlenda:</b> <i>Sol e chuva, casamento de viúva</i>. <b>Línguas:</b> <i>sun · le soleil · sōl</i> · <i>moon · la lune · lūna</i>.",
        materiais="Lanterna; guarda-chuva; um copo transparente com água e algodão (a “nuvem” que chove); giz de cera amarelo.",
        vida="Escolher a roupa conforme o tempo (com duas opções); ajudar a fechar a janela quando chove; rotina da noite com os cartões do dia.",
        etapas=[["Olhar o céu pela janela em horas diferentes.", "Dizer os poemas com gestos.", "Ouvir <i>Clair de lune</i> no escuro."],
                ["Ordenar os quatro cartões do dia.", "Uma lua, muitas estrelas.", "“De dia ou de noite?” com os cartões."],
                ["Fazer chover: água no algodão.", "Inventar um verso para a chuva.", "Traçar os raios do sol."]],
        indicadores=["Nomeia o sol e a lua apontando para o céu.", "Diz “noite” ou “dia” diante dos cartões.", "Coloca dois cartões do dia na ordem certa.",
                     "Completa a palavra final de um verso.", "Diferencia “um” de “muitos”.", "Faz traços do centro para fora."],
        interesse="faça um “diário do céu”: todo sábado, uma olhada pela janela e um desenho do que viu.",
        dificil="só a chuva no guarda-chuva e o poema.",
        alerta="<b>Nunca olhar diretamente para o sol</b>, nem por um instante — também vale para lupas e binóculos."))

    poema(L, "A chuva", "Robert Louis Stevenson · <i>Rain</i> (1885) · tradução da coleção",
          ["A chuva chove em todo lugar,<br>no campo e na árvore também,",
           "chove aqui nos guarda-chuvas<br>e nos navios do mar além."],
          pd("greenaway_chuva", "150mm"),
          adulto("dizer e observar",
                 "Diga o poema batendo de leve os dedos na mesa, como chuva. Na imagem de Kate Greenaway, duas meninas dividem um guarda-chuva e, lá "
                 "no mar, há navios: aponte tudo o que o poema diz — os guarda-chuvas, as árvores, os navios. "
                 "Num dia de chuva, abram um guarda-chuva de verdade e escutem o barulho das gotas.",
                 credito_pd("greenaway_chuva"),
          ),
          original="The rain is raining all around, / It falls on field and tree, / It rains on the umbrellas here, / And on the ships at sea.",
          aba="--d-historias")

    poema(L, "A lua", "Robert Louis Stevenson · <i>The Moon</i> (1885) · tradução livre da coleção",
          ["A lua tem rosto de relógio da sala;<br>ela brilha na rua, no campo, no cais,<br>e nos passarinhos que dormem nos galhos.",
           "O gato que mia, o ratinho que chia,<br>o morcego que dorme de dia —<br>todos gostam de passear à luz da lua.",
           "Mas tudo o que é do dia vai se aninhar;<br>as flores e as crianças fecham os olhos<br>até o sol, de manhã, voltar."],
          img("lua", "34mm", "display:inline-block;margin:0 4mm") + img("estrela", "16mm", "display:inline-block;margin:0 2mm 10mm")
          + img("estrela", "11mm", "display:inline-block;margin:0 2mm"),
          adulto("poema para a hora de dormir",
                 "Um poema longo para a idade: diga só a primeira estrofe por algumas semanas e acrescente as outras quando ela pedir mais. "
                 "Leia à noite, perto da janela, e procurem a lua de verdade. O poema separa os seres da noite (gato, rato, morcego) e os do dia "
                 "(flores, crianças): pergunte “e você, é do dia ou da noite?”."),
          aba="--d-historias")

    sequencia(L, "Do amanhecer à noite", "recortar os quatro quadros e pôr em ordem",
              [("o sol nasce", img("dia_amanhecer", "74mm")), ("meio-dia", img("dia_meiodia", "74mm")),
               ("o sol se põe", img("dia_entardecer", "74mm")), ("noite", img("dia_noite", "74mm"))],
              adulto("sequência temporal",
                     "<b>Descobrir:</b> olhe os quatro quadros e conte o que muda (onde está o sol, a cor do céu, a janela acesa). "
                     "<b>Relacionar:</b> recortados e misturados, ela põe em fila “primeiro… depois…”. Comece com só dois (dia e noite). "
                     "<b>Criar:</b> use os cartões na rotina: “agora é o sol se pondo — hora do banho”. A ordem certa é a da página.",
                     estilo="top:226mm;bottom:auto"))

    svg = ""
    for k in range(12):
        ang = k * math.pi / 6
        x0, y0 = 105 + 28 * math.cos(ang), 135 + 28 * math.sin(ang)
        x1, y1 = 105 + 72 * math.cos(ang), 135 + 72 * math.sin(ang)
        svg += pontilhado(f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}", cor="#d9a02a") + ponto_inicio(round(x0, 1), round(y0, 1))
    svg += '<circle cx="105" cy="135" r="22" fill="none" stroke="#d9a02a" stroke-width="1" stroke-dasharray="0.1 5" stroke-linecap="round"/>'
    tracado(L, "Os raios do sol", "do meio para fora, um raio de cada vez", svg,
            img("sol", "34mm", "position:absolute;left:24mm;top:216mm"),
            adulto("traço radial",
                   "Cada raio começa no círculo verde, perto do sol, e vai para fora. Com o dedo primeiro, dizendo “sol… brilha!”. Depois com o giz amarelo. "
                   "Doze raios são muitos: dois ou três num dia está ótimo; a página volta outras vezes. Este gesto, do centro para fora, prepara o "
                   "desenho da figura humana (os bracinhos e as perninhas que saem do corpo).",
                   estilo="left:64mm"),
            aba="--d-memoria")

    c = f"""<div class="miolo">{titulo("Uma lua, muitas estrelas", "um e muitos", 28)}</div>
    <div style="position:absolute;left:16mm;top:50mm;width:84mm;height:120mm;background:#3f4f74;border-radius:2mm" class="centro">
      <div style="color:#f4e6a8;font-size:18pt;margin-top:4mm">uma</div>
      <div style="width:48mm;height:48mm;margin:22mm auto 0;border-radius:50%;background:#f1e3a8;box-shadow:inset -12mm -2mm 0 0 #3f4f74"></div></div>
    <div style="position:absolute;left:110mm;top:50mm;width:84mm;height:120mm;background:#3f4f74;border-radius:2mm" class="centro">
      <div style="color:#f4e6a8;font-size:18pt;margin-top:4mm">muitas</div>
      {''.join(f'<div style="position:absolute;left:{x}mm;top:{y}mm;color:#f4e6a8;font-size:{s}pt">★</div>' for x, y, s in
               ((10, 22, 18), (30, 30, 12), (52, 20, 22), (66, 40, 14), (14, 48, 16), (40, 52, 24), (60, 66, 12), (20, 78, 20),
                (46, 86, 14), (64, 92, 18), (8, 100, 12), (34, 104, 16)))}</div>
    {adulto("comparar quantidades",
            "Os dois quadros foram feitos para imprimir: o fundo azul-noite é o único lugar desta coleção com cor chapada, porque o contraste ajuda a ver. "
            "<b>Descobrir:</b> “aqui tem <i>uma</i> lua; ali, <i>muitas</i> estrelas”. <b>Relacionar:</b> procure em casa “um” e “muitos” "
            "(um nariz, muitos dedos; uma mesa, muitas cadeiras). <b>Criar:</b> com estrelinhas de papel, ela decide quantas põe em cada céu — "
            "e você conta junto, até três.",
            estilo="top:180mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    observacao(L, "O sapo na chuva", "Beatrix Potter · <i>The Tale of Mr. Jeremy Fisher</i> (1906)", pd("potter_sapo_chuva", "104mm"),
               ["O que está caindo do céu? Veja os risquinhos.",
                "O sapo está molhado ou seco? Ele se importa?",
                "Onde ele está sentado? Num barquinho de folha!",
                "De que cor é o céu num dia de chuva?",
                "E você, gosta de chuva? O que faz quando chove?"],
               adulto("ler uma imagem",
                      "Beatrix Potter desenhava a chuva com riscos finos e um céu cinza-azulado. Mostre isso: “olha como ela pintou a chuva!”. "
                      "Na história original, o Sr. Jeremy Fisher, um sapo, sai para pescar no lago num dia chuvoso — e não se importa nada com a chuva. "
                      "Pergunte depois: “por que o sapo gosta de chuva?” (porque mora na água).",
                      credito_pd("potter_sapo_chuva")),
               aba="--d-artes")

    c = f"""<div class="miolo">{titulo("Música para a noite", "Claude Debussy · <i>Clair de lune</i> (Luar), da <i>Suíte bergamasca</i> (1905)", 28)}
      <div class="centro" style="margin:10mm 0 6mm">{img("dia_noite", "150mm")}</div>
      <p class="centro" style="font-size:15pt;font-style:italic;line-height:1.55">Um piano sozinho,<br>bem devagar,<br>como a luz da lua<br>passeando no mar.</p>
    </div>
    {adulto("escuta tranquila",
            "Cerca de cinco minutos de piano solo, muito suave. Apague a luz, acenda uma lanterna e deixe que ela faça a “lua” passear devagar pelo teto "
            "enquanto escuta. Se ela se mexer, que seja bem devagar, “para não acordar a lua”. Esta é uma música para repetir antes de dormir, "
            "pela semana inteira. Debussy (1862–1918) era francês e gostava de pintar com sons: água, nuvens, luar. "
            "<b>Parlenda para os dias de sol com chuva:</b> “Sol e chuva, casamento de viúva; chuva e sol, casamento de espanhol.”")}"""
    L.add(c, aba="--d-musica")


# ================================================================== UNIDADE 6

def unidade6(L):
    L.unidade = "Unidade 6 · Água, lago e patos"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 6 · Água, lago e patos", aba="--d-matematica",
        pergunta="O que flutua e o que afunda? Quem mora na água?",
        duracao="Dois fins de semana · dois encontros · 20 a 25 minutos (brincar com água pede tempo, toalha e paciência).",
        objetivos=["Prever, testar e contar o resultado: flutua ou afunda.", "Nomear animais e plantas do lago (pato, peixe, sapo, ninfeia).",
                   "Conhecer o começo de <i>O Patinho Feio</i> e falar de sentimentos (diferente, sozinho, acolhido).",
                   "Transferir água entre recipientes com cuidado.", "Traço ondulado contínuo."],
        repertorio="<b>Conto:</b> Hans Christian Andersen, <i>O Patinho Feio</i> (1843) — só o começo, em versão da coleção; a história completa está no Volume 2. "
                   "<b>Cantiga:</b> <i>A canoa virou</i> (tradicional). <b>Imagens:</b> John R. Neill (1908), Kate Greenaway (1878), Beatrix Potter (1906). "
                   "<b>Música:</b> Tchaikovsky, <i>O Lago dos Cisnes</i>. <b>Línguas:</b> <i>duck · le canard · anas</i>.",
        materiais="Bacia grande com água; maçã, chave, folha, pedra, colher de metal e rolha; toalha; jarra pequena e dois copos; avental.",
        vida="Transferir água da jarra para o copo; enxugar a mesa; esvaziar a bacia no jardim.",
        etapas=[["Brincar livremente na bacia.", "Começo de <i>O Patinho Feio</i>.", "Ouvir o tema do cisne."],
                ["Flutua ou afunda: testar e separar.", "“Quem é diferente?” nos patinhos.", "Contar os patos de Greenaway."],
                ["Prever antes de soltar o objeto.", "Cantar <i>A canoa virou</i> com o nome dela.", "Desenhar ondas."]],
        indicadores=["Diz “afundou” ou “boiou” depois de soltar o objeto.", "Arrisca um palpite antes de testar.", "Fala de um sentimento do patinho.",
                     "Transfere água sem derramar quase nada.", "Faz linhas onduladas contínuas.", "Canta um trecho da cantiga."],
        interesse="visite um lago ou parque com patos; leve uma lupa para olhar as plantas da margem.",
        dificil="só a bacia de água e a cantiga.",
        alerta="<b>Água e criança pequena:</b> mesmo poucos centímetros de água exigem um adulto ao lado, o tempo todo. Esvazie a bacia logo depois."))

    historia(L, "O Patinho Feio", "Hans Christian Andersen · o começo da história, em versão da coleção", f"""
      {pd("neill_pata", "64mm", "float:right;margin:0 0 3mm 5mm")}
      <p class="capitular" style="margin-top:4mm">Era verão no campo. Perto do lago, uma mamãe pata chocava os seus ovos.</p>
      <p>Um dia, os ovos começaram a fazer <i>craque, craque!</i> — e saíram patinhos amarelinhos:</p>
      <p class="fala">— Piu, piu! Que mundo grande!</p>
      <p>Só o último ovo, o maior de todos, demorava. Até que, <i>craaaque</i>, saiu um patinho grande, cinzento, diferente dos outros.</p>
      <p>Os bichos do terreiro disseram: <i>— Que patinho feio!</i></p>
      <p>Mas a mamãe pata viu o filho nadar e disse:</p>
      <p class="fala">— Ele nada tão bem! É meu filho também.</p>""",
             adulto("conversa sobre sentimentos",
                    "Aqui a história para — o resto (o inverno, a viagem e o cisne) fica para o Volume 2, quando ela tiver mais fôlego para a narrativa longa. "
                    "Pergunte: “como o patinho se sentiu quando disseram que ele era feio?” e “o que a mamãe pata fez?”. Aceite qualquer resposta "
                    "e nomeie o sentimento: triste, sozinho, feliz com a mamãe. Na imagem de John R. Neill, a pata branca está com os patinhos no ninho.",
                    credito_pd("neill_pata")),
             aba="--d-historias")

    poema(L, "A canoa virou", "cantiga tradicional brasileira — com o nome da Marina",
          ["A canoa virou,<br>pois deixaram ela virar;<br>foi por causa da Marina,<br>que não soube remar.",
           "Se eu fosse um peixinho<br>e soubesse nadar,<br>eu tirava a Marina<br>do fundo do mar."],
          pd("greenaway_tina", "118mm"),
          adulto("cantar e balançar",
                 "Sentadas no chão, uma de frente para a outra, de mãos dadas, balancem para a frente e para trás como um barco; em “virou”, caiam "
                 "de ladinho, rindo. Troque o nome a cada vez: o papai, a vovó, o ratinho. Na imagem de Kate Greenaway, crianças navegam numa tina "
                 "pelo rio — conte quantas estão na tina.",
                 credito_pd("greenaway_tina")),
          aba="--d-historias")

    objs = [("maca", "maçã"), ("chave", "chave"), ("folha", "folha"), ("pedra", "pedra"), ("colher", "colher"), ("rolha", "rolha")]
    cards = "".join(f'<div class="carta" style="width:28mm;height:34mm;display:inline-flex;margin:1mm">{img(m, "20mm")}'
                    f'<div class="peq">{n}</div></div>' for m, n in objs)
    c = f"""<div class="miolo">{titulo("Flutua ou afunda?", "uma experiência na bacia", 28)}</div>
    <div style="position:absolute;left:16mm;top:48mm;width:84mm;height:96mm;background:linear-gradient(#ffffff 0 30%, #dbe8f1 30% 100%);border-radius:2mm" class="caixa centro">
      <div style="font-size:16pt;font-weight:600;margin-top:1mm">flutua</div><div class="peq">fica em cima da água</div></div>
    <div style="position:absolute;left:110mm;top:48mm;width:84mm;height:96mm;background:linear-gradient(#ffffff 0 30%, #dbe8f1 30% 100%);border-radius:2mm" class="caixa centro">
      <div style="font-size:16pt;font-weight:600;margin-top:1mm">afunda</div><div class="peq">vai para o fundo</div></div>
    <div class="centro" style="position:absolute;left:0;right:0;top:150mm">{cards}</div>
    <div class="centro peq" style="position:absolute;left:0;right:0;top:190mm">recortar os seis objetos e colar no lado certo depois de testar</div>
    {adulto("prever, testar, registrar",
            "Tenha os seis objetos reais. Antes de soltar cada um na bacia, pergunte: “o que você acha: vai ficar em cima ou ir para o fundo?”. "
            "Depois solte e observe juntas. Só então ela cola o desenho no quadro certo. Resultado esperado: maçã, folha e rolha flutuam; chave, pedra "
            "e colher de metal afundam. Se algo surpreender (a maçã grande flutua!), ótimo: é para isso que se testa. "
            "Não é preciso explicar densidade aos 2 anos — o que importa é palpitar, ver e dizer o que aconteceu.",
            estilo="top:200mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    observacao(L, "Quem mora no lago?", "Beatrix Potter · <i>The Tale of Mr. Jeremy Fisher</i> (1906)", pd("potter_sapo_ninfeia", "108mm"),
               ["Ache o <b>sapo</b>. O que ele está segurando?",
                "As folhas redondas na água são de <b>ninfeia</b>. E a flor branca?",
                "Que outras plantas crescem na beira do lago?",
                "A água está parada ou mexendo?",
                "Que bichos podem morar embaixo da água?"],
               adulto("vocabulário do lago",
                      "Palavras novas: lago, margem, ninfeia (ou vitória-régia, a parente gigante da Amazônia), junco, vara de pescar. "
                      "Se visitarem um lago, levem esta página e procurem as mesmas coisas.",
                      credito_pd("potter_sapo_ninfeia")),
               aba="--d-natureza")

    ondas = ""
    for k, y in enumerate((88, 128, 168, 208)):
        d = f"M 30 {y} " + " ".join(f"Q {30 + 15 * (2 * i + 1)} {y + (-11 if i % 2 == 0 else 11)} {30 + 30 * (i + 1)} {y}" for i in range(5))
        ondas += pontilhado(d) + ponto_inicio(30, y)
    imgs = "".join(img("peixe" if k % 2 == 0 else "peixe_azul", "22mm", f"position:absolute;left:{182 - 11}mm;top:{y - 11}mm")
                   for k, y in enumerate((88, 128, 168, 208)))
    tracado(L, "As ondas do lago", "o peixinho nada, sobe e desce, até chegar do outro lado", ondas, imgs,
            adulto("traço ondulado",
                   "Primeiro, ondas com o braço no ar e com o corpo. Depois, o dedo sobre a linha, do círculo verde até o peixe, dizendo “sobe… desce…”. "
                   "A onda contínua combina a linha e a curva: é um passo depois da linha vertical e do círculo. Não precisa seguir exatamente."),
            aba="--d-memoria")

    passos(L, "Da jarra para o copo", "transferir água sem pressa",
           [(img("jarra", "30mm"), "Segurar a jarra pela alça, com a outra mão embaixo"),
            (img("xicara", "30mm"), "Pôr o copo firme na bandeja"),
            (img("jarra", "30mm", "transform:rotate(-30deg)"), "Inclinar devagar até a água sair"),
            (img("gota", "16mm", "margin:5mm auto 7mm"), "Parar quando chegar na marca"),
            (img("toalha", "30mm"), "Derramou? Enxugar com o pano"),
            (img("bolhas", "28mm"), "Esvaziar e começar de novo")],
           adulto("vida prática",
                  "Use uma bandeja com borda (ela segura o que derramar), uma jarra pequena e leve e um copo transparente com uma linha de fita "
                  "marcando até onde encher — o controle do erro. Mostre uma vez, devagar e em silêncio. Comece com feijões secos em vez de água, "
                  "se preferir. Esta é a mesma habilidade de servir o próprio suco à mesa."),
           aba="--d-vida")

    c = f"""<div class="miolo">{titulo("O tema do cisne", "Piotr Ilitch Tchaikovsky · <i>O Lago dos Cisnes</i> (1877)", 28)}
      <div class="centro" style="margin:8mm 0 4mm">{pd("neill_pata", "62mm")}</div>
      <p class="centro" style="font-size:14pt;font-style:italic;line-height:1.55;margin-top:4mm">O oboé canta, triste e bonito,<br>
      os violinos tremem como a água,<br>e o cisne desliza no lago escuro.</p>
    </div>
    {adulto("escuta e movimento lento",
            "Procure a “cena do lago” (o tema que abre o 2º ato e fecha o 1º, com a melodia do oboé sobre o tremor das cordas); são uns três minutos. "
            "Com um lenço leve em cada mão, dancem devagar como cisnes: braços longos, passos na ponta dos pés. "
            "Pergunte: “essa música é alegre ou triste?” — não há resposta errada; ela pode dizer “bonita”. Ela vai reencontrar o cisne no fim de "
            "<i>O Patinho Feio</i>, no Volume 2. Tchaikovsky (1840–1893) era russo e escreveu músicas para balé — histórias contadas com dança.",
            credito_pd("neill_pata"))}"""
    L.add(c, aba="--d-musica")


# ================================================================== UNIDADE 7

def unidade7(L):
    L.unidade = "Unidade 7 · As estações"
    INICIO[L.unidade] = L.proximo
    guia(L, dict(
        titulo="Unidade 7 · As estações", aba="--d-artes",
        pergunta="Por que as árvores mudam? O que vestimos no calor, na chuva e no frio?",
        duracao="Dois fins de semana · dois encontros · 15 a 25 minutos. Volte a esta unidade em cada troca de estação, ao longo do ano.",
        objetivos=["Nomear as quatro estações e uma marca de cada uma.", "Ordenar quatro cartões de uma árvore ao longo do ano.",
                   "Classificar roupas e objetos por tempo: sol, chuva, frio.", "Ouvir um mito muito curto e repeti-lo com a família.",
                   "Pintar com as cores de uma estação."],
        repertorio="<b>Mito:</b> Deméter e Perséfone, em versão muito simplificada da coleção. <b>Imagens:</b> Kate Greenaway (1878), Randolph Caldecott (1879), "
                   "Beatrix Potter (1903). <b>Música:</b> Vivaldi, <i>O Inverno</i>, 2º movimento (Largo). <b>Línguas:</b> "
                   "<i>spring · le printemps · vēr</i> · <i>winter · l’hiver · hiems</i>.",
        materiais="Guarda-chuva, chapéu, bota de chuva, luvas (de verdade); guache em quatro cores (verde-claro, verde-escuro, laranja, branco); pincel grosso.",
        vida="Escolher entre duas roupas a que serve para o dia; guardar a bota molhada no lugar; pendurar o casaco.",
        etapas=[["Olhar a mesma árvore da rua em meses diferentes.", "As quatro estações na pintura.", "Ouvir o Largo de <i>O Inverno</i>."],
                ["Ordenar as quatro árvores.", "Sol, chuva ou frio: o que vestir?", "Comparar as quatro imagens."],
                ["Recontar Perséfone com dois cartões.", "Pintar a árvore da estação de agora.", "Escolher a estação favorita."]],
        indicadores=["Nomeia ao menos duas estações.", "Diz o que muda na árvore (flor, fruta, folha caindo, galho sem folha).",
                     "Põe duas árvores na ordem certa.", "Associa guarda-chuva à chuva e luva ao frio.", "Pinta escolhendo cores de propósito.",
                     "Reconta o mito em uma ou duas frases."],
        interesse="adote uma árvore da rua e tire uma foto dela por mês; cole no álbum do fim do volume.",
        dificil="só a pintura e a roupa do dia.",
        alerta="<b>Estações no Brasil.</b> Em boa parte do país as estações são menos marcadas do que nos livros europeus: não há neve, e muitas árvores "
               "não perdem as folhas. Diga isso a ela com naturalidade: “nos livros de longe, o inverno tem neve; aqui, o inverno é mais fresquinho”. "
               "Procure os sinais locais: os ipês florindo no fim do inverno, as chuvas de verão, as mangas na primavera e no verão."))

    historia(L, "Por que existe o inverno?", "um mito grego, em versão bem curtinha", f"""
      <div class="centro" style="margin:2mm 0 4mm">{img("arvore_inverno", "52mm", "display:inline-block;margin:0 6mm")}{img("arvore_primavera", "52mm", "display:inline-block;margin:0 6mm")}</div>
      <p class="capitular">Há muito tempo, os gregos contavam a história de Deméter, que cuidava das plantas da terra, e de sua filha, Perséfone.</p>
      <p>Uma parte do ano, Perséfone ia morar num reino lá embaixo, debaixo da terra. Deméter sentia tanta saudade que as plantas paravam de crescer,
      as folhas caíam e fazia frio: era o <b>inverno</b>.</p>
      <p>Quando Perséfone voltava, Deméter ficava tão feliz que as flores abriam e as árvores ficavam verdinhas de novo: era a <b>primavera</b>!</p>""",
             adulto("um mito para explicar o mundo",
                    "Esta é uma versão muito simplificada, só com a saudade e a volta; o mito completo, com Hades, vem anos mais tarde. Explique, com naturalidade, "
                    "que esta é uma história antiga que os gregos contavam para explicar as estações — não é o que acontece de verdade, mas é bonita. "
                    "Use os dois cartões de árvore: “Perséfone foi embora…” (inverno); “Perséfone voltou!” (primavera)."),
             aba="--d-historias")

    quatro = [("primavera", "greenaway_primavera"), ("verão", "greenaway_girassois"), ("outono", "caldecott_outono"), ("inverno", "potter_neve")]
    cel = "".join(f'<div class="estacao">{pd(n, "80mm", "max-height:82mm;object-fit:contain")}<div class="legenda-q" style="font-size:13pt">{e}</div></div>'
                  for e, n in quatro)
    c = f"""<div class="miolo">{titulo("As quatro estações na pintura", "olhar, comparar, escolher", 26)}<div class="grade4">{cel}</div></div>
    {adulto("comparar imagens",
            "<b>Primavera:</b> Kate Greenaway — uma moça lê sob uma árvore em flor. <b>Verão:</b> Greenaway — girassóis altos e uma mãe com o bebê. "
            "<b>Outono:</b> Randolph Caldecott — folhas avermelhadas caindo no bosque, árvores ficando nuas. <b>Inverno:</b> Beatrix Potter — uma rua coberta "
            "de neve e um gato atravessando. Pergunte: “em qual faz frio? em qual tem flor? em qual as folhas caem?”. E por fim: “de qual você gosta mais?”.",
            credito_pd("greenaway_primavera", "greenaway_girassois", "caldecott_outono", "potter_neve"))}"""
    L.add(c, aba="--d-artes")

    sequencia(L, "A árvore durante o ano", "recortar os quatro quadros e pôr em ordem",
              [("primavera", img("arvore_primavera", "62mm")), ("verão", img("arvore_verao", "62mm")),
               ("outono", img("arvore_outono", "62mm")), ("inverno", img("arvore_inverno", "62mm"))],
              adulto("ciclo",
                     "Diferente do dia, o ano não termina: depois do inverno vem a primavera de novo. Mostre isso fazendo um círculo com os quatro cartões na mesa. "
                     "<b>Relacionar:</b> comece pelo par mais fácil (verão, com frutas, e inverno, sem folhas). <b>Criar:</b> “o que vem depois do inverno?”.",
                     estilo="top:226mm;bottom:auto"),
              aba="--d-natureza")

    tempos = [("sol", "sol"), ("guarda_chuva", "chuva"), ("estrela", "frio")]
    colunas = "".join(f'<div style="position:absolute;left:{16 + i * 60}mm;top:48mm;width:56mm;height:104mm" class="caixa centro">'
                      f'<div style="font-size:15pt;font-weight:600;margin-top:1mm">{nome}</div>'
                      f'{img("sol" if nome == "sol" else ("nuvem" if nome == "chuva" else "arvore_inverno"), "26mm" if nome != "chuva" else "40mm", "margin:3mm auto 0;opacity:.55")}</div>'
                      for i, (_, nome) in enumerate(tempos))
    objs = [("chapeu", "chapéu de palha"), ("guarda_chuva", "guarda-chuva"), ("bota", "bota de chuva"), ("luva", "luvas")]
    cards = "".join(f'<div class="carta" style="width:40mm;height:42mm;display:inline-flex;margin:1mm">{img(m, "28mm")}'
                    f'<div class="peq">{n}</div></div>' for m, n in objs)
    c = f"""<div class="miolo">{titulo("O que vestir?", "sol, chuva ou frio", 28)}</div>{colunas}
    <div class="centro" style="position:absolute;left:0;right:0;top:158mm">{cards}</div>
    {adulto("classificar por uso",
            "Recorte as quatro peças e deixe que ela as coloque na coluna certa: chapéu no sol; guarda-chuva e bota na chuva; luvas no frio. "
            "A bota pode ir para a chuva ou para o frio — se ela explicar, aceite. Melhor ainda: faça a mesma brincadeira com as roupas de verdade, "
            "antes de sair de casa. <b>Criar:</b> “e o que a gente veste para ir à praia?”.",
            estilo="top:208mm;bottom:auto")}"""
    L.add(c, aba="--d-vida")

    c = f"""<div class="miolo">{titulo("A chuva lá fora", "Antonio Vivaldi · <i>O Inverno</i> · Concerto em fá menor, RV 297 · 2º movimento, Largo", 26)}
      <div class="centro" style="margin:8mm 0 4mm">{pd("potter_neve", "86mm")}</div>
      <p class="centro" style="font-size:10pt;color:var(--sepia)"><i>Passar al foco i dì quieti e contenti / mentre la pioggia fuor bagna ben cento.</i><br>
      “Passar junto ao fogo dias calmos e contentes, enquanto lá fora a chuva molha todo mundo.” — do soneto que acompanha a partitura.</p>
    </div>
    {adulto("escuta: dentro e fora",
            "Um movimento curto (cerca de dois minutos). Os violinos tocam <i>pizzicato</i> — beliscando as cordas — e fazem a chuva lá fora: "
            "plim, plim, plim. Por cima, um violino solo canta uma melodia tranquila: é quem está aquecido perto do fogo. "
            "Brinquem: com uma das mãos, os dedos fazem a chuva na mesa; com a outra, um carinho lento no braço. "
            "Ela vai reconhecer Vivaldi, o mesmo de <i>A Primavera</i> (Unidade 3).",
            credito_pd("potter_neve"))}"""
    L.add(c, aba="--d-musica")

    c = f"""<div class="miolo">{titulo("Pintar a árvore", "com as cores da estação de hoje", 28)}
      <div class="centro" style="margin-top:4mm">{img("arvore_verao", "150mm", colorir=True)}</div></div>
    {adulto("pintura livre",
            "Guache e pincel grosso; a página toda pode ser pintada. Antes, olhem pela janela: a árvore de hoje tem flor? fruta? folha caindo? "
            "Deixe que ela escolha as cores — não há cor errada, mas pode perguntar “por que você escolheu esta?”. Imprima mais de uma cópia e pinte "
            "uma árvore a cada estação; guarde-as juntas no álbum do fim do volume.")}"""
    L.add(c, aba="--d-artes")

    c = f"""<div class="miolo">{titulo("A minha estação", "desenho, colagem ou foto", 28)}
      <div class="caixa" style="height:150mm;margin-top:6mm"></div>
      <p style="font-size:12pt;margin-top:5mm">A estação de que eu mais gosto é ______________________, porque ________________________________</p>
      <p style="font-size:12pt">__________________________________________________________________________</p></div>
    {adulto("expressão e registro",
            "Escreva você as palavras dela, exatamente como ela disser. Ela pode desenhar, colar folhas secas, flores prensadas ou pedaços de papel colorido. "
            "Data e assinatura (o rabisco dela já é assinatura) no canto. Esta página vai para o “Meu livro do mundo”, nas páginas finais.")}"""
    L.add(c, aba="--d-artes")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo
    for metade, temas in enumerate(([("Eu e meus sentidos", "uma foto dela fazendo bolhas, ou o desenho das bolhas"),
                                     ("Minha casa", "a mesa posta por ela"),
                                     ("O jardim e o pomar", "a maçã aberta, uma flor prensada")],
                                    [("Os animais", "um bicho que ela viu de verdade"),
                                     ("O céu e a água", "a lua da janela, a bacia de água"),
                                     ("As estações", "a árvore da rua, este mês")])):
        quadros = "".join(f'<div class="quadro-album"><div class="caixa" style="height:62mm"></div>'
                          f'<div style="font-size:12pt;font-weight:600;margin-top:1.5mm">{t}</div><div class="peq it">{d}</div></div>'
                          for t, d in temas)
        c = f"""<div class="miolo">{titulo("Meu livro do mundo", "fotos, desenhos e achados do Volume 1" if metade == 0 else "continuação", 28)}{quadros}</div>"""
        L.add(c, aba="--d-artes")

    for metade, unidades in enumerate((UNIDADES[1:5], UNIDADES[5:8])):
        linhas = "".join(f'<tr><td style="width:44mm"><b>{n.split(" · ", 1)[1]}</b><div class="peq">{n.split(" · ")[0]}</div></td>'
                         f'<td style="height:{48 if metade == 0 else 62}mm"></td></tr>' for n, _ in unidades)
        c = f"""<div class="miolo">{titulo("Diário de observação", "para o adulto · datas, falas e descobertas — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Unidade</th><th>O que ela fez, disse e perguntou (com data)</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    import fontes_v1
    por_livro = {}
    for n, (item, pg, *_r) in fontes_v1.ITENS.items():
        por_livro.setdefault(item, []).append(f"n{pg}")
    cred = "".join(f"<li>{fontes_v1.LIVROS[i]} — Internet Archive, <i>{i}</i>, páginas {', '.join(sorted(set(p), key=lambda x: int(x[1:])))}.</li>"
                   for i, p in por_livro.items())
    c = f"""<div class="miolo texto">{titulo("Repertório e créditos", "Volume 1", 26)}
      <h2>Literatura</h2><p style="font-size:9.6pt">Textos originais da coleção: <i>As cinco janelinhas</i>, <i>Cada coisa no seu lugar</i>, <i>A cesta do pomar</i>,
      <i>Quem acordou primeiro?</i>, a versão do começo de <i>O Patinho Feio</i> (H. C. Andersen, 1843) e a versão do mito de Deméter e Perséfone.
      Traduções da coleção: R. L. Stevenson, <i>Rain</i> e <i>The Moon</i> (<i>A Child's Garden of Verses</i>, 1885). Cantigas e parlendas tradicionais:
      <i>O sapo não lava o pé</i>, <i>A canoa virou</i>, <i>Pirulito que bate bate</i>, <i>Sol e chuva</i>, <i>Alecrim dourado</i>.</p>
      <h2>Música</h2><p style="font-size:9.6pt">Saint-Saëns, <i>O Aquário</i> e <i>Galinhas e Galos</i> (<i>O Carnaval dos Animais</i>, 1886) · Vivaldi, <i>A Primavera</i> (1º mov.) e
      <i>O Inverno</i> (2º mov.), <i>As Quatro Estações</i> (1725) · Debussy, <i>Clair de lune</i> (1905) · Tchaikovsky, <i>O Lago dos Cisnes</i> (1877).
      Todas as obras estão em domínio público; as gravações têm direitos próprios: use a que tiver.</p>
      <h2>Ilustrações em domínio público</h2><p style="font-size:9pt">Todas em domínio público no Brasil (ilustradores mortos há mais de 70 anos), reproduzidas de digitalizações do Internet Archive (archive.org), com recorte e ajuste do tom do papel; nenhuma pintura foi retocada.</p><ul style="font-size:8.6pt;line-height:1.35">{cred}</ul>
      <p style="font-size:9pt">Motivos de cartões, jogos e traçados: aquarela digital procedural da coleção. Tipografia: EB Garamond (licença OFL).</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 1</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">o Patinho Feio vira cisne,<br>Cachinhos Dourados visita a casa dos ursos,<br>
      o Coelho Pedro se esconde na horta,<br>e o Lobo… bem, o Lobo também aparece.</p>
      <div style="margin-top:12mm">{img("ratinho", "40mm", "margin:0 auto")}</div>
      <p class="peq" style="margin-top:8mm">Volume 2 · Histórias, memória e imaginação</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

def montar():
    L = Livro(1, "O mundo ao meu redor")
    capa(L)
    rosto(L)
    carta(L)
    como_usar(L)
    n_sum = L.add("", cabecalho=False)    # sumário: preenchido depois
    unidade1(L); unidade2(L); unidade3(L); unidade4(L); unidade5(L); unidade6(L); unidade7(L)
    encerramento(L)
    # agora que as páginas são conhecidas, refaz o sumário
    num, _ = L.paginas[n_sum - 1]
    conteudo = sumario(L, INICIO)
    L.paginas[n_sum - 1] = (num, f'<section class="pagina"><div class="moldura"></div>{conteudo}'
                                 f'<div class="rodape"><span class="num">{num}</span></div></section>')
    return L


def main():
    os.makedirs(SAIDA, exist_ok=True)
    ok = True
    for versao, nome in (("impressao", "volume1-impressao"), ("tela", "volume1-tela")):
        VERSAO["atual"] = versao
        L = montar()
        h = os.path.join(AQUI, f"{nome}.html")
        open(h, "w", encoding="utf-8").write(L.html())
        ok &= gerar_pdf(h, os.path.join(SAIDA, f"{nome}.pdf"))
        print(versao, len(L.paginas), "páginas")
    if not ok:   # geração falhou: não renderizar páginas de inspeção a partir de um PDF antigo
        sys.exit(1)
    insp = os.path.join(SAIDA, "inspecao")
    os.makedirs(insp, exist_ok=True)
    for f in os.listdir(insp):
        os.remove(os.path.join(insp, f))
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume1-tela.pdf"), os.path.join(insp, "p")], check=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
