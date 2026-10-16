"""
VOLUME 5 — O MUNDO DAS ARTES
uso: python3 volume5.py
"""
import os
import subprocess
import sys

from PIL import Image

from livro import (Livro, VERSAO, adulto, cabeca_folha, cartoes, gerar_pdf, guia, img, lista, marcas_corte, memoria,
                   observacao, passos, pontilhado, ponto_inicio, sequencia, texto, titulo, tracado)
from musica import linha_do_tempo
import fontes_v5

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume5")

UNIDADES = [
    ("Unidade 1 · Três cores, todas as cores", "--d-artes"),
    ("Unidade 2 · Linhas e círculos", "--d-musica"),
    ("Unidade 3 · Dürer, olhar de perto", "--d-natureza"),
    ("Unidade 4 · Monet e o jardim", "--d-matematica"),
    ("Unidade 5 · Van Gogh e os girassóis", "--d-jogos"),
    ("Unidade 6 · Mary Cassatt", "--d-historias"),
    ("Unidade 7 · Modelar", "--d-vida"),
    ("Unidade 8 · Colar", "--d-memoria"),
]
INICIO = {}


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


def tira(itens, w="22mm", gap="2mm"):
    """Fila de motivos pequenos."""
    return '<div class="centro" style="line-height:0">' + "".join(img(m, w, f"display:inline-block;margin:0 {gap}") for m in itens) + "</div>"


def obra(nome, w_max, h_max, estilo=""):
    """Reprodução de uma obra em cores, com moldura fina, no maior tamanho que cabe na caixa (mm)."""
    with Image.open(os.path.join(fontes_v5.SAIDA, f"{nome}.jpg")) as im:
        k = min(w_max / im.width, h_max / im.height)
        w, h = im.width * k, im.height * k
    return (f'<img class="obra" src="dominio_publico/v5/{nome}.jpg" '
            f'style="width:{w:.1f}mm;height:{h:.1f}mm;display:block;margin:0 auto;{estilo}" alt="">')


def credito_obra(*nomes):
    return '<div class="credito">Obra: ' + " · ".join(fontes_v5.credito(n) for n in nomes) + "</div>"


def apreciar(L, nome, t, sub, perguntas, texto_adulto, rotulo, aba, w=150, h=118):
    """Página de apreciação: a obra grande e perguntas de observação (nunca “o que o artista quis dizer”)."""
    return observacao(L, t, sub, obra(nome, w, h), perguntas,
                      adulto(rotulo, texto_adulto, credito_obra(nome)), aba=aba)


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
    potes = "".join(img(m, "34mm", "display:inline-block;margin:0 2mm") for m in ("pote_vermelho", "pote_amarelo", "pote_azul"))
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 5</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">O mundo<br>das artes</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:140mm;left:0;right:0">{obra("durer_lebre", 80, 88)}</div>
    <div class="centro" style="position:absolute;top:236mm;left:0;right:0;line-height:0">{potes}</div>
    <div class="centro" style="position:absolute;top:268mm;left:0;right:0;line-height:0">{tira(["pincel", "girassol", "tulipa", "argila_vaso"], "17mm", "3mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 5</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O mundo das artes</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">A galeria deste livro é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(["pote_vermelho", "pote_amarelo", "pote_azul", "pincel"], "30mm", "3mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Olhar com calma, fazer com as mãos</h1>
      <p>Neste volume a Marina vai fazer duas coisas que quase sempre andam juntas: <b>olhar</b> e <b>fazer</b>. Olhar com calma, e por bastante tempo,
      para poucas obras de artistas que viveram há muito tempo; e fazer com as próprias mãos, com tinta, argila e papel, sem modelo para copiar e sem nota.</p>
      <h2>Três ideias</h2>
      <ul>
        <li><b>Olhar é uma atividade</b> (Charlotte Mason). Uma obra por semana, na mesa, em tamanho grande, por alguns minutos. Depois, <b>sem a obra à vista</b>,
        a criança conta o que lembra. Atenção se treina assim, com poucas coisas e muita calma.</li>
        <li><b>Não se copia</b>. Dürer, Monet, Van Gogh e Mary Cassatt são para olhar e conversar, não para imitar. O que a Marina pinta é dela.
        Por isso este livro não traz modelos para copiar nem “o jeito certo” de pintar.</li>
        <li><b>O processo vale mais que o resultado</b>. Misturar cores, apertar a argila e rasgar o papel são o aprendizado. O que fica pronto é só um resto bonito.</li>
      </ul>
      <h2>O que este volume traz</h2>
      <p>Oito unidades: <i>três cores, todas as cores</i> (guache), <i>linhas e círculos</i> (Kandinsky), <i>Dürer</i> (uma lebre e uma planta, para olhar de perto),
      <i>Monet</i> (o jardim e a luz), <i>Van Gogh</i> (os girassóis), <i>Mary Cassatt</i> (mães e crianças), <i>modelar</i> (argila) e <i>colar</i> (papel pintado por ela).</p>
      <h2>Sobre as reproduções</h2>
      <p>As obras vêm de acervos abertos e são de artistas mortos há mais de 70 anos. <b>Uma fotografia nunca tem exatamente a cor do original</b>; quando puder,
      leve a Marina a um museu ou mostre um livro de arte. Em cada página dizemos de onde veio a imagem.</p>
      <div class="centro" style="margin-top:8mm">""" + tira(["pote_vermelho", "pote_amarelo", "pote_azul", "pincel", "tesoura", "cola"], "22mm", "1.5mm") + "</div>")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Uma mesa de artes</h1>
      <p>Monte, antes de começar, uma <b>mesa de artes</b> que possa ficar arrumada: papel grosso (ou o verso de papel já usado), guache atóxico em vermelho, amarelo, azul, branco e preto,
      dois pincéis (um largo e um fino), um pote com água, um pano, um avental velho, giz de cera, argila ou massa de modelar e uma tesoura sem ponta.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Dois encontros por fim de semana, de 20 a 30 minutos. Uma unidade a cada dois fins de semana. Nas semanas de obra, só <b>olhar</b> já vale um encontro.</td></tr>
        <tr><th>Olhar</th><td>Mostre a obra grande (a página do livro basta), em silêncio por um minuto. Faça uma pergunta de cada vez. <b>Depois vire a página</b> e peça que ela conte o que lembra.</td></tr>
        <tr><th>Fazer</th><td>Prepare tudo antes; ela mexe em tudo. Não dirija o pincel nem conserte o desenho. Elogie o que ela fez (“você usou muito azul”), não o resultado (“que bonito”).</td></tr>
        <tr><th>Sujar</th><td>É normal e esperado. Avental, jornal na mesa e uma bacia para lavar as mãos diminuem a tensão dos adultos.</td></tr>
        <tr><th>Guardar</th><td>Datar o que ela faz, no verso, e guardar numa pasta. A galeria do fim do livro serve para colar o que ela mais gostou.</td></tr>
        <tr><th>Idiomas</th><td>Os cartões trazem o nome das cores em inglês, francês e (quando existe) latim no verso.</td></tr>
      </table>
      <h2>Segurança</h2>
      <p>Use tintas e colas atóxicas e tesouras sem ponta. Argila e massa são para modelar, não para comer. Pincéis, pauzinhos e tampinhas ficam longe de quem ainda põe tudo na boca.</p>
      <div class="centro" style="margin-top:5mm">{tira(["pote_vermelho", "pote_amarelo", "pote_azul", "pincel", "tesoura"], "20mm")}</div>""")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio.get(n, "")}</td></tr>' for n, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Galeria, diário de arte e créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Volume 5 · O mundo das artes", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["pote_vermelho", "pote_amarelo", "pote_azul", "pincel", "tesoura", "cola"], "22mm", "1.5mm")}</div></div>"""


# ================================================================== U1 TRÊS CORES

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · Três cores, todas as cores", aba="--d-artes",
        pergunta="Com três tintas, quantas cores dá para fazer?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Sem pressa: misturar é a atividade.",
        objetivos=["Usar só vermelho, amarelo e azul (e branco) para fazer outras cores.", "Descobrir, misturando, que vermelho + amarelo = laranja, amarelo + azul = verde, azul + vermelho = roxo.",
                   "Nomear as cores em português (e, nos cartões, em inglês e francês).", "Pintar sem contorno, com manchas largas.", "Lavar o pincel entre uma cor e outra."],
        repertorio="<b>Cores:</b> vermelho, amarelo, azul (primárias); laranja, verde, roxo (as misturas); rosa, marrom e cinza. <b>Línguas:</b> <i>red · rouge · rūber</i>; <i>yellow · jaune · flāvus</i>; <i>blue · bleu</i>.",
        materiais="Guache atóxico (vermelho, amarelo, azul, branco), dois pincéis, um pote com água, um pano, papel grosso, avental e jornal na mesa; uma paleta (um prato de papelão serve).",
        vida="Lavar pincéis, limpar a mesa, secar as mãos; nomear as cores das roupas e dos alimentos durante o dia.",
        etapas=[["Pintar uma folha só de vermelho, outra de amarelo, outra de azul.", "Nomear cada cor em voz alta.", "Achar cada cor pela casa."],
                ["Misturar duas cores no meio da folha e ver o que nasce.", "Fazer a receita das cores.", "Pintar o arco-íris com três tintas."],
                ["Inventar uma cor nova e dar nome a ela.", "Pintar uma paisagem usando só as três cores e suas misturas.", "Escolher a cor preferida da semana."]],
        indicadores=["Pega a tinta com o pincel limpo e lava antes de trocar de cor.", "Diz o nome de pelo menos três cores sem ajuda.", "Descobre sozinha que duas cores fazem uma terceira.",
                     "Pinta com manchas largas, sem ter medo de borrar.", "Dá um nome à cor que inventou.", "Aponta cores nas coisas ao seu redor."],
        interesse="misturar o branco para fazer cores claras (rosa, azul-bebê) e o preto, em gotas bem pequenas, para fazer cores escuras.",
        dificil="só olhar as três tintas nos potes e escolher uma cor para pintar a folha toda.",
        alerta="Use tinta atóxica e fique por perto: pincel e tinta não vão à boca. Misturar demais deixa tudo marrom; é normal, e também é uma descoberta."))

    c = f"""<div class="miolo">{titulo("O pote vermelho, o pote amarelo e o pote azul", "uma história para contar antes de pintar", 22)}
      <div class="centro" style="margin:3mm 0">{tira(["pote_vermelho", "pote_amarelo", "pote_azul"], "40mm", "3mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Numa prateleira da cozinha moravam três potes: o <b>vermelho</b>, o <b>amarelo</b> e o <b>azul</b>.
      Os três achavam que eram muito diferentes, e não gostavam de ficar perto. “Eu sou quente como o morango”, dizia o vermelho. “Eu sou luminoso como o sol”, dizia o amarelo.
      “Eu sou fresco como o mar”, dizia o azul.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Um dia, caiu uma gotinha do vermelho dentro do amarelo. Houve um silêncio. Depois, uma cor que ninguém conhecia: <b>laranja</b>, como a laranja da fruteira.
      “Que é isso?”, perguntou o amarelo. “Sou eu… e você”, disse o vermelho, espantado.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Então o amarelo pingou no azul, e nasceu o <b>verde</b> das folhas. E o azul pingou no vermelho, e nasceu o <b>roxo</b> das uvas.
      Daquele dia em diante, os três potes passaram a ser grandes amigos: sabiam que, juntos, eram quase todas as cores do mundo.</p>
      <div class="centro" style="margin-top:4mm">{tira(["circulo_laranja", "circulo_verde", "circulo_roxo"], "26mm", "4mm")}</div></div>
      {adulto("contar e perguntar",
              "Conte devagar, mostrando os potes de tinta de verdade na mesa. Pare nas misturas e peça que ela adivinhe a cor que vai nascer; depois faça com ela. "
              "Não é preciso dizer a palavra “primária”: basta que ela perceba que há cores que nascem de outras. A história é da coleção.")}"""
    L.add(c, aba="--d-artes")

    c = f"""<div class="miolo">{titulo("A receita das cores", "misturar duas cores e ver o que nasce", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;margin-top:6mm;text-align:center">
        <div class="caixa">{img("circulo_vermelho", "24mm", "margin:0 auto")}<div style="font-size:22pt">+</div>{img("circulo_amarelo", "24mm", "margin:0 auto")}<div style="font-size:22pt">=</div>
          <div style="height:26mm;border:0.6pt dashed var(--linha);border-radius:50%;width:26mm;margin:0 auto"></div><div class="legenda-q">pintar o resultado</div></div>
        <div class="caixa">{img("circulo_amarelo", "24mm", "margin:0 auto")}<div style="font-size:22pt">+</div>{img("circulo_azul", "24mm", "margin:0 auto")}<div style="font-size:22pt">=</div>
          <div style="height:26mm;border:0.6pt dashed var(--linha);border-radius:50%;width:26mm;margin:0 auto"></div><div class="legenda-q">pintar o resultado</div></div>
        <div class="caixa">{img("circulo_azul", "24mm", "margin:0 auto")}<div style="font-size:22pt">+</div>{img("circulo_vermelho", "24mm", "margin:0 auto")}<div style="font-size:22pt">=</div>
          <div style="height:26mm;border:0.6pt dashed var(--linha);border-radius:50%;width:26mm;margin:0 auto"></div><div class="legenda-q">pintar o resultado</div></div></div>
      <div class="caixa" style="margin-top:6mm;height:78mm"><div class="peq centro">mais uma mistura que ela quiser tentar (com branco? com preto? com as três?)</div></div></div>
      {adulto("misturar de verdade",
              "Os círculos desta página são para <b>pintar com guache de verdade</b>: ela mistura numa paleta e passa para o círculo. Deixe que ela erre as proporções: se o laranja ficar muito vermelho, "
              "é o jeito de aprender quanto de amarelo faz falta. As três misturas (laranja, verde e roxo) são o que os pintores chamam de cores secundárias; guarde a palavra para depois. "
              "Os potes de tinta e os círculos são desenhos da coleção.")}"""
    L.add(c, aba="--d-artes")

    faixas = "".join(f'<div style="height:21mm;border:0.5pt solid var(--linha);border-radius:10mm 10mm 0 0;margin:0 {i * 6}mm;border-bottom:none"></div>' for i in range(6))
    c = f"""<div class="miolo">{titulo("O arco-íris de três tintas", "pintar com vermelho, amarelo e azul — e as misturas", 25)}
      <div style="margin:8mm 0 4mm">{faixas}</div>
      <div class="centro" style="margin-top:6mm">{tira(["pote_vermelho", "pote_amarelo", "pote_azul"], "28mm", "3mm")}</div>
      <div class="caixa" style="margin-top:6mm;height:60mm"><div class="peq centro">uma paisagem, só com as três tintas e as misturas</div></div></div>
      {adulto("o arco-íris",
              "As faixas em arco são para ela pintar como quiser: do vermelho ao roxo, ou no sentido contrário, ou fora de ordem. Se quiser, mostre um arco-íris de verdade (num livro ou no céu depois da chuva), "
              "mas sem exigir que ela copie as cores. A caixa de baixo é para uma paisagem livre, só com as três tintas e o que elas fazem juntas.")}"""
    L.add(c, aba="--d-artes")

    cores = [dict(pt="vermelho", mot="circulo_vermelho", en="red", fr="rouge", la="rūber", dica="morango, tomate, fogo"),
             dict(pt="amarelo", mot="circulo_amarelo", en="yellow", fr="jaune", la="flāvus", dica="sol, gema de ovo, girassol"),
             dict(pt="azul", mot="circulo_azul", en="blue", fr="bleu", la="caeruleus", dica="céu, mar, jeans"),
             dict(pt="laranja", mot="circulo_laranja", en="orange", fr="orange", la=None, dica="a fruta e a cor; os romanos não tinham essa palavra"),
             dict(pt="verde", mot="circulo_verde", en="green", fr="vert", la="viridis", dica="folhas, grama, ervilha"),
             dict(pt="roxo", mot="circulo_roxo", en="purple", fr="violet", la="purpureus", dica="uva, berinjela, lavanda"),
             dict(pt="rosa", mot="papel_rosa", en="pink", fr="rose", la="roseus", dica="rosa, algodão-doce, flor de pessegueiro"),
             dict(pt="marrom", mot="argila_bola", en="brown", fr="marron", la=None, dica="terra, chocolate, tronco"),
             dict(pt="cinza", mot="pedra", en="gray", fr="gris", la="cinereus", dica="pedra, nuvem de chuva, elefante")]
    cartoes(L, "as cores", cores, "Volume 5 · Cores")

    diario(L, "O que pintei hoje", "colar ou pintar aqui o que ela mais gostou", ["a cor que inventei", "a mistura que eu mais gostei", "o arco-íris", "uma paisagem de três tintas"],
           "--d-artes", "Cole aqui, com fita, as pinturas de que ela mais gostou, ou deixe que ela pinte direto nos quadros. Escreva ao lado, com a letra dela ou a sua, o que ela disser sobre cada uma, e a data.")


