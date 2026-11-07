"""
CADERNO DE ATIVIDADES DA MARINA (2 anos) — acompanha os oito volumes de O Grande Tesouro de Marina.
uso: python3 caderno.py            (monta o caderno com as unidades já escritas; ver UNIDADES_PRONTAS)
Uma unidade por volume, com várias atividades curtas. Nada de papel e caneta como centro: o caderno mistura seis tipos de atividade
(cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo e nomear). Sem tela. Ilustrações: motivos em aquarela da coleção.
Rimas e cantigas: só as tradicionais de autoria desconhecida (a letra varia de região para região) e as escritas pela coleção; ver ADR 0021.
"""
import os
import subprocess
import sys

from livro import Livro, VERSAO, adulto, gerar_pdf, img, texto, titulo
from volume6 import cena, tira   # composição de motivos em posição livre e fila de motivos: os mesmos dos outros volumes

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "caderno-2-anos")

# tipo: (nome, cor da etiqueta, motivo-ícone)
TIPOS = {
    "cantar": ("Cantar e rimar", "--d-musica", "tambor"),
    "conversar": ("Conversar", "--d-historias", "livro"),
    "mundo": ("Mostrar o mundo", "--d-natureza", "folha"),
    "maos": ("Fazer com as mãos", "--d-artes", "mao"),
    "corpo": ("Mexer o corpo", "--d-vida", "pegada"),
    "nomear": ("Nomear", "--d-ingles", "cesta"),
}

UNIDADES = [
    ("Unidade 1 · Olhar a casa e o quintal", "Volume 1 · O mundo ao meu redor", "--d-natureza"),
    ("Unidade 2 · Contar e imitar", "Volume 2 · Histórias, memória e imaginação", "--d-historias"),
    ("Unidade 3 · Muito, pouco, igual", "Volume 3 · Números, formas e raciocínio", "--d-matematica"),
    ("Unidade 4 · Som e movimento", "Volume 4 · O mundo da música", "--d-musica"),
    ("Unidade 5 · Olhar e sujar as mãos", "Volume 5 · O mundo das artes", "--d-artes"),
    ("Unidade 6 · Sair e tocar", "Volume 6 · O livro da natureza", "--d-memoria"),
    ("Unidade 7 · Uma palavra, dois jeitos", "Volume 7 · Primeiras línguas", "--d-ingles"),
    ("Unidade 8 · Brincar junto", "Volume 8 · Jogos e descobertas", "--d-jogos"),
]
INICIO = {}


class Caderno(Livro):
    def __init__(self):
        super().__init__(0, "Caderno de atividades da Marina")

    def cab(self):
        return f"Caderno de atividades · 2 anos" + (f" &nbsp;—&nbsp; {self.unidade}" if self.unidade else "")

    def html(self):
        return super().html().replace("O Grande Tesouro de Marina — Volume 0", "O Grande Tesouro de Marina — Caderno de atividades (2 anos)")


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


# ------------------------------------------------------------------ blocos

def etiqueta(tipo):
    nome, cor, _ = TIPOS[tipo]
    return (f'<span style="display:inline-block;font-size:8.6pt;text-transform:uppercase;letter-spacing:.12em;color:#fff;background:var({cor});'
            f'border-radius:1.2mm;padding:.5mm 2.4mm;vertical-align:middle">{nome}</span>')


def bloco(rotulo, corpo, cor="--musgo"):
    return (f'<div style="margin-top:3.2mm"><div style="font-family:\'EB Garamond\',serif;font-weight:600;font-size:12.5pt;color:var({cor});'
            f'border-bottom:0.4pt solid var(--linha);margin-bottom:1.2mm">{rotulo}</div>{corpo}</div>')


def passos_txt(itens, tam=12.6):
    return f'<ol style="font-size:{tam}pt;line-height:1.38;padding-left:5.5mm;margin:0">' + "".join(f"<li style='margin-bottom:.9mm'>{i}</li>" for i in itens) + "</ol>"


