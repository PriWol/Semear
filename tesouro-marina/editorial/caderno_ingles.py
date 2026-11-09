"""
CADERNO DE INGLÊS DA MARINA (2 anos) — para quem fala inglês com ela em casa; a língua materna dela é o português.
uso: python3 caderno_ingles.py            (monta o caderno com as unidades já escritas; ver UNIDADES_PRONTAS)
Métodos: entrada compreensível (Krashen e Terrell, Natural Approach), Resposta Física Total (Asher), língua por hora e lugar (Grosjean) com um falante de inglês,
leitura dialogada (Whitehurst) e rimas e cantigas de domínio público. O adulto fala inglês; o texto de apoio é em português. Sem tela. Ver ADR 0026.
As páginas e os blocos são os do caderno de atividades (caderno.py); aqui ficam só o conteúdo e a ordem.
"""
import os
import subprocess
import sys

import caderno
from caderno import (AGUA, CAL, COLECAO, DOMPUB, ICONES, TIPOS, adulto, atividade, bloco, cena, etiqueta, falas, gerar_pdf, passos_txt, rimas, texto, tira, titulo, img)
from livro import VERSAO
from caderno import Caderno

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "caderno-ingles")

UNIDADES = [
    ("Unidade 1 · Good morning", "Acordar e se arrumar", "--d-ingles"),
    ("Unidade 2 · Bath time", "O banho", "--d-frances"),
    ("Unidade 3 · Mealtime", "Comer e ajudar na mesa", "--d-vida"),
    ("Unidade 4 · Let's play", "Brincar dentro de casa", "--d-artes"),
    ("Unidade 5 · Outside", "Sair e passear", "--d-natureza"),
    ("Unidade 6 · Animals", "Os bichos", "--d-memoria"),
    ("Unidade 7 · Family and feelings", "A família e os sentimentos", "--d-historias"),
    ("Unidade 8 · Bedtime", "Hora de dormir", "--d-musica"),
]
TRAD_EN = "Rima tradicional inglesa, de autoria desconhecida e em domínio público; a letra tem pequenas variações."


class CadernoIngles(Caderno):
    def __init__(self):
        super().__init__()
        self.titulo_volume = "Caderno de inglês da Marina"

    def cab(self):
        return "Caderno de inglês · 2 anos" + (f" &nbsp;—&nbsp; {self.unidade}" if self.unidade else "")

    def html(self):
        return super().html().replace("O Grande Tesouro de Marina — Volume 0", "O Grande Tesouro de Marina — Caderno de inglês (2 anos)")


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    L.inicio[L.unidade] = L.proximo


def en(t):
    """Texto em inglês dentro de um parágrafo em português: marca o idioma para o leitor de tela e para a hifenização."""
    return f'<span lang="en">{t}</span>'


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Caderno de inglês · 2 anos</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0" lang="en">Good morning,<br>Marina!</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:148mm;left:0;right:0">{cena([("sol", 36, 8, 4), ("nuvem", 40, 56, 14), ("flor_rosa", 30, 104, 22), ("cesta", 40, 134, 8), ("estrela", 26, 20, 58), ("lua", 28, 150, 64)], 100)}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(["sol", "mao", "cesta", "bolhas", "lua"], "14mm", "3mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Caderno de inglês</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">para a Marina, aos 2 anos</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">Este caderno é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(["sol", "mao", "cesta", "bolhas", "lua"], "22mm", "3mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Carta ao adulto que fala inglês</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">O português é a língua da Marina; o inglês é o seu jeito de brincar com ela</h1>
      <p>A língua materna da Marina é o português, e vai continuar sendo a língua de quase tudo. Este caderno é para <b>você, que fala inglês com ela</b>: ele dá as frases, os gestos, as rimas e os livros
      para que o inglês entre na rotina como parte da vida, e não como aula. Não há prova, não há “falar certo” e não há pressa.</p>
      <h2>Os métodos em que o caderno se apoia</h2>
      <ul>
        <li><b>Entrada compreensível</b> (Stephen Krashen e Tracy Terrell, <i>Natural Approach</i>): a criança entende muito antes de falar. Por isso o inglês vem sempre com objeto, gesto ou situação, e <b>ninguém cobra resposta</b>.</li>
        <li><b>Resposta Física Total</b> (James Asher): comandos curtos que ela cumpre com o corpo ({en("“stand up”, “touch your nose”, “give me the spoon”")}). É o jeito mais usado de começar uma língua com crianças pequenas.</li>
        <li><b>Língua por hora e lugar</b> (François Grosjean, famílias bilíngues): momentos fixos do dia em que você fala só inglês, como o banho, o lanche e a hora de dormir, e o resto do dia em português. Quando só uma pessoa fala inglês, ela se torna a “pessoa do inglês”.</li>
        <li><b>Leitura dialogada</b> (Grover Whitehurst): ler perguntando e ampliando o que a criança diz. Cada unidade indica um livro infantil, pelo título, e como conversar sobre ele.</li>
        <li><b>Rimas e cantigas:</b> as mesmas, muitas vezes, com gesto. Só entram rimas de domínio público e as escritas pela coleção.</li>
      </ul>
      <h2>O que a pesquisa diz, e o que não diz</h2>
      <p>Os estudos de Patricia Kuhl, com bebês, mostram que uma língua nova é aprendida melhor com uma pessoa presente do que com vídeo ou áudio, e outro estudo com crianças pequenas ligou o aprendizado ao adulto que responde na hora ao que a criança faz. O que a pesquisa
      <b>não</b> mostra é quanto tempo por dia basta nessa idade, nem se “uma pessoa, uma língua” vale mais que “língua por hora e lugar”. Os números que circulam (“30% das horas acordada”) vêm de blogs, não foram confirmados e não são usados aqui.
      Este caderno também não promete fluência. Para dúvidas sobre fala ou desenvolvimento, converse com o pediatra ou com uma fonoaudióloga que acompanhe crianças bilíngues.</p>
      <div class="centro" style="margin-top:4mm">{tira(["sol", "mao", "cesta", "bolhas", "lua"], "18mm", "3mm")}</div>""")


def como_funciona(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como funciona</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Cinco regras para a “hora do inglês”</h1>
      <ol style="line-height:1.4">
        <li><b>Escolha momentos fixos.</b> Por exemplo: acordar, o banho e a hora de dormir. Neles você fala só inglês, todo dia. Fora deles, português, sem culpa.</li>
        <li><b>Frases curtas e iguais.</b> {en("“Let's wash your hands.” “Look, a bird!”")} Use as mesmas por semanas: a repetição é o que fixa.</li>
        <li><b>Mostre o que diz.</b> Aponte, pegue, faça o gesto. Uma frase com objeto na mão vale dez sem.</li>
        <li><b>Repita e amplie.</b> Ela diz “au-au”; você diz {en("“Yes! A big dog! The dog says woof-woof.”")} Não corrija: diga certo, de passagem.</li>
        <li><b>Respeite o “não”.</b> Se ela recusar o inglês, volte ao português e tente outro dia. Forçar uma língua vira só mais uma briga na fase do “não”.</li>
      </ol>
      <h2>Quando ela responde em português</h2>
      <p>É o normal, e é bom sinal: ela entendeu. Repita a ideia dela em inglês e siga em frente. {en("“Cachorro!” → “Yes, a dog! A big dog.”")} Não peça “say it in English”.</p>
      <h2>Uma unidade, dez páginas</h2>
      <p>Cada unidade tem uma rotina do dia, com quatro atividades (a maioria com o corpo e com objetos de casa), duas páginas de rimas, duas de acalmar e um livro para ler juntos.
      Escolha o que couber no dia; não é preciso fazer tudo, nem na ordem. As atividades de acalmar são para os momentos tranquilos: assim, na hora difícil, vocês já conhecem o caminho.</p>
      <h2>Sobre a pronúncia</h2>
      <p>O caderno não grava áudio. Para as palavras de que você não tiver certeza, ouça um dicionário com áudio ou uma gravação de falante nativo. A Marina aprende com o seu jeito de falar, e isso basta.</p>
      <div class="centro" style="margin-top:5mm">{tira(["mao", "pegada", "boca", "orelha"], "20mm", "5mm")}</div>""")


def frases(L):
    def lista(itens):
        return "".join(f'<tr><td style="width:62mm"><i lang="en">{a}</i></td><td style="font-size:11pt">{b}</td></tr>' for a, b in itens)
    c = f"""<div class="miolo">{titulo("Frases-chave", "para ter à mão no dia a dia", 26)}
      {bloco("Ações (Resposta Física Total)", f'<table class="tab">{lista([("Stand up. Sit down.", "levantar e sentar"), ("Come here. Give me your hand.", "venha aqui; dê a mão"), ("Touch your nose. Clap your hands.", "toque o nariz; bata palmas"), ("Jump! Stop!", "pular; parar"), ("Wash your hands.", "lavar as mãos"), ("Put it here. Take it.", "ponha aqui; pegue")])}</table>')}
      {bloco("Escolhas e “não” (para a fase do não)", f'<table class="tab">{lista([("Red cup or blue cup?", "escolha entre duas coisas que você aceita"), ("You can do it. Do you need help?", "ela quer fazer sozinha"), ("You're angry. I'm here.", "dar nome à raiva e ficar perto"), ("Let's breathe. Smell the flower, blow the candle.", "o jeito de respirar"), ("All done! Good job.", "fim de atividade, com elogio"), ("My turn. Your turn.", "revezar")])}</table>')}
      {bloco("Elogio e carinho", f'<table class="tab">{lista([("Well done! You did it!", "conseguiu!"), ("I love you.", "eu te amo"), ("Thank you. Please.", "obrigada, por favor"), ("Good job helping!", "boa ajuda")])}</table>')}</div>"""
    L.add(c, aba="--d-ingles")


def livros(L):
    c = f"""<div class="miolo">{titulo("Livros para ler juntos", "indicados pelo título; procure em biblioteca, livraria ou sebo", 26)}
      <table class="tab" style="margin-top:3mm">
        <tr><td style="width:7mm"></td><td><b lang="en">Brown Bear, Brown Bear, What Do You See?</b> — Bill Martin Jr. e Eric Carle<br><span class="peq">unidade 1: repetição, cores e bichos</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Where Is Baby's Belly Button?</b> — Karen Katz<br><span class="peq">unidade 2: partes do corpo, abas para abrir</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">The Very Hungry Caterpillar</b> — Eric Carle<br><span class="peq">unidade 3: comida, contar e dias da semana</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">From Head to Toe</b> — Eric Carle<br><span class="peq">unidade 4: gestos do corpo, no estilo da Resposta Física Total</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Rosie's Walk</b> — Pat Hutchins<br><span class="peq">unidade 5: passear e palavras de posição</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Dear Zoo</b> — Rod Campbell<br><span class="peq">unidade 6: bichos e abas para abrir</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">When Sophie Gets Angry — Really, Really Angry…</b> — Molly Bang<br><span class="peq">unidade 7: raiva e como ela passa, para ler depois que a crise passou</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Hands Are Not for Hitting</b> — Martine Agassi<br><span class="peq">unidade 7, se quiser outro: o que se pode fazer com as mãos</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Goodnight Moon</b> — Margaret Wise Brown e Clement Hurd<br><span class="peq">unidade 8: hora de dormir</span></td></tr>
        <tr><td style="width:7mm"></td><td><b lang="en">Time for Bed</b> — Mem Fox e Jane Dyer<br><span class="peq">unidade 8, se quiser outro: rima e repetição para dormir</span></td></tr>
      </table></div>
      {adulto("como ler", "O caderno não reproduz nenhum desses livros, só os indica pelo título e diz como conversar sobre cada um. Leia com ela no colo, devagar, apontando; deixe que ela vire a página. Se ela quiser ler o mesmo livro cem vezes, melhor: faça perguntas diferentes a cada vez. Os livros são de autores contemporâneos e estão sob direitos autorais: compre ou tome emprestado.")}"""
    L.add(c, aba="--d-historias")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt"><i lang="en">{n.split(" · ", 1)[1]}</i><br><span class="peq">{sub}</span></td><td class="pg">{inicio.get(n, "")}</td></tr>'
                     for n, sub, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento<br><span class="peq">Registro, fontes e créditos</span></td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Caderno de inglês · 2 anos", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["sol", "mao", "cesta", "bolhas", "lua"], "18mm", "2mm")}</div></div>"""


def abertura_unidade(L, i, intro, atividades, cena_html):
    nome, sub, cor = UNIDADES[i]
    inicio_unidade(L, i)
    itens = "".join(f'<tr><td style="width:7mm"><span class="bolinha" style="background:var({TIPOS[tp][1]})"></span></td>'
                    f'<td style="font-size:12.2pt"><b lang="en">{t}</b><br><span class="peq">{TIPOS[tp][0]} · {tempo}</span></td></tr>' for t, tp, tempo in atividades)
    c = f"""<div class="miolo">
      <div class="centro peq versal" style="letter-spacing:.2em">{sub}</div>
      {titulo(nome.replace("Unidade ", "Unidade "), None, 26)}
      <div class="centro" style="margin:3mm 0">{cena_html}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">{intro}</p>
      <table class="sumario" style="margin-top:2mm">{itens}</table></div>"""
    return L.add(c, aba=cor)


def leitura(L, titulo_livro, autores, tempo, cenario, fazer, dizer, perguntas, porque, variar=()):
    """Página de leitura dialogada: o livro, indicado pelo título, e como conversar sobre ele (Whitehurst, adaptado a 2 anos)."""
    return atividade(L, f"Ler juntos: {titulo_livro}", "ler", tempo, f"o livro <i lang=\"en\">{titulo_livro}</i> ({autores}), de uma biblioteca, livraria ou sebo",
                     cenario, fazer, dizer, perguntas, porque, variar=variar,
                     registro="Hoje a Marina… (apontou, repetiu uma palavra, pediu o livro de novo) — data: ______")


# ================================================================== U1 GOOD MORNING