# ================================================================== U2 LINHAS E CÍRCULOS (KANDINSKY)

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · Linhas e círculos", aba="--d-musica",
        pergunta="Uma linha pode andar, dançar, pular e parar? E um círculo pode ter música?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Duas obras de Kandinsky e muitas linhas de verdade.",
        objetivos=["Olhar com calma duas obras de Kandinsky e dizer o que vê (cores, formas, tamanhos).", "Traçar com o dedo e com o giz de cera retas, ondas, zigue-zagues, espirais e círculos.",
                   "Perceber que as linhas “têm jeito”: calma, nervosa, saltitante.", "Fazer um desenho só de linhas e círculos, ouvindo uma música sem palavras.", "Contar o que lembra de uma obra com o livro fechado."],
        repertorio="<b>Obras:</b> Wassily Kandinsky (1866–1944), <i>Estudo de cores: quadrados com círculos concêntricos</i> (1913) e <i>Vários círculos</i> (1926). "
                   "<b>Palavras:</b> reta, curva, onda, espiral, círculo, concêntrico (dentro um do outro). <b>Línguas:</b> <i>line · la ligne</i>; <i>circle · le cercle · circulus</i>.",
        materiais="Papel grosso, giz de cera ou lápis de cor, guache, uma música sem palavras (instrumental) baixinho; a reprodução das obras (as páginas deste livro).",
        vida="Traçar, no ar, na areia ou no vapor do espelho; reparar em círculos pela casa (pratos, rodas, relógio).",
        etapas=[["Olhar <i>Vários círculos</i> em silêncio, por um minuto.", "Dizer o que vê: cores, tamanhos, quantos.", "Traçar uma linha reta e uma onda com o dedo."],
                ["Olhar <i>Quadrados com círculos concêntricos</i>.", "Traçar círculos dentro de círculos.", "Ouvir música e riscar linhas “do jeito dela”."],
                ["Fazer um desenho só de linhas e círculos.", "Pintar círculos que se sobrepõem (guache aguado).", "Dar nome ao desenho e dizer que música ele tem."]],
        indicadores=["Descreve a obra com pelo menos três palavras (cores, formas, tamanhos).", "Traça uma onda e uma espiral com o giz de cera.", "Faz círculos de tamanhos diferentes.",
                     "Diz como uma linha parece (calma, brava, pulando).", "Lembra de um detalhe da obra com o livro fechado.", "Dá nome ao seu desenho."],
        interesse="ouvir uma peça curta e pedir que ela risque o que ouve, com giz de cera, enquanto a música toca.",
        dificil="só olhar <i>Vários círculos</i> e dizer qual círculo ela escolheria para si."))

    c = f"""<div class="miolo">{titulo("Kandinsky, o pintor que ouvia as cores", "Moscou, 1866 · Munique · Paris", 24)}
      <div class="centro" style="margin:3mm 0">{tira(["circulo_vermelho", "circulo_amarelo", "circulo_azul"], "30mm", "3mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Wassily Kandinsky nasceu em Moscou, na Rússia, e começou a pintar só quando já era um homem adulto. Ele gostava muito de música e dizia que as cores faziam nele
      o efeito dos sons: o amarelo era como uma trombeta, o azul como um violoncelo. Por isso muitos dos seus quadros não mostram uma casa, uma pessoa ou uma árvore: mostram <b>formas e cores</b>, como uma música que a gente olha.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Foi um dos primeiros pintores a fazer isso. Morou na Alemanha e depois na França, e deu aulas de arte. Quando a gente olha um quadro dele, não é preciso entender “o que é”:
      basta ver o que as formas fazem e o que elas fazem a gente sentir.</p></div>
      {adulto("sem decifrar",
              "Kandinsky chamava de “música” o efeito das cores e das formas, e isso inspira a unidade. Não explique os quadros e não peça que ela “adivinhe” o que são: peça que ela diga o que vê "
              "e o que sente. As cores do círculo desta página são desenhos da coleção.")}"""
    L.add(c, aba="--d-musica")

    apreciar(L, "kandinsky_circulos", "Vários círculos", "Kandinsky, 1926 · olhar por um minuto, em silêncio",
             ["Quais cores você vê? Quantas?", "Qual é o círculo maior? De que cor ele é? E o menor?", "Há círculos dentro de outros círculos? Onde?", "Alguns círculos passam por cima de outros. O que acontece com as cores onde eles se cruzam?",
              "De que cor é o fundo? Algum círculo parece estar longe, e outro perto?", "Se esse quadro fizesse música, seria forte ou fraca? Rápida ou lenta?"],
             "Deixe a obra aberta por um minuto, em silêncio, antes de qualquer pergunta. Faça uma pergunta de cada vez e aceite qualquer resposta. Depois feche o livro e peça: <i>conte o que você lembra</i>. "
             "O maior círculo é preto, dentro de um anel azul com uma borda clara; em volta flutuam círculos de todos os tamanhos e cores, alguns transparentes, como se fossem de vidro colorido. Muitas crianças falam em bolhas, planetas ou balões; todas as respostas valem.",
             "olhar e conversar", "--d-musica", w=140, h=122)

    apreciar(L, "kandinsky_quadrados", "Quadrados com círculos", "Kandinsky, 1913 · um estudo de cores",
             ["Quantos quadrados você vê? E quantos círculos em cada um?", "Que cores tem o círculo do meio de cada quadrado?", "Qual quadrado você escolheria para você? Por quê?", "Os círculos de dentro e de fora se parecem? O que muda?"],
             "É uma aquarela feita para estudar como as cores se comportam umas ao lado das outras: doze quadrados, cada um com anéis de cores diferentes, um dentro do outro. Pode ser comparada ao jogo dos círculos concêntricos desta unidade. "
             "A imagem disponível tem pouca resolução e perde nitidez no tamanho impresso; ela não substitui a visita a um museu.",
             "olhar e comparar", "--d-musica", w=110, h=90)

    import math
    espiral = " ".join(f"L{70 + (2 + 20 * t / 90) * math.cos(t * 6 * math.pi / 90):.1f} {204 + (2 + 20 * t / 90) * math.sin(t * 6 * math.pi / 90):.1f}" for t in range(1, 91))
    lacos = " ".join(f"L{25 + 160 * t / 120 - 8 * math.sin(t / 120 * 6 * math.pi):.1f} {242 - 8 * math.cos(t / 120 * 6 * math.pi):.1f}" for t in range(1, 121))
    svg = "".join([
        ponto_inicio(25, 74), pontilhado("M25 74 L185 74"),
        ponto_inicio(25, 108), pontilhado("M25 108 q10 -16 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0"),
        ponto_inicio(25, 150), pontilhado("M25 150 " + " ".join("l10 -14 l10 14" for _ in range(8))),
        ponto_inicio(72, 204), pontilhado("M72 204 " + espiral),
        ponto_inicio(25, 234), pontilhado("M25 234 " + lacos)])
    tracado(L, "Linhas que dançam", "seguir com o dedo, depois com o giz de cera", svg, "",
            adulto("traçar",
                   "Cada linha começa no círculo e vai até o fim da página. Primeiro ela segue com o dedo, depois com o giz de cera, devagar. Dê um jeito a cada linha: a reta “anda”, a onda “nada”, o zigue-zague “pula”, a espiral “gira”. "
                   "Troque os papéis: ela diz o jeito, você traça. Não corrija o traço: o que treina é o movimento da mão.", ), aba="--d-musica")

    circulos = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--tracejado)" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0.1 5.5"/>'
                       for cx, cy, rs in ((58, 88, (8, 16, 24, 32)), (152, 88, (8, 16, 24, 32)), (105, 168, (10, 20, 30, 40, 50))) for r in rs)
    tracado(L, "Círculos dentro de círculos", "contornar os círculos, de dentro para fora", circulos + "".join(ponto_inicio(cx, cy - 8) for cx, cy in ((58, 88), (152, 88), (105, 168))), "",
            adulto("concêntricos",
                   "Peça que ela contorne cada círculo com o giz de cera, de uma cor diferente por anel, e diga o nome da palavra: <i>círculos concêntricos</i> (um dentro do outro). "
                   "Depois, no verso da folha, ela faz seus próprios círculos, do tamanho e com as cores que quiser. Como na obra de Kandinsky, o centro pode ter uma cor diferente da de fora."), aba="--d-musica")

    diario(L, "Meu estudo de linhas e círculos", "desenhar ouvindo uma música sem palavras", ["linhas calmas", "linhas pulando", "círculos pequenos", "círculos grandes e se cruzando"], "--d-musica",
           "Ponha uma música sem palavras, baixinho, e deixe que ela desenhe em cada quadro o que a música “pede”: linhas ou círculos, grandes ou pequenos, calmos ou agitados. Peça que dê nome a cada quadro e anote, com a data.")


