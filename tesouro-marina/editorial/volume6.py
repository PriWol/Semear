"""
VOLUME 6 — O LIVRO DA NATUREZA
uso: python3 volume6.py            (monta o volume com as unidades já escritas; ver UNIDADES_PRONTAS)
As ilustrações são pranchas antigas de naturalistas (fontes_v6.py) e motivos em aquarela da coleção, os novos em motivos7.py (ADR 0019).
"""
import html
import os
import re
import subprocess
import sys

from PIL import Image

from livro import (Livro, VERSAO, adulto, cabeca_folha, cartoes, gerar_pdf, guia, img, lista, observacao, passos, poema, sequencia, texto, titulo)
from musica import linha_do_tempo
import fontes_v6

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume6")

UNIDADES = [
    ("Unidade 1 · O diário da natureza", "--d-natureza"),
    ("Unidade 2 · Aves do quintal", "--d-musica"),
    ("Unidade 3 · Insetos e pequenos bichos", "--d-artes"),
    ("Unidade 4 · Árvores e folhas", "--d-memoria"),
    ("Unidade 5 · Sementes", "--d-vida"),
    ("Unidade 6 · Água e chuva", "--d-matematica"),
    ("Unidade 7 · Céu, sol, lua e estrelas", "--d-ingles"),
    ("Unidade 8 · O corpo humano", "--d-historias"),
    ("Unidade 9 · As estações", "--d-jogos"),
]
INICIO = {}


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


def tira(itens, w="22mm", gap="2mm"):
    """Fila de motivos pequenos."""
    return '<div class="centro" style="line-height:0">' + "".join(img(m, w, f"display:inline-block;margin:0 {gap}") for m in itens) + "</div>"


def prancha(nome, w_max, h_max, estilo=""):
    """Prancha de naturalista, no maior tamanho que cabe na caixa (mm)."""
    with Image.open(os.path.join(fontes_v6.SAIDA, f"{nome}.jpg")) as im:
        k = min(w_max / im.width, h_max / im.height)
        w, h = im.width * k, im.height * k
    legenda = html.escape(re.sub(r"<[^>]+>", "", f"{fontes_v6.OBRAS[nome][2]}, {fontes_v6.OBRAS[nome][1]}"), quote=True)
    return (f'<img class="obra" src="dominio_publico/v6/{nome}.jpg" '
            f'style="width:{w:.1f}mm;height:{h:.1f}mm;display:block;margin:0 auto;{estilo}" alt="{legenda}">')


def recorte(nome, caixa, largura_mm):
    """Recorte de uma prancha (x, y, largura, altura em pixels do JPEG), feito pelo estilo: nenhum arquivo novo, nenhum retoque."""
    x, y, w, h = caixa
    with Image.open(os.path.join(fontes_v6.SAIDA, f"{nome}.jpg")) as im:
        total_w, total_h = im.size
    k = largura_mm / w
    return (f'<div class="obra" role="img" aria-label="{html.escape(fontes_v6.OBRAS[nome][2], quote=True)}" '
            f'style="width:{largura_mm:.1f}mm;height:{h * k:.1f}mm;margin:0 auto;background-image:url(dominio_publico/v6/{nome}.jpg);'
            f'background-repeat:no-repeat;background-size:{total_w * k:.1f}mm {total_h * k:.1f}mm;background-position:-{x * k:.1f}mm -{y * k:.1f}mm"></div>')


def credito_prancha(*nomes):
    return '<div class="credito">Prancha: ' + " · ".join(fontes_v6.credito(n) for n in nomes) + "</div>"


def apreciar(L, nome, t, sub, perguntas, texto_adulto, rotulo, aba, w=120, h=130):
    """Página de apreciação: a prancha grande e perguntas de observação (só o que se vê)."""
    return observacao(L, t, sub, prancha(nome, w, h), perguntas, adulto(rotulo, texto_adulto, credito_prancha(nome)), aba=aba)


def moldura_vazia(rotulo, h="62mm"):
    return f'<div class="caixa" style="height:{h}"><div class="peq centro">{rotulo}</div></div>'


def diario(L, t, sub, rotulos, aba, adulto_texto, h="62mm", faixa=None):
    cel = "".join(moldura_vazia(r, h) for r in rotulos)
    topo = f'<div style="margin:3mm 0 0">{tira(faixa, "22mm", "3mm")}</div>' if faixa else ""
    c = f"""<div class="miolo">{titulo(t, sub, 27)}{topo}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">{cel}</div></div>
      {adulto("registrar", adulto_texto)}"""
    return L.add(c, aba=aba)



def cena(itens, h=80, w=170):
    """Composição de motivos em posição livre (mm): itens = (motivo, largura, x, y[, rotação em graus])."""
    partes = []
    for m, lg, x, y, *r in itens:
        rot = f"transform:rotate({r[0]}deg);" if r else ""
        partes.append(f'<div style="position:absolute;left:{x}mm;top:{y}mm;line-height:0;{rot}">{img(m, f"{lg}mm")}</div>')
    return f'<div style="position:relative;height:{h}mm;width:{w}mm;margin:0 auto">' + "".join(partes) + "</div>"


def historia6(L, t, sub, paragrafos, topo, base, adulto_html, aba):
    """Página de história: tira de motivos no alto, texto e uma cena de motivos embaixo."""
    ps = "".join(f'<p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">{p}</p>' for p in paragrafos)
    c = f"""<div class="miolo">{titulo(t, sub, 24)}<div class="centro" style="margin:3mm 0">{topo}</div>{ps}<div style="margin-top:5mm">{base}</div></div>{adulto_html}"""
    return L.add(c, aba=aba)


def passos6(L, t, sub, itens, adulto_html, aba, vinheta=""):
    """Como `passos`, com uma vinheta de motivos no espaço de baixo."""
    cel = "".join(f'<div class="passo"><div class="n">{i + 1}</div>{im}<div class="txt">{tx}</div></div>' for i, (im, tx) in enumerate(itens))
    c = f"""<div class="miolo">{titulo(t, sub)}<div class="passos">{cel}</div><div style="margin-top:8mm">{vinheta}</div></div>{adulto_html}"""
    return L.add(c, aba=aba)


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 6</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">O livro<br>da natureza</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:140mm;left:0;right:0">{prancha("beijaflor", 100, 118)}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(["folha", "pena", "gota", "lupa"], "15mm", "3mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 6</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O livro da natureza</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">O diário de natureza é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(["folha", "pena", "gota", "lupa"], "30mm", "3mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Sair, olhar, voltar e contar</h1>
      <p>Este volume é para <b>sair de casa</b>. A natureza que a Marina vai conhecer está no quintal, na praça, na calçada e na janela, e este livro só ajuda a olhar:
      um passarinho de cada vez, uma folha de cada vez, uma nuvem de cada vez.</p>
      <h2>Três ideias</h2>
      <ul>
        <li><b>O diário da natureza</b> (Charlotte Mason). Um caderno em que ela desenha e escreve o que viu, com a data e o lugar. Não precisa desenhar bem: precisa <b>olhar de verdade</b>.
        Quem desenha uma folha vê a folha.</li>
        <li><b>Poucas coisas, muitas vezes.</b> A mesma árvore, no mesmo lugar, em estações diferentes ensina mais que dez passeios apressados.</li>
        <li><b>Nomear com cuidado.</b> Saber o nome do sabiá, do bem-te-vi ou do beija-flor é uma maneira de gostar deles. Quando você não souber o nome, diga “não sei, vamos descobrir”.</li>
      </ul>
      <h2>O que este volume traz</h2>
      <p>Nove unidades: <i>o diário da natureza</i>, <i>aves do quintal</i>, <i>insetos e pequenos bichos</i>, <i>árvores e folhas</i>, <i>sementes</i>, <i>água e chuva</i>, <i>céu, sol, lua e estrelas</i>,
      <i>o corpo humano</i> e <i>as estações</i>, no Brasil e no hemisfério norte.</p>
      <h2>Sobre as imagens</h2>
      <p>As pranchas deste livro são de naturalistas de muito tempo atrás, em domínio público, e cada página diz de onde veio a imagem. <b>Nenhum desenho de ave ou de bicho substitui o
      bicho de verdade.</b> A prancha serve para olhar de perto o que no quintal passa depressa demais.</p>
      <div class="centro" style="margin-top:8mm">""" + tira(["folha", "pena", "gota", "lupa", "raminho"], "22mm", "2mm") + "</div>")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Um caderno e uma sacola</h1>
      <p>Separe um <b>caderno de natureza</b> (sem pauta, com capa dura se der), lápis de cor, uma lupa, uma sacolinha de pano para guardar folhas e sementes caídas e uma garrafa de água.
      Escolha um lugar perto de casa para voltar sempre: a praça, um canto do quintal, a janela.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Um encontro por semana, ao ar livre, de 20 a 30 minutos. Uma unidade a cada duas ou três semanas. Quando chover, olhe pela janela: também vale.</td></tr>
        <tr><th>Olhar</th><td>Peça que ela fique <b>quieta por um minuto</b> antes de falar. Faça uma pergunta de cada vez. Depois de olhar, ela <b>conta com o caderno fechado</b> o que lembra.</td></tr>
        <tr><th>Desenhar</th><td>Um só objeto por página, grande, com a data e o lugar. Não corrija o desenho nem copie por ela. Se não sair parecido, pergunte: “O que ainda falta olhar?”</td></tr>
        <tr><th>Bichos</th><td>Olhar, nunca pegar: bicho desconhecido, ninho e flor ficam onde estão. Insetos e aranhas vistos de perto, de longe ou de lupa. Lavar as mãos depois de mexer em terra e plantas.</td></tr>
        <tr><th>Guardar</th><td>O diário fica numa gaveta que ela alcança. Releia com ela no fim de cada estação: “Olha, em março tinha tantas flores…”</td></tr>
        <tr><th>Idiomas</th><td>Os cartões trazem o nome em inglês, francês e (quando existe) latim no verso.</td></tr>
      </table>
      <h2>Segurança</h2>
      <p>Protetor solar e chapéu, repelente quando indicado, calçado fechado em mato alto. Não coma frutinhas, sementes nem cogumelos encontrados. Nunca beba água de rio ou de poça. Fique perto de água.</p>
      <div class="centro" style="margin-top:5mm">{tira(["lupa", "folha", "pena", "gota"], "20mm")}</div>""")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio.get(n, "")}</td></tr>' for n, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Galeria, diário de natureza e créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Volume 6 · O livro da natureza", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["folha", "pena", "gota", "lupa", "raminho", "estrela"], "22mm", "1.5mm")}</div></div>"""


