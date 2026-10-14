"""
VOLUME 2 — HISTÓRIAS, MEMÓRIA E IMAGINAÇÃO
Gera volume2/volume2-impressao.pdf e volume2/volume2-tela.pdf e as páginas de inspeção.
uso: python3 volume2.py
"""
import math
import os
import subprocess
import sys

from livro import (Livro, VERSAO, adulto, arte, cabeca_folha, credito_pd, gerar_pdf, guia, historia, img,
                   lista, marcas_corte, memoria, observacao, passos, pd, poema, ponto_inicio, pontilhado,
                   rodape_folha, sequencia, texto, titulo, tracado)

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume2")

UNIDADES = [
    ("Unidade 1 · O Patinho Feio", "--d-historias"),
    ("Unidade 2 · Cachinhos Dourados e os Três Ursos", "--d-matematica"),
    ("Unidade 3 · Chapeuzinho Vermelho", "--d-historias"),
    ("Unidade 4 · Os Três Porquinhos", "--d-matematica"),
    ("Unidade 5 · O Coelho Pedro", "--d-natureza"),
    ("Unidade 6 · Fábulas: a lebre, a tartaruga, o leão e o rato", "--d-memoria"),
    ("Unidade 7 · Os Músicos de Bremen", "--d-musica"),
    ("Unidade 8 · A Princesa e a Ervilha e histórias do Brasil", "--d-artes"),
]
INICIO = {}


def fig(nome, w, legenda=None, estilo=""):
    """Ilustração de domínio público centrada, com legenda opcional."""
    leg = f'<div class="legenda-q centro">{legenda}</div>' if legenda else ""
    return f'<div style="margin:2mm auto 3mm;{estilo}">{pd(nome, w)}{leg}</div>'


def lado(nome, w, direita=True):
    f = "right" if direita else "left"
    m = "0 0 3mm 5mm" if direita else "0 5mm 3mm 0"
    return pd(nome, w, f"float:{f};clear:both;margin:{m}")


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div>
    </div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 2</div>
      <div style="font-weight:500;font-size:28pt;line-height:1.05;margin:2mm 0">Histórias, memória<br>e imaginação</div>
      <div class="vinheta-sep">❦</div></div>
    <div style="position:absolute;top:128mm;left:0;right:0;text-align:center">
      {pd("brooke_ursos_fim", "58mm", "display:inline-block;margin:0 2mm;vertical-align:top")}
      {pd("crane_chapeu_porta", "50mm", "display:inline-block;margin:0 2mm;vertical-align:top")}
      {pd("potter_familia", "54mm", "display:inline-block;margin:0 2mm;vertical-align:top")}</div>
    <div style="position:absolute;bottom:22mm;left:0;right:0;text-align:center;font-size:10.5pt;font-style:italic;color:var(--sepia);line-height:1.5">
      o patinho · os três ursos · a menina de capuz vermelho · os três porquinhos<br>o coelho Pedro · a lebre e a tartaruga · os músicos · a princesa · o Curupira</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""
    <div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 2</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">Histórias, memória e imaginação</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">As histórias deste livro são da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:14mm auto 0;width:96mm;height:72mm" class="caixa"><div class="peq" style="margin-top:30mm">a história preferida dela, num desenho</div></div>
      <div style="margin-top:8mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div>
    </div>
    {img('ratinho', '28mm', 'position:absolute;right:26mm;bottom:28mm')}"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">O que muda no Volume 2</h1>
      <p>No primeiro volume, a Marina olhou, cheirou, nomeou e separou as coisas do mundo. Agora o centro são as <b>histórias</b>:
      contos de fadas, fábulas, um conto de Andersen, as aquarelas de Beatrix Potter e lendas do Brasil. A pergunta deixa de ser
      “o que é isto?” e passa a ser “o que aconteceu primeiro? e depois? por quê? e se fosse diferente?”.</p>
      <h2>O que ela vai fazer</h2>
      <ul>
        <li><b>Ouvir e recontar.</b> Cada conto aparece em versão curta, para ler em voz alta, com perguntas de narração no pé da página.</li>
        <li><b>Ordenar.</b> Cartões de sequência (quatro cenas) para pôr a história em ordem — primeiro com ajuda, depois sozinha.</li>
        <li><b>Comparar.</b> Grande, médio e pequeno; forte e fraco; rápido e devagar; igual e diferente.</li>
        <li><b>Lembrar.</b> “O que tinha na cesta?”, “o que o Pedro perdeu?”, “qual sumiu?”.</li>
        <li><b>Inventar.</b> Trocar um personagem, mudar o final, contar a história ao ratinho.</li>
      </ul>
      <h2>Lobos, medo e finais</h2>
      <p>A Marina gosta do Lobo, e ele aparece em duas histórias. As versões desta coleção são as tradicionais, suavizadas: o lobo engana,
      sopra e assusta, mas ninguém é devorado — a vovó se esconde no armário e o lobo, cansado, vai embora. Se ela quiser outra versão,
      contem juntas. Medo pequeno, numa história contada no colo, ajuda a criança a pensar sobre o perigo em segurança; se alguma parte
      incomodar, pule-a sem cerimônia.</p>
      <h2>A versão da família</h2>
      <p>Em casa vocês contam <i>Cachinhos Dourados</i> com o Lobo no lugar dos ursos. A Unidade 2 traz a versão tradicional, com as pranchas
      de Leslie Brooke, e uma página só para a versão de vocês: as duas convivem muito bem.</p>
    """)


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Uma história, muitas voltas</h1>
      <table class="tab">
        <tr><th>1ª semana</th><td>Contar a história no colo, mostrando as imagens. Sem perguntas difíceis: só o prazer de ouvir.</td></tr>
        <tr><th>2ª semana</th><td>Contar de novo e parar antes das falas repetidas. Fazer as perguntas de narração do pé da página.</td></tr>
        <tr><th>3ª semana</th><td>Cartões de sequência e atividade da unidade. Ela reconta com os cartões ou com bonecos.</td></tr>
        <tr><th>Sempre</th><td>Deixar que ela peça a mesma história quantas vezes quiser. Errar de propósito (“e o lobo soprou a casa de chocolate!”) e deixar que ela corrija.</td></tr>
      </table>
      <h2>Os cartões de sequência</h2>
      <p>Cada unidade tem uma folha com quatro cenas de 8,6 cm. Recorte, cole em papelão e guarde num envelope com o nome da história.
      Comece com duas cenas (o começo e o fim); quando ela acertar com facilidade, três; depois, quatro. A ordem certa é sempre a da folha.</p>
      <h2>Narração</h2>
      <p>Narrar é contar com as próprias palavras o que se ouviu. Aos 2 ou 3 anos, a narração é uma conversa: você pergunta, ela responde
      com uma palavra ou um gesto, você completa a frase. Não corrija o conteúdo; repita o que ela disse, ampliando. Anote as falas
      mais bonitas no diário do fim do volume — em poucos meses, você vai ver o quanto elas crescem.</p>
      <h2>Impressão</h2>
      <p>Igual ao Volume 1: páginas em papel creme de 90 a 120 g; folhas recortáveis em papel de 180 a 240 g. As folhas recortáveis
      não têm moldura, para não atrapalhar o corte.</p>
      <div class="centro" style="margin-top:4mm">{img("patinho", "26mm", "display:inline-block;margin:0 3mm")}{img("tartaruga", "30mm", "display:inline-block;margin:0 3mm")}{img("ervilha", "28mm", "display:inline-block;margin:0 3mm")}</div>
    """)


def sumario(inicio):
    linhas = []
    for nome, cor in UNIDADES:
        num, tit = nome.split(" · ", 1)
        linhas.append(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{num}</td>'
                      f'<td style="font-size:13pt">{tit}</td><td class="pg">{inicio.get(nome, "")}</td></tr>')
    linhas.append(f'<tr><td></td><td style="font-size:13pt">Encerramento · Meu livro de histórias, diário e repertório</td>'
                  f'<td class="pg">{inicio.get("Encerramento", "")}</td></tr>')
    return f"""<div class="miolo">{titulo("Sumário", "Volume 2 · Histórias, memória e imaginação", 30)}
      <table class="sumario">{''.join(linhas)}</table>
      <div class="centro" style="margin-top:8mm">{pd("neill_cisne", "40mm", "display:inline-block;margin:0 3mm")}
      {pd("rackham_bremen", "30mm", "display:inline-block;margin:0 3mm")}{pd("potter_ceia", "44mm", "display:inline-block;margin:0 3mm")}</div></div>"""


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