# ================================================================== U3 DÜRER

def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · Dürer, olhar de perto", aba="--d-natureza",
        pergunta="Quanta coisa dá para ver num animal, ou num tufo de grama, se a gente olhar de pertinho?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Olhar demora; fazer é rápido.",
        objetivos=["Olhar com calma <i>A lebre jovem</i> e <i>Tufo de prímulas</i>, de Dürer.", "Apontar e nomear detalhes: orelhas, bigodes, olho, pelo, patas; folhas, raízes, flores.",
                   "Contar quantas coisas diferentes vê numa obra.", "Procurar no quintal ou na praça plantas e bichos de verdade e olhar de perto, com lupa.", "Desenhar um tufo de plantas observando de verdade."],
        repertorio="<b>Obras:</b> Albrecht Dürer (1471–1528), <i>A lebre jovem</i> (1502, aquarela da Albertina, em Viena) e <i>Tufo de prímulas</i> (1526, National Gallery of Art, em Washington). "
                   "<b>Palavras:</b> pelo, bigode, orelha, folha, raiz, talo, detalhe. <b>Línguas:</b> <i>hare · le lièvre · lepus</i>; <i>primrose · la primevère · primula</i>; <i>root · la racine · radix</i>.",
        materiais="Uma lupa (se tiver), papel e lápis, lápis de cor, uma prancheta ou livro grosso para apoiar; as reproduções deste livro.",
        vida="Passear olhando o chão; levar uma lupa no bolso; separar três coisas pequenas encontradas no caminho.",
        etapas=[["Olhar a lebre em silêncio, de perto.", "Contar bigodes, orelhas, patas.", "Procurar o ano e a assinatura do artista."],
                ["Olhar o tufo de prímulas: quantas flores? quantas folhas?", "Procurar um tufo no quintal e olhar de perto, com lupa.", "Jogar o jogo da memória da lebre e das plantas."],
                ["Desenhar um tufo observando de verdade.", "Escolher o detalhe de que mais gostou e contar por quê.", "Mostrar o desenho para alguém."]],
        indicadores=["Aponta pelo menos cinco detalhes da lebre.", "Diz que há plantas diferentes no tufo.", "Usa a lupa para olhar de perto uma folha ou um inseto.",
                     "Desenha com atenção, sem pressa.", "Lembra de um detalhe com o livro fechado.", "Acha pares iguais no jogo da memória."],
        interesse="procurar um bicho pequeno (caracol, joaninha, formiga) e olhar com lupa, desenhando só o que vê.",
        dificil="olhar só a lebre, só as orelhas, por um minuto, e dizer o que as orelhas parecem.",
        alerta="Não toque nem pegue bichos desconhecidos; olhar é suficiente. Lave as mãos depois de mexer em terra e plantas."))

    c = f"""<div class="miolo">{titulo("Dürer, que olhava de pertinho", "Nuremberg, 1471 · um artista que desenhava bichos e plantas", 23)}
      <div class="centro" style="margin:3mm 0">{tira(["lebre", "tufo", "lupa"], "36mm", "4mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Albrecht Dürer nasceu na cidade de Nuremberg, na Alemanha, há mais de 500 anos. O pai era ourives, e o filho aprendeu a desenhar com muito cuidado.
      Dürer fazia gravuras, que eram impressas e vendidas em muitas cidades, e pintava quadros. Mas também fazia estudos de bichos e plantas, para olhar e aprender: uma lebre, uma planta com raízes e flores.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Na época, poucos pintores olhavam tão de perto um animal ou um punhado de mato. Dürer olhou, e desenhou cada pelo e cada folha. Mais de 500 anos depois, quem olha esses desenhos ainda sente que o bicho vai se mexer
      e que a planta vai balançar.</p></div>
      {adulto("olhar com vagar",
              "As duas obras desta unidade são <b>estudos</b>: bichos e plantas desenhados de perto, para observar. Esse é o espírito da unidade: olhar muito e com calma, uma coisa só. "
              "Mostre na página a assinatura dele, um <b>A</b> com um <b>D</b> dentro, que ele punha em suas obras.")}"""
    L.add(c, aba="--d-natureza")

    apreciar(L, "durer_lebre", "A lebre jovem", "Dürer, 1502 · uma aquarela que cabe numa folha",
             ["Quantas orelhas você vê? Para onde cada uma aponta?", "Onde estão os bigodes? Quantos você consegue contar?", "Para onde a lebre está olhando? Como você sabe?", "De que cores é o pelo? Todas as partes têm a mesma cor?",
              "Procure, embaixo, o ano e a assinatura do artista. Você acha?"],
             "Deixe a imagem na mesa, grande, por um minuto. A lebre é uma aquarela com guache, de uns 25 cm de altura, e tem muitíssimos pelos desenhados um a um. "
             "Peça que ela conte com os dedos os bigodes; depois, que feche o livro e diga <b>três coisas</b> da lebre. Perto da base ficam o ano (1502) e a assinatura de Dürer.",
             "olhar de perto", "--d-natureza", w=120, h=130)

    apreciar(L, "durer_primulas", "Tufo de prímulas", "Dürer, 1526 · uma planta inteira, com raízes",
             ["Quantas flores você consegue contar? De que cor são?", "Como são as folhas? Todas têm o mesmo tamanho?", "Onde estão as raízes? E a terra?", "Os talos das flores são altos ou baixos? Para onde apontam?",
              "Procure, embaixo, o ano e a assinatura do artista. Você acha?"],
             "Esta obra mostra uma planta inteira, com flores, folhas, raízes e um pouco de terra, como se tivesse sido tirada do chão para ser olhada. As flores amarelas ficam em cima de talos finos e altos, e as folhas largas e enrugadas ficam embaixo. "
             "No canto inferior direito estão o ano (1526) e a assinatura de Dürer, um A com um D. É uma boa porta para o passeio com a lupa: ela procura uma planta no quintal, olha folha por folha e conta o que vê.",
             "olhar e comparar", "--d-natureza", w=125, h=140)

    itens = [(img("lupa", "22mm"), "Pegar a lupa e sair com um adulto"),
             (img("tufo", "22mm"), "Achar um tufo de plantas no chão"),
             (img("folha", "20mm"), "Olhar de perto uma folha: a borda é lisa ou serrilhada?"),
             (img("florzinha_amarela", "20mm"), "Procurar uma flor pequena e contar as pétalas"),
             (img("lebre", "22mm"), "Procurar um bicho de verdade (sem pegar): um inseto, um passarinho"),
             (img("estrela", "20mm"), "Desenhar um só detalhe, com todo o cuidado")]
    passos(L, "Passeio com a lupa", "olhar de perto o que existe perto de casa", itens,
           adulto("o passeio",
                  "Não é preciso ir longe: o canto de um quintal, uma rachadura de calçada ou uma floreira bastam. Leve uma lupa (se não tiver, a mão em concha também ajuda) e escolha <b>um</b> tufo ou uma folha. "
                  "Peça que ela conte quantas coisas diferentes vê. Depois, em casa, desenhe só um detalhe, como Dürer fazia. <b>Criar:</b> ela escolhe o bicho ou a planta de que mais gostou e inventa um nome para ele."),
           aba="--d-natureza")

    memoria(L, "a lebre e as plantas",
            [("lebre", img("lebre", "36mm")), ("tufo", img("tufo", "36mm")), ("folha", img("folha", "36mm")), ("margarida", img("margarida", "36mm")),
             ("cogumelo", img("cogumelo", "36mm")), ("bolota", img("bolota", "36mm"))],
            [0, 3, 5, 1, 2, 4, 3, 0, 1, 5, 4, 2],
            adulto("jogar e conversar",
                   "Vire as cartas, e cada jogador abre duas por vez, procurando pares iguais. Antes de começar, deixe que ela olhe cada carta e diga o nome. Ao achar um par, ela diz o que vê nas duas figuras. "
                   "Para os pequenos, comece com só três pares.", estilo="position:absolute;left:18mm;right:18mm;bottom:18mm"), verso_motivo="raminho")

    diario(L, "Olhei de perto", "desenhar o que ela viu com a lupa", ["uma folha de perto", "um bichinho", "um tufo de plantas", "o detalhe que eu mais gostei"], "--d-natureza",
           "Desenhe ou cole aqui o que ela viu no passeio, com a data. Se ela quiser, copie o que ela disser sobre cada desenho ao lado dele.")


