"""
CADERNO DE ATIVIDADES DA MARINA (2 anos) — acompanha os oito volumes de O Grande Tesouro de Marina.
uso: python3 caderno.py            (monta o caderno com as unidades já escritas; ver UNIDADES_PRONTAS)
Uma unidade por volume, com várias atividades curtas. Nada de papel e caneta como centro: o caderno mistura sete tipos de atividade
(cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo, nomear e acalmar). Sem tela. Ilustrações: motivos em aquarela da coleção.
Rimas e cantigas: só as tradicionais de autoria desconhecida ou de domínio público (a letra varia de região para região) e as escritas pela coleção; ver ADR 0021.
"""
import os
import subprocess
import sys

from livro import Livro, VERSAO, adulto, gerar_pdf, img, texto, titulo
from volume6 import cena as _cena, tira   # composição de motivos em posição livre e fila de motivos: os mesmos dos outros volumes


def cena(itens, h=80, w=170):
    """Como a cena do Volume 6, mas centrada na coluna de 174 mm (uma cena mais larga que a coluna começaria na margem esquerda e passaria da área segura à direita)."""
    return f'<div style="margin-left:{(174 - w) / 2:.1f}mm">{_cena(itens, h, w)}</div>'

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
    "acalmar": ("Acalmar", "--d-frances", "bolhas"),
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




def rimas(L, t, itens, porque, tipo="cantar"):
    """Uma página com duas rimas ou cantigas curtas. itens: dicts com t, linhas, gesto, origem, motivos."""
    nome, cor, _ = TIPOS[tipo]
    blocos = ""
    for it in itens:
        versos = "<br>".join(it["linhas"])
        blocos += f"""<div style="margin-top:4mm;padding-top:3mm;border-top:0.4pt solid var(--linha)">
          <div class="centro" style="line-height:0">{tira(it["motivos"], "17mm", "3mm")}</div>
          <h2 class="titulo" style="font-size:17pt;text-align:center;margin:2mm 0 1mm">{it["t"]}</h2>
          <p style="font-size:{16 if len(itens) == 1 else 14}pt;line-height:1.42;text-align:center;font-style:italic;margin:1mm 0 2mm">{versos}</p>
          <div style="font-size:11.4pt;line-height:1.35"><b>O gesto:</b> {it["gesto"]}</div>
          <div class="peq" style="margin-top:1.2mm">{it["origem"]}</div></div>"""
    c = f"""<div class="miolo">
      <div class="centro" style="margin-top:1mm">{etiqueta(tipo)}</div>
      {titulo(t, None, 24)}{blocos}</div>
      {adulto("por que isto importa", porque)}"""
    return L.add(c, aba=cor)


TRAD = "Rima tradicional brasileira, de autoria desconhecida; a letra varia de região para região."
DOMPUB = "Cantiga de domínio público; a letra tem pequenas variações."
COLECAO = "Rima escrita pela coleção."
CAL = "Hoje o que ajudou a Marina a se acalmar foi… — data: ______"
# ================================================================== ABERTURA

ICONES = ["tambor", "livro", "folha", "mao", "pegada", "cesta", "bolhas"]


def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Caderno de atividades · 2 anos</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">Para brincar,<br>cantar, acalmar<br>e olhar o mundo</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:148mm;left:0;right:0">{cena([("cesta", 46, 8, 22), ("folha", 30, 60, 6), ("mao", 34, 96, 20), ("poca", 44, 126, 40), ("bota", 28, 64, 56), ("sol", 30, 140, 0), ("bolhas", 30, 24, 66)], 100)}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(ICONES, "13mm", "2mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Caderno de atividades</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">para a Marina, aos 2 anos</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">Este caderno é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(ICONES, "20mm", "2mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Aos dois anos, aprender é viver junto</h1>
      <p>Os volumes da coleção foram escritos para crianças de 3 a 8 anos. A Marina tem 2, e nessa idade o aprendizado não está no papel: está em <b>ser carregada até a janela e
      ouvir o nome das coisas</b>, em repetir a mesma rima cem vezes, em despejar água de um copo no outro, em pular numa poça. Este caderno acompanha cada volume com atividades
      para essa idade, e <b>quase nenhuma usa papel e lápis</b>.</p>
      <h2>Sete tipos de atividade</h2>
      <p>Cantar e rimar, conversar, mostrar o mundo, fazer com as mãos, mexer o corpo, nomear e <b>acalmar</b>. Cada unidade tem rimas e parlendas, atividades curtas e pelo menos duas
      atividades para os momentos em que o dia está difícil. Cada página termina com uma nota para o adulto sobre por que aquilo importa.</p>
      <h2>Quatro ideias que guiam o caderno</h2>
      <ul>
        <li><b>Curto e repetido.</b> De 2 a 10 minutos. Nessa idade a atenção é curta, e cresce aos poucos; repetir a mesma atividade é o jeito de aprender, e não sinal de que ela “acabou”.</li>
        <li><b>Você fala, ela mostra.</b> Frases curtas, devagar, e espere uns 5 segundos. Repita o que ela quis dizer e acrescente um pouco: ela diz “au-au” e você responde “sim, o cachorro está latindo!”.</li>
        <li><b>Coisas de verdade e gente de verdade.</b> A colher é a colher da cozinha; a folha é a folha do quintal. Rima, toque, colo e olhar fazem mais que qualquer tela:
        a Sociedade Brasileira de Pediatria não recomenda telas antes dos 2 anos e pede, depois disso, pouco tempo e acompanhado. Este caderno não usa tela.</li>
        <li><b>A calma se treina quando está tudo bem.</b> É nessa idade que aparece a fase do “não” e vêm as emoções grandes. As atividades de acalmar são para brincar nos momentos tranquilos,
        para que ela já conheça o jeito quando o dia ficar difícil. Veja as próximas páginas.</li>
      </ul>
      <h2>Cuidados</h2>
      <p>Nada de peça pequena que caiba na boca (engasgo). Água, mesmo rasa, só com um adulto junto o tempo todo. Se ela não quiser, pare e tente outro dia. Este caderno não é avaliação nem faz diagnóstico:
      se você tiver dúvidas sobre fala, audição, comportamento ou desenvolvimento, converse com o pediatra.</p>
      <div class="centro" style="margin-top:5mm">""" + tira(ICONES, "18mm", "2mm") + "</div>")


def fase_do_nao(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Para o adulto · 1 de 2</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">A fase do “não”</h1>
      <p>Entre um ano e meio e três ou quatro anos é muito comum a criança dizer “não” a tudo, querer fazer sozinha, testar limites e ter birras. A Sociedade Brasileira de Pediatria chama de
      “crise dos dois anos”. Ela está descobrindo que é uma pessoa, com vontades próprias, mas ainda tem poucos recursos para lidar com frustração e emoções fortes.
      <b>Não é “mau comportamento” nem sinal de que alguém errou.</b> Em vez de um rótulo (“geniosa”, “teimosa”), vale descrever o momento: “agora você está com muita raiva”.</p>
      <h2>O que ajuda no dia a dia</h2>
      <ol style="line-height:1.4">
        <li><b>Olhar fome, sono e cansaço primeiro.</b> Eles pioram quase toda birra. Uma rotina previsível (comer, brincar, dormir, nas mesmas horas) ajuda.</li>
        <li><b>Avisar antes de trocar de atividade.</b> “Mais cinco pulos e vamos tomar banho.” Uma rima fixa para cada troca ajuda muito: o caderno traz a das mãos sujas.</li>
        <li><b>Dar escolha entre duas coisas que você aceita:</b> “copo azul ou copo verde?”. Ela ganha um pouco de controle, e você mantém o essencial. Não pergunte “quer?” quando a resposta não pode ser “não”.</li>
        <li><b>Dizer o que pode, e não só o que não pode.</b> Em vez de “não sobe na mesa”: “os pés ficam no chão; se quiser subir, vamos ao banquinho”.</li>
        <li><b>Dar nome ao sentimento, sem ceder ao que foi pedido.</b> “Você está brava porque acabou o passeio. Eu entendo. Amanhã a gente volta.” O limite continua, o sentimento é aceito.</li>
        <li><b>Dar pequenas tarefas de verdade:</b> levar o prato, regar a planta, escolher a meia. Muita birra vem de querer escolher e não poder.</li>
        <li><b>Brincar de acalmar quando está tudo bem:</b> sopro, bolhas, balanço, cantiga baixinha. Na hora difícil, ela e você já conhecem o caminho.</li>
      </ol>
      <div class="centro" style="margin-top:6mm">""" + tira(["dedo_nao", "coracao", "bolhas", "carinha_feliz", "maos_juntas"], "20mm", "3mm") + "</div>")
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Para o adulto · 2 de 2</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Na hora da crise, e quando ela não aguenta ficar</h1>
      <h2>Durante a birra</h2>
      <ul style="line-height:1.4">
        <li>Fique perto, em segurança, e <b>fale baixo e pouco</b>. Argumentar no meio da crise não funciona: ela ainda não consegue ouvir.</li>
        <li>Se for num lugar com gente olhando, leve-a para um canto sem plateia.</li>
        <li>Sem gritos, sem ameaças e sem castigo físico. O “cantinho da calma” não é castigo: vocês vão juntas, e ela sai quando quiser.</li>
        <li>Quando a crise passar, um abraço e uma frase: “você estava muito brava, e agora passou”. Só então volte ao assunto, em uma frase.</li>
        <li>Cuide de você: respire fundo antes de responder. A calma do adulto é o que ela “pega”.</li>
      </ul>
      <h2>Atenção curta</h2>
      <p>Nessa idade, ficar poucos minutos numa mesma atividade é normal, e dura mais quando é uma coisa de que ela gosta. Comece pelas atividades que ela já mostrou interesse, deixe poucos brinquedos à vista,
      combine uma “versão de 2 minutos” e deixe crescer devagar. Se ela soltar a atividade, tudo bem: guarde para outro dia.</p>
      <h2>Quando conversar com o pediatra</h2>
      <p>Procure o pediatra se as birras ficarem <b>muito longas, muito frequentes ou muito intensas</b>; se ela se machucar ou machucar os outros; se perder uma habilidade que já tinha; se a dificuldade continuar
      ou piorar depois dos 4 anos; ou se você sentir que não está dando conta. <b>Este caderno não faz diagnóstico e não substitui o pediatra</b>; é só um conjunto de brincadeiras de apoio.</p>
      <p class="peq" style="margin-top:4mm">Base: orientações da SBP sobre a “crise dos dois anos” e materiais de pediatras e de associações de pais e de psiquiatria infantil (ver ADR 0021).
      Faixas e prazos variam de uma fonte para outra: vale conferir com o pediatra da Marina.</p>
      <div class="centro" style="margin-top:4mm">""" + tira(["estrela", "lua", "estrela"], "18mm", "6mm") + "</div>")


def cantinho_calma(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Para o adulto · preparar</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">O cantinho da calma</h1>
      <div class="centro" style="margin:2mm 0 4mm">{cena([("cama", 36, 8, 6), ("livro", 30, 52, 12), ("bolhas", 34, 92, 6), ("estrela", 24, 136, 10), ("jarra", 26, 62, 38)], 56, 190)}</div>
      <p>Um canto pequeno e macio, <b>escolhido junto com ela</b>: uma manta, uma almofada, um bichinho e duas ou três coisas calmas. Não é lugar de castigo e não é só para a hora difícil:
      comece a usar quando estiver tudo bem, para que ela o conheça como um lugar gostoso.</p>
      <h2>O que pôr nele</h2>
      <ul>
        <li>um bichinho ou pano macio;</li>
        <li>um livro de figuras e a garrafa da calma (receita abaixo);</li>
        <li>um cata-vento ou bolhas de sabão, para soprar devagar (o adulto fica por perto);</li>
        <li>uma foto da família, ou uma almofada que cheire a casa.</li>
      </ul>
      <h2>A garrafa da calma</h2>
      <p>Garrafa de plástico transparente e pequena, quase cheia de água morna, com uma colher de cola líquida transparente e uma colher de glitter grosso. <b>O adulto fecha a tampa com cola quente e fita</b>,
      testa se não vaza e <b>só deixa a criança usar com você por perto</b>. Chacoalhar e olhar o glitter descer devagar é um jeito de respirar mais lento. Não serve para mastigar nem para jogar.</p>
      <h2>Como usar</h2>
      <p>“Quer ir ao cantinho? Eu vou com você.” Sentem juntas, respirem devagar, e deixe que ela escolha o que quer segurar. Saiam quando ela quiser.</p>""")