# ================================================================== U1 PATINHO FEIO

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · O Patinho Feio", aba="--d-historias",
        pergunta="Quem é diferente? Como alguém se sente quando não é aceito — e quando encontra o seu lugar?",
        duracao="Três fins de semana · dois encontros · 15 a 25 minutos. A história é longa para a idade: conte em duas partes (até a casa da velhinha; depois o inverno e o cisne).",
        objetivos=["Acompanhar uma narrativa em várias partes e lembrar o começo no fim.", "Ordenar quatro cenas: ovo, terreiro, voo, cisne.",
                   "Achar o diferente num grupo e dizer em que ele é diferente.", "Nomear sentimentos: triste, sozinho, com frio, feliz.",
                   "Escutar uma melodia lenta e acompanhá-la com o corpo."],
        repertorio="<b>Conto:</b> Hans Christian Andersen, <i>O Patinho Feio</i> (1843), versão da coleção. <b>Imagens:</b> John R. Neill (1908). "
                   "<b>Música:</b> Saint-Saëns, <i>O Cisne</i> (<i>O Carnaval dos Animais</i>). <b>Línguas:</b> <i>swan · le cygne · cygnus</i>.",
        materiais="Um ovo de verdade (cozido) para olhar; uma pena branca; lenço branco para a dança; cartões de sequência da unidade.",
        vida="Acolher: quando chega uma visita, ela oferece um copo d’água ou mostra onde guardar o casaco.",
        etapas=[["Primeira parte da história.", "Olhar as imagens de Neill: as estações.", "Ouvir <i>O Cisne</i>."],
                ["Ordenar as cenas.", "Qual é diferente?", "Comparar o patinho e o cisne."],
                ["“Como ele se sentiu?”", "Inventar um amigo para o patinho.", "Dançar o cisne com o lenço."]],
        indicadores=["Lembra que o patinho era diferente dos irmãos.", "Ordena duas ou três cenas.", "Aponta o diferente e diz por quê (cor, tamanho).",
                     "Usa uma palavra de sentimento sobre o personagem.", "Diz como a história termina.", "Move-se devagar com a música lenta."],
        interesse="observem patos e cisnes num parque; comparem os filhotes com os adultos.",
        dificil="conte só o começo e o fim, com duas imagens."))

    historia(L, "O Patinho Feio", "Hans Christian Andersen · versão da coleção", f"""
      {lado("neill_ovo", "66mm")}
      <p class="capitular" style="margin-top:4mm">Era verão. Perto do lago, uma mamãe pata chocava seus ovos.</p>
      <p>Um dia — <i>craque, craque!</i> — saíram os patinhos, amarelinhos e fofos.</p>
      <p>Só o último ovo, o maior de todos, demorava. Até que, <i>craaaque</i>, saiu um patinho grande, cinzento e desajeitado.</p>
      <p class="fala">— Que patinho feio! — disseram os outros bichos.</p>
      <p>A mamãe pata levou os filhos para nadar. O patinho cinzento nadava muito bem!</p>
      <p class="fala">— Ele não é feio — disse ela. — É só diferente.</p>""",
             credito_pd("neill_ovo").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'))

    historia(L, None, None, f"""
      {lado("neill_terreiro", "62mm", False)}
      <p style="margin-top:6mm">Mas no terreiro todos implicavam com ele. As galinhas bicavam, o peru estufava o peito:</p>
      <p class="fala">— Glu, glu, glu! Vá embora, patinho feio!</p>
      <p>Tão triste ficou o patinho que, uma noite, saiu voando por cima da cerca.</p>
      {lado("neill_velha", "58mm")}
      <p>Chegou à casinha de uma velhinha que morava com um gato e uma galinha.</p>
      <p class="fala">— Você sabe pôr ovos? — perguntou a galinha.<br>— Sabe ronronar? — perguntou o gato.</p>
      <p>O patinho só sabia nadar. Então foi embora outra vez, sozinho.</p>""",
             adulto("primeira pausa",
                    "Se ela estiver cansada, pare aqui e continue em outro dia. Pergunte: “por que os bichos implicavam com o patinho?” · "
                    "“o que o patinho sabia fazer muito bem?” (nadar). Não é preciso tirar lição; deixe a pergunta no ar.",
                    credito_pd("neill_terreiro", "neill_velha")))

    historia(L, None, None, f"""
      {lado("neill_cisnes_voam", "56mm")}
      <p style="margin-top:6mm">No outono, ele viu passar no céu umas aves brancas, lindas, de pescoço comprido. Como queria ser como elas!</p>
      <p>Veio o inverno. Fez frio, o lago gelou, e o patinho passou dias difíceis.</p>
      {lado("neill_voo", "52mm", False)}
      <p>Mas a primavera voltou. O patinho abriu as asas — e elas estavam grandes e fortes! Voou até um lago onde nadavam as aves brancas.</p>
      <p>Abaixou a cabeça para a água… e viu o seu reflexo. Ele não era mais um patinho cinzento: <b>era um cisne!</b></p>
      <p class="fala">— Nunca sonhei com tanta felicidade quando era o patinho feio — pensou ele.</p>""",
             adulto("narração",
                    "A última frase é quase a de Andersen. Depois de contar: “o que o patinho viu na água?” · “ele era mesmo feio?” · "
                    "mostre de novo a primeira imagem (o ninho) e esta (o cisne): “é o mesmo?”. A história inteira, com mais detalhes, pode ser lida "
                    "a partir dos 4 ou 5 anos.",
                    credito_pd("neill_cisnes_voam", "neill_voo")))

    sequencia(L, "O Patinho Feio · cartões de sequência", "recortar os quatro quadros e pôr em ordem",
              [("o ninho", pd("neill_ovo", "56mm", "max-height:66mm;object-fit:contain")),
               ("o terreiro", pd("neill_terreiro", "56mm", "max-height:66mm;object-fit:contain")),
               ("o voo", pd("neill_voo", "56mm", "max-height:66mm;object-fit:contain")),
               ("o cisne", pd("neill_cisne", "56mm", "max-height:66mm;object-fit:contain"))],
              adulto("ordenar e recontar",
                     "<b>Descobrir:</b> nomeie as quatro cenas. <b>Relacionar:</b> começo e fim primeiro (o ninho e o cisne); depois as quatro. "
                     "<b>Criar:</b> ela segura um cartão e conta “o que aconteceu aqui”. Ordem certa: ninho, terreiro, voo, cisne.",
                     credito_pd("neill_ovo", "neill_cisne"), estilo="top:226mm;bottom:auto"))

    # qual é diferente?
    linhas = ""
    for k, (base, dif, pos) in enumerate((("patinho", "patinho_cinza", 3), ("patinho", "patinho_cinza", 1), ("florzinha_amarela", "florzinha_azul", 2))):
        cel = "".join(img(dif if i == pos else base, "30mm", "display:inline-block;margin:0 3mm" + (";transform:scaleX(-1)" if i % 2 else ""))
                      for i in range(4))
        linhas += f'<div class="caixa centro" style="margin-bottom:5mm;padding:4mm">{cel}</div>'
    c = f"""<div class="miolo">{titulo("Qual é diferente?", "olhe a fileira toda e aponte", 28)}<div style="margin-top:7mm">{linhas}</div></div>
    {adulto("igual e diferente",
            "Em cada fileira, um é diferente. Peça que ela aponte e, se puder, diga em quê: a cor, o tamanho, o jeito. Na última fileira não há "
            "patinho: a ideia de “diferente” vale para tudo. <b>Criar:</b> monte fileiras com objetos da casa (três colheres e um garfo) e "
            "deixe que ela monte uma para você descobrir.")}"""
    L.add(c, aba="--d-memoria")

    quatro = [("triste", "neill_terreiro"), ("sozinho", "neill_velha"), ("com saudade", "neill_cisnes_voam"), ("feliz", "neill_cisne")]
    cel = "".join(f'<div class="estacao">{pd(n, "62mm", "max-height:70mm;object-fit:contain")}<div class="legenda-q" style="font-size:14pt">{e}</div></div>'
                  for e, n in quatro)
    c = f"""<div class="miolo">{titulo("Como ele se sentia?", "olhar as imagens e conversar", 28)}<div class="grade4">{cel}</div></div>
    {adulto("sentimentos",
            "Aponte cada imagem e pergunte “como o patinho está se sentindo aqui?”. As palavras sob as imagens são sugestões: aceite as dela. "
            "Faça a cara de cada sentimento no espelho, juntas. <b>Criar:</b> “quando você se sentiu assim?” — e conte uma vez em que você se sentiu também.",
            credito_pd("neill_terreiro", "neill_velha", "neill_cisnes_voam", "neill_cisne"))}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo">{titulo("O Cisne", "Camille Saint-Saëns · <i>O Carnaval dos Animais</i> (1886)", 28)}
      <div class="centro" style="margin:6mm 0">{pd("neill_cisne", "84mm")}</div>
      <p class="centro" style="font-size:15pt;font-style:italic;line-height:1.55">O violoncelo canta comprido,<br>os pianos fazem a água,<br>
      e o cisne passa, passa, devagar…</p></div>
    {adulto("escuta e movimento",
            "Cerca de três minutos: um violoncelo canta uma melodia longa e lenta sobre ondas de dois pianos. É a única peça do <i>Carnaval</i> "
            "que Saint-Saëns deixou publicar em vida. Com um lenço branco, ela é o cisne: braços compridos, passos bem devagar, sem parar. "
            "Compare com <i>O Aquário</i> (Volume 1): as duas têm água; qual é mais calma?",
            credito_pd("neill_cisne"))}"""
    L.add(c, aba="--d-musica")


# ================================================================== U2 CACHINHOS

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · Cachinhos Dourados e os Três Ursos", aba="--d-matematica",
        pergunta="Grande, médio e pequenino: cada um tem o seu. E se alguém mexe no que é dos outros?",
        duracao="Dois ou três fins de semana · dois encontros · 15 a 25 minutos. Esta é a história preferida para dramatizar com objetos de verdade.",
        objetivos=["Seriação de três: grande, médio, pequeno.", "Correspondência: cada urso com a sua tigela, cadeira e cama.",
                   "Antecipar a fala repetida (“Alguém comeu o meu mingau!”).", "Usar vozes diferentes: grossa, média, fininha.",
                   "Recontar e trocar personagens (a versão da família, com o Lobo)."],
        repertorio="<b>Conto:</b> tradicional inglês (Robert Southey, 1837), versão da coleção. <b>Imagens:</b> L. Leslie Brooke, <i>The Golden Goose Book</i> (1905). "
                   "<b>Música:</b> Brahms, <i>Canção de ninar</i>, op. 49 n.º 4. <b>Línguas:</b> <i>big, small · grand, petit · magnus, parvus</i>.",
        materiais="Três tigelas, três colheres e três almofadas de tamanhos diferentes; três bichinhos de pelúcia (ou o Lobo da família); a folha recortável da unidade.",
        vida="Servir a fruta em tigelas de tamanhos diferentes: “a grande para o papai, a pequena para você”. Arrumar a almofada no lugar.",
        etapas=[["História com as imagens de Brooke.", "Fazer as três vozes.", "Ouvir a canção de ninar."],
                ["Pôr as tigelas em ordem.", "Uma colher para cada tigela.", "De quem é? (cartões)"],
                ["Dramatizar com pelúcias.", "A versão do Lobo.", "Mudar o final."]],
        indicadores=["Diz grande, médio e pequeno apontando.", "Ordena três tigelas reais.", "Faz pelo menos duas vozes diferentes.",
                     "Completa a fala repetida.", "Diz o que Cachinhos fez de errado (mexeu no que não era dela).", "Propõe uma troca na história."],
        interesse="a história dos três cabritinhos (<i>Os Três Cabritinhos Rudes</i>) usa o mesmo grande-médio-pequeno.",
        dificil="só as três tigelas e as três vozes."))

    historia(L, "Cachinhos Dourados e os Três Ursos", "conto tradicional inglês · versão da coleção", f"""
      {lado("brooke_mingau", "70mm")}
      <p class="capitular" style="margin-top:4mm">Numa casinha no bosque moravam três ursos: o Papai Urso, grande; a Mamãe Ursa, média; e o Ursinho, pequenininho.</p>
      <p>Uma manhã, fizeram mingau. Mas o mingau estava quente demais, e os três foram passear enquanto ele esfriava.</p>
      <p>Nisso, chegou uma menina de cabelos dourados. A porta estava aberta… e ela entrou.</p>
      <p>Provou o mingau da tigela grande: <i>— Quente demais!</i><br>Provou o da tigela média: <i>— Frio demais!</i><br>
      Provou o da tigelinha: <i>— Ah… este está bom!</i> E comeu tudinho.</p>""",
             credito_pd("brooke_mingau").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'),
             tam=26)

    historia(L, None, None, f"""
      {lado("brooke_cama", "72mm", False)}
      <p style="margin-top:6mm">Cansada, Cachinhos quis sentar. A cadeira grande era dura demais; a média, mole demais; a cadeirinha… era boa — mas, <i>crac!</i>, quebrou.</p>
      <p>Então ela subiu a escada. A cama grande era alta demais; a média, baixa demais; a caminha… era certinha. E Cachinhos dormiu.</p>
      <p>Os ursos voltaram.</p>
      <p class="fala">— Alguém provou o meu mingau! — disse o Papai Urso, com voz <b>grossa</b>.</p>
      <p class="fala">— Alguém provou o meu mingau! — disse a Mamãe Ursa, com voz <b>média</b>.</p>
      <p class="fala">— Alguém provou o meu mingau… e comeu tudinho! — disse o Ursinho, com voz <b>fininha</b>.</p>""",
             adulto("as três vozes",
                    "O segredo desta história são as vozes: grave e lenta para o Papai Urso, média para a Mamãe Ursa, fininha e rápida para o Ursinho. "
                    "Na segunda leitura, ela faz a voz do Ursinho. Na imagem de Brooke, Cachinhos dorme na caminha — repare no ursinho bordado no lençol.",
                    credito_pd("brooke_cama")))

    historia(L, None, None, f"""
      {lado("brooke_ursos_fim", "74mm")}
      <p style="margin-top:6mm">Os ursos subiram a escada.</p>
      <p class="fala">— Alguém deitou na minha cama! — disse o Papai Urso.<br>— Alguém deitou na minha cama! — disse a Mamãe Ursa.</p>
      <p class="fala">— Alguém deitou na minha cama… e está aqui! — gritou o Ursinho.</p>
      <p>Cachinhos acordou com o grito, viu os três ursos olhando para ela, pulou da cama, saiu pela janela e correu, correu, até em casa.</p>
      <p>E os três ursos nunca mais a viram.</p>""",
             adulto("narração e julgamento",
                    "Perguntas: “o que Cachinhos comeu? onde sentou? onde dormiu?” — três lembranças em ordem. Depois, uma pergunta de pensar: "
                    "“Cachinhos podia ter entrado na casa dos ursos?” e “o que ela podia ter feito?” (bater, esperar, pedir desculpas). Não há uma resposta só.",
                    credito_pd("brooke_ursos_fim")))

    # tigelas em ordem (recortável)
    tamanhos = [("Papai Urso", 56), ("Mamãe Ursa", 42), ("Ursinho", 30)]
    lugares = "".join(f'<td style="vertical-align:bottom;text-align:center;width:33%"><div class="caixa" style="height:{w}mm;width:{w + 8}mm;margin:0 auto"></div>'
                      f'<div style="font-size:12pt;margin-top:1mm">{n}</div></td>' for n, w in tamanhos)
    misturadas = [tamanhos[1], tamanhos[2], tamanhos[0]]
    tig = "".join(f'<td style="vertical-align:bottom;text-align:center"><div class="carta" style="display:inline-flex;width:{w + 4}mm;height:{w * 0.8 + 4}mm">'
                  f'{img("tigela", f"{w}mm")}</div></td>' for _, w in misturadas)
    col = "".join(f'<td style="vertical-align:bottom;text-align:center"><div class="carta" style="display:inline-flex;width:{w * 0.5 + 6}mm;height:{w * 0.75}mm">'
                  f'{img("colher", f"{w * 0.7}mm")}</div></td>' for _, w in [tamanhos[2], tamanhos[0], tamanhos[1]])
    c = f"""{cabeca_folha("Cada urso com a sua tigela", "recortar as tigelas e as colheres · imprimir em papel de 180 g", 12)}
    <table style="position:absolute;left:16mm;right:16mm;top:30mm;width:178mm;border-collapse:collapse"><tr>{lugares}</tr></table>
    <div class="peq centro" style="position:absolute;left:0;right:0;top:104mm">tigelas para recortar</div>
    <table style="position:absolute;left:16mm;top:110mm;width:178mm"><tr>{tig}</tr></table>
    <div class="peq centro" style="position:absolute;left:0;right:0;top:170mm">colheres para recortar</div>
    <table style="position:absolute;left:16mm;top:175mm;width:178mm"><tr>{col}</tr></table>
    {adulto("seriação e correspondência",
            "As tigelas recortadas estão misturadas. <b>Descobrir:</b> “qual é a maior? e a menor?”. <b>Relacionar:</b> ela põe cada tigela no lugar do urso "
            "certo (o quadro grande, o médio, o pequeno) e depois uma colher para cada tigela — a colher grande com a tigela grande. "
            "<b>Criar:</b> faça o mesmo com tigelas de verdade e pelúcias. Se ela trocar a média, pergunte: “será que cabe?” — e deixe que ela confira.",
            estilo="top:228mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    sequencia(L, "Cachinhos Dourados · cartões de sequência", "recortar os quatro quadros e pôr em ordem",
              [("os ursos saem", pd("brooke_mingau", "58mm", "max-height:66mm;object-fit:contain")),
               ("o mingau", pd("brooke_tigelas", "58mm", "max-height:66mm;object-fit:contain")),
               ("a caminha", pd("brooke_cama", "58mm", "max-height:66mm;object-fit:contain")),
               ("os ursos voltam", pd("brooke_ursos_fim", "58mm", "max-height:66mm;object-fit:contain"))],
              adulto("ordenar e recontar",
                     "Ordem: os ursos fazem o mingau e saem · Cachinhos prova o mingau · dorme na caminha · os ursos a encontram. "
                     "Peça que ela conte cada quadro com a voz do personagem.",
                     credito_pd("brooke_mingau", "brooke_tigelas", "brooke_cama", "brooke_ursos_fim"), estilo="top:226mm;bottom:auto"))

    c = f"""<div class="miolo">{titulo("Na nossa casa, quem mora é o Lobo", "a versão da família", 26)}
      <div class="texto" style="margin-top:4mm"><p>Em casa, a Marina conhece esta história com o Lobo no lugar dos ursos. Use esta página para contar a versão de vocês
      e registrar as escolhas dela.</p></div>
      <table class="tab" style="font-size:12pt;margin-top:2mm">
        <tr><td style="width:62mm">Quem mora na casinha?</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>O que tem nas tigelas?</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>O que acontece quando o Lobo chega?</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Como termina?</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
      </table>
      <div class="caixa" style="height:96mm;margin-top:6mm"><div class="peq centro" style="margin-top:2mm">o desenho dela</div></div></div>
    {adulto("criar: trocar personagens",
            "Trocar um personagem e manter a estrutura (três tigelas, três cadeiras, três camas) é um passo grande: mostra que ela entende "
            "como a história é feita. Escreva as respostas dela com as palavras dela. Se o Lobo é um só, quem são o grande, o médio e o pequeno? "
            "Deixe que ela resolva — talvez sejam três lobos, talvez o Lobo e dois amigos.")}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo">{titulo("A canção de ninar", "Johannes Brahms · <i>Wiegenlied</i> (Canção de ninar), op. 49 n.º 4 (1868)", 26)}
      <div class="centro" style="margin:5mm 0">{pd("brooke_camas_ursos", "92mm")}</div>
      <table class="tab" style="font-size:12pt"><tr><th style="width:52mm">A voz</th><th>Quem canta</th></tr>
        <tr><td>bem grave, devagar</td><td>o Papai Urso</td></tr><tr><td>média</td><td>a Mamãe Ursa</td></tr>
        <tr><td>fininha, bem baixinho</td><td>o Ursinho</td></tr></table></div>
    {adulto("escuta e voz",
            "A canção de ninar mais famosa do mundo dura menos de dois minutos. Ouçam uma versão instrumental e balancem um ursinho de pelúcia no colo, "
            "no pulso da música (ela é em três tempos: <i>um</i>-dois-três, <i>um</i>-dois-três). Depois cantarolem a melodia com “lá-lá-lá” em três vozes: "
            "grave como o Papai Urso, média, fininha como o Ursinho. É um primeiro jogo de altura do som: grave e agudo.",
            credito_pd("brooke_camas_ursos"))}"""
    L.add(c, aba="--d-musica")


# ================================================================== U3 CHAPEUZINHO

def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · Chapeuzinho Vermelho", aba="--d-historias",
        pergunta="Por que ouvir os conselhos de quem cuida de nós? Como se reconhece um disfarce?",
        duracao="Dois ou três fins de semana · dois encontros · 15 a 25 minutos.",
        objetivos=["Acompanhar e antecipar o diálogo repetido (“Que olhos grandes você tem!”).", "Nomear partes do rosto e o que fazem.",
                   "Seguir um caminho com o dedo e escolher entre dois caminhos.", "Lembrar o que havia na cesta (memória de 3 a 5 itens).",
                   "Perceber aceleração e crescendo numa música."],
        repertorio="<b>Conto:</b> Charles Perrault (1697) e irmãos Grimm (1812), versão suave da coleção. <b>Imagens:</b> Walter Crane (c. 1875). "
                   "<b>Música:</b> Grieg, <i>Na gruta do Rei da Montanha</i>, de <i>Peer Gynt</i> (1875). <b>Línguas:</b> <i>wolf · le loup · lupus</i>.",
        materiais="Uma cesta com 3 a 5 coisas de verdade (pão, uma fruta, um potinho de mel, uma flor); um lenço vermelho; os cartões da unidade.",
        vida="Levar uma cesta com cuidado até alguém da casa (ou da vizinhança, com o adulto) e entregar dizendo “trouxe para você”.",
        etapas=[["História com as imagens de Crane.", "Rosto no espelho: olhos, orelhas, boca.", "Ouvir Grieg."],
                ["O caminho da floresta.", "O que tinha na cesta?", "Ordenar as cenas."],
                ["Dramatizar o diálogo.", "Inventar outro conselho da mãe.", "A cesta dela: o que levaria?"]],
        indicadores=["Completa “que olhos grandes você tem!”.", "Diz o que a mãe pediu (não sair do caminho).", "Segue o caminho com o dedo do começo ao fim.",
                     "Lembra 3 itens da cesta.", "Percebe que a música fica mais rápida e forte.", "Reconta com os cartões."],
        interesse="compare com a versão dos Grimm (com o caçador) e com a de Perrault (sem caçador), contadas por você — ela pode preferir uma.",
        dificil="só o diálogo dos “olhos grandes”, com o espelho.",
        alerta="<b>Medo.</b> Se o Lobo assustar, deixe que ela seja o Lobo na dramatização: quem faz o papel do assustador costuma perder o medo."))

    historia(L, "Chapeuzinho Vermelho", "conto tradicional · versão suave da coleção", f"""
      {lado("crane_mae", "68mm")}
      <p class="capitular" style="margin-top:4mm">Era uma vez uma menina que usava sempre um capuz vermelho. Por isso todos a chamavam de Chapeuzinho Vermelho.</p>
      <p>Um dia, a mãe lhe deu uma cesta com bolo e mel:</p>
      <p class="fala">— Leve para a vovó, que está doente. Vá pelo caminho e não pare para conversar com ninguém.</p>
      <p>No meio da floresta, apareceu o Lobo.</p>
      <p class="fala">— Aonde você vai, menina?<br>— Vou levar esta cesta para a vovó, que mora do outro lado da floresta.</p>""",
             credito_pd("crane_mae").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'))

    historia(L, None, None, f"""
      {lado("crane_flores", "64mm", False)}
      <p style="margin-top:6mm">O Lobo, espertalhão, disse:</p>
      <p class="fala">— Por que não colhe umas flores para a vovó?</p>
      <p>Chapeuzinho saiu do caminho para colher flores… e o Lobo correu, correu, e chegou primeiro à casa da vovó.</p>
      {lado("crane_vovo_janela", "64mm")}
      <p>Mas a vovó viu o Lobo pela janela! Escondeu-se bem depressa dentro do armário.</p>
      <p>O Lobo vestiu a touca da vovó, deitou na cama e cobriu-se até o nariz.</p>""",
             adulto("prever",
                    "Antes de virar a página, pergunte: “o que você acha que vai acontecer quando a Chapeuzinho chegar?”. Qualquer palpite é bom. "
                    "Nesta versão, a vovó se esconde: ninguém é devorado.",
                    credito_pd("crane_flores", "crane_vovo_janela")))

    historia(L, None, None, f"""
      {lado("crane_lobo_cama", "60mm")}
      <p style="margin-top:6mm">Chapeuzinho chegou e olhou para a cama.</p>
      <p class="fala">— Vovó, que olhos grandes você tem!<br>— São para te ver melhor.</p>
      <p class="fala">— Vovó, que orelhas grandes você tem!<br>— São para te ouvir melhor.</p>
      <p class="fala">— Vovó, que boca grande você tem!<br>— É para te…</p>
      {lado("crane_cacador", "56mm", False)}
      <p>Nesse instante, o lenhador, que passava por ali, abriu a porta. O Lobo pulou da cama e fugiu para a floresta — e nunca mais voltou.</p>
      <p>A vovó saiu do armário, e os três comeram o bolo com mel.</p>""",
             adulto("o diálogo",
                    "Diga as perguntas devagar, apontando nos olhos, nas orelhas e na boca dela. Na terceira leitura, ela faz a Chapeuzinho e você o Lobo; "
                    "depois, troquem. Perguntas: “o que a mãe pediu?” · “a Chapeuzinho saiu do caminho?” · “quem ajudou?”.",
                    credito_pd("crane_lobo_cama", "crane_cacador")))

    # caminho com duas trilhas
    curto = "M 40 230 C 80 200 110 170 105 140 S 140 90 170 70"
    longo = "M 40 230 C 30 180 60 160 50 120 S 20 60 70 50 S 140 40 170 70"
    svg = (f'<path d="{curto}" fill="none" stroke="#e9dcc0" stroke-width="13" stroke-linecap="round"/>'
           f'<path d="{longo}" fill="none" stroke="#e9dcc0" stroke-width="13" stroke-linecap="round"/>'
           + pontilhado(curto) + pontilhado(longo, cor="var(--rosa)") + ponto_inicio(40, 230))
    imgs = (img("cesta", "24mm", "position:absolute;left:20mm;top:232mm") +
            pd("crane_vovo_janela", "40mm", "position:absolute;left:150mm;top:38mm") +
            "".join(img(n, "15mm", f"position:absolute;left:{x}mm;top:{y}mm") for n, x, y in
                    (("florzinha_rosa", 16, 120), ("florzinha_azul", 30, 70), ("florzinha_amarela", 58, 40), ("arvore_verao", 120, 150),
                     ("arvore_verao", 140, 190), ("arvore_primavera", 70, 160))))
    tracado(L, "O caminho da floresta", "da casa da Chapeuzinho até a casa da vovó", svg, imgs,
            adulto("seguir um caminho",
                   "Há dois caminhos: o azul é o caminho curto, que a mãe mandou seguir; o rosa passa pelas flores e é mais comprido. "
                   "Com o dedo, ela leva a cesta da casa (círculo verde) até a vovó, primeiro pelo caminho azul. Pergunte: “qual caminho é mais "
                   "comprido?”. Depois, se ela quiser, com o giz. Brincadeira de corpo: um caminho de fita crepe no chão da sala.",
                   credito_pd("crane_vovo_janela"), estilo="left:62mm"))

    memoria(L, "O que tinha na cesta?", [("maçã", img("maca", "32mm")), ("mel", img("mel", "32mm")), ("uvas", img("uva", "32mm")),
                                        ("flor", img("florzinha_rosa", "28mm")), ("xícara", img("xicara", "32mm")), ("livro", img("livro", "32mm"))],
            [2, 0, 4, 1, 5, 3, 1, 5, 0, 3, 2, 4],
            adulto("memória e “qual sumiu?”",
                   "Além do jogo da memória comum, este conjunto serve para o jogo da cesta: ponha 3 cartas (uma de cada par) numa cesta de verdade, "
                   "mostre, cubra com um pano, tire uma escondido e pergunte “o que sumiu da cesta?”. Aumente para 4 e 5 cartas quando ficar fácil.",
                   estilo="bottom:19mm;top:auto"))

    sequencia(L, "Chapeuzinho Vermelho · cartões de sequência", "recortar os quatro quadros e pôr em ordem",
              [("a mãe e a cesta", pd("crane_mae", "56mm", "max-height:66mm;object-fit:contain")),
               ("o Lobo na floresta", pd("crane_lobo_bosque", "56mm", "max-height:66mm;object-fit:contain")),
               ("que olhos grandes!", pd("crane_lobo_cama", "56mm", "max-height:66mm;object-fit:contain")),
               ("o lenhador chega", pd("crane_cacador", "56mm", "max-height:66mm;object-fit:contain"))],
              adulto("ordenar e recontar",
                     "Ordem: a mãe entrega a cesta · o Lobo encontra a Chapeuzinho · o diálogo na cama · o lenhador chega. "
                     "O segundo cartão é a imagem de Crane do encontro no bosque, que não aparece na história: deixe que ela conte o que vê.",
                     credito_pd("crane_mae", "crane_lobo_bosque", "crane_lobo_cama", "crane_cacador"), estilo="top:226mm;bottom:auto"))

    c = f"""<div class="miolo">{titulo("Os passos na floresta", "Edvard Grieg · <i>Na gruta do Rei da Montanha</i>, de <i>Peer Gynt</i> (1875)", 26)}
      <div class="centro" style="margin:6mm 0">{pd("crane_lobo_bosque", "78mm")}</div>
      <div class="centro" style="font-size:13pt;line-height:1.7">
        <span style="font-size:10pt;letter-spacing:.3em">pé ante pé…</span> &nbsp;→&nbsp; <span style="font-size:13pt;letter-spacing:.15em">mais depressa…</span>
        &nbsp;→&nbsp; <span style="font-size:18pt;font-weight:600">CORRE!</span></div></div>
    {adulto("acelerando e crescendo",
            "Uma melodia curta repete-se muitas vezes, cada vez <b>mais rápida</b> e <b>mais forte</b>, até um final barulhento (cerca de dois minutos e meio). "
            "Andem pela sala na ponta dos pés no começo, cada vez mais depressa, até correr — e parem juntas no último acorde. "
            "É uma música de suspense: brinque de “o Lobo está chegando”, mas deixe que ela decida se quer ser a Chapeuzinho ou o Lobo. "
            "Grieg (1843–1907) era norueguês; a peça foi escrita para uma peça de teatro.",
            credito_pd("crane_lobo_bosque"))}"""
    L.add(c, aba="--d-musica")


# ================================================================== U4 TRÊS PORQUINHOS

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · Os Três Porquinhos", aba="--d-matematica",
        pergunta="Qual casa é mais forte? Por que vale a pena fazer as coisas com cuidado?",
        duracao="Dois ou três fins de semana · dois encontros · 20 a 25 minutos (a experiência do sopro pede espaço).",
        objetivos=["Contar até 3 e associar número e quantidade (1, 2, 3 porquinhos e casas).", "Comparar materiais: leve e pesado, fraco e forte.",
                   "Testar uma ideia: o que o sopro derruba?", "Recitar o refrão com ritmo.", "Ordenar quatro cenas."],
        repertorio="<b>Conto:</b> tradicional inglês (J. O. Halliwell-Phillipps, 1843; Joseph Jacobs, 1890), versão da coleção. "
                   "<b>Imagens:</b> L. Leslie Brooke (1905). <b>Ritmo:</b> o refrão do Lobo, com tambor. <b>Línguas:</b> <i>pig · le cochon · porcus</i>; <i>one, two, three · un, deux, trois · ūnus, duo, trēs</i>.",
        materiais="Palha (ou palitos de picolé), gravetos, blocos de montar; canudo; bolinha de algodão, pena, papel amassado, uma pedrinha; um tambor ou panela.",
        vida="Construir junto: empilhar blocos com cuidado; guardar as peças na caixa ao terminar.",
        etapas=[["História com Brooke.", "Tocar palha, madeira e tijolo (ou blocos).", "O refrão com tambor."],
                ["Palha, madeira ou tijolo?", "Contar 1, 2, 3.", "O que o sopro derruba?"],
                ["Construir três casinhas e soprar.", "Inventar uma quarta casa.", "Mudar o final."]],
        indicadores=["Recita o refrão (ou parte dele).", "Conta 3 objetos tocando cada um.", "Diz qual casa é a mais forte e por quê.",
                     "Prevê se o sopro vai derrubar.", "Ordena as cenas.", "Propõe um material novo para a casa."],
        interesse="visitem uma obra, uma marcenaria ou uma casa de taipa; procurem tijolos, madeira e palha (num chapéu, numa vassoura).",
        dificil="só o refrão e o sopro na palha."))

    historia(L, "Os Três Porquinhos", "conto tradicional inglês · versão da coleção", f"""
      {lado("brooke_porcos_mae", "64mm")}
      <p class="capitular" style="margin-top:4mm">Era uma vez uma mamãe porca que tinha três porquinhos. Quando eles cresceram, ela disse:</p>
      <p class="fala">— Agora cada um vai construir a sua casa.</p>
      <p>O primeiro porquinho fez uma casa de <b>palha</b>, bem depressa, e foi brincar.</p>
      <p>O segundo fez uma casa de <b>madeira</b>, um pouco mais devagar.</p>
      <p>O terceiro fez uma casa de <b>tijolos</b>, devagarinho, com muito cuidado, tijolo por tijolo.</p>""",
             credito_pd("brooke_porcos_mae").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'))

    historia(L, None, None, f"""
      {lado("brooke_lobo_palha", "60mm", False)}
      <p style="margin-top:6mm">Um dia, o Lobo bateu na casa de palha:</p>
      <p class="fala">— Porquinho, porquinho, deixa eu entrar!<br>— Não, não, pelos pelinhos do meu queixinho!<br>
      — Então eu vou soprar, e vou bufar, e a sua casa vou derrubar!</p>
      <p>E soprou, e bufou, e a casa de palha voou! O porquinho correu para a casa de madeira do irmão.</p>
      <p>O Lobo soprou, e bufou… e a casa de madeira caiu! Os dois porquinhos correram para a casa de tijolos.</p>""",
             adulto("o refrão",
                    "Diga o refrão com ritmo, batendo nas pernas: <b>Por</b>-qui-nho, <b>por</b>-qui-nho, <b>dei</b>-xa eu en-<b>trar</b>! Na segunda vez, ela "
                    "responde “Não, não!”. Sopre de verdade na hora de soprar: ela vai querer soprar também.",
                    credito_pd("brooke_lobo_palha")))

    historia(L, None, None, f"""
      {lado("brooke_tijolos", "62mm")}
      <p style="margin-top:6mm">O Lobo chegou à casa de tijolos.</p>
      <p class="fala">— Porquinho, porquinho, deixa eu entrar!<br>— Não, não, pelos pelinhos do meu queixinho!</p>
      <p>E o Lobo soprou, e bufou, e soprou, e bufou… e a casa não caiu.</p>
      <p>Soprou tanto que ficou sem fôlego, sentou no chão, cansado, e foi embora pela estrada, resmungando.</p>
      {lado("brooke_porco_casa", "52mm", False)}
      <p>E os três porquinhos fizeram uma festa na casa de tijolos.</p>""",
             adulto("narração",
                    "Perguntas: “de que era a primeira casa? e a segunda? e a terceira?” · “qual casa o Lobo não conseguiu derrubar? por quê?”. "
                    "Na versão antiga inglesa, o Lobo tenta outros truques e termina mal; esta coleção usa um final suave. Brooke pintou o terceiro porquinho "
                    "assentando os tijolos com uma colher de pedreiro.",
                    credito_pd("brooke_tijolos", "brooke_porco_casa")))

    mats = [("palha", "palha", "leve · o sopro leva"), ("madeira", "madeira", "mais pesada"), ("tijolo", "tijolos", "pesado e forte")]
    cols = "".join(f'<div class="caixa centro" style="display:inline-block;width:54mm;margin:0 2mm;padding:3mm;vertical-align:top">'
                   f'{img(m, "40mm", "margin:0 auto")}<div style="font-size:15pt;font-weight:600">{n}</div><div class="peq it">{d}</div>'
                   f'</div>' for n, m, d in mats)
    contas = ""
    for k in range(1, 4):
        contas += (f'<div style="display:flex;align-items:center;gap:4mm;margin:2mm 0"><div style="font-size:30pt;width:16mm;text-align:center;color:var(--rosa)">{k}</div>'
                   + "".join(pd("brooke_porco_saco", "22mm", "display:inline-block") for _ in range(k)) + "</div>")
    c = f"""<div class="miolo">{titulo("Palha, madeira, tijolo · um, dois, três", "comparar e contar", 26)}
      <div class="centro" style="margin-top:5mm">{cols}</div>
      <div style="margin:6mm 0 0 18mm">{contas}</div></div>
    {adulto("comparar materiais e contar",
            "<b>Comparar:</b> se puder, tenha palha (ou palitos), gravetos e um tijolo de verdade. Ela segura cada um: “qual é mais leve? qual é mais pesado?”. "
            "<b>Contar:</b> toque cada porquinho dizendo um número por toque — 1; 1, 2; 1, 2, 3. O número grande diz quantos há. "
            "Em inglês: <i>one, two, three</i>; em francês: <i>un, deux, trois</i>.",
            credito_pd("brooke_porco_saco"))}"""
    L.add(c, aba="--d-matematica")

    objs = [("pena", "pena"), ("bolhas", "algodão"), ("folha", "folha seca"), ("pedra", "pedrinha"), ("colher", "colher"), ("palha", "palitos")]
    cards = "".join(f'<div class="carta" style="width:28mm;height:34mm;display:inline-flex;margin:1mm">{img(m, "20mm")}'
                    f'<div class="peq">{n}</div></div>' for m, n in objs)
    c = f"""<div class="miolo">{titulo("O sopro do Lobo", "o que o sopro consegue mover?", 28)}</div>
    <div style="position:absolute;left:16mm;top:48mm;width:84mm;height:90mm" class="caixa centro">
      <div style="font-size:16pt;font-weight:600;margin-top:1mm">voou!</div><div class="peq">o sopro levou</div></div>
    <div style="position:absolute;left:110mm;top:48mm;width:84mm;height:90mm" class="caixa centro">
      <div style="font-size:16pt;font-weight:600;margin-top:1mm">não saiu do lugar</div><div class="peq">pesado demais para o sopro</div></div>
    <div class="centro" style="position:absolute;left:0;right:0;top:146mm">{cards}</div>
    <div class="centro peq" style="position:absolute;left:0;right:0;top:186mm">recortar os seis objetos e colar no lado certo depois de testar</div>
    {adulto("prever e testar",
            "Ponha cada objeto real na mesa. Antes, ela adivinha: “o sopro vai levar?”. Depois ela sopra — com a boca ou com um canudo — e cola o desenho "
            "no lado certo. Esperado: pena, algodão e folha seca voam; pedrinha e colher não saem do lugar; os palitos dependem de quantos são. "
            "<b>Criar:</b> construam três casinhas (palitos soltos, gravetos amarrados, blocos) e soprem com um secador de cabelo na potência fria, "
            "com o adulto segurando. Qual cai primeiro?",
            estilo="top:198mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    sequencia(L, "Os Três Porquinhos · cartões de sequência", "recortar os quatro quadros e pôr em ordem",
              [("a mamãe e os filhotes", pd("brooke_porcos_mae", "58mm", "max-height:66mm;object-fit:contain")),
               ("a casa de palha voa", pd("brooke_lobo_palha", "58mm", "max-height:66mm;object-fit:contain")),
               ("a casa de tijolos", pd("brooke_tijolos", "58mm", "max-height:66mm;object-fit:contain")),
               ("a festa", pd("brooke_porco_casa", "58mm", "max-height:66mm;object-fit:contain"))],
              adulto("ordenar e recontar",
                     "Ordem: a mamãe porca e os filhotes · o Lobo derruba a casa de palha · o porquinho constrói a casa de tijolos · a festa em casa. "
                     "Peça que ela diga o refrão em cada cartão onde aparece o Lobo.",
                     credito_pd("brooke_porcos_mae", "brooke_lobo_palha", "brooke_tijolos", "brooke_porco_casa"), estilo="top:226mm;bottom:auto"))

    c = f"""<div class="miolo">{titulo("O tambor do Lobo", "ritmo das palavras", 28)}
      <div class="centro" style="margin:6mm 0">{img("tambor", "52mm")}</div>
      <table class="tab" style="font-size:15pt">
        <tr><td><b>POR</b> · qui · nho · <b>POR</b> · qui · nho</td><td style="font-size:20pt;letter-spacing:.15em;color:var(--d-musica)">● · · ● · ·</td></tr>
        <tr><td><b>DEI</b> · xa · eu · en · <b>TRAR</b>!</td><td style="font-size:20pt;letter-spacing:.15em;color:var(--d-musica)">● · · · ●</td></tr>
        <tr><td><b>NÃO</b>, <b>NÃO</b>, <b>NÃO</b>!</td><td style="font-size:20pt;letter-spacing:.15em;color:var(--d-musica)">● ● ●</td></tr>
        <tr><td><b>SO</b> · prar · e · <b>BU</b> · far</td><td style="font-size:20pt;letter-spacing:.15em;color:var(--d-musica)">● · · ● ·</td></tr>
      </table></div>
    {adulto("sílabas e pulso",
            "O ponto grande é uma batida forte no tambor (ou na panela); os pontinhos são as sílabas fracas, que se dizem sem bater. "
            "Dizer palavras batendo as sílabas fortes é um começo de consciência fonológica (perceber que as palavras têm pedaços) e de ritmo musical. "
            "<b>Criar:</b> batam o nome dela: <b>Ma</b>-ri-na; e o de cada pessoa da família. Quantas batidas tem cada nome?")}"""
    L.add(c, aba="--d-musica")


# ================================================================== U5 COELHO PEDRO

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · O Coelho Pedro", aba="--d-natureza",
        pergunta="O que acontece quando a gente desobedece? Onde fica cada coisa na horta?",
        duracao="Dois ou três fins de semana · dois encontros · 15 a 25 minutos. A história tem quatro páginas: conte em duas partes.",
        objetivos=["Ouvir um livro “de verdade”: o texto e as aquarelas de Beatrix Potter (1902).", "Relações espaciais: dentro, embaixo, atrás, perto, longe.",
                   "Seguir um percurso num mapa simples.", "Lembrar o que o Pedro perdeu (inferência e memória).",
                   "Observar uma aquarela: cores, pinceladas, o que é de verdade e o que é de história."],
        repertorio="<b>Conto:</b> Beatrix Potter, <i>The Tale of Peter Rabbit</i> (1902), tradução e adaptação da coleção. "
                   "<b>Imagens:</b> as aquarelas originais (edição Warne, 1921). <b>Línguas:</b> <i>rabbit · le lapin · cunīculus</i>; <i>garden · le jardin · hortus</i>.",
        materiais="Uma alface, rabanetes e uma vagem de verdade; um regador; aquarela escolar e pincel; papel grosso.",
        vida="Regar uma planta com o regador; lavar folhas de alface; ajudar a pôr os sapatos no lugar ao chegar em casa.",
        etapas=[["História, em duas partes.", "Ver e cheirar alface, rabanete e vagem.", "Achar os animais nas imagens."],
                ["Mapa da horta: onde o Pedro passou?", "O que ele perdeu?", "Dentro, embaixo, atrás."],
                ["Pintar com aguada, como Potter.", "Contar o que a mãe disse ao Pedro.", "Inventar outro esconderijo."]],
        indicadores=["Reconta a desobediência e a fuga.", "Usa “embaixo”, “dentro”, “atrás” para dizer onde o Pedro estava.", "Percorre o mapa com o dedo.",
                     "Lembra que o Pedro perdeu os sapatos e o casaco.", "Diz uma diferença entre um coelho de verdade e o Pedro.", "Mistura água e tinta com intenção."],
        interesse="leia as outras histórias de Potter em domínio público (<i>Benjamin Coelho</i>, <i>Jeremy Fisher</i>); visite uma horta.",
        dificil="só a primeira parte e a horta de verdade."))

    historia(L, "O Coelho Pedro", "Beatrix Potter (1902) · tradução e adaptação da coleção", f"""
      {lado("potter_familia", "60mm")}
      <p class="capitular" style="margin-top:4mm">Era uma vez quatro coelhinhos: Flopsy, Mopsy, Rabo-de-Algodão e Pedro. Moravam com a mãe numa toca embaixo de um pinheiro muito grande.</p>
      <p class="fala">— Podem ir para o campo ou pela trilha — disse a Mamãe Coelha —, mas não entrem na horta do Sr. McGregor.</p>
      <p>Flopsy, Mopsy e Rabo-de-Algodão, que eram coelhinhas bem-comportadas, foram colher amoras.</p>
      <p>Mas Pedro, que era muito travesso, correu direto para a horta do Sr. McGregor… e se espremeu por baixo da porteira!</p>""",
             credito_pd("potter_familia").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'),
             aba="--d-historias", tam=28)

    historia(L, None, None, f"""
      {lado("potter_rabanetes", "58mm", False)}
      <p style="margin-top:6mm">Primeiro ele comeu alface, depois vagem, depois rabanetes. E então, sentindo-se meio enjoado, foi procurar salsinha.</p>
      <p>Mas, virando a esquina de um canteiro, quem ele encontrou? O Sr. McGregor!</p>
      {lado("potter_mcgregor", "58mm")}
      <p>O Sr. McGregor correu atrás dele, gritando: <i>— Pega ladrão!</i></p>
      <p>Pedro ficou tão assustado que correu pela horta inteira e esqueceu o caminho de volta. Perdeu um sapato entre os repolhos e o outro entre as batatas.</p>""",
             adulto("primeira pausa",
                    "Pergunte: “o que a mamãe disse?” · “o Pedro obedeceu?” · “o que ele comeu?”. Mostre uma alface e um rabanete de verdade. "
                    "Repare com ela no passarinho (um pisco-de-peito-ruivo) que aparece em várias imagens: Potter gostava de pôr bichinhos observando a cena.",
                    credito_pd("potter_rabanetes", "potter_mcgregor")), aba="--d-historias")

    historia(L, None, None, f"""
      {lado("potter_rede", "58mm")}
      <p style="margin-top:6mm">Sem os sapatos, Pedro correu mais depressa — mas os botões do casaco azul se enroscaram numa rede de groselheira!</p>
      <p>Uns pardais amigos pediram: <i>— Coragem, Pedro, força!</i> E Pedro se soltou, deixando o casaco para trás.</p>
      {lado("potter_regador", "50mm", False)}
      <p>Correu para o galpão e pulou dentro de um regador. Seria um ótimo esconderijo… se o regador não estivesse cheio de água!</p>
      <p class="fala">— Atchim! — espirrou Pedro. E o Sr. McGregor quase o pegou.</p>""",
             adulto("onde ele está?",
                    "Use as palavras de lugar: Pedro está <b>embaixo</b> da rede, <b>dentro</b> do regador, <b>atrás</b> do vaso. Depois, brinque com um bichinho de "
                    "pelúcia: “ponha o coelho dentro da caixa… embaixo da mesa… atrás da cortina”.",
                    credito_pd("potter_rede", "potter_regador")), aba="--d-historias")

    historia(L, None, None, f"""
      {lado("potter_portao", "56mm", False)}
      <p style="margin-top:6mm">Pedro pulou pela janela, passou por uma ratinha carregando uma ervilha e por uma gata branca olhando os peixes do lago.</p>
      <p>Até que, de cima de um carrinho de mão, ele viu — o portão! Correu com todas as forças, passou por baixo e chegou, enfim, à toca.</p>
      {lado("potter_mae_cha", "58mm")}
      <p>Estava tão cansado que se jogou no chão. A mãe, que cozinhava, não perguntou nada sobre o casaco nem sobre os sapatos.</p>
      <p>Naquela noite, Pedro foi para a cama com uma colherada de chá de camomila. E Flopsy, Mopsy e Rabo-de-Algodão jantaram pão, leite e amoras.</p>""",
             adulto("narração e consequência",
                    "Perguntas: “como o Pedro voltou para casa?” · “o que ele perdeu?” · “por que ele tomou chá de camomila e as irmãs comeram amoras?”. "
                    "Deixe que ela chegue sozinha à ideia de consequência; não é preciso dizer a moral.",
                    credito_pd("potter_portao", "potter_mae_cha")), aba="--d-historias")

    # mapa da horta
    lugares = [("toca", 30, 40, "potter_familia"), ("porteira", 95, 40, "potter_pedro_porteira"), ("rabanetes", 150, 70, "potter_rabanetes"),
               ("galpão e regador", 150, 140, "potter_regador"), ("lago", 85, 150, "potter_gata_lago"), ("portão", 35, 135, "potter_portao")]
    pts = [(x + 20, y + 22) for _, x, y, _ in lugares] + [(50, 62)]
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    cel = "".join(f'<div style="position:absolute;left:{x}mm;top:{y + 16}mm;width:40mm;text-align:center">'
                  f'{pd(n, "30mm", "max-height:30mm;object-fit:contain;margin:0 auto")}'
                  f'<div style="font-size:11pt;font-weight:600;margin-top:1mm"><span style="color:var(--rosa)">{i + 1}</span> · {nome}</div></div>'
                  for i, (nome, x, y, n) in enumerate(lugares))
    svg = f'<path d="M {" L ".join(f"{x} {y + 16}" for x, y in pts)}" fill="none" stroke="var(--rosa)" stroke-width="1" stroke-dasharray="2 2"/>'
    c = f"""<div class="miolo">{titulo("O caminho do Pedro", "um mapa da horta do Sr. McGregor", 26)}</div>
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>{cel}
    {adulto("mapa e relações espaciais",
            "Com o dedo, ela faz o caminho do Pedro seguindo os números: da toca à porteira, aos rabanetes, ao galpão do regador, ao lago e ao portão — e de volta à toca. "
            "Perguntas: “o que fica perto do lago?” · “qual lugar é mais longe da toca?”. <b>Criar:</b> desenhe com ela o mapa da casa de vocês: "
            "onde fica a cama, a mesa, a porta.",
            credito_pd("potter_familia", "potter_pedro_porteira", "potter_rabanetes", "potter_regador", "potter_gata_lago", "potter_portao"))}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Como Beatrix Potter pintava", "olhar de perto uma aquarela", 26)}
      <div class="centro" style="margin:5mm 0">{pd("potter_gata_lago", "120mm")}</div>
      <ol class="perguntas">
        <li>Ache a <b>gata branca</b>. Ela está olhando o quê?</li>
        <li>Ache o <b>Pedro</b>, pequenino, lá atrás.</li>
        <li>Que cores há na água? E nas folhas?</li>
        <li>A gata é de verdade ou de história? E o Pedro, de casaco?</li></ol></div>
    {adulto("apreciação e pintura",
            "Beatrix Potter (1866–1943) desenhava coelhos, ratos e plantas de verdade, com muita atenção, e depois pintava com aquarela em camadas leves: "
            "por isso o branco do papel aparece e as cores parecem transparentes. <b>Pintar como Potter:</b> molhe o papel com um pincel só com água e depois "
            "toque com tinta verde ou azul — a cor se espalha sozinha. Ela vai adorar ver a mancha crescer. Guarde a pintura no álbum do fim do volume.",
            credito_pd("potter_gata_lago"))}"""
    L.add(c, aba="--d-artes")

    sequencia(L, "O Coelho Pedro · cartões de sequência", "recortar os quatro quadros e pôr em ordem",
              [("a mamãe avisa", pd("potter_familia", "60mm", "max-height:66mm;object-fit:contain")),
               ("na horta", pd("potter_rabanetes", "60mm", "max-height:66mm;object-fit:contain")),
               ("preso na rede", pd("potter_rede", "60mm", "max-height:66mm;object-fit:contain")),
               ("chá de camomila", pd("potter_mae_cha", "60mm", "max-height:66mm;object-fit:contain"))],
              adulto("ordenar e recontar",
                     "Ordem: a mamãe avisa · Pedro come na horta · Pedro preso na rede · em casa, com o chá. <b>Lembrar:</b> com os cartões na mesa, pergunte "
                     "“em qual cartão o Pedro ainda tem o casaco? e em qual já perdeu?”.",
                     credito_pd("potter_familia", "potter_rabanetes", "potter_rede", "potter_mae_cha"), estilo="top:226mm;bottom:auto"))