# ================================================================== U4 MONET

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · Monet e o jardim", aba="--d-matematica",
        pergunta="Dá para pintar a luz do dia só com manchas de cor?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Olhar uma obra, pintar manchas.",
        objetivos=["Olhar com calma <i>Medas de trigo</i> e <i>Ninfeias</i>, de Monet.", "Perceber que a cor muda ao longo do dia (manhã, meio-dia, tarde, noite).",
                   "Pintar com manchas largas, sem contorno.", "Ordenar quatro momentos do dia.", "Contar o que lembra de uma obra com o livro fechado."],
        repertorio="<b>Obras:</b> Claude Monet (1840–1926), <i>Medas de trigo (fim do verão)</i> (1890–91) e <i>Ninfeias</i> (1906), as duas no Instituto de Arte de Chicago. "
                   "<b>Palavras:</b> mancha, luz, reflexo, jardim, lago, manhã, tarde. <b>Línguas:</b> <i>flower · la fleur · flos</i>; <i>garden · le jardin · hortus</i>.",
        materiais="Guache ou aquarela, pincel largo, papel grosso, água e pano; um jardim, uma praça ou até uma planta de vaso para olhar.",
        vida="Observar a luz na janela em horas diferentes; regar uma planta ou o jardim.",
        etapas=[["Olhar as <i>Medas de trigo</i>: de que cores são as medas?", "Dizer o que vê: céu, campo, medas, casas ao longe.", "Pintar uma folha só com manchas de rosa, lilás e amarelo."],
                ["Olhar <i>Ninfeias</i>: onde estão as flores e as folhas?", "Ordenar os quatro momentos do dia.", "Olhar a luz da janela em duas horas diferentes."],
                ["Pintar uma paisagem com manchas, sem contorno.", "Dar nome à paisagem e dizer a hora do dia.", "Escolher a obra de Monet preferida."]],
        indicadores=["Pinta com manchas largas, sem contornar tudo.", "Aponta as cores das medas e do campo (rosa, lilás, amarelo).", "Diz como a luz muda de manhã para a noite.",
                     "Ordena os quatro momentos do dia.", "Lembra de um detalhe da obra com o livro fechado.", "Dá nome à sua paisagem."],
        interesse="olhar a mesma árvore ou janela em três horas diferentes do dia e desenhar cada vez só as cores que viu.",
        dificil="olhar uma obra e dizer qual cor ela mais vê, sem pintar nada.",
        alerta="Se for pintar fora de casa, proteja a roupa e leve água. Não precisa terminar: parar quando cansar é o ritmo certo."))

    c = f"""<div class="miolo">{titulo("Monet e o jardim", "Paris, 1840 · Giverny · um pintor que pintava a luz", 24)}
      <div class="centro" style="margin:3mm 0">{tira(["ninfeia", "florzinha_rosa", "dia_meiodia"], "34mm", "4mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Claude Monet era francês e adorava pintar ao ar livre: campos, rios, jardins. Pintou muitas vezes as mesmas medas de trigo, em estações e horas diferentes, só para mostrar como a luz muda. Ele reparou que a cor das coisas muda ao longo do dia, conforme a luz do sol: de manhã é de um jeito, ao meio-dia de outro, à tarde de outro.
      Então pintava depressa, com <b>manchas de cor</b>, para pegar a luz antes que ela mudasse.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Mais tarde, Monet plantou um jardim em Giverny, na França, com um lago cheio de ninfeias, e pintou esse lago muitas e muitas vezes. Os pintores como ele ficaram conhecidos como impressionistas.
      Quando a gente olha de perto, só vê manchas; quando se afasta, as manchas viram flores, água e céu.</p></div>
      {adulto("olhar de perto e de longe",
              "Uma boa brincadeira com Monet é <b>chegar perto e afastar-se</b> do livro: de perto são só manchas, de longe viram um jardim. A criança vai gostar de fazer isso com o corpo. "
              "As duas obras desta unidade estão no Instituto de Arte de Chicago. A <i>Medas de trigo</i> faz parte de uma série de mais de vinte quadros das mesmas medas, o que combina com a sequência da luz do dia.")}"""
    L.add(c, aba="--d-matematica")

    apreciar(L, "monet_medas", "Medas de trigo", "Monet, 1890–91 · fim do verão, luz de fim de tarde",
             ["Quantas medas de trigo você vê? Qual é a maior?", "De que cores são as medas? E o campo na frente delas?", "O que aparece ao longe, atrás das medas?", "De que cor é o céu? Parece de manhã, de tarde ou de noite?",
              "Procure o nome do pintor e o ano, no canto de baixo."],
             "Monet pintou estas medas (montes de trigo colhido, empilhados no campo) muitas vezes, em horas e estações diferentes. Aqui o sol está baixo: as medas ficam cor-de-rosa e alaranjadas, e as sombras no chão são lilases e azuis. "
             "Peça que ela se afaste e se aproxime: de perto são só manchas, de longe são medas e campo. A assinatura e o ano (91) ficam no canto inferior esquerdo.",
             "olhar e conversar", "--d-matematica", w=170, h=100)

    apreciar(L, "monet_ninfeias", "Ninfeias", "Monet, 1906 · um lago visto de cima",
             ["Onde estão as flores? De que cor são? Quantas você acha?", "O que você acha que são as manchas verdes?", "A água parece ter nuvens? Que cores ela tem?", "Procure o nome do pintor e o ano, no canto de baixo.",
              "É de manhã, de tarde ou de noite? Como você sabe?"],
             "Esta é uma das muitas pinturas do lago de ninfeias do jardim de Monet. Quase não há margem nem céu: o quadro é a água, com folhas verdes boiando, poucas flores cor-de-rosa e o reflexo azulado das nuvens. "
             "A assinatura e o ano (1906) estão no canto inferior direito. Não é preciso decifrar nada: basta olhar e dizer o que se vê.",
             "olhar e conversar", "--d-matematica", w=130, h=130)

    itens = [(img("jarra", "20mm"), "Molhe o pincel largo e a folha, de leve"),
             (img("pote_azul", "20mm"), "Pinte manchas de azul no alto: o céu"),
             (img("pote_amarelo", "20mm"), "Ponha manchas de amarelo e de verde embaixo: o campo"),
             (img("pote_vermelho", "20mm"), "Salpique pontinhos de vermelho: as flores"),
             (img("circulo_roxo", "20mm"), "Deixe as cores se encontrarem, sem contorno"),
             (img("sol", "20mm"), "Afaste-se e olhe: o que as manchas viraram?")]
    passos(L, "Pintar com manchas", "uma paisagem sem contorno", itens,
           adulto("pintar a luz",
                  "Evite pedir que ela “desenhe primeiro e pinte depois”. O exercício é fazer a paisagem só com manchas. Quando secar, peça que ela se afaste e diga o que as manchas viraram. "
                  "<b>Criar:</b> ela diz a hora do dia da paisagem, e você escreve atrás do papel, com a data."),
           aba="--d-matematica")

    quadros = [("manhã", img("dia_amanhecer", "60mm", "margin:0 auto")), ("meio-dia", img("dia_meiodia", "60mm", "margin:0 auto")),
               ("tarde", img("dia_entardecer", "60mm", "margin:0 auto")), ("noite", img("dia_noite", "60mm", "margin:0 auto"))]
    sequencia(L, "A luz muda durante o dia", "recortar os quatro cartões e ordenar, da manhã à noite", quadros,
              adulto("ordenar o dia",
                     "Monet pintou o mesmo lugar várias vezes, em horas diferentes do dia, para mostrar como a luz muda. Misture os cartões e peça que ela os ordene, da manhã à noite. "
                     "Depois pergunte: <i>que cores mudam? o que fica igual?</i> Para os menores, use só dois cartões (dia e noite).",
                     estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"), aba="--d-matematica")

    diario(L, "Meu jardim de manchas", "pintar ou colar o que ela fez com manchas", ["um campo de flores", "um lago", "o céu de manhã", "o céu de noite"], "--d-matematica",
           "Cole aqui as pinturas de manchas, com a data atrás. Peça que ela diga a hora do dia e o lugar de cada uma, e escreva ao lado.")


# ================================================================== U5 VAN GOGH

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · Van Gogh e os girassóis", aba="--d-jogos",
        pergunta="Quantos amarelos cabem num só quadro?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Olhar, misturar amarelos, pintar um vaso de flores.",
        objetivos=["Olhar com calma <i>Girassóis</i>, de Van Gogh, e dizer o que vê.", "Perceber que o amarelo tem muitas versões (mais claro, mais escuro, mais verde, mais laranja).",
                   "Misturar amarelos com um pouquinho de outras cores.", "Pintar um vaso de flores observando flores de verdade.", "Nomear flores e plantas em três idiomas, nos cartões."],
        repertorio="<b>Obra:</b> Vincent van Gogh (1853–1890), <i>Girassóis</i> (Arles, 1888–89). <b>Palavras:</b> amarelo, vaso, pétala, talo, semente, girassol. "
                   "<b>Línguas:</b> <i>sunflower · le tournesol · helianthus</i>; <i>flower · la fleur · flos</i>.",
        materiais="Guache (amarelo, branco, um pouquinho de vermelho, verde e azul), pincel largo e fino, papel grosso, um vaso com flores de verdade (ou uma única flor).",
        vida="Colher ou comprar uma flor, pôr num vaso com água, regar plantas, observar uma planta crescer.",
        etapas=[["Olhar <i>Girassóis</i> em silêncio, por um minuto.", "Dizer quantas flores vê e como cada uma é diferente.", "Achar amarelos diferentes pela casa."],
                ["Misturar amarelos: com branco, com um toque de vermelho, com azul.", "Fazer a paleta de amarelos.", "Jogar os cartões das plantas."],
                ["Pintar um vaso de flores olhando as de verdade.", "Escolher o amarelo preferido e dar um nome a ele.", "Mostrar o quadro para alguém."]],
        indicadores=["Diz que cada girassol do quadro é diferente.", "Mistura amarelo com outra cor de propósito.", "Pinta pelo menos três amarelos diferentes.",
                     "Pinta um vaso de flores olhando as de verdade.", "Dá nome à sua cor de amarelo.", "Nomeia três plantas do jogo."],
        interesse="olhar uma flor por dia durante uma semana e pintar só uma pétala, com o amarelo mais parecido que ela conseguir.",
        dificil="olhar o quadro, escolher o girassol de que mais gosta e dizer por quê.",
        alerta="Se usar flores de verdade, evite as que podem fazer mal se comidas e lave as mãos depois de mexer nelas. Guache não é para comer."))

    c = f"""<div class="miolo">{titulo("Vincent e o amarelo", "Países Baixos, 1853 · Arles, no sul da França", 24)}
      <div class="centro" style="margin:3mm 0">{tira(["girassol", "pote_amarelo", "pincel"], "34mm", "4mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Vincent van Gogh nasceu nos Países Baixos e passou boa parte da vida desenhando e pintando, mesmo sem ter muito dinheiro. Ele escrevia cartas para o irmão Theo, contando o que pintava e o que sentia.
      Foi morar no sul da França, em Arles, atraído pelo sol e pela luz forte.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Em Arles pintou vários quadros de girassóis num vaso. Gostava de usar o amarelo quase puro, em pinceladas grossas, onde a tinta se vê. Cada flor do quadro é de um amarelo um pouco diferente:
      umas mais claras, outras mais alaranjadas, outras quase verdes. Ele quis mostrar que um só amarelo tem muitos amarelos.</p></div>
      {adulto("o amarelo de Vincent",
              "Van Gogh pintou mais de uma versão dos girassóis; a que aparece aqui é uma delas. Mostre à criança, de perto, que a tinta é grossa e que dá para ver as pinceladas. "
              "Deixe de lado a vida difícil do pintor: para esta idade, interessa o que ele fez, as flores e o amarelo.")}"""
    L.add(c, aba="--d-jogos")

    apreciar(L, "vangogh_girassois", "Girassóis", "Van Gogh, 1888–89 · um vaso de flores e muitos amarelos",
             ["Quantos girassóis você consegue contar?", "Todos os girassóis são iguais? Qual é o mais claro? E o mais escuro?", "Alguma flor parece velha ou murchando? Qual? E quais têm o miolo marrom-escuro?", "De que cor é o fundo? E a mesa?",
              "Onde dá para ver a pincelada grossa da tinta?"],
             "O quadro tem uma assinatura, “Vincent”, escrita no vaso. Peça que ela procure. Como a tinta está bem grossa, a criança pode perceber os traços do pincel, mesmo na reprodução. "
             "Mostre também, se puder, um girassol de verdade, ao lado do livro, e pergunte em que se parecem e em que são diferentes.",
             "olhar e comparar", "--d-jogos", w=115, h=140)

    amarelos = ["amarelo + um pouquinho de branco", "amarelo puro", "amarelo + uma gota de vermelho", "amarelo + uma gota de azul", "amarelo + um toque de verde", "amarelo + uma gota de preto"]
    cel = "".join(f'<div class="caixa" style="height:44mm"><div class="peq centro">{a}</div></div>' for a in amarelos)
    c = f"""<div class="miolo">{titulo("Todos os amarelos", "misturar e pintar a paleta de amarelos", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">{cel}</div>
      <div class="centro" style="margin-top:6mm">{tira(["pote_amarelo", "pote_vermelho", "pote_azul"], "24mm", "3mm")}</div></div>
      {adulto("mais amarelos",
              "Cada quadrado é para ela pintar com a mistura que está escrita embaixo (as gotas devem ser bem pequenas!). Depois, pergunte qual é o amarelo de que mais gosta e que nome daria a ele: “amarelo-pintinho”, “amarelo-sol”. "
              "A paleta é um jeito de ela ver, por si, o que Van Gogh mostrou no quadro: que o amarelo tem muitos amarelos.")}"""
    L.add(c, aba="--d-jogos")

    itens = [dict(pt="girassol", mot="girassol", en="sunflower", fr="tournesol", la="helianthus", dica="segue o sol; as sementes se comem"),
             dict(pt="margarida", mot="margarida", en="daisy", fr="marguerite", la="bellis", dica="miolo amarelo, pétalas brancas"),
             dict(pt="tulipa", mot="tulipa", en="tulip", fr="tulipe", la="tulipa", dica="vem de bulbo; flor de primavera"),
             dict(pt="folha", mot="folha", en="leaf", fr="feuille", la="folium", dica="achar folhas de formas diferentes"),
             dict(pt="raminho", mot="raminho", en="twig", fr="brindille", la="ramus", dica="um galho pequeno, com folhas"),
             dict(pt="bolota", mot="bolota", en="acorn", fr="gland", la="glans", dica="o fruto do carvalho"),
             dict(pt="cogumelo", mot="cogumelo", en="mushroom", fr="champignon", la="fungus", dica="nunca comer os do mato; só olhar"),
             dict(pt="flor", mot="florzinha_rosa", en="flower", fr="fleur", la="flos", dica="a palavra geral para todas as flores"),
             dict(pt="nuvem", mot="nuvem", en="cloud", fr="nuage", la="nubes", dica="olhar o céu: que forma a nuvem tem hoje?")]
    cartoes(L, "plantas e céu", itens, "Volume 5 · Plantas")

    itens = [(img("jarra", "22mm"), "Ponha as flores num vaso com água, na mesa, perto da luz"),
             (img("lupa", "20mm"), "Olhe uma flor de perto: quantas pétalas? que cores?"),
             (img("pote_amarelo", "20mm"), "Pinte o vaso e os talos com manchas largas"),
             (img("girassol", "22mm"), "Pinte as flores, uma de cada vez, olhando as de verdade"),
             (img("pincel", "22mm"), "Com o pincel fino, faça os detalhes, se quiser"),
             (img("estrela", "20mm"), "Dê um nome ao quadro e escolha a parede onde ele fica")]
    passos(L, "Um vaso de flores", "pintar olhando flores de verdade", itens,
           adulto("pintar o que se vê",
                  "Pinte junto, sem mostrar como. Fale do que vê: <i>esta flor está virada para a janela</i>, <i>esta pétala é mais clara</i>. Evite corrigir proporções e cores; o que se treina é olhar e decidir. "
                  "<b>Criar:</b> ela escolhe a cor do fundo e o nome do quadro."),
           aba="--d-jogos")

    diario(L, "Meus amarelos e meus girassóis", "guardar o que ela pintou nesta unidade", ["meu amarelo preferido", "uma flor que eu vi", "um vaso de flores", "um girassol do meu jeito"], "--d-jogos",
           "Cole aqui o que ela pintou, com a data atrás. Peça que diga o nome que deu ao amarelo de que mais gostou e escreva ao lado.")