def como_usar(L):
    linhas = "".join(
        f'<tr><td style="width:24mm;text-align:center">{img(m, "13mm")}</td><td><b>{nome}</b><br><span style="font-size:10pt">{exemplo}</span></td></tr>'
        for (nome, _, m), exemplo in zip(TIPOS.values(), (
            "Parlendas, cantigas e jogos de dedos, sempre com um gesto junto.",
            "Falar do que se vê e do que se faz; esperar a vez dela; contar o dia.",
            "Passear, apresentar um bicho, uma planta, um lugar: o mundo de verdade.",
            "Água, terra, massa, tecidos, panelas: tocar, despejar, misturar.",
            "Pular, andar devagar e rápido, dançar, esconder, equilibrar.",
            "Dizer o nome de objetos reais, numa cesta ou num passeio.",
            "Respirar, soprar, balançar, olhar devagar: brincadeiras para os momentos calmos.")))
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este caderno</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:3mm">Um caderno para abrir de vez em quando</h1>
      <table class="tab">{linhas}</table>
      <h2>Ritmo</h2>
      <p>Uma ou duas atividades por dia bastam, e dias sem nenhuma também valem. O caderno tem uma unidade para cada volume da coleção: use a unidade do volume que a família estiver
      lendo, e volte às outras quando quiser. Não é preciso seguir a ordem. As rimas valem em qualquer hora: na fila, no carro, na troca de roupa.</p>
      <h2>Quando ela perder o interesse, ou disser “não”</h2>
      <p>Pare, sem insistir. Guarde para outro dia, ou mude de tipo: troque uma atividade de mãos por uma de corpo, ou por uma de acalmar. Se a atividade for boa, ela vai pedir de novo.
      Se a resposta for “não” e você puder aceitar, aceite: assim o “não” dela ganha valor, e o seu também.</p>
      <div class="centro" style="margin-top:5mm">{tira(["folha", "gota", "mao", "tambor", "estrela"], "20mm", "2.5mm")}</div>""")


def semana(L):
    dias = (("Segunda", "A cesta de tesouros", "Passeio dos cinco sentidos", "O dia em três tempos"),
            ("Terça", "Bom dia, sol · Mindinho", "Estátua", "Cheirar a flor, soprar a vela"),
            ("Quarta", "Pintar com o dedo", "Caça-folhas", "Boa noite em três línguas"),
            ("Quinta", "Voz de bicho", "Pular a poça", "Balançar e cantar baixinho"),
            ("Sexta", "Massinha de farinha", "Minha vez, sua vez", "Respirar com o bichinho"),
            ("Sábado", "Esconde-esconde", "Bichinho de perto", "Deitar e olhar as nuvens"),
            ("Domingo", "Um, dois, feijão com arroz", "Dançar e derreter", "Uma história de ninar"))
    linhas = "".join(f'<tr><td style="height:19mm;width:24mm"><b>{d}</b></td><td style="font-size:11pt">{a}</td><td style="font-size:11pt">{b}</td><td style="font-size:11pt">{c}</td></tr>' for d, a, b, c in dias)
    c = f"""<div class="miolo">{titulo("Uma semana de exemplo", "só uma sugestão: pule, troque, repita", 26)}
      <table class="tab" style="margin-top:4mm"><tr><th>Dia</th><th>De manhã</th><th>À tarde</th><th>Antes de dormir</th></tr>{linhas}</table>
      <div class="centro" style="margin-top:5mm">{tira(["sol", "folha", "lua"], "18mm", "8mm")}</div></div>
      {adulto("montar a sua semana", "A ideia é misturar os tipos: de manhã uma atividade de mãos, de corpo ou de nomear; à tarde, o mundo lá fora; e, antes de dormir, uma de acalmar. Uma rima serve para qualquer hora, e para as trocas (hora de sair, hora de lavar as mãos). Use só o que fizer sentido, e deixe dias sem nenhuma.")}"""
    L.add(c, aba="--d-vida")



def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}<br><span class="peq">{vol}</span></td><td class="pg">{inicio.get(n, "")}</td></tr>'
                     for n, vol, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Registro, fontes e créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Caderno de atividades · 2 anos", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(ICONES, "18mm", "1.5mm")}</div></div>"""


def abertura_unidade(L, i, intro, atividades, cena_html):
    """Página de abertura de uma unidade: a ligação com o volume e a lista de atividades."""
    nome, vol, cor = UNIDADES[i]
    inicio_unidade(L, i)
    itens = "".join(f'<tr><td style="width:7mm"><span class="bolinha" style="background:var({TIPOS[tp][1]})"></span></td>'
                    f'<td style="font-size:12.2pt"><b>{t}</b><br><span class="peq">{TIPOS[tp][0]} · {tempo}</span></td></tr>' for t, tp, tempo in atividades)
    c = f"""<div class="miolo">
      <div class="centro peq versal" style="letter-spacing:.2em">{vol}</div>
      {titulo(nome, None, 26)}
      <div class="centro" style="margin:3mm 0">{cena_html}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">{intro}</p>
      <table class="sumario" style="margin-top:2mm">{itens}</table></div>"""
    return L.add(c, aba=cor)


# ================================================================== U1 OLHAR A CASA E O QUINTAL (Volume 1)

