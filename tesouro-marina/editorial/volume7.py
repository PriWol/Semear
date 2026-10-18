"""
VOLUME 7 — PRIMEIRAS LÍNGUAS
uso: python3 volume7.py            (monta o volume com as unidades já escritas; ver UNIDADES_PRONTAS)
Inglês e francês em unidades paralelas, com o latim como cultura (docs/01-arquitetura-curricular.md, §4). Cada cartão e cada página traz
um idioma por vez, sempre rotulado. As ilustrações são gravuras de domínio público (fontes_v1.py: Greenaway e Boutet de Monvel) e
motivos em aquarela da coleção (motivos8.py); ver ADR 0020.
"""
import os
import subprocess
import sys

from livro import (Livro, VERSAO, adulto, cartoes, credito_pd, gerar_pdf, guia, img, pd, texto, titulo)
from volume6 import cena, tira   # composição de motivos em posição livre e fila de motivos: os mesmos dos outros volumes
import fontes_v1

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume7")

UNIDADES = [
    ("Unidade 1 · Cumprimentos", "--d-ingles"),
    ("Unidade 2 · A família", "--d-frances"),
    ("Unidade 3 · A casa", "--d-latim"),
    ("Unidade 4 · A comida", "--d-vida"),
    ("Unidade 5 · Os animais", "--d-natureza"),
    ("Unidade 6 · As cores", "--d-artes"),
    ("Unidade 7 · O corpo", "--d-historias"),
    ("Unidade 8 · A natureza", "--d-memoria"),
]
INICIO = {}
# gravuras de domínio público que entram no volume (os créditos da última página saem desta lista)
USADOS = ("greenaway_pelicoes", "monvel_polichinelle", "monvel_polichinelle_cena")
INGLES, FRANCES, LATIM = "--d-ingles", "--d-frances", "--d-latim"


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


def rotulo(idioma, cor):
    """Etiqueta de idioma: nenhum texto estrangeiro aparece sem ela."""
    return (f'<span style="display:inline-block;font-size:7.6pt;text-transform:uppercase;letter-spacing:.12em;color:#fff;background:var({cor});'
            f'border-radius:1.2mm;padding:.3mm 2mm;vertical-align:middle">{idioma}</span>')


def versos(idioma, cor, linhas, lang=None):
    """Bloco de versos com a etiqueta do idioma; `lang` marca o idioma do texto para o leitor de tela e para a hifenização."""
    marca = f' lang="{lang}"' if lang else ""
    return (f'<div style="text-align:center">{rotulo(idioma, cor)}'
            f'<p{marca} style="font-size:14pt;line-height:1.42;font-style:italic;margin:2mm 0 0">' + "<br>".join(linhas) + "</p></div>")


def duas_colunas(esq, dir):
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:4mm;padding-top:3mm;border-top:0.4pt solid var(--linha)">{esq}{dir}</div>'


# ================================================================== ABERTURA