# ================================================================== U6 MARY CASSATT

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · Mary Cassatt", aba="--d-historias",
        pergunta="Como alguém pinta o cuidado: o banho, o colo, a hora de descansar?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Três obras para olhar, uma sequência para ordenar, um retrato para fazer.",
        objetivos=["Olhar com calma três obras de Mary Cassatt e dizer o que vê (pessoas, gestos, cores, objetos).", "Perceber o que as pessoas fazem uma com a outra: segurar, lavar, descansar.",
                   "Ordenar quatro momentos do cuidado (encher a bacia, lavar, secar, dormir).", "Fazer o retrato de alguém que cuida dela.", "Falar do que lembra com o livro fechado."],
        repertorio="<b>Obras:</b> Mary Cassatt (1844–1926), <i>O banho da criança</i> (1893), <i>Menina na poltrona azul</i> (1878) e <i>Crianças brincando na praia</i> (1884). "
                   "<b>Palavras:</b> colo, banho, brincar, cuidar, descansar, poltrona, praia. <b>Línguas:</b> <i>mother · la mère · māter</i>; <i>child · l'enfant</i>.",
        materiais="Papel grosso, lápis de cor ou giz de cera, guache; uma bacia, uma toalha e um sabonete (para a sequência); um espelho ou uma foto da família.",
        vida="Participar do banho e da hora de dormir; dizer “obrigada” a quem cuida; ajudar a cuidar de uma boneca ou de uma planta.",
        etapas=[["Olhar <i>O banho da criança</i> em silêncio, por um minuto.", "Dizer o que cada pessoa está fazendo.", "Procurar as cores que se repetem."],
                ["Olhar as outras duas obras e comparar.", "Ordenar os quatro cartões da hora do banho.", "Cuidar de uma boneca: dar banho, secar, pôr para dormir."],
                ["Fazer o retrato de quem cuida dela.", "Contar uma história para o retrato.", "Escolher a obra de Cassatt de que mais gostou."]],
        indicadores=["Descreve o que as pessoas fazem em cada obra.", "Compara duas obras (o que é igual, o que é diferente).", "Ordena os quatro cartões do banho.",
                     "Faz o retrato de alguém, com cabeça, corpo e mãos.", "Fala de quem cuida dela com carinho.", "Lembra de um detalhe com o livro fechado."],
        interesse="olhar fotos de família com ela e conversar sobre quem está com quem, e o que estão fazendo.",
        dificil="olhar só uma obra, por pouco tempo, e dizer quem está no quadro.",
        alerta="Conversar sobre cuidado pode despertar lembranças; acolha o que ela disser, sem exigir. Se a família é diferente da dos quadros, vale dizer isso com naturalidade."))

    c = f"""<div class="miolo">{titulo("Mary Cassatt e o cuidado", "Pensilvânia, 1844 · Paris", 24)}
      <div class="centro" style="margin:3mm 0">{tira(["sabonete", "toalha", "tigela"], "34mm", "4mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Mary Cassatt nasceu nos Estados Unidos e foi estudar pintura na Europa, quando poucas mulheres podiam fazer isso. Foi morar na França e pintou ao lado dos impressionistas, como Monet.
      Gostava de pintar a vida de todos os dias: pessoas lendo, tomando chá, no teatro.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Pintou muitas vezes <b>mães e crianças</b>: o banho, o colo, o abraço, a hora de dormir. Em vez de mostrar heróis ou grandes batalhas, mostrou os gestos pequenos de cuidar, que a gente faz sem pensar.
      Olhando seus quadros, a gente percebe quanto carinho cabe num gesto simples.</p></div>
      {adulto("gestos de cuidado",
              "Cassatt é uma boa porta para conversar sobre cuidado, sobre o que as pessoas da família fazem umas pelas outras. Peça que ela olhe os gestos das mãos nos quadros e depois que mostre o gesto no próprio corpo. "
              "Não é preciso falar de “mães” se a família da criança é de outro jeito: o importante é olhar os gestos.")}"""
    L.add(c, aba="--d-historias")

    apreciar(L, "cassatt_banho", "O banho da criança", "Cassatt, 1893 · um colo, uma bacia e um pé",
             ["Quantas pessoas você vê? O que cada uma está fazendo?", "Onde está a mão da pessoa grande? E o outro braço dela?", "Para onde cada uma olha?", "Onde estão as listras? De que cores elas são?",
              "Procure a jarra de água. Que desenho ela tem?", "Quem dá banho em você? Como é?"],
             "O quadro mostra a cena vista um pouco de cima. A pessoa grande segura o pé da criança dentro da bacia, e as duas olham para a água. A criança está sentada no colo, com um pano branco, "
             "e ao fundo há um papel de parede com flores. Peça que ela mostre, com o próprio corpo, o gesto que vê (segurar, lavar). Depois feche o livro e peça que conte três coisas.",
             "olhar e conversar", "--d-historias", w=95, h=145)

    apreciar(L, "cassatt_poltrona", "Menina na poltrona azul", "Cassatt, 1878 · uma tarde de descanso",
             ["O que a menina está fazendo? Como ela está sentada? Onde está a mão dela?", "Quantas poltronas você vê? De que cor são?", "Procure o cachorrinho. Onde ele está? O que faz?", "Que desenhos tem o tecido das poltronas?",
              "Para onde a menina olha? O que você acha que ela está pensando?", "Onde você gosta de se sentar para descansar?"],
             "Esta obra mostra uma menina de vestido branco e faixa xadrez, quase deitada na poltrona azul, com a mão atrás da cabeça, como as crianças se sentam quando estão cansadas. Peça que ela imite a postura, rindo. "
             "Depois procure junto os detalhes: as outras poltronas, o cachorrinho dormindo numa delas, as flores do tecido e a janela clara ao fundo.",
             "olhar e imaginar", "--d-historias", w=170, h=105)

    apreciar(L, "cassatt_praia", "Crianças brincando na praia", "Cassatt, 1884 · duas crianças, uma pá e um balde",
             ["Quantas crianças você vê? O que cada uma está fazendo?", "O que a criança da frente segura nas mãos?", "Como é o chapéu da outra criança? De que cor é a fita?", "O que aparece lá no alto, no mar? Que cor têm as velas?",
              "Compare com o quadro do banho: o que é igual e o que é diferente?"],
             "É uma boa obra para comparar com <i>O banho da criança</i>: lá a criança é cuidada por alguém; aqui as duas brincam juntas. As duas cenas mostram um momento tranquilo do dia. "
             "Na praia, uma criança senta na areia com um balde e uma pá, e a outra, de chapéu de palha com fita vermelha, está logo atrás. Ao fundo há o mar, com um barco de velas brancas e, mais à esquerda, um barquinho com gente; deixe que ela conte do jeito dela, sem exigir um número. A assinatura fica no canto inferior direito.",
             "olhar e comparar", "--d-historias", w=100, h=145)

    quadros = [("encher a bacia", img("tigela", "46mm", "margin:0 auto")), ("ensaboar", img("sabonete", "46mm", "margin:0 auto")),
               ("secar", img("toalha", "46mm", "margin:0 auto")), ("dormir", img("lua", "46mm", "margin:0 auto"))]
    sequencia(L, "A hora do banho", "recortar os quatro cartões e ordenar, do começo ao fim", quadros,
              adulto("ordenar o cuidado",
                     "Misture os cartões e peça que ela os ordene, contando a hora do banho. Depois, com uma boneca, uma bacia e uma toalha, ela dá banho, seca e põe a boneca para dormir. "
                     "É uma boa hora de falar do que ela mesma já sabe fazer sozinha.", estilo="position:absolute;left:18mm;right:18mm;bottom:16mm"), aba="--d-historias")

    c = f"""<div class="miolo">{titulo("Retrato de quem cuida de mim", "desenhar ou pintar uma pessoa, devagar", 25)}
      <div class="caixa" style="margin-top:6mm;height:150mm"><div class="peq centro">o retrato</div></div>
      <div style="margin-top:6mm;font-size:12pt">Quem é: ______________________________<br>
      <span class="peq">o que essa pessoa faz por mim:</span><div style="border-bottom:0.5pt solid var(--linha);height:10mm"></div><div style="border-bottom:0.5pt solid var(--linha);height:10mm"></div></div></div>
      {adulto("um retrato",
              "Deixe que ela escolha quem retratar: pode ser a mãe, o pai, avó, um irmão, a professora. Ela pode olhar a pessoa ou uma foto; se não quiser, pinta de memória. "
              "Escreva ao lado, com as palavras dela, o que essa pessoa faz por ela. É um bom presente para dar à pessoa retratada.")}"""
    L.add(c, aba="--d-historias")

    diario(L, "Meu álbum de cuidados", "guardar o que ela fez nesta unidade", ["a hora do banho", "um abraço", "uma pessoa que cuida de mim", "o que eu faço pelos outros"], "--d-historias",
           "Cole aqui o que ela desenhou ou pintou, com a data. Peça que diga o que cada desenho mostra e escreva ao lado.")


