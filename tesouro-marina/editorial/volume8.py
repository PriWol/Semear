"""
VOLUME 8 — JOGOS E DESCOBERTAS (primeira versão, estória #112; ADR 0031)
uso: python3 volume8.py
Versão menor do volume: só o que os cadernos de 2 anos prometem para a unidade "Brincar junto" (esperar a vez, mandar e obedecer,
esconder e achar, acalmar) mais o diário de observação do adulto, que o currículo promete desde o Volume 1
(docs/01-arquitetura-curricular.md, Volume 8). Os conjuntos recortáveis completos, os bonecos de vara, os cenários dobráveis e os projetos
integradores ficam para uma edição futura. Todas as figuras são aquarelas da coleção (motivos*.py); não há gravura de domínio público.
"""
import os
import re
import subprocess
import sys

from caderno import AGUA, CAL, COLECAO, TRAD, atividade, cena, rimas   # as mesmas atividades e rimas do caderno de 2 anos, com os mesmos textos de origem
from livro import (Livro, VERSAO, adulto, cartoes, gerar_pdf, guia, img, marcas_corte, memoria, rodape_folha, cabeca_folha, texto, titulo)
from motivos9 import MOTIVOS9
from volume6 import tira   # fila de motivos: a mesma dos outros volumes

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume8")

UNIDADES = [
    ("Bloco 1 · Esconder e achar", "--d-jogos"),
    ("Bloco 2 · Minha vez, sua vez", "--d-memoria"),
    ("Bloco 3 · Mandar e obedecer", "--d-vida"),
    ("Bloco 4 · Calma", "--d-frances"),
    ("Bloco 5 · Diário de observação", "--d-natureza"),
]
INICIO = {}
ICONES = ["bola", "ursinho", "lenco", "cortina", "garrafa_calma"]


def inicio_bloco(L, i):
    L.unidade = UNIDADES[i][0].split(" · ", 1)[1]
    INICIO[UNIDADES[i][0]] = L.proximo


def niveis(a, b, c):
    """Os três níveis de um jogo, com os 2 anos como ponto de partida."""
    return [f"<b>2 anos:</b> {a}", f"<b>3 anos:</b> {b}", f"<b>4 anos:</b> {c}"]


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 8</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">Jogos e<br>descobertas</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:146mm;left:0;right:0">{cena([("cortina", 52, 8, 6), ("bola", 36, 64, 40), ("ursinho", 40, 104, 4), ("lenco", 34, 142, 44), ("garrafa_calma", 34, 20, 66), ("caixa", 38, 100, 60)], 104, 190)}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(["maca", "gato", "casa", "sol", "estrela", "lua"], "15mm", "3mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 8</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">Jogos e descobertas</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">O livro de jogos é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(ICONES, "26mm", "3mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Brincar junto</h1>
      <p>Este é o oitavo livro da coleção, e é uma <b>primeira versão, menor que os outros</b>. Ele traz só os jogos que o <i>Caderno de atividades · 2 anos</i> já promete na unidade
      <i>Brincar junto</i>, mais um diário para o adulto anotar o que viu. Os jogos pensados para crianças maiores (conjuntos grandes de recortar, bonecos, cenários e projetos) ficam para uma edição futura.</p>
      <h2>Três ideias</h2>
      <ul>
        <li><b>Esperar a vez.</b> É uma das coisas mais difíceis dos 2 aos 4 anos. Os jogos são curtos e com poucas peças, e a frase “minha vez, sua vez” vira um hábito que ela pode usar com outras crianças.</li>
        <li><b>Mandar e obedecer.</b> Na fase do “não”, ser a chefe por alguns minutos, dentro de uma regra, é um alívio. Depois ela também segue o comando, e as duas trocam de lugar.</li>
        <li><b>Esconder e achar.</b> Quem some, volta: o “achou!” ensina isso com um abraço. Esconder e procurar também treina a memória e a espera.</li>
      </ul>
      <h2>Sem competição</h2>
      <p>Nenhum jogo deste livro é disputa. O que conta é brincar junto, repetir quantas vezes ela pedir e parar quando ela quiser parar. Se ela não quiser jogar, guarde para outro dia.</p>
      <h2>O que este livro traz</h2>
      <p>Quatro blocos de jogos (<i>esconder e achar</i>, <i>minha vez, sua vez</i>, <i>mandar e obedecer</i> e <i>calma</i>), com cartões, um jogo da memória, um dominó e um loto de figuras para recortar,
      rimas de roda e um diário de observação. Cada jogo tem versões para 2, 3 e 4 anos: comece pela de 2 anos.</p>
      <div class="centro" style="margin-top:6mm">{tira(ICONES, "24mm", "2mm")}</div>""")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este livro</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Pouco, de vez em quando, junto</h1>
      <table class="tab">
        <tr><th>Ritmo</th><td>De 5 a 10 minutos, um jogo por vez. Pode ser repetido muitas vezes: repetir é o jeito de aprender, e não sinal de que ela “acabou”.</td></tr>
        <tr><th>Poucas peças</th><td>Comece com poucas peças na mesa (3 pares na memória, 4 figuras no loto) e aumente só quando ela pedir mais.</td></tr>
        <tr><th>A vez</th><td>Diga sempre “minha vez” e “sua vez”, e espere uns segundos. Se ela quiser ficar com a peça, diga “agora é a minha, e depois a sua”. Esperar é um treino, não uma obrigação perfeita.</td></tr>
        <tr><th>Sem prova</th><td>Não há resposta errada nem pontos. Se ela inventar outra regra, brinque com a regra dela: está criando.</td></tr>
        <tr><th>Recortar</th><td>O adulto recorta as peças nas linhas tracejadas e guarda numa caixa. Papel de 180 g ou mais dura mais. As peças recortadas ficam fora do alcance dela quando o jogo acaba.</td></tr>
        <tr><th>Fim do jogo</th><td>Combine antes: “mais uma vez e acabou”. Avisar o fim evita muita birra.</td></tr>
      </table>
      <div class="centro" style="margin-top:6mm">{tira(["bola", "ursinho", "lenco", "cortina"], "26mm")}</div>""")


