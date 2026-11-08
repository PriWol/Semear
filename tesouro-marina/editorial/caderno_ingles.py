"""
CADERNO DE INGLÊS DA MARINA (2 anos) — para quem fala inglês com ela em casa; a língua materna dela é o português.
uso: python3 caderno_ingles.py            (monta o caderno com as unidades já escritas; ver UNIDADES_PRONTAS)
Métodos: entrada compreensível (Krashen e Terrell, Natural Approach), Resposta Física Total (Asher), língua por hora e lugar (Grosjean) com um falante de inglês,
leitura dialogada (Whitehurst) e rimas e cantigas de domínio público. O adulto fala inglês; o texto de apoio é em português. Sem tela. Ver ADR 0022.
As páginas e os blocos são os do caderno de atividades (caderno.py); aqui ficam só o conteúdo e a ordem.
"""
import os
import subprocess
import sys

import caderno
from caderno import (CAL, COLECAO, DOMPUB, ICONES, TIPOS, adulto, atividade, bloco, cena, etiqueta, falas, gerar_pdf, passos_txt, rimas, texto, tira, titulo, img)
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
INICIO = {}
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
    INICIO[L.unidade] = L.proximo


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
        <tr><td style="width:7mm"></td><td><b lang="en">Brown Bear, Brown Bear, What Do You See?</b> — Bill Martin Jr. e Eric Carle<br><span class="peq">repetição, cores e bichos: ótimo para a unidade 1</span></td></tr>
        <tr><td></td><td><b lang="en">Pat the Bunny</b> — Dorothy Kunhardt<br><span class="peq">livro de tocar, rotina de brincar</span></td></tr>
        <tr><td></td><td><b lang="en">Where Is Baby's Belly Button?</b> — Karen Katz<br><span class="peq">partes do corpo, “peekaboo”</span></td></tr>
        <tr><td></td><td><b lang="en">Dear Zoo</b> — Rod Campbell<br><span class="peq">bichos, abas para abrir</span></td></tr>
        <tr><td></td><td><b lang="en">From Head to Toe</b> — Eric Carle<br><span class="peq">gestos do corpo, no estilo da Resposta Física Total</span></td></tr>
        <tr><td></td><td><b lang="en">Hands Are Not for Hitting</b> — Martine Agassi<br><span class="peq">para a fase do “não”: o que se pode fazer com as mãos</span></td></tr>
        <tr><td></td><td><b lang="en">When Sophie Gets Angry — Really, Really Angry…</b> — Molly Bang<br><span class="peq">raiva e como ela passa, para ler depois que a crise passou</span></td></tr>
        <tr><td></td><td><b lang="en">Goodnight Moon</b> — Margaret Wise Brown e Clement Hurd<br><span class="peq">hora de dormir, para a unidade 8</span></td></tr>
        <tr><td></td><td><b lang="en">Time for Bed</b> — Mem Fox e Jane Dyer<br><span class="peq">hora de dormir, rima e repetição</span></td></tr>
        <tr><td></td><td><b lang="en">The Very Hungry Caterpillar</b> — Eric Carle<br><span class="peq">dias da semana, comida e bichos</span></td></tr>
      </table></div>
      {adulto("como ler", "O caderno não reproduz nenhum desses livros, só os indica pelo título e diz como conversar sobre cada um. Leia com ela no colo, devagar, apontando; deixe que ela vire a página. Se ela quiser ler o mesmo livro cem vezes, melhor: faça perguntas diferentes a cada vez. Os livros são de autores contemporâneos e estão sob direitos autorais: compre ou tome emprestado.")}"""
    L.add(c, aba="--d-historias")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt"><i lang="en">{n.split(" · ", 1)[1]}</i><br><span class="peq">{sub}</span></td><td class="pg">{inicio.get(n, "")}</td></tr>'
                     for n, sub, cor in UNIDADES)
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


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1,)


def montar(unidades=None):
    L = CadernoIngles()
    capa(L); rosto(L); carta(L); como_funciona(L)
    frases(L)
    livros(L)
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
    for versao, nome in (("impressao", "caderno-ingles-impressao"), ("tela", "caderno-ingles-tela")):
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "caderno-ingles-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