def unidade1(L):
    ativ = [("A cesta de tesouros", "nomear", "5 a 8 min"), ("Passeio dos cinco sentidos", "mundo", "10 min"),
            ("O que tem na janela?", "conversar", "3 a 5 min"), ("Água na bacia", "maos", "10 min"), ("Pular a poça", "corpo", "5 min"),
            ("Mindinho, seu vizinho · Borboletinha · Bom dia, sol", "cantar", "2 min cada, quantas vezes ela pedir"),
            ("Cheirar a flor, soprar a vela", "acalmar", "2 a 3 min"), ("Bolhas devagar", "acalmar", "5 min")]
    abertura_unidade(L, 0,
                     "No Volume 1 a Marina aprende a olhar a casa, o quintal, o céu e a água. Aos 2 anos, isso vira: <b>pegar, escutar, cheirar, nomear e pular</b>. "
                     "Cada atividade usa o que já existe em casa e pode ser repetida muitas vezes. Comece pela que parecer mais fácil no seu dia, e guarde as de acalmar para os momentos tranquilos.",
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



    rimas(L, "Duas rimas para o quintal", [
        dict(t="Borboletinha", linhas=["Borboletinha", "tá na cozinha", "fazendo chocolate", "para a madrinha.", "Poti, poti,", "perna de pau,", "olho de vidro", "e nariz de pica-pau, pau, pau."],
             gesto="junte os polegares e abra as mãos como asas, batendo devagar; em “poti, poti”, balance-a no joelho; no último “pau”, um beijo.", origem=TRAD, motivos=["borboleta", "colher"]),
        dict(t="Bom dia, sol", linhas=["Bom dia, sol, bom dia, céu,", "bom dia, nuvem de chapéu!", "Bom dia, pé, bom dia, mão,", "bom dia, Marina, de coração!"],
             gesto="estique os braços para o alto no “sol”, aponte o céu, depois toque o pé, a mão e o peito. Boa para a hora de acordar.", origem=COLECAO, motivos=["sol", "nuvem", "coracao"])],
        "Rimas curtas, sempre com um gesto, ensinam o ritmo da língua e dão à criança algo que ela pode pedir (“de novo!”). A do bom dia pode virar o ritual de acordar, e a repetição todos os dias é o que a torna calmante.")

    atividade(L, "Cheirar a flor, soprar a vela", "acalmar", "2 a 3 minutos",
              "nenhum (uma flor de verdade ou desenhada ajuda); a vela é só de faz de conta: o dedo erguido",
              cena([("flor_rosa", 34, 12, 8), ("vela", 22, 60, 20), ("nariz", 26, 96, 14), ("boca", 30, 134, 12)], 46, 190),
              ["Sentem de frente, num canto calmo, com você mais perto que de costume.", "“Cheira a flor”: inspire pelo nariz, devagar, de olhos fechados. “Sopra a vela”: sopre pela boca, bem comprido, com o dedo dela de vela.",
               "Faça junto, no mesmo ritmo, três vezes. Mostre o seu peito subindo e descendo.", "Termine com um abraço ou um “muito bem, respirador!”."],
              ["Cheira a flor… hmmm, que cheirinho.", "Agora sopra a vela… fuuuu. Bem devagar.", "Mais uma vez? Devagarinho."],
              ["Que cheiro tem a flor?", "A vela apagou?", "Como está o corpinho agora?"],
              "Soprar devagar, com um sopro longo, é o jeito mais simples de desacelerar o corpo. <b>Brinque quando ela está calma</b>: assim, na hora da raiva, basta dizer “vamos cheirar a flor?”. "
              "Não force: se ela recusar, respire você e deixe que ela observe.",
              variar=["Sopre uma pena ou um cata-vento, para ela ver o sopro.", "“Cheira a flor” e “sopra a sopa quente”, na hora de comer.", "Faça de dragão: sopro forte; depois de gatinho: sopro bem fraquinho."],
              registro=CAL)

    atividade(L, "Bolhas devagar", "acalmar", "5 minutos",
              "bolhas de sabão com varinha, e um lugar aberto ou o quintal",
              cena([("bolhas", 44, 14, 8), ("bolhas", 30, 66, 22), ("mao", 34, 108, 14), ("nuvem", 38, 148, 6)], 52, 190),
              ["Sopre uma bolha de cada vez, bem devagar, e deixe que ela estoure com o dedo.", "Pergunte: “bolha grande ou pequena?”. A grande vem de um sopro longo e lento.",
               "Depois deixe que ela tente soprar. Peça “bem devagar, como o vento”.", "Quando ela se cansar, guarde o frasco e fiquem olhando a última bolha subir."],
              ["Olha como ela sobe… devagar, devagar.", "Plof! Acabou. Vem outra.", "Uma bolha grande! Que sopro comprido!"],
              ["Onde está a bolha?", "Grande ou pequena?", "Quem estourou?"],
              "Seguir com os olhos uma coisa que flutua devagar acalma, e soprar bolha grande exige um sopro lento: é respiração controlada disfarçada de brincadeira. "
              "Boa para o fim de um passeio ou antes de uma troca difícil (banho, sair do parque).",
              atencao="o líquido de bolha não é para beber e pode irritar os olhos; se cair, lave com água. Guarde o frasco fora do alcance depois.",
              variar=["Faça bolhas na hora do banho.", "Bolhas “paradas”: as que pousam na grama sem estourar.", "Deixe que ela escolha: bolha grande ou bolha pequena."],
              registro=CAL)



# ================================================================== U2 CONTAR E IMITAR (Volume 2)

def unidade2(L):
    ativ = [("O dia em três tempos", "conversar", "3 a 5 min"), ("Voz de bicho", "conversar", "5 min"), ("O fantoche de meia", "maos", "10 min"),
            ("Onde está?", "conversar", "5 min"), ("Cadê o toucinho? · O cravo brigou com a rosa · Estou com raiva", "cantar", "2 min cada"),
            ("Fazer cara", "acalmar", "5 min"), ("Uma história de ninar", "acalmar", "5 min")]
    abertura_unidade(L, 1,
                     "No Volume 2 a Marina ouve e reconta histórias. Aos 2 anos, isso vira <b>contar o dia, imitar vozes, fazer de conta e brincar de lembrar</b>. "
                     "Há também um fantoche que diz “não” e depois se acalma, e uma história de ninar para repetir sempre igual.",
                     ativ, cena([("livro", 34, 8, 8), ("lupa", 24, 52, 14), ("chapeu", 30, 84, 8), ("carinha_feliz", 28, 120, 10), ("dedo_nao", 30, 154, 8)], 44, 190))

    atividade(L, "O dia em três tempos", "conversar", "3 a 5 minutos",
              "nenhum; funciona bem na hora de deitar ou no colo, ao fim do dia",
              cena([("sol", 30, 14, 8), ("prato", 32, 62, 14), ("lua", 28, 108, 8), ("estrela", 22, 148, 20)], 46, 190),
              ["Sentem juntas, com a luz baixa. Conte o dia dela em três partes: “primeiro…”, “depois…”, “no fim…”.", "Use frases curtas e as mesmas palavras todo dia.",
               "Pare e espere: ela completa, aponta ou conta sua parte?", "Termine com algo bom: “e agora é hora de dormir”."],
              ["Hoje, primeiro, tomamos café.", "Depois, fomos à praça e você brincou na areia.", "No fim, tomamos banho. E agora é hora de dormir."],
              ["E depois, o que aconteceu?", "Do que você mais gostou?", "Quem estava lá?"],
              "Contar a ordem das coisas (primeiro, depois, no fim) é a base de toda história e treina a memória. Repetido todas as noites, vira também um ritual calmo para fechar o dia, "
              "o que ajuda em dias de muita agitação. Se ela corrigir você, ótimo: significa que ela lembra.",
              variar=["Use três objetos ou fotos, um para cada parte.", "Conte o dia do bichinho de pelúcia.", "Deixe que ela “conte” o dia dela primeiro, mesmo com poucas palavras."])

    atividade(L, "Voz de bicho", "conversar", "5 minutos",
              "nenhum; um bichinho de pelúcia ajuda",
              cena([("leao", 34, 8, 8), ("ratinho", 26, 52, 16), ("gato", 30, 88, 10), ("cachorro", 32, 126, 10)], 46, 190),
              ["Escolha três bichos: um grande (leão), um pequeno (ratinho) e um que você sabe que ela gosta.", "Cada bicho tem uma voz: o leão fala grosso e alto; o ratinho, fininho e baixinho, quase um sussurro.",
               "Faça uma conversa curta entre os dois bichos. Deixe que ela escolha quem fala.", "Termine com os bichos dormindo: voz de sono, bem baixa."],
              ["O leão fala: ROOOAR! Bom dia!", "O ratinho fala: psiu, psiu… quase não dá pra ouvir.", "Agora todo mundo está com sono: shhh."],
              ["Como faz o gato?", "Quem fala baixinho?", "Qual voz a Marina quer?"],
              "Brincar de alto e baixo, grosso e fino, treina o controle da voz e mostra que ela pode escolher como falar. O sussurro e a “voz de sono” são o mesmo controle que usamos para acalmar. "
              "Nessa idade, muita criança adora “mandar” no bicho: deixe.",
              variar=["Voz de monstro bravo que fica pequeno e dócil.", "Voz de chuva (baixinho) e de trovão (alto).", "Um bicho que fala só em sussurro."])

    atividade(L, "O fantoche de meia", "maos", "10 minutos",
              "uma meia limpa e sem botões; olhos de feltro ou de caneta de tecido (nada colado que solte)",
              cena([("luva", 36, 10, 8), ("dedo_nao", 32, 60, 12), ("coracao", 26, 104, 14), ("maos_juntas", 32, 144, 8)], 46, 190),
              ["Vista a meia na mão e faça o fantoche aparecer devagar, dizendo “oi!”.", "O fantoche responde “não!” a tudo: “quer lanche?” “Não!”. Faça com voz engraçada, sem exagerar.",
               "De repente, o fantoche fica bravo (bate o pé). Peça ajuda a ela: “o que a gente faz?”. Respirem juntos: cheirar a flor, soprar a vela.", "O fantoche melhora, e agradece: “obrigado, Marina!”."],
              ["Eu não quero! Não, não, não!", "Ele está bravo. Vamos respirar junto com ele?", "Pronto, a raiva já passou. Obrigado!"],
              ["Por que o fantoche está bravo?", "O que a gente faz quando fica bravo?", "O fantoche quer um abraço?"],
              "Crianças pequenas aprendem a lidar com emoções grandes olhando o boneco, porque é mais fácil ajudar o outro que a si mesma. Aqui o “não” do fantoche é aceito e depois superado, "
              "com o jeito de respirar que vocês já conhecem. Use sempre o mesmo fantoche, com a mesma voz.",
              atencao="olhos bordados ou desenhados, nunca botões ou peças coladas que ela possa soltar e engolir.",
              variar=["Fantoche de dedo, feito com uma luva velha.", "Sombras de bicho na parede, com a lanterna.", "O fantoche conta a história do dia da Marina."])

    atividade(L, "Onde está?", "conversar", "5 minutos",
              "dois ou três panos (ou guardanapos de tecido) e um brinquedo ou bichinho que ela goste",
              cena([("cesta", 40, 12, 12), ("lebre", 28, 62, 18), ("toalha", 34, 104, 14), ("lupa", 28, 150, 14)], 46, 190),
              ["Mostre o brinquedo, cubra com o pano e pergunte “cadê?”.", "Deixe que ela descubra. Comemore: “achou!”.", "Depois esconda atrás de uma almofada, sem que ela veja, e dê pistas: “está perto da janela”.",
               "Troquem: ela esconde, e você procura devagar, fingindo não achar."],
              ["Cadê o coelhinho? Sumiu!", "Será que está embaixo do pano? Achou!", "Agora você esconde. Eu vou procurar."],
              ["Onde está o coelhinho?", "Quem escondeu?", "Quer esconder agora?"],
              "Esconder e achar treina a memória e o saber que as coisas continuam existindo mesmo quando não se veem, e exige esperar para descobrir. "
              "Quando é a vez dela de esconder, ela lidera, e muita criança que diz “não” a ordens adora mandar nas regras do jogo.",
              variar=["Três panos, um brinquedo: em qual está?", "Esconda um som (um sininho) e procurem juntas.", "Esconda você: “cadê a mamãe/o papai?”, e apareça."])

    rimas(L, "O toucinho que sumiu", [
        dict(t="Cadê o toucinho?", linhas=["Cadê o toucinho que estava aqui?", "— O gato comeu.", "Cadê o gato? — Foi pro mato.", "Cadê o mato? — O fogo queimou.", "Cadê o fogo? — A água apagou.",
                                           "Cadê a água? — O boi bebeu.", "Cadê o boi? — Foi carregar milho.", "Cadê o milho? — A galinha comeu.", "Cadê a galinha? — Foi botar ovo…"],
             gesto="a cada “cadê?”, abra as mãos e olhe em volta; a resposta vem de uma voz de cada vez, e ela pode fazer uma delas. A parlenda segue por muitos versos e tem muitas versões; aqui vai um trecho.", origem=TRAD, motivos=["gato", "gota", "ovo"])],
        "Parlendas de perguntas e respostas, como esta, treinam a escuta e a vez de falar, e são ótimas para esperar (na fila, no carro). Deixe que ela complete as respostas que souber: é uma conversa de verdade.")

    rimas(L, "Fazer as pazes", [
        dict(t="O cravo brigou com a rosa", linhas=["O cravo brigou com a rosa", "debaixo de uma sacada.", "O cravo saiu ferido", "e a rosa, despedaçada.", "O cravo ficou doente,", "a rosa foi visitar.", "O cravo teve um desmaio,", "a rosa pôs-se a chorar."],
             gesto="use as duas mãos: um punho (o cravo) e uma mão aberta (a rosa), que brigam e depois se aproximam. No fim, as mãos se abraçam.", origem=TRAD, motivos=["flor_rosa", "maos_juntas"]),
        dict(t="Estou com raiva", linhas=["Estou com raiva, estou com raiva:", "bato o pé — pum, pum, pum!", "Respiro fundo, sopro, fuuu…", "a raiva vai embora", "e não fica nenhuma."],
             gesto="bata o pé nos três “pum”; inspire pelo nariz; sopre devagar pela boca; abra as mãos como quem solta a raiva. Cante junto, quando ela estiver calma, para ela conhecer.", origem=COLECAO, motivos=["pegada", "dedo_nao", "carinha_feliz"])],
        "A briga e as pazes da rosa e do cravo falam de uma coisa que ela já vive: brigar e fazer as pazes. A rima própria da raiva dá ao sentimento um lugar e um gesto. "
        "<b>Cante-a quando ela estiver calma</b>, não no meio da crise: assim, depois, vocês podem recorrer a ela.")

    atividade(L, "Fazer cara", "acalmar", "5 minutos",
              "um espelho inquebrável (de parede ou de mão)",
              cena([("carinha_feliz", 34, 10, 8), ("dedo_nao", 30, 56, 14), ("coracao", 28, 98, 14), ("olho", 30, 138, 10)], 46, 190),
              ["Sentem de frente para o espelho. Faça uma cara feliz e peça que ela imite.", "Faça a cara brava (testa franzida, boca apertada), a triste, a de sono, a de surpresa.",
               "Diga o nome de cada uma e acrescente: “às vezes a gente fica assim, e tudo bem”.", "Deixe que ela escolha uma cara e você imite."],
              ["Olha a cara de brava! A testa fica assim.", "Agora a cara de feliz. Que sorriso!", "Às vezes a gente fica brava. E depois passa."],
              ["Que cara é esta?", "Onde a gente sente a raiva?", "O que ajuda a raiva a passar?"],
              "Dar nome às emoções, nos momentos calmos, é o primeiro passo para ela usar as palavras no meio da raiva, em vez de gritar ou bater. Nada de “cara feia”: todas as caras são permitidas, só varia o que fazemos com elas. "
              "Repita várias vezes: o vocabulário dos sentimentos leva tempo.",
              variar=["Fotos da família com caras diferentes.", "Cara de bicho: leão bravo, ratinho com medo.", "Cara do fantoche de meia."], registro=CAL)

    atividade(L, "Uma história de ninar", "acalmar", "5 minutos",
              "luz baixa, uma almofada ou o colo; o bichinho preferido dela",
              cena([("cama", 36, 12, 10), ("lua", 28, 58, 6), ("gato", 32, 96, 12), ("estrela", 24, 142, 12)], 46, 190),
              ["Baixe a luz e fale mais devagar e mais baixo que o normal.", "Afague as costas dela no ritmo da história, uma pausa a cada frase.", "Conte sempre as mesmas palavras: a repetição é o que acalma.",
               "No fim, diga “boa noite” ao gatinho, e a ela."],
              ["Era uma vez um gatinho cinza.", "Ele brincou o dia inteiro: pulou, correu, subiu na almofada.", "Quando a noite chegou, os olhinhos ficaram pesados.", "Ele se enrolou, fez “rom-rom”…", "e dormiu bem quietinho."],
              ["O gatinho está com sono?", "E a Marina?", "Faz rom-rom com ele?"],
              "Uma história curta, sempre igual e contada devagar, faz o corpo entender que é hora de desacelerar. Vale para dormir e também para depois de uma crise, quando ela está cansada e precisa de colo. "
              "Troque o gatinho pelo bicho preferido dela e use o nome dela só no fim.",
              variar=["Conte sem luz, só com a voz.", "Troque o bicho por um da família: o cachorro, o pássaro.", "Conte a mesma história por uma semana e veja o que ela passa a dizer junto."], registro=CAL)


# ================================================================== U3 MUITO, POUCO, IGUAL (Volume 3)

def unidade3(L):
    ativ = [("Empilhar e derrubar", "maos", "5 a 8 min"), ("Muito e pouco", "conversar", "5 min"), ("Par de meias", "nomear", "5 min"), ("Caça às formas", "mundo", "10 min"),
            ("Um, dois, feijão com arroz · Quantos dedinhos? · Pirulito · Grande e pequeno", "cantar", "2 min cada"),
            ("Cinco respirações na mão", "acalmar", "2 a 3 min"), ("Torre devagar", "acalmar", "5 min")]
    abertura_unidade(L, 2,
                     "No Volume 3 a Marina vê números, formas e padrões. Aos 2 anos, isso vira <b>muito e pouco, igual e diferente, grande e pequeno</b>, sempre com coisas de verdade nas mãos. "
                     "As atividades de calma desta unidade usam os dedos e a lentidão.",
                     ativ, cena([("quadrado_azul", 28, 8, 12), ("circulo_vermelho", 28, 44, 14), ("triangulo_amarelo", 28, 80, 12), ("barra_3", 26, 116, 14), ("maca", 26, 152, 12)], 44, 190))

    atividade(L, "Empilhar e derrubar", "maos", "5 a 8 minutos",
              "3 a 5 copos plásticos, caixinhas de papelão ou blocos grandes e leves",
              cena([("caixa", 36, 12, 10), ("tijolos", 36, 56, 18), ("quadrado_verde", 28, 100, 22), ("retangulo_azul", 30, 140, 20)], 50, 190),
              ["Faça uma torre de 3 e deixe que ela derrube: “tudo cai!”.", "Depois, deixe que ela construa. Ajude só se ela pedir.", "Se a torre cair sozinha, não conserte: diga “caiu” e “de novo?”.", "Guardem juntas, contando os blocos que voltam para a caixa."],
              ["Um, dois, três… em cima. E… pum! Caiu!", "De novo? Vamos fazer outra torre.", "Quantos copos tem? Vamos contar."],
              ["Quantos copos tem?", "Qual está em cima?", "Quer fazer mais alta?"],
              "Empilhar mostra causa e efeito e exige calma nas mãos; e derrubar e recomeçar é um treino de frustração em miniatura. Se ela ficar brava quando cai, "
              "nomeie (“que raiva quando cai!”) e ofereça recomeçar. Cada torre que ela refaz é uma pequena vitória sobre a raiva.",
              atencao="blocos leves e sem peças pequenas; derrube longe do rosto.",
              variar=["Com almofadas e travesseiros: uma torre fofa.", "Cada bloco, uma cor: “agora o vermelho”.", "Um copo de cada vez, enchendo com água (no quintal)."])

    atividade(L, "Muito e pouco", "conversar", "5 minutos",
              "dois pratos e umas 8 frutas ou bolas de meia grandes (nada que caiba na boca)",
              cena([("prato", 40, 14, 14), ("prato", 40, 66, 14), ("laranja", 22, 22, 4), ("laranja", 22, 74, 4), ("laranja", 22, 90, 10), ("maca", 24, 110, 18), ("pera", 24, 146, 14)], 54, 190),
              ["Ponha uma fruta num prato e cinco no outro.", "Pergunte: “qual tem muito? qual tem pouco?”. Aceite o apontar.", "Peça: “me dá poucas”, “me dá muitas”.",
               "Conte tocando em cada fruta, uma a uma, e deixe que ela repita o que souber."],
              ["Aqui tem uma. Aqui tem muitas.", "Um, dois, três, quatro, cinco!", "Você quer muitas ou poucas?"],
              ["Qual prato tem mais?", "Quantas você quer?", "Vamos contar juntas?"],
              "Antes de conhecer os números, a criança entende “muito” e “pouco”. Contar tocando cada objeto, um a um, faz a ligação entre o número e a coisa. "
              "Peça sempre “me dá…” e agradeça: é uma tarefa de verdade, e muita criança que diz “não” adora ser ajudante.",
              atencao="frutas ou bolas bem maiores que a boca dela.",
              variar=["Na feira ou no mercado: “quantas laranjas?”.", "Com colheres, com meias, com sapatos.", "Divida as frutas entre dois bichinhos de pelúcia."])

    atividade(L, "Par de meias", "nomear", "5 minutos",
              "3 ou 4 pares de meias limpas de cores diferentes, bagunçadas num cesto",
              cena([("cesta", 38, 10, 12), ("luva", 30, 56, 18), ("luva", 30, 90, 18), ("gorro", 28, 126, 16), ("gorro", 28, 160, 16)], 48, 190),
              ["Espalhe as meias no chão e mostre uma: “cadê outra igual?”.", "Deixe que ela procure e junte as duas.", "Diga “igual” quando for par, e “diferente” quando não for.", "No fim, dobre o par junto: é uma ajuda de verdade na casa."],
              ["Esta é azul. Cadê outra igual?", "Igual! Achou o par.", "Esta é diferente: é vermelha."],
              ["Qual é igual a esta?", "Qual é diferente?", "Quantas meias temos?"],
              "Parear é a primeira forma de classificar, base da matemática, e ajudar na roupa é uma tarefa real, que dá orgulho. "
              "Se ela não tiver paciência, comece com 2 pares e aumente aos poucos.",
              variar=["Parear sapatos, colheres ou tampas e potes.", "Parear por cor: tudo o que é vermelho junto.", "Esconda uma meia e peça para achar o par perdido."])

    atividade(L, "Caça às formas", "mundo", "10 minutos",
              "nenhum: a casa ou o quintal",
              cena([("circulo_azul", 32, 14, 10), ("quadrado_vermelho", 30, 58, 14), ("triangulo_verde", 30, 100, 12), ("retangulo_amarelo", 30, 142, 14)], 46, 190),
              ["Mostre um prato e diga: “redondo”. Passe o dedo na borda dele, com ela.", "Saiam pela casa procurando coisas redondas: relógio, tampa, bola.", "Depois, coisas quadradas ou compridas: janela, caixa, porta.",
               "Cada achado vale um “achamos!” e uma palma."],
              ["O prato é redondo, como uma lua.", "A janela é quadrada. Quatro cantinhos!", "Você achou uma coisa redonda!"],
              ["O que mais é redondo?", "Cadê uma coisa quadrada?", "A bola rola? E a caixa?"],
              "Procurar formas no mundo mistura movimento, atenção e vocabulário. Dá ao “passeio dentro de casa” um objetivo, útil nos dias em que não dá para sair. "
              "Passar o dedo no contorno ajuda ela a sentir a forma.",
              variar=["Faça a forma com o corpo: braços em círculo, mãos em quadrado.", "Desenhe com o dedo no ar, na areia ou no vidro embaçado.", "Procure só uma forma por dia."])

    rimas(L, "Para contar e brincar", [
        dict(t="Um, dois, feijão com arroz", linhas=["Um, dois, feijão com arroz;", "três, quatro, feijão no prato;", "cinco, seis, falar inglês;", "sete, oito, comer biscoito;", "nove, dez, comer pastéis."],
             gesto="bata palmas no ritmo e mostre os dedos de cada número: um, dois… Ela pode bater no joelho, ou nos seus joelhos.", origem=TRAD, motivos=["barra_1", "barra_2", "barra_3"]),
        dict(t="Quantos dedinhos?", linhas=["Cinco dedinhos tem esta mão,", "e outros cinco, a outra mão.", "Um, dois, três, quatro, cinco,", "bate palmas: plim, plão!"],
             gesto="mostre uma mão aberta e a outra, conte tocando cada dedo, e bata palmas no “plim, plão”.", origem=COLECAO, motivos=["mao", "mao"])],
        "Parlendas de contar são o jeito mais antigo de aprender a sequência dos números: a criança canta antes de entender. Não cobre a quantidade: o ritmo vem primeiro.")

    rimas(L, "Mais duas para mexer", [
        dict(t="Pirulito que bate, bate", linhas=["Pirulito que bate, bate,", "pirulito que já bateu;", "quem gosta de mim é ela,", "quem gosta dela sou eu."],
             gesto="bata palmas no ritmo e, no “ela”, aponte para a Marina; no “eu”, abrace-a.", origem=TRAD, motivos=["maos_juntas", "coracao"]),
        dict(t="Grande e pequeno", linhas=["Grande, grande, grande,", "braços para o céu!", "Pequeno, pequeno, pequeno,", "encolhido no chapéu!"],
             gesto="levante os braços e fique na ponta dos pés; depois agache e esconda a cabeça. Faça devagar, depois rápido.", origem=COLECAO, motivos=["estrela", "chapeu"])],
        "Rimas com o corpo gastam energia e ensinam os contrários (grande e pequeno, depressa e devagar). Faça rápido para animar e devagar para terminar: é um jeito de a criança sentir a diferença entre agitar e acalmar.")

    atividade(L, "Cinco respirações na mão", "acalmar", "2 a 3 minutos",
              "nenhum; uma das suas mãos e uma das dela",
              cena([("mao", 44, 14, 6), ("mao", 44, 76, 6), ("estrela", 24, 138, 16), ("coracao", 26, 164, 22)], 50, 190),
              ["Abra a mão dela. Com o seu dedo, suba por fora do polegar enquanto vocês inspiram, e desça pelo outro lado enquanto expiram.", "Passe pelos cinco dedos, um por vez, contando de 1 a 5.",
               "No fim, deixe que ela faça o mesmo na sua mão.", "Termine com a mão no peito: “sente o coração?”."],
              ["Sobe o dedinho… cheira a flor.", "Desce… sopra a vela. Um!", "Muito bem. Mais um dedinho."],
              ["Quantos dedinhos?", "Como está o corpo agora?", "Quer fazer na minha mão?"],
              "Respirar acompanhando o toque num dedo dá à criança uma tarefa concreta e liga a respiração à contagem, sem exigir que ela “fique quieta”. "
              "Pratique em dias calmos, no colo ou antes de dormir; na hora de uma crise, só proponha se ela aceitar.",
              variar=["Faça na sua própria mão, para ela ver.", "Com a voz: “um… dois…” baixinho.", "Faça no pé, também."], registro=CAL)

    atividade(L, "Torre devagar", "acalmar", "5 minutos",
              "3 copos plásticos ou 3 almofadas pequenas",
              cena([("tijolos", 34, 14, 14), ("caracol", 30, 62, 20), ("mao", 32, 104, 12), ("caixa", 30, 144, 16)], 48, 190),
              ["Mostre como mover “como uma lesma”: a mão sobe devagar, pousa o copo bem de mansinho.", "Deixe que ela repita, um copo por vez, sem pressa.", "Conte baixinho a cada copo que sobe: “um… dois… três…”.",
               "No fim, respirem juntas olhando a torre. Derrubar é permitido, mas devagar."],
              ["Devagar… devagarinho… como uma lesma.", "Mãos de pluma. Pousa de mansinho.", "Está de pé! Vamos respirar olhando a torre."],
              ["Está devagar?", "Quer fazer mais devagar ainda?", "A torre ficou firme?"],
              "Mover-se devagar de propósito treina o controle do impulso, e dar uma tarefa com começo, meio e fim, curta e visível, sustenta a atenção por alguns minutos. "
              "É o contrário da “pressa” que costuma vir antes de uma birra.",
              variar=["Despeje água devagar de uma jarra para um copo.", "Leve uma bola de meia numa colher sem deixar cair.", "Andar como lesma até a porta."], registro=CAL)


# ================================================================== U4 SOM E MOVIMENTO (Volume 4)

def unidade4(L):
    ativ = [("Batuque de panela", "corpo", "5 a 8 min"), ("Estátua", "corpo", "5 min"), ("Os três sons", "mundo", "3 a 5 min"), ("Chocalho de casa", "maos", "10 min"),
            ("Marcha, soldado · Ciranda · Se essa rua fosse minha · Devagar, devagarinho", "cantar", "2 min cada"),
            ("Balançar e cantar baixinho", "acalmar", "5 min"), ("Dançar e derreter", "acalmar", "5 min")]
    abertura_unidade(L, 3,
                     "No Volume 4 a Marina ouve o som e o silêncio, o pulso, o forte e o fraco. Aos 2 anos, isso vira <b>bater, dançar, parar, escutar e cantar</b>. "
                     "Muita criança pequena usa o som e o movimento para gastar energia e, depois, se acalmar: as duas últimas atividades usam essa mudança do rápido para o lento.",
                     ativ, cena([("tambor", 34, 8, 10), ("pandeiro", 30, 48, 14), ("chocalho", 28, 86, 8), ("sino", 26, 122, 12), ("seminima", 22, 156, 14)], 44, 190))

    atividade(L, "Batuque de panela", "corpo", "5 a 8 minutos",
              "uma panela ou lata, uma colher de pau, e uma toalha dobrada para abafar, se for preciso",
              cena([("tambor", 38, 12, 10), ("colher", 32, 60, 18), ("chocalho", 28, 100, 14), ("seminima", 22, 146, 16)], 46, 190),
              ["Ponha a panela virada de boca para baixo. Bata o pulso, sempre igual: toc, toc, toc.", "Deixe que ela bata também. Alterne: você, ela, você, ela.", "Experimente forte e fraco, rápido e devagar. Peça que ela escolha.",
               "Termine com um toc bem fraquinho e silêncio."],
              ["Toc, toc, toc: forte!", "Toc… toc… toc: fraco, bem fraquinho.", "Agora rápido: toc-toc-toc-toc! E devagar."],
              ["Quer forte ou fraco?", "Rápido ou devagar?", "Quem toca agora?"],
              "O pulso (a batida regular) é a base da música, e bater forte descarrega energia de um jeito aceito e divertido. "
              "Ter de parar no silêncio e esperar a vez treina o controle sem parecer lição.",
              atencao="se o barulho incomodar, bata numa almofada ou toalha dobrada; nunca perto dos ouvidos dela.",
              variar=["Bata no chão com a mão, no colo, na barriga.", "Cante uma cantiga no ritmo da batida.", "Dois instrumentos: um forte, um fraco."])

    atividade(L, "Estátua", "corpo", "5 minutos",
              "uma música cantada por você, ou um rádio; um espaço sem obstáculos",
              cena([("pegada", 17, 14, 6), ("pegada_esq", 17, 54, 6), ("estrela", 26, 98, 14), ("coracao", 26, 138, 12)], 46, 190),
              ["Cante ou ponha música e dancem juntas.", "De repente, pare e diga “estátua!”. As duas ficam paradas, como uma estátua.", "Conte baixinho até 3 e diga “dança!”. Repita várias vezes.",
               "Termine com uma estátua bem comprida e uma respiração."],
              ["Dança, dança, dança… estátua!", "Ficou paradinha, como pedra.", "Um, dois, três… dança!"],
              ["Quem ficou parada?", "Qual estátua é mais engraçada?", "Quer ser a que manda?"],
              "Parar de repente, no meio do movimento, é um dos exercícios mais completos de autocontrole: a criança segura um impulso. Como é brincadeira, ela adora. "
              "Deixe que ela mande a parada de vez em quando: assim ela exercita os dois lados.",
              variar=["Estátua de bicho: leão, passarinho, sapo.", "Estátua bem devagar, derretendo aos poucos.", "Estátua só dos braços, só da cabeça."])

    atividade(L, "Os três sons", "mundo", "3 a 5 minutos",
              "nenhum; um lugar com uns poucos sons (janela, quintal, varanda)",
              cena([("orelha", 36, 10, 10), ("sino", 26, 56, 16), ("m_passaros", 34, 92, 10), ("nuvem", 34, 138, 12)], 46, 190),
              ["Sentem juntas e diga: “vamos escutar três sons”.", "Fiquem em silêncio por um minuto. Levante um dedo para cada som que ouvir.", "Cada som tem nome: “carro”, “passarinho”, “vento”. Deixe que ela diga também.",
               "Depois, imitem um dos sons, bem baixinho."],
              ["Shhh… escuta. Um som!", "Era um passarinho! Piu, piu.", "Dois. Três. Que bom que a gente escutou."],
              ["O que você ouviu?", "De onde veio?", "Era um som alto ou baixinho?"],
              "Escutar em silêncio, mesmo por um minuto, treina a atenção e acalma. Funciona bem logo depois do batuque ou da estátua, para fechar a agitação. "
              "Não é preciso acertar o som: o que conta é ficar quieta e perceber.",
              variar=["De olhos fechados, se ela quiser.", "Com a janela fechada e depois aberta: quais sons mudam?", "À noite, com a luz baixa."])

    atividade(L, "Chocalho de casa", "maos", "10 minutos",
              "uma garrafa plástica pequena e limpa, grãos grandes (grão-de-bico, feijão grande), cola quente e fita, fitas coloridas para enfeitar",
              cena([("chocalho", 40, 12, 8), ("tijolos", 28, 62, 20), ("pincel", 32, 104, 12), ("papel_azul", 28, 146, 16)], 48, 190),
              ["Escolha com ela a garrafa e o que vai dentro (macarrão penne ou feijão grande). <b>Só o adulto põe os grãos na garrafa</b>; ela escolhe e olha.", "<b>O adulto fecha a tampa com cola quente e fita</b>, longe dela.", "Enfeitem a garrafa com fitas coloridas.",
               "Toquem: forte, fraco, rápido, devagar, e deitem o chocalho para silenciar."],
              ["Chacoalha! Que barulho! Chuá, chuá.", "Agora bem fraquinho.", "Quieto: o chocalho dormiu."],
              ["Que barulho faz?", "É forte ou fraco?", "Onde o chocalho dorme?"],
              "Fazer o próprio instrumento dá orgulho e cuidado: ele é “dela”. Os sons de grãos e garrafa são também suaves e repetitivos, bons para acalmar.",
              atencao="os grãos ficam só nas mãos do adulto: confira que nenhum ficou solto no chão ou na mesa antes de ela chegar. Tampa bem vedada com cola e fita; troque o chocalho se rachar ou soltar o conteúdo. Use só com você por perto.",
              variar=["Chocalhos diferentes, só com coisas grandes: macarrão penne, feijão grande, grão-de-bico graúdo (sempre selados pelo adulto).", "Cante e acompanhe com o chocalho.", "Guarde na “caixa dos sons”."])

    rimas(L, "Para marchar e rodar", [
        dict(t="Marcha, soldado", linhas=["Marcha, soldado,", "cabeça de papel;", "quem não marchar direito", "vai preso no quartel."],
             gesto="marchem juntas no lugar, no ritmo da batida; no último verso, parem de uma vez, como estátua.", origem=TRAD, motivos=["pegada", "pegada_esq"]),
        dict(t="Ciranda, cirandinha", linhas=["Ciranda, cirandinha,", "vamos todos cirandar;", "vamos dar a meia-volta,", "volta e meia vamos dar."],
             gesto="de mãos dadas, girem devagar em roda; na “meia-volta”, virem para o outro lado. Com duas pessoas, é uma roda de dois.", origem=TRAD, motivos=["maos_juntas", "estrela"])],
        "Marchar e rodar de mãos dadas são movimentos antigos de brincadeira, com pulso marcado. Os versos para na estátua ajudam a ela aprender a parar quando a música para.")

    rimas(L, "Para ir e para ninar", [
        dict(t="Se essa rua fosse minha", linhas=["Se essa rua, se essa rua fosse minha,", "eu mandava, eu mandava ladrilhar,", "com pedrinhas, com pedrinhas de brilhante,", "para o meu, para o meu amor passar."],
             gesto="balance de um lado para o outro, devagar, com ela no colo ou sentadas de frente. É uma cantiga lenta: cante baixinho.", origem=TRAD, motivos=["pedra", "estrela"]),
        dict(t="Devagar, devagarinho", linhas=["Depressa, depressa,", "o coelho corre assim.", "Devagar, devagarinho,", "a lesma vem pra mim."],
             gesto="mexa as mãos depressa nos dois primeiros versos e bem devagar nos dois últimos, até ficarem paradas. Repita mais lento a cada vez.", origem=COLECAO, motivos=["lebre", "caracol"])],
        "Cantigas lentas, balançando, são o jeito mais antigo de acalmar. A rima do coelho e da lesma mostra o contraste: terminar sempre no devagar faz o corpo acompanhar.")

    atividade(L, "Balançar e cantar baixinho", "acalmar", "5 minutos",
              "o colo, ou uma cadeira de balanço; luz baixa",
              cena([("cama", 36, 10, 12), ("lua", 28, 56, 8), ("estrela", 22, 92, 16), ("coracao", 28, 132, 10)], 46, 190),
              ["Sente com ela no colo, de frente para o seu peito, e balance de um lado para o outro, bem devagar.", "Cante baixinho a cantiga abaixo, com a voz bem suave. Repita.",
               "Quando o corpo dela amolecer, vá parando de balançar, até ficarem paradas.", "Termine com um beijo e um “está tudo bem”."],
              ["Dorme, dorme, a lua vem,", "a noite chega e faz bem;", "fecha os olhos, o sono vem,", "e eu estou aqui também."],
              ["Quer balançar?", "Quer mais uma vez?", "Está gostoso?"],
              "Balançar num ritmo regular e cantar baixinho é uma das formas mais antigas de acalmar uma criança: o corpo reconhece o ritmo, e a voz do adulto mostra que está tudo bem. "
              "Pode ser usado depois de uma crise, quando ela precisa de colo. A cantiga é da coleção; invente a sua.",
              variar=["Só cantarole, sem letra: “hummm”.", "Cante o nome dela no lugar da lua.", "Deitadas, com a mão dela no seu peito."], registro=CAL)

    atividade(L, "Dançar e derreter", "acalmar", "5 minutos",
              "um espaço livre; uma música rápida (cantada por você) e depois uma lenta",
              cena([("pegada", 17, 12, 6), ("pegada_esq", 17, 52, 6), ("sorvete", 26, 100, 8), ("nuvem", 34, 140, 14)], 48, 190),
              ["Dancem rápido, como foguete: braços, pés, pulos.", "Então diga “derrete!” e deixem o corpo ir devagar para o chão, como um sorvete ao sol.", "Fiquem deitadas, respirando, por alguns segundos.",
               "Levantem devagar e repita se ela quiser."],
              ["Rápido, rápido, rápido, como foguete!", "E agora derrete, derrete, derrete…", "Respira. O corpo ficou molinho."],
              ["Como está o corpo agora?", "Está mais quentinho? Mais mole?", "Quer ser foguete de novo?"],
              "Gastar energia e depois “derreter” ensina o corpo a passar do rápido para o lento. É um bom ritual antes do banho, do sono ou depois de uma brincadeira agitada. "
              "Nomeie o que ela sente (“o coração está batendo rápido”).",
              variar=["Fogo e neve: quente e frio, rápido e lento.", "Derreter só de uma vez, ou aos poucos.", "Termine com um abraço de urso apertado."], registro=CAL)


# ================================================================== U5 OLHAR E SUJAR AS MÃOS (Volume 5)

def unidade5(L):
    ativ = [("Pintar com o dedo", "maos", "10 min"), ("Rabisco grande", "maos", "5 min"), ("Massinha de farinha", "maos", "10 min"), ("Um quadro por um minuto", "mundo", "3 min"),
            ("Meu limão, meu limoeiro · As cores · Mão suja, mão limpa · O sapo não lava o pé", "cantar", "2 min cada"),
            ("Pintar com água", "acalmar", "5 a 10 min"), ("Massagem nas mãos", "acalmar", "3 a 5 min")]
    abertura_unidade(L, 4,
                     "No Volume 5 a Marina olha obras de arte e experimenta cor, linha e massa. Aos 2 anos, isso vira <b>sujar as mãos, fazer grande e olhar devagar</b>. "
                     "Atividades com tinta e massinha são ótimas para quem se frustra fácil: o resultado não precisa ser bonito, e a mão faz tudo.",
                     ativ, cena([("pincel", 34, 8, 8), ("papel_azul", 28, 44, 16), ("papel_amarelo", 28, 78, 12), ("papel_vermelho", 28, 112, 16), ("argila_bola", 28, 150, 12)], 44, 190))

    atividade(L, "Pintar com o dedo", "maos", "10 minutos",
              "tinta atóxica (ou iogurte natural com corante de comida), vermelha, amarela e azul; papel grande; avental velho; um pano úmido",
              cena([("circulo_vermelho", 30, 10, 12), ("circulo_amarelo", 30, 48, 8), ("circulo_azul", 30, 86, 14), ("mao", 34, 126, 10), ("pincel", 28, 162, 14)], 48, 190),
              ["Forre o chão ou a mesa, ponha o avental e deixe o pano úmido à mão.", "Ponha uma colherada de cada cor num prato. Deixe que ela mergulhe o dedo e pinte onde quiser.",
               "Quando as cores se misturarem, nomeie: “vermelho com amarelo… laranja!”.", "Depois, lavem as mãos juntas, cantando a rima da mão suja."],
              ["Vermelho! Amarelo! Azul!", "Misturou: olha, ficou laranja!", "A mão ficou toda colorida."],
              ["Que cor é esta?", "O que aconteceu quando misturou?", "Quer mais azul?"],
              "Pintar com os dedos junta tato, cor e movimento, e não tem jeito errado: é um alívio para quem se frustra se algo “não fica bom”. As três cores primárias são as do Volume 5. "
              "O que importa é o gesto, não o desenho.",
              atencao="tinta atóxica e lavável; não é para provar. Sem tinta ou corante perto de feridas ou de olhos; lave as mãos no fim.",
              variar=["Pinte com uma esponja, uma folha, uma colher.", "Pinte o próprio pé e deixe pegadas.", "Pinte só de uma cor hoje."])

    atividade(L, "Rabisco grande", "maos", "5 minutos",
              "um giz grosso no chão do quintal, ou papel grande na parede e giz de cera grosso",
              cena([("lapis_cor", 40, 12, 12, -12), ("m_riacho", 34, 62, 16), ("circulo_verde", 28, 104, 14), ("papel_rosa", 30, 144, 14)], 46, 190),
              ["Ponha o giz na mão dela e faça uma linha comprida. Peça que ela imite com o braço inteiro.", "Experimente linhas retas, curvas, bolinhas, zigue-zague.", "Faça rápido e devagar. Dê nome ao que ela fizer: “uma cobra!”.",
               "No fim, “apaguem” juntas com um pano úmido ou com os pés."],
              ["Uma linha comprida! Ssssh.", "Uma curva, como uma onda.", "Um redondo. Redondo, redondo, redondo."],
              ["Quer fazer rápido ou devagar?", "O que é isto?", "Faz uma linha comprida?"],
              "O rabisco com o braço todo é a primeira forma de desenhar, e mexe os ombros e o corpo. Linhas e círculos são o que os artistas do Volume 5 (como Kandinsky) usavam. "
              "Não peça que ela “desenhe uma coisa”: deixe que o rabisco seja só rabisco.",
              atencao="giz e giz de cera grossos, para não irem à boca.",
              variar=["Rabisque ao som de música: rápida, lenta.", "Desenhe no vidro do boxe com tinta de banho.", "Uma linha longa pelo chão inteiro."])

    atividade(L, "Massinha de farinha", "maos", "10 minutos",
              "2 xícaras de farinha de trigo, 1 de sal, 1 de água morna e 1 colher de óleo (uma massinha caseira); uma tábua ou um pano",
              cena([("argila_bola", 30, 12, 16), ("argila_cobra", 34, 52, 12), ("argila_vaso", 30, 94, 8), ("tigela", 32, 134, 14)], 48, 190),
              ["Misture os ingredientes com ela (despejar e mexer já é brincadeira) até ficar uma massa macia.", "Deixe que ela aperte, bata, belisque, enrole. Mostre uma cobra e uma bola.", "Dê nome ao que sai: “uma bolinha!”, “uma cobrinha comprida!”.",
               "Guarde num pote fechado, na geladeira, por uns dias."],
              ["Aperta! Que macia.", "Enrola, enrola, enrola: uma cobrinha.", "Bate! Pam, pam, pam!"],
              ["É mole ou é dura?", "O que você fez?", "Quer uma bola ou uma cobra?"],
              "Apertar e bater a massa é bom para a força das mãos e para a raiva (descarregar, sem machucar ninguém). A massinha caseira é segura e é a versão simples do Volume 5, na unidade de modelar. "
              "Pode repetir todos os dias: a massa não “acaba”.",
              atencao="a massa é salgada e não é comida: não deixe que ela coma; tire do alcance depois. Alergia a trigo: troque por massinha comprada atóxica.",
              variar=["Esconda um brinquedo grande na massa.", "Imprima a mão e o pé na massa.", "Faça um “bolo” e cante parabéns ao bichinho."])

    atividade(L, "Um quadro por um minuto", "mundo", "3 minutos",
              "uma obra do Volume 5 (os Girassóis, de Van Gogh, ou outra), ou qualquer livro de arte",
              cena([("girassol", 36, 14, 10), ("lupa", 28, 62, 20), ("olho", 30, 100, 12), ("ninfeia", 34, 140, 14)], 46, 190),
              ["Abra o livro no quadro e sentem de frente para ele, juntas.", "Fiquem em silêncio por um minuto, só olhando.", "Depois pergunte: “o que você vê?”. Aceite qualquer resposta.", "Feche o livro e conte: “vimos flores amarelas”."],
              ["Olha quanta cor! Amarelo, amarelo.", "Tem flores. E um vaso.", "Que quadro bonito. Vamos olhar mais um pouquinho?"],
              ["O que você vê?", "Qual cor você mais gosta?", "Tem flor? Quantas?"],
              "Olhar uma imagem por um minuto, em silêncio, treina a atenção sem exigir fala nem tarefa, e apresenta a ela uma obra de verdade, como fazem os museus com os pequenos. "
              "Um minuto basta: se ela quiser mais, ótimo; se não, fim.",
              variar=["Escolha o mesmo quadro por uma semana.", "Imite o quadro com o corpo: flor, sol.", "Procure no quintal algo da mesma cor."])

    rimas(L, "Meu limão e as cores", [
        dict(t="Meu limão, meu limoeiro", linhas=["Meu limão, meu limoeiro,", "meu pé de jacarandá;", "uma vez, tindolelê,", "outra vez, tindolalá."],
             gesto="balance de um lado para o outro; em “tindolelê” e “tindolalá”, gire a mão e depois a outra. Fique em pé, rodando devagar.", origem=TRAD, motivos=["laranja", "folha"]),
        dict(t="As cores", linhas=["Vermelho, vermelho, cor de morango.", "Amarelo, amarelo, cor de banana.", "Azul, azul, cor do céu lá no alto.", "Verde, verde, folha que se balança."],
             gesto="aponte cada cor numa coisa de verdade, no cenário, na roupa. Deixe que ela aponte também.", origem=COLECAO, motivos=["morango", "banana", "papel_azul", "folha"])],
        "As cantigas de roda e as rimas de cor ligam som, movimento e vocabulário. A das cores, repetida, serve de ponte para o Volume 5 e para a hora da tinta.")

    rimas(L, "Para limpar as mãos", [
        dict(t="Mão suja, mão limpa", linhas=["Mão suja, mão suja,", "pra água vai!", "Esfrega, esfrega,", "a espuma sai.", "Mão limpa, mão limpa,", "cheirinho de sabão;", "seca, seca, seca", "na toalha, pronto, então!"],
             gesto="molhe as mãos, esfregue no “esfrega”, enxágue no “sai”, e seque cantando. É a rima da troca: pintura, massa, terra e comida acabam sempre assim.", origem=COLECAO, motivos=["sabonete", "gota", "toalha"]),
        dict(t="O sapo não lava o pé", linhas=["O sapo não lava o pé,", "não lava porque não quer.", "Ele mora lá na lagoa", "e não lava o pé porque não quer.", "Mas que chulé!"],
             gesto="tape o nariz no “chulé” e faça a careta; mostre o pé do sapo sujo e depois limpo. É uma rima divertida para a hora de lavar os pés.", origem=TRAD, motivos=["pe", "poca"])],
        "Uma rima fixa para cada troca (pintar → lavar as mãos) avisa o fim de uma atividade e reduz o “não”: ela já sabe o que vem. Use sempre a mesma música, na mesma ordem.")

    atividade(L, "Pintar com água", "acalmar", "5 a 10 minutos",
              "um pincel grosso (ou uma esponja) e um balde com água; uma parede, um muro ou o chão do quintal",
              cena([("pincel", 38, 12, 8, 20), ("jarra", 30, 56, 18), ("gota", 22, 92, 10), ("m_riacho", 36, 128, 14)], 48, 190),
              ["Dê a ela o pincel molhado e mostre: pinte a parede ou o chão.", "Observem juntas: a água escurece o chão e depois some, bem devagar.", "Deixe que ela “apague” o que você pintou e “apague” o que ela pintou.",
               "Quando acabar, tire o balde e fiquem olhando a parede secar."],
              ["A água pinta de escuro. Olha!", "Está sumindo, sumindo… devagar.", "Agora a parede está seca. Pinta de novo?"],
              ["O que a água fez?", "Cadê o que você pintou?", "Quer pintar o chão ou a parede?"],
              "Pintar com água tem todos os gestos da pintura, sem sujeira nem “errado”, porque o desenho some sozinho. O movimento repetido de pintar e ver secar é calmante e ensina a esperar. "
              "Ótima para depois de uma crise ou numa tarde difícil.",
              atencao="com água em balde, não a deixe sozinha; esvazie o balde no fim.",
              variar=["Pinte o espelho do banheiro.", "Pinte uma “pegada” de água com o pé.", "Pinte letras e formas grandes e depois apague."], registro=CAL)

    atividade(L, "Massagem nas mãos", "acalmar", "3 a 5 minutos",
              "um creme hidratante suave (ou óleo) sem perfume forte, se ela gostar; nada mais",
              cena([("mao", 44, 14, 8), ("mao", 44, 74, 8), ("coracao", 26, 140, 14), ("maos_juntas", 30, 158, 24)], 50, 190),
              ["Pergunte: “posso fazer carinho nas suas mãos?”. Só comece se ela aceitar.", "Ponha um pouquinho de creme nas mãos e alise a palma dela, devagar, com uma pressão firme.", "Passe um dedinho de cada vez, do punho até a ponta.",
               "Se ela quiser, deixe que ela faça em você."],
              ["Palma… devagar… cada dedinho.", "Que mãozinha macia.", "Quer que eu pare ou quer mais?"],
              ["Está gostoso?", "Quer mais ou quer parar?", "Quer fazer na minha mão?"],
              "O toque firme e lento é calmante e aproxima vocês. Pedir licença e parar quando ela quiser também ensina que o corpo é dela. "
              "Combine bem com o final do dia, depois do banho ou antes de dormir.",
              atencao="se ela tiver pele sensível ou alergia, teste antes uma pontinha de creme; não deixe o creme ir aos olhos ou à boca.",
              variar=["Faça nos pés.", "Cantarole baixinho enquanto massageia.", "Troquem: ela faz em você."], registro=CAL)


# ================================================================== U6 SAIR E TOCAR (Volume 6)

def unidade6(L):
    ativ = [("Caça-folhas", "mundo", "10 min"), ("Regar a plantinha", "maos", "5 a 8 min"), ("Bichinho de perto", "mundo", "5 a 10 min"), ("Lama e terra molhada", "maos", "10 min"),
            ("A dona aranha · Sapo-cururu · Peixe vivo · Formiguinha", "cantar", "2 min cada"),
            ("Deitar e olhar as nuvens", "acalmar", "5 min"), ("Corrida de lesma", "acalmar", "5 min")]
    abertura_unidade(L, 5,
                     "No Volume 6 a Marina observa aves, bichinhos, árvores e a água. Aos 2 anos, isso vira <b>sair, tocar, cuidar e olhar de mansinho</b>. "
                     "A natureza é um dos melhores lugares para acalmar e gastar energia: muitas atividades aqui já são de calma sem se chamarem assim.",
                     ativ, cena([("folha_carvalho", 30, 8, 12), ("caracol", 28, 44, 20), ("formiga", 26, 78, 14), ("pinha", 26, 112, 16), ("plantinha", 28, 148, 12)], 44, 190))

    atividade(L, "Caça-folhas", "mundo", "10 minutos",
              "uma sacola de pano ou uma cesta; um quintal, uma praça ou uma calçada com árvores",
              cena([("folha_carvalho", 34, 12, 10), ("folha_bordo", 30, 54, 18), ("folha_coracao", 30, 92, 10), ("folha_seca", 28, 128, 16), ("cesta", 30, 160, 16)], 48, 190),
              ["Combine: “vamos achar cinco folhas”. Só as que já estão no chão.", "Cada folha que ela achar entra na cesta, com um nome: “grande”, “pequena”, “amarela”.", "Em casa, espalhem as folhas e ponham em fila, da maior para a menor.",
               "Colem uma folha no caderno de natureza (Volume 6), se ela quiser."],
              ["Olha uma folha! É grande e verde.", "Esta é pequena e seca. Faz crec, crec.", "Cinco folhas! Conseguimos."],
              ["Qual é a maior?", "Qual folha você mais gostou?", "Tem folha amarela?"],
              "Procurar folhas dá um objetivo ao passeio, e contar até cinco ajuda quem tem pouca paciência a saber quando acaba. Comparar o tamanho e a cor é vocabulário e matemática ao mesmo tempo. "
              "A coleção de folhas combina com a unidade 4 do Volume 6.",
              atencao="só folhas caídas; não tire do galho; nada de plantas desconhecidas na boca; lave as mãos depois.",
              variar=["Procure só folhas verdes, ou só secas.", "Esfregue uma folha e cheire.", "Faça um “tapete de folhas” e pule em cima."])

    atividade(L, "Regar a plantinha", "maos", "5 a 8 minutos",
              "um vaso com uma planta resistente, um regador pequeno ou uma jarra, um prato embaixo",
              cena([("vaso", 34, 12, 14), ("plantinha", 36, 52, 6), ("regador", 40, 96, 14), ("gota", 14, 144, 22), ("gota", 12, 156, 36)], 52, 190),
              ["Mostre a terra e ponha o dedo: “seca ou molhada?”.", "Deixe que ela despeje a água, só um pouco. “Para!” quando for suficiente.", "Fiquem olhando a água sumir na terra.", "Marquem um dia para olhar de novo: “amanhã a planta vai estar assim?”."],
              ["A planta está com sede. Só um pouquinho!", "Glub, glub… a terra bebeu a água.", "Amanhã a gente olha de novo."],
              ["A terra está seca ou molhada?", "Quanta água?", "A planta está feliz?"],
              "Cuidar de uma planta dá uma tarefa real, repetida todo dia, e mostra uma mudança lenta, a lição de esperar. “Pouquinho” e “para” treinam o controle das mãos. "
              "É também uma tarefa bem aceita por quem diz “não” a ordens: aqui ela é a responsável.",
              atencao="não deixe que ela coma terra ou folhas; escolha uma planta que não seja tóxica.",
              variar=["Plante um feijão no algodão (Volume 6, unidade 5).", "Regue as plantas do quintal.", "Desenhe a planta toda semana."])

    atividade(L, "Bichinho de perto", "mundo", "5 a 10 minutos",
              "nenhum; uma lupa de brinquedo, se quiser; um jardim, uma praça ou um vaso",
              cena([("formiga", 30, 12, 18), ("caracol", 32, 54, 14), ("besouro", 28, 96, 18), ("lupa", 30, 136, 10), ("borboleta", 28, 160, 14)], 46, 190),
              ["Procurem um bichinho pequeno (formiga, caracol, joaninha) e chegue de mansinho: “shhh”.", "Fiquem quietas olhando. Não toquem, não peguem.", "Diga o nome dele e o que ele faz: “a formiga carrega comida”.",
               "Despeçam-se: “tchau, formiga, vá para casa”."],
              ["Shhh, chegamos de mansinho.", "A formiga está carregando uma migalha. Quanta força!", "Ele tem casa. Vamos deixar ele ir."],
              ["Onde ele está indo?", "Quantas perninhas?", "Qual é o nome dele?"],
              "Aproximar-se devagar de um bicho é um exercício de controle: ela precisa ficar quieta e baixar a voz para não assustá-lo. "
              "Funciona porque a razão é do bicho (e não uma ordem sua). Mostra também respeito pelos seres vivos, ideia central do Volume 6.",
              atencao="olhar, nunca pegar; afaste-se de abelhas, vespas, aranhas e lagartas peludas; sapato fechado; lave as mãos.",
              variar=["Siga uma formiga por um minuto.", "Desenhe o bicho depois, com giz.", "Olhe o caracol de dia de chuva."])

    atividade(L, "Lama e terra molhada", "maos", "10 minutos",
              "terra, água, uma bacia e colheres; roupa que possa sujar; um canto do quintal",
              cena([("tigela", 32, 12, 18), ("colher", 32, 52, 10), ("pedra", 26, 92, 22), ("gota", 18, 130, 14), ("bota", 28, 158, 14)], 48, 190),
              ["Ponha terra na bacia e um pouco de água. Deixe que ela misture com as mãos e a colher.", "Faça “bolos”, “sopas”, “montanhas”, ou só espalhe.", "Se quiser, enfeite com folhas e pedras.",
               "No fim, lavem as mãos e os pés na mangueira ou no tanque, cantando “mão suja, mão limpa”."],
              ["Que lama macia! Squash, squash.", "Fazemos um bolo de lama.", "Agora está na hora de lavar."],
              ["É mole ou duro?", "O que você está fazendo?", "Quer pôr mais água?"],
              "A terra molhada oferece um dos melhores jogos sensoriais: macia, fria, moldável. É um espaço em que bagunça é permitida, o que alivia quem ouve muitos “não”. "
              "Combine antes o fim (“mais cinco minutos e vamos lavar”).",
              atencao="não deixe que ela coma a terra; evite terra de lugares com fezes de animais ou lixo; lave bem as mãos e as unhas depois.",
              variar=["Impressões de pedras e folhas na lama.", "Uma “pista de carrinho” de lama.", "Pintar o tronco com lama (e lavar)."])

    rimas(L, "Bichos de quintal", [
        dict(t="A dona aranha", linhas=["A dona aranha subiu pela parede.", "Veio a chuva forte e a derrubou.", "Já passou a chuva, o sol já vai surgindo,", "e a dona aranha continua a subir.", "Ela é teimosa e desobediente:", "sobe, sobe, sobe e nunca está contente."],
             gesto="os dedos de uma mão “sobem” pelo seu braço; a “chuva” é uma chuva de dedos que derruba; abra as mãos como sol; e os dedos voltam a subir.", origem=TRAD, motivos=["aranha", "nuvem_chuva", "sol"]),
        dict(t="Sapo-cururu", linhas=["Sapo-cururu", "na beira do rio,", "quando o sapo canta, ó maninha,", "é porque tem frio.", "A mulher do sapo", "é quem está lá dentro,", "fazendo rendinha, ó maninha,", "para o casamento."],
             gesto="agache e pule como sapo nos versos “sapo-cururu”; fique quieta e abraçada nos outros, e termine com um sapo bem baixinho.", origem=TRAD, motivos=["m_riacho", "ninfeia"])],
        "A dona aranha é um jogo de dedos que fala de insistir depois de uma queda, o que vale para quem se frustra fácil: ela cai e sobe de novo. O sapo-cururu junta pulos e silêncio. "
        "Cantá-las ao ar livre, olhando a parede ou o rio, liga o verso ao mundo.")

    rimas(L, "Água e formigas", [
        dict(t="Peixe vivo", linhas=["Como pode um peixe vivo", "viver fora da água fria?", "Como poderei viver", "sem a tua, sem a tua, sem a tua companhia?"],
             gesto="faça as mãos de peixe nadando de um lado ao outro; no último verso, abrace-a. Cante devagar, como uma cantiga de ninar.", origem=TRAD, motivos=["peixe", "peixe_azul"]),
        dict(t="Formiguinha", linhas=["Formiguinha, formiguinha,", "leva a folha pro ninho;", "passinho por passinho,", "vai bem devagarzinho."],
             gesto="com dois dedos, “ande” a formiguinha pelo braço dela, bem devagar, até o ombro. No último verso, pare e dê um beijo.", origem=COLECAO, motivos=["formiga", "folha"])],
        "Cantigas de água e de bichos pequenos pedem voz suave e gestos lentos. A da formiguinha termina no “devagarzinho”, o que ajuda a baixar a agitação, e pode ser usada na hora de sair do parque.")

    atividade(L, "Deitar e olhar as nuvens", "acalmar", "5 minutos",
              "uma manta ou toalha na grama, ou o colo; um dia com nuvens",
              cena([("nuvem", 40, 10, 10), ("nuvem", 34, 58, 20), ("sol", 30, 100, 8), ("arvore_verao", 34, 144, 8)], 48, 190),
              ["Estendam a manta e deitem lado a lado, de barriga para cima, no sol brando ou na sombra.", "Fiquem em silêncio um pouco, olhando o céu.", "Procurem formas: “aquela nuvem parece um cachorro?”.",
               "Deixem que ela diga o que vê. Fiquem o quanto ela quiser."],
              ["Olha aquela nuvem. Parece um cachorro!", "Ela está se mexendo, devagar, devagar.", "Que bom ficar aqui deitada, olhando."],
              ["O que a nuvem parece?", "Qual nuvem é a maior?", "Para onde ela vai?"],
              "Deitar e olhar o céu pede quietude sem exigir nada. É um dos jeitos mais gostosos de baixar a agitação depois de correr, e serve também de conversa (o que você vê?). "
              "Boa para o fim de um passeio.",
              atencao="não olhe para o sol; use chapéu e protetor solar; verifique a grama (formigas, espinhos).",
              variar=["À noite, olhando a lua e as estrelas.", "Olhando o balanço das folhas de uma árvore.", "Ouça os sons: o que dá para escutar deitada?"], registro=CAL)

    atividade(L, "Corrida de lesma", "acalmar", "5 minutos",
              "um corredor, uma sala ou o quintal; uma linha de partida e uma de chegada (fita ou cadarço)",
              cena([("caracol", 38, 12, 14), ("pegada", 17, 58, 6), ("pegada_esq", 17, 86, 6), ("caracol", 30, 124, 16), ("tartaruga", 30, 158, 14)], 48, 190),
              ["Explique: “vence quem for o mais devagar”. Mostre andando bem, bem devagar.", "Dê a largada e vão as duas, passo por passo, sem parar.", "Elogie o devagar: “que lesma lenta! Quase parada!”.",
               "Quem chega por último ganha. Repita, trocando de “lesma”."],
              ["Mais devagar… devagar… que lesma!", "Cada pé demora muito, muito tempo.", "Você ganhou: foi a lesma mais lenta!"],
              ["Você é lesma ou lebre?", "Dá para ir mais devagar?", "Quem ganhou?"],
              "Fazer da lentidão uma vitória inverte o jogo: em vez de correr, ela precisa segurar o impulso, o que treina o autocontrole sem que ela perceba. "
              "É ótima antes de uma hora de quietude, ou para entrar numa loja ou consultório sem correr.",
              variar=["Mãos de lesma: mover só as mãos, devagar.", "Voz de lesma: falar bem devagar.", "Deite e “seja uma lesma sonolenta”."], registro=CAL)


# ================================================================== U7 UMA PALAVRA, DOIS JEITOS (Volume 7)

def unidade7(L):
    ativ = [("Oi, hello, bonjour", "conversar", "3 min"), ("Os bichos em três línguas", "nomear", "5 a 8 min"), ("Um, dois, três, pula", "corpo", "5 min"),
            ("Twinkle, twinkle · Frère Jacques · Row, row · Pat-a-cake", "cantar", "2 min cada"),
            ("Boa noite em três línguas", "acalmar", "3 min"), ("Remar o barquinho", "acalmar", "5 min")]
    abertura_unidade(L, 6,
                     "No Volume 7 a Marina ouve inglês e francês por meio de cantigas e palavras. Aos 2 anos, isso vira <b>ouvir uma palavra de um jeito diferente, brincando</b>. "
                     "Um idioma por vez, sem cobrar. As cantigas lentas, como a do barquinho, são boas para acalmar.",
                     ativ, cena([("mao_acenando", 32, 8, 10), ("janela_sol", 30, 46, 14), ("cama", 30, 84, 12), ("porta_aberta", 28, 122, 14), ("carinha_feliz", 26, 156, 14)], 44, 190))

    atividade(L, "Oi, hello, bonjour", "conversar", "3 minutos",
              "um bichinho de pelúcia, ou qualquer pessoa que passar",
              cena([("mao_acenando", 36, 12, 10), ("porta_aberta", 32, 58, 10), ("carinha_feliz", 28, 100, 14), ("janela_sol", 30, 140, 10)], 46, 190),
              ["Cumprimente o bichinho em português: “oi!”. Depois, em outra língua: “hello!”, e acene.", "No outro dia, “bonjour!” (francês). Um idioma por encontro.",
               "Deixe que ela escolha como o bichinho vai dizer oi hoje.", "Na despedida: “tchau”, “bye-bye”, “au revoir”."],
              ["Oi, ursinho! Hello, ursinho!", "Bonjour! É bom-dia em francês.", "Tchau! Bye-bye! Au revoir!"],
              ["Como o ursinho diz oi?", "Quer dizer hello?", "Quem mais a gente cumprimenta?"],
              "Ouvir a mesma ideia em outro jeito, com carinho, prepara o ouvido para os sons de outras línguas. Não cobre pronúncia nem repetição: basta ouvir. "
              "Para a pronúncia, ouça uma gravação de falante nativo ou um dicionário com áudio.",
              variar=["Cumprimente com um beijo, um aperto de mão e um aceno: três jeitos.", "Diga bom dia em cada idioma, em dias diferentes.", "Faça o bichinho dizer tchau em outra língua."])

    atividade(L, "Os bichos em três línguas", "nomear", "5 a 8 minutos",
              "três bichinhos de pelúcia ou figuras: cachorro, gato, peixe",
              cena([("cachorro", 34, 14, 10), ("gato", 32, 58, 14), ("peixe", 34, 104, 16), ("lupa", 26, 148, 14)], 46, 190),
              ["Mostre o cachorro: “cachorro”. Depois: “dog” (inglês) e “chien” (francês).", "Faça o mesmo com o gato (“cat”, “chat”) e com o peixe (“fish”, “poisson”). Um bicho por vez.",
               "Deixe que ela escolha qual bicho vem agora. Repita o nome em um só idioma por dia.", "Termine com os sons: “au-au”, “miau”, “glub”."],
              ["Este é o cachorro. Em inglês, dog.", "Em francês, chien.", "O gato faz miau. Cat, em inglês; chat, em francês."],
              ["Qual bicho é este?", "Como faz o gato?", "Qual você quer hoje?"],
              "Nomear com o objeto na mão é o jeito mais seguro de aprender uma palavra, em qualquer língua. Repetir sempre os mesmos três bichos funciona melhor que aumentar a lista. "
              "Para a pronúncia, use uma gravação de falante nativo: este livro não grava áudio.",
              variar=["Procure os bichos em livros e na rua.", "Vire cartas do Volume 7 e diga o nome.", "Imite o bicho e peça que ela adivinhe."])

    atividade(L, "Um, dois, três, pula", "corpo", "5 minutos",
              "um espaço livre",
              cena([("barra_1", 22, 14, 16), ("barra_2", 22, 44, 16), ("barra_3", 22, 74, 16), ("pegada", 17, 112, 6), ("pegada_esq", 17, 146, 6)], 46, 190),
              ["Fique de frente para ela e diga, em português: “um, dois, três… pula!”, pulando junto.", "Em outro dia, em inglês: “one, two, three… jump!”.", "Em outro, em francês: “un, deux, trois… saute!”.",
               "Deixe que ela dê o sinal de “pula!”."],
              ["Um, dois, três… pula!", "One, two, three… jump!", "Un, deux, trois… saute!"],
              ["Quer pular de novo?", "Quem dá o sinal?", "Pulamos alto ou baixinho?"],
              "Contar com o corpo faz da palavra um movimento, e a criança lembra melhor. É uma brincadeira de pausa e de impulso (esperar o “pula!”), como a estátua. "
              "Um idioma por vez; não precisa corrigir a pronúncia.",
              atencao="pule em chão firme e sem escorregar.",
              variar=["Conte de 1 a 3 batendo palmas.", "Conte os degraus ao subir a escada, em um idioma por dia.", "Pule “até 3” e fique parada como estátua."])

    rimas(L, "Cantigas em inglês e francês", [
        dict(t="Twinkle, twinkle, little star (inglês)", linhas=["Twinkle, twinkle, little star,", "how I wonder what you are!", "Up above the world so high,", "like a diamond in the sky."],
             gesto="abra e feche as mãos como estrelas que piscam; no “up above”, aponte o céu. Em português: brilha, brilha, estrelinha; como eu queria saber o que és, lá no alto.", origem="Poema de Jane Taylor (1806), em domínio público; melodia francesa tradicional.", motivos=["estrela", "lua"]),
        dict(t="Frère Jacques (francês)", linhas=["Frère Jacques, Frère Jacques,", "dormez-vous? Dormez-vous?", "Sonnez les matines! Sonnez les matines!", "Ding, dang, dong. Ding, dang, dong."],
             gesto="balance as mãos como um sino no “ding, dang, dong”; deite a cabeça nas mãos no “dormez-vous?”. Em português: irmão Jacques, você dorme? Toque o sino da manhã.", origem="Cantiga tradicional francesa, de autoria desconhecida e em domínio público.", motivos=["sino", "cama"])],
        "Cantigas antigas, de melodia simples e repetida, são o melhor jeito de ouvir outro idioma. Cante bem baixinho e devagar; a criança aprende a melodia antes da letra. Um idioma por vez.")

    rimas(L, "Mais duas para balançar", [
        dict(t="Row, row, row your boat (inglês)", linhas=["Row, row, row your boat,", "gently down the stream.", "Merrily, merrily, merrily, merrily,", "life is but a dream."],
             gesto="sentadas de frente, de mãos dadas e pernas abertas, balancem para a frente e para trás, remando. Em português: reme, reme o seu barco, devagar pelo rio; felizes, felizes, a vida é um sonho.", origem="Cantiga de domínio público (letra publicada em 1852).", motivos=["barquinho", "m_riacho"]),
        dict(t="Pat-a-cake (inglês)", linhas=["Pat-a-cake, pat-a-cake, baker's man,", "bake me a cake as fast as you can.", "Roll it, and pat it, and mark it with a B,", "and put it in the oven for baby and me."],
             gesto="bata palma com as mãos dela, e depois role as suas mãos uma na outra; “mark it with a B”: desenhe um B no ar. Em português: bata, bata o bolo, padeiro, faça rápido; role e bata e ponha no forno.", origem="Rima inglesa de domínio público (publicada no século XVII).", motivos=["pao", "maos_juntas"])],
        "Remar de mãos dadas é um dos balanços mais calmantes que existem, e a segunda é um jogo de palmas para esperar a vez. Qualquer uma pode ser dita em português se a língua for difícil.")

    atividade(L, "Boa noite em três línguas", "acalmar", "3 minutos",
              "nenhum; luz baixa, cama ou colo",
              cena([("lua", 34, 12, 10), ("estrela", 24, 56, 18), ("cama", 34, 94, 12), ("coracao", 26, 140, 14)], 46, 190),
              ["Antes de dormir, diga boa-noite a tudo que tem no quarto: ao sol, que já foi; à lua, que veio.", "Diga em português: “boa noite”. Em inglês: “good night”. Em francês: “bonne nuit”. Um por noite, ou os três, devagar.",
               "Apague a luz dizendo boa-noite a ela.", "Fique mais um pouco, em silêncio, até ela relaxar."],
              ["Boa noite, sol. Boa noite, lua.", "Good night, Marina.", "Bonne nuit, Marina. Dorme bem."],
              ["Quem vai dormir agora?", "Boa-noite ao ursinho?", "Quer dizer você?"],
              "Um ritual de despedida, sempre igual e em voz baixa, marca o fim do dia e ajuda a criança a se soltar do que a agitou. Misturar o inglês e o francês é só um jeito de a noite virar um momento mágico, sem cobrança.",
              variar=["Boa noite aos bichos, às plantas, às estrelas.", "Um beijo para cada língua.", "Cante a Frère Jacques bem baixinho."], registro=CAL)

    atividade(L, "Remar o barquinho", "acalmar", "5 minutos",
              "um tapete macio; você e ela sentadas de frente, com as pernas abertas",
              cena([("barquinho", 40, 12, 10), ("m_riacho", 40, 60, 24), ("gota", 18, 108, 12), ("coracao", 26, 140, 14)], 46, 190),
              ["Sentem de frente, com as solas dos pés se tocando e as mãos dadas.", "Balancem para a frente e para trás, devagar, como quem rema.", "Cantem baixinho “row, row, row your boat”, ou “reme, reme, reme o barco”.",
               "Terminem com um abraço de “chegamos à margem”."],
              ["Reme, reme, reme o barco, devagar pelo rio.", "Felizes, felizes: a vida é um sonho.", "Chegamos! Que bom."],
              ["Quer remar mais devagar?", "Onde estamos?", "Quer um abraço?"],
              "Balançar de frente, de mãos dadas e olhando uma para a outra, é um jeito antigo e calmo de se conectar, e a cantiga lenta marca o ritmo da respiração. "
              "Funciona bem quando ela está cansada, ou depois de uma crise, como retorno à proximidade.",
              variar=["Com um bichinho no meio, o “passageiro”.", "Em silêncio, só com o balanço.", "Cantando em português."], registro=CAL)


# ================================================================== U8 BRINCAR JUNTO (Volume 8)

def unidade8(L):
    ativ = [("Esconde-esconde", "corpo", "5 a 10 min"), ("A caixa surpresa", "nomear", "5 min"), ("Minha vez, sua vez", "conversar", "5 min"), ("Siga a Marina", "corpo", "5 min"),
            ("Corre, cotia · Cadê? Achou! · A canoa virou · Um elefante", "cantar", "2 min cada"),
            ("A garrafa da calma", "acalmar", "10 min"), ("Respirar com o bichinho", "acalmar", "3 a 5 min")]
    abertura_unidade(L, 7,
                     "No Volume 8 a Marina brinca com os jogos da coleção. Aos 2 anos, isso vira <b>brincar junto: esperar a vez, mandar e obedecer, esconder e achar</b>. "
                     "É a unidade com mais atividades de revezar e de fazer juntas, boas para quem ainda está aprendendo a esperar.",
                     ativ, cena([("caixa", 34, 8, 12), ("lupa", 24, 46, 16), ("dedo_nao", 30, 78, 10), ("polegar_cima", 28, 114, 12), ("maos_juntas", 30, 150, 12)], 44, 190))

    atividade(L, "Esconde-esconde", "corpo", "5 a 10 minutos",
              "uma casa ou um quarto com cantinhos seguros (cortina, atrás da porta, embaixo da mesa)",
              cena([("porta_aberta", 34, 12, 8), ("casinha", 32, 56, 16), ("coracao", 26, 98, 20), ("carinha_feliz", 28, 136, 12)], 46, 190),
              ["Esconda-se atrás da cortina ou da porta, deixando um pedacinho aparecendo, e diga: “cadê a mamãe/o papai?”.", "Quando ela chegar, abrace: “achou!”.", "Troque: ela se esconde, e você procura devagar, fingindo não achar.",
               "Combine um sinal de fim: “mais uma vez e acabou”."],
              ["Cadê o papai? Será que está aqui?", "Achou! Que abraço!", "Agora você se esconde. Eu vou contar até três."],
              ["Onde está o papai?", "Quer se esconder?", "Quer que eu procure?"],
              "Esconder e achar treina a memória e traz a segurança de que quem some, volta. O abraço do “achou!” é um pequeno encontro: ótimo para quem sente a separação. "
              "Conte até três antes de procurar: ela aprende a esperar.",
              atencao="esconderijos seguros: nada de geladeira, caixas fechadas ou lugares pequenos demais.",
              variar=["Esconda um brinquedo.", "Esconda a cabeça e depois apareça.", "Esconda-se e faça um som: ela procura com os ouvidos."])

    atividade(L, "A caixa surpresa", "nomear", "5 minutos",
              "uma caixa de sapato ou de papelão com um buraco do tamanho da mão; 3 ou 4 objetos de casa maiores que o punho dela",
              cena([("caixa", 40, 12, 12), ("mao", 34, 60, 8), ("colher", 30, 100, 16), ("maca", 26, 138, 14), ("tigela", 28, 160, 14)], 48, 190),
              ["Ponha um objeto dentro da caixa, sem que ela veja.", "Peça que ela ponha a mão pelo buraco e apalpe.", "Pergunte: “o que será?”. Aceite “não sei” e dê pistas: “é redondo”, “serve para comer”.",
               "Tire o objeto e comemore: “era uma maçã!”."],
              ["Põe a mão aqui. O que será?", "É redondo e liso… é uma maçã!", "Agora é a sua vez de escolher o que esconder."],
              ["É duro ou mole?", "É grande ou pequeno?", "O que será?"],
              "Sentir sem ver treina o tato e o vocabulário, e “não sei” é uma resposta boa. Ela escolhe o que esconder depois, e liderar o jogo ajuda quem tem muita vontade própria.",
              atencao="só objetos maiores que o punho dela e sem pontas.",
              variar=["Use objetos todos da cozinha.", "Faça pares: o que está na caixa também está na mesa.", "Ela esconde, você adivinha."])

    atividade(L, "Minha vez, sua vez", "conversar", "5 minutos",
              "uma bola leve ou uma meia enrolada; um espaço no chão",
              cena([("circulo_vermelho", 30, 12, 14), ("pegada", 17, 54, 6), ("pegada_esq", 17, 86, 6), ("maos_juntas", 32, 124, 12), ("laranja", 24, 164, 18)], 46, 190),
              ["Sentem no chão, de frente, a uns dois passos. Role a bola devagar para ela: “minha vez!”.", "Quando ela rolar de volta: “sua vez!”.", "Deixe uma pausa e espere. Se ela quiser ficar com a bola, diga “agora é a minha, e depois a sua”.",
               "Aumentem o número de participantes quando ela já souber."],
              ["Minha vez! Lá vai a bola.", "Agora é a sua vez!", "Obrigada por devolver. Que bom brincar com você."],
              ["De quem é a vez?", "Quer rolar forte ou fraco?", "Quem rola agora?"],
              "Esperar a vez é uma das coisas mais difíceis aos 2 anos: a criança tem que segurar o desejo de ter a bola o tempo todo. Revezar com poucas palavras, em jogos curtos, treina essa espera, "
              "e dizer “minha vez / sua vez” dá a ela uma frase para usar com outras crianças. É normal que ela fique brava quando a bola vai embora: nomeie e continue.",
              variar=["Com uma pessoa a mais.", "Role a bola até um bichinho.", "Cantem “minha vez, sua vez” no ritmo."])

    atividade(L, "Siga a Marina", "corpo", "5 minutos",
              "um espaço livre",
              cena([("pegada", 17, 14, 6), ("mao", 34, 52, 10), ("pe", 28, 92, 18), ("estrela", 24, 130, 12), ("coracao", 26, 160, 18)], 46, 190),
              ["Diga: “hoje a Marina é a chefe”. Ela faz um gesto (bater palmas, pular, dar uma volta) e você imita.", "Troque de chefe: agora você faz um gesto e ela imita.", "Combine um gesto especial para parar: mãos no peito.",
               "Termine com os dois gestos preferidos de cada uma."],
              ["A chefe mandou: palmas! Eu faço igual.", "Agora o gesto da chefe é pular.", "A chefe mandou parar? Mãos no peito."],
              ["O que a chefe manda?", "Quer ser chefe ou seguir?", "E agora, o que fazemos?"],
              "Ser “a chefe” permitida, por um tempo e dentro de uma regra, é uma das melhores respostas à fase do “não”: ela exerce o poder que tanto procura. Obedecer ao seu comando também, "
              "como quem segue o jogo. A parada de mãos no peito é uma pausa conhecida.",
              variar=["Siga com músicas.", "Siga em silêncio, só com gestos.", "Chefe bem devagar, chefe bem rápido."])

    rimas(L, "Para brincar de roda", [
        dict(t="Corre, cotia", linhas=["Corre, cotia, na casa da tia,", "corre, cipó, na casa da avó;", "lencinho na mão, caiu no chão."],
             gesto="em roda, com poucas pessoas, uma anda por fora com um lencinho; deixa cair atrás de alguém. Com a Marina, deixe cair atrás dela e corra de mão dada.", origem=TRAD, motivos=["gorro", "casinha"]),
        dict(t="Cadê? Achou!", linhas=["Cadê a Marina?", "Cadê, cadê?", "Está escondida?", "Eu vou achar você!", "Achou! Achou!", "Achou! Achou!"],
             gesto="cubra o rosto dela com um lenço leve (ou o seu com as mãos) nos primeiros versos, e descubra no “achou”. Brinque com paciência: ela pode pedir muitas vezes.", origem=COLECAO, motivos=["olho", "carinha_feliz"])],
        "Brincar de roda reúne rima, corpo e espera. O “cadê? achou!” treina a antecipação (o que vem depois?) e o susto bom.")

    rimas(L, "Mais duas, para contar e rir", [
        dict(t="A canoa virou", linhas=["A canoa virou,", "pois deixaram ela virar;", "foi por causa da Maria", "que não soube remar.", "Se eu fosse um peixinho", "e soubesse nadar,", "eu tirava a Maria", "do fundo do mar."],
             gesto="balançando sentadas, cante e, no “virou”, caiam juntas devagar para o lado, rindo. No fim, “tire” a Marina do fundo do mar com um abraço.", origem=TRAD, motivos=["barquinho", "peixe"]),
        dict(t="Um elefante", linhas=["Um elefante incomoda muita gente;", "dois elefantes incomodam, incomodam muito mais.", "Três elefantes incomodam muita gente;", "quatro elefantes incomodam, incomodam, incomodam muito mais."],
             gesto="mostre os dedos para cada número; cada elefante é uma voz mais grossa. Faça o elefante com o braço de tromba e deixe que ela escolha a voz.", origem=TRAD, motivos=["elefante"])],
        "A canoa e os elefantes são cantigas conhecidas, de jogos de roda. Elas juntam corpo, risada e números. Dá para fazer em qualquer lugar, com qualquer idade, e a Marina pode “conduzir”.")

    atividade(L, "A garrafa da calma", "acalmar", "10 minutos",
              "uma garrafa plástica transparente e pequena, água morna, uma colher de cola líquida transparente, glitter grosso, cola quente e fita",
              cena([("jarra", 34, 14, 10), ("estrela", 24, 58, 6), ("estrela", 20, 80, 24), ("gota", 18, 108, 14), ("coracao", 26, 144, 12)], 48, 190),
              ["Encham a garrafa com água morna até quase o alto. Ela despeja a água e o glitter com a ajuda de um funil ou de uma colher.", "Ponha uma colher de cola líquida: ela deixa o glitter descer devagar.",
               "<b>O adulto fecha a tampa com cola quente e fita</b>, longe dela, e testa se não vaza.", "Chacoalhem juntas e olhem o glitter cair, respirando devagar."],
              ["Vamos fazer uma garrafa mágica.", "Chacoalha… e olha o glitter descer, devagar, devagar.", "Quando fico brava, posso olhar a garrafa e respirar."],
              ["Para onde vai o glitter?", "Está caindo devagar ou depressa?", "Onde vamos guardar a garrafa?"],
              "Ver o glitter descer devagar dá à criança algo para acompanhar com os olhos enquanto respira, e fazer a garrafa juntas a torna “dela”. Guarde no cantinho da calma e use quando ela já estiver mais tranquila, "
              "nunca como castigo nem como distração de uma crise já grande.",
              atencao="só use com você por perto, e troque a garrafa se vazar ou rachar. Não é brinquedo para jogar, morder ou abrir.",
              variar=["Faça cada uma de uma cor (corante de comida).", "Use miçangas grandes seladas, só com o adulto.", "Conte quantas respirações o glitter leva para descer."], registro=CAL)

    atividade(L, "Respirar com o bichinho", "acalmar", "3 a 5 minutos",
              "um bichinho de pelúcia leve; uma manta ou tapete macio",
              cena([("cama", 36, 12, 14), ("lebre", 28, 56, 20), ("nuvem", 34, 98, 10), ("coracao", 26, 142, 14)], 46, 190),
              ["Deitem de barriga para cima. Ponha o bichinho na barriga dela.", "Inspirem pelo nariz, devagar: o bichinho sobe. Expirem pela boca: ele desce.", "Faça junto, com o seu bichinho (ou a mão) na sua barriga.",
               "Repitam cinco vezes. Terminem com um abraço no bichinho."],
              ["O ursinho sobe… e desce.", "Sobe de novo… e desce devagar.", "Que respiração! O bichinho dormiu."],
              ["O bichinho está subindo?", "E agora está descendo?", "Quer fazer de novo?"],
              "Ver o bichinho subir e descer faz a respiração virar algo que ela vê e sente. É a mais antiga das atividades de respiração para crianças, e funciona bem no fim do dia ou depois de uma crise, "
              "quando ela está mais calma.",
              atencao="o bichinho fica só na barriga, nunca no rosto ou no pescoço; leve e sem peças soltas.",
              variar=["Deitem lado a lado, cada uma com um bichinho.", "Cantem “hummm” na expiração.", "Faça de folha: sobe e desce com o vento."], registro=CAL)


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo
    linhas = "".join('<tr><td style="height:15mm;width:24mm"></td><td></td><td></td><td></td></tr>' for _ in range(11))
    c = f"""<div class="miolo">{titulo("O que ajudou a Marina", "um registro de calma, para o adulto preencher", 26)}
      <div class="centro" style="margin:2mm 0">{tira(["bolhas", "estrela", "coracao", "lua"], "17mm", "5mm")}</div>
      <table class="tab" style="margin-top:3mm"><tr><th>Data</th><th>O que aconteceu</th><th>O que ajudou</th><th>Quanto durou</th></tr>{linhas}</table></div>
      {adulto("registrar", "Anote, sem julgar, o que provocou a raiva e o que ajudou a passar: um abraço, a rima, o sopro, o cantinho da calma, um copo de água. Em algumas semanas você vê o que funciona <b>para ela</b>. "
              "Se as crises ficarem muito longas, frequentes ou intensas, leve este registro ao pediatra.")}"""
    L.add(c, aba="--d-frances")

    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Fontes e créditos</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">De onde vêm as ideias e as rimas</h1>
      <h2>Ideias</h2>
      <p>As atividades se inspiram em Charlotte Mason (hábitos, ar livre e os cinco sentidos até os 6 anos; <i>Home Education</i>, 1886), na pedagogia Waldorf (imitação, ritmo e jogos de dedos), na educação Montessori em casa
      (vida prática e nomear objetos reais) e nos campos de experiência da BNCC para a educação infantil. As orientações sobre telas e sobre a “crise dos dois anos” seguem a Sociedade Brasileira de Pediatria e materiais de pediatria e de
      psiquiatria infantil. <b>São inspirações, não regras</b>, e a leitura foi feita em páginas de divulgação, não nos textos originais: confira com o pediatra da Marina (ADR 0021).</p>
      <h2>Rimas, parlendas e cantigas</h2>
      <p><b>Tradicionais brasileiras</b>, de autoria desconhecida, de transmissão oral, com muitas variações regionais: <i>Mindinho, seu vizinho</i>; <i>Borboletinha</i>; <i>Cadê o toucinho?</i>; <i>O cravo brigou com a rosa</i>;
      <i>Um, dois, feijão com arroz</i>; <i>Pirulito que bate, bate</i>; <i>Marcha, soldado</i>; <i>Ciranda, cirandinha</i>; <i>Se essa rua fosse minha</i>; <i>Meu limão, meu limoeiro</i>; <i>O sapo não lava o pé</i>;
      <i>A dona aranha</i>; <i>Sapo-cururu</i>; <i>Peixe vivo</i>; <i>Corre, cotia</i>; <i>A canoa virou</i>; <i>Um elefante incomoda muita gente</i>. A versão da letra pode variar da que você conhece.</p>
      <p><b>Em inglês e francês, de domínio público:</b> <i>Twinkle, twinkle, little star</i> (Jane Taylor, 1806), <i>Frère Jacques</i> (tradicional francesa), <i>Row, row, row your boat</i> (letra de 1852) e <i>Pat-a-cake</i> (rima inglesa do século XVII).
      As traduções em português são da coleção.</p>
      <p><b>Escritas pela coleção:</b> <i>Bom dia, sol</i>; <i>Estou com raiva</i>; <i>Quantos dedinhos?</i>; <i>Grande e pequeno</i>; <i>As cores</i>; <i>Mão suja, mão limpa</i>; <i>Devagar, devagarinho</i>; <i>Formiguinha</i>; <i>Cadê? Achou!</i>;
      o acalanto da unidade 4 e a história do gatinho da unidade 2.</p>
      <h2>Ilustração</h2>
      <p>Todas as figuras são motivos em aquarela da coleção (<i>editorial/motivos*.py</i>). Nenhum dado de criança ou de família é coletado ou enviado.</p>""")

    c = f"""<div class="miolo centro" style="top:60mm">
      <div style="font-size:11pt;letter-spacing:.3em;text-transform:uppercase;color:var(--sepia)">Até logo</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">Brincar é o trabalho dela</div>
      <div class="vinheta-sep">❦</div>
      <p style="font-size:13pt;font-style:italic;color:var(--sepia);max-width:120mm;margin:6mm auto">Quando ela disser “não”, respire. Quando ela disser “de novo”, repita. E quando ela disser “mamãe” ou “papai”, deixe tudo e olhe.</p>
      <div style="margin:10mm auto 0">{tira(ICONES, "20mm", "2mm")}</div>
      <div style="margin-top:12mm;font-size:10pt;color:var(--sepia)">Caderno de atividades · volte aos Volumes 1 a 8 da coleção quando ela crescer</div></div>"""
    L.add(c, cabecalho=False, numero=False)


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8)


def montar(unidades=None):
    L = Caderno()
    capa(L); rosto(L); carta(L); como_usar(L)
    fase_do_nao(L)
    cantinho_calma(L)
    semana(L)
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