def unidade1(L):
    ativ = [("Good morning, sunshine", "conversar", "3 min"), ("Stretch and wake up", "corpo", "5 min"), ("Get dressed", "maos", "10 min"), ("What's the weather?", "mundo", "3 a 5 min"),
            ("Good morning to you · Open, shut them · Sun is up · This little piggy", "cantar", "2 min cada"),
            ("Smell the flower, blow the candle", "acalmar", "2 a 3 min"), ("Cat stretch", "acalmar", "3 min"), ("Brown Bear, Brown Bear, What Do You See?", "ler", "5 a 10 min")]
    abertura_unidade(L, 0,
                     "A rotina da manhã é o primeiro momento fixo de inglês: as mesmas frases, todos os dias, com a luz, a roupa e o tempo lá fora. Comece por <b>uma</b> atividade e repita até virar hábito. "
                     "As de acalmar são para quando ela está tranquila, para já conhecerem o caminho quando o dia ficar difícil.",
                     ativ, cena([("sol", 30, 8, 10), ("janela_sol", 30, 44, 12), ("luva", 26, 80, 18), ("gorro", 26, 112, 16), ("nuvem", 34, 148, 10)], 44, 190))

    atividade(L, "Good morning, sunshine", "conversar", "3 minutos",
              "nenhum; a cortina ou a janela do quarto",
              cena([("sol", 34, 12, 8), ("janela_sol", 32, 56, 12), ("carinha_feliz", 28, 100, 14), ("cama", 34, 140, 10)], 46, 190),
              ["Entre no quarto devagar, com a voz baixa, e diga bom dia em inglês, no mesmo tom todos os dias.", "Abra a cortina com ela: “let's open the curtains”. Deixe que ela ajude.", "Diga o que vê lá fora: sol, nuvem, passarinho.",
               "Pergunte, e espere uns 5 segundos. Se ela responder em português, repita em inglês."],
              ["Good morning, Marina! Good morning, sun!", "Time to wake up. Let's open the curtains.", "Look, the sun is up! It's a bright day."],
              ["Are you awake?", "Do you see the sun?", "What do you see?"],
              "Um ritual de acordar, sempre igual e na mesma língua, é o que a abordagem de “língua por hora e lugar” pede: o inglês ganha um momento só dele, e ela aprende a esperar essas frases. "
              "A voz baixa e calma da manhã também ajuda numa criança que acorda de mau humor.",
              variar=["Diga bom dia ao sol, ao gato, à planta, ao ursinho.", "Cante “good morning” (a rima das páginas seguintes) ao abrir a cortina.", "Deixe que ela escolha: “curtain or window?”."])

    atividade(L, "Stretch and wake up", "corpo", "5 minutos",
              "um espaço livre ao lado da cama",
              cena([("mao", 34, 12, 10), ("pegada", 18, 58, 6), ("pe", 28, 82, 20), ("estrela", 24, 124, 14), ("coracao", 26, 156, 18)], 46, 190),
              ["Mostre cada movimento e diga a frase ao mesmo tempo: “stretch up high” (braços para cima).", "Depois: “touch your toes”, “shake your hands”, “jump!”.", "Deixe que ela faça com você; não corrija os movimentos, só mostre de novo.",
               "Termine com “stop” e uma respiração: “big breath in… and out”."],
              ["Stretch up high! Reach for the sky!", "Touch your toes. Shake, shake, shake your hands.", "Jump! One, two, three. And stop."],
              ["Can you jump?", "Can you touch your toes?", "Where are your hands?"],
              "Esta é a Resposta Física Total de James Asher: a criança mostra que entendeu com o corpo, sem precisar falar. Comandos curtos e visíveis, os mesmos todo dia, são o melhor jeito de começar uma língua com quem tem 2 anos. "
              "“Jump” e “stop” treinam também o controle do impulso: pular, e parar quando o adulto diz.",
              atencao="chão firme e sem escorregar.",
              variar=["Faça de bicho: stretch like a cat, jump like a frog.", "Ela dá os comandos e você faz.", "“Slow motion”: faça tudo muito devagar."])

    atividade(L, "Get dressed", "maos", "10 minutos",
              "as roupas do dia, dispostas na cama: meias, camiseta, calça, sapato",
              cena([("luva", 28, 12, 14), ("gorro", 28, 48, 14), ("casaco", 30, 84, 10), ("sandalia", 26, 122, 18), ("bota", 28, 156, 14)], 46, 190),
              ["Mostre duas meias de cores diferentes e deixe que ela escolha: “red socks or blue socks?”.", "Diga o nome de cada peça ao vesti-la: “put on your socks”.", "Deixe que ela faça o que consegue (puxar a meia, enfiar o braço) e ajude no resto.",
               "No fim, olhe no espelho: “all dressed!”."],
              ["Red socks or blue socks? You choose.", "One sock, two socks! Put on your shoes.", "All dressed! You look great."],
              ["Which one?", "Where's your sock?", "Can you put it on?"],
              "Escolher entre duas coisas que você aceita dá à criança um pouco de controle, e na fase do “não” isso evita muitas brigas. Vestir-se é também uma tarefa de vida prática (ideia da educação Montessori) e um bom contexto para nomear peças de roupa com o objeto na mão. "
              "Se ela recusar, mude a escolha, não a regra.",
              variar=["Uma peça por dia em inglês: hoje, só “socks”.", "Escolha de cores: “which color today?”.", "Vista o ursinho antes."])

    atividade(L, "What's the weather?", "mundo", "3 a 5 minutos",
              "uma janela ou a porta aberta",
              cena([("sol", 32, 10, 8), ("nuvem", 38, 52, 14), ("nuvem_chuva", 36, 98, 10), ("guarda_chuva", 32, 140, 16)], 46, 190),
              ["Vão juntas à janela e olhem o céu. Diga a palavra do dia em inglês e faça o gesto: sol (mãos abertas), nuvem (mão arredondada), chuva (dedos caindo).", "Deixe que ela “faça o tempo” com as mãos.",
               "Decidam juntas o que vestir: “it's sunny, let's wear a hat”.", "Repita todo dia: o tempo muda, e as palavras também."],
              ["It's sunny! Look, the sun.", "It's cloudy. Do you see the clouds?", "It's rainy. We need an umbrella."],
              ["Is it sunny or cloudy?", "Is it hot or cold?", "What do we need?"],
              "Falar do tempo é um assunto que muda todos os dias e é visível pela janela, ideal para aprender palavras de verdade. O gesto ajuda a fixar (Resposta Física Total) e a decisão (“vamos de casaco?”) dá sentido à frase.",
              variar=["Faça o tempo com o corpo: chuva (dedos), vento (braços), sol (abrir os braços).", "Desenhe o tempo de hoje no vidro embaçado.", "À noite: “is it dark? Where's the moon?”."])

    rimas(L, "Para acordar", [
        dict(t="Good morning to you", linhas=["Good morning to you,", "good morning to you,", "we're all in our places", "with bright shining faces,", "good morning to you."],
             gesto="toque a mão dela, o nariz e as bochechas em “bright shining faces”; abra os braços no “good morning to you”. Cante baixinho, na mesma melodia que você conhece.",
             origem="“Good Morning to All”, de Patty Smith Hill e Mildred J. Hill (1893), em domínio público.", motivos=["sol", "carinha_feliz"]),
        dict(t="Open, shut them", linhas=["Open, shut them, open, shut them,", "give a little clap.", "Open, shut them, open, shut them,", "lay them in your lap.", "Creep them, creep them, creep them, creep them,", "right up to your chin;", "open wide your little mouth,", "but do not let them in."],
             gesto="abra e feche as mãos, bata uma palma e pouse no colo; depois “ande” com os dedos até o queixo e abra a boca. Ela vai querer o “de novo”.", origem=TRAD_EN, motivos=["mao", "boca"])],
        "Rimas de dedos e de mãos, como estas, são o melhor material de inglês aos 2 anos: curtas, repetidas, com gesto, e a criança entende pelo corpo. Cante as mesmas por semanas.")

    rimas(L, "Para se mexer", [
        dict(t="Sun is up", linhas=["Sun is up, sun is up,", "time to wake, time to wake,", "stretch up high, touch your toes,", "good morning, Marina, off we go!"],
             gesto="faça o gesto do sol com os braços, estique alto, toque os pés e saia andando. Troque “Marina” pelo nome do bichinho se quiser.", origem=COLECAO, motivos=["sol", "pe"]),
        dict(t="This little piggy", linhas=["This little piggy went to market,", "this little piggy stayed at home,", "this little piggy had roast beef,", "this little piggy had none,", "and this little piggy cried “wee, wee, wee”", "all the way home."],
             gesto="toque um dedo do pé de cada vez, do dedão ao mindinho; no “wee, wee, wee” suba as cócegas pela perna. É uma rima antiga, muito usada para trocar de roupa.", origem=TRAD_EN, motivos=["pe", "estrela"])],
        "Rimas para o corpo transformam a rotina de se vestir em brincadeira. Quando ela estiver com pressa ou com “não”, dê a ela uma escolha (“sun is up” ou “this little piggy”?) em vez de uma ordem.")

    atividade(L, "Smell the flower, blow the candle", "acalmar", "2 a 3 minutos",
              "nenhum (uma flor de verdade ou desenhada ajuda); a vela é só de faz de conta: o dedo erguido",
              cena([("flor_rosa", 34, 12, 8), ("vela", 22, 60, 20), ("nariz", 26, 96, 14), ("boca", 30, 134, 12)], 46, 190),
              ["Sentem de frente, com você mais perto que de costume.", "“Smell the flower”: inspire devagar pelo nariz, de olhos fechados. “Blow the candle”: sopre pela boca, bem comprido, com o dedo dela de vela.",
               "Faça junto, no mesmo ritmo, três vezes.", "Termine com um abraço: “well done, breather!”."],
              ["Smell the flower… mmm, it smells so good.", "Now blow the candle… whoooo. Nice and slow.", "One more time. Slow and gentle."],
              ["What does the flower smell like?", "Did the candle go out?", "How does your body feel?"],
              "Soprar devagar é o jeito mais simples de baixar o ritmo do corpo. Faça com ela calma, no momento fixo de inglês: assim, quando a raiva vier, bastará dizer “let's smell the flower” e ela já conhecerá o caminho. Não force: se ela recusar, respire você e deixe que ela olhe.",
              variar=["Sopre uma pena ou um cata-vento.", "“Smell the soup, blow the soup”, na hora de comer.", "Dragão: sopro forte; gatinho: sopro fraquinho."], registro=CAL)

    atividade(L, "Cat stretch", "acalmar", "3 minutos",
              "um tapete macio, no chão",
              cena([("gato", 34, 14, 10), ("estrela", 22, 60, 18), ("lua", 26, 94, 14), ("coracao", 26, 134, 16)], 46, 190),
              ["Fique de quatro, como um gato, e mostre: “cat stretch”: peito para baixo e bumbum para cima, bem devagar.", "Depois “round back”: arredonde as costas, como gato bravo, e solte.",
               "Façam três vezes, bem devagar, respirando.", "Termine sentadas, com a mão no peito: “purr, purr”."],
              ["Stretch like a cat. Nice and slow.", "Round your back. Now relax.", "Purr, purr, purr. What a calm kitty."],
              ["Are you a cat?", "Can you purr?", "Is your body slow now?"],
              "Alongar devagar, como um bichinho, é um movimento que acalma depois de uma noite ou de uma crise, e é uma das posturas mais simples das brincadeiras de yoga para crianças pequenas. O ronronar (um som baixo e contínuo) ajuda a soltar a respiração.",
              variar=["Seja outro bicho: um cachorro que sacode, uma lesma bem lenta.", "Com música baixa.", "Antes de dormir, com a luz baixa."], registro=CAL)

    leitura(L, "Brown Bear, Brown Bear, What Do You See?", "Bill Martin Jr. e Eric Carle", "5 a 10 minutos",
            cena([("leao", 30, 12, 12), ("pena", 22, 52, 22), ("peixe", 30, 82, 16), ("gato", 28, 118, 14), ("cachorro", 30, 152, 12)], 46, 190),
            ["Sentem juntas, com ela no colo, e deixe que ela segure o livro.", "Mostre a capa e diga o título. Vire a página e aponte o bicho.", "Faça a pergunta do livro e espere: ela completa, aponta ou imita o bicho?",
             "Repita o livro quantas vezes ela pedir; a cada vez, faça uma pergunta diferente."],
            ["Look! A bear. What color is the bear?", "What does the bear see?", "Can you roar? Roar like a lion!"],
            ["What do you see?", "Where is the bird?", "Can you point to the fish?"],
            "É leitura dialogada (Grover Whitehurst): em vez de só ler, você pergunta e acrescenta. Para 2 anos, as perguntas mais úteis são as de completar (ela diz a palavra que falta), as abertas (“what do you see?”) e as de “o quê / onde”. "
            "O livro de Bill Martin Jr. e Eric Carle repete a mesma pergunta em cada página, o que ajuda a criança a entender e a falar antes de saber ler.",
            variar=["Imite o som de cada bicho.", "Procure no quarto os bichos e as cores do livro.", "Leia em português uma vez, para ela entender a história, e depois em inglês."])


# ================================================================== U2 BATH TIME

