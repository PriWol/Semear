"""
VOLUME 6 — O LIVRO DA NATUREZA
uso: python3 volume6.py            (monta o volume com as unidades já escritas; ver UNIDADES_PRONTAS)
As ilustrações são pranchas antigas de naturalistas (fontes_v6.py) e motivos que a coleção já tem (ADR 0019): não se desenha nada novo aqui.
"""
import html
import os
import re
import subprocess
import sys

from PIL import Image

from livro import (Livro, VERSAO, adulto, cabeca_folha, cartoes, gerar_pdf, guia, img, lista, observacao, passos, poema, texto, titulo)
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


def diario(L, t, sub, rotulos, aba, adulto_texto, h="68mm"):
    cel = "".join(moldura_vazia(r, h) for r in rotulos)
    c = f"""<div class="miolo">{titulo(t, sub, 27)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">{cel}</div></div>
      {adulto("registrar", adulto_texto)}"""
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

    c = f"""<div class="miolo">{titulo("Como se olha uma coisa só", "uma história curta, para contar antes de sair", 24)}
      <div class="centro" style="margin:3mm 0">{tira(["lupa", "folha", "raminho"], "36mm", "4mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Marina tinha um caderno novo, sem nenhuma linha. “O que a gente escreve num caderno sem linhas?”, ela perguntou. “O que a gente vê”, disse o avô.
      Eles saíram para o quintal e se sentaram no degrau.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">“Escolha uma coisa só”, disse o avô. Marina escolheu uma folha. “Agora fique olhando um minuto, sem falar.” O minuto demorou. Primeiro a folha era verde.
      Depois ela viu que tinha uma linha no meio e linhas menores saindo dela, como os galhos de uma árvore. A borda tinha uns dentinhos. Num cantinho, um furo pequeno: alguém já tinha comido um pedaço.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">“Agora desenhe”, disse o avô. Marina desenhou a linha do meio, as linhas pequenas, os dentinhos e o furo. No cantinho da página escreveu, com a ajuda do avô,
      o dia e o lugar: <i>quintal, degrau, sol fraco</i>. Quando acabou, ela disse: “Nunca vi tanta coisa numa folha só.” O avô sorriu: “É por isso que a gente olha uma coisa de cada vez.”</p></div>
      {adulto("contar e olhar",
              "Conte devagar, e peça que ela escolha a sua folha antes de sair. A ideia da unidade está na história: <b>uma coisa só, por um minuto, em silêncio</b>. "
              "A história é da coleção; o diário de natureza, como hábito, vem de Charlotte Mason.")}"""
    L.add(c, aba="--d-natureza")

    c = f"""<div class="miolo">{titulo("Meu registro de hoje", "uma página do diário, para repetir toda semana", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:6mm">
        <div class="caixa" style="height:18mm"><div class="peq centro">data</div></div>
        <div class="caixa" style="height:18mm"><div class="peq centro">lugar</div></div>
        <div class="caixa" style="height:18mm"><div class="peq centro">como está o tempo</div></div></div>
      <div class="caixa" style="margin-top:5mm;height:112mm"><div class="peq centro">o que eu olhei, desenhado grande</div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:5mm">
        <div class="caixa" style="height:30mm"><div class="peq centro">o nome (se eu souber)</div></div>
        <div class="caixa" style="height:30mm"><div class="peq centro">quantas eu vi? que cores?</div></div></div></div>
      {adulto("o registro",
              "Fotocopie esta página, se quiser, ou copie o modelo no caderno de natureza. Ela completa o que conseguir; escreva por ela o que ela ditar. <b>Nunca corrija o desenho.</b> "
              "Se ela não souber o nome, escreva “não sei” e procurem depois num livro ou numa pesquisa.")}"""
    L.add(c, aba="--d-natureza")

    itens = [(img("lupa", "22mm"), "Sentar no lugar escolhido e ficar quieta"),
             (img("pena", "20mm"), "Olhar: o que tem de mais perto? E de mais longe?"),
             (img("nuvem", "22mm"), "Escutar: quantos sons diferentes? De onde vêm?"),
             (img("folha", "20mm"), "Tocar (só o que é seguro): liso, áspero, mole, duro?"),
             (img("florzinha_amarela", "20mm"), "Cheirar com cuidado: tem cheiro? Qual?"),
             (img("estrela", "20mm"), "Fechar os olhos e contar uma coisa que lembra")]
    passos(L, "Passeio dos cinco sentidos", "olhar, escutar, tocar e cheirar, devagar", itens,
           adulto("os sentidos",
                  "Não prove nada que encontrar. Para o <b>tato</b>, escolha folhas lisas e pedras; fuja de plantas desconhecidas (algumas queimam ou coçam). "
                  "O <b>cheiro</b> é com cuidado: uma folha amassada de erva-cidreira ou de hortelã, se houver. Termine pedindo que ela conte, de olhos fechados, o que lembra: é o jeito mais seguro de saber o que ela guardou."),
           aba="--d-natureza")

    sem = "".join(f'<div class="caixa" style="height:46mm"><div class="peq centro">{d}</div></div>' for d in ("domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"))
    c = f"""<div class="miolo">{titulo("O tempo da semana", "olhar pela janela e desenhar o céu de cada dia", 26)}
      <div class="centro" style="margin:3mm 0">{tira(["sol", "nuvem", "gota", "lua"], "22mm", "3mm")}</div>
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
           "Escolha uma folha, uma flor ou uma pedra do lugar de olhar e desenhe nos dois primeiros quadros, com uma semana de intervalo. Nos outros dois, ela desenha ou conta o que mudou e o que quer olhar de novo. Escreva a data de cada um.")


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

    apreciar(L, "sabia", "O sabiá-laranjeira", "uma prancha antiga, com duas aves num galho com frutinhas",
             ["Quantas aves você vê? Em que galho está cada uma?", "De que cor é a barriga da ave de cima? E as costas?", "De que cor é a ave de baixo? O que ela tem de laranja?",
              "Como são os galhos? Você vê espinhos? E frutinhas, de que cor?", "Qual das duas aves tem o bico mais forte? Como você sabe?"],
             "A ave de cima, de costas marrons e barriga cor de laranja, é o <b>sabiá-laranjeira</b>, <i>Turdus rufiventer</i> no rótulo da prancha. É a ave símbolo do Brasil e canta de manhã cedo e no fim da tarde. "
             "A ave preta de peito alaranjado, na parte de baixo, é outra espécie, <i>Coracina scutata</i> no rótulo. Não é preciso explicar a diferença: basta que ela perceba que são duas aves, "
             "e descreva cada uma. Peça que ela feche o livro e diga <b>três coisas</b> de cada ave.",
             "olhar e comparar", "--d-musica", w=104, h=138)

    poema(L, "Canção do exílio", "Gonçalves Dias, 1843",
          ["Minha terra tem palmeiras,<br>Onde canta o Sabiá;<br>As aves, que aqui gorjeiam,<br>Não gorjeiam como lá."],
          tira(["pena", "raminho"], "26mm", "4mm"),
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

    linhas = "".join(f'<tr><td style="width:60mm;height:15mm;font-size:13pt">{a}</td><td style="width:28mm"></td><td style="width:28mm"></td><td></td></tr>'
                     for a in ("sabiá", "bem-te-vi", "beija-flor", "pombo", "outra ave: ______________", "outra ave: ______________"))
    c = f"""<div class="miolo">{titulo("Quem canta no quintal?", "uma folha para marcar o que vi e o que ouvi", 26)}
      <table class="tab" style="margin-top:6mm"><tr><th>Ave</th><th>Vi</th><th>Ouvi</th><th>Onde estava / o que fazia</th></tr>{linhas}</table>
      <div class="caixa" style="margin-top:6mm;height:60mm"><div class="peq centro">o canto de que mais gostei, em desenho (linhas para cima e para baixo, pontinhos, ondas…)</div></div></div>
      {adulto("escutar",
              "Sentem-se por <b>cinco minutos</b>, de manhã cedo ou no fim da tarde. A cada som, ela marca na folha. Se não souber o nome da ave, ela dá um nome só dela (“a que faz tchi-tchi”) e vocês descobrem depois. "
              "Repita o mesmo lugar e horário em outros dias e compare o que mudou.")}"""
    L.add(c, aba="--d-musica")

    diario(L, "Minhas aves", "desenhar as aves que ela viu e ouviu", ["a ave que eu mais gostei", "o bico dela", "o canto dela", "onde ela estava"], "--d-musica",
           "Peça que desenhe a ave de que mais gostou, em cima, e depois só o bico, o canto (em rabisco) e o lugar. Escreva a data e o nome, ou “não sei o nome”.")


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
             (img("folha", "22mm"), "Olhar as folhas: alguma tem furos? Há bichinhos embaixo?"),
             (img("pedra", "20mm"), "Olhar embaixo de uma pedra ou de um vaso (e pôr de volta)"),
             (img("florzinha_amarela", "20mm"), "Olhar uma flor: quem visita?"),
             (img("raminho", "20mm"), "Olhar um galho: há casulo, ovinhos ou teia?"),
             (img("estrela", "20mm"), "Contar as pernas de um bichinho e desenhar")]
    passos(L, "Caça aos bichinhos", "olhar de pertinho, com a lupa, sem pegar", itens,
           adulto("o passeio",
                  "Não é preciso ir longe: um canto de jardim, um vaso ou uma calçada bastam. <b>Olhar, não pegar.</b> Se ela quiser olhar um bichinho de perto, ponha-o num pote transparente por poucos minutos "
                  "e solte-o no mesmo lugar. Fuja de lagartas peludas, abelhas e vespas. Conte as pernas: <b>inseto tem seis; aranha tem oito</b> (e aranha não é inseto)."),
           aba="--d-artes")

    linhas = "".join(f'<tr><td style="height:18mm;width:62mm;font-size:13pt">{a}</td><td style="width:34mm;text-align:center;font-size:15pt">{b}</td><td></td></tr>'
                     for a, b in (("formiga", "6 patas"), ("borboleta", "6 patas"), ("besouro", "6 patas"), ("aranha", "8 patas"),
                                  ("outro bichinho: ____________", "___ patas"), ("outro bichinho: ____________", "___ patas")))
    c = f"""<div class="miolo">{titulo("Seis patas ou oito?", "contar as patas dos bichinhos", 26)}
      <table class="tab" style="margin-top:6mm"><tr><th>Bicho</th><th>Patas</th><th>Como é? (cor, antenas, asas)</th></tr>{linhas}</table></div>
      {adulto("contar",
              "Os insetos têm <b>seis patas</b>, três pares, e o corpo dividido em três partes (cabeça, tórax e abdômen). As aranhas têm <b>oito patas</b> e não são insetos. "
              "Se ela encontrar um bichinho que não esteja na lista, ela conta as patas de verdade, com a lupa, e anota.")}"""
    L.add(c, aba="--d-artes")

    diario(L, "Meus bichinhos", "desenhar o que ela encontrou com a lupa", ["o bichinho que achei", "onde ele estava", "quantas patas?", "o caminho da lagarta à borboleta"], "--d-artes",
           "Desenhe ou cole aqui o que ela viu na caça aos bichinhos, com a data e o lugar. Se ela quiser, copie o que ela disser sobre cada desenho ao lado dele.")


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1, unidade2, unidade3)


def montar(unidades=None):
    L = Livro(6, "O livro da natureza")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidades or UNIDADES_PRONTAS):
        u(L)
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