def capa(L):
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 7</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">Primeiras<br>línguas</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:146mm;left:0;right:0">{pd("monvel_polichinelle_cena", "118mm", "margin:0 auto")}</div>
    <div class="centro" style="position:absolute;top:258mm;left:0;right:0;line-height:0">{tira(["mao_acenando", "janela_sol", "cama", "porta_aberta"], "15mm", "3mm")}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 7</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">Primeiras línguas</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">O livro de línguas é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0">{tira(["mao_acenando", "janela_sol", "cama", "porta_aberta"], "30mm", "3mm")}</div>
      <div style="margin-top:12mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Uma língua de cada vez, cantando</h1>
      <p>Este volume apresenta à Marina o <b>inglês</b> e o <b>francês</b> do jeito que se aprende a primeira língua: ouvindo, repetindo, cantando e brincando, com as palavras
      ligadas a coisas, gestos e histórias. Não é aula, não tem prova, e <b>não substitui nada do que a escola faz</b>. São poucos minutos, de vez em quando, sem pressa.</p>
      <h2>Três ideias</h2>
      <ul>
        <li><b>Um idioma por vez.</b> Num encontro, só inglês ou só francês. Cada cartão e cada página traz uma etiqueta com o nome da língua, e o livro nunca mistura idiomas numa frase
        sem avisar. Assim a criança aprende que são “maneiras de dizer” diferentes, e você não precisa explicar nada.</li>
        <li><b>Cantigas e rimas.</b> Repetir um verso curto, com ritmo, é o jeito mais antigo de guardar palavras (e vem de Bauer e Wise, e de Suzuki). Só entram letras de domínio público.
        Quando a melodia está no livro, ela é a original de uma partitura antiga; quando não, a página diz que a rima é para dizer, não para cantar.</li>
        <li><b>O latim como cultura.</b> O latim aparece pequeno, no verso dos cartões e numa seção própria no fim: lemas, números romanos e as “palavras-mãe” do português.
        Ele não é para ser aprendido agora, e sim para a Marina, mais tarde, reconhecer de onde vêm as palavras.</li>
      </ul>
      <h2>Se você não fala inglês ou francês</h2>
      <p>Não faz mal. A criança pequena se beneficia de ouvir a língua com carinho, mesmo com sotaque; e vocês podem descobrir juntos. Para a pronúncia, use um dicionário com áudio ou
      uma gravação de falante nativo: o livro não grava nada, e as dicas do verso dos cartões são só um apoio.</p>
      <h2>O que este volume traz</h2>
      <p>""" + ("Esta é uma edição em produção: por enquanto, a primeira unidade (<i>cumprimentos</i>), com uma rima ou canção, cartões com o verso em inglês, francês e latim, um jogo e uma rotina curta. "
                "O volume completo terá oito unidades (<i>cumprimentos</i>, <i>a família</i>, <i>a casa</i>, <i>a comida</i>, <i>os animais</i>, <i>as cores</i>, <i>o corpo</i> e <i>a natureza</i>) e uma seção de latim."
                if parcial() else
                "Oito unidades, uma para cada tema — <i>cumprimentos</i>, <i>a família</i>, <i>a casa</i>, <i>a comida</i>, <i>os animais</i>, <i>as cores</i>, <i>o corpo</i> e <i>a natureza</i> — e, "
                "em cada uma, uma rima ou canção, cartões com o verso em inglês, francês e latim, um jogo e uma rotina curta.") + """</p>
      <div class="centro" style="margin-top:6mm">""" + tira(["mao_acenando", "janela_sol", "cama", "porta_aberta", "carinha_feliz"], "22mm", "2mm") + "</div>")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Pouco, sempre, e na hora certa</h1>
      <p>Separe uma caixa para os cartões recortados, um lugar na parede para pendurar os da semana e, se tiver, uma porta de papelão para o jogo da primeira unidade.
      Use o cumprimento <b>na hora em que ele acontece</b>: <i>bom dia</i> ao acordar, <i>boa noite</i> ao dormir. É assim que a palavra gruda na vida.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Dois encontros por semana, de 5 a 10 minutos, dentro do tempo da família. Uma unidade dura de 2 a 3 fins de semana. Repetir é o método.</td></tr>
        <tr><th>Um idioma</th><td>Cada encontro usa um só idioma. Alterne: uma semana inglês, outra francês. Os cartões de cada idioma ficam do mesmo lado da caixa.</td></tr>
        <tr><th>A ordem</th><td>Primeiro ouvir (a rima ou a canção, várias vezes), depois mostrar o cartão, depois o jogo. Só então, se ela quiser, repetir a palavra. <b>Nunca peça para “dizer em inglês”.</b></td></tr>
        <tr><th>Erros</th><td>Se ela misturar as línguas, ótimo: está brincando com elas. Repita a forma certa sem corrigir (“<i>sim, bonjour!</i>”) e siga em frente.</td></tr>
        <tr><th>Cartões</th><td>A frente traz a figura e a palavra em português. O verso, para o adulto, traz a palavra em inglês, em francês e em latim, cada uma com a sua etiqueta.</td></tr>
        <tr><th>Latim</th><td>Cultura, não matéria. As palavras latinas são curiosidades; <b>ninguém cobra</b> nem espera que a criança as repita.</td></tr>
      </table>
      <div class="centro" style="margin-top:6mm">{tira(["mao_acenando", "janela_sol", "cama", "porta_aberta"], "22mm")}</div>""")


def parcial(inicio=None):
    """Verdadeiro enquanto faltam unidades: o workflow publica o PDF a cada merge, e ele não pode prometer o que não tem."""
    return len(UNIDADES_PRONTAS) < len(UNIDADES) if inicio is None else not all(n in inicio for n, _ in UNIDADES)


def sumario(inicio):
    feitas = [(n, cor) for n, cor in UNIDADES if n in inicio]
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio[n]}</td></tr>' for n, cor in feitas)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    aviso = ('<p class="peq centro" style="margin-top:6mm;font-style:italic">Edição em produção: as demais unidades e a seção de latim ainda não estão neste arquivo.</p>'
             if parcial(inicio) else "")
    return f"""<div class="miolo">{titulo("Sumário", "Volume 7 · Primeiras línguas", 30)}<table class="sumario">{linhas}</table>{aviso}
      <div class="centro" style="margin-top:8mm">{tira(["mao_acenando", "janela_sol", "cama", "porta_aberta", "porta", "carinha_feliz"], "22mm", "1.5mm")}</div></div>"""