def unidade2(L):
    ativ = [("Bath time!", "conversar", "10 a 15 min"), ("Wash, wash, wash", "corpo", "5 min"), ("Pour and fill", "maos", "10 min"), ("Towel time", "mundo", "5 min"),
            ("Rub-a-dub-dub · Splash, splash, splash · Row, row, row your boat · Here we go round the mulberry bush", "cantar", "2 min cada"),
            ("Bubble breathing", "acalmar", "3 min"), ("Towel hug", "acalmar", "3 min"), ("Where Is Baby's Belly Button?", "ler", "5 a 10 min")]
    abertura_unidade(L, 1,
                     "O banho é o segundo momento fixo de inglês: tem objetos de verdade (água, sabonete, toalha), gestos e uma sequência que se repete todo dia. É também um bom lugar para a fase do “não”, "
                     "com escolhas pequenas (“bubbles or no bubbles?”). <b>Nenhuma atividade desta unidade dispensa o adulto dentro do banheiro, o tempo todo.</b>",
                     ativ, cena([("bolhas", 30, 8, 14), ("sabonete", 28, 44, 18), ("gota", 24, 80, 12), ("toalha", 30, 112, 14), ("patinho", 28, 150, 14)], 44, 190))

    atividade(L, "Bath time!", "conversar", "10 a 15 minutos",
              "a banheira ou a bacia, sabonete, toalha, copos de plástico e um brinquedo que boie",
              cena([("barquinho", 34, 12, 14), ("bolhas", 32, 54, 10), ("sabonete", 26, 94, 22), ("toalha", 32, 132, 12)], 46, 190),
              ["Prepare tudo antes de a chamar, e teste a água no seu pulso: morna, nunca quente.", "Diga sempre as mesmas frases na mesma ordem: “bath time”, “take off your clothes”, “in you go”.",
               "Dê uma escolha: “bubbles or no bubbles?”, “duck or boat?”.", "Narre o que faz: “water, soap, bubbles”. Termine com “all done, let's get out”."],
              ["It's bath time! Let's go to the bathroom.", "In you go. The water is warm. Splash!", "Bubbles or no bubbles? You choose."],
              ["Is the water warm?", "Where is the duck?", "Do you want the soap?"],
              "Um momento do dia que se repete, com as mesmas palavras, é o melhor lugar para o inglês de “língua por hora e lugar” (Grosjean): o banho já tem a sua sequência, e a criança entende as palavras pelos objetos. "
              "Escolher entre duas coisas ajuda na fase do “não”.",
              atencao=AGUA + " Teste a temperatura no pulso, esvazie a banheira ao terminar e nunca saia do banheiro, nem para atender o telefone.",
              variar=["Um só objeto novo por dia: hoje, “soap”.", "Cante a rima da unidade ao encher a banheira.", "Deixe que ela escolha a ordem: “wash your face or your feet first?”."])

    atividade(L, "Wash, wash, wash", "corpo", "5 minutos",
              "o banho, ou um boneco e uma bacia (só com você junto)",
              cena([("mao", 34, 12, 12), ("pe", 28, 52, 14), ("nariz", 28, 88, 14), ("sabonete", 26, 124, 18), ("gota", 22, 160, 22)], 46, 190),
              ["Mostre cada parte do corpo, diga o nome e lave-a devagar com ela: “wash your hands”.", "Depois peça: “wash your feet”, “wash your tummy”. Ela mostra com a mão, ou lava.",
               "Deixe que ela lave o boneco: “wash the baby”.", "No fim, “rinse” (enxaguar) e “all clean”."],
              ["Wash your hands. Rub, rub, rub.", "Wash your feet. One foot, two feet.", "Rinse, rinse, rinse. All clean!"],
              ["Where are your hands?", "Can you wash your tummy?", "Is the baby clean?"],
              "É a Resposta Física Total de James Asher: a criança mostra que entendeu com o corpo, e o banho já traz o objeto e o gesto de cada palavra. Comandos curtos, os mesmos todo dia. "
              "Deixar que ela lave o boneco dá a ela o papel de quem cuida, que muita criança dessa idade adora.",
              atencao=AGUA,
              variar=["Lave o ursinho no banho, com pouca água.", "“Wash, wash, wash” cantando a rima da unidade.", "Ela diz qual parte lavar agora."])

    atividade(L, "Pour and fill", "maos", "10 minutos",
              "copos e potes de plástico de tamanhos diferentes, uma colher grande, na banheira ou numa bacia rasa",
              cena([("jarra", 32, 12, 12), ("tigela", 30, 52, 16), ("xicara", 26, 90, 20), ("gota", 22, 124, 18), ("peixe", 30, 156, 14)], 48, 190),
              ["Deixe que ela encha um copo e despeje em outro: “fill it up”, “pour it out”.", "Compare: “big cup, small cup”; “full”, “empty”.", "Jogue um brinquedo: “it floats!”; uma colher: “it sinks!”.",
               "Termine esvaziando a bacia juntos: “all gone”."],
              ["Fill it up. Pour, pour, pour.", "It's full! Now it's empty.", "Splash! The cup is empty."],
              ["Is it full or empty?", "Big cup or small cup?", "Does it float or sink?"],
              "Encher e despejar é ciência de verdade para quem tem 2 anos, e as palavras (full, empty, big, small, float, sink) vêm com o objeto na mão, que é o modo mais seguro de aprender uma palavra. "
              "A atividade também acalma: o movimento repetido de despejar tem ritmo.",
              atencao=AGUA + " Use só recipientes de plástico inquebrável, maiores que a boca dela.",
              variar=["Corante de comida: “blue water”, “yellow water”.", "Um peneira: “it goes through!”.", "Lave o brinquedo de cada banho: “wash the duck”."])

    atividade(L, "Towel time", "mundo", "5 minutos",
              "uma toalha macia e quente (pode ser aquecida na secadora, e testada na sua mão)",
              cena([("toalha", 36, 12, 10), ("coracao", 26, 56, 18), ("pe", 26, 90, 16), ("mao", 30, 124, 12), ("carinha_feliz", 26, 160, 18)], 46, 190),
              ["Enrole-a na toalha assim que sair da água: “up you come”.", "Seque uma parte de cada vez e diga o nome: “dry your head”, “dry your arms”, “dry your toes”.",
               "Faça um “pacote” de toalha e dê um abraço: “snug as a bug”.", "Vista a roupa dizendo cada peça: “shirt on”, “socks on”."],
              ["Up you come! Here's your towel.", "Dry your head. Dry your arms. Dry your toes.", "All dry! Pajamas on."],
              ["Where are your toes?", "Is the towel soft?", "Are you all dry?"],
              "A saída do banho costuma ser o momento mais difícil: ela não quer sair, e é aí que a rotina ajuda. As mesmas palavras, na mesma ordem, e o gesto de secar cada parte dão previsibilidade, e um abraço de toalha ajuda a voltar à calma. "
              "Se ela quiser ficar mais, avise: “two more splashes, and then we get out”.",
              atencao=AGUA + " Segure-a com firmeza ao tirá-la do banho, que fica escorregadio.",
              variar=["“Where's [Marina]?” com a toalha na cabeça, e “there you are!”.", "Seque o ursinho também.", "Cante “this is the way we dry our toes”."])

    rimas(L, "Para o banho", [
        dict(t="Rub-a-dub-dub", linhas=["Rub-a-dub-dub,", "three men in a tub,", "and who do you think they be?", "The butcher, the baker,", "the candlestick-maker,", "they all sailed out to sea."],
             gesto="esfregue as mãos dela e as suas no ritmo de “rub-a-dub-dub”, bata palmas no “tub” e faça as mãos de barquinho no “sailed out to sea”. Cante-a no banho.", origem=TRAD_EN, motivos=["barquinho", "bolhas"]),
        dict(t="Splash, splash, splash", linhas=["Splash, splash, splash,", "bubbles in the bath;", "wash my hands, wash my toes,", "wash my little nose!"],
             gesto="bata a água de leve no “splash”, e toque cada parte do corpo quando a rima nomear: mãos, dedos dos pés, nariz.", origem=COLECAO, motivos=["gota", "sabonete"])],
        "A rima do banho marca o ritmo do banho, e a criança passa a antecipar as palavras. Cante as mesmas por semanas; a rima própria da coleção tem só palavras de objetos do banho.")

    rimas(L, "Mais para o banho", [
        dict(t="Row, row, row your boat", linhas=["Row, row, row your boat,", "gently down the stream.", "Merrily, merrily, merrily, merrily,", "life is but a dream."],
             gesto="sentados, balancem para a frente e para trás, como quem rema. Faz o banho virar uma pausa tranquila.", origem="Cantiga de domínio público (letra publicada em 1852).", motivos=["barquinho", "m_riacho"]),
        dict(t="Here we go round the mulberry bush", linhas=["Here we go round the mulberry bush,", "the mulberry bush, the mulberry bush;", "here we go round the mulberry bush", "on a cold and frosty morning.", "This is the way we wash our hands,", "wash our hands, wash our hands;", "this is the way we wash our hands", "on a cold and frosty morning."],
             gesto="gire de mãos dadas na primeira estrofe e, na segunda, mime lavar as mãos. Depois troque o verbo: “dry our toes”, “brush our teeth”. É uma rima feita para as rotinas.", origem=TRAD_EN, motivos=["mao", "estrela"])],
        "“Here we go round the mulberry bush” é uma rima que aceita qualquer verbo, e por isso serve de rotina do dia inteiro: lavar, vestir, comer. Repetida, vira a “música do banho”.")

    atividade(L, "Bubble breathing", "acalmar", "3 minutos",
              "bolhas de sabão na banheira ou espuma na palma da mão",
              cena([("bolhas", 40, 12, 10), ("boca", 28, 58, 20), ("nariz", 24, 92, 18), ("gota", 24, 124, 14)], 46, 190),
              ["Ponha um pouco de espuma na palma da mão dela, ou sopre uma bolha com a varinha.", "Mostre: “breathe in… and blow”. Sopre devagar e olhe a bolha ir.", "Deixe que ela sopre a espuma: “blow the bubbles away”.",
               "Termine com um abraço: “nice and slow”."],
              ["Breathe in… and blow, blow, blow.", "Look, a big bubble! Nice and slow.", "Pop! One more time?"],
              ["Can you blow?", "Where did the bubble go?", "Is your body slow now?"],
              "Soprar devagar ajuda o corpo a baixar o ritmo, e a espuma dá um motivo concreto para o sopro. O banho calmo, com voz baixa, também ajuda a criança que está agitada ou brava.",
              atencao=AGUA + " A espuma e o líquido de bolhas não são para beber e podem irritar os olhos.",
              variar=["Sopre um barquinho de papel na água.", "“Blow the duck” de um lado ao outro da banheira.", "Faça a “barba” de espuma: “ho, ho, ho”."], registro=CAL)

    atividade(L, "Towel hug", "acalmar", "3 minutos",
              "uma toalha grande e quentinha",
              cena([("toalha", 40, 12, 10), ("coracao", 28, 60, 16), ("maos_juntas", 30, 98, 14), ("lua", 24, 136, 16)], 46, 190),
              ["Enrole-a bem, da cabeça aos pés, deixando o rosto livre, e sente com ela no colo.", "Balance devagar e diga: “snug as a bug in a rug”.", "Aperte com firmeza, mas com delicadeza: “squeeze, squeeze”.",
               "Solte aos poucos: “and… relax”."],
              ["Snug as a bug in a rug.", "Squeeze, squeeze. A big hug.", "And relax. All better."],
              ["Are you warm?", "Do you want another squeeze?", "Is your body calm?"],
              "O abraço firme e lento, embrulhada numa toalha, é um modo conhecido de acalmar crianças pequenas, e dá uma sensação de proteção depois de um banho agitado ou de uma crise. Ela deve poder sair quando quiser. "
              "A frase “snug as a bug in a rug” é uma expressão inglesa famosa e fácil de repetir.",
              atencao="deixe sempre o rosto livre e nunca cubra a cabeça; solte se ela se agitar. Esvazie a banheira antes de sentar com ela. " + AGUA,
              variar=["Faça com a manta no quarto.", "Embrulhe o ursinho também.", "Cante baixinho enquanto balança."], registro=CAL)

    leitura(L, "Where Is Baby's Belly Button?", "Karen Katz", "5 a 10 minutos",
            cena([("mao", 30, 12, 14), ("pe", 28, 50, 16), ("nariz", 26, 86, 16), ("orelha", 28, 118, 14), ("boca", 30, 152, 16)], 46, 190),
            ["Sentem juntas, com o livro no colo, e deixe que ela abra as abas.", "Faça a pergunta do título e espere: ela procura a página, aponta ou levanta a aba?", "Ao achar, comemore e aponte a parte do corpo dela: “here's your tummy!”.",
             "Repita no banho: “where are your toes?”."],
            ["Where is the belly button? Let's look.", "Lift the flap. There it is!", "Where is your tummy? Show me."],
            ["Where are your hands?", "Can you find your nose?", "What's under the flap?"],
            "É leitura dialogada (Whitehurst): a pergunta do livro é de completar e de “onde”, as mais fáceis para 2 anos, e as abas dão a ela uma tarefa de procurar. O livro de Karen Katz repete o jogo de achar, que a criança adora. "
            "Ligar o livro ao banho (“where are your toes?”) faz o inglês sair do livro e entrar na vida.",
            variar=["Procure as partes do corpo no ursinho.", "Esconda o rosto atrás de um pano: “where is [name]? Peekaboo!”.", "Ler uma só página por dia, se ela se cansar."])


# ================================================================== U3 MEALTIME

ENGASGO = "Na hora de comer, <b>fique junto e com ela sentada</b>; corte as frutas em pedaços pequenos e macios e evite uvas inteiras, nozes, pipoca e balas duras, que podem causar engasgo. Cheque alergias."