def falas(itens, tam=12.6):
    return (f'<div style="font-size:{tam}pt;line-height:1.4;font-style:italic;color:var(--tinta)">'
            + "".join(f'<p style="margin:0 0 1.2mm">“{i}”</p>' for i in itens) + "</div>")


def extras(variar, registro):
    """Para variar (se ela gostar ou não) e um quadro de registro do que ela disse ou fez."""
    v = bloco("Para variar", passos_txt(variar, 12.2)) if variar else ""
    return v + (f'<div style="margin-top:4mm;border:0.5pt solid var(--linha);border-radius:2mm;padding:2.5mm 3mm;height:26mm">'
                f'<div class="peq">{registro}</div></div>')


def atividade(L, t, tipo, tempo, material, cenario, fazer, dizer, perguntas, porque, atencao="", variar=(), registro="Hoje a Marina… (uma palavra nova, um gesto, o que ela mais gostou) — data: ______"):
    """Uma atividade por página: etiqueta, tempo e material, cena, o que fazer e dizer, perguntas e o porquê para o adulto."""
    nome, cor, _ = TIPOS[tipo]
    aviso = f'<br><b>Atenção:</b> {atencao}' if atencao else ""
    c = f"""<div class="miolo">
      <div class="centro" style="margin-top:1mm">{etiqueta(tipo)} <span class="peq" style="margin-left:2mm">{tempo}</span></div>
      {titulo(t, None, 26)}
      <div class="centro peq" style="margin:1mm 0 2mm"><b>Material:</b> {material}</div>
      <div style="margin:0 0 1mm">{cenario}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
        <div>{bloco("O que fazer", passos_txt(fazer))}</div>
        <div>{bloco("O que dizer", falas(dizer))}{bloco("Perguntas para a Marina", passos_txt(perguntas, 12))}</div>
      </div>{extras(variar, registro)}</div>
      {adulto("por que isto importa", porque + aviso)}"""
    return L.add(c, aba=cor)