# ================================================================== U7 MODELAR

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · Modelar", aba="--d-vida",
        pergunta="O que as mãos conseguem fazer com um pedaço de argila?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. Apertar e amassar já é a atividade.",
        objetivos=["Apertar, rolar, beliscar e achatar a massa com as duas mãos.", "Fazer uma bola, uma cobrinha e um vaso de beliscão.",
                   "Fazer um bichinho a partir de formas simples (bola + cobrinha).", "Falar do que fez, sem pressa e sem comparar.", "Guardar a massa e limpar a mesa depois."],
        repertorio="<b>Formas:</b> bola, cobrinha, disco, vaso. <b>Palavras:</b> apertar, rolar, beliscar, achatar, alisar. <b>Línguas:</b> <i>clay · l'argile · argilla</i>.",
        materiais="Argila de modelar ou massa caseira (receita na página seguinte), uma tábua ou prato, um paninho úmido, um pote para guardar; palitos lisos (opcional) para riscar.",
        vida="Lavar as mãos, limpar a mesa com pano úmido e guardar a massa num pote fechado.",
        etapas=[["Apertar, bater e rolar a massa sem forma definida.", "Fazer uma bola entre as palmas.", "Fazer uma cobrinha rolando na mesa."],
                ["Fazer um vaso: abrir a bola com o polegar e girar.", "Juntar bola e cobrinha para fazer um bichinho.", "Alisar com um dedinho de água."],
                ["Inventar uma criatura que não existe.", "Modelar uma pessoa que cuida dela (como Mary Cassatt pintou).", "Dar nome à peça e escolher onde guardá-la."]],
        indicadores=["Rola uma cobrinha de espessura mais ou menos igual.", "Faz uma bola e a achata num disco.", "Beliscando, abre um vaso com paredes mais ou menos finas.",
                     "Junta duas peças com um pouco de água.", "Conta o que fez sem precisar de ajuda.", "Guarda a massa no pote e limpa a mesa."],
        interesse="olhar um vaso, um prato ou uma cuia de verdade e conversar sobre como alguém os fez com as mãos.",
        dificil="só apertar e amassar a massa por alguns minutos, sem fazer nada com ela.",
        alerta="Massa e argila não são para comer, e a massa caseira leva sal e farinha: observe crianças que ainda põem tudo na boca ou com alergia a trigo."))

    itens = [(img("tigela", "20mm"), "Misture 2 xícaras de farinha de trigo e 1 xícara de sal fino numa tigela"),
             (img("jarra", "20mm"), "Junte aos poucos 1 xícara de água morna"),
             (img("gota", "18mm"), "Acrescente 1 colher (sopa) de óleo para a massa ficar macia"),
             (img("palma", "20mm"), "Amasse até desgrudar das mãos, 5 minutos"),
             (img("argila_bola", "20mm"), "Guarde num pote bem fechado, na geladeira"),
             (img("sol", "20mm"), "As peças secam ao ar em 1 a 2 dias, sem forno")]
    passos(L, "Massa caseira de modelar", "uma receita para fazer junto", itens,
           adulto("fazer a massa",
                  "A criança pode medir, despejar e amassar, e isso já é uma atividade completa. A massa dura alguns dias na geladeira, em pote fechado. Peças finas secam ao ar; as grossas demoram e podem rachar. "
                  "Se preferir, use argila de verdade, que dá uma sensação diferente nas mãos. <b>Atenção:</b> o sal em excesso faz mal se comido, e quem tem alergia a trigo deve usar uma massa pronta sem glúten."),
           aba="--d-vida")

    itens = [(img("argila_bola", "22mm"), "Rolar entre as palmas: uma bola"),
             (img("argila_cobra", "22mm"), "Rolar na mesa com os dedos abertos: uma cobrinha"),
             (img("argila_bola", "22mm"), "Achatar a bola com a palma: um disco"),
             (img("argila_vaso", "22mm"), "Enfiar o polegar na bola e beliscar em volta: um vaso"),
             (img("pedra", "22mm"), "Juntar bola e cobrinha com uma gotinha de água: um bichinho"),
             (img("estrela", "20mm"), "Alisar com o dedo úmido ou riscar com um palito liso")]
    passos(L, "Três jeitos de começar", "bola, cobrinha e vaso de beliscão", itens,
           adulto("o jeito das mãos",
                  "Os pratos, os potes e os vasos mais antigos que se conhecem foram feitos exatamente assim: com bolas, cobras e beliscões. Mostre uma vez e deixe que ela descubra o resto. "
                  "Não corrija a forma: se o “bichinho” parecer uma pedra, pergunte o nome dele e acredite. <b>Criar:</b> ela inventa uma criatura que não existe, e você escreve o nome que ela disser."),
           aba="--d-vida")

    c = f"""<div class="miolo">{titulo("Um bichinho de argila", "primeiro desenhar no ar, depois com as mãos", 25)}
      <div class="centro" style="margin:3mm 0">{tira(["argila_bola", "argila_cobra", "argila_vaso", "lebre"], "30mm", "3mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Antes de começar, olhe com ela para um bicho de verdade (um cachorro, um passarinho, um gato) ou para uma figura num livro.
      Pergunte: <i>de quantas bolas é feito o corpo? E a cabeça? Tem rabo? É uma cobrinha, uma bolinha ou um disco?</i></p>
      <div class="caixa" style="margin-top:4mm;height:100mm"><div class="peq centro">desenhar aqui o bichinho que ela vai fazer (ou colar uma foto da peça depois)</div></div></div>
      {adulto("planejar com as mãos e com os olhos",
              "Esta é a hora de olhar antes de fazer. Desenhar o bichinho no papel (ou só descrevê-lo) ajuda a decidir quantas bolas e cobrinhas ele terá, e dá à criança uma pequena sensação de projeto. "
              "Não importa se o resultado não ficar parecido: o que se treina é olhar e fazer.")}"""
    L.add(c, aba="--d-vida")

    diario(L, "Galeria de argila", "colar a foto ou desenhar o que ela modelou", ["minha bola", "minha cobrinha", "meu vaso", "minha criatura"], "--d-vida",
           "Fotografe as peças depois de secas e cole aqui, ou desenhe-as. Escreva o nome que ela deu a cada uma e a data. As peças de massa caseira guardam-se numa caixa de sapatos forrada com papel.")