def unidade3(L):
    ativ = [("Wash your hands, let's eat", "conversar", "5 min"), ("Set the table", "maos", "10 min"), ("Apple or banana?", "nomear", "10 min"), ("Yum or yuck?", "mundo", "10 min"),
            ("Pease porridge hot · Hot cross buns · Yum, yum, yum · Wash your hands", "cantar", "2 min cada"),
            ("Smell the soup, blow the soup", "acalmar", "3 min"), ("Slow bites", "acalmar", "5 min"), ("The Very Hungry Caterpillar", "ler", "5 a 10 min")]
    abertura_unidade(L, 2,
                     "A refeição é o terceiro momento fixo de inglês: tem objetos de verdade (prato, copo, colher), gestos e a vez de cada um. É também uma fonte de “não”, e por isso as escolhas entre duas coisas valem aqui. "
                     "<b>Em todas as atividades de comida, a criança come sentada e com você junto.</b>",
                     ativ, cena([("prato", 30, 8, 14), ("colher", 28, 44, 16), ("xicara", 26, 80, 20), ("maca", 26, 114, 14), ("pao", 28, 150, 14)], 44, 190))

    atividade(L, "Wash your hands, let's eat", "conversar", "5 minutos",
              "uma pia ou bacia, sabonete e a mesa posta",
              cena([("sabonete", 28, 12, 14), ("mao", 32, 48, 12), ("toalha", 30, 86, 14), ("prato", 32, 124, 16)], 46, 190),
              ["Avise com antecedência: “five more minutes, then it's lunchtime”.", "Lavem as mãos juntos: “water, soap, rub, rub, rinse, dry”.", "Sentem à mesa e diga: “let's eat!”.",
               "Ao acabar: “all done?”, “wipe your hands”."],
              ["It's lunchtime! Let's wash our hands.", "Rub, rub, rub. Rinse. Dry.", "Sit down. Let's eat."],
              ["Are you hungry?", "Are your hands clean?", "Where is your spoon?"],
              "A mesma sequência de palavras, todos os dias, no mesmo momento, é o que a abordagem de língua por hora e lugar pede, e o aviso de antecedência reduz as brigas na troca de atividade, que é um ponto difícil na fase do “não”. "
              "Lavar as mãos juntos é também uma tarefa de vida prática (Montessori).",
              atencao=AGUA + " " + ENGASGO,
              variar=["Cante “wash your hands” (rima desta unidade) na pia.", "Ela escolhe: “this towel or that towel?”.", "Lave as mãos do ursinho."])

    atividade(L, "Set the table", "maos", "10 minutos",
              "um prato, um copo e uma colher de plástico ou de inox, e um guardanapo de tecido; tudo inquebrável",
              cena([("prato", 34, 12, 12), ("xicara", 28, 52, 16), ("colher", 28, 88, 18), ("mesa", 32, 124, 12), ("cadeira", 26, 160, 16)], 48, 190),
              ["Mostre cada objeto e diga o nome: “plate”, “cup”, “spoon”, “napkin”.", "Peça que ela leve um de cada vez à mesa: “bring me the spoon”, “put it here”.", "Conte os lugares: “one plate for Mama, one plate for you”.",
               "Ao terminar, agradeçam: “thank you for helping”."],
              ["This is a plate. Can you put it here?", "Spoon, cup, napkin. Thank you!", "One plate, two plates. We're ready."],
              ["Where does the spoon go?", "Can you bring me the cup?", "How many plates?"],
              "Pôr a mesa é uma tarefa de verdade, dada à criança como ajuda (Montessori), que muita criança na fase do “não” aceita com orgulho. As palavras (plate, cup, spoon) vêm com o objeto na mão, e os comandos simples (“bring me”, “put it here”) são Resposta Física Total.",
              atencao=ENGASGO + " Só objetos inquebráveis e sem pontas.",
              variar=["Ela põe a mesa do ursinho.", "Quem leva o prato é “the helper of the day”.", "Troque de objeto: “fork”, “bowl”."])

    atividade(L, "Apple or banana?", "nomear", "10 minutos",
              "duas frutas cortadas e servidas em pedaços pequenos e macios, num prato",
              cena([("maca", 32, 12, 14), ("banana", 30, 50, 16), ("pera", 28, 86, 18), ("laranja", 28, 120, 16), ("morango", 26, 156, 18)], 48, 190),
              ["Mostre uma fruta inteira e depois o pedaço: “apple”, “a slice of apple”.", "Ofereça a escolha: “apple or banana?”. Aceite o apontar.", "Nomeie o sabor e a textura: “sweet”, “soft”, “crunchy”.",
               "Pergunte se quer mais: “more?”, “all done?”."],
              ["Apple or banana? You choose.", "Mmm, sweet! It's so soft.", "More, or all done?"],
              ["Which one do you want?", "Is it sweet?", "More or all done?"],
              "Escolher entre duas coisas é o que dá algum controle à criança, e as palavras de fruta aprendidas com a fruta na mão ficam. Ela pode dizer “não” a uma delas, e tudo bem: dê tempo e ofereça de novo depois, sem forçar.",
              atencao=ENGASGO,
              variar=["Procure a fruta nos livros: “where is the apple?”.", "Corte uma fruta e mostre as sementes.", "Duas frutas, e peça que ela “dê” uma ao ursinho."])

    atividade(L, "Yum or yuck?", "mundo", "10 minutos",
              "alimentos que ela já conhece, em pedaços pequenos e macios (pão, queijo, banana), no prato",
              cena([("pao", 30, 12, 16), ("queijo", 28, 48, 18), ("copo_leite", 28, 82, 16), ("mel", 26, 116, 18), ("ovo", 26, 150, 18)], 48, 190),
              ["Faça cara de “yum” (esfregue a barriga) ao provar, e deixe que ela imite.", "Faça a cara de “yuck” também, brincando: “I don't like it, no, thank you”. Mostre que é permitido dizer não com educação.",
               "Dê o nome do gosto: “sweet”, “salty”, “hot”, “cold”.", "Nunca force: “you don't have to eat it, but let's try one little bite”."],
              ["Mmm, yum! Do you like it?", "No, thank you. That's okay.", "It's cold. It's sweet. It's good!"],
              ["Yum or yuck?", "Is it hot or cold?", "Do you want one more bite?"],
              "Dar nome aos gostos e permitir um “no, thank you” educado leva a briga para um lugar seguro: a recusa vira palavra, e não choro. Provar “um pedacinho”, sem pressão, é uma das orientações mais comuns para crianças que recusam comida.",
              atencao=ENGASGO + "",
              variar=["Prove de olhos fechados e adivinhe: “is it sweet?”.", "Misture: “bread and cheese”.", "Faça o ursinho dizer “yum”."])

    rimas(L, "Para a mesa", [
        dict(t="Pease porridge hot", linhas=["Pease porridge hot,", "pease porridge cold,", "pease porridge in the pot,", "nine days old."],
             gesto="bata as mãos dela nas suas no ritmo; “hot”, abane como se estivesse quente; “cold”, esfregue os braços. É um jogo de palmas antigo.", origem=TRAD_EN, motivos=["tigela", "colher"]),
        dict(t="Hot cross buns", linhas=["Hot cross buns! Hot cross buns!", "One a penny, two a penny,", "hot cross buns!"],
             gesto="cante e mostre um dedo para “one”, dois para “two”; no “hot”, sopre. Funciona bem à mesa, enquanto o prato chega.", origem=TRAD_EN, motivos=["pao", "estrela"])],
        "Rimas de comida e de contar (“one a penny, two a penny”) ensinam palavras e números pelo ritmo. Cante antes de comer, quando a criança está esperando: ela passa a esperar cantando.")

    rimas(L, "Mais para a mesa", [
        dict(t="Yum, yum, yum", linhas=["Yum, yum, yum,", "food for my tum;", "one bite, two bites, three,", "yum, yum, yum for me!"],
             gesto="esfregue a barriga no “yum”, mostre os dedos para contar as mordidas. Serve para começar a comer com alegria.", origem=COLECAO, motivos=["prato", "carinha_feliz"]),
        dict(t="Wash your hands", linhas=["Wash, wash, wash your hands,", "bubbles, bubbles, one, two, three;", "rinse, rinse, rinse them clean,", "dry, dry, dry, and now we eat!"],
             gesto="faça o gesto de lavar, enxaguar e secar as mãos junto com ela, antes de cada refeição. É a rima da troca: acaba a brincadeira, começa a comida.", origem=COLECAO, motivos=["sabonete", "toalha"])],
        "Uma rima fixa para a troca (brincar → lavar as mãos → comer) avisa o fim de uma atividade e reduz o “não”: ela já sabe o que vem. Use sempre a mesma música, na mesma ordem.")

    atividade(L, "Smell the soup, blow the soup", "acalmar", "3 minutos",
              "uma xícara de sopa morna (não quente) ou um prato de comida morna",
              cena([("tigela", 34, 12, 14), ("nariz", 26, 52, 18), ("boca", 28, 86, 18), ("colher", 28, 122, 14)], 46, 190),
              ["Antes de comer, sentem com a comida na frente, ainda sem tocar.", "“Smell the soup”: inspire pelo nariz. “Blow the soup”: sopre devagar pela boca.", "Faça junto, duas vezes, e só então: “now we eat”.",
               "Se a comida estiver quente demais, espere: “it's too hot, let's blow more”."],
              ["Smell the soup… mmm, it smells so good.", "Now blow the soup. Nice and slow.", "It's warm now. Let's eat."],
              ["Does it smell good?", "Is it hot or warm?", "Can you blow?"],
              "Cheirar e soprar a comida é uma respiração calma disfarçada, e dá a ela um jeito de esperar a comida esfriar, em vez de querer comer na hora. Serve também de “porta” para o início da refeição, e ajuda quem chega à mesa agitada.",
              atencao="teste a temperatura da comida antes de servir: morna, nunca quente.",
              variar=["“Smell the flower, blow the candle” (da unidade 1) antes de comer.", "Sopre o chá morno.", "Cheire as frutas: “smell the orange”."], registro=CAL)

    atividade(L, "Slow bites", "acalmar", "5 minutos",
              "três pedaços pequenos de uma fruta mole, no prato",
              cena([("maca", 30, 12, 14), ("morango", 26, 48, 18), ("banana", 28, 82, 16), ("colher", 26, 118, 18), ("coracao", 24, 152, 18)], 46, 190),
              ["Sentem sem pressa, sem outras distrações, e ponha três pedaços no prato dela.", "Diga: “one slow bite”. Mostre como mastigar devagar e sentir o gosto.", "Pergunte: “is it sweet? is it soft?”.",
               "Repita com o segundo e o terceiro pedaço."],
              ["One slow bite. Chew, chew, chew.", "Is it sweet? Is it soft?", "Two slow bites. Three! All done."],
              ["How does it taste?", "Is it soft or crunchy?", "Do you want another?"],
              "Comer devagar, prestando atenção ao gosto, é uma atividade de poucos minutos, com começo, meio e fim, que a criança consegue completar: ótimo para quem tem dificuldade de se concentrar por muito tempo. "
              "É também um jeito de baixar a agitação antes de uma refeição.",
              atencao=ENGASGO,
              variar=["Prove de olhos fechados.", "Ela conta as mordidas: “one, two, three”.", "Faça de conta que a fruta é um “tesouro”."], registro=CAL)

    leitura(L, "The Very Hungry Caterpillar", "Eric Carle", "5 a 10 minutos",
            cena([("lagarta", 32, 12, 16), ("maca", 26, 50, 18), ("pera", 26, 82, 18), ("morango", 24, 114, 18), ("borboleta", 30, 146, 14)], 46, 190),
            ["Sentem com o livro e deixe que ela vire a página; mostre o buraco que a lagarta faz.", "Em cada página, nomeie a comida e conte: “one apple”, “two pears”.", "Peça que ela aponte a fruta: “where is the strawberry?”.",
             "No fim, falem da borboleta: “a beautiful butterfly”."],
            ["Look! The caterpillar is hungry.", "One apple. Where is the apple?", "Now the caterpillar is full."],
            ["What did the caterpillar eat?", "How many pears?", "Can you find the strawberry?"],
            "Leitura dialogada (Whitehurst) com um livro de comida e de contar: as palavras vêm com a imagem e a repetição. As comidas do livro também podem ser procuradas na cozinha (“where is the apple?”), o que leva o inglês do livro à vida. "
            "Em dias de recusa à mesa, ler o livro antes do lanche ajuda.",
            variar=["Procure na cozinha o que a lagarta comeu.", "Conte os buraquinhos da página.", "Leia só até a quinta página, se ela se cansar."])


# ================================================================== U4 LET'S PLAY

def unidade4(L):
    ativ = [("Stomp and freeze", "corpo", "5 min"), ("Build and knock down", "maos", "10 min"), ("Where is it?", "conversar", "5 a 10 min"), ("My turn, your turn", "conversar", "5 min"),
            ("Jack be nimble · One, two, buckle my shoe · Stomp, stomp, stomp · The Grand Old Duke of York", "cantar", "2 min cada"),
            ("Robot and noodle", "acalmar", "3 min"), ("Tidy-up song", "acalmar", "5 min"), ("From Head to Toe", "ler", "5 a 10 min")]
    abertura_unidade(L, 3,
                     "Brincar dentro de casa é o momento em que o inglês mais cabe: pular, empilhar, esconder, revezar. As frases são curtas e vêm com o gesto. "
                     "Brincar também é onde aparecem o “não” e a frustração, então há atividades de revezar e de acalmar depois de agitar.",
                     ativ, cena([("tijolos", 30, 8, 14), ("pegada", 18, 44, 6), ("tambor", 28, 66, 16), ("estrela", 24, 104, 18), ("sino", 26, 140, 16)], 44, 190))

    atividade(L, "Stomp and freeze", "corpo", "5 minutos",
              "uma música cantada por você e um espaço livre de obstáculos",
              cena([("pe", 28, 12, 14), ("pegada", 18, 52, 8), ("estrela", 24, 80, 18), ("sino", 26, 114, 16), ("coracao", 24, 150, 18)], 46, 190),
              ["Cante ou ponha uma música e comecem: “stomp, stomp, stomp!”.", "De repente, diga “freeze!” e as duas ficam paradas como estátua.", "Conte “one, two, three” e diga “go!” para voltar a dançar.",
               "Troquem de papéis: ela diz “freeze”."],
              ["Stomp, stomp, stomp your feet!", "Freeze! Don't move.", "One, two, three… go!"],
              ["Can you stomp?", "Can you freeze?", "Who says freeze now?"],
              "Parar de repente no meio do movimento é um exercício de controle do impulso, e uma brincadeira de Resposta Física Total: “stomp”, “freeze” e “go” são comandos que a criança entende pelo corpo. "
              "Deixar que ela dê o comando ajuda quem gosta de mandar.",
              atencao="chão firme e sem obstáculos.",
              variar=["Freeze de bicho: “freeze like a cat”.", "Freeze bem devagar: “slow motion”.", "Dance com um lenço e deixe cair no “freeze”."])

    atividade(L, "Build and knock down", "maos", "10 minutos",
              "blocos grandes e leves, ou caixas de papelão e copos de plástico",
              cena([("tijolos", 34, 12, 14), ("caixa", 30, 50, 18), ("quadrado_azul", 24, 86, 20), ("retangulo_verde", 28, 118, 18), ("triangulo_amarelo", 24, 152, 20)], 48, 190),
              ["Construa uma torre: “one block, two blocks, three blocks”, e deixe que ela ponha o último.", "Diga “up, up, up!”, e depois “knock it down!”: ela derruba.", "Recomece: “again!”. Diga “oh no!” sem drama quando cair sozinha.",
               "Guardem juntos: “blocks in the box”."],
              ["One block, two blocks, three blocks. Up, up, up!", "Knock it down! Crash!", "Again? Let's build it again."],
              ["How many blocks?", "Up or down?", "Do you want to build again?"],
              "Empilhar e derrubar ensina “up” e “down”, contar até 3 e, o que é mais importante aos 2 anos, a recomeçar sem raiva: quando a torre cai, a resposta é “again!”. "
              "Para quem se frustra fácil, é um bom treino com a emoção.",
              atencao="blocos leves, sem peças pequenas; derrube longe do rosto dela.",
              variar=["Empilhem almofadas.", "Cada bloco, uma cor: “the red block”.", "Faça uma ponte para o carrinho: “over, under”."])

    atividade(L, "Where is it?", "conversar", "5 a 10 minutos",
              "um brinquedo pequeno e três lugares: uma caixa, uma cadeira, uma almofada",
              cena([("caixa", 32, 12, 16), ("cadeira", 28, 50, 14), ("coracao", 26, 88, 18), ("lupa", 28, 122, 16), ("estrela", 24, 156, 18)], 46, 190),
              ["Mostre o brinquedo e esconda-o: “in the box”, “under the chair”, “on the pillow”.", "Pergunte: “where is it?”. Deixe que ela procure e aponte.", "Ao achar: “there it is! Under the chair!”.",
               "Troquem: ela esconde e você procura, com lentidão."],
              ["Where is the ball? Let's look.", "Under the chair! There it is.", "Now you hide it. I'll count to three."],
              ["Where is it?", "Is it in the box?", "Is it under the chair?"],
              "“In”, “on” e “under” são as palavras de posição mais fáceis de aprender com o corpo, porque se mostram com as mãos. A brincadeira de esconder também treina a memória e a espera, e quando ela é a escondedora, ela manda no jogo.",
              variar=["Esconda o ursinho em três lugares, um por dia.", "Procurem “under the bed”.", "Esconda você: “where is Mama?”, e apareça."])

    atividade(L, "My turn, your turn", "conversar", "5 minutos",
              "uma bola leve ou uma meia enrolada; um espaço no chão",
              cena([("circulo_vermelho", 30, 12, 14), ("pegada", 18, 52, 10), ("maos_juntas", 30, 80, 14), ("laranja", 24, 118, 18), ("estrela", 24, 152, 18)], 46, 190),
              ["Sentem de frente, a dois passos. Role a bola: “my turn!”.", "Quando ela devolver: “your turn!”.", "Faça uma pausa e espere; se ela quiser ficar com a bola, diga “my turn… then your turn”.",
               "Aumentem para três jogadores quando ela já souber."],
              ["My turn! Here it comes.", "Your turn! Roll it to me.", "Thank you for sharing. Good job!"],
              ["Whose turn is it?", "Do you want to roll it?", "Can you give it to me?"],
              "Esperar a vez é uma das coisas mais difíceis aos 2 anos: a criança precisa segurar o desejo de ter a bola o tempo todo. “My turn / your turn” é uma frase curta, repetida, que ela pode usar com outras crianças. "
              "Quando ficar brava com a bola indo embora, dê nome à emoção (“you're upset”) e continue.",
              variar=["Revezem para empilhar blocos.", "Com um ursinho: “Teddy's turn!”.", "Cantem a frase no ritmo."])

    rimas(L, "Para pular e contar", [
        dict(t="Jack be nimble", linhas=["Jack be nimble,", "Jack be quick,", "Jack jump over", "the candlestick."],
             gesto="ponha um pano no chão (a “vela” é de faz de conta, nunca fogo) e pulem juntos por cima no “jump”. Repita mais rápido e mais devagar.", origem=TRAD_EN, motivos=["pegada", "vela"]),
        dict(t="One, two, buckle my shoe", linhas=["One, two, buckle my shoe;", "three, four, knock at the door;", "five, six, pick up sticks;", "seven, eight, lay them straight;", "nine, ten, a big fat hen."],
             gesto="mostre os dedos de cada número; mime fivelar o sapato, bater à porta, pegar gravetos. Cante só até quatro, se ela se cansar.", origem=TRAD_EN, motivos=["barra_1", "barra_2", "barra_3"])],
        "Rimas de pular e de contar juntam corpo e números, e as palavras de verbos (jump, knock, pick up) se aprendem pelo gesto. Escolha uma por semana e repita.")

    rimas(L, "Para dançar e subir", [
        dict(t="Stomp, stomp, stomp", linhas=["Stomp, stomp, stomp your feet,", "clap, clap, clap, clap, clap;", "stop, stop, stop and freeze,", "one, two, three… go!"],
             gesto="bata os pés, bata palmas, pare como estátua e volte a dançar no “go”. É a rima da brincadeira “stomp and freeze”.", origem=COLECAO, motivos=["pe", "maos_juntas"]),
        dict(t="The Grand Old Duke of York", linhas=["Oh, the grand old Duke of York,", "he had ten thousand men;", "he marched them up to the top of the hill,", "and he marched them down again.", "And when they were up, they were up,", "and when they were down, they were down,", "and when they were only half-way up,", "they were neither up nor down."],
             gesto="marchem juntos; levantem-se nos “up” e agachem nos “down”, e fiquem no meio no último verso. É uma rima antiga para aprender “up” e “down”.", origem=TRAD_EN, motivos=["pegada", "estrela"])],
        "“Up” e “down” são as primeiras palavras de direção, e esta rima as mostra com o corpo inteiro. A criança entende pelo movimento antes de falar, e depois pede “again!”.")

    atividade(L, "Robot and noodle", "acalmar", "3 minutos",
              "um espaço livre",
              cena([("pegada", 18, 12, 10), ("mao", 30, 40, 16), ("coracao", 24, 76, 18), ("estrela", 22, 108, 18), ("lua", 24, 142, 16)], 46, 190),
              ["Fiquem em pé. Diga “robot!” e fiquem duros como robôs, braços e pernas bem firmes.", "Depois diga “noodle!” e fiquem moles como macarrão cozido, braços e cabeça soltos.", "Repita três vezes, cada vez mais devagar.",
               "Termine deitados ou sentados: “soft and calm”."],
              ["Robot! Stiff and strong.", "Noodle! Soft and floppy.", "Now we're calm. Breathe in… and out."],
              ["Are you a robot or a noodle?", "Is your body soft?", "Can you be a noodle?"],
              "Alternar o corpo duro e o corpo mole é um jeito de sentir a diferença entre tensão e relaxamento, e funciona depois de uma brincadeira agitada ou de uma crise. “Robot” e “noodle” são palavras novas e engraçadas, que a criança repete com prazer.",
              variar=["Faça de gato: “stretch” e “soft”.", "Com música: rápida e lenta.", "Termine com a mão no peito: “feel your heart”."], registro=CAL)

    atividade(L, "Tidy-up song", "acalmar", "5 minutos",
              "os brinquedos do dia e uma caixa",
              cena([("caixa", 34, 12, 14), ("tijolos", 28, 50, 18), ("tambor", 26, 84, 18), ("sino", 24, 118, 18), ("coracao", 24, 152, 18)], 48, 190),
              ["Avise antes: “five more minutes, then tidy up”.", "Cantem uma frase sua, sempre a mesma, enquanto guardam: “tidy up, tidy up, blocks in the box” (invente a melodia).", "Dê a ela um brinquedo de cada vez: “blocks in the box”.",
               "No fim, “all done! Good job!” e um abraço."],
              ["Time to tidy up. Blocks in the box.", "Pick it up. Put it in. Good job!", "All done. Let's have a hug."],
              ["Where do the blocks go?", "Can you put the ball in the box?", "Is it all clean?"],
              "Guardar os brinquedos é uma das trocas mais difíceis: a criança não quer parar de brincar. Avisar antes, cantar e dar tarefas pequenas (“blocks in the box”) transforma a troca em ritual, e o fim calmo (um abraço) volta ao carinho depois do conflito. "
              "É também uma atividade de vida prática.",
              variar=["Cada brinquedo tem a sua “casa”.", "Guardem como bichos: “hop like a frog”.", "Quem guarda mais rápido: você ou ela?"], registro=CAL)

    leitura(L, "From Head to Toe", "Eric Carle", "5 a 10 minutos",
            cena([("gato", 28, 12, 16), ("cisne", 28, 46, 16), ("elefante", 30, 82, 14), ("tartaruga", 28, 118, 18), ("canguru", 28, 152, 14)], 46, 190),
            ["Sentem juntos, com o livro aberto, e deixe que ela escolha o bicho.", "Leia a pergunta do livro e faça o gesto do bicho; espere ela fazer também.", "Elogie: “you can do it!”.",
             "Repitam o movimento do bicho, em pé, depois do livro."],
            ["Look! The cat arches its back. Can you?", "I can do it! Can you do it?", "Wow, you did it!"],
            ["Can you do it?", "What does the elephant do?", "Can you wiggle like me?"],
            "É leitura dialogada com Resposta Física Total: o livro de Eric Carle pergunta se a criança consegue fazer o gesto de cada bicho, e ela mostra com o corpo, sem precisar falar. A pergunta “can you do it?” é a mais fácil de responder, com um gesto, e “you can do it” é um elogio que vale o dia todo.",
            variar=["Escolha um bicho por dia e faça o movimento no tapete.", "Leia só até o macaco.", "Ela escolhe a página: “this one!”."])