# ================================================================== U1 CUMPRIMENTOS

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · Cumprimentos", aba=INGLES,
        pergunta="Como se diz olá, por favor e obrigado em outras línguas, e quando se diz cada coisa?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · um idioma por encontro (inglês num, francês no outro).",
        objetivos=["Ouvir uma rima inglesa e uma canção francesa, várias vezes, sem pedir que repita.", "Acenar e dizer o cumprimento certo ao chegar e ao sair.",
                   "Ligar o cumprimento à hora do dia: de manhã, à tarde e à noite.", "Brincar de bater à porta e responder, no jogo.", "Conhecer nove expressões nas duas línguas, com <i>salvē</i> e <i>valē</i> como curiosidade."],
        repertorio="<b>Em português:</b> olá, bom dia, boa noite, tchau, por favor, obrigado, sim, não, tudo bem? <b>Rima em inglês:</b> as senhoritas Pelicoe, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>La Polichinelle</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>salvē</i> (olá), <i>valē</i> (adeus), <i>grātiās</i> (obrigado).",
        materiais="Os cartões da unidade recortados, uma porta de papelão (ou uma folha de papel dobrada), a rotina do dia no fim da unidade, e a sua voz.",
        vida="Cumprimentar na hora certa e no idioma da semana: <i>bom dia</i> ao acordar, <i>boa noite</i> ao dormir, <i>tchau</i> e <i>até logo</i> na porta de casa.",
        etapas=[["Escutar a rima inglesa e a canção francesa, uma de cada vez.", "Olhar a gravura e acenar junto.", "Mostrar o cartão <i>olá</i> e dizer a palavra no idioma da semana."],
                ["Ligar cada cartão à hora do dia (manhã, tarde, noite).", "Parear o cartão com a figura da rotina.", "Dizer <i>sim</i> ou <i>não</i> com o cartão certo, no jogo."],
                ["Bater à porta e escolher o cumprimento.", "Cumprimentar um ursinho, uma boneca ou o ratinho.", "Inventar uma pergunta para quem chega (“quem é?”)."]],
        indicadores=["Acena ao ver alguém, sem ser lembrada.", "Escolhe o cartão <i>bom dia</i> de manhã e <i>boa noite</i> à noite.", "Repete o verso da rima ou o “pan!” da canção.",
                     "Brinca de bater à porta e esperar a resposta.", "Reconhece a figura do cartão antes de ouvir a palavra.", "Pergunta como se diz outra coisa em outro idioma."],
        interesse="cumprimentar em duas línguas no mesmo dia (uma de manhã, outra à noite) e fazer um cartaz com os cumprimentos da casa.",
        dificil="só o cartão <i>olá</i>, com o aceno, no idioma da semana. Uma palavra basta.",
        alerta="O inglês e o francês não precisam sair perfeitos: a pronúncia da criança melhora ouvindo a língua, não sendo corrigida. Não use o idioma como cobrança nem como castigo."))

    # ---- rima inglesa
    L.add(f"""<div class="miolo">{titulo("As doze senhoritas Pelicoe", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", 24)}
      <div class="centro" style="margin:3mm 0 0">{pd("greenaway_pelicoes", "92mm", "margin:0 auto")}</div>
      {duas_colunas(versos("inglês", INGLES, ["The twelve Miss Pelicoes", "Were always most polite,—", "Said “If you please,” and “Many thanks,”", "“Good morning,” and “Good night.”"], "en"),
                    versos("português · tradução da coleção", INGLES, ["As doze senhoritas Pelicoe", "eram sempre muito educadas:", "diziam “por favor” e “muito obrigada”,", "“bom dia” e “boa noite”."]))}</div>
      {adulto("uma rima para dizer",
              "Diga os versos devagar, com a gravura aberta, e peça que ela acene para as meninas. Esta é uma rima do livro <i>Under the Window</i>, de Kate Greenaway (1878, domínio público): "
              "o livro não traz melodia, e a coleção não inventa uma, por isso é para <b>dizer</b>, marcando o ritmo com palmas. <i>Miss</i> quer dizer “senhorita”, e <i>Pelicoe</i> é um sobrenome inventado. "
              "Mostre as quatro expressões que aparecem: <i>if you please</i> (por favor), <i>many thanks</i> (muito obrigada), <i>good morning</i> (bom dia) e <i>good night</i> (boa noite).",
              credito_pd("greenaway_pelicoes"))}""", aba=INGLES)

    # ---- canção francesa
    L.add(f"""<div class="miolo">{titulo("Pan ! Qu’est-c’ qu’est là ?", "canção tradicional francesa · a partitura é a original de 1883", 24)}
      <div class="centro" style="margin:3mm 0 0">{pd("monvel_polichinelle", "150mm", "margin:0 auto")}</div>
      {duas_colunas(versos("francês", FRANCES, ["Pan ! qu’est-c’ qu’est là ?", "C’est Polichinelle,", "Mam’selle.", "Pan ! qu’est-c’ qu’est là ?", "C’est Polichinell’ que v’là."], "fr"),
                    versos("português · tradução da coleção", FRANCES, ["Pan! Quem está aí?", "É o Polichinelo,", "senhorita.", "Pan! Quem está aí?", "É o Polichinelo que chegou."]))}</div>
      {adulto("uma canção para cantar",
              "A melodia é a que está impressa na página: a linha de cima (<i>chant</i>, “canto”) é a voz, e a de baixo é o acompanhamento de piano de Charles-Marie Widor, que você pode deixar de lado. "
              "<i>Allegretto moderato</i> pede um andamento animado, sem pressa. No “pan!”, bata na mesa ou numa porta, como quem chega. <i>Mam’selle</i> é <i>mademoiselle</i> (“senhorita”), "
              "e Polichinelo é um bufão dos teatros de fantoches. A letra é tradicional; a gravura é de Boutet de Monvel (1883).",
              credito_pd("monvel_polichinelle"))}""", aba=FRANCES)

    # ---- cartões
    itens = [dict(pt="olá", mot="mao_acenando", en="hello", fr="bonjour", la="salvē", dica="em francês, <i>bonjour</i> serve de manhã e de tarde; os romanos diziam <i>salvē</i>"),
             dict(pt="bom dia", mot="janela_sol", en="good morning", fr="bonjour", la="salvē", dica="os romanos diziam <i>salvē</i> a qualquer hora do dia"),
             dict(pt="boa noite", mot="cama", en="good night", fr="bonne nuit", la="<span class='peq'>sem fórmula fixa</span>", dica="diz-se ao ir dormir; ao chegar à noite, em francês, é <i>bonsoir</i>"),
             dict(pt="tchau", mot="porta_aberta", en="goodbye", fr="au revoir", la="valē", dica="<i>au revoir</i> quer dizer “até nos vermos de novo”"),
             dict(pt="por favor", mot="maos_juntas", en="please", fr="s’il vous plaît", la="quaesō", dica="<i>s’il vous plaît</i>: “se lhe agrada”"),
             dict(pt="obrigado", mot="coracao", en="thank you", fr="merci", la="grātiās", dica="<i>grātiās</i> é a palavra-mãe de “graças”"),
             dict(pt="sim", mot="polegar_cima", en="yes", fr="oui", la="ita", dica="<i>oui</i> lê-se quase “ui”"),
             dict(pt="não", mot="dedo_nao", en="no", fr="non", la="nōn", dica="<i>non</i>, em francês e em latim, é a origem do nosso “não”"),
             dict(pt="tudo bem?", mot="carinha_feliz", en="how are you?", fr="ça va ?", la="quid agis?", dica="<i>ça va ?</i> serve de pergunta e de resposta: “<i>ça va !</i>”")]
    cartoes(L, "cumprimentos", itens, "Volume 7 · Cumprimentos",
            nota_latim="Latim: vogal com traço (ā, ē, ī, ō, ū) é longa · os romanos usavam estas fórmulas; aqui são só curiosidade, ninguém precisa decorar")

    # ---- jogo e rotina
    horas = (("dia_amanhecer", "de manhã", "bom dia", "good morning", "bonjour"), ("dia_meiodia", "à tarde", "boa tarde", "good afternoon", "bonjour"),
             ("dia_entardecer", "ao anoitecer", "boa noite", "good evening", "bonsoir"), ("dia_noite", "para dormir", "boa noite", "good night", "bonne nuit"))
    linhas = "".join(f'<tr><td style="width:28mm">{img(m, "22mm")}</td><td style="font-size:11.5pt;font-style:italic">{q}<br><b style="font-style:normal;font-size:12.5pt">{pt}</b></td>'
                     f'<td lang="en" style="font-size:12.5pt">{en}</td><td lang="fr" style="font-size:12.5pt">{fr}</td></tr>' for m, q, pt, en, fr in horas)
    L.add(f"""<div class="miolo">{titulo("Toc, toc! Quem é?", "um jogo de porta e uma rotina do dia", 26)}
      <div class="centro" style="margin:1mm 0 2mm">{cena([("porta", 42, 8, 0), ("mao_acenando", 36, 58, 10), ("porta_aberta", 42, 100, 0), ("carinha_feliz", 28, 140, 14)], 48)}</div>
      <h2 class="titulo" style="font-size:14pt;text-align:left;margin:2mm 0 1mm">O jogo da porta</h2>
      <ol style="font-size:11.5pt;line-height:1.4;padding-left:6mm;margin:0">
        <li>O adulto fica atrás de uma porta (de verdade ou de papel dobrado) e bate: <i>toc, toc!</i></li>
        <li>Marina pergunta “<i>quem é?</i>” (em português; a pergunta não troca de idioma).</li>
        <li>O adulto responde com um cumprimento do idioma da semana (por exemplo, “<i>hello!</i>” ou “<i>bonjour!</i>”), abre a porta e acena. Depois trocam de lugar.</li>
        <li>Marina escolhe um cartão e o adulto adivinha o cumprimento. Quem erra, ri.</li>
      </ol>
      <h2 class="titulo" style="font-size:14pt;text-align:left;margin:4mm 0 1mm">A rotina do dia</h2>
      <table class="tab"><tr><th></th><th>quando</th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th></tr>{linhas}</table></div>
      {adulto("jogo e rotina",
              "A rotina é uma só: <b>cumprimentar na hora certa</b>, no idioma da semana, sempre com o mesmo gesto. Em português, o “boa noite” serve para chegar e para dormir; em francês, são duas palavras "
              "(<i>bonsoir</i> ao chegar, <i>bonne nuit</i> para dormir), e em inglês também (<i>good evening</i> e <i>good night</i>). Se a Marina já entende, peça que ela escolha, entre dois cartões, o que combina com a figura.")}""", aba="--d-jogos")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo

    gravuras = "".join(f"<li>{fontes_v1.credito(n)}</li>" for n in USADOS)
    c = f"""<div class="miolo texto">{titulo("Rimas, canções e créditos", "Volume 7", 26)}
      <h2>Letras e partituras</h2>
      <p style="font-size:9.4pt">A rima das senhoritas Pelicoe é de Kate Greenaway (1846–1901), em <i>Under the Window</i> (1878), e está em domínio público. <i>La Polichinelle</i> (<i>Pan ! qu’est-c’ qu’est là ?</i>) é uma canção
      tradicional francesa; a partitura reproduzida é a de <i>Vieilles chansons pour les petits enfants</i> (1883), com os acompanhamentos de Charles-Marie Widor (1844–1937), em domínio público. As traduções são da coleção.
      Nenhuma letra de canção moderna, e nenhuma melodia que não esteja impressa numa partitura antiga, entra neste livro.</p>
      <h2>Ilustrações em domínio público</h2>
      <p style="font-size:9pt">Digitalizações do Internet Archive, só recortadas e reduzidas; nenhuma pintura foi retocada. Cada página foi conferida por SHA-256 antes de entrar no livro.</p>
      <ul style="font-size:8.4pt;line-height:1.3">{gravuras}</ul>
      <h2>Fundamentos</h2><p style="font-size:9.4pt">Cantigas e rimas para guardar palavras (Susan Wise Bauer e Jessie Wise); ouvir muito antes de falar, com a família como ambiente (Shinichi Suzuki); o latim como cultura, sem cobrança (Charlotte Mason,
      Dorothy Sayers). Nenhum material reproduz métodos ou produtos comerciais.</p>
      <h2>Ilustrações da coleção</h2><p style="font-size:9.4pt">Mão, porta, janela, cama, carinha e demais desenhos: aquarela digital procedural da coleção (nove motivos novos para este volume, e outros já usados antes). Tipografia: EB Garamond (licença OFL).</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 7</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">jogos para recortar, projetos para fazer em casa<br>e um diário de observação, para guardar<br>tudo o que a Marina descobriu.</p>
      <div style="margin-top:12mm">{tira(["livro", "estrela", "sino", "pena"], "28mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 8 · Jogos e descobertas</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1,)


def montar(unidades=None):
    L = Livro(7, "Primeiras línguas")
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
    for versao, nome in (("impressao", "volume7-impressao"), ("tela", "volume7-tela")):
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume7-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