# ================================================================== U8 COLAR

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · Colar", aba="--d-memoria",
        pergunta="Dá para fazer um quadro só com papel rasgado e cola?",
        duracao="Dois fins de semana · dois encontros · 20 a 30 minutos. O primeiro encontro é só para pintar os papéis.",
        objetivos=["Pintar papéis com guache, livremente, para depois usar na colagem.", "Rasgar e cortar papel (com tesoura sem ponta).", "Passar cola e posicionar as peças com cuidado.",
                   "Compor uma colagem com formas simples (bolas, tiras, manchas).", "Dar nome à colagem."],
        repertorio="<b>Formas:</b> manchas, tiras, círculos, rasgos. <b>Palavras:</b> rasgar, cortar, colar, sobrepor, compor. <b>Línguas:</b> <i>paper · le papier · charta</i>; <i>glue · la colle</i>.",
        materiais="Papéis que ela pintou na primeira sessão (secos), revistas velhas ou papel de embrulho, cola atóxica, tesoura sem ponta, uma folha grossa de fundo.",
        vida="Guardar os pedaços de papel num envelope, jogar as sobras fora e lavar as mãos ao final.",
        etapas=[["Pintar folhas de papel com as tintas da Unidade 1.", "Deixar secar de um dia para o outro.", "Olhar as cores que ficaram."],
                ["Rasgar o papel em tiras e manchas.", "Cortar um círculo, uma tira e um triângulo.", "Experimentar a composição sem colar."],
                ["Colar a composição, uma peça de cada vez.", "Dar um nome à colagem.", "Mostrar para alguém da família."]],
        indicadores=["Rasga o papel em pedaços de tamanhos diferentes.", "Corta uma forma simples com a tesoura sem ponta.", "Passa cola só no verso da peça, sem exagero.",
                     "Experimenta o lugar da peça antes de colar.", "Cola de modo a cobrir parte da folha, sem pressa.", "Conta o que mostra a colagem."],
        interesse="olhar colagens em livros de arte e perguntar o que o artista usou e como as formas foram postas.",
        dificil="só rasgar papel e fazer uma pilha de pedaços coloridos, sem colar nada.",
        alerta="Tesoura sempre sem ponta e cola atóxica; pedaços muito pequenos de papel são risco de engasgo para os menores."))

    itens = [(img("pote_vermelho", "20mm"), "Pinte uma folha de vermelho, outra de amarelo, outra de azul"),
             (img("papel_laranja", "20mm"), "Misture e pinte folhas de laranja, verde e roxo"),
             (img("pincel", "22mm"), "Pinte com manchas largas, em várias direções"),
             (img("sol", "20mm"), "Deixe secar bem, de um dia para o outro"),
             (img("papel_azul", "20mm"), "Olhe as folhas: quais cores ficaram?"),
             (img("cesta", "20mm"), "Guarde as folhas secas num envelope ou numa pasta")]
    passos(L, "Papel pintado por ela", "primeiro encontro: pintar os papéis da colagem", itens,
           adulto("preparar o material",
                  "O papel pintado é a matéria-prima da colagem: ela vai usar cores que ela mesma fez, o que dá orgulho. Use papel um pouco mais grosso e tinta não muito aguada. "
                  "Não peça que ela “pinte bonito”: manchas, riscos e borrões vão funcionar bem depois de rasgados. Deixe secar sobre jornal."),
           aba="--d-memoria")

    itens = [(img("papel_vermelho", "20mm"), "Rasgar: puxar o papel devagar, com as duas mãos"),
             (img("tesoura", "22mm"), "Cortar: um círculo, uma tira e um triângulo"),
             (img("papel_amarelo", "20mm"), "Experimentar: pôr as peças na folha sem colar"),
             (img("cola", "20mm"), "Passar cola só no verso de cada peça"),
             (img("papel_verde", "20mm"), "Colar sobrepondo: uma cor aparece por baixo da outra"),
             (img("estrela", "20mm"), "Dar um nome e assinar com a data")]
    passos(L, "Rasgar, cortar, colar", "segundo encontro: montar a colagem", itens,
           adulto("o artista decide",
                  "Deixe que ela experimente o lugar das peças antes de colar; mudar de ideia faz parte. Rasgar dá um contorno macio; cortar dá contorno reto. Pergunte qual ela prefere. "
                  "<b>Criar:</b> ela escolhe o tema da colagem (um jardim? uma cidade? uma noite?) e você escreve o título que ela disser."),
           aba="--d-memoria")

    formas = "".join(f'<div class="centro">{img(m, "32mm", "margin:0 auto")}</div>' for m in
                     ("papel_vermelho", "papel_amarelo", "papel_azul", "papel_verde", "papel_laranja", "papel_roxo", "papel_rosa", "circulo_azul", "circulo_amarelo"))
    c = f"""<div class="miolo">{titulo("Formas para recortar", "se faltar papel pintado, estas formas servem", 25)}
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6mm 4mm;margin-top:8mm;align-items:center">{formas}</div>
      <div class="caixa" style="margin-top:8mm;height:70mm"><div class="peq centro">colar aqui as formas que ela escolher, na ordem que quiser</div></div></div>
      {adulto("quando faltar papel",
              "Estas formas são desenhos em aquarela da coleção, para quem quiser começar sem pintar papéis antes. Imprima, deixe que ela recorte (com a sua ajuda, se precisar) e cole na caixa de baixo. "
              "O melhor material continua sendo o papel que ela mesma pintou.")}"""
    L.add(c, aba="--d-memoria")

    c = f"""<div class="miolo">{titulo("A minha colagem", "uma folha inteira para ela montar", 28)}
      <div class="caixa" style="margin-top:6mm;height:170mm"></div>
      <div style="margin-top:4mm;font-size:12pt">Nome da colagem: ____________________________________________<br>
      <span class="peq">feita por Marina em ___/___/_____</span></div></div>
      {adulto("uma obra para guardar",
              "Se a colagem ficar em outra folha (um papel maior, uma cartolina), cole aqui uma foto. O título é da criança; escreva o que ela disser. "
              "<b>Sobre os artistas:</b> as colagens de papel recortado de Henri Matisse, feitas nos últimos anos de sua vida, são das mais famosas do mundo. "
              "Como ainda há direitos autorais sobre elas em vários países, não as reproduzimos aqui; vale procurar num livro de arte ou numa visita a um museu.")}"""
    L.add(c, aba="--d-memoria")

    diario(L, "Meu museu de papel", "colar fotos e guardar o que ela fez nesta unidade", ["a colagem de formas", "a colagem do jardim", "a colagem da noite", "uma colagem livre"], "--d-memoria",
           "Cole aqui as colagens menores, ou fotos das maiores. Peça que ela diga o que cada uma mostra e escreva ao lado. Guarde as folhas grandes numa pasta.")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo

    itens = [("Dürer", 1471, 1528, "#5f8f8a"), ("Monet", 1840, 1926, "#5f7f9c"), ("Cassatt", 1844, 1926, "#c0716b"),
             ("Van Gogh", 1853, 1890, "#c9963f"), ("Kandinsky", 1866, 1944, "#8a6f9e")]
    c = f"""<div class="miolo">{titulo("Os artistas desta coleção", "quando viveram", 28)}
      <div style="margin-top:8mm">{linha_do_tempo(itens, 1450, 1960)}</div>
      <table class="tab" style="margin-top:8mm;font-size:11pt">
        <tr><td style="width:32mm"><b>Dürer</b></td><td><i>A lebre jovem</i> e <i>Tufo de prímulas</i> · olhar de perto, pelo, folha por folha</td></tr>
        <tr><td><b>Monet</b></td><td><i>Medas de trigo</i> e <i>Ninfeias</i> · manchas de cor e a luz do dia</td></tr>
        <tr><td><b>Cassatt</b></td><td><i>O banho da criança</i>, <i>Menina na poltrona azul</i> e <i>Crianças brincando na praia</i> · crianças e quem cuida delas</td></tr>
        <tr><td><b>Van Gogh</b></td><td><i>Girassóis</i> · amarelo sobre amarelo</td></tr>
        <tr><td><b>Kandinsky</b></td><td><i>Vários círculos</i> · círculos, cores e música</td></tr></table></div>
      {adulto("o tempo na arte",
              "Mostre as barras como ruas compridas de tempo: Dürer viveu há quase 500 anos; os outros quatro viveram entre os anos 1800 e meados dos anos 1900. Mesmo assim, a lebre de Dürer, o lago de Monet e a poltrona de Cassatt "
              "vivem juntos na mesma parede da sua casa. Pergunte qual ela gostaria de visitar e por quê.")}"""
    L.add(c, aba="--d-artes")

    diario(L, "Meu museu", "colar aqui as obras da coleção de que ela mais gostou, e as dela", ["a obra que eu mais gostei", "a que eu fiz e mais gostei", "a cor da semana", "o que eu quero fazer de novo"],
           "--d-artes", "Peça que ela escolha, entre as páginas olhadas e os trabalhos que fez, o que levaria para um museu só dela. Escreva o motivo da escolha, com as palavras dela.", h="66mm")

    for k in range(2):
        linhas = "".join('<tr><td style="width:36mm;height:44mm"><div class="peq">data</div></td><td style="width:50mm"><div class="peq">obra ou atividade</div></td>'
                         '<td><div class="peq">o que ela viu, fez ou disse</div></td></tr>' for _ in range(5))
        c = f"""<div class="miolo">{titulo("Diário de arte", "para o adulto · o que ela olhou, fez e disse — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Data</th><th>Obra ou atividade</th><th>O que ela viu, fez ou disse</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    obras = "".join(f"<li>{fontes_v5.credito(n)}</li>" for n in fontes_v5.OBRAS)
    c = f"""<div class="miolo texto">{titulo("Obras e créditos", "Volume 5", 26)}
      <h2>Reproduções de obras de arte</h2>
      <p style="font-size:9.2pt">Todas as obras são de artistas mortos há mais de 70 anos e estão em domínio público (ou CC0), segundo a fonte indicada em cada crédito: Wikimedia Commons ou acervo do museu. Os <i>Girassóis</i> foram fornecidos pela editora. As imagens foram reduzidas ao tamanho de impressão, sem retoque de cor. Uma fotografia nunca reproduz fielmente as cores de um original.</p>
      <ul style="font-size:8.4pt;line-height:1.3">{obras}</ul>
      <h2>Fundamentos</h2><p style="font-size:9.4pt">Apreciação de arte por narração e por observação, com poucas obras e muita atenção (Charlotte Mason, <i>estudo de pintores</i>); processo antes do produto; cores primárias e misturas, modelagem e colagem como atividades de ateliê infantil. Nenhum material reproduz métodos ou produtos comerciais.</p>
      <h2>Ilustrações da coleção</h2><p style="font-size:9.4pt">Potes, pincéis, argilas, papéis, ninfeia, lebre, tufo, círculos e demais desenhos: aquarela digital procedural da coleção. Cartões de cores: textos da coleção. Tipografia: EB Garamond (licença OFL).</p>
      <h2>Henri Matisse</h2><p style="font-size:9.4pt">As colagens de papel recortado de Matisse são citadas no texto, mas não reproduzidas, porque as obras ainda têm direitos autorais em vários países.</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 5</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">o livro da natureza:<br>um diário para desenhar o que se vê,<br>as aves do quintal, as árvores e a água da chuva.</p>
      <div style="margin-top:12mm">{tira(["folha", "raminho", "pena", "gota"], "28mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 6 · O livro da natureza</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

def montar(unidades=None):
    L = Livro(5, "O mundo das artes")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidades or (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8)):
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
    for versao, nome in (("impressao", "volume5-impressao"), ("tela", "volume5-tela")):
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume5-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