# ================================================================== U5 OUTSIDE

def unidade5(L):
    ativ = [("Look up, look down", "mundo", "10 min"), ("Collect a leaf", "mundo", "10 min"), ("Puddle jump", "corpo", "5 min"), ("Walk, run, stop", "corpo", "10 min"),
            ("Rain, rain, go away · Round and round the garden · Itsy Bitsy Spider · Look around", "cantar", "2 min cada"),
            ("Cloud watching", "acalmar", "5 min"), ("Three sounds", "acalmar", "3 min"), ("Rosie's Walk", "ler", "5 a 10 min")]
    abertura_unidade(L, 4,
                     "Sair é o quinto momento de inglês: há tudo para apontar e nomear (sol, nuvem, folha, passarinho) e o corpo todo para mexer. "
                     "Aqui o inglês é de olhar e escutar, e várias atividades servem de acalmar sem se chamarem assim. <b>Na rua, mão dada e olhos sempre nela.</b>",
                     ativ, cena([("sol", 30, 8, 10), ("arvore_verao", 30, 44, 12), ("folha_carvalho", 26, 80, 18), ("nuvem", 32, 112, 12), ("bota", 26, 152, 16)], 44, 190))

    atividade(L, "Look up, look down", "mundo", "10 minutos",
              "um quintal, uma praça ou uma calçada",
              cena([("sol", 30, 12, 8), ("nuvem", 34, 48, 12), ("arvore_verao", 30, 88, 10), ("pedra", 24, 124, 20), ("formiga", 24, 156, 22)], 48, 190),
              ["Pare e diga “look up!”, apontando o céu: “the sky, the sun, a cloud, a bird”.", "Depois: “look down!”, apontando o chão: “the ground, a stone, an ant”.", "Fiquem em silêncio um minuto antes de nomear.",
               "Deixe que ela aponte e diga o que quiser, em português: repita em inglês."],
              ["Look up! I see the sky. I see a cloud.", "Look down! I see a stone. I see an ant.", "What do you see? Show me."],
              ["What do you see?", "Where is the bird?", "Is it big or small?"],
              "Dar um nome ao que se vê, com o dedo apontando, é o que a entrada compreensível pede: a palavra vem com o objeto. “Up” e “down” são palavras de direção que o corpo entende, e olhar para cima e para baixo é um jeito de parar e olhar (Charlotte Mason).",
              atencao="não olhe para o sol; em lugar com trânsito, mão dada o tempo todo.",
              variar=["Procure só uma cor: “find something green”.", "Olhe só para cima hoje, só para baixo amanhã.", "Fotografe com os olhos: “click!”."])

    atividade(L, "Collect a leaf", "mundo", "10 minutos",
              "uma sacola de pano ou uma cesta",
              cena([("folha_carvalho", 32, 12, 14), ("folha_bordo", 28, 48, 18), ("folha_coracao", 28, 84, 16), ("folha_seca", 26, 118, 20), ("cesta", 30, 152, 14)], 48, 190),
              ["Combine: “let's find three leaves”. Só as que já estão no chão.", "Cada folha vai para a cesta com um nome: “big leaf”, “small leaf”, “green”, “yellow”.", "Em casa, ponham as folhas em fila: “big, bigger, biggest”.",
               "Pare em três ou cinco folhas: é uma tarefa com fim."],
              ["I found a leaf! A big, green leaf.", "This one is small and yellow. Into the basket.", "Three leaves! We did it."],
              ["Is it big or small?", "What color is it?", "How many leaves?"],
              "Procurar folhas dá um objetivo ao passeio, e contar até três ou cinco ajuda quem tem pouca paciência a saber quando acaba. Comparar tamanho e cor (“big, small, green, yellow”) é vocabulário de verdade, com o objeto na mão.",
              atencao="só folhas caídas; não tire do galho nem leve à boca; lave as mãos depois.",
              variar=["Esfregue uma folha: “it smells”.", "Faça um “tapete de folhas” e pule: “crunch!”.", "Procure só folhas vermelhas."])

    atividade(L, "Puddle jump", "corpo", "5 minutos",
              "botas (ou pés descalços), uma poça rasa e limpa, ou um tapete azul fazendo de poça",
              cena([("poca", 40, 12, 22), ("bota", 28, 62, 6), ("guarda_chuva", 30, 96, 10), ("gota", 14, 132, 8), ("gota", 12, 148, 28)], 52, 190),
              ["Mostre o pulo com os dois pés: “jump, jump, jump!”.", "Conte: “one, two, three… splash!”.", "Alternem rápido e devagar: “fast”, “slow”.", "Troquem: ela diz quando pular."],
              ["One, two, three… splash!", "Jump, jump, jump! A big puddle.", "Now slow. Nice and slow."],
              ["Is the puddle big or small?", "Fast or slow?", "Who jumps next?"],
              "Pular junto, com comando de voz, trabalha equilíbrio e coordenação e as palavras que descrevem o movimento (fast, slow, big, small), e é Resposta Física Total. É uma das brincadeiras mais queridas por quem gosta de chuva e de bagunça.",
              atencao=AGUA + " Chão firme e sem escorregar; poça só se a água estiver limpa e você vir o fundo.",
              variar=["Pule uma fita no chão.", "Pule de sapo: “frog jump”.", "Em casa, um tapete azul: “the puddle”."])

    atividade(L, "Walk, run, stop", "corpo", "10 minutos",
              "uma calçada larga, um parque ou um corredor",
              cena([("pegada", 18, 12, 8), ("pe", 28, 40, 16), ("estrela", 24, 76, 18), ("pegada_esq", 18, 108, 8), ("coracao", 24, 140, 18)], 48, 190),
              ["De mãos dadas, diga “walk” e caminhem; “run” e corram um pouco; “stop!” e parem.", "Pare sempre na beira da calçada: “stop at the edge. Hold my hand.”.", "Deixe que ela diga “walk”, “run” e “stop” e que você obedeça.",
               "Termine com um abraço: “good listening”."],
              ["Walk, walk, walk. Hold my hand.", "Run, run, run! And… stop!", "Stop at the edge. Good job stopping!"],
              ["Do you want to walk or run?", "Can you stop?", "Where do we stop?"],
              "“Walk, run, stop” é uma Resposta Física Total com um uso de segurança: a criança aprende a parar ao comando, e o “stop at the edge” é uma regra que vale na rua. Também é uma brincadeira de controle do impulso: ela corre, e para quando você diz.",
              atencao="em lugar com carros, só com ela de mão dada; nunca solte a mão dela na beira da calçada.",
              variar=["Corra de formiga: pequenos passos.", "Pare como estátua: “freeze”.", "Faça o carrinho: “beep beep, stop”."])

    rimas(L, "Para a chuva e para o jardim", [
        dict(t="Rain, rain, go away", linhas=["Rain, rain, go away,", "come again another day;", "little [Marina] wants to play,", "rain, rain, go away."],
             gesto="mostre a chuva com os dedos caindo e abane para mandar embora; no terceiro verso, ponha o nome da criança. Cante olhando a janela.", origem=TRAD_EN, motivos=["nuvem_chuva", "sol"]),
        dict(t="Round and round the garden", linhas=["Round and round the garden", "like a teddy bear;", "one step, two step,", "tickle you under there!"],
             gesto="faça um círculo na palma dela com o dedo; “one step, two step”: suba os dedos pelo braço; “tickle you”: cócegas debaixo do braço. É um jogo antigo de mão.", origem=TRAD_EN, motivos=["mao", "flor_rosa"])],
        "Rimas de chuva e de jardim ligam o inglês ao que ela vê da janela, e as de mão têm o toque, o que ajuda quem se distrai fácil. O “de novo!” depois das cócegas é o melhor pedido.")

    rimas(L, "Para a aranha e para olhar", [
        dict(t="Itsy Bitsy Spider", linhas=["The itsy bitsy spider", "climbed up the waterspout;", "down came the rain", "and washed the spider out;", "out came the sun", "and dried up all the rain,", "and the itsy bitsy spider", "climbed up the spout again."],
             gesto="faça a aranha com os dedos subindo pelo braço, a chuva com os dedos caindo, o sol com as mãos abertas, e a aranha subindo de novo. É uma rima de insistir depois de cair.", origem=TRAD_EN, motivos=["aranha", "nuvem_chuva"]),
        dict(t="Look around", linhas=["Look up, look down,", "look all around;", "what do you see?", "what do you hear?"],
             gesto="aponte para cima, para baixo, e gire a cabeça nos dois primeiros versos; nos últimos, espere e deixe que ela responda com um gesto. Cante ao chegar a qualquer lugar.", origem=COLECAO, motivos=["olho", "orelha"])],
        "A aranha é uma rima de insistir: ela cai, e sobe de novo, o que vale para quem se frustra fácil. A rima da coleção serve de ritual de chegada ao passeio: sempre as mesmas perguntas, e a criança aprende a olhar e a ouvir.")

    atividade(L, "Cloud watching", "acalmar", "5 minutos",
              "uma manta na grama ou o colo; um dia com nuvens",
              cena([("nuvem", 40, 12, 10), ("nuvem", 32, 58, 20), ("sol", 28, 98, 8), ("arvore_verao", 30, 136, 12)], 48, 190),
              ["Deitem lado a lado, de barriga para cima, em silêncio por um minuto.", "Diga o que vê: “a big cloud”, “a small cloud”, “a fluffy cloud”.", "Procurem formas: “is it a dog?”.",
               "Fiquem o quanto ela quiser."],
              ["Look at the sky. A big, white cloud.", "It's moving slowly. Whoosh.", "What does it look like? A dog? A bird?"],
              ["What do you see?", "Is the cloud big or small?", "Where is it going?"],
              "Deitar e olhar o céu pede quietude sem exigir nada: é calma sem ser “aula de calma”. As palavras (cloud, big, small, slow) vêm com o objeto que se vê, e a imaginação (“what does it look like?”) é bem-vinda.",
              atencao="não olhe para o sol; use chapéu e protetor solar; verifique a grama (formigas, espinhos).",
              variar=["À noite, com a lua e as estrelas.", "Olhe as folhas balançando.", "Sopre a nuvem: “blow the cloud away”."], registro=CAL)

    atividade(L, "Three sounds", "acalmar", "3 minutos",
              "nenhum; um lugar com poucos sons",
              cena([("orelha", 36, 12, 10), ("m_passaros", 34, 56, 12), ("sino", 26, 96, 18), ("nuvem", 32, 130, 14)], 46, 190),
              ["Sentem juntos e diga: “let's listen for three sounds”.", "Fiquem em silêncio um minuto. Levante um dedo a cada som.", "Dê o nome de cada um: “a bird”, “a car”, “the wind”.",
               "Depois, imitem um dos sons, bem baixinho."],
              ["Shh… listen. One sound!", "It's a bird. Tweet, tweet.", "Two sounds. Three. Good listening."],
              ["What do you hear?", "Is it loud or quiet?", "Where is it coming from?"],
              "Escutar em silêncio, mesmo por um minuto, treina a atenção e acalma. É uma das atividades mais curtas e mais fáceis de repetir em qualquer lugar. “Listen” e “quiet” são palavras úteis, e “good listening” é um elogio que vale ao dia todo.",
              variar=["De olhos fechados, se ela quiser.", "Em casa, de dia e de noite: o que muda?", "Com um sino: “ding, ding, listen”."], registro=CAL)

    leitura(L, "Rosie's Walk", "Pat Hutchins", "5 a 10 minutos",
            cena([("cuco", 28, 12, 16), ("arvore_verao", 30, 46, 10), ("cesta", 28, 84, 18), ("casinha", 28, 118, 16), ("folha", 24, 154, 20)], 46, 190),
            ["Sentem juntos, com o livro aberto; leia o texto curto e deixe que ela olhe as figuras.", "Aponte para onde Rosie anda: “across the yard”, “around the pond”.", "Mostre as posições com a mão: “over”, “under”, “through”.",
             "Saiam depois para uma caminhada e nomeiem os lugares: “over the grass”, “under the tree”."],
            ["Rosie goes for a walk. Look, a hen.", "Over the haystack. Under the tree.", "Where is the hen now?"],
            ["Where is the hen?", "Is she over the haystack or under the tree?", "What do you see in the picture?"],
            "É leitura dialogada (Whitehurst): o texto do livro é curto e todo de posições (“across”, “over”, “under”), que se entendem com a mão e com o corpo; a graça está nas figuras, que o texto não conta. "
            "O passeio depois do livro leva as palavras de posição para a vida.",
            variar=["Faça o percurso do livro com almofadas: “over the pillow”.", "Procure a raposa em cada página.", "Leia só até a metade."])