def parcial(inicio=None):
    """Verdadeiro se faltar algum bloco no arquivo: o workflow gera o PDF a cada merge, e o sumário não pode prometer o que não tem."""
    return False if inicio is None else not all(n in inicio for n, _ in UNIDADES)


def sumario(inicio):
    feitas = [(n, cor) for n, cor in UNIDADES if n in inicio]
    linhas = ""
    if "Antes de brincar" in inicio:
        linhas += f'<tr><td></td><td style="font-size:13pt">Antes de brincar · níveis e cuidados</td><td class="pg">{inicio["Antes de brincar"]}</td></tr>'
    linhas += "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                      f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio[n]}</td></tr>' for n, cor in feitas)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    aviso = ('<p class="peq centro" style="margin-top:6mm;font-style:italic">Edição em produção: alguns blocos ainda não estão neste arquivo.</p>' if parcial(inicio) else "")
    return f"""<div class="miolo">{titulo("Sumário", "Volume 8 · Jogos e descobertas", 30)}<table class="sumario">{linhas}</table>{aviso}
      <div class="centro" style="margin-top:8mm">{tira(["bola", "ursinho", "lenco", "cortina", "garrafa_calma", "caixa"], "22mm", "1.5mm")}</div></div>"""


def antes_de_brincar(L):
    INICIO["Antes de brincar"] = L.proximo
    linhas = [("Esconde-esconde", "um esconderijo; você procura devagar", "ela escolhe o esconderijo e conta até três", "ela esconde um objeto e você pergunta “está perto ou longe?”"),
              ("A caixa surpresa", "3 objetos e um só na caixa", "5 objetos; ela diz uma pista (“é redondo”)", "os 9 cartões: ela acha o cartão do que sentiu"),
              ("Memória", "3 pares, viradas para cima", "4 a 5 pares, viradas para baixo", "6 pares, viradas para baixo"),
              ("Minha vez, sua vez", "rolar a bola entre duas pessoas", "três pessoas, na roda", "dominó e loto, esperando a vez de cada um"),
              ("A chefe mandou", "um gesto de cada vez", "dois gestos em seguida", "três gestos, ou o “contrário”"),
              ("Calma", "3 respirações com o bichinho", "5 respirações, contando", "ela escolhe o jeito de se acalmar")]
    tab = "".join(f"<tr><th>{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in linhas)
    L.unidade = ""
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Antes de brincar</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:3mm">Três idades, um ponto de partida</h1>
      <p>Cada jogo começa na versão de <b>2 anos</b>. Se ela se divertir, passe para a de <b>3 anos</b> e depois para a de <b>4 anos</b>. A idade é só uma pista: o ritmo é dela.</p>
      <table class="tab" style="margin-top:2mm"><tr><th>Jogo</th><th>2 anos</th><th>3 anos</th><th>4 anos</th></tr>{tab}</table>
      <h2>Cuidados</h2>
      <ul>
        <li><b>Peças pequenas:</b> objetos e peças só <b>maiores que o punho dela</b> e sem pontas; nada que caiba na boca.</li>
        <li><b>Esconderijos seguros:</b> cortina, atrás da porta, embaixo da mesa; <b>nada de geladeira</b>, baú, caixa fechada ou lugar pequeno demais. O adulto vê onde ela está o tempo todo.</li>
        <li>Água só com um adulto junto o tempo todo. A garrafa da calma é feita só pelo adulto.</li>
        <li>Este livro não é avaliação e não faz diagnóstico: se tiver dúvidas sobre fala, audição ou desenvolvimento, converse com o pediatra.</li>
      </ul>""")


# ================================================================== BLOCO 1 · ESCONDER E ACHAR

MEMO = [("gato", "gato"), ("maçã", "maca"), ("casa", "casa"), ("sol", "sol"), ("lua", "lua"), ("pão", "pao")]


def bloco1(L):
    inicio_bloco(L, 0)
    guia(L, dict(
        titulo="Esconder e achar", aba="--d-jogos",
        pergunta="Como brincar de sumir e aparecer sem medo, e o que muda dos 2 aos 4 anos?",
        duracao="De 5 a 10 minutos, um jogo por vez · quantas vezes ela pedir.",
        objetivos=["Perceber que quem some, volta, e que o “achou!” é uma festa.", "Sentir com a mão e dizer o nome do que está na caixa.", "Lembrar onde está uma figura, na memória.", "Esperar três segundos antes de procurar."],
        repertorio="<b>Em português:</b> cadê, achou, escondido, dentro, fora, atrás, embaixo e o nome dos objetos de casa. <b>Rima:</b> <i>Cadê? Achou!</i>, escrita pela coleção.",
        materiais="Uma cortina ou uma porta; uma caixa com buraco do tamanho da mão; os cartões <i>O que está na caixa?</i> e o jogo da memória recortados; objetos de casa maiores que o punho dela.",
        vida="Brincar de achar: “cadê a meia? cadê o chinelo?” na hora de vestir; “cadê a colher?” na hora de pôr a mesa.",
        etapas=[["Esconder-se devagar, com um pedacinho à mostra.", "Pôr a mão na caixa e sentir, sem olhar.", "Olhar as figuras dos cartões e dizer o nome."],
                ["Achar a figura igual na memória.", "Ligar o objeto da caixa ao cartão.", "Contar até três antes de procurar."],
                ["Esconder um bichinho para o adulto achar.", "Escolher o que vai na caixa.", "Inventar uma pista: “é redondo”."]],
        indicadores=["Ri ou se surpreende no “achou!”.", "Fica esperando o adulto aparecer.", "Põe a mão na caixa sem medo.", "Diz o nome de um objeto sem olhar.",
                     "Vira duas cartas e as compara.", "Pede o jogo de novo."],
        interesse="mais pares na memória, mais objetos na caixa, ela como “escondedora” e você como quem procura.",
        dificil="só “cadê? achou!” com as mãos no rosto do adulto, no colo. Um minuto basta.",
        alerta="Nunca cubra o rosto dela, nem a esconda em lugar fechado. Se ela se assustar com o escuro, a cortina, a caixa ou o sumiço, pare e abrace."))

    atividade(L, "Esconde-esconde", "corpo", "5 a 10 minutos",
              "uma casa ou um quarto com cantinhos seguros (cortina, atrás da porta, embaixo da mesa)",
              cena([("cortina", 32, 8, 6), ("porta_aberta", 32, 50, 6), ("coracao", 26, 92, 20), ("carinha_feliz", 28, 128, 12), ("ursinho", 28, 160, 12)], 46, 190),
              ["Esconda-se atrás da cortina, deixando um pedacinho à mostra, e diga: “cadê o papai? cadê a mamãe?”.", "Quando ela chegar, abrace: “achou!”.", "Troque: ela se esconde, e você procura devagar, fingindo que não acha.",
               "Combine o fim: “mais uma vez e acabou”."],
              ["Cadê o papai? Será que está aqui?", "Achou! Que abraço!", "Agora você se esconde. Eu conto até três."],
              ["Onde está o papai?", "Quer se esconder?", "Quer que eu procure?"],
              "Esconder e achar traz a certeza de que quem some, volta, e o abraço do “achou!” é um pequeno reencontro. Contar até três antes de procurar treina a espera, e esconder-se treina a memória.",
              atencao="esconderijos seguros: nada de geladeira, caixas fechadas ou lugares pequenos demais.",
              variar=niveis("você se esconde e ela procura.", "ela se esconde e conta até três antes de você procurar.", "ela esconde um brinquedo e você pergunta “está perto ou longe?”."), registro="Hoje a Marina… (onde se escondeu, o que disse) — data: ______")

    atividade(L, "A caixa surpresa", "nomear", "5 minutos",
              "uma caixa de sapato com um buraco do tamanho da mão; 3 ou 4 objetos de casa maiores que o punho dela",
              cena([("caixa", 40, 12, 12), ("mao", 34, 60, 8), ("colher", 30, 100, 16), ("maca", 26, 138, 14), ("bola", 28, 164, 14)], 48, 190),
              ["Ponha um objeto na caixa sem que ela veja.", "Peça que ela ponha a mão pelo buraco e apalpe.", "Pergunte: “o que será?”. Aceite “não sei” e dê pistas: “é redondo”, “serve para comer”.", "Tire o objeto e comemore: “era uma maçã!”."],
              ["Põe a mão aqui. O que será?", "É redondo e liso… é uma maçã!", "Agora você escolhe o que esconder."],
              ["É duro ou mole?", "É grande ou pequeno?", "O que será?"],
              "Sentir sem ver treina o tato e o vocabulário, e “não sei” é uma resposta boa. Quando ela escolhe o que esconder, liderar o jogo ajuda quem tem muita vontade própria. Os cartões da página seguinte mostram os mesmos objetos.",
              atencao="só objetos maiores que o punho dela e sem pontas.",
              variar=niveis("um objeto por vez, com pista.", "cinco objetos na mesa; ela tira um e diz o nome.", "ela acha o cartão do que sentiu."), registro="Hoje a Marina… (o que adivinhou, que pista pediu) — data: ______")

    objetos = [dict(pt="maçã", mot="maca", en="apple", fr="pomme", la="mālum", dica="redonda e lisa: é a mesma maçã do Volume 1"),
               dict(pt="colher", mot="colher", en="spoon", fr="cuillère", la=None, dica="comprida, com uma concha numa ponta"),
               dict(pt="bola", mot="bola", en="ball", fr="balle", la=None, dica="redonda e macia: rola de um lado para o outro"),
               dict(pt="ursinho", mot="ursinho", en="teddy bear", fr="ours en peluche", la=None, dica="macio e peludo: é bom de abraçar"),
               dict(pt="pera", mot="pera", en="pear", fr="poire", la="pirum", dica="mais fina em cima e redonda embaixo"),
               dict(pt="laranja", mot="laranja", en="orange", fr="orange", la=None, dica="redonda, com a casca grossa e cheirosa"),
               dict(pt="xícara", mot="xicara", en="cup", fr="tasse", la=None, dica="oca por dentro, com uma alça"),
               dict(pt="sabonete", mot="sabonete", en="soap", fr="savon", la=None, dica="liso e cheiroso"),
               dict(pt="toalha", mot="toalha", en="towel", fr="serviette", la=None, dica="macia, para secar as mãos")]
    cartoes(L, "O que está na caixa?", objetos, "Volume 8 · O que está na caixa?",
            nota_latim="Latim: vogal com traço (ā, ē, ī, ō, ū) é longa · só curiosidade: ninguém precisa decorar")

    itens = [(r, img(m, "34mm")) for r, m in MEMO]
    memoria(L, "Achados de casa", itens, [3, 0, 5, 1, 4, 2, 2, 5, 0, 3, 1, 4],
            adulto("como brincar",
                   "<b>2 anos:</b> separe só 3 pares e deixe todas as cartas viradas para cima: ela procura a igual. <b>3 anos:</b> 4 ou 5 pares, viradas para baixo. <b>4 anos:</b> os 6 pares. "
                   "Cada um vira duas cartas por vez, na sua vez; se forem iguais, ficam com quem achou, e se não forem, voltam. Ninguém conta pontos: o jogo acaba quando todas forem achadas."))

    rimas(L, "Esconder, achar e cantar", [
        dict(t="Cadê? Achou!", linhas=["Cadê a Marina?", "Cadê, cadê?", "Está escondida?", "Eu vou achar você!", "Achou! Achou!", "Achou! Achou!"],
             gesto="cubra o <b>seu</b> rosto com as mãos (ou com um lenço leve que ela possa puxar) nos primeiros versos e descubra no “achou”. Nunca cubra o rosto dela. Ela pode pedir muitas vezes: repita.",
             origem=COLECAO, motivos=["cortina", "olho", "carinha_feliz"])],
        "O “cadê? achou!” treina a antecipação (o que vem depois?) e o susto bom. Sentadas no colo, com a rima, o esconder e o achar viram um jeito de brincar com a separação, sem pressa.")


# ================================================================== BLOCO 2 · MINHA VEZ, SUA VEZ

def folha_recortavel(L, t, sub, celulas, cols, rows, cw, ch, gx, gy, adulto_html="", rodape=""):
    """Folha de peças soltas (dominó, loto, fichas): grade tracejada, marcas de corte e nada no verso."""
    c = f"""{cabeca_folha(t, sub, 12)}
    <div class="grade" style="left:{gx}mm;top:{gy}mm;grid-template-columns:repeat({cols},{cw}mm);grid-template-rows:repeat({rows},{ch}mm)">{''.join(celulas)}</div>
    {marcas_corte(gx, gy, cols, rows, cw, ch)}{adulto_html}"""
    return L.add(c + rodape_folha(f"{L.proximo} · {rodape}"), moldura=False, cabecalho=False, numero=False)


def bloco2(L):
    inicio_bloco(L, 1)
    guia(L, dict(
        titulo="Minha vez, sua vez", aba="--d-memoria",
        pergunta="Como esperar a vez e dividir uma peça, num jogo em que ninguém precisa perder?",
        duracao="De 5 a 10 minutos · jogos curtos, para repetir.",
        objetivos=["Dizer “minha vez” e “sua vez” e esperar a vez do outro.", "Comparar duas figuras e achar a igual.", "Combinar a figura da peça com a do jogo (dominó e loto).", "Terminar o jogo juntas, sem pressa."],
        repertorio="<b>Em português:</b> minha vez, sua vez, igual, diferente, outra, de novo e os nomes das figuras (maçã, gato, casa, sol, lua, pão, folha, bola, ursinho, peixe, flor, estrela).",
        materiais="Uma bola leve ou uma meia enrolada; o dominó, o loto e as fichas da vez, recortados; uma caixa para guardar as peças.",
        vida="Revezar na hora de pôr a mesa (“você põe o prato, eu ponho o garfo”), de lavar as mãos e de escolher a música.",
        etapas=[["Rolar a bola e dizer “minha vez”.", "Olhar as figuras do dominó e dizer os nomes.", "Mostrar a ficha da vez."],
                ["Achar a peça com a figura igual.", "Pôr cada ficha de loto no lugar.", "Esperar o outro terminar a sua vez."],
                ["Montar a fila do dominó, peça com peça.", "Dizer de quem é a vez sem ajuda.", "Convidar uma terceira pessoa."]],
        indicadores=["Rola a bola de volta.", "Diz “minha vez” ou “sua vez” sozinha.", "Espera o outro sem tomar a peça.", "Acha a figura igual.", "Fica brava e depois se recompõe.", "Pede para jogar de novo."],
        interesse="mais pessoas na roda, mais peças no dominó, ela como quem distribui as peças.",
        dificil="só rolar a bola, duas ou três vezes. Esperar a vez já é um jogo inteiro.",
        alerta="Aos 2 anos é normal ficar brava quando a peça vai embora. Dê nome ao que ela sente (“você queria ficar com ela”) e continue, sem sermão. Guarde as peças recortadas depois do jogo."))

    atividade(L, "Minha vez, sua vez", "conversar", "5 minutos",
              "uma bola leve ou uma meia enrolada; um espaço no chão",
              cena([("bola", 32, 12, 12), ("pegada", 17, 54, 6), ("pegada_esq", 17, 86, 6), ("maos_juntas", 32, 124, 12), ("laranja", 24, 164, 18)], 46, 190),
              ["Sentem no chão, de frente, a uns dois passos. Role a bola devagar até ela: “minha vez!”.", "Quando ela rolar de volta: “sua vez!”.", "Deixe uma pausa e espere. Se ela quiser ficar com a bola, diga “agora é a minha, e depois a sua”.",
               "Chame outra pessoa para a roda quando ela já souber."],
              ["Minha vez! Lá vai a bola.", "Agora é a sua vez!", "Obrigada por devolver. Que bom brincar com você."],
              ["De quem é a vez?", "Quer rolar forte ou fraco?", "Quem rola agora?"],
              "Esperar a vez é um treino de segurar o desejo de ter a bola o tempo todo. Revezar com poucas palavras, em jogos curtos, dá a ela uma frase para usar com outras crianças. "
              "É normal que ela fique brava quando a bola vai embora: nomeie o que ela sente e continue.",
              variar=niveis("só você e ela, a bola rolando.", "três pessoas, em roda.", "cada um diz o nome de quem recebe a bola."), registro="Hoje a Marina… (esperou? disse “minha vez”?) — data: ______")

    pecas = [("maca", "maçã"), ("gato", "gato"), ("casa", "casa"), ("sol", "sol"), ("lua", "lua"), ("pao", "pão"),
             ("folha", "folha"), ("bola", "bola"), ("ursinho", "ursinho"), ("peixe", "peixe"), ("flor_rosa", "flor"), ("estrela", "estrela")]
    dom = []
    for i in range(12):   # cada peça junta duas figuras vizinhas do anel: a última volta à primeira
        (m1, _), (m2, _) = pecas[i], pecas[(i + 1) % 12]
        dom.append(f'<div class="carta"><div class="borda"></div><div style="display:flex;align-items:center;justify-content:space-around;width:100%;height:100%;line-height:0">'
                   f'{img(m1, "25mm")}<div style="width:0.6pt;height:24mm;background:var(--linha)"></div>{img(m2, "25mm")}</div></div>')
    folha_recortavel(L, "Dominó de figuras", "12 peças · imprimir em papel de 180 g ou mais · cortar nas linhas tracejadas", dom, 2, 6, 80, 36, 25, 28,
                     adulto("como brincar",
                            "Misture as peças com as figuras para cima. Comecem por uma peça qualquer: cada um, na sua vez, põe uma peça cuja figura seja igual à ponta da fila. "
                            "As peças formam um anel, e o jogo termina quando a fila fecha. <b>2 anos:</b> só 4 peças, e você ajuda a achar a igual."), "Volume 8 · Dominó")

    gr = [[("maca", "maçã"), ("gato", "gato"), ("casa", "casa"), ("sol", "sol")], [("lua", "lua"), ("pao", "pão"), ("folha", "folha"), ("bola", "bola")],
          [("ursinho", "ursinho"), ("peixe", "peixe"), ("flor_rosa", "flor"), ("estrela", "estrela")]]
    cartelas = ""
    for k, cart in enumerate(gr):
        x = 15 + k * 62
        cel = "".join(f'<div class="carta"><div class="borda"></div>{img(m, "21mm")}</div>' for m, _ in cart)
        cartelas += (f'<div class="peq" style="position:absolute;left:{x}mm;top:30mm;width:56mm;text-align:center">cartela {k + 1}</div>'
                     f'<div class="grade" style="left:{x}mm;top:36mm;grid-template-columns:repeat(2,28mm);grid-template-rows:repeat(2,28mm)">{cel}</div>')
    fichas = [f'<div class="carta"><div class="borda"></div>{img(m, "24mm")}<div class="peq" style="margin-top:.5mm">{r}</div></div>' for g in gr for m, r in g]
    c = f"""{cabeca_folha("Loto de figuras", "3 cartelas e 12 fichas · imprimir em papel de 180 g ou mais · cortar as fichas nas linhas tracejadas", 12)}
    {cartelas}
    <div class="grade" style="left:25mm;top:112mm;grid-template-columns:repeat(4,40mm);grid-template-rows:repeat(3,40mm)">{''.join(fichas)}</div>
    {marcas_corte(25, 112, 4, 3, 40, 40)}
    {adulto("como brincar", "Cada um escolhe uma cartela e deixa as fichas misturadas, viradas para cima. Na sua vez, escolhe uma ficha e diz o nome da figura; se ela estiver na sua cartela, põe lá; se não, entrega a ficha a quem precisa dela. "
                            "Todos terminam juntos. <b>2 anos:</b> só uma cartela e as 4 fichas dela. As fichas são maiores que o punho dela e, quando o jogo acaba, vão para a caixa, fora do alcance.")}"""
    L.add(c + rodape_folha(f"{L.proximo} · Volume 8 · Loto"), moldura=False, cabecalho=False, numero=False)

    vez = []
    for i in range(8):
        minha = i % 2 == 0
        vez.append(f'<div class="carta"><div class="borda"></div>{img("mao" if minha else "mao_acenando", "26mm")}<div class="palavra">{"minha vez" if minha else "sua vez"}</div></div>')
    folha_recortavel(L, "Fichas da vez", "8 fichas · uma cor de mão para “minha vez” e outra para “sua vez” · cortar nas linhas tracejadas", vez, 2, 4, 80, 50, 25, 32,
                     adulto("como brincar",
                            "A ficha na mão de quem está jogando mostra de quem é a vez. Ao passar a bola ou a peça, passe também a ficha, dizendo “sua vez”. Com crianças pequenas, uma ficha só já basta."), "Volume 8 · Fichas da vez")


# ================================================================== BLOCO 3 · MANDAR E OBEDECER

def bloco3(L):
    inicio_bloco(L, 2)
    guia(L, dict(
        titulo="Mandar e obedecer", aba="--d-vida",
        pergunta="Como ser a chefe por alguns minutos e depois seguir quem manda, e voltar a ser as duas?",
        duracao="De 5 minutos, com as rimas de roda de 2 minutos cada.",
        objetivos=["Dar uma ordem simples, como bater palmas, e ser obedecida.", "Seguir um gesto do outro, olhando e imitando.", "Parar quando o gesto de parar aparece (mãos no peito).", "Cantar e fazer o gesto da rima de roda."],
        repertorio="<b>Em português:</b> a chefe mandou, palmas, pular, parar, escutar, soprar, piscar. <b>Rimas:</b> <i>Corre, cotia</i> e <i>Um elefante</i>, tradicionais brasileiras.",
        materiais="Um espaço livre; os cartões <i>A chefe mandou</i> recortados; um lenço para a roda.",
        vida="Pedir e receber ajuda: “a chefe mandou trazer o sapato”, e esperar o “obrigada”.",
        etapas=[["Olhar um gesto e imitar.", "Mostrar o cartão e fazer o gesto.", "Ouvir a rima e andar em roda."],
                ["Mandar um gesto e ver o outro fazer.", "Escolher o cartão do gesto que quer.", "Parar com as mãos no peito."],
                ["Dar a ordem e depois obedecer.", "Combinar dois gestos em seguida.", "Escolher uma voz para o elefante."]],
        indicadores=["Imita um gesto sem ajuda.", "Pede “agora eu mando”.", "Para quando o gesto de parar aparece.", "Ri ao ver o adulto obedecer.", "Escolhe um cartão.", "Canta ou faz o gesto da rima."],
        interesse="dois gestos em seguida, o “contrário” (a chefe manda pular e todos ficam parados), uma terceira pessoa como chefe.",
        dificil="só um gesto: palmas, e o gesto de parar. Uma ordem basta.",
        alerta="Mandar é um jogo com regra: a chefe nunca manda um gesto que machuque ou que envergonhe alguém, e o gesto de parar (mãos no peito) sempre vale."))

    atividade(L, "Siga a Marina", "corpo", "5 minutos",
              "um espaço livre; se quiser, os cartões da próxima folha",
              cena([("pegada", 17, 14, 6), ("mao", 34, 52, 10), ("pe", 28, 92, 18), ("estrela", 24, 130, 12), ("coracao", 26, 160, 18)], 46, 190),
              ["Diga: “hoje a Marina é a chefe”. Ela faz um gesto (palmas, pular, uma volta) e você imita.", "Troque de chefe: agora você faz um gesto e ela imita.", "Combine um gesto para parar: mãos no peito.", "Terminem com o gesto de que cada uma mais gostou."],
              ["A chefe mandou: palmas! Eu faço igual.", "Agora o gesto da chefe é pular.", "A chefe mandou parar? Mãos no peito."],
              ["O que a chefe manda?", "Quer ser a chefe ou seguir?", "E agora, o que fazemos?"],
              "Ser a chefe, por um tempo e dentro de uma regra, é uma boa resposta à fase do “não”: ela exerce o poder que tanto procura. Obedecer também faz parte do jogo, e o gesto de parar é uma pausa que ela conhece.",
              variar=niveis("um gesto por vez.", "dois gestos em seguida.", "três gestos, ou o “contrário”: a chefe manda pular e todos ficam parados."), registro="Hoje a Marina… (que gesto mandou, parou?) — data: ______")

    gestos = [dict(pt="acenar", mot="mao_acenando", en="wave", fr="saluer de la main", la=None, dica="a chefe manda e todos acenam"),
              dict(pt="bater palmas", mot="maos_juntas", en="clap", fr="applaudir", la=None, dica="palmas devagar e depressa"),
              dict(pt="joinha", mot="polegar_cima", en="thumbs up", fr="pouce levé", la=None, dica="o polegar para cima quer dizer “tudo bem”"),
              dict(pt="dizer não", mot="dedo_nao", en="say no", fr="dire non", la=None, dica="com o dedo, devagar e sorrindo"),
              dict(pt="bater o pé", mot="pe", en="stomp", fr="taper du pied", la=None, dica="um, dois, três pisões"),
              dict(pt="soprar", mot="boca", en="blow", fr="souffler", la=None, dica="soprar como quem apaga uma vela"),
              dict(pt="piscar", mot="olho", en="blink", fr="cligner de l’œil", la=None, dica="piscar os dois olhos, devagar"),
              dict(pt="escutar", mot="orelha", en="listen", fr="écouter", la=None, dica="a mão na orelha e todos em silêncio"),
              dict(pt="mãos no peito", mot="coracao", en="hands on heart", fr="mains sur le cœur", la=None, dica="o gesto de parar: sempre vale")]
    cartoes(L, "A chefe mandou", gestos, "Volume 8 · A chefe mandou",
            sub_frente="frente · a chefe escolhe um cartão e faz o gesto · imprimir frente e verso (virar pela borda longa) em papel de 180 g ou mais",
            nota_latim="Cada verso diz o gesto em inglês e em francês, só como curiosidade: o jogo é em português")

    rimas(L, "Para brincar de roda", [
        dict(t="Corre, cotia", linhas=["Corre, cotia, na casa da tia,", "corre, cipó, na casa da avó;", "lencinho na mão, caiu no chão."],
             gesto="em roda, com poucas pessoas, uma anda por fora com um lencinho e deixa cair atrás de alguém. Com a Marina, deixe cair atrás dela e corra de mão dada.", origem=TRAD, motivos=["lenco", "casinha"]),
        dict(t="Um elefante", linhas=["Um elefante incomoda muita gente;", "dois elefantes incomodam, incomodam muito mais.", "Três elefantes incomodam muita gente;", "quatro elefantes incomodam, incomodam, incomodam muito mais."],
             gesto="mostre os dedos para cada número; cada elefante é uma voz mais grossa. Faça a tromba com o braço e deixe que ela escolha a voz.", origem=TRAD, motivos=["elefante"])],
        "As duas rimas são conhecidas de jogos de roda e juntam corpo, risada e ritmo. Dá para fazer em qualquer lugar, com qualquer idade, e a Marina pode conduzir a roda.")


# ================================================================== BLOCO 4 · CALMA

def bloco4(L):
    inicio_bloco(L, 3)
    guia(L, dict(
        titulo="Calma", aba="--d-frances",
        pergunta="Como brincar de acalmar nos dias tranquilos, para já conhecer o caminho nos dias difíceis?",
        duracao="De 3 a 10 minutos · de preferência no fim do dia, quando está tudo bem.",
        objetivos=["Respirar devagar, vendo o bichinho subir e descer.", "Olhar o glitter descer na garrafa da calma.", "Balançar com uma rima lenta.", "Pedir para ir ao cantinho da calma."],
        repertorio="<b>Em português:</b> devagar, respirar, subir, descer, calma, abraço. <b>Rima:</b> <i>O barquinho de papel</i>, escrita pela coleção.",
        materiais="Um bichinho de pelúcia leve; uma garrafa da calma, feita só pelo adulto; uma manta ou tapete macio.",
        vida="Uma respiração lenta antes de comer, e um “agora vamos devagar” antes de sair de casa.",
        etapas=[["Deitar e ver o bichinho subir e descer.", "Olhar o glitter descer na garrafa.", "Ouvir a rima balançando."],
                ["Respirar juntas, contando devagar.", "Escolher a cor da garrafa.", "Balançar com o ritmo da rima."],
                ["Escolher sozinha o jeito de se acalmar.", "Ensinar o bichinho a respirar.", "Pedir a garrafa ou o cantinho."]],
        indicadores=["Acompanha o bichinho com os olhos.", "Respira mais devagar.", "Pede a garrafa da calma.", "Balança com a rima.", "Procura o cantinho da calma.", "Se acalma mais depressa que antes."],
        interesse="uma respiração contada de 1 a 5, e uma segunda garrafa de outra cor.",
        dificil="só um abraço e a rima do barquinho, bem baixinho. A calma do adulto é o que ela “pega”.",
        alerta="Estas brincadeiras não são castigo nem substituem o abraço. Se as crises ficarem muito longas, frequentes ou intensas, converse com o pediatra."))

    atividade(L, "Respirar com o bichinho", "acalmar", "3 a 5 minutos",
              "um bichinho de pelúcia leve; uma manta ou tapete macio",
              cena([("cama", 36, 12, 14), ("ursinho", 28, 56, 12), ("nuvem", 34, 98, 10), ("coracao", 26, 142, 14)], 46, 190),
              ["Deitem de barriga para cima. Ponha o bichinho na barriga dela.", "Inspirem pelo nariz, devagar: o bichinho sobe. Expirem pela boca: ele desce.", "Faça junto, com o seu bichinho (ou a mão) na sua barriga.", "Repitam cinco vezes e terminem com um abraço no bichinho."],
              ["O ursinho sobe… e desce.", "Sobe de novo… e desce devagar.", "Que respiração! O bichinho dormiu."],
              ["O bichinho está subindo?", "E agora está descendo?", "Quer fazer de novo?"],
              "Ver o bichinho subir e descer faz a respiração virar algo que ela vê e sente. Funciona bem no fim do dia ou depois de uma crise, quando ela já está mais calma.",
              atencao="o bichinho fica só na barriga, nunca no rosto ou no pescoço; leve e sem peças soltas.",
              variar=niveis("3 respirações.", "5 respirações, contando.", "ela ensina o bichinho a respirar."), registro=CAL)

    atividade(L, "A garrafa da calma", "acalmar", "10 minutos",
              "uma garrafa plástica transparente e pequena, água morna, uma colher de cola líquida transparente, glitter grosso, cola quente e fita",
              cena([("garrafa_calma", 34, 14, 6), ("estrela", 24, 58, 6), ("estrela", 20, 80, 24), ("gota", 18, 108, 14), ("coracao", 26, 144, 12)], 48, 190),
              ["<b>O adulto enche a garrafa</b> com água morna (testada no pulso, nunca quente) e <b>só ele põe o glitter e a cola</b>; ela escolhe a cor e olha.", "O adulto acrescenta uma colher de cola líquida, que deixa o glitter descer devagar.",
               "<b>O adulto fecha a tampa com cola quente e fita</b>, longe dela, e testa se não vaza.", "Chacoalhem juntas e olhem o glitter descer, respirando devagar."],
              ["Vamos fazer uma garrafa mágica.", "Chacoalha… e olha o glitter descer, devagar, devagar.", "Quando fico brava, posso olhar a garrafa e respirar."],
              ["Para onde vai o glitter?", "Está caindo devagar ou depressa?", "Onde vamos guardar a garrafa?"],
              "Ver o glitter descer dá a ela algo para acompanhar com os olhos enquanto respira, e fazer a garrafa juntas a torna “dela”. <b>Guarde a garrafa fora do alcance dela</b> e leve-a ao cantinho da calma só quando estiverem juntas, "
              "com ela já mais tranquila, nunca como castigo.",
              atencao="só use com você por perto, e troque a garrafa se vazar ou rachar. Não é brinquedo para jogar, morder ou abrir. " + AGUA,
              variar=niveis("só olhar a garrafa no colo.", "contar quantas respirações o glitter leva para descer.", "escolher a cor do glitter e pedir a garrafa quando precisar."), registro=CAL)

    rimas(L, "Para balançar", [
        dict(t="O barquinho de papel", linhas=["Barquinho de papel", "vai passear no rio:", "balança pra lá,", "balança pra cá,", "chega devagar", "e vem me abraçar."],
             gesto="sentadas, balancem de um lado para o outro, devagar, como um barquinho na água calma; no último verso, abracem-se.", origem=COLECAO, motivos=["barquinho", "m_riacho", "coracao"])],
        "O barquinho é uma rima da coleção, para balançar com calma. Funciona no fim do dia e depois de uma crise, como retorno à proximidade.", tipo="acalmar")


# ================================================================== BLOCO 5 · DIÁRIO

def diario(L):
    inicio_bloco(L, 4)
    for _ in range(2):
        linhas = "".join('<tr><td style="width:34mm;height:36mm"><div class="peq">data e jogo</div></td><td><div class="peq">o que ela disse, fez ou pediu</div></td>'
                         '<td><div class="peq">uma ideia para outro dia</div></td></tr>' for _ in range(5))
        L.add(f"""<div class="miolo">{titulo("Diário de observação", "para o adulto · não é avaliação", 26)}
          <table class="tab diario"><tr><th>Data e jogo</th><th>O que vi</th><th>O que tentar depois</th></tr>{linhas}</table>
          <p class="peq" style="margin-top:2mm">Escreva só o que viu, com as palavras dela. Sem comparar com outras crianças, sem metas: o diário é para você olhar a Marina crescer.</p></div>""", aba="--d-natureza")


# ================================================================== ENCERRAMENTO

def gravuras_usadas(L):
    """Nomes das gravuras de domínio público que aparecem nas páginas já montadas (nenhuma nesta versão: todas as figuras são aquarelas da coleção)."""
    nomes = []
    for _, h in L.paginas:
        for n in re.findall(r"dominio_publico/v1/([a-z0-9_]+?)_(?:branco|creme)\.jpg", h):
            if n not in nomes:
                nomes.append(n)
    return nomes


def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo
    L.add(f"""<div class="miolo texto">{titulo("Rimas e créditos", "Volume 8", 26)}
      <h2>Rimas e cantigas</h2>
      <p><b>Tradicionais brasileiras</b>, de autoria desconhecida e de domínio público, de transmissão oral; a letra varia de região para região: <i>Corre, cotia</i> e <i>Um elefante</i>.</p>
      <p><b>Escritas pela coleção</b>: <i>Cadê? Achou!</i> e <i>O barquinho de papel</i>.</p>
      <h2>Ideias</h2>
      <p>Os jogos se inspiram em Charlotte Mason (hábitos e brincadeira ao ar livre), na pedagogia Waldorf (imitação, ritmo e jogos de roda), na educação Montessori em casa (vida prática e nomear objetos reais) e nos campos de experiência da BNCC
      para a educação infantil. As orientações sobre a “crise dos dois anos” seguem a Sociedade Brasileira de Pediatria. <b>São inspirações, não regras</b>: confira com o pediatra da Marina (ADR 0021).</p>
      <h2>Ilustrações</h2>
      <p>Aquarela digital procedural da coleção ({len(MOTIVOS9)} motivos novos para este volume, e outros já usados antes). Nenhuma gravura de domínio público entra nesta versão. Tipografia: EB Garamond (licença OFL).</p>
      <h2>Privacidade</h2>
      <p>Este livro não coleta nem envia nenhum dado da criança ou da família. O diário é de papel: fica com você.</p>
      <div class="centro" style="margin-top:6mm">{tira(ICONES, "20mm", "2mm")}</div></div>""")

    L.add(f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 8</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">Esta é a primeira versão</div>
      <p style="font-size:14pt;line-height:1.6;font-style:italic">Os jogos maiores do roteiro completo (mais conjuntos para recortar,<br>bonecos de vara, cenários dobráveis e projetos para fazer em família)<br>ficam para uma edição futura.</p>
      <div style="margin-top:12mm">{tira(["bola", "ursinho", "lenco", "cortina"], "26mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 8 · Jogos e descobertas</p></div>""", cabecalho=False)


# ================================================================== MONTAGEM

def montar():
    L = Livro(8, "Jogos e descobertas")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    antes_de_brincar(L)
    bloco1(L); bloco2(L); bloco3(L); bloco4(L); diario(L)
    encerramento(L)
    num, _ = L.paginas[n_sum - 1]
    L.paginas[n_sum - 1] = (num, f'<section class="pagina"><div class="moldura"></div>{sumario(INICIO)}'
                                 f'<div class="rodape"><span class="num">{num}</span></div></section>')
    return L


def main():
    os.makedirs(SAIDA, exist_ok=True)
    ok = True
    for versao, nome in (("impressao", "volume8-impressao"), ("tela", "volume8-tela")):
        VERSAO["atual"] = versao
        INICIO.clear()
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume8-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