# ================================================================== U6 FÁBULAS

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · Fábulas: a lebre, a tartaruga, o leão e o rato", aba="--d-memoria",
        pergunta="Quem chega primeiro: o rápido ou o que não desiste? Um pequeno pode ajudar um grande?",
        duracao="Dois fins de semana · uma fábula por fim de semana · 15 a 20 minutos.",
        objetivos=["Ouvir uma fábula e dizer o que aconteceu no fim.", "Comparar rápido e devagar; grande e pequeno.",
                   "Ordenar posições: primeiro, segundo, último.", "Dramatizar com o corpo.", "Perceber andamento na música (rápido, lento)."],
        repertorio="<b>Fábulas:</b> Esopo, <i>A Lebre e a Tartaruga</i> e <i>O Leão e o Rato</i>, versões da coleção. <b>Imagem:</b> Arthur Rackham (1912). "
                   "<b>Música:</b> Saint-Saëns, <i>Tartarugas</i> e <i>Hemíones</i> (<i>O Carnaval dos Animais</i>). <b>Línguas:</b> <i>fast, slow · vite, lentement · celer, lentus</i>.",
        materiais="Um fio de lã ou barbante (a rede do leão); dois bichinhos (lebre ou coelho e tartaruga); fita para marcar a chegada no chão.",
        vida="Ajudar alguém maior: segurar a porta, levar um objeto leve; agradecer quando alguém ajuda.",
        etapas=[["Ouvir a fábula da corrida.", "Andar rápido e devagar.", "Ouvir as duas músicas."],
                ["Quem é rápido? Quem é devagar?", "Primeiro, segundo, último.", "Grande e pequeno: o leão e o rato."],
                ["Dramatizar a corrida.", "O rato rói a rede (com barbante).", "Inventar outra corrida."]],
        indicadores=["Diz quem ganhou a corrida.", "Separa animais rápidos e lentos.", "Usa “primeiro” e “último”.",
                     "Diz como o rato ajudou o leão.", "Move-se no andamento da música.", "Dramatiza uma parte."],
        interesse="conte outras fábulas de Esopo: <i>A raposa e as uvas</i>, <i>O vento e o sol</i>.",
        dificil="só a corrida dramatizada."))

    historia(L, "A Lebre e a Tartaruga", "fábula de Esopo · versão da coleção", f"""
      {lado("rackham_lebre", "64mm")}
      <p class="capitular" style="margin-top:4mm">A lebre vivia caçoando da tartaruga:</p>
      <p class="fala">— Como você é lenta! Aposto que eu ganho de você numa corrida.</p>
      <p class="fala">— Então vamos correr — respondeu a tartaruga.</p>
      <p>Foi dada a largada. A lebre disparou e logo sumiu na estrada. Lá na frente, olhou para trás e não viu ninguém.</p>
      <p class="fala">— Vou tirar uma soneca — pensou. — Ela vai demorar muito.</p>""",
             credito_pd("rackham_lebre").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'),
             aba="--d-historias")

    historia(L, None, None, f"""
      <div class="centro" style="margin:8mm 0 4mm">{img("tartaruga", "88mm")}</div>
      <p>Enquanto a lebre dormia, a tartaruga ia passo a passo, passo a passo, sem parar nem um pouquinho.</p>
      <p>Passou pela lebre adormecida… e continuou.</p>
      <p>Quando a lebre acordou, deu um pulo e correu o mais que pôde. Mas era tarde: a tartaruga já tinha cruzado a linha de chegada!</p>
      <p class="fala">— Devagar e sempre se chega lá — disse a tartaruga.</p>""",
             adulto("fábula e moral",
                    "As fábulas terminam com uma frase que ensina — a <b>moral</b>. Pergunte primeiro “quem ganhou?” e só depois “por quê?”. "
                    "Na prancha de Rackham, a tartaruga chega sob os aplausos de outros bichos, e a lebre, atrasada, vem lá atrás. "
                    "<b>Dramatizar:</b> marque a chegada com fita no chão; ela é a tartaruga, você a lebre que dorme no meio do caminho."),
             aba="--d-historias")

    historia(L, "O Leão e o Rato", "fábula de Esopo · versão da coleção", f"""
      <div class="centro" style="margin:2mm 0 3mm">{img("ratinho", "44mm", "display:inline-block;margin:0 6mm")}{img("rede", "50mm", "display:inline-block;margin:0 6mm")}</div>
      <p class="capitular">Um leão dormia na sombra quando um ratinho passou correndo por cima do seu nariz. O leão acordou e prendeu o ratinho com a pata.</p>
      <p class="fala">— Por favor, me solte! — pediu o ratinho. — Um dia eu posso ajudar você.</p>
      <p>O leão riu — como um bichinho tão pequeno poderia ajudar o rei dos animais? —, mas soltou o ratinho.</p>
      <p>Dias depois, o leão caiu numa rede de caçadores. Rugiu, puxou, e não conseguia sair. O ratinho ouviu o rugido, veio correndo e roeu as cordas, uma por uma, até o leão ficar livre.</p>
      <p class="fala">— Viu? — disse o ratinho. — Até um pequeno pode ajudar um grande.</p>""",
             adulto("grande e pequeno",
                    "Brincadeira: amarre frouxamente os pulsos de um bichinho grande com barbante e deixe que ela, como o ratinho, solte nó por nó. "
                    "Perguntas: “quem era grande? quem era pequeno?” · “quem ajudou quem?” · “você já ajudou alguém maior que você?”."),
             aba="--d-historias")

    cards = [("tartaruga", "tartaruga", "devagar"), ("patinho", "patinho", "devagar"), ("peixe", "peixe", "rápido"),
             ("pd:cartao_cavalo", "cavalo", "rápido"), ("ratinho", "ratinho", "rápido"), ("pd:potter_benjamin", "coelho", "rápido")]
    def figura(m):
        return pd(m[3:], "26mm", "max-height:28mm;object-fit:contain") if m.startswith("pd:") else img(m, "26mm")
    cel = "".join(f'<div class="carta" style="width:30mm;height:38mm;display:inline-flex;margin:1mm">{figura(m)}<div class="peq">{n}</div></div>'
                  for m, n, _ in cards)
    c = f"""<div class="miolo">{titulo("Rápido ou devagar?", "e quem chega primeiro?", 28)}</div>
    <div style="position:absolute;left:16mm;top:46mm;width:84mm;height:84mm" class="caixa centro"><div style="font-size:16pt;font-weight:600">rápido</div></div>
    <div style="position:absolute;left:110mm;top:46mm;width:84mm;height:84mm" class="caixa centro"><div style="font-size:16pt;font-weight:600">devagar</div></div>
    <div class="centro" style="position:absolute;left:0;right:0;top:136mm">{cel}</div>
    <div style="position:absolute;left:18mm;right:18mm;top:182mm;display:flex;justify-content:space-around;align-items:flex-end">
      <div class="centro"><div style="font-size:22pt;color:var(--rosa)">1º</div><div class="caixa" style="width:36mm;height:22mm"></div><div class="peq">primeiro</div></div>
      <div class="centro"><div style="font-size:22pt;color:var(--rosa)">2º</div><div class="caixa" style="width:36mm;height:16mm"></div><div class="peq">segundo</div></div>
      <div class="centro"><div style="font-size:22pt;color:var(--rosa)">último</div><div class="caixa" style="width:36mm;height:10mm"></div><div class="peq">último</div></div></div>
    {adulto("classificar e ordenar",
            "<b>Separar:</b> recorte os seis animais; ela decide quem é rápido e quem é devagar (o patinho anda devagar, mas nada depressa — aceite se ela explicar). "
            "<b>Ordenar:</b> faça uma corrida com três bichinhos de brinquedo e ponha-os no pódio: primeiro, segundo, último. "
            "Na fábula, quem chegou primeiro foi a tartaruga — a mais lenta!",
            credito_pd("cartao_cavalo", "potter_benjamin"), estilo="top:224mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Rápido e devagar na música", "Camille Saint-Saëns · <i>O Carnaval dos Animais</i> (1886)", 26)}
      <div style="display:flex;gap:8mm;margin-top:8mm;align-items:center">
        <div class="caixa centro" style="flex:1;padding:4mm">{img("tartaruga", "52mm", "margin:0 auto")}
          <div style="font-size:15pt;font-weight:600">Tartarugas</div><div class="peq it">bem devagar</div>
          <p style="font-size:10.5pt;margin-top:2mm">Saint-Saëns pegou o cancã, uma dança rapidíssima, e mandou tocar muito, muito devagar.</p></div>
        <div class="caixa centro" style="flex:1;padding:4mm">{pd("cartao_cavalo", "44mm", "margin:0 auto")}
          <div style="font-size:15pt;font-weight:600">Hemíones</div><div class="peq it">depressa, depressa!</div>
          <p style="font-size:10.5pt;margin-top:2mm">Hemíones são burros selvagens da Ásia, que correm muito: dois pianos sobem e descem a toda velocidade.</p></div>
      </div></div>
    {adulto("andamento",
            "Duas peças curtas (as duas juntas têm menos de três minutos). Ouça <i>Hemíones</i> e corram pela sala; ouça <i>Tartarugas</i> e andem de quatro, bem devagar. "
            "Depois, uma brincadeira: você toca uma das duas sem avisar, e ela escolhe se é a lebre ou a tartaruga. "
            "<b>Para o adulto curioso:</b> o tema das <i>Tartarugas</i> é o famoso cancã de Offenbach — tocado na velocidade normal, ela vai reconhecer o contraste.",
            credito_pd("cartao_cavalo"))}"""
    L.add(c, aba="--d-musica")

    passos(L, "Ajudar alguém", "pequenos gestos, como o ratinho",
           [(img("chave", "28mm"), "Segurar a porta para alguém passar"),
            (img("livro", "28mm"), "Levar um livro até a estante"),
            (img("jarra", "28mm"), "Servir água para quem tem sede"),
            (img("cesta", "30mm"), "Carregar a cesta pequena da feira"),
            (img("toalha", "28mm"), "Ajudar a dobrar os panos"),
            (img("ratinho", "30mm"), "Dizer “obrigada” quando alguém ajuda")],
           adulto("vida prática e formação",
                  "Escolha um ou dois gestos da semana, não todos. Quando ela ajudar, nomeie o que ela fez (“você segurou a porta para a vovó”), em vez de só elogiar. "
                  "A fábula do leão e do rato dá a ideia; a vida dá a prática."),
           aba="--d-vida")