# ================================================================== U6 ANIMALS

def unidade6(L):
    ativ = [("Animal sounds", "nomear", "5 min"), ("Animal walks", "corpo", "5 a 10 min"), ("Feed the animals", "maos", "10 min"), ("Mama and baby", "conversar", "5 a 10 min"),
            ("Baa, baa, black sheep · Mary had a little lamb · Hey diddle diddle · Hickory dickory dock", "cantar", "2 min cada"),
            ("Soft hands", "acalmar", "3 min"), ("Sleepy animals", "acalmar", "5 min"), ("Dear Zoo", "ler", "5 a 10 min")]
    abertura_unidade(L, 5,
                     "Os bichos são o assunto que mais combina com o inglês aos 2 anos: cada um tem nome, som e movimento, e a criança já os conhece em português. "
                     "Aqui há sons para imitar, andares para fazer e um bicho para cuidar: “soft hands” é uma das frases mais úteis para quem está aprendendo a ser gentil.",
                     ativ, cena([("cachorro", 28, 8, 14), ("gato", 28, 42, 16), ("leao", 28, 76, 12), ("patinho", 26, 112, 18), ("elefante", 30, 148, 12)], 44, 190))

    atividade(L, "Animal sounds", "nomear", "5 minutos",
              "três bichos de pelúcia ou de figuras: cachorro, gato, pato",
              cena([("cachorro", 30, 12, 14), ("gato", 28, 48, 16), ("patinho", 26, 84, 18), ("leao", 28, 118, 14), ("elefante", 30, 152, 12)], 46, 190),
              ["Mostre um bicho e diga o nome: “dog”. Faça o som: “woof, woof”.", "Deixe que ela faça o som; repita o nome e acrescente: “a big dog”.", "Troque: “cat… meow”, “duck… quack”.",
               "Esconda um bicho: “where is the cat?”."],
              ["This is a dog. The dog says woof!", "A cat. The cat says meow.", "A duck says quack, quack!"],
              ["What does the dog say?", "Where is the cat?", "Is the duck big or small?"],
              "Nomear com o bicho na mão e fazer o som é uma entrada compreensível (Krashen e Terrell): a criança entende pelo objeto e pelo som, e o som ajuda a lembrar o nome. Os sons em inglês (woof, meow, quack) diferem do português (au-au, miau, quá-quá) e ela pode ficar com os dois.",
              variar=["Um bicho por dia, só um.", "Procure bichos no livro: “where is the cow?”.", "Esconda o bicho e dê dicas de som."])

    atividade(L, "Animal walks", "corpo", "5 a 10 minutos",
              "um espaço livre, no chão firme",
              cena([("lebre", 28, 12, 14), ("tartaruga", 28, 46, 18), ("canguru", 28, 82, 12), ("cisne", 26, 118, 16), ("elefante", 30, 152, 12)], 48, 190),
              ["Mostre um bicho e faça o andar: “hop like a bunny”, “waddle like a duck”, “stomp like an elephant”.", "Ela imita; depois, ela escolhe o bicho.", "Alterne fast e slow: “run like a horse, creep like a turtle”.",
               "Termine com “freeze like a statue”."],
              ["Hop, hop, hop like a bunny.", "Waddle, waddle like a duck.", "Slow, slow like a turtle."],
              ["Can you hop?", "Can you waddle?", "Which animal are you?"],
              "É uma Resposta Física Total, com os bichos como pretexto: os verbos (hop, waddle, stomp, creep) são aprendidos pelo corpo, e as variações de ritmo (fast, slow) servem para gastar energia e voltar à calma. A criança dessa idade adora ser bicho.",
              atencao="chão firme e sem obstáculos.",
              variar=["Ela faz o bicho e você adivinha.", "Marchem como elefante e voltem como lesma.", "Faça o bicho dormindo: “sleepy cat”."])

    atividade(L, "Feed the animals", "maos", "10 minutos",
              "bichos de pelúcia, uma tigela de plástico e “comidas” de brinquedo grandes ou de pano",
              cena([("tigela", 32, 12, 16), ("maca", 26, 48, 18), ("cachorro", 28, 82, 14), ("gato", 28, 116, 14), ("morango", 24, 152, 20)], 48, 190),
              ["Alinhe os bichos e diga: “they are hungry”. Ela “dá” a comida a cada um.", "Nomeie a comida: “apple for the dog”, “milk for the cat”.", "Quando estiver cheio: “full”; quando quiser mais: “more?”.",
               "Ponham os bichos para dormir: “night night”."],
              ["The dog is hungry. Apple for the dog.", "Yum, yum! Is he full?", "More? Or all done?"],
              ["Who is hungry?", "What does the cat eat?", "Is the dog full?"],
              "Cuidar dos bichos de brinquedo é uma brincadeira de faz de conta que dá à criança o papel de quem cuida, e é nela que as palavras de comida e de “hungry/full” aparecem em situação real. Dar de comer ao boneco antes de a criança comer ajuda a recusa na mesa.",
              atencao="só objetos grandes e sem peças soltas; nada de comida de verdade para os bichos de pelúcia.",
              variar=["Faça o bicho dizer “no, thank you”.", "Dê banho no bicho: “wash the dog” (sem água de verdade).", "Conte os bichos que comeram."])

    atividade(L, "Mama and baby", "conversar", "5 a 10 minutos",
              "figuras ou bichos de plástico em pares (mãe e filhote), ou um livro de animais",
              cena([("gato", 30, 12, 16), ("patinho", 24, 48, 22), ("elefante", 30, 82, 12), ("lebre", 24, 118, 20), ("coracao", 24, 152, 20)], 48, 190),
              ["Mostre o par: “a cat and a kitten”. Aponte: “mama cat, baby cat”.", "Faça o som dos dois: um grave, outro agudo.", "Deixe que ela junte as famílias: “where is the baby?”.",
               "Fale do cuidado: “Mama feeds the baby”."],
              ["This is the mama cat. This is the baby.", "Mama says meow. Baby says mew, mew.", "Where is the baby duck? Show me."],
              ["Who is the mama?", "Where is the baby?", "Are they together?"],
              "Os pares de mãe e filhote ensinam “mama” e “baby” e as primeiras palavras de família, e ligam o assunto dos bichos ao afeto, o que ajuda a criança a falar de si mesma como “baby”. A brincadeira de juntar famílias é também de classificar.",
              variar=["Procure famílias de bichos em um livro.", "Faça a sua família: “Mama, Papa, baby”.", "Esconda o bebê: “where is the baby?”."])

    rimas(L, "Para as ovelhas", [
        dict(t="Baa, baa, black sheep", linhas=["Baa, baa, black sheep,", "have you any wool?", "Yes sir, yes sir,", "three bags full."],
             gesto="faça o som da ovelha e mostre as sacolas com os dedos (“three bags full”). Pode perguntar e responder revezando as vozes.", origem=TRAD_EN, motivos=["leao", "cesta"]),
        dict(t="Mary had a little lamb", linhas=["Mary had a little lamb,", "its fleece was white as snow;", "and everywhere that Mary went", "the lamb was sure to go."],
             gesto="faça a ovelhinha com as mãos, e ande de mãos dadas no “everywhere that Mary went”. No lugar de Mary, ponha o nome dela, se quiser.", origem="Poema de Sarah Josepha Hale (1830), em domínio público.", motivos=["lebre", "folha"])],
        "Rimas de bichos, com sons e com perguntas e respostas, são o jeito mais fácil de ouvir o inglês: curtas, repetidas e com gesto. “Yes sir” é uma resposta que ela pode aprender a dizer.")

    rimas(L, "Para o gato e o rato", [
        dict(t="Hey diddle diddle", linhas=["Hey diddle diddle,", "the cat and the fiddle,", "the cow jumped over the moon;", "the little dog laughed", "to see such sport,", "and the dish ran away with the spoon."],
             gesto="faça o violino com os braços, pule por cima da lua com a mão, e fuja como o prato com a colher. É uma rima do absurdo, e o riso é o objetivo.", origem=TRAD_EN, motivos=["gato", "lua"]),
        dict(t="Hickory dickory dock", linhas=["Hickory, dickory, dock,", "the mouse ran up the clock;", "the clock struck one,", "the mouse ran down,", "hickory, dickory, dock."],
             gesto="suba os dedos pelo braço dela (o rato) até “one”, e desça rápido; bata uma palma no “one”. É uma rima para “up” e “down” e para contar até um.", origem=TRAD_EN, motivos=["ratinho", "sino"])],
        "Rimas de bichos e de absurdos fazem rir, e o riso ajuda a criança a lembrar. “Up” e “down” aparecem de novo, desta vez com o dedinho, e a rima do rato é uma das primeiras de contar.")

    atividade(L, "Soft hands", "acalmar", "3 minutos",
              "um bicho de pelúcia macio, ou o gato ou cachorro da casa, se ele gostar de carinho",
              cena([("mao", 34, 12, 12), ("gato", 30, 52, 16), ("coracao", 26, 90, 18), ("cachorro", 30, 122, 14), ("maos_juntas", 28, 156, 16)], 46, 190),
              ["Mostre como fazer carinho no bicho: “soft hands”, com a mão aberta e devagar.", "Pegue a mão dela e faça junto: “gentle, gentle”.", "Se ela bater ou apertar, pare, e diga calmamente: “soft hands, like this”.",
               "Elogie: “so gentle! The kitty likes it”."],
              ["Soft hands. Gentle, gentle.", "Like this. Pat, pat, pat.", "So gentle! The kitty likes it."],
              ["Are your hands soft?", "Does the kitty like it?", "Can you pat the kitty softly?"],
              "“Soft hands” é uma frase curta e útil para a fase do “não”, em que as mãos às vezes batem ou apertam: ela aprende o que fazer com as mãos, em vez de só o que não fazer. Acariciar devagar, no ritmo, é calmante também para a criança.",
              atencao="com animal de verdade, só se ele for calmo e você ficar junto, e nunca deixe a criança sozinha com ele; lave as mãos depois.",
              variar=["Faça carinho no próprio braço.", "Faça carinho no rosto do ursinho.", "Elogie sempre: “gentle hands!”."], registro=CAL)

    atividade(L, "Sleepy animals", "acalmar", "5 minutos",
              "bichos de pelúcia e uma manta; luz baixa",
              cena([("gato", 30, 12, 16), ("cachorro", 28, 46, 18), ("lebre", 26, 80, 20), ("lua", 24, 114, 16), ("estrela", 22, 148, 18)], 48, 190),
              ["Alinhem os bichos e diga: “the animals are sleepy”.", "Cubra cada um com a manta, devagar: “night night, doggy”, “night night, kitty”.", "Falem baixinho: “shh, they're sleeping”.",
               "Terminem com um beijo em cada bicho e um para ela."],
              ["The animals are sleepy. Let's tuck them in.", "Night night, kitty. Shh, shh.", "They're sleeping. Let's be quiet."],
              ["Are they sleepy?", "Who needs a blanket?", "Can you say night night?"],
              "Pôr os bichos para dormir é uma brincadeira de faz de conta com voz baixa e movimentos lentos, e a criança cuida de quem está cansado: é uma das melhores atividades de acalmar antes do sono ou depois de uma crise. As frases (“night night”, “shh”) já preparam a unidade da hora de dormir.",
              variar=["Cante a canção de ninar para os bichos.", "Cada um tem o seu lugar.", "Ela escolhe quem dorme primeiro."], registro=CAL)

    leitura(L, "Dear Zoo", "Rod Campbell", "5 a 10 minutos",
            cena([("elefante", 30, 12, 14), ("leao", 28, 48, 16), ("tartaruga", 26, 82, 20), ("cachorro", 28, 114, 16), ("caixa", 26, 150, 18)], 46, 190),
            ["Sentem com o livro e deixe que ela abra as abas, uma a uma.", "Antes de abrir, pergunte: “what's in the box?”. Deixe que ela adivinhe.", "Abra, e nomeie o bicho: “an elephant! It's too big”.",
             "Diga a razão de cada devolução: “too big”, “too tall”, “too fierce” (com a mão ou a voz) e mostre."],
            ["What's in the box? Let's look.", "A lion! Roar! Can you roar?", "It's too big. Send it back."],
            ["What's in the box?", "Is it big or small?", "What does it say?"],
            "É leitura dialogada (Whitehurst) com um livro de abas, em que cada página tem uma pergunta e uma surpresa, e a criança participa abrindo. O livro de Rod Campbell tem poucas palavras, repetidas, e adjetivos (big, tall, fierce) que se mostram com o corpo. "
            "O final, em que o bicho certo chega, é um final feliz.",
            variar=["Faça o som e o movimento de cada bicho.", "Esconda os bichos de pelúcia na caixa e adivinhem.", "Leia até o terceiro bicho, se ela se cansar."])


# ================================================================== U7 FAMILY AND FEELINGS