# ================================================================== U1 O DIÁRIO DA NATUREZA

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · O diário da natureza", aba="--d-natureza",
        pergunta="O que a gente vê quando para, olha e desenha uma coisa só?",
        duracao="Dois fins de semana · dois passeios de 20 a 30 minutos · registro em casa, no mesmo dia.",
        objetivos=["Escolher <b>uma</b> coisa da natureza e olhar para ela em silêncio.", "Desenhar o que vê e escrever (ou ditar) a data, o lugar e o tempo.",
                   "Contar o que viu com o caderno fechado.", "Usar os cinco sentidos, com cuidado, para observar.", "Nomear em português (e, nos cartões, em inglês, francês e latim) nove coisas da natureza."],
        repertorio="<b>Palavras:</b> folha, pedra, pena, gota, nuvem, sol, lua, galho, flor. <b>Línguas:</b> <i>leaf · la feuille · folium</i>; <i>stone · la pierre · lapis</i>; <i>feather · la plume · penna</i>; <i>sun · le soleil · sol</i>.",
        materiais="Caderno sem pauta, lápis preto e de cor, uma lupa, uma sacolinha de pano, uma prancheta ou livro grosso para apoiar. Chapéu e água.",
        vida="Olhar pela janela ao acordar e dizer como está o tempo; guardar uma folha ou uma pena encontrada no caminho na caixa de tesouros.",
        etapas=[["Passeio curto, em silêncio, até o lugar de olhar.", "Escolher uma coisa e olhar por um minuto.", "Dizer o que viu, de olhos fechados."],
                ["Desenhar a coisa, grande, com todos os detalhes que lembrar.", "Escrever a data, o lugar e o tempo.", "Comparar o desenho com a coisa de verdade."],
                ["Voltar ao mesmo lugar uma semana depois e olhar de novo.", "Dizer o que mudou.", "Escolher o que mais gostou para contar a outra pessoa."]],
        indicadores=["Fica quieta olhando por um minuto, sem ser pedida a toda hora.", "Diz o que vê usando palavras de cor, forma e tamanho.", "Desenha a coisa com algum detalhe real (a borda da folha, a nervura).",
                     "Lembra do que viu com o caderno fechado.", "Percebe o que mudou de um dia para o outro.", "Pergunta “o que é isso?” ou “por que é assim?”."],
        interesse="voltar ao mesmo lugar toda semana, no mesmo dia e hora, e anotar o que mudou.",
        dificil="ficar só na janela por um minuto e dizer três coisas que viu lá fora.",
        alerta="Olhar não é pegar: bicho e ninho ficam onde estão. Em mato alto, calçado fechado; água e protetor solar sempre. Fique ao alcance do olhar dela."))

    historia6(L, "Como se olha uma coisa só", "uma história curta, para contar antes de sair",
              ["Marina tinha um caderno novo, sem nenhuma linha. “O que a gente escreve num caderno sem linhas?”, ela perguntou. “O que a gente vê”, disse o papai. Eles saíram para o quintal e se sentaram no degrau.",
               "“Escolha uma coisa só”, disse o papai. Marina escolheu uma folha. “Agora fique olhando um minuto, sem falar.” O minuto demorou. Primeiro a folha era verde. Depois ela viu que tinha uma linha no meio e linhas menores saindo dela, como os galhos de uma árvore. A borda tinha uns dentinhos. Num cantinho, um furo pequeno: alguém já tinha comido um pedaço.",
               "“Agora desenhe”, disse o papai. Marina desenhou a linha do meio, as linhas pequenas, os dentinhos e o furo. No cantinho da página escreveu, com a ajuda do papai, o dia e o lugar: <i>quintal, degrau, sol fraco</i>. Quando acabou, ela disse: “Nunca vi tanta coisa numa folha só.” O papai sorriu: “É por isso que a gente olha uma coisa de cada vez.”"],
              tira(["caderno", "lupa", "folha_carvalho"], "34mm", "5mm"),
              cena([("caderno", 52, 52, 4), ("lupa", 42, 112, 12, 12), ("folha_carvalho", 32, 6, 6, -14), ("folha_bordo", 32, 16, 44, 10),
                    ("lapis_cor", 40, 96, 44), ("pena", 24, 142, 44, 20), ("folha_fina", 26, 62, 52, -8)], 78),
              adulto("contar e olhar",
                     "Conte devagar, e peça que ela escolha a sua folha antes de sair. A ideia da unidade está na história: <b>uma coisa só, por um minuto, em silêncio</b>. "
                     "A história é da coleção; o diário de natureza, como hábito, vem de Charlotte Mason."), "--d-natureza")

    c = f"""<div class="miolo">{titulo("Meu registro de hoje", "uma página do diário, para repetir toda semana", 26)}
      <div class="centro" style="margin:2mm 0 0">{tira(["lapis_cor", "lupa", "caderno"], "20mm", "5mm")}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:5mm">
        <div class="caixa" style="height:18mm"><div class="peq centro">data</div></div>
        <div class="caixa" style="height:18mm"><div class="peq centro">lugar</div></div>
        <div class="caixa" style="height:18mm"><div class="peq centro">como está o tempo</div></div></div>
      <div class="caixa" style="margin-top:5mm;height:104mm"><div class="peq centro">o que eu olhei, desenhado grande</div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:5mm">
        <div class="caixa" style="height:30mm"><div class="peq centro">o nome (se eu souber)</div></div>
        <div class="caixa" style="height:30mm"><div class="peq centro">quantas eu vi? que cores?</div></div></div></div>
      {adulto("o registro",
              "Fotocopie esta página, se quiser, ou copie o modelo no caderno de natureza. Ela completa o que conseguir; escreva por ela o que ela ditar. <b>Nunca corrija o desenho.</b> "
              "Se ela não souber o nome, escreva “não sei” e procurem depois num livro ou numa pesquisa.")}"""
    L.add(c, aba="--d-natureza")

    itens = [(img("lupa", "22mm"), "Sentar no lugar escolhido e ficar quieta"),
             (img("olho", "26mm"), "Olhar: o que tem de mais perto? E de mais longe?"),
             (img("orelha", "20mm"), "Escutar: quantos sons diferentes? De onde vêm?"),
             (img("mao", "20mm"), "Tocar (só o que é seguro): liso, áspero, mole, duro?"),
             (img("nariz", "20mm"), "Cheirar com cuidado: tem cheiro? Qual?"),
             (img("caderno", "20mm"), "Fechar os olhos e contar uma coisa que lembra")]
    passos6(L, "Passeio dos cinco sentidos", "olhar, escutar, tocar e cheirar, devagar", itens,
            adulto("os sentidos",
                   "Não prove nada que encontrar. Para o <b>tato</b>, escolha folhas lisas e pedras; fuja de plantas desconhecidas (algumas queimam ou coçam). "
                   "O <b>cheiro</b> é com cuidado: uma folha amassada de erva-cidreira ou de hortelã, se houver. Termine pedindo que ela conte, de olhos fechados, o que lembra: é o jeito mais seguro de saber o que ela guardou."),
            "--d-natureza",
            cena([("folha_carvalho", 34, 14, 6, -10), ("flor_rosa", 36, 62, 0), ("pinha", 28, 112, 12, 8), ("folha_bordo", 34, 142, 2, 14),
                  ("pena", 26, 40, 56, -20), ("pedra", 30, 90, 58), ("raminho", 36, 126, 60, -5)], 92))

    sem = "".join(f'<div class="caixa" style="height:46mm"><div class="peq centro">{d}</div></div>' for d in ("domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"))
    c = f"""<div class="miolo">{titulo("O tempo da semana", "olhar pela janela e desenhar o céu de cada dia", 26)}
      <div class="centro" style="margin:3mm 0">{tira(["sol", "nuvem", "nuvem_chuva", "arco_iris", "lua_cheia"], "26mm", "2mm")}</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:4mm">{sem}
        <div class="caixa" style="height:46mm"><div class="peq centro">o que mudou?</div></div></div></div>
      {adulto("o tempo",
              "Uma vez por dia, no mesmo horário, ela olha o céu pela janela e desenha o que vê: sol, nuvens, chuva, noite. Não é previsão do tempo: é <b>olhar com regularidade</b>. "
              "No fim da semana, pergunte o que mudou e o que ficou igual.")}"""
    L.add(c, aba="--d-natureza")

    itens = [dict(pt="folha", mot="folha", en="leaf", fr="feuille", la="folium", dica="cai da árvore; tem nervuras"),
             dict(pt="pedra", mot="pedra", en="stone", fr="pierre", la="lapis", dica="dura, fria; fica no chão"),
             dict(pt="pena", mot="pena", en="feather", fr="plume", la="penna", dica="cai das aves; leve"),
             dict(pt="gota", mot="gota", en="drop", fr="goutte", la="gutta", dica="de chuva ou de orvalho"),
             dict(pt="nuvem", mot="nuvem", en="cloud", fr="nuage", la="nubes", dica="de água, no céu"),
             dict(pt="sol", mot="sol", en="sun", fr="soleil", la="sol", dica="dá luz e calor"),
             dict(pt="lua", mot="lua", en="moon", fr="lune", la="lūna", dica="aparece à noite, e às vezes de dia"),
             dict(pt="galho", mot="raminho", en="twig", fr="brindille", la="ramus", dica="sai do tronco"),
             dict(pt="flor", mot="florzinha_rosa", en="flower", fr="fleur", la="flōs", dica="vira fruto, depois")]
    cartoes(L, "o diário da natureza", itens, "Volume 6 · Natureza")

    diario(L, "Meu primeiro diário", "desenhar a mesma coisa em duas semanas", ["a primeira semana", "uma semana depois", "o que mudou", "o que eu quero olhar de novo"], "--d-natureza",
           "Escolha uma folha, uma flor ou uma pedra do lugar de olhar e desenhe nos dois primeiros quadros, com uma semana de intervalo. Nos outros dois, ela desenha ou conta o que mudou e o que quer olhar de novo. Escreva a data de cada um.",
           faixa=["folha_fina", "folha_coracao", "flor_rosa", "pedra"])



# ================================================================== U2 AVES DO QUINTAL

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · Aves do quintal", aba="--d-musica",
        pergunta="Quem canta lá fora, e como é essa ave quando a gente olha de perto?",
        duracao="Três fins de semana · um passeio de escuta e dois de olhar · 20 a 30 minutos.",
        objetivos=["Olhar com calma pranchas antigas do sabiá, do bem-te-vi e do beija-flor.", "Dizer três coisas de cada ave: cor, forma do bico, onde está pousada.",
                   "Escutar as aves do quintal e contar quantos cantos diferentes ouve.", "Aprender os nomes: sabiá, bem-te-vi, beija-flor.", "Conhecer uma poesia brasileira com o sabiá."],
        repertorio="<b>Aves:</b> sabiá-laranjeira, bem-te-vi, beija-flor. <b>Palavras:</b> ave, pena, bico, asa, ninho, canto. <b>Poesia:</b> <i>Canção do exílio</i>, de Gonçalves Dias (1843). "
                   "<b>Línguas:</b> <i>bird · l’oiseau · avis</i>; <i>feather · la plume · penna</i>.",
        materiais="Caderno de natureza, lápis de cor, uma garrafa de água; se tiver, um binóculo de brinquedo ou de verdade; as pranchas deste livro.",
        vida="Pôr água fresca num prato raso no quintal ou na janela para as aves; escutar os sons logo ao acordar.",
        etapas=[["Escutar o quintal por três minutos, de olhos fechados.", "Olhar a prancha do sabiá em silêncio.", "Contar quantos cantos diferentes ouviu."],
                ["Olhar o bem-te-vi e o beija-flor, um de cada vez.", "Comparar os bicos: qual é fino? qual é forte?", "Procurar uma ave de verdade na janela ou no quintal."],
                ["Ouvir a poesia do sabiá e dizer o que imagina.", "Desenhar, no caderno, a ave de que mais gostou.", "Contar para alguém como ela é."]],
        indicadores=["Diz a cor da barriga e das costas de cada ave.", "Aponta o bico e compara um com o outro.", "Escuta e conta pelo menos dois cantos diferentes.",
                     "Diz o nome de uma ave que viu ou ouviu.", "Imita o canto do bem-te-vi com a voz.", "Lembra de um detalhe de uma prancha com o livro fechado."],
        interesse="ouvir as aves no mesmo horário todo dia por uma semana e anotar quantos cantos diferentes escutou.",
        dificil="olhar só uma prancha, só o bico, e dizer o que o bico faz.",
        alerta="Olhar e escutar bastam: nada de pegar filhote, tocar em ninho ou alimentar com pão. Lave as mãos depois de mexer em comedouro ou bebedouro."))

    apreciar(L, "sabia", "O sabiá-laranjeira", "uma prancha antiga, de Descourtilz, com um sabiá num galho com espinhos",
             ["De que cor é a cabeça? E as costas?", "De que cor é a barriga? E o peito, tem manchinhas?", "Como é o bico: curto ou comprido? Fino ou grosso?",
              "Como são as pernas e os pés? Como eles seguram o galho?", "Como é o galho? Você vê espinhos? E folhas, de que cor?"],
             "Esta é a ave <b>sabiá-laranjeira</b>, <i>Turdus rufiventer</i> no rótulo da prancha: costas e cabeça marrons, barriga cor de laranja, peito claro com pintinhas. É a ave símbolo do Brasil. "
             "A prancha é a de número 26 do livro <i>Ornithologie brésilienne</i>, de Jean-Théodore Descourtilz, que anotou que o sabiá é comum em toda parte, até nos jardins perto das casas, "
             "e que canta no fim do dia, mesmo depois de uma tempestade. Na prancha inteira há outra ave (o pavó); aqui aparece só o sabiá. Peça que ela feche o livro e diga <b>três coisas</b> sobre ele.",
             "olhar e comparar", "--d-musica", w=140, h=100)

    poema(L, "Canção do exílio", "Gonçalves Dias, 1843",
          ["Minha terra tem palmeiras,<br>Onde canta o Sabiá;<br>As aves, que aqui gorjeiam,<br>Não gorjeiam como lá."],
          cena([("palma", 40, 10, 4, -8), ("pena", 26, 60, 18, 14), ("raminho", 40, 96, 8), ("palma", 36, 128, 14, 10)], 52),
          adulto("uma poesia para escutar",
                 "Leia só a estrofe, devagar, duas vezes, e pergunte: <b>quem canta na poesia?</b> O poeta escreveu estes versos longe do Brasil, com saudade. Para ela, basta a música das palavras. "
                 "<i>Gorjear</i> é cantar como as aves. Gonçalves Dias morreu em 1864, e a poesia é de domínio público. No dia seguinte, peça que ela diga a estrofe de memória, ou o pedacinho que ficou."),
          aba="--d-musica")

    apreciar(L, "bemtevi", "O bem-te-vi", "uma prancha de 1920, com uma ave amarela num galho",
             ["De que cor é a barriga? E as costas?", "O que tem na cabeça: listras? De que cores?", "Como é o bico: curto ou comprido? Fino ou grosso?", "Em que a ave está pousada? Como são as folhas?",
              "Para que lado ela olha?"],
             "O nome vem do canto, que parece dizer <b>“bem-te-vi”</b>: peça que ela diga a palavra e depois tente imitar o canto. É uma das aves mais comuns nas cidades e nos quintais do Brasil. "
             "O rótulo da prancha, de 1920, diz <i>Bienteveo Tyrant</i> (<i>Pitangus bolivianus</i>), e o livro mantém o nome da prancha. Procure no quintal uma ave amarela de cabeça listrada.",
             "olhar e escutar", "--d-musica", w=105, h=150)

    apreciar(L, "beijaflor", "O beija-flor", "uma prancha de Gould, de 1861, com três aves num ramo de flores",
             ["Quantos beija-flores você vê? Em que posição está cada um?", "De que cor são as costas? E a barriga?", "Como é o bico: curto ou comprido? Fino ou grosso?",
              "De que cor são as flores? Onde os beija-flores estão?", "O que as asas parecem estar fazendo?"],
             "Os beija-flores se alimentam do néctar das flores, com o bico fino e comprido, e ficam parados no ar batendo as asas muito depressa, dezenas de vezes por segundo. "
             "Só existem nas Américas, e há muitas espécies no Brasil. Esta prancha mostra três beija-flores em posições diferentes, num ramo de flores vermelhas. É uma litografia colorida à mão, de John Gould e Henry Richter. "
             "Se tiver flores no quintal, vale ficar um tempo olhando quem visita.",
             "olhar de perto", "--d-musica", w=88, h=165)

    itens = [(img("bebedouro", "26mm"), "Água fresca: pôr um prato raso com água, num lugar seguro"),
             (img("casinha", "22mm"), "Casa: uma casinha de passarinho, num poste ou árvore"),
             (img("ninho", "26mm"), "Ninho: olhar de longe, sem tocar"),
             (img("ovo", "20mm"), "Ovos: bem escondidos, nunca mexer"),
             (img("pena", "20mm"), "Penas: juntar as que caíram, olhar de perto"),
             (img("girassol", "22mm"), "Comida: sementes e frutas, só se a ave for de comedouro")]
    passos6(L, "O que as aves precisam", "água, casa, ninho e um quintal sossegado", itens,
            adulto("cuidar das aves",
                   "Não precisa de nada caro: um prato raso com água fresca (trocada todo dia) já atrai as aves. Nunca dê pão ou comida de casa. Olhe os ninhos <b>de longe</b>: mexer neles assusta os pais e pode levá-los a abandonar os filhotes. "
                   "Se ela achar um filhote no chão, chame um adulto. Lave as mãos depois de mexer em bebedouro ou comedouro."),
            "--d-musica",
            cena([("casinha", 38, 10, 4), ("pena", 26, 62, 20, -10), ("ninho", 44, 96, 8), ("ovo", 24, 144, 28, 8), ("raminho", 40, 56, 54), ("folha_carvalho", 28, 12, 54, -20)], 84))

    linhas = "".join(f'<tr><td style="width:60mm;height:15mm;font-size:13pt">{a}</td><td style="width:28mm"></td><td style="width:28mm"></td><td></td></tr>'
                     for a in ("sabiá", "bem-te-vi", "beija-flor", "pombo", "outra ave: ______________", "outra ave: ______________"))
    c = f"""<div class="miolo">{titulo("Quem canta no quintal?", "uma folha para marcar o que vi e o que ouvi", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["pena", "ninho", "ovo", "casinha"], "24mm", "4mm")}</div>
      <table class="tab" style="margin-top:4mm"><tr><th>Ave</th><th>Vi</th><th>Ouvi</th><th>Onde estava / o que fazia</th></tr>{linhas}</table>
      <div class="caixa" style="margin-top:6mm;height:56mm"><div class="peq centro">o canto de que mais gostei, em desenho (linhas para cima e para baixo, pontinhos, ondas…)</div></div></div>
      {adulto("escutar",
              "Sentem-se por <b>cinco minutos</b>, de manhã cedo ou no fim da tarde. A cada som, ela marca na folha. Se não souber o nome da ave, ela dá um nome só dela (“a que faz tchi-tchi”) e vocês descobrem depois. "
              "Repita o mesmo lugar e horário em outros dias e compare o que mudou.")}"""
    L.add(c, aba="--d-musica")

    diario(L, "Minhas aves", "desenhar as aves que ela viu e ouviu", ["a ave que eu mais gostei", "o bico dela", "o canto dela", "onde ela estava"], "--d-musica",
           "Peça que desenhe a ave de que mais gostou, em cima, e depois só o bico, o canto (em rabisco) e o lugar. Escreva a data e o nome, ou “não sei o nome”.",
           faixa=["pena", "ninho", "ovo", "casinha"])