def rima(L, t, linhas, como, origem, cenario, porque, tipo="cantar", variar=(), registro="Hoje a Marina… (qual dedo ela já sabe, que parte ela repete) — data: ______"):
    """Rima, parlenda ou cantiga: o texto grande e o gesto que a acompanha."""
    nome, cor, _ = TIPOS[tipo]
    versos = "<br>".join(linhas)
    c = f"""<div class="miolo">
      <div class="centro" style="margin-top:1mm">{etiqueta(tipo)}</div>
      {titulo(t, None, 26)}
      <div class="centro" style="margin:3mm 0">{cenario}</div>
      <p style="font-size:17pt;line-height:1.55;text-align:center;font-style:italic;margin:3mm 0">{versos}</p>
      {bloco("O gesto", passos_txt(como))}{extras(variar, registro)}
      <div class="peq" style="margin-top:3mm">{origem}</div></div>
      {adulto("por que isto importa", porque)}"""
    return L.add(c, aba=cor)


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Caderno de atividades · 2 anos</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">Para brincar,<br>conversar e olhar<br>o mundo</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:148mm;left:0;right:0">{cena([("cesta", 46, 8, 22), ("folha", 30, 60, 6), ("mao", 34, 96, 20), ("poca", 44, 126, 40), ("bota", 28, 64, 56), ("sol", 30, 140, 0)], 100)}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(["tambor", "livro", "folha", "mao", "pegada", "cesta"], "14mm", "2.5mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Caderno de atividades</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">para a Marina, aos 2 anos</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">Este caderno é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(["tambor", "livro", "folha", "mao", "pegada", "cesta"], "22mm", "2mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Aos dois anos, aprender é viver junto</h1>
      <p>Os volumes da coleção foram escritos para crianças de 3 a 8 anos. A Marina tem 2, e nessa idade o aprendizado não está no papel: está em <b>ser carregada até a janela e
      ouvir o nome das coisas</b>, em repetir a mesma rima cem vezes, em despejar água de um copo no outro, em pular numa poça. Este caderno acompanha cada volume com atividades
      para essa idade, e <b>quase nenhuma usa papel e lápis</b>.</p>
      <h2>Seis tipos de atividade</h2>
      <p>Cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo e nomear. Cada atividade tem uma etiqueta com o tipo, o tempo e o material de casa,
      o que fazer, o que dizer (falas prontas, curtas) e perguntas simples. Cada página termina com uma nota para o adulto sobre por que aquilo importa.</p>
      <h2>Quatro ideias que guiam o caderno</h2>
      <ul>
        <li><b>Curto e repetido.</b> De 3 a 10 minutos. A criança dessa idade quer a mesma coisa muitas vezes: repetir é o jeito de aprender, e não um sinal de que a atividade “acabou”.</li>
        <li><b>Você fala, ela mostra.</b> Frases curtas, devagar, e espere uns 5 segundos. Se ela responder com um gesto, um som ou meia palavra, repita o que ela quis dizer e acrescente um pouco:
        ela diz “au-au” e você responde “sim, é o cachorro! O cachorro é grande!”.</li>
        <li><b>Coisas de verdade.</b> A colher é a colher da cozinha; a folha é a folha do quintal. Nomeie com o objeto na mão.</li>
        <li><b>Sem tela.</b> A Sociedade Brasileira de Pediatria não recomenda telas antes dos 2 anos e pede, depois disso, tempo curto e acompanhado. Aqui, tudo é com gente, voz e mãos.</li>
      </ul>
      <h2>Cuidados</h2>
      <p>Nada de peça pequena que caiba na boca (engasgo). Água, mesmo rasa, só com um adulto junto o tempo todo. Se ela não quiser, pare e tente outro dia. Este caderno não é avaliação:
      se você tiver dúvidas sobre fala, audição ou desenvolvimento, converse com o pediatra.</p>
      <div class="centro" style="margin-top:5mm">""" + tira(["tambor", "livro", "folha", "mao", "pegada", "cesta"], "20mm", "2mm") + "</div>")


def como_usar(L):
    linhas = "".join(
        f'<tr><td style="width:24mm;text-align:center">{img(m, "15mm")}</td><td><b>{nome}</b><br><span style="font-size:10.2pt">{exemplo}</span></td></tr>'
        for (nome, _, m), exemplo in zip(TIPOS.values(), (
            "Parlendas, cantigas e jogos de dedos, sempre com um gesto junto.",
            "Falar do que se vê e do que se faz, com perguntas fáceis; esperar a vez dela.",
            "Passear, apresentar um bicho, uma planta, um lugar: o mundo de verdade.",
            "Água, terra, massa, tecidos, panelas: tocar, despejar, misturar.",
            "Pular, andar devagar e rápido, dançar, esconder, equilibrar.",
            "Dizer o nome de objetos reais, numa cesta ou num passeio.")))
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este caderno</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Um caderno para abrir de vez em quando</h1>
      <table class="tab">{linhas}</table>
      <h2>Ritmo</h2>
      <p>Uma ou duas atividades por dia bastam, e dias sem nenhuma também valem. O caderno tem uma unidade para cada volume da coleção: use a unidade do volume que a família estiver
      lendo, e volte às outras quando quiser. Não é preciso seguir a ordem.</p>
      <h2>Quando ela perder o interesse</h2>
      <p>Pare. Guarde para outro dia, ou mude o tipo de atividade: troque uma de mãos por uma de corpo. Se a atividade for boa, ela vai pedir de novo.</p>
      <div class="centro" style="margin-top:6mm">{tira(["folha", "gota", "mao", "tambor", "estrela"], "20mm", "2.5mm")}</div>""")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}<br><span class="peq">{vol}</span></td><td class="pg">{inicio.get(n, "")}</td></tr>'
                     for n, vol, cor in UNIDADES)
    return f"""<div class="miolo">{titulo("Sumário", "Caderno de atividades · 2 anos", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["tambor", "livro", "folha", "mao", "pegada", "cesta"], "20mm", "1.5mm")}</div></div>"""