def unidade7(L):
    ativ = [("Who is who?", "nomear", "5 a 10 min"), ("Feeling faces", "conversar", "5 min"), ("I can do it!", "maos", "10 min"), ("Kind hands", "corpo", "5 min"),
            ("Tommy Thumb · Happy, sad, angry, sleepy · I can do it · Soft hands", "cantar", "2 min cada"),
            ("Stomp it out", "acalmar", "3 min"), ("The calm-down corner", "acalmar", "5 min"), ("When Sophie Gets Angry — Really, Really Angry…", "ler", "5 a 10 min")]
    abertura_unidade(L, 6,
                     "A família e os sentimentos são o centro desta unidade, e o inglês aqui serve para dar nome ao que a criança sente: “happy”, “sad”, “angry”, “sleepy”. "
                     "É a unidade da fase do “não”: aqui há as frases para oferecer ajuda (“do you need help?”), para dar nome à raiva (“you're angry”) e para acalmar (“let's breathe”). <b>O sentimento é aceito; o limite continua.</b>",
                     ativ, cena([("carinha_feliz", 28, 8, 14), ("coracao", 26, 44, 18), ("maos_juntas", 28, 78, 14), ("dedo_nao", 28, 114, 14), ("casa", 28, 150, 14)], 44, 190))

    atividade(L, "Who is who?", "nomear", "5 a 10 minutos",
              "fotos da família (de papel, não no celular), ou desenhos",
              cena([("casa", 32, 12, 12), ("carinha_feliz", 26, 50, 18), ("coracao", 26, 84, 18), ("maos_juntas", 28, 118, 16), ("polegar_cima", 26, 152, 18)], 46, 190),
              ["Mostre uma foto e diga quem é: “Mama”, “Papa”, “Grandma”, “baby”, “brother”, “sister”.", "Aponte para a pessoa na foto e depois para a pessoa de verdade, se estiver por perto.", "Pergunte: “where is Papa?”. Aceite o apontar.",
               "Diga o que cada um faz: “Mama is reading”, “Papa is cooking”."],
              ["This is Mama. This is Papa.", "Where is Grandma? Show me.", "Papa is cooking. Mama is reading."],
              ["Who is this?", "Where is the baby?", "What is Mama doing?"],
              "Os nomes da família são as primeiras palavras de uma criança em qualquer língua, e as fotos dão o objeto a que a palavra se liga. Use os termos que fazem sentido na sua família: este caderno não presume quem mora na casa dela. "
              "Ela já conhece essas pessoas, o que faz da atividade um acerto garantido, e isso ajuda quem se frustra fácil.",
              variar=["Faça um “livro da família” de fotos, com um nome em cada página.", "Brinque de esconder uma foto: “where is Papa?”.", "Diga “I love you” a cada foto."])

    atividade(L, "Feeling faces", "conversar", "5 minutos",
              "um espelho inquebrável, ou o seu rosto",
              cena([("carinha_feliz", 32, 12, 12), ("dedo_nao", 28, 50, 16), ("coracao", 26, 86, 18), ("olho", 28, 118, 14), ("lua", 24, 154, 18)], 46, 190),
              ["Sentem de frente para o espelho. Faça uma cara feliz e diga “happy”; ela imita.", "Faça as outras: “sad” (boca para baixo), “angry” (testa franzida), “sleepy” (olhos pesados), “surprised”.", "Diga a frase “it's okay to feel angry”. Faça cada cara, e depois volte à feliz.",
               "Deixe que ela escolha uma cara e você imite."],
              ["I'm happy! Look at my smile.", "Now I'm angry. Grrr. It's okay to feel angry.", "Sad. Sleepy. Surprised! Now happy again."],
              ["How do you feel?", "Are you happy or sad?", "Can you make an angry face?"],
              "Dar nome às emoções, em um momento calmo, é o primeiro passo para ela usá-las no meio da raiva, em vez de gritar ou bater. “It's okay to feel angry” diz à criança que o sentimento é aceito, e o que se faz com ele é que muda. "
              "Repita muitas vezes: o vocabulário dos sentimentos leva tempo.",
              variar=["Fotos da família com caras diferentes.", "Cara de bicho: um leão bravo, um coelho com medo.", "Cara do ursinho: “Teddy is sad”."])

    atividade(L, "I can do it!", "maos", "10 minutos",
              "uma tarefa que ela pode quase fazer sozinha: calçar um sapato, abrir uma caixa, lavar um pano",
              cena([("bota", 28, 12, 16), ("mao", 30, 46, 14), ("polegar_cima", 26, 82, 18), ("caixa", 28, 114, 16), ("estrela", 24, 150, 20)], 46, 190),
              ["Escolha uma tarefa que ela consegue com pouca ajuda e diga: “do you want to try?”.", "Espere e não ajude logo: “you can do it”.", "Se ela pedir, ajude só um pouco: “do you need help?”; deixe que ela diga “yes” ou “no”.",
               "Ao terminar: “you did it! All by yourself!”."],
              ["Do you want to try? You can do it.", "Do you need help? Yes or no?", "You did it! All by yourself!"],
              ["Can you do it?", "Do you need help?", "Are you proud?"],
              "“Eu faço!” é a frase mais típica da fase do “não”: a criança quer fazer sozinha, e o adulto acaba brigando com ela por pressa. Dar tempo, oferecer ajuda como pergunta (“do you need help?”) e elogiar o resultado (“you did it!”) transforma a briga em orgulho. "
              "A palavra “help” é uma das mais úteis a aprender.",
              atencao="escolha tarefas seguras, sem objetos pontudos nem água quente.",
              variar=["Ela guarda os próprios sapatos.", "Ela põe o prato na pia.", "Ela escolhe a camiseta: “this one or that one?”."])

    atividade(L, "Kind hands", "corpo", "5 minutos",
              "um ursinho ou um boneco macio",
              cena([("mao", 34, 12, 12), ("coracao", 26, 50, 18), ("maos_juntas", 30, 84, 14), ("carinha_feliz", 26, 120, 18), ("polegar_cima", 26, 154, 18)], 46, 190),
              ["Mostre: “hands are for hugs”, e abrace o ursinho; depois “hands are for helping”, e ajude a pôr algo no lugar.", "Pergunte: “what can hands do?”. Ela mostra: bater palmas, abraçar, pegar, acenar.",
               "Se ela bater, pare com calma: “hands are not for hitting. Hands are for hugs.”.", "Ofereça o que fazer com a energia: “clap your hands!”."],
              ["Hands are for hugs. Hands are for helping.", "Hands are not for hitting. Show me a hug.", "Clap, clap, clap! Good hands."],
              ["What are hands for?", "Can you give a hug?", "Can you clap?"],
              "Dizer o que as mãos podem fazer, e não só o que não podem, é o conselho mais comum para a fase em que a criança bate: dê a ela uma alternativa (abraçar, bater palmas) em vez de só um “não”. A frase “hands are not for hitting” é curta e fácil de repetir, e há livros infantis com esse título. "
              "Use sempre o mesmo tom calmo, sem gritar.",
              variar=["Faça um abraço no ursinho.", "Dê um “high five”: “up high!”.", "Aperte a mão dela: “nice to meet you”."])

    rimas(L, "Para a família e os sentimentos", [
        dict(t="Tommy Thumb", linhas=["Tommy Thumb, Tommy Thumb,", "where are you?", "Here I am, here I am,", "how do you do?"],
             gesto="esconda os polegares atrás das costas e mostre-os no “here I am”; balance-os como quem cumprimenta. Depois, com os outros dedos, invente os nomes: Peter Pointer, Toby Tall…", origem=TRAD_EN, motivos=["mao", "polegar_cima"]),
        dict(t="Happy, sad, angry, sleepy", linhas=["Happy, happy, clap, clap, clap;", "sad, sad, rub your eyes;", "angry, angry, stomp, stomp, stomp;", "sleepy, sleepy, sigh."],
             gesto="faça o gesto de cada sentimento (palmas, esfregar os olhos, bater os pés, suspirar) e termine no suspiro, com um abraço. Cante-a quando ela estiver calma.", origem=COLECAO, motivos=["carinha_feliz", "dedo_nao"])],
        "A primeira rima é um jogo de dedos da família (o polegar é o “Tommy”), e a segunda dá um gesto para cada sentimento, e termina no mais calmo. Cante as duas quando ela estiver tranquila: assim os gestos ficam prontos para a hora difícil.")

    rimas(L, "Para ajudar e para ser gentil", [
        dict(t="I can do it", linhas=["I can do it, I can do it,", "one, two, three;", "and if I need some help,", "you can help me!"],
             gesto="faça uma tarefa pequena no ritmo (ponha um bloco na caixa); no último verso, estenda a mão para pedir ajuda. É a rima do “eu faço!”.", origem=COLECAO, motivos=["mao", "estrela"]),
        dict(t="Soft hands", linhas=["Soft hands, soft hands,", "pat, pat, pat;", "gentle hands, gentle hands,", "stroke the cat."],
             gesto="faça carinho no ursinho, devagar, no ritmo da rima; no “stroke the cat”, alise o braço dela com um dedo, bem de leve.", origem=COLECAO, motivos=["gato", "mao"])],
        "As rimas da coleção dão, em inglês, as frases da fase do “não”: “I can do it” (eu faço) e “soft hands” (mãos delicadas). Cantá-las nos momentos calmos faz delas um recurso para a hora difícil.")

    atividade(L, "Stomp it out", "acalmar", "3 minutos",
              "um espaço onde ela possa bater os pés",
              cena([("pe", 28, 12, 14), ("pegada", 18, 46, 8), ("pegada_esq", 18, 68, 18), ("coracao", 24, 98, 18), ("estrela", 22, 132, 18)], 46, 190),
              ["Quando ela estiver calma, combine o jogo: “when you're angry, we stomp!”.", "Batam os pés juntos: “stomp, stomp, stomp!”, bem forte, três vezes.", "Depois, respirem fundo: “breathe in… and out”.",
               "Termine com um abraço: “all better”."],
              ["Angry feet! Stomp, stomp, stomp!", "Now breathe in… and out.", "Better? Let's have a hug."],
              ["Are your feet angry?", "Can you stomp louder?", "How do you feel now?"],
              "Dar à raiva um lugar no corpo (os pés), forte e curto, e depois uma respiração lenta, é um modo de a criança soltar a energia sem machucar ninguém. Combine o jogo antes, em um momento calmo, e depois, na raiva de verdade, basta dizer “let's stomp it out”. "
              "A rima “Estou com raiva” (do caderno de atividades) tem a mesma lógica.",
              variar=["Soque uma almofada: “punch the pillow”.", "Rasgue papel: “rip, rip, rip”.", "Sopre uma pena: “blow it away”."], registro=CAL)

    atividade(L, "The calm-down corner", "acalmar", "5 minutos",
              "o cantinho da calma (ver o caderno de atividades) ou um canto com manta e almofada",
              cena([("cama", 34, 12, 12), ("livro", 28, 48, 18), ("bolhas", 30, 82, 14), ("estrela", 24, 118, 18), ("coracao", 26, 152, 18)], 46, 190),
              ["Num momento calmo, mostre o cantinho: “this is our calm-down corner”.", "Sentem juntas e diga o que se faz lá: “we sit, we breathe, we hug”.", "Respirem: “smell the flower, blow the candle”.",
               "Fiquem o quanto ela quiser, e saiam quando ela disser."],
              ["This is our calm-down corner. Come sit with me.", "We sit. We breathe. We hug.", "Smell the flower. Blow the candle. All better."],
              ["Do you want to sit here?", "Do you want a hug?", "Are you calm now?"],
              "Visitar o cantinho nos momentos calmos, com as mesmas frases, faz dele um lugar conhecido e gostoso. Não é castigo: vocês vão juntas, e ela sai quando quiser. "
              "As frases (“we sit, we breathe, we hug”) são curtas e podem ser ditas no meio de uma crise, em voz baixa.",
              atencao="deixe fora do alcance dela a garrafa da calma, se houver; leve-a ao cantinho só quando estiverem juntas.",
              variar=["Leve um livro de figuras.", "Escolham juntas o bichinho do cantinho.", "Cantem baixinho uma rima calma."], registro=CAL)

    leitura(L, "When Sophie Gets Angry — Really, Really Angry…", "Molly Bang", "5 a 10 minutos",
            cena([("dedo_nao", 28, 12, 16), ("pegada", 18, 46, 10), ("arvore_verao", 30, 74, 10), ("coracao", 26, 112, 18), ("carinha_feliz", 26, 148, 18)], 46, 190),
            ["Leia numa hora calma, e não no meio da crise. Mostre a capa e o rosto de Sophie.", "Pergunte: “how does Sophie feel?”. Deixe que ela aponte as cores e o rosto.", "Mostre o que Sophie faz para se acalmar, e diga: “she goes outside”.",
             "No fim, “she feels better”: pergunte como ela se acalma."],
            ["Sophie is angry. Look at her face.", "She runs, she cries. Then she looks around.", "Now she feels better. Her family is happy."],
            ["How does Sophie feel?", "What does she do?", "What do you do when you're angry?"],
            "É um livro sobre a raiva e sobre como ela passa, e o livro de Molly Bang foi premiado (Caldecott Honor). Em leitura dialogada, as perguntas são sobre o rosto e as cores, que a criança entende, e sobre o que fazer, que ela mostra com o corpo. "
            "Leia depois que a crise passou, e nunca no meio dela. Se o livro parecer longo, leia só as páginas do meio.",
            variar=["Ela escolhe a cor da raiva do livro.", "Procure o lugar do livro no parque.", "Leia uma vez em português, para ela entender a história."])


# ================================================================== U8 BEDTIME