# ================================================================== U7 MÚSICOS DE BREMEN

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · Os Músicos de Bremen", aba="--d-musica",
        pergunta="O que quatro amigos conseguem fazer juntos? Como soa cada voz?",
        duracao="Dois fins de semana · dois encontros · 20 minutos. Unidade de música: a história é o pretexto para uma orquestra de casa.",
        objetivos=["Ouvir e recontar uma história com quatro personagens.", "Ordenar do maior para o menor (a torre).",
                   "Reconhecer e imitar quatro vozes; associar voz e timbre.", "Tocar juntas, cada uma na sua vez e depois todas ao mesmo tempo.",
                   "Contar até 4."],
        repertorio="<b>Conto:</b> irmãos Grimm, <i>Os Músicos de Bremen</i> (1819), versão da coleção. <b>Imagem:</b> Arthur Rackham (1916). "
                   "<b>Música:</b> Saint-Saëns, <i>Personagens de orelhas compridas</i> (o jumento). <b>Línguas:</b> <i>donkey, dog, cat, rooster · l’âne, le chien, le chat, le coq</i>.",
        materiais="Tambor ou panela, sino, chocalho (a caixa de sons do Volume 1), tigela e colher; quatro bichinhos de tamanhos diferentes.",
        vida="Esperar a vez: na orquestra, cada um toca quando o regente aponta.",
        etapas=[["História com a silhueta de Rackham.", "As quatro vozes.", "Ouvir o jumento de Saint-Saëns."],
                ["A torre: do maior ao menor.", "Contar os animais.", "Que instrumento é cada voz?"],
                ["Orquestra de casa.", "Ela é a regente.", "Inventar um quinto músico."]],
        indicadores=["Nomeia os quatro animais.", "Faz as quatro vozes.", "Ordena do maior ao menor.",
                     "Toca só quando é a vez dela.", "Rege: aponta e para os músicos.", "Conta até 4."],
        interesse="mostre no mapa onde fica Bremen, na Alemanha; há uma estátua dos quatro músicos na cidade.",
        dificil="só as quatro vozes e a torre de bichinhos."))

    historia(L, "Os Músicos de Bremen", "irmãos Grimm · versão da coleção", f"""
      {lado("cartao_galo", "40mm")}
      <p class="capitular" style="margin-top:4mm">Um jumento, já velhinho, resolveu ir para a cidade de Bremen ser músico.</p>
      <p>No caminho encontrou um cão cansado. <i>— Venha comigo! Você toca tambor e eu canto.</i> E o cão foi.</p>
      <p>Depois encontraram um gato triste. <i>— Venha conosco! Você canta de noite tão bem…</i> E o gato foi.</p>
      <p>Por fim, um galo em cima de um portão. <i>— Venha também! Que voz forte você tem!</i> E o galo foi.</p>
      <p>Agora eram quatro: o jumento, o cão, o gato e o galo.</p>""",
             credito_pd("cartao_galo").replace('class="credito"', 'class="credito" style="position:absolute;left:18mm;right:18mm;bottom:20mm"'),
             aba="--d-historias")

    historia(L, None, None, f"""
      {lado("rackham_bremen", "56mm", False)}
      <p style="margin-top:6mm">À noite, na floresta, viram uma luz: era uma casa onde uns ladrões jantavam.</p>
      <p>Os amigos tiveram uma ideia. O jumento ficou embaixo; o cão subiu nas costas do jumento; o gato, nas costas do cão; e o galo, lá no alto, na cabeça do gato.</p>
      <p>E todos cantaram ao mesmo tempo:</p>
      <p class="fala" style="font-size:20pt">— Ii-óó! Au-au! Miau! Cocoricó!</p>
      <p>Os ladrões levaram tamanho susto que fugiram para a floresta e nunca mais voltaram. E os quatro músicos gostaram tanto da casinha que ficaram morando lá.</p>""",
             adulto("contar e cantar",
                    "Faça você as quatro vozes, uma de cada vez, e depois todas juntas, o mais alto possível: ela vai rir e pedir de novo. "
                    "Na silhueta de Rackham, a torre aparece de perfil: o jumento empinado, o cão, o gato e o galo no topo. "
                    "Perguntas: “quem ficou embaixo? e lá em cima?” · “por que os ladrões fugiram?”.",
                    credito_pd("rackham_bremen")), aba="--d-historias")

    # torre: do maior para o menor (recortável)
    bichos = [("jumento", "ii-óó!", 74), ("cão", "au-au!", 58), ("gato", "miau!", 44), ("galo", "cocoricó!", 32)]
    ordem = [2, 0, 3, 1]
    cel = "".join(f'<td style="vertical-align:bottom;text-align:center"><div class="carta" style="display:inline-flex;width:{bichos[i][2] * 0.55}mm;height:{bichos[i][2] * 0.5}mm">'
                  f'<div style="font-size:{9 + bichos[i][2] / 9:.0f}pt;font-weight:600">{bichos[i][0]}</div><div class="peq it">{bichos[i][1]}</div></div></td>'
                  for i in ordem)
    cel = f'<table style="width:178mm;margin:0 auto"><tr>{cel}</tr></table>'
    c = f"""{cabeca_folha("A torre dos músicos", "recortar os quatro cartões e montar a torre: o maior embaixo", 12)}
    <div class="centro" style="position:absolute;left:0;right:0;top:34mm">{pd("rackham_bremen", "62mm")}</div>
    <div style="position:absolute;left:16mm;top:160mm">{cel}</div>
    {adulto("seriação de quatro",
            "Os cartões têm tamanhos diferentes, como os animais. Ela monta a torre na mesa: o maior embaixo (jumento), depois o cão, o gato e o galo no alto — "
            "como na silhueta. Em cada cartão que pôr, faz a voz do bicho. Ordenar quatro é mais difícil que três (Cachinhos): comece com dois. "
            "<b>Contar:</b> “quantos músicos há na torre?” — um, dois, três, quatro.",
            credito_pd("rackham_bremen"), estilo="top:220mm;bottom:auto")}"""
    L.add(c + rodape_folha(str(L.proximo)), moldura=False, cabecalho=False, numero=False)

    linhas = "".join(f'<tr><td style="font-size:13pt;width:30mm"><b>{a}</b></td><td style="font-size:12pt;font-style:italic">{v}</td>'
                     f'<td>{img(m, "18mm", "display:inline-block")}</td><td style="font-size:11.5pt">{inst}</td></tr>'
                     for a, v, m, inst in (("jumento", "ii-óó!", "tigela", "voz grave e comprida · panela ou tigela grande"),
                                           ("cão", "au-au!", "tambor", "batidas curtas · tambor"),
                                           ("gato", "miau!", "bolhas", "voz que sobe e desce · chocalho de arroz (caixa de sons)"),
                                           ("galo", "cocoricó!", "sino", "voz aguda e forte · sino")))
    c = f"""<div class="miolo">{titulo("A orquestra de casa", "cada voz, um instrumento", 28)}
      <table class="tab" style="margin-top:6mm">{linhas}</table>
      <div class="caixa" style="margin-top:7mm;font-size:12pt;line-height:1.6">
      <b>1.</b> Cada músico toca sozinho, na sua vez. &nbsp; <b>2.</b> Dois juntos. &nbsp; <b>3.</b> Os quatro ao mesmo tempo — forte! &nbsp;
      <b>4.</b> A regente levanta a mão: silêncio!</div>
      <p class="centro" style="margin-top:6mm;font-size:13pt;font-style:italic">E o jumento na música de verdade? Saint-Saëns, <i>Personagens de orelhas compridas</i>: os violinos zurram — ii-óó!</p></div>
    {adulto("timbre e regência",
            "Timbre é a “cor” de cada som: o mesmo “lá” no sino e na panela soa diferente. Distribua os instrumentos entre a família; a Marina é a regente "
            "e aponta quem toca. Depois troquem: ela toca e você rege. <i>Personagens de orelhas compridas</i> dura menos de um minuto: dois violinos imitam "
            "o zurro alternando notas muito agudas e muito graves.")}"""
    L.add(c, aba="--d-musica")

    sequencia(L, "Os Músicos de Bremen · cartões de sequência", "desenhe em cada quadro, ou recorte e conte",
              [("o jumento parte", img("estrela", "30mm", "opacity:.0") + '<div class="peq">(desenhar)</div>'),
               ("os quatro amigos", '<div class="peq">(desenhar)</div>'),
               ("a torre e o canto", pd("rackham_bremen", "40mm", "max-height:62mm;object-fit:contain")),
               ("a casinha deles", '<div class="peq">(desenhar)</div>')],
              adulto("desenhar a sequência",
                     "Desta vez só uma cena tem imagem: as outras três ela desenha (ou você desenha o que ela ditar). Rabiscos valem: o que importa é ela dizer o que "
                     "está em cada quadro. Depois recortem e ordenem como as outras histórias.",
                     credito_pd("rackham_bremen"), estilo="top:226mm;bottom:auto"))