# ================================================================== U3 INSETOS E PEQUENOS BICHOS

# recortes da prancha de Merian (x, y, largura, altura em pixels do JPEG tratado)
LAGARTA = (230, 340, 390, 180)
CASULO = (520, 780, 160, 220)
BORBOLETA = (760, 1500, 340, 280)


def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · Insetos e pequenos bichos", aba="--d-artes",
        pergunta="Como uma lagarta vira borboleta, e quantos bichinhos moram perto de nós?",
        duracao="Dois fins de semana · um passeio com lupa e um de olhar a prancha · 20 a 30 minutos.",
        objetivos=["Olhar com calma a prancha de Maria Sibylla Merian.", "Reconhecer a lagarta, o casulo (a pupa) e a borboleta, e dizer em que ordem aparecem.",
                   "Procurar bichinhos de verdade no quintal, com lupa, sem pegar.", "Contar as patas de um inseto (seis) e de uma aranha (oito).", "Nomear: inseto, lagarta, casulo, asa, perna, antena."],
        repertorio="<b>Obra:</b> Maria Sibylla Merian (1647–1717), <i>Metamorphosis insectorum Surinamensium</i> (1705). <b>Palavras:</b> lagarta, casulo, borboleta, asa, antena, perna. "
                   "<b>Línguas:</b> <i>butterfly · le papillon · papilio</i>; <i>insect · l’insecte · insectum</i>.",
        materiais="Uma lupa, caderno de natureza, lápis de cor, um pote transparente com furinhos na tampa para olhar um bichinho por pouco tempo e soltá-lo no mesmo lugar.",
        vida="Olhar as plantas do quintal e as da feira em busca de lagartas e folhas comidas; soltar sempre o bicho onde foi achado.",
        etapas=[["Olhar a prancha de Merian em silêncio.", "Achar a lagarta, o casulo e a borboleta.", "Dizer qual vem primeiro."],
                ["Ordenar os três recortes (lagarta, casulo, borboleta).", "Sair com a lupa e procurar bichinhos num canto do quintal.", "Contar quantas patas tem um inseto."],
                ["Desenhar um bichinho que viu de perto.", "Comparar com a aranha: quantas patas?", "Contar para alguém o caminho da lagarta até a borboleta."]],
        indicadores=["Aponta a lagarta, o casulo e a borboleta na prancha.", "Ordena os três recortes sem ajuda.", "Usa a lupa e diz o que viu de perto.",
                     "Diz que o inseto tem seis patas.", "Solta o bichinho onde o achou.", "Desenha o bichinho com detalhes reais (antenas, asas)."],
        interesse="criar, com um adulto, uma lagarta de verdade numa caixa com folhas, e ver o que acontece (e soltar a borboleta depois).",
        dificil="olhar só a lagarta da prancha, por um minuto, e dizer como ela é.",
        alerta="Não pegue lagarta peluda nem bicho desconhecido: algumas queimam. Olhe com a lupa, de longe, e lave as mãos depois de mexer em terra e plantas."))

    historia6(L, "A lagarta que virou borboleta", "uma história curta, para contar antes de olhar a prancha",
              ["Numa folha verde, bem cedinho, nasceu uma lagarta pequena. Ela só sabia fazer uma coisa: comer. Comeu a folha da esquerda, comeu a folha da direita, e foi ficando grande, grande, grande.",
               "Um dia, a lagarta sentiu sono. Subiu num galho, pendurou-se de cabeça para baixo e ficou quietinha, bem quietinha. Por fora, parecia uma folha seca, ou uma bolsinha verde e dourada. Era o casulo.",
               "Passaram os dias. Dentro do casulo, a lagarta ia mudando, sem ninguém ver. Até que, numa manhã de sol, o casulo se abriu, e saiu de dentro dele uma borboleta, com as asas ainda molhadas e dobradinhas. Ela abriu as asas devagar, esperou secar, e voou para a flor mais perto."],
              tira(["lagarta", "casulo", "borboleta"], "36mm", "5mm"),
              cena([("flor_rosa", 40, 10, 20), ("lagarta", 40, 58, 40), ("casulo", 28, 100, 10), ("borboleta", 42, 128, 30, 10), ("folha_carvalho", 30, 140, 4, 20), ("joaninha", 22, 8, 4, -8)], 82),
              adulto("contar e perguntar",
                     "Conte devagar e peça que ela acompanhe, com os dedos, as três mudanças: lagarta, casulo, borboleta. A história é da coleção e resume o que Maria Sibylla Merian mostrou há mais de 300 anos. "
                     "Não é preciso falar em ovo nem em pupa, mas, se ela perguntar, diga que antes da lagarta há um ovo bem pequeno."), "--d-artes")

    apreciar(L, "merian_frangipani", "A lagarta, o casulo e a borboleta", "Maria Sibylla Merian, 1705 · uma prancha com uma planta florida",
             ["Quantas borboletas você vê? Onde estão?", "Onde está a lagarta? De que cor ela é?", "Você acha o casulo? Onde ele está pendurado?", "De que cor são as flores? E as folhas?",
              "As duas borboletas são iguais? O que muda?"],
             "Maria Sibylla Merian foi uma naturalista e artista alemã. Em 1699 viajou ao Suriname, na América do Sul, com a filha Dorothea, para olhar de perto os insetos, e publicou o livro em 1705. "
             "Ela desenhava <b>a planta onde o bicho vive</b>, a lagarta, o casulo e a borboleta, tudo na mesma página, para mostrar como o inseto muda. A gravura é de P. Sluyter, como se lê na prancha. "
             "Peça que ela conte, com o dedo, o caminho: <b>lagarta, casulo, borboleta</b>.",
             "olhar e contar", "--d-artes", w=100, h=165)

    cel = "".join(f'<div style="border:0.6pt dashed var(--linha);padding:3mm;margin:0 auto 7mm;width:{mm + 6}mm;text-align:center;line-height:0">'
                  f'{recorte("merian_frangipani", caixa, mm)}</div>'
                  for caixa, mm in ((BORBOLETA, 70), (LAGARTA, 110), (CASULO, 38)))
    c = f"""<div class="miolo">{titulo("Qual vem primeiro?", "cortar os três cartões e ordenar: da lagarta à borboleta", 25)}
      <div style="margin-top:10mm">{cel}</div></div>
      {adulto("ordenar",
              "Os três recortes são partes da prancha de Merian, sem nenhum retoque. Cole numa cartolina, recorte nas linhas tracejadas, embaralhe e peça que ela ponha em ordem. Não existe só uma pergunta certa: peça que ela conte o que acha que a lagarta faz "
              "dentro do casulo. Repare: faltam aqui o ovo, que vem antes, e outras mudanças que a prancha não mostra.", credito_prancha("merian_frangipani"))}"""
    L.add(c, aba="--d-artes")

    itens = [(img("lupa", "22mm"), "Pegar a lupa e escolher um canto do quintal"),
             (img("folha_carvalho", "22mm"), "Olhar as folhas: alguma tem furos? Há bichinhos embaixo?"),
             (img("pedra", "20mm"), "Olhar embaixo de uma pedra ou de um vaso (e pôr de volta)"),
             (img("flor_rosa", "22mm"), "Olhar uma flor: quem visita?"),
             (img("teia", "22mm"), "Olhar um galho ou um canto: há casulo, ovinhos ou teia?"),
             (img("joaninha", "20mm"), "Contar as pernas de um bichinho e desenhar")]
    passos6(L, "Caça aos bichinhos", "olhar de pertinho, com a lupa, sem pegar", itens,
            adulto("o passeio",
                   "Não é preciso ir longe: um canto de jardim, um vaso ou uma calçada bastam. <b>Olhar, não pegar.</b> Se ela quiser olhar um bichinho de perto, ponha-o num pote transparente por poucos minutos "
                   "e solte-o no mesmo lugar. Fuja de lagartas peludas, abelhas e vespas. Conte as pernas: <b>inseto tem seis; aranha tem oito</b> (e aranha não é inseto)."),
            "--d-artes",
            cena([("caracol", 40, 6, 24), ("minhoca", 40, 52, 30), ("abelha", 38, 96, 6), ("formiga", 34, 134, 28), ("besouro", 30, 70, 56, -10), ("libelula", 40, 118, 52, 6)], 90))

    linhas = "".join(f'<tr><td style="width:30mm;text-align:center;height:22mm">{img(m, "18mm")}</td><td style="width:44mm;font-size:13pt">{a}</td><td style="width:34mm;text-align:center;font-size:15pt">{b}</td><td></td></tr>'
                     for m, a, b in (("formiga", "formiga", "6 patas"), ("borboleta", "borboleta", "6 patas"), ("besouro", "besouro", "6 patas"), ("aranha", "aranha", "8 patas"),
                                     ("lupa", "outro bichinho: _________", "___ patas")))
    c = f"""<div class="miolo">{titulo("Seis patas ou oito?", "contar as patas dos bichinhos", 26)}
      <table class="tab" style="margin-top:6mm"><tr><th></th><th>Bicho</th><th>Patas</th><th>Como é? (cor, antenas, asas)</th></tr>{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["abelha", "libelula", "joaninha", "aranha"], "30mm", "4mm")}</div></div>
      {adulto("contar",
              "Os insetos têm <b>seis patas</b>, três pares, e o corpo dividido em três partes (cabeça, tórax e abdômen). As aranhas têm <b>oito patas</b> e não são insetos. "
              "Se ela encontrar um bichinho que não esteja na lista, ela conta as patas de verdade, com a lupa, e anota.")}"""
    L.add(c, aba="--d-artes")

    itens = [dict(pt="formiga", mot="formiga", en="ant", fr="fourmi", la="formīca", dica="mora em formigueiro; carrega folhas"),
             dict(pt="abelha", mot="abelha", en="bee", fr="abeille", la="apis", dica="faz mel e visita as flores"),
             dict(pt="joaninha", mot="joaninha", en="ladybug", fr="coccinelle", la=None, dica="vermelha com pintinhas"),
             dict(pt="caracol", mot="caracol", en="snail", fr="escargot", la="cochlea", dica="leva a casa nas costas"),
             dict(pt="borboleta", mot="borboleta", en="butterfly", fr="papillon", la="papiliō", dica="começou como lagarta"),
             dict(pt="aranha", mot="aranha", en="spider", fr="araignée", la="arāneus", dica="oito patas; faz teia"),
             dict(pt="minhoca", mot="minhoca", en="worm", fr="ver de terre", la="vermis", dica="vive na terra úmida"),
             dict(pt="besouro", mot="besouro", en="beetle", fr="scarabée", la="scarabaeus", dica="tem asas duras por fora"),
             dict(pt="libélula", mot="libelula", en="dragonfly", fr="libellule", la=None, dica="voa perto da água")]
    cartoes(L, "bichinhos", itens, "Volume 6 · Bichinhos")

    diario(L, "Meus bichinhos", "desenhar o que ela encontrou com a lupa", ["o bichinho que achei", "onde ele estava", "quantas patas?", "o caminho da lagarta à borboleta"], "--d-artes",
           "Desenhe ou cole aqui o que ela viu na caça aos bichinhos, com a data e o lugar. Se ela quiser, copie o que ela disser sobre cada desenho ao lado dele.",
           faixa=["joaninha", "abelha", "caracol", "borboleta"])