def abertura_unidade(L, i, intro, atividades, cena_html):
    """Página de abertura de uma unidade: a ligação com o volume e a lista de atividades."""
    nome, vol, cor = UNIDADES[i]
    inicio_unidade(L, i)
    itens = "".join(f'<tr><td style="width:7mm">{etiqueta(tp)[:0]}<span class="bolinha" style="background:var({TIPOS[tp][1]})"></span></td>'
                    f'<td style="font-size:12.5pt"><b>{t}</b><br><span class="peq">{TIPOS[tp][0]} · {tempo}</span></td></tr>' for t, tp, tempo in atividades)
    c = f"""<div class="miolo">
      <div class="centro peq versal" style="letter-spacing:.2em">{vol}</div>
      {titulo(nome, None, 26)}
      <div class="centro" style="margin:4mm 0">{cena_html}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">{intro}</p>
      <table class="sumario" style="margin-top:3mm">{itens}</table></div>"""
    return L.add(c, aba=cor)


# ================================================================== U1 OLHAR A CASA E O QUINTAL (Volume 1)

def unidade1(L):
    ativ = [("A cesta de tesouros", "nomear", "5 a 8 min"), ("Passeio dos cinco sentidos", "mundo", "10 min"),
            ("O que tem na janela?", "conversar", "3 a 5 min"), ("Mindinho, seu vizinho", "cantar", "2 min, quantas vezes ela pedir"),
            ("Água na bacia", "maos", "10 min"), ("Pular a poça", "corpo", "5 min")]
    abertura_unidade(L, 0,
                     "No Volume 1 a Marina aprende a olhar a casa, o quintal, o céu e a água. Aos 2 anos, isso vira: <b>pegar, escutar, cheirar, nomear e pular</b>. "
                     "Cada atividade usa o que já existe em casa e pode ser repetida muitas vezes. Comece pela que parecer mais fácil no seu dia.",
                     ativ, cena([("colher", 30, 8, 14), ("orelha", 30, 44, 8), ("olho", 30, 80, 12), ("mao", 34, 116, 8), ("bota", 28, 154, 14)], 44, 190))

    atividade(L, "A cesta de tesouros", "nomear", "5 a 8 minutos",
              "uma cesta e 5 objetos de casa, sem peças pequenas (colher de pau, tigela, escova de cabelo, pano macio, pedra lisa maior que o punho dela)",
              cena([("cesta", 44, 8, 8), ("colher", 34, 60, 22, -18), ("tigela", 34, 100, 18), ("pedra", 28, 140, 30), ("madeira", 30, 70, 2, 14)], 54, 190),
              ["Sente no chão, de frente para ela, com a cesta entre vocês.", "Tire um objeto de cada vez e diga o nome, devagar: “co-lher”.",
               "Deixe que ela pegue, cheire, balance e bata de leve no chão.", "Peça: “cadê a tigela?”. Aceite que ela aponte ou entregue.",
               "Guardem tudo juntas, nomeando cada coisa que volta para a cesta."],
              ["Olha, uma colher! É de madeira.", "A colher é dura. Toc, toc, toc!", "A pedra é lisa e pesada. Ufa!"],
              ["O que é isto?", "É duro ou é macio?", "Onde fica a colher lá na cozinha?"],
              "Nomear um objeto real, com ele na mão, é o jeito mais direto de ampliar o vocabulário dessa idade, e a repetição fixa as palavras. É uma ideia da educação Montessori para os primeiros anos. "
              "Troque os objetos de vez em quando; deixe só os que ela mais gosta.",
              "tudo precisa ser maior que o punho dela, para não caber na boca. Fique junto o tempo todo.",
              variar=["Uma cesta por assunto: só coisas macias, só coisas que fazem barulho, só coisas da cozinha.", "Esconda um objeto num pano: “o que será?”. Ela tateia e adivinha.", "Se ela perder o interesse, guarde a cesta e traga de novo em outro dia."])

    atividade(L, "Passeio dos cinco sentidos", "mundo", "10 minutos",
              "nenhum: um quintal, uma praça, uma varanda ou até a janela",
              cena([("orelha", 36, 6, 8), ("olho", 36, 50, 8), ("nariz", 34, 94, 8), ("mao", 38, 138, 6), ("folha", 24, 80, 30, 20)], 58, 190),
              ["Chegue ao lugar e fiquem em silêncio por um minuto, de pé ou sentadas.", "“Escuta!” Aponte a orelha e espere. Depois: “Olha!”, “Cheira!”, “Toca!”.",
               "Deixe que ela toque numa folha, na terra, numa casca, num tronco.", "Nomeie o que encontrarem. Nenhuma pressa: um sentido já é um passeio.", "Na volta, lavem as mãos juntas."],
              ["Shhh… escuta! Que barulho é esse?", "Que cheiro bom! É a terra molhada.", "A folha é lisa. E o tronco é áspero."],
              ["O que você ouviu?", "Onde está o passarinho?", "Qual é mais macio: a folha ou a pedra?"],
              "Para Charlotte Mason, o trabalho da criança pequena é conhecer o mundo pelos cinco sentidos, ao ar livre. Não há o que acertar: o passeio é o objetivo. "
              "Faça no mesmo lugar várias vezes, para ela perceber o que mudou.",
              "não deixe que ela prove plantas, frutinhas nem terra. Em lugar de mato alto, calçado fechado.",
              variar=["Faça o passeio com um só sentido: hoje, só escutar; amanhã, só tocar.", "Leve uma sacolinha para guardar uma folha ou uma pedra: um tesouro para a cesta.", "Se estiver chovendo, faça da janela: ouvir a chuva, ver as gotas, sentir o vento."])

    atividade(L, "O que tem na janela?", "conversar", "3 a 5 minutos",
              "uma janela, uma varanda ou a porta aberta",
              cena([("sol", 34, 10, 10), ("nuvem", 40, 56, 14), ("arvore_verao", 34, 108, 6), ("pena", 22, 150, 24, 20)], 50, 190),
              ["Leve-a no colo, até a janela, e fiquem olhando juntas.", "Diga, bem devagar, o que você vê: “tem sol”, “vem uma nuvem”, “passou um carro”.",
               "Espere uns 5 segundos. Se ela apontar ou falar algo, repita o que ela quis dizer e acrescente uma palavra.", "Termine com um tchau: “tchau, nuvem; tchau, sol”."],
              ["Tem sol hoje. O sol está quentinho.", "Olha a nuvem! Branca e fofa.", "Você viu o passarinho? Ele voou!"],
              ["O que você está vendo?", "Cadê o sol?", "Está calor ou está frio?"],
              "Narrar o que se vê e ampliar o que a criança diz (“carro” → “o carro grande passou”) é uma das formas mais eficazes de estimular a fala. Não corrija os erros: repita certo, de passagem. "
              "Pode ser feito todo dia, no mesmo lugar, e vai ficando cada vez mais rico.",
              variar=["Faça de manhã e de noite: o que mudou no céu?", "Peça que ela “conte” para um bicho de pelúcia o que viu.", "Acene e diga tchau para quem passar na rua."])

    rima(L, "Mindinho, seu vizinho", ["Mindinho,", "seu vizinho,", "pai de todos,", "fura-bolo,", "mata-piolho!"],
         ["Segure a mãozinha dela, com a palma para cima.", "A cada verso, toque num dedo, do mindinho ao polegar.", "No fim, faça cócegas na palma. Depois deixe que ela faça em você."],
         "Rima tradicional brasileira, de autoria desconhecida; as palavras variam um pouco de região para região.",
         cena([("mao", 56, 20, 6), ("estrela", 24, 94, 12), ("mao", 56, 116, 6)], 62, 190),
         "Jogos de dedos como este juntam rima, ritmo, toque e olhar, e a Marina ouve a mesma sequência de sons vezes seguidas. É por isso que a pedagogia Waldorf os usa com crianças pequenas. "
         "Vá devagar e mantenha sempre a mesma ordem. As palavras “fura-bolo” e “mata-piolho” são nomes antigos dos dedos; ela não precisa saber o significado.",
         variar=["Faça no pé, também: “mindinho do pé…”.", "Diga mais baixo, e depois mais alto, e deixe que ela escolha.", "Pare antes do fim e espere: ela completa a palavra?"])

    atividade(L, "Água na bacia", "maos", "10 minutos",
              "uma bacia rasa, um copo plástico, uma colher, uma toalha, e coisas que boiam ou afundam (folha, tampa de pote grande, colher de pau, pedra lisa maior que o punho)",
              cena([("gota", 20, 12, 8), ("barquinho", 40, 44, 22), ("bolhas", 34, 92, 8), ("toalha", 36, 136, 18)], 50, 190),
              ["Ponha a bacia no chão, com uns 5 cm de água, sobre uma toalha.", "Deixe que ela passe a água de um copo para o outro, e que molhe tudo à vontade.",
               "Jogue uma folha: “boia!”. Jogue a pedra: “afunda!”. Depois ela mesma escolhe o que jogar.", "Enxugue as mãos e o chão juntas, dizendo “sequinho”."],
              ["Splash! A água espirrou.", "A folha boia. A pedra afunda. Glub!", "A água está fria. Brrr!"],
              ["Cadê a água?", "Boia ou afunda?", "O que mais quer pôr na água?"],
              "Despejar, mexer e ver as coisas boiarem e afundarem é ciência de verdade para quem tem 2 anos, e um dos trabalhos mais calmantes que existem. "
              "Use roupa que possa molhar, ou deixe só de fralda e avental.",
              "<b>nunca deixe a criança sozinha com água, nem por um instante</b>, mesmo rasa. Esvazie a bacia no fim.",
              variar=["Ponha uma gota de corante de comida: a água muda de cor.", "Dê uma esponja e deixe que ela torça: a água sai.", "Lave um brinquedo ou um pano junto com ela."])

    atividade(L, "Pular a poça", "corpo", "5 minutos",
              "botas (ou pés descalços), uma poça de verdade, ou um tapete azul ou uma toalha no chão fazendo de poça",
              cena([("poca", 56, 8, 22), ("bota", 36, 78, 4), ("guarda_chuva", 40, 118, 8), ("gota", 14, 164, 6), ("gota", 12, 170, 30)], 56, 190),
              ["Mostre como pular com os dois pés juntos, dobrando os joelhos.", "Conte baixinho: “um, dois… e pula!”.", "Pulem depressa, depois devagarinho, na pontinha dos pés.",
               "Troquem: agora ela diz quando pular."],
              ["Um, dois… e pula! Splash!", "Pula, pula, pula!", "Agora devagarinho, de mansinho."],
              ["A poça é grande ou pequena?", "Vamos pular rápido ou devagar?", "Quem sabe pular mais alto?"],
              "Pular junto, em pé, com comando de voz, trabalha o equilíbrio, a coordenação e as palavras que descrevem o movimento (rápido, devagar, alto, baixo). "
              "A brincadeira com poça serve também para olhar para o tempo: ontem choveu?",
              "chão firme e sem escorregar; em poça de verdade, só se a água estiver limpa e você vir o fundo.",
              variar=["Pule de um lado para o outro de uma linha de fita no chão.", "Faça o “sapo”: agachada, e pula bem baixo.", "Depois de pular, fiquem quietas e escutem a chuva (ou o silêncio)."])


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1,)


def montar(unidades=None):
    L = Caderno()
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
    for versao, nome in (("impressao", "caderno-impressao"), ("tela", "caderno-tela")):
        VERSAO["atual"] = versao
        INICIO.clear()
        L = montar()
        h = os.path.join(AQUI, f"{nome}.html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(L.html())
        ok &= gerar_pdf(h, os.path.join(SAIDA, f"{nome}.pdf"))
        print(versao, len(L.paginas), "páginas")
    if not ok:
        sys.exit(1)
    insp = os.path.join(SAIDA, "inspecao")
    os.makedirs(insp, exist_ok=True)
    for f in os.listdir(insp):
        os.remove(os.path.join(insp, f))
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "caderno-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