def unidade8(L):
    ativ = [("Brush, brush, brush", "corpo", "5 min"), ("Pajamas on", "maos", "10 min"), ("Good night to everything", "conversar", "5 min"), ("Whisper time", "conversar", "5 min"),
            ("Twinkle, twinkle, little star · Hush, little baby · Good night, sun · Brush your teeth", "cantar", "2 min cada"),
            ("Teddy breathing", "acalmar", "3 min"), ("Rock and hum", "acalmar", "5 min"), ("Goodnight Moon", "ler", "5 a 10 min")]
    abertura_unidade(L, 7,
                     "A hora de dormir é o último momento fixo de inglês do dia, e o mais calmo: a luz baixa, a voz baixa, as mesmas frases todas as noites. "
                     "Para uma criança que reage mal às trocas, uma sequência sempre igual, com um aviso antes (“five more minutes”), ajuda muito. As rimas, as de acalmar e o livro da hora de dormir fecham o caderno.",
                     ativ, cena([("lua", 28, 8, 12), ("estrela", 22, 42, 18), ("cama", 30, 72, 12), ("escova_dentes", 26, 110, 16), ("livro", 28, 148, 14)], 44, 190))

    atividade(L, "Brush, brush, brush", "corpo", "5 minutos",
              "escova de dentes, uma pasta com pouco flúor (um grão de arroz) e um copo",
              cena([("escova_dentes", 30, 12, 14), ("dente", 26, 48, 18), ("boca", 28, 82, 16), ("gota", 22, 118, 18), ("estrela", 22, 150, 20)], 46, 190),
              ["Mostre a escova: “toothbrush”, e uma pontinha de pasta: “a little bit”.", "Escovem juntas, no espelho: “brush, brush, brush the front, the back, the top”.", "“Open wide”: ela abre a boca, e você escova a dela, depois ela escova a sua.",
               "“Spit, spit”: cuspir a espuma; “rinse”; “all clean!”."],
              ["Time to brush our teeth. Open wide!", "Brush, brush, brush. Front, back, top.", "Spit, spit. All clean!"],
              ["Where are your teeth?", "Can you open wide?", "Are your teeth clean?"],
              "Escovar os dentes é um ritual da hora de dormir, e as palavras (teeth, brush, open wide, spit) vêm com o gesto. Com 2 anos, a criança ainda precisa que o adulto escove, e brincar de trocar (ela escova o adulto) dá a ela o papel de quem faz.",
              atencao=AGUA + " Pasta só uma pontinha, do tamanho de um grão de arroz; fique junto e sem deixar que ela engula a espuma.",
              variar=["Escove o dente do ursinho.", "Cantem a rima desta unidade.", "Ela escolhe a cor da escova."])

    atividade(L, "Pajamas on", "maos", "10 minutos",
              "o pijama e o ursinho",
              cena([("luva", 28, 12, 16), ("gorro", 28, 46, 16), ("casaco", 30, 82, 12), ("cama", 30, 118, 14), ("lua", 22, 154, 18)], 46, 190),
              ["Avise antes: “five more minutes, then pajamas”.", "Dê uma escolha: “the blue pajamas or the yellow ones?”.", "Diga cada peça ao vestir: “arms in”, “head through”, “legs in”.",
               "No fim: “all dressed! Now we're cozy”."],
              ["Five more minutes. Then pajamas.", "Blue or yellow? You choose.", "Arms in. Head through. All dressed!"],
              ["Which pajamas do you want?", "Where are your arms?", "Are you cozy?"],
              "Trocar de roupa para dormir é uma troca que pode gerar “não”. Um aviso antes, uma escolha entre duas coisas e uma sequência de palavras sempre iguais ajudam a criança a aceitar. Se ela recusar, diga “okay, then pajamas in two minutes”, e cumpra.",
              variar=["Vista o ursinho primeiro.", "Uma peça por noite em inglês.", "Cantem “pajamas on”."])

    atividade(L, "Good night to everything", "conversar", "5 minutos",
              "o quarto, com a luz baixa",
              cena([("lua", 30, 12, 12), ("estrela", 24, 46, 18), ("janela_sol", 28, 80, 14), ("cama", 30, 114, 14), ("coracao", 24, 150, 18)], 46, 190),
              ["Fiquem na porta, ou junto da cama, com a luz baixa.", "Diga boa-noite a tudo o que vê: “good night, sun”, “good night, moon”, “good night, window”.", "Deixe que ela escolha o próximo: “what's next?”.",
               "Termine com “good night, Marina. I love you.”."],
              ["Good night, sun. Good night, moon.", "Good night, window. Good night, bed.", "Good night, Marina. I love you."],
              ["Who is next?", "Is the moon sleepy?", "Can you say good night?"],
              "Um ritual de despedida, sempre igual e com a voz baixa, marca o fim do dia e ajuda a criança a se soltar do que a agitou. O livro *Goodnight Moon* faz o mesmo; aqui o ritual é seu e do quarto dela, e não reproduz o livro. "
              "As palavras (sun, moon, window, bed) vêm com o objeto na mão.",
              variar=["Boa-noite aos bichos de pelúcia.", "Um beijo para cada coisa.", "Em vez de “good night”, diga “sleep tight”."])

    atividade(L, "Whisper time", "conversar", "5 minutos",
              "o quarto, com a luz baixa e o ursinho",
              cena([("cama", 32, 12, 14), ("boca", 26, 48, 18), ("orelha", 26, 82, 18), ("estrela", 22, 116, 20), ("lua", 24, 150, 16)], 46, 190),
              ["Deitem e fale em voz de sussurro: “let's whisper”.", "Conte uma coisa boa do dia, em uma frase: “we played in the park”.", "Peça uma coisa a ela: “tell me one nice thing”. Aceite uma palavra.",
               "Termine com um sussurro: “sleep tight”."],
              ["Shh, let's whisper.", "Today we played in the park. That was fun.", "Tell me one nice thing. Sleep tight."],
              ["What was fun?", "Who did we see?", "Are you sleepy?"],
              "Falar em sussurro é um ótimo jeito de baixar o ritmo, e contar uma coisa boa do dia, em uma frase, treina a memória e termina o dia em paz. Em inglês, a frase é sempre a mesma, e ela a reconhece. "
              "Se ela não quiser falar, só escute: o silêncio também vale.",
              variar=["Conte três coisas: “first, then, last”.", "Sussurre no ouvido do ursinho.", "Ela conta uma coisa só, em português: repita em inglês."])

    rimas(L, "Para a hora de dormir", [
        dict(t="Twinkle, twinkle, little star", linhas=["Twinkle, twinkle, little star,", "how I wonder what you are!", "Up above the world so high,", "like a diamond in the sky."],
             gesto="abra e feche as mãos como estrelas que piscam, e aponte o céu em “up above”. Cante bem baixinho.", origem="Poema de Jane Taylor (1806), em domínio público; melodia tradicional.", motivos=["estrela", "lua"]),
        dict(t="Hush, little baby", linhas=["Hush, little baby, don't say a word,", "Mama's gonna buy you a mockingbird.", "And if that mockingbird won't sing,", "Mama's gonna buy you a diamond ring."],
             gesto="balance a criança no colo, devagar, no ritmo da cantiga; no fim, cantarole. É uma canção de ninar tradicional, com muitas versões.", origem="Canção de ninar tradicional dos Estados Unidos, de autoria desconhecida e em domínio público.", motivos=["cama", "cuco"])],
        "Canções de ninar cantadas baixinho, balançando, são uma das formas mais antigas de acalmar uma criança, e em inglês elas são tão boas quanto em português. A mesma canção, todas as noites, vira o sinal de que o dia acabou.")

    rimas(L, "Boa-noite e escovar os dentes", [
        dict(t="Good night, sun", linhas=["Good night, sun, good night, sky,", "good night, birdie flying by;", "good night, moon, good night, star,", "good night, Marina, here you are."],
             gesto="aponte cada coisa pela janela, ou no teto, e diga boa-noite; no último verso, abrace-a ou beije-a. Troque “Marina” pelo nome do bichinho, se quiser.", origem=COLECAO, motivos=["lua", "estrela"]),
        dict(t="Brush your teeth", linhas=["Brush, brush, brush your teeth,", "up and down and round;", "front and back and top and bottom,", "make a happy sound!"],
             gesto="escovem os dentes juntas, no ritmo da rima: para cima, para baixo, em volta. No “happy sound”, façam “ahh”, boca bem aberta.", origem=COLECAO, motivos=["escova_dentes", "dente"])],
        "As rimas da coleção para a hora de dormir têm só as palavras do quarto e do banheiro, com ritmo. A de escovar os dentes dá um tempo à escovação (cerca de um minuto), e a de boa-noite fecha o dia da mesma maneira, todas as noites.")

    atividade(L, "Teddy breathing", "acalmar", "3 minutos",
              "um ursinho leve, e uma cama ou um tapete macio",
              cena([("cama", 36, 12, 12), ("coracao", 26, 52, 18), ("lebre", 26, 86, 18), ("lua", 24, 120, 16), ("estrela", 22, 154, 18)], 46, 190),
              ["Deitem de barriga para cima. Ponha o ursinho na barriga dela.", "Diga “breathe in… the bear goes up”; “breathe out… the bear goes down”.", "Faça junto, com o seu ursinho (ou a mão) na sua barriga.",
               "Repitam cinco vezes, e terminem com um abraço no ursinho."],
              ["Breathe in… the bear goes up.", "Breathe out… the bear goes down.", "Again. Nice and slow. Sleepy bear."],
              ["Is the bear going up?", "And now going down?", "Are you sleepy?"],
              "Ver o ursinho subir e descer faz a respiração virar algo que ela vê e sente, e a respiração pela barriga é a mais calma. É uma atividade clássica de respiração para crianças pequenas, e a frase de “up” e “down” liga ao que ela já aprendeu na unidade de brincar.",
              atencao="o ursinho fica só na barriga, nunca no rosto ou no pescoço; leve e sem peças soltas.",
              variar=["Deitem lado a lado, cada uma com um ursinho.", "Cantarolem “hmm” ao soltar o ar.", "Faça de folha: “up and down with the wind”."], registro=CAL)

    atividade(L, "Rock and hum", "acalmar", "5 minutos",
              "o colo ou uma cadeira de balanço; luz baixa",
              cena([("cama", 34, 12, 12), ("lua", 26, 50, 16), ("estrela", 22, 84, 18), ("coracao", 26, 118, 18), ("maos_juntas", 28, 152, 16)], 46, 190),
              ["Sente com ela no colo e balance devagar de um lado para o outro.", "Cantarole sem letra, ou cante baixinho “Hush, little baby”.", "Diga, sussurrando: “you're safe. I'm here.”.",
               "Quando o corpo dela amolecer, vá parando de balançar até ficarem paradas."],
              ["Hush, little baby. I'm here.", "You're safe. Shh, shh.", "Sleep tight, my love."],
              ["Are you cozy?", "Do you want one more song?", "Are you sleepy?"],
              "Balançar num ritmo regular e cantarolar é uma das formas mais antigas de acalmar uma criança, e dizer “I'm here” a faz saber que alguém está perto. Pode ser usada depois de uma crise, quando ela precisa de colo. "
              "Em dias de “não”, o colo no fim do dia é um jeito de fazer as pazes.",
              variar=["Só cantarole, sem letra.", "Cante o nome dela no lugar da palavra “baby”.", "Deitadas, com a mão dela no seu peito."], registro=CAL)

    leitura(L, "Goodnight Moon", "Margaret Wise Brown e Clement Hurd", "5 a 10 minutos",
            cena([("lua", 30, 12, 12), ("cama", 32, 48, 14), ("janela_sol", 28, 84, 16), ("lampada", 24, 118, 18), ("lebre", 26, 150, 18)], 46, 190),
            ["Sentem juntas, com a luz baixa, e leia devagar e baixinho.", "Aponte as coisas do quarto do livro e procure as mesmas no quarto dela: “where is the moon?”.", "Deixe que ela vire a página e diga boa-noite a cada coisa.",
             "Leia sempre o mesmo livro, na mesma hora."],
            ["Look, the great green room. Where is the moon?", "Good night, moon. Good night, stars.", "Now it's time to sleep."],
            ["Where is the moon?", "What do you see in the room?", "Can you say good night?"],
            "É o livro de dormir mais conhecido em inglês, e a leitura dialogada (Whitehurst) funciona aqui por procurar, no livro e no quarto, as coisas que se dizem. A repetição (o mesmo livro, todas as noites) é o que o torna um ritual, e um ritual ajuda a acalmar antes do sono. "
            "O texto está sob direitos autorais; compre ou tome emprestado.",
            variar=["Procure o camundongo em cada página.", "Leia só até a metade, se ela dormir.", "Termine com o “good night, [name]”."])


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    L.inicio["Encerramento"] = L.proximo
    linhas = "".join('<tr><td style="height:15mm;width:24mm"></td><td></td><td></td><td></td></tr>' for _ in range(11))
    c = f"""<div class="miolo">{titulo("O inglês da Marina", "um registro, para o adulto preencher", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["sol", "mao", "cesta", "lua"], "17mm", "5mm")}</div>
      <table class="tab" style="margin-top:3mm"><tr><th>Data</th><th>O que fizemos</th><th>O que ela disse ou fez</th><th>O que ajudou</th></tr>{linhas}</table></div>
      {adulto("registrar", "Anote, sem julgar: a atividade, o que ela entendeu (apontou, imitou, riu), uma palavra nova que ela disse (em qualquer língua), e o que ajudou quando ela disse “não”. Em algumas semanas você vê o que funciona <b>para ela</b>. "
              "Se tiver dúvidas sobre fala, audição ou comportamento, leve este registro ao pediatra ou a uma fonoaudióloga que acompanhe crianças bilíngues.")}"""
    L.add(c, aba="--d-ingles")

    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Fontes e créditos</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">De onde vêm as ideias e as rimas</h1>
      <h2>Métodos</h2>
      <p>Entrada compreensível (Stephen Krashen e Tracy Terrell, <i>The Natural Approach</i>); Resposta Física Total (James Asher); língua por hora e lugar, em famílias bilíngues (François Grosjean); leitura dialogada (Grover Whitehurst); e, para o tempo ao ar livre, os sentidos e os hábitos, Charlotte Mason.
      <b>São inspirações, não regras:</b> as buscas trouxeram manuais, resumos e páginas de divulgação, e não os textos originais, e quase nada específico sobre crianças de 2 anos. Este caderno não promete fluência. Confira as orientações sobre a fase do “não” e a atenção curta com o pediatra da Marina (ADR 0026).</p>
      <h2>Rimas e cantigas</h2>
      <p><b>Tradicionais inglesas e norte-americanas, de autoria desconhecida e em domínio público:</b> <i>Open, shut them</i>; <i>This little piggy</i>; <i>Rub-a-dub-dub</i>; <i>Pease porridge hot</i>; <i>Hot cross buns</i>; <i>Jack be nimble</i>; <i>One, two, buckle my shoe</i>;
      <i>The Grand Old Duke of York</i>; <i>Rain, rain, go away</i>; <i>Round and round the garden</i>; <i>Itsy Bitsy Spider</i>; <i>Baa, baa, black sheep</i>; <i>Hey diddle diddle</i>; <i>Hickory dickory dock</i>; <i>Here we go round the mulberry bush</i>; <i>Tommy Thumb</i>; <i>Hush, little baby</i> (canção de ninar dos Estados Unidos). A letra pode variar da que você conhece.</p>
      <p><b>Com autoria conhecida, em domínio público:</b> <i>Good morning to you</i> (“Good Morning to All”, de Patty Smith Hill e Mildred J. Hill, 1893); <i>Twinkle, twinkle, little star</i> (Jane Taylor, 1806); <i>Mary had a little lamb</i> (Sarah Josepha Hale, 1830); <i>Row, row, row your boat</i> (letra de 1852).</p>
      <p><b>Escritas pela coleção:</b> <i>Sun is up</i>; <i>Splash, splash, splash</i>; <i>Yum, yum, yum</i>; <i>Wash your hands</i>; <i>Stomp, stomp, stomp</i>; <i>Look around</i>; <i>Happy, sad, angry, sleepy</i>; <i>I can do it</i>; <i>Soft hands</i>; <i>Good night, sun</i>; <i>Brush your teeth</i>.</p>
      <h2>Livros</h2>
      <p>Os livros indicados estão sob direitos autorais e não são reproduzidos aqui: o caderno os indica pelo título e diz como conversar sobre cada um. Procure-os em biblioteca, livraria ou sebo.</p>
      <h2>Ilustração</h2>
      <p>Todas as figuras são motivos em aquarela da coleção. Nenhum dado de criança ou de família é coletado ou enviado.</p>""")

    c = f"""<div class="miolo centro" style="top:60mm">
      <div style="font-size:11pt;letter-spacing:.3em;text-transform:uppercase;color:var(--sepia)">See you soon</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0" lang="en">Good night, Marina</div>
      <div class="vinheta-sep">❦</div>
      <p style="font-size:13pt;font-style:italic;color:var(--sepia);max-width:120mm;margin:6mm auto">O português é a língua dela; o inglês é o seu jeito de brincar. Quando ela disser “não”, volte ao português. Quando ela disser “de novo”, repita.</p>
      <div style="margin:10mm auto 0">{tira(["sol", "mao", "cesta", "bolhas", "lua"], "20mm", "3mm")}</div></div>"""
    L.add(c, cabecalho=False, numero=False)


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8)


def montar(unidades=None):
    L = CadernoIngles()
    capa(L); rosto(L); carta(L); como_funciona(L)
    frases(L)
    livros(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidades or UNIDADES_PRONTAS):
        u(L)
    if not unidades:
        encerramento(L)
    num, _ = L.paginas[n_sum - 1]
    L.paginas[n_sum - 1] = (num, f'<section class="pagina"><div class="moldura"></div>{sumario(L.inicio)}'
                                 f'<div class="rodape"><span class="num">{num}</span></div></section>')
    return L


def main():
    os.makedirs(SAIDA, exist_ok=True)
    ok = True
    for versao, nome in (("impressao", "caderno-ingles-impressao"), ("tela", "caderno-ingles-tela")):
        VERSAO["atual"] = versao
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "caderno-ingles-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