# ================================================================== U4 ÁRVORES E FOLHAS

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · Árvores e folhas", aba="--d-memoria",
        pergunta="Como é uma árvore por fora, de pertinho, e o que dá para fazer com as folhas que caem?",
        duracao="Dois fins de semana · um passeio até uma árvore e um de coleção de folhas · 20 a 30 minutos.",
        objetivos=["Escolher <b>uma</b> árvore perto de casa e voltar a ela mais de uma vez.", "Nomear as partes: raiz (escondida), tronco, galho, folha, flor, fruto.",
                   "Olhar a casca com a ponta dos dedos e passar giz de cera sobre ela, no papel.", "Juntar folhas <b>caídas</b> e separar por forma, tamanho e cor.",
                   "Dizer se a árvore tem folhas, flores ou frutos em cada visita."],
        repertorio="<b>Palavras:</b> árvore, tronco, casca, galho, folha, nervura, raiz, fruto. <b>Línguas:</b> <i>tree · l’arbre · arbor</i>; <i>leaf · la feuille · folium</i>; <i>branch · la branche · ramus</i>.",
        materiais="Papel fino, giz de cera sem o papel, lápis de cor, uma sacolinha de pano para folhas caídas, um pedaço de barbante para medir o tronco, uma lupa, o caderno de natureza.",
        vida="Passar pela mesma árvore a caminho da escola ou da padaria e dizer uma coisa que mudou; separar as folhas secas do vaso em casa.",
        etapas=[["Ir até a árvore escolhida e ficar um minuto quieta, olhando.", "Passar a mão no tronco e dizer como é a casca.", "Abraçar o tronco e ver se os braços dão a volta."],
                ["Fazer o desenho da casca: papel no tronco e giz por cima.", "Juntar folhas caídas e olhar a nervura de cada uma.", "Separar as folhas em montinhos (grande e pequena, lisa e serrilhada)."],
                ["Colar ou desenhar as folhas no caderno.", "Voltar à árvore uma semana depois e contar o que mudou.", "Dar um nome à árvore e contar a alguém por quê."]],
        indicadores=["Diz o nome de pelo menos três partes da árvore.", "Descreve a casca com palavras (áspera, lisa, rachada, mole).", "Junta só folhas que já caíram.",
                     "Separa as folhas por um critério e explica qual.", "Percebe o que mudou na árvore de uma visita para outra.", "Volta a falar da árvore sem ser lembrada."],
        interesse="medir a sombra da árvore em horas diferentes do dia, ou procurar quantas espécies de folha há numa quadra.",
        dificil="olhar uma folha só, grande, por um minuto, e passar o dedo pela nervura.",
        alerta="Não suba em árvore desconhecida, não coma frutos nem sementes que achar e evite a seiva (algumas plantas queimam a pele ou coçam). Lave as mãos depois."))

    historia6(L, "A árvore da esquina", "uma história curta, para contar antes de sair",
              ["Na esquina da rua da Marina havia uma árvore grande. Marina passava por ela todo dia e nunca tinha reparado. Um dia, o papai disse: “Vamos conhecer essa árvore?” Eles chegaram bem pertinho, e Marina passou a mão no tronco. “É áspero, e tem uns buraquinhos”, ela disse. O papai deu o barbante: “Vamos ver quantos barbantes de tronco cabem em volta?” Deu duas voltas e meia.",
               "Depois, Marina olhou para cima. Os galhos saíam do tronco e se abriam em outros galhos menores, e nos menores, as folhas. Algumas folhas estavam no chão. Ela pegou três, e cada uma era diferente: uma grande e lisa, uma pequena e cheia de dentinhos, uma amarelada nas pontas. “Cada folha tem um jeito”, disse Marina.",
               "Em casa, ela colou as três folhas no caderno e escreveu embaixo: <i>a árvore da esquina</i>. Na semana seguinte voltou lá e viu que tinha uma folha nova, bem verdinha, num galho de baixo. “Ela está crescendo”, disse Marina. “Todo dia um pouquinho”, respondeu o papai."],
              tira(["arvore_verao", "folha_carvalho", "bolota"], "34mm", "4mm"),
              cena([("tronco", 38, 8, 6), ("folha_carvalho", 32, 54, 14, -12), ("folha_bordo", 32, 92, 4, 8), ("folha_coracao", 30, 128, 16, -6), ("pinha", 26, 60, 52), ("bolota", 22, 100, 54), ("folha_seca", 26, 134, 54, 20)], 84),
              adulto("contar e perguntar",
                     "Conte devagar, e peça que ela escolha uma árvore perto de casa para ser a <b>dela</b>. Pare em “cada folha tem um jeito” e pergunte o que ela acha que cada folha conta. A história é da coleção."), "--d-memoria")

    itens = [(img("arvore_verao", "24mm"), "Ir até a árvore escolhida e ficar quieta"),
             (img("folha_carvalho", "22mm"), "Olhar bem uma folha: como é a nervura? E a borda?"),
             (img("raminho", "24mm"), "Seguir um galho com o dedo, do tronco até as folhas"),
             (img("bolota", "20mm"), "Procurar no chão: folhas, frutos, gravetos caídos"),
             (img("lupa", "20mm"), "Olhar a casca de perto: tem buraquinhos? Tem algum bichinho?"),
             (img("tronco", "22mm"), "Abraçar o tronco e dizer o que sentiu")]
    passos6(L, "Passeio até a árvore", "olhar uma árvore só, de perto e de longe", itens,
            adulto("o passeio",
                   "Escolha uma árvore que a Marina possa visitar de novo: da calçada, da praça, do quintal. O tempo importa mais que o número de árvores. "
                   "Peça que ela olhe de <b>longe</b> (a forma da copa, a cor) e de <b>perto</b> (a casca, uma folha). Colete só o que já caiu; não arranque folhas nem galhos."),
            "--d-memoria",
            cena([("arvore_primavera", 50, 6, 4), ("arvore_verao", 50, 60, 0), ("arvore_outono", 50, 114, 4), ("folha_bordo", 26, 20, 60, 12), ("folha_seca", 26, 94, 62, -14), ("bolota", 20, 138, 62)], 90))

    c = f"""<div class="miolo">{titulo("O desenho da casca", "passar o giz sobre o papel, contra o tronco", 26)}
      <div class="centro" style="margin:3mm 0">{tira(["tronco", "pinha", "tronco"], "28mm", "8mm")}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm">{moldura_vazia("a casca da minha árvore", "86mm")}{moldura_vazia("a casca de outra árvore", "86mm")}</div>
      <div class="caixa" style="margin-top:6mm;height:50mm"><div class="peq centro">como é a casca? (áspera, lisa, com buracos, com listras…)</div></div></div>
      {adulto("frotagem",
              "Segure uma folha de papel fino contra o tronco e peça que ela passe o lado do giz de cera, sem o papel do giz, devagar, até a textura aparecer. Faça com duas árvores diferentes e compare. "
              "Escreva a data e o lugar atrás. Se o dia estiver difícil, a casca de uma só árvore já é uma boa atividade.")}"""
    L.add(c, aba="--d-memoria")

    c = f"""<div class="miolo">{titulo("Minha coleção de folhas", "colar ou contornar as folhas caídas", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["folha_carvalho", "folha_bordo", "folha_coracao", "folha_fina", "folha_seca"], "24mm", "3mm")}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;margin-top:4mm">{moldura_vazia("folha grande", "58mm")}{moldura_vazia("folha pequena", "58mm")}{moldura_vazia("folha de pontas", "58mm")}
        {moldura_vazia("folha lisa", "58mm")}{moldura_vazia("folha com dentinhos", "58mm")}{moldura_vazia("folha amarela ou seca", "58mm")}</div></div>
      {adulto("separar",
              "Ela cola ou contorna as folhas caídas que juntou, em cada quadro. Não precisa dar nome à folha: o critério é <b>forma, tamanho ou cor</b>. Peça que explique por que pôs cada folha num quadro. "
              "Se quiser, passe as folhas entre duas folhas de papel e ponha um livro por cima por alguns dias, para secarem sem enrolar.")}"""
    L.add(c, aba="--d-memoria")

    itens = [dict(pt="árvore", mot="arvore_verao", en="tree", fr="arbre", la="arbor", dica="tem raiz, tronco e copa"),
             dict(pt="tronco", mot="tronco", en="trunk", fr="tronc", la="truncus", dica="sustenta os galhos"),
             dict(pt="galho", mot="raminho", en="branch", fr="branche", la="ramus", dica="sai do tronco"),
             dict(pt="folha", mot="folha_coracao", en="leaf", fr="feuille", la="folium", dica="verde; tem nervuras"),
             dict(pt="raiz", mot="raiz_arvore", en="root", fr="racine", la="rādix", dica="fica escondida na terra"),
             dict(pt="flor", mot="flor_rosa", en="flower", fr="fleur", la="flōs", dica="depois vira fruto"),
             dict(pt="fruto", mot="maca", en="fruit", fr="fruit", la="frūctus", dica="guarda as sementes"),
             dict(pt="bolota", mot="bolota", en="acorn", fr="gland", la="glāns", dica="é o fruto do carvalho"),
             dict(pt="pinha", mot="pinha", en="pine cone", fr="pomme de pin", la=None, dica="guarda sementes entre as escamas")]
    cartoes(L, "as árvores", itens, "Volume 6 · Árvores")

    diario(L, "Minha árvore", "voltar à árvore e desenhar o que mudou", ["a árvore de longe", "uma folha de perto", "o que mudou", "o nome que eu dei"], "--d-memoria",
           "Desenhe a árvore na primeira visita e outra vez, uma semana depois, no mesmo lugar. Nos outros dois quadros, ela desenha uma folha de perto e dá um nome à árvore. Escreva a data de cada desenho.",
           faixa=["arvore_verao", "folha_bordo", "bolota", "folha_carvalho"])