# ================================================================== U8 PRINCESA E FOLCLORE

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · A Princesa e a Ervilha e histórias do Brasil", aba="--d-artes",
        pergunta="O que se sente sem ver? Quem mora na mata, nas histórias do Brasil?",
        duracao="Dois ou três fins de semana · dois encontros · 15 a 25 minutos.",
        objetivos=["Contar até 5 (e depois até 10) com os colchões.", "Reconhecer objetos pelo tato, sem olhar.",
                   "Conhecer três figuras do folclore brasileiro: Curupira, Saci e Iara.", "Seguir pegadas para a frente e para trás.",
                   "Cantar uma cantiga tradicional brasileira."],
        repertorio="<b>Conto:</b> Hans Christian Andersen, <i>A Princesa e a Ervilha</i> (1835), versão da coleção. <b>Lendas:</b> Curupira, Saci-Pererê e Iara, "
                   "versões curtas da coleção, a partir da tradição oral. <b>Cantiga:</b> <i>Peixe vivo</i> (tradicional). <b>Línguas:</b> <i>pea · le petit pois · pīsum</i>.",
        materiais="Um grão de ervilha (ou feijão); almofadas e cobertores; um saco de pano opaco com 4 ou 5 objetos conhecidos; tinta guache e papel grande para pegadas.",
        vida="Arrumar a cama com o adulto: esticar o lençol, pôr o travesseiro, dobrar a coberta.",
        etapas=[["Ouvir a princesa.", "Ouvir as lendas.", "Cantar <i>Peixe vivo</i>."],
                ["Contar os colchões.", "O saco surpresa.", "Pegadas para a frente e para trás."],
                ["Montar a pilha de almofadas e esconder a ervilha.", "Inventar um morador da mata.", "Carimbar os próprios pés."]],
        indicadores=["Conta até 5 com correspondência.", "Reconhece 3 objetos pelo tato.", "Nomeia o Curupira e diz como são os pés dele.",
                     "Diz para que lado as pegadas vão.", "Canta um trecho da cantiga.", "Reconta a princesa em poucas frases."],
        interesse="procure livros de lendas brasileiras ilustrados por artistas brasileiros e conte uma lenda por semana.",
        dificil="só a pilha de almofadas e a ervilha.",
        alerta="<b>Ervilha e feijão</b> são pequenos o bastante para engasgar ou entrar no nariz: use sempre com o adulto ao lado e guarde depois."))

    cols = ["colchao_rosa", "colchao_azul", "colchao_verde", "colchao_ocre", "colchao_lilas"] * 2
    pilha = "".join(img(n, "70mm", "margin:-2.5mm auto 0") for n in cols[:7])
    historia(L, "A Princesa e a Ervilha", "Hans Christian Andersen · versão da coleção", f"""
      <div style="float:right;width:72mm;margin:0 0 3mm 5mm">{img("ervilha", "30mm", "margin:0 auto 1mm")}{pilha}</div>
      <p class="capitular" style="margin-top:4mm">Era uma vez um príncipe que queria casar com uma princesa de verdade.</p>
      <p>Numa noite de tempestade, alguém bateu no portão do castelo: era uma moça encharcada, que disse ser princesa.</p>
      <p>A rainha, para descobrir, pôs uma <b>ervilha</b> no estrado da cama e, por cima, muitos e muitos colchões.</p>
      <p>De manhã, perguntaram como ela tinha dormido.</p>
      <p class="fala">— Muito mal! Havia uma coisa dura na cama, e fiquei toda roxinha!</p>
      <p>Só uma princesa de verdade sentiria uma ervilha embaixo de tantos colchões. E o príncipe casou com ela.</p>""",
             adulto("contar e rir",
                    "É um conto curto e engraçado — no original, a ervilha termina num museu. Pergunte: “o que estava embaixo dos colchões?” · “como ela sentiu?”. "
                    "Brincadeira: empilhem almofadas, ponham um feijão embaixo da última e deixe que ela se deite — consegue sentir?"),
             aba="--d-historias")

    linhas = ""
    for k in range(1, 6):
        linhas += (f'<td style="vertical-align:bottom;text-align:center;width:20%">' + "".join(img(cols[i], "30mm", "margin:-1mm auto 0") for i in reversed(range(k)))
                   + f'<div style="font-size:28pt;color:var(--rosa)">{k}</div></td>')
    linhas = f'<table style="width:100%"><tr>{linhas}</tr></table>'
    c = f"""<div class="miolo">{titulo("Quantos colchões?", "contar de baixo para cima", 28)}
      <div style="margin-top:10mm">{linhas}</div>
      <div class="centro" style="margin-top:8mm">{img("ervilha", "34mm")}</div></div>
    {adulto("contar até 5",
            "Toque cada colchão de baixo para cima, dizendo um número por toque. O número grande diz quantos há. Depois, com almofadas ou toalhas dobradas de verdade, "
            "montem pilhas de 1 a 5. <b>Desafio:</b> “se eu tirar um, quantos ficam?” — ela confere contando de novo. Quando 5 ficar fácil, vá até 10.")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("O saco surpresa", "sentir sem ver", 28)}
      <div class="centro" style="margin:6mm 0">{img("colher", "26mm", "display:inline-block;margin:0 3mm")}{img("chave", "30mm", "display:inline-block;margin:0 3mm")}
      {img("pena", "28mm", "display:inline-block;margin:0 3mm")}{img("pedra", "30mm", "display:inline-block;margin:0 3mm")}{img("laranja", "28mm", "display:inline-block;margin:0 3mm")}</div>
      <table class="tab" style="font-size:12pt;margin-top:4mm">
        <tr><th style="width:40mm">Nível</th><th>Como brincar</th></tr>
        <tr><td>Descobrir</td><td>Ela vê os objetos, você põe um no saco, ela tateia e diz qual é.</td></tr>
        <tr><td>Relacionar</td><td>Você mostra um cartão (ou um objeto igual); ela procura no saco o mesmo, só pelo tato.</td></tr>
        <tr><td>Criar</td><td>Ela esconde um objeto e dá pistas: “é duro, é frio, abre a porta…” — e você adivinha.</td></tr>
      </table></div>
    {adulto("percepção tátil",
            "É o “saco misterioso” de Montessori: o tato isolado da visão. Use objetos que ela conhece bem e que tenham formas e texturas bem diferentes "
            "(colher, chave, pena, pedra, laranja). Vocabulário: liso, áspero, macio, duro, frio, redondo, pontudo. A princesa sentiu a ervilha sem ver: ela também consegue!")}"""
    L.add(c, aba="--d-memoria")

    historia(L, "Histórias da mata brasileira", "lendas da tradição oral · versões da coleção", f"""
      <p class="capitular" style="margin-top:4mm"><b>O Curupira</b> é o guardião da mata. É um menino pequeno, de cabelo vermelho como fogo, e tem os pés virados para trás!
      Quem segue as pegadas dele pensa que ele foi para um lado… e ele foi para o outro. Assim ele protege os bichos de quem quer fazer mal à floresta.</p>
      <div class="centro" style="margin:2mm 0">{img("pegada", "16mm", "display:inline-block;margin:0 3mm;transform:rotate(180deg)")}{img("pegada_esq", "16mm", "display:inline-block;margin:0 3mm;transform:rotate(180deg) translateY(8mm)")}</div>
      <p><b>O Saci-Pererê</b> é um menino de uma perna só, muito brincalhão, com um gorro vermelho mágico. Ele vive aprontando: esconde coisas, dá nó no rabo dos cavalos
      e passa pulando num redemoinho de vento.</p>
      <div class="centro" style="margin:1mm 0">{img("gorro", "26mm")}</div>
      <p><b>A Iara</b> mora no fundo dos rios. Dizem que canta tão bonito que até os peixes param de nadar para ouvir.</p>""",
             adulto("lendas brasileiras",
                    "Estas lendas vêm da tradição oral (indígena, africana e portuguesa misturadas) e mudam de região para região. Conte uma por vez, de modo leve. "
                    "Para esta idade, o Curupira é um protetor da mata, não um bicho-papão. Pergunte: “por que ele tem os pés virados?” e deixe que ela imagine.",
                    estilo=""),
             aba="--d-historias")

    svg = ""
    for k in range(5):
        y = 70 + k * 32
        svg += f'<g transform="translate({40 + k * 24} {y})">' + "</g>"
    imgs = ""
    for k in range(5):
        x, y = 30 + k * 30, 210 - k * 34
        imgs += img("pegada" if k % 2 else "pegada_esq", "14mm", f"position:absolute;left:{x}mm;top:{y}mm;transform:rotate(30deg)")
    for k in range(5):
        x, y = 120 + k * 12, 70 + k * 30
        imgs += img("pegada" if k % 2 else "pegada_esq", "14mm", f"position:absolute;left:{x}mm;top:{y}mm;transform:rotate(200deg)")
    c = f"""<div class="miolo">{titulo("Para onde ele foi?", "as pegadas do Curupira", 28)}</div>{imgs}
    <div class="peq it" style="position:absolute;left:24mm;top:248mm">pegadas de gente</div>
    <div class="peq it" style="position:absolute;left:140mm;top:54mm">pegadas do Curupira</div>
    {adulto("direção e inferência",
            "Duas trilhas: à esquerda, pegadas comuns — os dedos apontam para onde a pessoa foi (para cima). À direita, as do Curupira: os dedos apontam para trás, "
            "mas ele foi no sentido contrário! Pergunte: “para onde vai esta pessoa?” e “e o Curupira, para onde foi de verdade?”. "
            "<b>Criar:</b> com os pés pintados de guache, ela anda num papel grande; depois andem para trás e comparem.",
            estilo="left:62mm")}"""
    L.add(c, aba="--d-memoria")

    poema(L, "Peixe vivo", "cantiga tradicional brasileira",
          ["Como pode o peixe vivo<br>viver fora da água fria?",
           "Como pode o peixe vivo<br>viver fora da água fria?",
           "Como poderei viver,<br>como poderei viver,<br>sem a tua, sem a tua,<br>sem a tua companhia?"],
          img("peixe", "42mm", "display:inline-block;margin:0 4mm") + img("peixe_azul", "38mm", "display:inline-block;margin:0 4mm;transform:scaleX(-1)"),
          adulto("cantar",
                 "Cantiga de roda mineira, conhecida em todo o Brasil. Cantem de mãos dadas, em roda, balançando. Pergunte: “o peixe vive fora da água?” — "
                 "e lembre da experiência da bacia (Volume 1). A Iara, que canta no fundo do rio, bem podia cantar esta canção."),
          aba="--d-musica")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo
    c = f"""<div class="miolo">{titulo("Meu livro de histórias", "a história que eu conto", 28)}
      <table class="tab" style="font-size:12pt;margin-top:4mm">
        <tr><td style="width:56mm">Minha história preferida:</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Meu personagem preferido:</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr>
        <tr><td>Uma história que eu inventei:</td><td style="border-bottom:0.6pt solid var(--linha)"></td></tr></table>
      <div class="caixa" style="height:150mm;margin-top:6mm"><div class="peq centro" style="margin-top:2mm">desenho, colagem ou a história ditada por ela</div></div></div>"""
    L.add(c, aba="--d-artes")

    for metade, unidades in enumerate((UNIDADES[:4], UNIDADES[4:])):
        linhas = "".join(f'<tr><td style="width:44mm"><b>{n.split(" · ", 1)[1]}</b><div class="peq">{n.split(" · ")[0]}</div></td>'
                         f'<td style="height:50mm"></td></tr>' for n, _ in unidades)
        c = f"""<div class="miolo">{titulo("Diário de observação", "para o adulto · falas, recontos e descobertas — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Unidade</th><th>O que ela contou, perguntou ou inventou (com data)</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    import fontes_v1
    usadas = ["neill_", "brooke_", "crane_", "potter_familia", "potter_mae", "potter_irmas", "potter_pedro", "potter_rabanetes", "potter_mcgregor",
              "potter_rede", "potter_regador", "potter_gata", "potter_portao", "potter_ceia", "potter_benjamin", "rackham_", "cartao_"]
    por_livro = {}
    for n, (item, pg, *_r) in fontes_v1.ITENS.items():
        if any(n.startswith(u) for u in usadas):
            por_livro.setdefault(item, set()).add(pg)
    cred = "".join(f"<li>{fontes_v1.LIVROS[i]} — Internet Archive, <i>{i}</i>, páginas {', '.join('n' + str(p) for p in sorted(ps))}.</li>"
                   for i, ps in por_livro.items())
    c = f"""<div class="miolo texto">{titulo("Repertório e créditos", "Volume 2", 26)}
      <h2>Literatura</h2><p style="font-size:9.6pt">Versões da coleção, a partir de: H. C. Andersen, <i>O Patinho Feio</i> (1843) e <i>A Princesa e a Ervilha</i> (1835);
      <i>Cachinhos Dourados e os Três Ursos</i> (tradicional inglês; Robert Southey, 1837); <i>Chapeuzinho Vermelho</i> (Perrault, 1697; Grimm, 1812);
      <i>Os Três Porquinhos</i> (tradicional inglês; Halliwell-Phillipps, 1843; Jacobs, 1890); Beatrix Potter, <i>The Tale of Peter Rabbit</i> (1902), tradução da coleção;
      Esopo, <i>A Lebre e a Tartaruga</i> e <i>O Leão e o Rato</i>; irmãos Grimm, <i>Os Músicos de Bremen</i> (1819); lendas do Curupira, do Saci e da Iara
      (tradição oral brasileira). Cantiga: <i>Peixe vivo</i> (tradicional). Todos os textos-fonte estão em domínio público.</p>
      <h2>Música</h2><p style="font-size:9.6pt">Saint-Saëns, <i>O Carnaval dos Animais</i> (1886): <i>O Cisne</i>, <i>Tartarugas</i>, <i>Hemíones</i>, <i>Personagens de orelhas compridas</i> ·
      Brahms, <i>Canção de ninar</i>, op. 49 n.º 4 (1868) · Grieg, <i>Na gruta do Rei da Montanha</i> (1875). Obras em domínio público; as gravações têm direitos próprios.</p>
      <h2>Ilustrações em domínio público</h2><p style="font-size:9pt">Reproduzidas de digitalizações do Internet Archive, com recorte e ajuste do tom do papel; nenhuma pintura foi retocada.</p>
      <ul style="font-size:8.6pt;line-height:1.35">{cred}</ul>
      <p style="font-size:9pt">Motivos de cartões e atividades: aquarela digital procedural da coleção. Tipografia: EB Garamond (licença OFL).</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 2</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">vamos contar os porquinhos de novo — e muito mais coisas,<br>
      medir com as mãos, achar formas na casa,<br>montar padrões de contas e de sons.</p>
      <div style="margin-top:12mm">{img("ratinho", "40mm", "margin:0 auto")}</div>
      <p class="peq" style="margin-top:8mm">Volume 3 · Números, formas e raciocínio</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

def montar():
    L = Livro(2, "Histórias, memória e imaginação")
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
    for versao, nome in (("impressao", "volume2-impressao"), ("tela", "volume2-tela")):
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume2-tela.pdf"), os.path.join(insp, "p")], check=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