# ================================================================== U5 SEMENTES

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · Sementes", aba="--d-vida",
        pergunta="O que tem dentro de uma semente, e o que acontece quando ela encontra água e luz?",
        duracao="Três fins de semana · um para plantar o feijão, um para observar todo dia e um para frutas e sementes.",
        objetivos=["Plantar um feijão no algodão úmido e olhar todo dia o que acontece.", "Dizer que a raiz aparece primeiro e depois o broto.", "Abrir frutas e achar as sementes.",
                   "Comparar sementes: grande e pequena, lisa e enrugada, clara e escura.", "Nomear em português (e, nos cartões, em inglês, francês e latim) nove frutas e sementes."],
        repertorio="<b>Palavras:</b> semente, feijão, raiz, broto, folha, fruta, caroço. <b>Línguas:</b> <i>seed · la graine · semen</i>; <i>apple · la pomme · mālum</i>; <i>pea · le pois · pisum</i>.",
        materiais="Feijão (de cozinha, seco), algodão, um copo transparente ou um potinho, água, uma janela com luz; frutas variadas (maçã, laranja, melancia, uva); uma lupa; o caderno de natureza.",
        vida="Guardar as sementes das frutas do almoço num pratinho; regar a plantinha de manhã; olhar o feijão antes de dormir.",
        etapas=[["Olhar os feijões secos: cor, forma, tamanho.", "Pôr um feijão no algodão úmido, no copo, perto da janela.", "Dizer o que acha que vai acontecer."],
                ["Olhar o feijão todo dia e desenhar o que mudou.", "Regar o algodão, sem encharcar.", "Contar em que dia apareceu a raiz."],
                ["Abrir uma fruta e achar as sementes, com a lupa.", "Comparar as sementes de duas frutas.", "Plantar uma semente num vaso e cuidar dela."]],
        indicadores=["Diz o que a semente precisa (água e um lugar iluminado).", "Olha o feijão todo dia sem ser lembrada.", "Descreve a raiz e o broto com palavras dela.",
                     "Abre uma fruta e acha as sementes sozinha.", "Compara duas sementes (tamanho, cor, jeito).", "Cuida da planta: rega, olha, conta."],
        interesse="plantar sementes de frutas diferentes, em potinhos, e comparar quais nascem primeiro e quais demoram mais.",
        dificil="olhar só o feijão seco, de pertinho, e dizer como ele é por fora.",
        alerta="Sementes pequenas e feijão seco engasgam: só com um adulto por perto, e longe de quem ainda põe tudo na boca. Não coma semente que não conhece e lave as mãos depois de mexer em terra."))

    historia6(L, "O feijão da Marina", "uma história curta, para contar antes de plantar",
              ["Marina achou um feijão no fundo do pacote da cozinha. Era pequeno, marrom e duro. “Será que isto é um bichinho?”, ela perguntou. “É uma semente”, disse o papai. “Dentro dele mora uma plantinha, bem pequena, dormindo.” “E como acorda?” “Com água e com luz.”",
               "Marina molhou um algodão, pôs o feijão em cima, no copo, e deixou na janela. No dia seguinte, nada. No outro, também nada. Mas no terceiro dia, o feijão estava mais gordinho, e do lado dele saía uma pontinha branca. “É a raiz”, disse o papai. “Ela vai primeiro, para buscar água.”",
               "Dias depois, o feijão abriu e saiu dele uma coisinha verde, dobrada, que foi subindo em direção à luz. Marina desenhou o feijão todo dia no caderno. No fim da semana, ela tinha uma plantinha de verdade. “Eu não fiz nada”, disse ela. “Você cuidou”, disse o papai. “O resto, a semente já sabia.”"],
              tira(["feijao", "gota", "sol", "plantinha"], "28mm", "4mm"),
              cena([("feijao", 34, 4, 28), ("feijao_raiz", 34, 46, 14), ("feijao_broto", 36, 90, 10), ("plantinha", 40, 132, 4), ("sol", 20, 6, 4), ("gota", 14, 92, 64)], 80),
              adulto("contar e perguntar",
                     "Conte devagar, mostrando um feijão seco de verdade. Peça que ela adivinhe o que vai acontecer. Os dias exatos variam com o calor e o feijão: o importante é <b>olhar todo dia</b>. A história é da coleção."), "--d-vida")

    sequencia(L, "Do feijão à planta", "cortar os quatro cartões e ordenar",
              [("a semente dormindo", img("feijao", "38mm", "margin:10mm auto 0")), ("aparece a raiz", img("feijao_raiz", "40mm", "margin:2mm auto 0")),
               ("sai o broto", img("feijao_broto", "42mm", "margin:2mm auto 0")), ("a plantinha cresce", img("plantinha", "42mm", "margin:2mm auto 0"))],
              adulto("ordenar",
                     "Corte os cartões e embaralhe. Peça que ela ponha em ordem e conte, com as palavras dela, o que a semente faz em cada um. Depois, compare com o feijão que ela plantou de verdade: está em qual cartão hoje?",
                     estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"), aba="--d-vida")

    itens = [(img("feijao", "24mm"), "Escolher um feijão e olhar de perto"),
             (img("tigela", "22mm"), "Molhar o algodão e pôr no fundo do copo"),
             (img("feijao", "20mm"), "Pôr o feijão em cima do algodão úmido"),
             (img("sol", "20mm"), "Deixar o copo perto da janela, com luz"),
             (img("regador", "24mm"), "Regar todo dia um pouquinho, sem encharcar"),
             (img("lupa", "20mm"), "Olhar todo dia e desenhar o que mudou")]
    passos6(L, "Plantar um feijão", "algodão, água, luz e paciência", itens,
            adulto("o experimento",
                   "Use feijão de cozinha, seco e inteiro (alguns lotes não nascem: ponha dois ou três por segurança). Mantenha o algodão úmido, não encharcado. "
                   "Em geral a raiz aparece em poucos dias e o broto em cerca de uma semana. Quando a planta crescer, passe para um vaso com terra. <b>Peça que ela adivinhe antes</b> de cada etapa."),
            "--d-vida",
            cena([("vaso", 40, 8, 26), ("plantinha", 44, 52, 6), ("regador", 44, 100, 18), ("gota", 12, 148, 22), ("gota", 10, 156, 40), ("feijao", 26, 132, 62, 14)], 84))

    dias = "".join(f'<div class="caixa" style="height:40mm"><div class="peq centro">dia {i}</div></div>' for i in range(1, 11))
    c = f"""<div class="miolo">{titulo("O diário do feijão", "um quadro para cada dia, desenhando o que se vê", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["feijao", "feijao_raiz", "feijao_broto", "plantinha"], "22mm", "6mm")}</div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:4mm">{dias}</div>
      <div class="caixa" style="margin-top:8mm;height:62mm"><div class="peq centro">em que dia apareceu a raiz? E o broto? O que mais me chamou a atenção?</div></div></div>
      {adulto("registrar",
              "Ela desenha o feijão uma vez por dia, no mesmo horário. Nos dias em que parecer que nada mudou, também vale desenhar: é assim que se percebe a mudança. "
              "Escreva por ela, com as palavras dela, o que disser.")}"""
    L.add(c, aba="--d-vida")

    linhas = "".join(f'<tr><td style="height:16mm;width:50mm;font-size:13pt">{a}</td><td style="width:36mm"></td><td style="width:40mm"></td><td></td></tr>'
                     for a in ("maçã", "laranja", "melancia", "uva", "pera", "outra fruta: ____________"))
    c = f"""<div class="miolo">{titulo("Quantas sementes tem a fruta?", "abrir, olhar com a lupa, contar", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["maca_cortada", "laranja", "melancia", "uva"], "26mm", "3mm")}</div>
      <table class="tab" style="margin-top:4mm"><tr><th>Fruta</th><th>Quantas sementes?</th><th>Cor e tamanho</th><th>Como são? (lisa, achatada, dura…)</th></tr>{linhas}</table></div>
      {adulto("contar",
              "Ofereça um pedaço da fruta e peça que ela procure as sementes: algumas têm uma só (como o caroço do pêssego), outras têm muitas (melancia). A fruta é uma embalagem que a planta faz para as sementes. "
              "Guarde algumas sementes secas para plantar depois. Atenção: sementes pequenas engasgam; fique ao lado e jogue-as fora com as cascas.")}"""
    L.add(c, aba="--d-vida")

    itens = [dict(pt="maçã", mot="maca", en="apple", fr="pomme", la="mālum", dica="tem sementes pretinhas no meio"),
             dict(pt="pera", mot="pera", en="pear", fr="poire", la="pirum", dica="doce, de miolo macio"),
             dict(pt="cereja", mot="cereja", en="cherry", fr="cerise", la="cerasum", dica="tem um caroço duro"),
             dict(pt="uva", mot="uva", en="grape", fr="raisin", la="ūva", dica="cresce em cachos"),
             dict(pt="laranja", mot="laranja", en="orange", fr="orange", la=None, dica="as sementes ficam nos gomos"),
             dict(pt="melancia", mot="melancia", en="watermelon", fr="pastèque", la=None, dica="muitas sementes pretas"),
             dict(pt="morango", mot="morango", en="strawberry", fr="fraise", la="frāgum", dica="as sementinhas ficam por fora"),
             dict(pt="banana", mot="banana", en="banana", fr="banane", la=None, dica="as sementes são minúsculas"),
             dict(pt="ervilha", mot="ervilha", en="pea", fr="pois", la="pisum", dica="as ervilhas moram numa vagem")]
    cartoes(L, "frutas e sementes", itens, "Volume 6 · Frutas e sementes")

    diario(L, "Minhas sementes", "desenhar as sementes que ela viu e a plantinha", ["o feijão no começo", "a plantinha depois", "uma semente de fruta", "a que eu quero plantar"], "--d-vida",
           "Ela desenha o feijão no primeiro dia e depois a plantinha, e escolhe duas sementes de fruta para desenhar. Escreva as datas e o que ela contar.",
           faixa=["feijao", "ervilha", "bolota", "pinha"])



# ================================================================== U6 ÁGUA E CHUVA

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · Água e chuva", aba="--d-matematica",
        pergunta="De onde vem a chuva, e para onde vai a água depois que cai?",
        duracao="Dois fins de semana · um de experimentos com água e um de olhar a chuva (ou a poça) · 20 a 30 minutos.",
        objetivos=["Contar o caminho da água: sol, nuvem, chuva, rio.", "Dizer o que flutua e o que afunda, depois de testar.", "Olhar e ouvir a chuva (ou a torneira) com atenção.",
                   "Medir um pouco de água com um copo e comparar.", "Cuidar da água: não desperdiçar e não beber de poça."],
        repertorio="<b>Palavras:</b> água, gota, nuvem, chuva, rio, poça, flutua, afunda, seca. <b>Línguas:</b> <i>water · l’eau · aqua</i>; <i>rain · la pluie · pluvia</i>; <i>cloud · le nuage · nubes</i>.",
        materiais="Uma bacia, copos, uma jarra, objetos para testar (pedra, pena, folha, rolha, colher, madeira), um pote transparente, régua ou fita, o caderno de natureza.",
        vida="Fechar a torneira ao escovar os dentes; olhar a chuva pela janela; molhar as plantas.",
        etapas=[["Olhar a chuva (ou ouvir a água) e dizer o que vê e ouve.", "Fazer a bacia: o que flutua? o que afunda?", "Dizer por que acha que cada coisa fica ou afunda."],
                ["Ordenar os quatro cartões do caminho da água.", "Pôr um pote ao ar livre para medir a chuva.", "Olhar a poça secando ao sol."],
                ["Contar o caminho da água com as palavras dela.", "Desenhar a chuva, a nuvem ou o rio.", "Pensar em um jeito de economizar água em casa."]],
        indicadores=["Diz o caminho da água na ordem certa (com ajuda dos cartões).", "Faz uma previsão antes de testar (“acho que a pedra afunda”).", "Anota o resultado do teste, com desenho ou palavra.",
                     "Percebe que a poça some e pergunta para onde foi.", "Fecha a torneira ou poupa a água sem ser lembrada.", "Descreve o som da chuva com palavras dela."],
        interesse="medir a chuva do mês, anotando quanta água o pote juntou em cada dia de chuva.",
        dificil="olhar uma só gota na janela, escorrendo, e dizer para onde ela vai.",
        alerta="Fique ao lado de qualquer água, até a da bacia. Não beba água de poça, rio ou chuva, e não deixe a criança entrar sozinha em água corrente. Em dia de trovão, fique dentro de casa."))

    historia6(L, "A viagem da gota", "uma história curta, para contar antes de olhar a chuva",
              ["Uma gota de água morava num rio. Um dia, o sol esquentou o rio, e a gota ficou tão leve que subiu pelo ar, sem ninguém ver. Lá em cima, encontrou outras gotas, e todas juntas formaram uma nuvem.",
               "A nuvem foi ficando pesada, e começou a cair uma chuva. Plim, plim, plim. A gota caiu numa folha, escorreu para o chão e entrou num riacho. O riacho desceu a montanha, passou por pedras e virou rio.",
               "Quando o sol esquentou o rio de novo, a gota subiu outra vez. “Será que já fui nuvem antes?”, perguntou a gota. Ninguém soube responder. Mas Marina, na janela, viu a chuva cair e disse: “Essa água já foi de outro rio, e vai voltar para ele.”"],
              tira(["gota", "sol", "nuvem", "guarda_chuva"], "26mm", "4mm"),
              cena([("sol", 30, 4, 4), ("nuvem", 48, 40, 8), ("nuvem_chuva", 44, 92, 0), ("orvalho_folha", 34, 6, 46, -10), ("m_riacho", 46, 46, 56), ("barquinho", 36, 100, 52), ("arco_iris", 34, 138, 40)], 92),
              adulto("contar e perguntar",
                     "Conte devagar, e depois peça que ela conte de volta, com as próprias palavras, para onde a gota vai. A história resume o <b>ciclo da água</b>: evaporar, formar nuvem, chover, escorrer. "
                     "Não precisa usar as palavras difíceis. A história é da coleção."), "--d-matematica")

    sequencia(L, "O caminho da água", "cortar os quatro cartões e ordenar",
              [("o sol esquenta a água", f'<div class="centro">{img("sol", "26mm")}{img("m_riacho", "34mm")}</div>'),
               ("a água sobe e vira nuvem", img("nuvem", "42mm", "margin:8mm auto 0")),
               ("a nuvem solta a chuva", img("nuvem_chuva", "40mm", "margin:2mm auto 0")),
               ("a água volta ao rio", img("m_riacho", "46mm", "margin:6mm auto 0"))],
              adulto("ordenar",
                     "Corte os cartões e embaralhe. Peça que ela ponha em ordem e conte o caminho em voz alta. Não existe uma única forma certa de contar: o que importa é ela perceber que a água <b>volta</b>. "
                     "Depois, ela tenta contar a viagem a outra pessoa, com os cartões nas mãos.", estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"),
              aba="--d-matematica")

    objetos = (("pedra", "pedra"), ("pena", "pena"), ("folha_seca", "folha seca"), ("rolha", "rolha"), ("colher", "colher"), ("madeira", "pedaço de madeira"))
    linhas = "".join(f'<tr><td style="width:30mm;text-align:center">{img(m, "16mm")}</td><td style="width:42mm;font-size:13pt">{n}</td><td style="width:42mm;font-size:12pt;color:var(--sepia)">acho que: ________</td><td style="font-size:12pt;color:var(--sepia)">foi: ________</td></tr>'
                     for m, n in objetos)
    c = f"""<div class="miolo">{titulo("Flutua ou afunda?", "adivinhar, testar na bacia e anotar", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["barquinho", "gota", "peixe_azul"], "28mm", "6mm")}</div>
      <table class="tab" style="margin-top:4mm"><tr><th></th><th>Objeto</th><th>Antes de testar</th><th>Depois de testar</th></tr>{linhas}</table>
      <div class="caixa" style="margin-top:6mm;height:50mm"><div class="peq centro">o que mais flutua? o que mais afunda? o que me surpreendeu?</div></div></div>
      {adulto("prever e testar",
              "Ela <b>adivinha primeiro</b>, escrevendo ou falando, e só depois testa na bacia. Não corrija a previsão: o erro é parte da descoberta. Pergunte o que os objetos que flutuam têm em comum (leves? ocos?). "
              "Fique ao lado da bacia o tempo todo. Seque o chão depois.")}"""
    L.add(c, aba="--d-matematica")

    itens = [(img("nuvem_chuva", "26mm"), "Olhar o céu: tem nuvem? Como ela é?"),
             (img("orelha", "20mm"), "Ouvir a chuva (ou a torneira): é forte ou fraca?"),
             (img("xicara", "20mm"), "Pôr um pote reto, aberto, no quintal ou na janela"),
             (img("m_riacho", "24mm"), "Olhar para onde a água escorre"),
             (img("poca", "26mm"), "Olhar uma poça ao sol: ela vai diminuindo?"),
             (img("lupa", "20mm"), "Medir quanta água o pote juntou e anotar")]
    passos6(L, "Olhar a chuva", "ouvir, medir e acompanhar uma poça", itens,
            adulto("a chuva",
                   "Num dia de chuva fraca, vá com ela à janela ou à varanda: não precisa se molhar. Para medir, use um pote de lados retos e deixe-o fora até a chuva passar; com uma régua, meça a altura da água. "
                   "Numa poça, risque o contorno com giz e volte mais tarde: ela encolheu? <b>Não beba, nem deixe beber</b>, água de chuva ou de poça."),
            "--d-matematica",
            cena([("guarda_chuva", 40, 8, 10), ("bota", 36, 56, 26), ("poca", 52, 98, 38), ("gota", 14, 52, 4), ("gota", 12, 90, 2), ("gota", 12, 140, 8)], 82))

    itens = [dict(pt="gota", mot="gota", en="drop", fr="goutte", la="gutta", dica="pequenina; faz o mar"),
             dict(pt="nuvem", mot="nuvem", en="cloud", fr="nuage", la="nūbēs", dica="é feita de gotinhas"),
             dict(pt="chuva", mot="nuvem_chuva", en="rain", fr="pluie", la="pluvia", dica="cai da nuvem"),
             dict(pt="arco-íris", mot="arco_iris", en="rainbow", fr="arc-en-ciel", la="arcus pluvius", dica="aparece com sol e chuva"),
             dict(pt="poça", mot="poca", en="puddle", fr="flaque", la=None, dica="a água que sobra no chão"),
             dict(pt="riacho", mot="m_riacho", en="stream", fr="ruisseau", la="rīvus", dica="água que corre"),
             dict(pt="barquinho", mot="barquinho", en="paper boat", fr="bateau en papier", la=None, dica="de papel; flutua um pouco"),
             dict(pt="regador", mot="regador", en="watering can", fr="arrosoir", la=None, dica="leva água às plantas"),
             dict(pt="guarda-chuva", mot="guarda_chuva", en="umbrella", fr="parapluie", la=None, dica="protege da chuva")]
    cartoes(L, "água e chuva", itens, "Volume 6 · Água")

    diario(L, "Minha água", "desenhar a água e a chuva", ["a chuva que eu vi", "o caminho da água", "a poça e o sol", "como eu economizo água"], "--d-matematica",
           "Ela desenha a chuva, o caminho da água, a poça e um jeito de economizar água em casa. Escreva a data e, ao lado de cada desenho, o que ela contar.",
           faixa=["nuvem_chuva", "arco_iris", "barquinho", "poca"])



# ================================================================== U7 CÉU, SOL, LUA E ESTRELAS

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · Céu, sol, lua e estrelas", aba="--d-ingles",
        pergunta="O que muda no céu do amanhecer à noite, e como a lua muda de um dia para o outro?",
        duracao="Quatro semanas de olhar · um encontro curto por semana · 15 a 20 minutos, de dia e à noite.",
        objetivos=["Dizer onde o sol nasce, onde passa ao meio-dia e onde se põe.", "Medir a sombra de um objeto de manhã, ao meio-dia e à tarde.", "Desenhar a lua em noites diferentes e perceber que ela muda de forma.",
                   "Olhar as estrelas e contar quantas vê.", "Ordenar o dia: amanhecer, meio-dia, entardecer, noite."],
        repertorio="<b>Palavras:</b> sol, lua, estrela, nuvem, amanhecer, entardecer, noite, sombra, crescente, cheia. <b>Línguas:</b> <i>sun · le soleil · sol</i>; <i>moon · la lune · lūna</i>; <i>star · l’étoile · stēlla</i>.",
        materiais="Um objeto que fique em pé no chão (um copo, um bloquinho), giz, fita, o caderno de natureza, uma lanterna pequena; uma noite com céu limpo.",
        vida="Dizer, ao acordar, como está o céu; olhar a lua da janela antes de dormir.",
        etapas=[["Olhar o sol no seu caminho (sem olhar para ele) e apontar onde nasce e onde se põe.", "Ordenar os quatro cartões do dia.", "Contar o que muda no céu entre uma hora e outra."],
                ["Medir a sombra do copo de manhã, ao meio-dia e à tarde.", "Comparar: quando ela é mais comprida?", "Dizer por que acha que a sombra muda."],
                ["Olhar a lua e desenhar no caderno, por vários dias.", "Contar as estrelas que consegue ver.", "Contar a alguém o que viu no céu."]],
        indicadores=["Aponta o lado onde o sol nasce e o lado onde ele se põe.", "Ordena os quatro momentos do dia sem ajuda.", "Percebe que a sombra muda de tamanho.",
                     "Desenha a lua com formas diferentes em dias diferentes.", "Conta estrelas com o dedo, sem pular.", "Faz perguntas sobre o céu."],
        interesse="olhar a lua todo dia por um mês e fazer a tabela completa, ou procurar a estrela mais brilhante do começo da noite.",
        dificil="olhar a lua pela janela por um minuto e dizer a forma que ela tem.",
        alerta="<b>Nunca olhe diretamente para o sol</b>, nem com binóculo ou óculos escuros: machuca os olhos. Use a sombra para estudá-lo. À noite, fique sempre junto com a criança, em lugar seguro e iluminado."))

    historia6(L, "O sol, a lua e a Marina", "uma história curta, para contar antes de olhar o céu",
              ["De manhã, o sol aparece de um lado do céu. Marina via, da janela, uma luz alaranjada subindo atrás dos telhados. “É o sol acordando”, dizia o papai. Ao meio-dia, o sol ficava lá no alto, e a sombra do poste ficava pequena, bem pertinho do poste. À tarde, o sol descia do outro lado, e a sombra crescia de novo, comprida, para o lado contrário.",
               "Quando o sol sumia, o céu ficava rosa, depois azul-escuro. Aí aparecia a lua. Na primeira noite, era um pedacinho fino, como um sorriso. Uma semana depois, estava mais gorda. Depois, ficou redonda e clarinha. E depois, foi sumindo, noite após noite, até quase não aparecer.",
               "“A lua está se mexendo?”, perguntou Marina. “Está”, disse o papai. “E o que muda é o pedaço dela que o sol ilumina, visto daqui da Terra.” Marina ficou pensando. Depois pegou o caderno e começou a desenhar a lua de cada noite."],
              tira(["sol", "nuvem", "lua", "estrela"], "28mm", "4mm"),
              cena([("dia_amanhecer", 38, 6, 4), ("dia_meiodia", 38, 48, 4), ("dia_entardecer", 38, 90, 4), ("dia_noite", 38, 132, 4)], 40),
              adulto("contar e olhar",
                     "Conte devagar e, de preferência, perto de uma janela. A explicação do papai é a verdadeira, mas a Marina não precisa entender tudo: basta <b>olhar e anotar</b>. "
                     "Ao meio-dia, a sombra é mais curta; de manhã e à tarde, mais comprida. O sol nasce no lado leste e se põe no oeste (aponte com ela, de onde ela está). A história é da coleção."), "--d-ingles")

    sequencia(L, "O dia, do começo ao fim", "cortar os quatro cartões e ordenar",
              [("o céu clareia", img("dia_amanhecer", "40mm")), ("o sol está no alto", img("dia_meiodia", "40mm")),
               ("o sol está descendo", img("dia_entardecer", "40mm")), ("as estrelas aparecem", img("dia_noite", "40mm"))],
              adulto("ordenar",
                     "Embaralhe os cartões e peça que ela ponha em ordem e diga o que fazemos em cada momento do dia. Depois, pergunte: o que muda no céu? Por que a sombra muda? "
                     "Se quiser, ela conta o seu dia usando os cartões.", estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"),
              aba="--d-ingles")

    itens = [(img("dia_amanhecer", "24mm"), "De manhã: pôr o copo no chão, riscar o contorno com giz"),
             (img("sol", "20mm"), "Com o giz, marcar onde termina a sombra do copo"),
             (img("dia_meiodia", "24mm"), "Ao meio-dia: marcar de novo, sem mexer no copo"),
             (img("sol", "20mm"), "A sombra ficou maior ou menor?"),
             (img("dia_entardecer", "24mm"), "À tarde: marcar mais uma vez a sombra"),
             (img("lupa", "20mm"), "Comparar as três marcas: onde está a mais curta?")]
    passos6(L, "A sombra do sol", "marcar a sombra de um copo em três momentos", itens,
            adulto("a sombra",
                   "Escolha um lugar de chão firme e com sol o dia inteiro. <b>Não mexa no copo</b> entre as marcas. A sombra mais curta é perto do meio-dia; de manhã e à tarde ela é mais comprida e fica de lados opostos. "
                   "<b>Nunca olhe para o sol</b>: o estudo é só pela sombra."),
            "--d-ingles",
            cena([("sol", 26, 20, 6), ("pegada", 14, 70, 38), ("lapis_cor", 40, 96, 26, 20), ("caderno", 34, 134, 8)], 70))

    fases = [("lua_nova", "lua nova"), ("lua_crescente", "crescente"), ("lua_quarto_crescente", "quarto crescente"), ("lua_gibosa_crescente", "gibosa crescente"),
             ("lua_cheia", "lua cheia"), ("lua_gibosa_minguante", "gibosa minguante"), ("lua_quarto_minguante", "quarto minguante"), ("lua_minguante", "minguante")]
    cel = "".join(f'<div style="text-align:center">{img(m, "34mm")}<div class="peq">{r}</div></div>' for m, r in fases)
    c = f"""<div class="miolo">{titulo("As fases da lua", "como a lua muda, vista do hemisfério sul", 26)}
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8mm 4mm;margin-top:10mm">{cel}</div>
      <div class="centro" style="margin-top:12mm">{tira(["estrela", "lua", "estrela"], "20mm", "8mm")}</div></div>
      {adulto("as fases",
              "A ordem é: nova (não se vê), crescente, quarto crescente, gibosa, cheia, e então o caminho de volta. <b>Aqui no hemisfério sul</b>, a lua crescente aparece com a parte clara do lado <b>esquerdo</b>; "
              "nos livros do hemisfério norte, ela vem desenhada do outro lado. Confira na janela. Cada fase dura cerca de uma semana.")}"""
    L.add(c, aba="--d-ingles")

    cel = "".join(f'<div style="text-align:center"><div style="width:26mm;height:26mm;border:0.6pt dashed var(--linha);border-radius:50%;margin:0 auto"></div><div class="peq">{n}</div></div>' for n in range(1, 15))
    c = f"""<div class="miolo">{titulo("A lua de cada noite", "desenhar, no círculo, a lua que se vê", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["lua", "estrela", "lua"], "18mm", "6mm")}</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6mm 4mm;margin-top:6mm">{cel}</div></div>
      {adulto("olhar a lua",
              "Em cada noite de céu limpo, no mesmo horário, ela olha a lua e pinta no círculo só a parte clara. Quando a lua não aparecer, deixe o círculo em branco e escreva “nublado”. "
              "O ciclo todo dura cerca de um mês (29 dias e meio), então os 14 círculos mostram só a primeira metade; continue no caderno. A lua também pode aparecer de dia.")}"""
    L.add(c, aba="--d-ingles")

    c = f"""<div class="miolo">{titulo("O Cruzeiro do Sul", "cinco estrelas que só o hemisfério sul vê", 26)}
      <div class="centro" style="margin:6mm 0">{img("cruzeiro_do_sul", "110mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Numa noite sem nuvens, longe das luzes mais fortes, procure no céu quatro estrelas formando uma cruz, com uma quinta estrela pequena ao lado. É o <b>Cruzeiro do Sul</b>. Ele aparece na bandeira do Brasil e foi usado por muita gente, durante séculos, para saber onde fica o sul.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Quem mora no hemisfério norte não vê essa cruz: lá o céu é outro. E nós não vemos a Estrela Polar, que eles usam para achar o norte.</p></div>
      {adulto("olhar as estrelas",
              "O desenho é esquemático, para reconhecer o formato; no céu real as estrelas têm brilhos diferentes. Procure a cruz em noite escura, a partir do início da noite em boa parte do ano, "
              "e deixe os olhos se acostumarem ao escuro por uns cinco minutos. Fique junto da criança, em lugar seguro. Um aplicativo de mapa do céu pode ajudar o adulto a achar a posição.")}"""
    L.add(c, aba="--d-ingles")

    itens = [dict(pt="sol", mot="sol", en="sun", fr="soleil", la="sōl", dica="não se olha de frente"),
             dict(pt="lua", mot="lua", en="moon", fr="lune", la="lūna", dica="muda de forma"),
             dict(pt="estrela", mot="estrela", en="star", fr="étoile", la="stēlla", dica="só aparece à noite"),
             dict(pt="nuvem", mot="nuvem", en="cloud", fr="nuage", la="nūbēs", dica="é feita de gotinhas"),
             dict(pt="arco-íris", mot="arco_iris", en="rainbow", fr="arc-en-ciel", la=None, dica="aparece com sol e chuva"),
             dict(pt="lua cheia", mot="lua_cheia", en="full moon", fr="pleine lune", la=None, dica="uma vez por mês"),
             dict(pt="Cruzeiro do Sul", mot="cruzeiro_do_sul", en="Southern Cross", fr="Croix du Sud", la=None, dica="cinco estrelas"),
             dict(pt="a Terra", mot="terra", en="Earth", fr="Terre", la="terra", dica="a nossa casa"),
             dict(pt="chuva", mot="nuvem_chuva", en="rain", fr="pluie", la="pluvia", dica="cai da nuvem")]
    cartoes(L, "no céu", itens, "Volume 6 · No céu")

    diario(L, "Meu céu", "desenhar o céu que ela viu", ["o céu de manhã", "a sombra e o sol", "a lua que eu mais gostei", "as estrelas que eu contei"], "--d-ingles",
           "Ela desenha o céu de manhã, a sombra que mediu, a lua de que mais gostou e as estrelas. Escreva as datas e quantas estrelas ela contou.",
           faixa=["sol", "nuvem", "lua_crescente", "cruzeiro_do_sul"])



# ================================================================== U8 O CORPO HUMANO

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · O corpo humano", aba="--d-historias",
        pergunta="O que o meu corpo faz, e como eu cuido dele?",
        duracao="Dois fins de semana · um para os sentidos e o coração, um para crescer e se cuidar · 20 a 30 minutos.",
        objetivos=["Nomear partes do corpo (cabeça, braço, mão, perna, pé, olhos, ouvidos, nariz, boca).", "Ligar cada sentido à parte do corpo que o faz.", "Sentir o coração batendo, parado e depois de pular.",
                   "Medir a mão e o pé, e perceber que o corpo cresce.", "Lavar as mãos em seis passos."],
        repertorio="<b>Palavras:</b> cabeça, braço, mão, dedo, perna, pé, olho, ouvido, nariz, boca, coração. <b>Línguas:</b> <i>hand · la main · manus</i>; <i>foot · le pied · pes</i>; <i>heart · le cœur · cor</i>.",
        materiais="Sabonete, toalha, uma fita métrica ou barbante, papel e lápis, um relógio com ponteiro de segundos; o caderno de natureza.",
        vida="Lavar as mãos antes de comer; dizer como o corpo está (com sono, com fome, com calor); escovar os dentes.",
        etapas=[["Nomear partes do corpo, apontando em si mesma.", "Fazer a tabela dos sentidos: com o que eu vejo? com o que eu escuto?", "Brincar de “mostre o seu nariz, a sua mão…”."],
                ["Sentir o coração com a mão no peito, parada e depois de pular dez vezes.", "Contornar a mão no papel e medir.", "Aprender a lavar as mãos em seis passos."],
                ["Desenhar o corpo todo no caderno.", "Dizer uma coisa que o corpo faz por ela.", "Ensinar a outra pessoa como lavar as mãos."]],
        indicadores=["Nomeia partes do corpo sem ajuda.", "Liga cada sentido à parte do corpo certa.", "Sente o coração e diz que bate mais depois de pular.",
                     "Contorna a própria mão e compara com a de um adulto.", "Lava as mãos nos seis passos, com ajuda ou sozinha.", "Diz como o corpo está (com sono, com fome, cansado)."],
        interesse="medir a altura na parede, a cada dois ou três meses, com uma marca e a data, e comparar.",
        dificil="só sentir o coração, com a mão no peito, por um minuto, e dizer o que sentiu.",
        alerta="Use os nomes corretos de todas as partes do corpo, sem vergonha. O corpo é dela: respeite quando ela não quiser ser tocada, medida ou abraçada. Água morna e sabonete suave, sem esfregar com força."))

    historia6(L, "O corpo da Marina", "uma história curta, para contar e brincar",
              ["De manhã, Marina acordou e esticou os braços. “Meu corpo acordou!”, disse. O papai riu: “E o que ele sabe fazer?” Marina pensou. Os <b>olhos</b> abrem e veem a luz. Os <b>ouvidos</b> escutam o passarinho. O <b>nariz</b> sente o cheiro do pão. A <b>boca</b> come, fala e canta. A <b>pele</b> sente quando a água está fria.",
               "“E o que eu não vejo?”, perguntou. “Seu coração”, disse o papai. Ele pôs a mão dela no peito. Bum-bum, bum-bum. Marina pulou dez vezes e pôs a mão no peito de novo. “Está mais rápido!” “Ele trabalha mais quando você corre”, disse o papai.",
               "Antes do almoço, Marina lavou as mãos, esfregando com sabonete, na palma, nas costas e entre os dedos. “Por que lavar?”, perguntou. “Para tirar bichinhos tão pequenos que a gente não vê”, disse o papai. Marina lavou de novo, com mais cuidado."],
              tira(["olho", "orelha", "nariz", "boca"], "24mm", "4mm"),
              cena([("mao", 36, 10, 4), ("coracao", 30, 62, 8), ("pe", 36, 102, 4), ("sabonete", 30, 142, 10)], 40),
              adulto("contar e brincar",
                     "Conte apontando em si mesma cada parte do corpo, e peça que ela aponte também. A explicação sobre o coração e as mãos é simples e verdadeira. Use sempre os nomes corretos das partes do corpo. A história é da coleção."), "--d-historias")

    sentidos = (("ver", "com os ________", "olho"), ("escutar", "com os ________", "orelha"), ("cheirar", "com o ________", "nariz"),
                ("provar o gosto", "com a ________", "boca"), ("sentir o frio e o calor", "com a ________", "mao"))
    linhas = "".join(f'<tr><td style="height:19mm;width:54mm;font-size:13pt">{a}</td><td style="font-size:13pt">{b}</td><td style="width:24mm;text-align:center">{img(m, "16mm")}</td></tr>' for a, b, m in sentidos)
    c = f"""<div class="miolo">{titulo("Com que parte do corpo?", "ligar cada sentido à parte que o faz", 26)}
      <table class="tab" style="margin-top:6mm"><tr><th>Eu consigo…</th><th>Com…</th><th>Dica</th></tr>{linhas}</table>
      <div class="caixa" style="margin-top:8mm;height:56mm"><div class="peq centro">desenhar a parte do corpo de que eu mais gosto, ou a que eu mais uso</div></div></div>
      {adulto("os sentidos",
              "Respostas: ver (olhos), escutar (ouvidos), cheirar (nariz), sentir o gosto (língua, dentro da boca), sentir frio e calor (pele). A coluna “Dica” traz o desenho da parte do corpo: cubra-a e só mostre depois que ela tentar. "
              "Vale experimentar: de olhos fechados, ela reconhece um cheiro? Um objeto, só pelo toque?")}"""
    L.add(c, aba="--d-historias")

    itens = [(img("coracao", "20mm"), "Sentar quieta e pôr a mão no peito: bum-bum"),
             (img("pegada", "18mm"), "Pular dez vezes no lugar"),
             (img("coracao", "22mm"), "Pôr a mão no peito de novo: está mais rápido?"),
             (img("estrela", "20mm"), "Ficar quieta de novo e sentir o coração devagar"),
             (img("lupa", "20mm"), "Contar as batidas por meio minuto, parada, com um adulto"),
             (img("mao", "20mm"), "Dizer: o coração bate o tempo todo, até quando durmo")]
    passos6(L, "O coração", "sentir o coração parado e depois de pular", itens,
            adulto("o coração",
                   "Se ela não achar as batidas no peito, use a mão no pulso (do lado do polegar) ou no pescoço, com cuidado. Contar não é necessário: o importante é <b>perceber</b> que o coração bate mais rápido depois de pular e volta ao ritmo em silêncio. "
                   "Não é exercício de resistência, nem prova."),
            "--d-historias",
            cena([("coracao", 34, 14, 6), ("pegada_esq", 16, 62, 20), ("pegada", 16, 78, 8), ("pegada_esq", 16, 94, 22), ("coracao", 28, 130, 12)], 54))

    itens = [(img("gota", "18mm"), "Molhar as mãos com água"),
             (img("sabonete", "20mm"), "Passar sabonete e fazer espuma"),
             (img("mao", "20mm"), "Esfregar a palma e as costas das mãos"),
             (img("lupa", "20mm"), "Esfregar entre os dedos e em volta dos polegares"),
             (img("gota", "20mm"), "Enxaguar com água, até a espuma sair"),
             (img("toalha", "22mm"), "Secar com a toalha, bem seco")]
    passos6(L, "Lavar as mãos em seis passos", "antes de comer e depois de brincar fora", itens,
            adulto("lavar as mãos",
                   "O que importa é a <b>espuma e o tempo</b>: cerca de 20 segundos (o tempo de cantar duas vezes “Parabéns a você”). Mostre uma vez e deixe que ela faça. "
                   "Lave as mãos depois de brincar na terra, depois de usar o banheiro e antes de comer. Água morna e sabonete suave."),
            "--d-historias",
            cena([("mao", 30, 14, 8), ("sabonete", 30, 56, 14), ("bolhas", 30, 96, 6), ("toalha", 34, 134, 10)], 50))

    c = f"""<div class="miolo">{titulo("Os dentes", "cuidar dos dentes de manhã e de noite", 26)}
      <div class="centro" style="margin:4mm 0">{tira(["dente", "escova_dentes", "boca"], "34mm", "8mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Os dentes mastigam a comida, ajudam a falar e dão forma ao sorriso. Quando a gente come, restos de comida ficam grudados neles, e é por isso que escovamos: <b>de manhã e antes de dormir</b>. Na escova, vai só uma pontinha de pasta, do tamanho de um grão de arroz.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Escove todos os cantinhos: os de fora, os de dentro e os de cima de cada dente. Depois, cuspa a espuma, sem engolir. E um dia, os dentinhos de leite vão ficar moles e cair — isso é normal, e os dentes de gente grande vão nascer no lugar.</p>
      <div class="caixa" style="margin-top:6mm;height:50mm"><div class="peq centro">desenhar o seu sorriso</div></div></div>
      {adulto("os dentes",
              "Escove junto com ela até que consiga sozinha (em geral, depois dos sete ou oito anos ela ainda precisa de ajuda no capricho). Use creme dental adequado à idade, em pouca quantidade. "
              "A primeira queda de dente de leite costuma acontecer por volta dos seis anos, mas varia muito. Se houver dor ou dente quebrado, procure um dentista.")}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo">{titulo("Quanto eu cresci", "contornar a mão e medir o corpo", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:6mm">{moldura_vazia("o contorno da minha mão", "88mm")}{moldura_vazia("o contorno do meu pé", "88mm")}</div>
      <table class="tab" style="margin-top:6mm"><tr><th>Data</th><th>Minha mão mede</th><th>Meu pé mede</th><th>Minha altura</th></tr>
        <tr><td style="height:12mm"></td><td></td><td></td><td></td></tr><tr><td style="height:12mm"></td><td></td><td></td><td></td></tr></table>
      <div class="centro" style="margin-top:5mm">{tira(["mao", "pe", "pegada"], "20mm", "10mm")}</div></div>
      {adulto("crescer",
              "Contorne a mão e o pé dela no papel e meça com a fita (ou com um barbante, depois comparado com uma régua). Guarde a página com a data. Em três meses, repita e compare. "
              "O corpo cresce no seu ritmo: nada de comparar com outras crianças.")}"""
    L.add(c, aba="--d-historias")

    itens = [dict(pt="mão", mot="mao", en="hand", fr="main", la="manus", dica="pega, aponta e cumprimenta"),
             dict(pt="pé", mot="pe", en="foot", fr="pied", la="pēs", dica="leva a gente para passear"),
             dict(pt="olho", mot="olho", en="eye", fr="œil", la="oculus", dica="vê a luz e as cores"),
             dict(pt="ouvido", mot="orelha", en="ear", fr="oreille", la="auris", dica="escuta os sons"),
             dict(pt="nariz", mot="nariz", en="nose", fr="nez", la="nāsus", dica="sente os cheiros"),
             dict(pt="boca", mot="boca", en="mouth", fr="bouche", la="ōs", dica="come, fala e canta"),
             dict(pt="dente", mot="dente", en="tooth", fr="dent", la="dēns", dica="mastiga a comida"),
             dict(pt="coração", mot="coracao", en="heart", fr="cœur", la="cor", dica="bate o tempo todo"),
             dict(pt="osso", mot="osso", en="bone", fr="os", la="os, ossis", dica="sustenta o corpo")]
    cartoes(L, "o corpo", itens, "Volume 6 · O corpo")

    diario(L, "Meu corpo", "desenhar o corpo todo e o que ele faz", ["eu inteira", "o que meu corpo faz", "como eu cuido do corpo", "o que eu quero aprender do corpo"], "--d-historias",
           "Ela desenha o corpo todo no primeiro quadro e, nos outros, o que o corpo faz, como ela se cuida e o que quer aprender. Escreva o que ela contar, com as palavras dela.",
           faixa=["mao", "olho", "coracao", "escova_dentes"])



# ================================================================== U9 AS ESTAÇÕES

def unidade9(L):
    inicio_unidade(L, 8)
    guia(L, dict(
        titulo="Unidade 9 · As estações", aba="--d-jogos",
        pergunta="O que muda na natureza durante o ano, e por que os livros de outros países contam estações diferentes das nossas?",
        duracao="O ano inteiro · uma visita por estação, de 15 a 20 minutos, à mesma árvore · mais uma leitura e uma conversa.",
        objetivos=["Visitar a mesma árvore (ou canto) em quatro épocas do ano.", "Dizer o que mudou: folhas, flores, frutos, bichos, roupas.", "Ordenar as quatro estações.",
                   "Ouvir a história de Deméter e Perséfone, adaptada, e dizer o que ela explica.", "Saber que, quando é verão aqui, é inverno no hemisfério norte."],
        repertorio="<b>Palavras:</b> primavera, verão, outono, inverno, calor, frio, chuva, seca. <b>Línguas:</b> <i>spring · le printemps</i>; <i>summer · l’été</i>; <i>autumn · l’automne · autumnus</i>; <i>winter · l’hiver · hiems</i>. <b>Mito:</b> Deméter e Perséfone (Grécia antiga, adaptado).",
        materiais="O caderno de natureza, lápis de cor, uma máquina fotográfica ou celular (se quiser), uma árvore ou canto de jardim para visitar toda estação.",
        vida="Vestir a roupa da estação; dizer o mês e a estação; olhar uma planta do quintal e ver o que mudou.",
        etapas=[["Escolher a árvore e visitar na primeira estação.", "Ouvir a história das estações.", "Dizer como está a árvore e o tempo."],
                ["Visitar a árvore na estação seguinte.", "Ordenar os cartões das quatro árvores.", "Comparar: o que mudou?"],
                ["Visitar nas outras estações.", "Desenhar a árvore nas quatro épocas.", "Contar a alguém o que o mito explica."]],
        indicadores=["Diz o nome das quatro estações, na ordem.", "Aponta o que mudou na árvore de uma visita para outra.", "Associa cada estação a roupas, clima e frutas.",
                     "Conta a história de Deméter e Perséfone com palavras dela.", "Diz que no outro hemisfério as estações são invertidas.", "Volta ao assunto sem ser lembrada."],
        interesse="registrar, a cada estação, o que está na feira (frutas da época) e o que a árvore tem (flores, frutos ou folhas secas).",
        dificil="olhar a árvore de hoje e dizer uma coisa dela: folhas, flores ou tempo.",
        alerta="Em regiões com estações pouco marcadas, a mudança maior pode ser entre a época de chuva e a de seca: observe isso também. Protetor solar e água no verão; agasalho no inverno."))

    historia6(L, "A árvore em quatro estações", "uma história curta, para contar antes de olhar",
              ["Na primavera, a árvore da Marina ficou cheia de folhinhas verdes e flores pequenas. Os passarinhos faziam ninho nos galhos, e o ar cheirava a mato novo. No verão, as folhas ficaram escuras e fartas, e a sombra era boa para brincar.",
               "No outono, algumas folhas ficaram amarelas e vermelhas e começaram a cair. A Marina juntava as que caíam. No inverno, a árvore ficou quase sem folhas, só galhos finos contra o céu. “Ela morreu?”, perguntou Marina. “Está descansando”, disse o papai. “Quando a primavera chegar, vai brotar de novo.”",
               "E brotou mesmo. Marina desenhou a árvore quatro vezes no caderno e guardou os quatro desenhos juntos. “É a mesma árvore”, disse. “Mas cada vez ela estava diferente.”"],
              tira(["arvore_primavera", "arvore_verao", "arvore_outono", "arvore_inverno"], "36mm", "2mm"),
              cena([("sandalia", 26, 12, 12), ("sorvete", 22, 52, 8), ("folha_seca", 26, 92, 14, 20), ("casaco", 30, 132, 8)], 40),
              adulto("contar e olhar",
                     "Nem toda árvore perde as folhas, e em muitos lugares do Brasil as estações são pouco marcadas: a mudança principal pode ser entre chuva e seca. Adapte a história à <b>sua árvore e ao seu clima</b>. "
                     "A história é da coleção."), "--d-jogos")

    historia6(L, "Deméter e Perséfone", "um mito da Grécia antiga, para explicar as estações",
              ["Há muito tempo, na Grécia, vivia uma deusa chamada <b>Deméter</b>, que cuidava das plantações: era ela quem fazia o trigo crescer e as árvores darem frutos. Sua filha, <b>Perséfone</b>, passava os dias colhendo flores nos campos.",
               "Um dia, Hades, o rei do mundo que fica debaixo da terra, levou Perséfone para o seu reino. Deméter procurou por toda parte, e de tristeza deixou de cuidar das plantas: as folhas caíram, o frio chegou e nada crescia. Então os deuses disseram a Hades que deixasse a menina voltar para casa.",
               "Perséfone pôde voltar, mas tinha comido algumas sementes de romã no reino de baixo, e por isso devia passar uma parte do ano lá. Quando ela está com a mãe, Deméter fica alegre e as plantas florescem: é a primavera e o verão. Quando Perséfone vai embora, Deméter fica triste e as folhas caem: é o outono e o inverno."],
              tira(["tulipa", "uva", "folha"], "26mm", "5mm"),
              cena([("flor_rosa", 34, 14, 4), ("folha_coracao", 28, 56, 10), ("uva", 28, 92, 6), ("folha_seca", 28, 128, 10, 30), ("floco_neve", 24, 158, 12)], 36, 190),
              adulto("um mito, não uma explicação científica",
                     "Os gregos antigos contavam este mito para explicar por que as plantas florescem e depois descansam. A explicação de hoje é outra (a inclinação da Terra), que ela vai estudar mais tarde. "
                     "Conte curto, sem insistir nos detalhes do rei de baixo. Pergunte: <b>o que a história quer explicar?</b> A versão é adaptada para a idade; o mito é antigo e de domínio público."), "--d-jogos")

    sequencia(L, "As quatro estações da árvore", "cortar os quatro cartões e ordenar, começando pela primavera",
              [("primavera", img("arvore_primavera", "46mm")), ("verão", img("arvore_verao", "46mm")),
               ("outono", img("arvore_outono", "46mm")), ("inverno", img("arvore_inverno", "46mm"))],
              adulto("ordenar",
                     "Embaralhe os cartões e peça que ela ponha em ordem, começando pela primavera. Pergunte o que há de diferente em cada árvore e que roupa ela usa em cada estação. "
                     "Aqui no sul do Brasil, a primavera começa em setembro; nos livros europeus, em março.", estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"),
              aba="--d-jogos")

    roupas = (("Primavera", "setembro a dezembro", "março a junho", "flor_rosa"), ("Verão", "dezembro a março", "junho a setembro", "sorvete"),
              ("Outono", "março a junho", "setembro a dezembro", "folha_seca"), ("Inverno", "junho a setembro", "dezembro a março", "floco_neve"))
    linhas = "".join(f'<tr><td style="height:22mm;font-size:13pt"><div style="display:flex;align-items:center;gap:3mm">{img(m, "14mm")}<b>{a}</b></div></td><td style="font-size:12pt">{b}</td><td style="font-size:12pt">{c}</td></tr>' for a, b, c, m in roupas)
    c = f"""<div class="miolo">{titulo("Aqui e do outro lado do mundo", "as estações no Brasil e no hemisfério norte", 26)}
      <table class="tab" style="margin-top:6mm"><tr><th>Estação</th><th>No Brasil (hemisfério sul)</th><th>Na Europa e na América do Norte</th></tr>{linhas}</table>
      <div class="caixa" style="margin-top:8mm;height:56mm"><div class="peq centro">o que as crianças de lá vestem no Natal? E nós? O que a gente come em cada estação?</div></div></div>
      {adulto("o outro hemisfério",
              "As estações são <b>invertidas</b> entre os dois lados da Terra: quando é verão aqui, é inverno lá. As datas dependem do ano; por isso, os meses são aproximados. "
              "Muitas histórias clássicas (como as de Natal com neve) foram escritas no hemisfério norte: converse com ela sobre isso. Em muitas regiões do Brasil, a diferença principal é entre a época de chuva e a de seca.")}"""
    L.add(c, aba="--d-jogos")

    c = f"""<div class="miolo">{titulo("O que vestir, o que comer", "ligar cada estação ao que ela pede", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:8mm">
        <div class="caixa" style="height:80mm"><div class="peq centro">no calor eu uso…</div><div class="centro" style="margin-top:4mm">{tira(["sandalia", "sorvete", "chapeu"], "20mm", "3mm")}</div></div>
        <div class="caixa" style="height:80mm"><div class="peq centro">no frio eu uso…</div><div class="centro" style="margin-top:4mm">{tira(["casaco", "caneca_quente", "gorro"], "20mm", "3mm")}</div></div></div>
      <div class="caixa" style="margin-top:8mm;height:70mm"><div class="peq centro">desenhar a roupa e a comida da estação de hoje</div></div></div>
      {adulto("roupa e comida",
              "Os desenhos servem de dica: peça que ela diga, olhando, o que combina com calor e o que combina com frio, e acrescente coisas da sua casa. "
              "Frutas e verduras mudam de época; vá com ela à feira e veja o que está na banca em cada estação.")}"""
    L.add(c, aba="--d-jogos")

    itens = [dict(pt="primavera", mot="arvore_primavera", en="spring", fr="printemps", la="vēr", dica="a árvore floresce"),
             dict(pt="verão", mot="arvore_verao", en="summer", fr="été", la="aestās", dica="sombra e calor"),
             dict(pt="outono", mot="arvore_outono", en="autumn", fr="automne", la="autumnus", dica="as folhas caem"),
             dict(pt="inverno", mot="arvore_inverno", en="winter", fr="hiver", la="hiems", dica="a árvore descansa"),
             dict(pt="casaco", mot="casaco", en="coat", fr="manteau", la=None, dica="para o frio"),
             dict(pt="sandália", mot="sandalia", en="sandal", fr="sandale", la=None, dica="para o calor"),
             dict(pt="sorvete", mot="sorvete", en="ice cream", fr="glace", la=None, dica="refresca no verão"),
             dict(pt="floco de neve", mot="floco_neve", en="snowflake", fr="flocon", la=None, dica="só cai em lugar muito frio"),
             dict(pt="a Terra", mot="terra", en="Earth", fr="Terre", la="terra", dica="gira em volta do sol")]
    cartoes(L, "as estações", itens, "Volume 6 · As estações")

    diario(L, "As estações da minha árvore", "desenhar a mesma árvore em quatro épocas do ano", ["primavera", "verão", "outono", "inverno"], "--d-jogos",
           "Ela desenha a mesma árvore em cada estação, no mesmo lugar, e escreve (ou dita) o que mudou. Anote a data de cada visita. Se o clima da sua região for outro, nomeie os quadros com as épocas dela (chuva, seca).",
           faixa=["flor_rosa", "sol", "folha_seca", "floco_neve"])



# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo

    itens = [("Merian", 1647, 1717, "#c9963f"), ("Descourtilz", 1796, 1855, "#4f6b3a"), ("Gould", 1804, 1881, "#5f8f8a"),
             ("Hudson", 1841, 1922, "#8a6f9e"), ("Grönvold", 1858, 1940, "#c0716b")]
    c = f"""<div class="miolo">{titulo("Quem desenhou a natureza", "os naturalistas deste livro e quando viveram", 28)}
      <div style="margin-top:8mm">{linha_do_tempo(itens, 1640, 1950)}</div>
      <table class="tab" style="margin-top:8mm;font-size:11pt">
        <tr><td style="width:34mm"><b>Merian</b></td><td><i>a lagarta, o casulo e a borboleta</i> · desenhou o bicho junto da planta onde ele vive</td></tr>
        <tr><td><b>Descourtilz</b></td><td><i>o sabiá-laranjeira</i> · ave do Brasil, na <i>Ornithologie brésilienne</i></td></tr>
        <tr><td><b>Gould</b></td><td><i>o beija-flor</i> · aves de asas pequenas e bico fino</td></tr>
        <tr><td><b>Hudson e Grönvold</b></td><td><i>o bem-te-vi</i> · o escritor e o desenhista de um livro de aves</td></tr></table></div>
      {adulto("o tempo e a natureza",
              "Mostre as barras como ruas compridas de tempo: Merian viveu há mais de 300 anos e Grönvold há menos de cem. Mesmo assim, todos olharam com atenção para bichos e plantas, como a Marina fez neste livro. "
              "Pergunte qual dos bichos ela gostaria de encontrar de verdade.")}"""
    L.add(c, aba="--d-natureza")

    diario(L, "Meu museu de natureza", "colar ou desenhar aqui o que ela mais gostou de olhar", ["a folha ou semente que eu mais gostei", "o bicho que eu mais gostei", "a coisa do céu que eu mais gostei", "o que eu quero olhar de novo"],
           "--d-natureza", "Peça que ela escolha, entre o que olhou e o que juntou, o que levaria para um museu só dela. Escreva o motivo da escolha, com as palavras dela.", h="66mm")

    for k in range(2):
        linhas = "".join('<tr><td style="width:36mm;height:44mm"><div class="peq">data e lugar</div></td><td style="width:50mm"><div class="peq">o que olhei</div></td>'
                         '<td><div class="peq">o que ela viu, fez ou disse</div></td></tr>' for _ in range(5))
        c = f"""<div class="miolo">{titulo("Diário de natureza", "para o adulto · o que ela olhou, fez e disse — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Data e lugar</th><th>O que olhei</th><th>O que ela viu, fez ou disse</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    pranchas = "".join(f"<li>{fontes_v6.credito(n)}</li>" for n in fontes_v6.OBRAS)
    c = f"""<div class="miolo texto">{titulo("Pranchas e créditos", "Volume 6", 26)}
      <h2>Pranchas de naturalistas</h2>
      <p style="font-size:9.2pt">Todas as pranchas são de autores mortos há mais de 70 anos e estão em domínio público, segundo a fonte indicada em cada crédito (Wikimedia Commons). A prancha do sabiá-laranjeira entra pela marcação do Commons e pelo texto do livro de Descourtilz.</p>
      <ul style="font-size:8.4pt;line-height:1.3">{pranchas}</ul>
      <h2>Fundamentos</h2><p style="font-size:9.4pt">O diário de natureza, a observação de uma coisa só e a volta ao mesmo lugar vêm de Charlotte Mason (<i>Home Education</i>, 1886). A narração, o olhar e a conversa antes da explicação seguem a mesma tradição.</p>
      <h2>Ilustrações da coleção</h2><p style="font-size:9.4pt">Folha, pena, gota, nuvem, sol, lua, estrela, lupa, galho, frutas, árvores, dias e demais desenhos: aquarela digital procedural da coleção, já usada em outros volumes. Nenhum desenho novo foi feito para este volume.</p>
      <h2>Histórias</h2><p style="font-size:9.4pt">As histórias da Marina são da coleção. O mito de Deméter e Perséfone é antigo, de domínio público, e foi adaptado para a idade. <i>Canção do exílio</i> é de Gonçalves Dias (1823–1864), em domínio público.</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 6</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">as primeiras línguas:<br>inglês e francês, com canções, cartões e jogos,<br>e um pouco de latim, para a Marina descobrir de onde vêm as palavras.</p>
      <div style="margin-top:12mm">{tira(["livro", "estrela", "sino", "pena"], "28mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 7 · Primeiras línguas</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8, unidade9)


def montar(unidades=None):
    L = Livro(6, "O livro da natureza")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidades or UNIDADES_PRONTAS):
        u(L)
    if not unidades:
        encerramento(L)
    num, _ = L.paginas[n_sum - 1]
    L.paginas[n_sum - 1] = (num, f'<section class="pagina"><div class="moldura"></div>{sumario(INICIO)}'
                                 f'<div class="rodape"><span class="num">{num}</span></div></section>')
    return L


def main():
    os.makedirs(SAIDA, exist_ok=True)
    ok = True
    for versao, nome in (("impressao", "volume6-impressao"), ("tela", "volume6-tela")):
        VERSAO["atual"] = versao
        L = montar()
        h = os.path.join(AQUI, f"{nome}.html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(L.html())
        ok &= gerar_pdf(h, os.path.join(SAIDA, f"{nome}.pdf"))
        print(versao, len(L.paginas), "páginas")
    if not ok:   # geração falhou: não renderizar páginas de inspeção a partir de um PDF antigo
        sys.exit(1)
    insp = os.path.join(SAIDA, "inspecao")
    os.makedirs(insp, exist_ok=True)
    for f in os.listdir(insp):
        os.remove(os.path.join(insp, f))
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume6-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
