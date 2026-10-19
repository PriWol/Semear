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

import re

from motivos8 import MOTIVOS8
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
INGLES, FRANCES, LATIM = "--d-ingles", "--d-frances", "--d-latim"
NOTA_LATIM = "Latim: vogal com traço (ā, ē, ī, ō, ū) é longa · só curiosidade: ninguém precisa decorar"   # para os conjuntos em que todo cartão tem palavra latina


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
    tam = 14 if len(linhas) <= 6 else 12.2   # estrofes longas ficam menores para a página caber
    return (f'<div style="text-align:center">{rotulo(idioma, cor)}'
            f'<p{marca} style="font-size:{tam}pt;line-height:1.4;font-style:italic;margin:2mm 0 0">' + "<br>".join(linhas) + "</p></div>")


def pagina_verso(L, t, sub, gravura, larg, idioma, cor, lang, original, traducao, rotulo_adulto, texto_adulto, aba, extra=""):
    """Página de rima ou canção: a gravura, o original e a tradução lado a lado (um idioma por bloco) e a nota do adulto."""
    L.add(f"""<div class="miolo">{titulo(t, sub, 24)}
      <div class="centro" style="margin:3mm 0 0">{pd(gravura, f"{larg}mm", "margin:0 auto")}</div>
      {duas_colunas(versos(idioma, cor, original, lang), versos("português · tradução da coleção", cor, traducao))}{extra}</div>
      {adulto(rotulo_adulto, texto_adulto, credito_pd(gravura))}""", aba=aba)


def passos_txt(itens, tam=11.5):
    return f'<ol style="font-size:{tam}pt;line-height:1.4;padding-left:6mm;margin:0">' + "".join(f"<li>{i}</li>" for i in itens) + "</ol>"


def subtitulo_h(t):
    return f'<h2 class="titulo" style="font-size:14pt;text-align:left;margin:4mm 0 1mm">{t}</h2>'


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
    if "Latim" in inicio:
        linhas += f'<tr><td><span class="bolinha" style="background:var(--d-latim)"></span>Latim</td><td style="font-size:13pt">De onde vêm as palavras</td><td class="pg">{inicio["Latim"]}</td></tr>'
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

    pagina_verso(L, "As doze senhoritas Pelicoe", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_pelicoes", 92, "inglês", INGLES, "en",
                 ["The twelve Miss Pelicoes", "Were always most polite,—", "Said “If you please,” and “Many thanks,”", "“Good morning,” and “Good night.”"],
                 ["As doze senhoritas Pelicoe", "eram sempre muito educadas:", "diziam “por favor” e “muito obrigada”,", "“bom dia” e “boa noite”."],
                 "uma rima para dizer",
                 "Diga os versos devagar, com a gravura aberta, e peça que ela acene para as meninas. Esta é uma rima do livro <i>Under the Window</i>, de Kate Greenaway (1878, domínio público): "
                 "o livro não traz melodia, e a coleção não inventa uma, por isso é para <b>dizer</b>, marcando o ritmo com palmas. <i>Miss</i> quer dizer “senhorita”, e <i>Pelicoe</i> é um sobrenome inventado. "
                 "Mostre as quatro expressões que aparecem: <i>if you please</i> (por favor), <i>many thanks</i> (muito obrigada), <i>good morning</i> (bom dia) e <i>good night</i> (boa noite).", INGLES)

    pagina_verso(L, "Pan ! Qu’est-c’ qu’est là ?", "canção tradicional francesa · a partitura é a original de 1883", "monvel_polichinelle", 150, "francês", FRANCES, "fr",
                 ["Pan ! qu’est-c’ qu’est là ?", "C’est Polichinelle,", "Mam’selle.", "Pan ! qu’est-c’ qu’est là ?", "C’est Polichinell’ que v’là."],
                 ["Pan! Quem está aí?", "É o Polichinelo,", "senhorita.", "Pan! Quem está aí?", "É o Polichinelo que chegou."],
                 "uma canção para cantar",
                 "A melodia é a que está impressa na página: a linha de cima (<i>chant</i>, “canto”) é a voz, e a de baixo é o acompanhamento de piano de Charles-Marie Widor, que você pode deixar de lado. "
                 "<i>Allegretto moderato</i> pede um andamento animado, sem pressa. No “pan!”, bata na mesa ou numa porta, como quem chega. <i>Mam’selle</i> é <i>mademoiselle</i> (“senhorita”), "
                 "e Polichinelo é um bufão dos teatros de fantoches. A letra é tradicional; a gravura é de Boutet de Monvel (1883).", FRANCES)

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

    horas = (("dia_amanhecer", "de manhã", "bom dia", "good morning", "bonjour"), ("dia_meiodia", "à tarde", "boa tarde", "good afternoon", "bonjour"),
             ("dia_entardecer", "ao anoitecer", "boa noite", "good evening", "bonsoir"), ("dia_noite", "para dormir", "boa noite", "good night", "bonne nuit"))
    linhas = "".join(f'<tr><td style="width:28mm">{img(m, "22mm")}</td><td style="font-size:11.5pt;font-style:italic">{q}<br><b style="font-style:normal;font-size:12.5pt">{pt}</b></td>'
                     f'<td lang="en" style="font-size:12.5pt">{en}</td><td lang="fr" style="font-size:12.5pt">{fr}</td></tr>' for m, q, pt, en, fr in horas)
    L.add(f"""<div class="miolo">{titulo("Toc, toc! Quem é?", "um jogo de porta e uma rotina do dia", 26)}
      <div class="centro" style="margin:1mm 0 2mm">{cena([("porta", 42, 8, 0), ("mao_acenando", 36, 58, 10), ("porta_aberta", 42, 100, 0), ("carinha_feliz", 28, 140, 14)], 48)}</div>
      {subtitulo_h("O jogo da porta")}
      {passos_txt(["O adulto fica atrás de uma porta (de verdade ou de papel dobrado) e bate: <i>toc, toc!</i>", "Marina pergunta “<i>quem é?</i>” (em português; a pergunta não troca de idioma).",
                   "O adulto responde com um cumprimento do idioma da semana (por exemplo, “<i>hello!</i>” ou “<i>bonjour!</i>”), abre a porta e acena. Depois trocam de lugar.",
                   "Marina escolhe um cartão e o adulto adivinha o cumprimento. Quem erra, ri."])}
      {subtitulo_h("A rotina do dia")}
      <table class="tab"><tr><th></th><th>quando</th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th></tr>{linhas}</table></div>
      {adulto("jogo e rotina",
              "A rotina é uma só: <b>cumprimentar na hora certa</b>, no idioma da semana, sempre com o mesmo gesto. Em português, o “boa noite” serve para chegar e para dormir; em francês, são duas palavras "
              "(<i>bonsoir</i> ao chegar, <i>bonne nuit</i> para dormir), e em inglês também (<i>good evening</i> e <i>good night</i>). Se a Marina já entende, peça que ela escolha, entre dois cartões, o que combina com a figura.")}""", aba="--d-jogos")


# ================================================================== U2 A FAMÍLIA

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · A família", aba=INGLES,
        pergunta="Como se chamam, em outras línguas, as pessoas de quem a gente gosta?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · inglês num encontro, francês no outro.",
        objetivos=["Ouvir uma rima inglesa sobre uma irmã e uma canção de ninar francesa, várias vezes.", "Apontar o cartão certo quando o adulto diz mãe, pai, bebê, irmão, irmã, avó.",
                   "Dizer a palavra do idioma da semana ao abraçar alguém.", "Cantar <i>Frère Jacques</i> em roda, como brincadeira.", "Conhecer a palavra-mãe latina de “mãe”, “pai” e “irmão”, só como curiosidade."],
        repertorio="<b>Em português:</b> mãe, pai, bebê, irmão, irmã, avó, família, abraço, amor. <b>Rima em inglês:</b> o carrinho da irmãzinha, de Kate Greenaway (1878). "
                   "<b>Canções em francês:</b> <i>Fais dodo, Colas</i> e <i>Frère Jacques</i>, tradicionais, com as partituras de 1883. <b>Latim:</b> <i>māter</i>, <i>pater</i>, <i>frāter</i>, <i>soror</i>.",
        materiais="Os cartões da unidade recortados, fotos da família (ou desenhos), uma caixa de sapatos para guardar os cartões e, se tiver, um bebê de brinquedo para o jogo.",
        vida="Dizer a palavra no idioma da semana ao abraçar (<i>hug</i> ou <i>câlin</i>) e ao apresentar as pessoas da casa, sem pedir que ela repita.",
        etapas=[["Escutar a rima e a canção de ninar, de colo, devagar.", "Olhar a gravura e dizer quem é quem.", "Mostrar o cartão e dizer a palavra no idioma da semana."],
                ["Espalhar os cartões e apontar o que o adulto diz.", "Parear o cartão com uma foto da família.", "Cantar <i>Frère Jacques</i> em roda."],
                ["Fazer um cartaz da família com fotos e os cartões.", "Apresentar a família ao ursinho: “esta é a mamãe”.", "Inventar uma canção de ninar com os nomes da casa."]],
        indicadores=["Aponta o cartão certo quando ouve a palavra.", "Reconhece a mãe, o bebê e os irmãos nas gravuras.", "Embala o bebê de brinquedo cantando baixinho.",
                     "Diz a palavra do idioma da semana espontaneamente, ao abraçar.", "Segura a mão de alguém na roda de <i>Frère Jacques</i>.", "Pergunta “quem é?” diante de uma foto."],
        interesse="olhar as fotos antigas da família e dizer, no idioma da semana, quem é a avó, quem é o irmão, quem é o bebê.",
        dificil="só a canção de ninar, de colo, com a luz baixa, e o cartão <i>mãe</i>.",
        alerta="Famílias são diferentes: se na casa da Marina quem cuida é outra pessoa (uma tia, um avô, duas mães, dois pais), use a palavra que combina com a vida dela; os cartões são um ponto de partida, não um modelo."))

    pagina_verso(L, "O carrinho da irmãzinha", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_carrinho", 96, "inglês", INGLES, "en",
                 ["In go-cart so tiny", "My sister I drew;", "And I’ve promised to draw her", "The wide world through.", "", "We have not yet started—", "I own it with sorrow—", "Because our trip’s always", "Put off till to-morrow."],
                 ["Num carrinho tão pequeno", "puxei a minha irmã;", "e prometi puxá-la", "pelo mundo afora.", "", "Ainda não partimos —", "confesso com tristeza —", "porque a nossa viagem", "fica sempre para amanhã."],
                 "uma rima para dizer",
                 "Diga os versos balançando, como quem puxa um carrinho. Aqui <i>draw</i> quer dizer “puxar” (o carrinho), e não “desenhar”, como a gravura mostra: o irmão vai na frente, a irmã puxa e a irmãzinha vai sentada. "
                 "Mostre <i>sister</i> (irmã) e <i>baby</i> (bebê) na gravura. A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); o livro não traz melodia, e a coleção não inventa uma.", INGLES)

    pagina_verso(L, "Fais dodo, Colas", "canção de ninar francesa · a partitura é a original de 1883", "monvel_fais_dodo", 148, "francês", FRANCES, "fr",
                 ["Fais dodo, Colas, mon p’tit frère;", "Fais dodo, t’auras du lolo;", "Maman est en haut", "Qui fait du gâteau,", "Papa est en bas", "Qui fait du chocolat:", "Fais dodo, Colas, mon p’tit frère,", "Fais dodo, t’auras du lolo."],
                 ["Dorme, Colas, meu irmãozinho;", "dorme, você vai ganhar leitinho;", "a mamãe está lá em cima", "fazendo bolo,", "o papai está lá embaixo", "fazendo chocolate:", "dorme, Colas, meu irmãozinho,", "dorme, você vai ganhar leitinho."],
                 "uma canção de ninar",
                 "A melodia é a impressa na página (a linha de cima, <i>chant</i>); a de baixo é o acompanhamento de piano, que você pode ignorar. Cante bem baixo, embalando. <i>Dodo</i> é como as crianças francesas chamam o sono "
                 "(<i>faire dodo</i>, “dormir”) e <i>lolo</i>, o leite; <i>Colas</i> é <i>Nicolas</i>. Aparecem <i>maman</i>, <i>papa</i> e <i>frère</i>. A gravura de Boutet de Monvel mostra uma mulher abraçando uma criança pequena, sob a lua e uma coruja.", FRANCES)

    itens = [dict(pt="mãe", pd="crane_porco_mae", en="mother", fr="mère", la="māter", dica="<i>māter</i> deu “mãe” e “maternal”"),
             dict(pt="pai", pd="brooke_urso_porta", en="father", fr="père", la="pater", dica="<i>pater</i> deu “pai” e “paterno”; aqui, o Papai Urso da história"),
             dict(pt="bebê", pd="cartao_bebe", en="baby", fr="bébé", la="īnfāns", dica="<i>īnfāns</i> quer dizer “quem ainda não fala”: daí “infante”"),
             dict(pt="irmão", pd="cartao_irmao", en="brother", fr="frère", la="frāter", dica="<i>frāter</i> deu “frade” e “fraternal”; “irmão” vem de <i>germānus</i>"),
             dict(pt="irmã", pd="cartao_irma", en="sister", fr="sœur", la="soror", dica="<i>soror</i> deu “sóror” e “sororidade”"),
             dict(pt="avó", pd="crane_vovo_janela", en="grandmother", fr="grand-mère", la="avia", dica="<i>avia</i> deu “avó”"),
             dict(pt="família", pd="cartao_familia", en="family", fr="famille", la="familia", dica="<i>familia</i>: as pessoas que moram na mesma casa"),
             dict(pt="abraço", pd="monvel_abraco", en="hug", fr="câlin", la="amplexus", dica="<i>câlin</i> é o abraço carinhoso, o das crianças"),
             dict(pt="amor", mot="coracao", en="love", fr="amour", la="amor", dica="<i>amor</i> é igual em latim e em português")]
    cartoes(L, "a família", itens, "Volume 7 · A família", nota_latim=NOTA_LATIM)

    L.add(f"""<div class="miolo">{titulo("Quem é quem?", "um jogo de cartões e uma canção em roda", 26)}
      <div class="centro" style="margin:2mm 0 0">{pd("monvel_frere_jacques", "100mm", "margin:0 auto")}</div>
      {duas_colunas(versos("francês", FRANCES, ["Frère Jacques, Frère Jacques,", "Dormez-vous? Dormez-vous?", "Sonnez les matines, sonnez les matines,", "Din, din, don! Din, din, don!"], "fr"),
                    versos("português · tradução da coleção", FRANCES, ["Irmão Jacques, irmão Jacques,", "está dormindo? está dormindo?", "toque as matinas, toque as matinas,", "din, din, dom! din, din, dom!"]))}
      {subtitulo_h("O jogo")}
      {passos_txt(["Espalhem os cartões da família com a figura para cima.", "O adulto diz uma palavra do idioma da semana (por exemplo, “<i>mother!</i>” ou “<i>maman!</i>”) e a Marina aponta o cartão. Sem pedir que repita.",
                   "Depois ela aponta uma pessoa de verdade (ou uma foto) e o adulto diz a palavra.", "Para terminar, cantem <i>Frère Jacques</i> em roda, balançando como os sinos da gravura."], 10.8)}</div>
      {adulto("jogo e canção",
              "<i>Frère Jacques</i> é uma canção tradicional de roda: “irmão Jacques” é um frade que precisa acordar para tocar os sinos da manhã (as <i>matines</i>). A melodia é a da partitura impressa; cantem duas vezes e, "
              "quando ela souber, comecem uma segunda voz depois da primeira frase (um cânone). Na rotina, diga a palavra do idioma da semana ao abraçar: <i>hug</i> ou <i>câlin</i>.", credito_pd("monvel_frere_jacques"))}""", aba="--d-jogos")


# ================================================================== U3 A CASA

def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · A casa", aba=INGLES,
        pergunta="Como se chamam, em outras línguas, as coisas que a gente encontra em casa?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · um passeio pela casa a cada encontro.",
        objetivos=["Ouvir uma rima inglesa sobre uma casa vermelha e uma canção francesa à luz da lua.", "Apontar, na casa de verdade, o que o cartão mostra: porta, janela, cama, mesa, cadeira.",
                   "Dizer a palavra do idioma da semana ao usar o objeto (abrir a porta, acender a luz).", "Brincar de “onde está?” com os cartões escondidos pela casa.", "Conhecer a origem latina de “casa”, “porta” e “janela”."],
        repertorio="<b>Em português:</b> casa, porta, janela, cama, mesa, cadeira, chave, vela, lamparina. <b>Rima em inglês:</b> a casa vermelha, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>Au clair de la lune</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>domus</i>, <i>porta</i>, <i>fenestra</i>, <i>lectus</i>, <i>clāvis</i>.",
        materiais="Os cartões da unidade recortados, fita para pendurar os cartões nos lugares da casa, uma vela de brinquedo (ou uma lanterna) e uma caixa com uma chave.",
        vida="Dizer a palavra ao abrir a porta, ao acender a luz, ao sentar na cadeira e ao ir para a cama, sempre no idioma da semana.",
        etapas=[["Escutar a rima e a canção do luar.", "Olhar a gravura e achar a porta, a janela e a vela.", "Mostrar o cartão e passear até o objeto de verdade."],
                ["Pendurar cada cartão no lugar certo da casa.", "Esconder um cartão e brincar de “onde está?”.", "Parear o cartão com a figura da gravura."],
                ["Desenhar a casa da Marina e colar os cartões.", "Fazer uma casa de caixa de papelão com porta e janela.", "Cantar <i>Au clair de la lune</i> à luz de uma lanterna."]],
        indicadores=["Aponta o objeto certo quando ouve a palavra.", "Leva o cartão até o lugar certo da casa.", "Abre e fecha a porta dizendo a palavra, de brincadeira.",
                     "Reconhece a vela e a janela na gravura da canção.", "Repete um pedacinho da rima, batendo palmas.", "Pergunta como se diz outra coisa da casa."],
        interesse="fazer uma casa de papelão com porta, janela e cama de brinquedo, e “morar” nela por um fim de semana, falando o idioma da semana.",
        dificil="só o cartão da porta, abrindo e fechando a porta de verdade.",
        alerta="Chave, vela e fósforo não são brinquedo: use cartões e objetos de brinquedo. Vela acesa só com adulto, longe da criança."))

    pagina_verso(L, "A casa vermelha", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_casa_vermelha", 96, "inglês", INGLES, "en",
                 ["My house is red—a little house,", "A happy child am I,", "I laugh and play the livelong day", "I hardly ever cry.", "", "I have a tree, a green, green tree,", "To shade me from the sun;", "And under it I often sit,", "When all my work is done."],
                 ["Minha casa é vermelha — uma casinha,", "sou uma criança feliz;", "rio e brinco o dia inteiro,", "quase nunca choro.", "", "Tenho uma árvore, uma árvore bem verde,", "que me faz sombra do sol;", "e debaixo dela muitas vezes me sento,", "quando o meu trabalho termina."],
                 "uma rima para dizer",
                 "Diga os versos e peça que ela aponte, na gravura, a casa, a árvore, o cesto de flores e a cerca. Aparecem <i>house</i> (casa), <i>tree</i> (árvore) e as cores <i>red</i> e <i>green</i>. "
                 "A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); o livro não traz melodia. Peça que ela diga, de memória, só “<i>my house is red</i>”.", INGLES)

    pagina_verso(L, "Au clair de la lune", "canção tradicional francesa · a partitura é a original de 1883", "monvel_clair_de_lune", 148, "francês", FRANCES, "fr",
                 ["Au clair de la lune,", "Mon ami Pierrot,", "Prête-moi ta plume", "Pour écrire un mot.", "Ma chandelle est morte,", "Je n’ai plus de feu;", "Ouvre-moi ta porte", "Pour l’amour de Dieu."],
                 ["Ao luar,", "meu amigo Pierrô,", "empresta-me a tua pena", "para escrever um bilhete.", "Minha vela apagou,", "não tenho mais fogo;", "abre-me a tua porta,", "por amor de Deus."],
                 "uma canção para cantar",
                 "A melodia é a que está impressa na página (a linha de cima, <i>chant</i>). É a mesma canção que o Volume 4 usa para ensinar notas. Na gravura, um homem de gorro branco segura uma vela do lado de fora, junto a uma cerca, e Pierrô aparece na janela. "
                 "Aparecem <i>chandelle</i> (vela), <i>porte</i> (porta) e, na segunda estrofe, <i>lit</i> (cama) e <i>cuisine</i> (cozinha). Cantem à luz de uma lanterna.", FRANCES)

    itens = [dict(pt="casa", mot="casa", en="house", fr="maison", la="domus", dica="“casa” vem do latim <i>casa</i>, “cabana”; a casa da família era a <i>domus</i>"),
             dict(pt="porta", mot="porta", en="door", fr="porte", la="porta", dica="<i>porte</i> e <i>porta</i> são a mesma palavra"),
             dict(pt="janela", mot="janela_sol", en="window", fr="fenêtre", la="fenestra", dica="<i>fenêtre</i> e <i>fenestra</i> são a mesma palavra"),
             dict(pt="cama", mot="cama", en="bed", fr="lit", la="lectus", dica="<i>lit</i> vem de <i>lectus</i>"),
             dict(pt="mesa", mot="mesa", en="table", fr="table", la="mēnsa", dica="<i>mēnsa</i> deu “mesa”"),
             dict(pt="cadeira", mot="cadeira", en="chair", fr="chaise", la="cathedra", dica="“cadeira” vem de <i>cathedra</i>"),
             dict(pt="chave", mot="chave", en="key", fr="clé", la="clāvis", dica="<i>clāvis</i> deu “chave”"),
             dict(pt="vela", mot="vela", en="candle", fr="bougie", la="candēla", dica="<i>bougie</i> vem de Bugia, cidade da Argélia onde se faziam velas"),
             dict(pt="lamparina", mot="lampada", en="lamp", fr="lampe", la="lucerna", dica="<i>lucerna</i>: a lamparina de barro dos romanos")]
    cartoes(L, "a casa", itens, "Volume 7 · A casa", nota_latim=NOTA_LATIM)

    L.add(f"""<div class="miolo">{titulo("Onde está?", "um passeio pela casa com os cartões", 26)}
      <div class="centro" style="margin:2mm 0 2mm">{cena([("casa", 38, 6, 6), ("porta", 34, 48, 10), ("janela_sol", 34, 86, 8), ("cadeira", 32, 124, 8), ("lampada", 34, 14, 52), ("cama", 34, 52, 54), ("vela", 28, 92, 50), ("chave", 30, 130, 54)], 94)}</div>
      {subtitulo_h("O passeio")}
      {passos_txt(["Cada um escolhe um cartão e diz a palavra do idioma da semana (por exemplo, “<i>door!</i>” ou “<i>porte !</i>”).", "Vão até o objeto de verdade, tocam nele e penduram o cartão ali com fita.",
                   "Na outra rodada, o adulto esconde um cartão e a Marina procura, ouvindo a palavra: “<i>where is the key?</i>” ou “<i>où est la clé ?</i>”.", "Antes de dormir, apaguem a luz dizendo o cumprimento da unidade 1: <i>good night</i> ou <i>bonne nuit</i>."], 11)}</div>
      {adulto("o passeio",
              "Ao fim do fim de semana, a casa fica rotulada com os cartões, e a Marina volta a encontrá-los no dia a dia: é assim que a palavra gruda. Em inglês, a pergunta é <i>where is…?</i>; em francês, <i>où est… ?</i>. "
              "Use só a pergunta do idioma da semana, e só se ela já estiver à vontade. Não é preciso que ela repita nada.")}""", aba="--d-jogos")


# ================================================================== U4 A COMIDA

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · A comida", aba=INGLES,
        pergunta="Como se chamam, em outras línguas, as coisas que a gente come e bebe?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · na cozinha, na feira ou à mesa.",
        objetivos=["Ouvir uma rima inglesa sobre o que se gosta de comer e uma canção francesa da padeira.", "Apontar o cartão do alimento que o adulto nomeia, e achar o alimento de verdade.",
                   "Pedir, no idioma da semana, “pão, por favor” e agradecer.", "Brincar de feira ou de mesa posta, com comida de brinquedo ou de verdade.", "Conhecer a origem latina de “pão”, “leite”, “queijo” e “ovo”."],
        repertorio="<b>Em português:</b> pão, leite, queijo, ovo, maçã, banana, laranja, mel, água. <b>Rima em inglês:</b> os três meninos que querem comer, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>La Boulangère</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>pānis</i>, <i>lac</i>, <i>cāseus</i>, <i>ōvum</i>, <i>mel</i>, <i>aqua</i>.",
        materiais="Os cartões da unidade recortados, frutas e pão de verdade, um prato e um copo de brinquedo, uma sacola de feira.",
        vida="No café da manhã, pedir e agradecer no idioma da semana: <i>bread, please</i> / <i>du pain, s’il vous plaît</i>, e <i>thank you</i> / <i>merci</i> (da unidade 1).",
        etapas=[["Escutar a rima e a canção da padeira.", "Olhar as gravuras e achar o pão, a maçã e o queijo.", "Mostrar o cartão e dizer a palavra ao dar o alimento."],
                ["Parear o cartão com o alimento de verdade.", "Separar os cartões: o que é de beber, o que é de comer.", "Brincar de feira: pedir, entregar, agradecer."],
                ["Montar uma mesa posta com os cartões como cardápio.", "Inventar um pedido para o ursinho: “pão e leite, por favor”.", "Fazer um pão com a família e dizer <i>bread</i> ou <i>pain</i> na hora de comer."]],
        indicadores=["Aponta o cartão do alimento que ouve.", "Dá o alimento certo ao brincar de feira.", "Diz <i>please</i> ou <i>s’il vous plaît</i> ao pedir, de brincadeira.",
                     "Separa o que é de beber do que é de comer.", "Repete “please” ou “merci” ao ouvir o adulto.", "Pergunta o nome de um alimento novo em outro idioma."],
        interesse="cozinhar algo simples juntos (uma salada de frutas, um pão) e dizer o nome de cada ingrediente no idioma da semana.",
        dificil="só o cartão do pão e o gesto de dar e agradecer.",
        alerta="Respeite as alergias e as restrições da família: troque o queijo, o ovo ou o leite por outro cartão, se for preciso. Não use a comida como prêmio nem como castigo."))

    pagina_verso(L, "O que vocês querem comer?", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_tres_meninos", 88, "inglês", INGLES, "en",
                 ["“For what are you longing, you three little boys?", "Oh, what would you like to eat?”", "“We should like some apples, or gingerbread,—", "Or a fine big drum to beat.”", "", "“Oh, what will you give me, you three little boys,", "In exchange for these good, good things?”", "“Some bread and cheese, and some radishes,", "And our little brown bird that sings.”"],
                 ["“Do que têm vontade, vocês três meninos?", "O que gostariam de comer?”", "“Queremos umas maçãs, ou pão de gengibre,", "ou um tambor grande para bater.”", "", "“E o que vocês me dão, três meninos,", "em troca dessas coisas tão boas?”", "“Um pouco de pão e queijo, e uns rabanetes,", "e o nosso passarinho marrom que canta.”"],
                 "uma rima para dizer",
                 "Diga como um diálogo, mudando a voz para quem pergunta e para os meninos. Aparecem <i>apples</i> (maçãs), <i>gingerbread</i> (pão de gengibre), <i>bread and cheese</i> (pão e queijo) e <i>radishes</i> (rabanetes). "
                 "A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); o livro não traz melodia. Em cada rodada, mostre o cartão do alimento que aparece.", INGLES)

    pagina_verso(L, "La Boulangère", "canção tradicional francesa · a partitura é a original de 1883", "monvel_boulangere", 148, "francês", FRANCES, "fr",
                 ["La boulangère a des écus", "Qui ne lui coûtent guère;", "Elle en a, je les ai vus;", "J’ai vu la boulangère aux écus,", "J’ai vu la boulangère."],
                 ["A padeira tem moedas", "que quase nada lhe custam;", "ela as tem, eu as vi;", "vi a padeira com as moedas,", "vi a padeira."],
                 "uma canção para cantar",
                 "A melodia é a da partitura impressa (a linha de cima, <i>chant</i>). <i>Boulangère</i> é a padeira, e <i>écus</i> são moedas antigas. No livro de 1883, dança-se em roda na primeira parte e, na segunda, faz-se a “corrente inglesa”, uma figura de dança. "
                 "Na gravura, a padeira está atrás do balcão, com os pães nas prateleiras e uma criança que espia pela janela. Mostre o cartão do <i>pão</i>: <i>pain</i> em francês, <i>bread</i> em inglês.", FRANCES)

    itens = [dict(pt="pão", mot="pao", en="bread", fr="pain", la="pānis", dica="<i>pānis</i> deu “pão”; “companhia” é quem divide o pão"),
             dict(pt="leite", mot="copo_leite", en="milk", fr="lait", la="lac", dica="<i>lac</i> deu “leite” e “lácteo”"),
             dict(pt="queijo", mot="queijo", en="cheese", fr="fromage", la="cāseus", dica="<i>cāseus</i> deu “queijo”"),
             dict(pt="ovo", mot="ovo", en="egg", fr="œuf", la="ōvum", dica="<i>ōvum</i> deu “ovo” e “oval”"),
             dict(pt="maçã", mot="maca", en="apple", fr="pomme", la="mālum", dica="<i>pomme</i> vem de <i>pōma</i>, “fruta”"),
             dict(pt="banana", mot="banana", en="banana", fr="banane", la=None, dica="os romanos ainda não conheciam a banana"),
             dict(pt="laranja", mot="laranja", en="orange", fr="orange", la=None, dica="a laranja doce só chegou à Europa muito depois dos romanos"),
             dict(pt="mel", mot="mel", en="honey", fr="miel", la="mel", dica="<i>mel</i> é igual em latim e em português"),
             dict(pt="água", html=img("gota", "30mm"), en="water", fr="eau", la="aqua", dica="<i>eau</i> também vem de <i>aqua</i>")]
    cartoes(L, "a comida", itens, "Volume 7 · A comida")

    L.add(f"""<div class="miolo">{titulo("A feira da Marina", "um jogo de pedir, entregar e agradecer", 26)}
      <div class="centro" style="margin:2mm 0 2mm">{cena([("pao", 36, 6, 4), ("queijo", 34, 46, 8), ("copo_leite", 30, 84, 4), ("maca", 30, 118, 8), ("ovo", 26, 148, 12), ("mel", 28, 20, 48), ("banana", 32, 60, 50), ("laranja", 28, 102, 50), ("gota", 24, 140, 52)], 88)}</div>
      {subtitulo_h("O jogo")}
      {passos_txt(["Um de vocês é o feirante, e o outro é o freguês. Os cartões ficam na “banca”, com a figura para cima.", "O freguês pede um alimento no idioma da semana e o feirante entrega o cartão (ou o alimento de brinquedo).",
                   "O freguês agradece e o feirante responde. Depois trocam de papel.", "Na mesa, de verdade: antes de comer, peçam o pão com as palavras da tabela."], 11)}
      <table class="tab" style="margin-top:3mm"><tr><th></th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th></tr>
        <tr><td><i>pedir</i></td><td lang="en" style="font-size:12pt">Bread, please.</td><td lang="fr" style="font-size:12pt">Du pain, s’il vous plaît.</td></tr>
        <tr><td><i>agradecer</i></td><td lang="en" style="font-size:12pt">Thank you.</td><td lang="fr" style="font-size:12pt">Merci.</td></tr>
        <tr><td><i>responder</i></td><td lang="en" style="font-size:12pt">Here you are.</td><td lang="fr" style="font-size:12pt">Voilà.</td></tr></table></div>
      {adulto("a feira",
              "Use as expressões da tabela só no idioma da semana. <i>Please</i> e <i>thank you</i> já foram vistos na unidade 1 (<i>s’il vous plaît</i> e <i>merci</i>, também). Se ela ainda não fala, basta que ela entregue e receba o cartão. "
              "O que importa é o gesto repetido: pedir, receber, agradecer.")}""", aba="--d-jogos")


# ================================================================== U5 OS ANIMAIS

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · Os animais", aba=INGLES,
        pergunta="Como se chamam, e como falam, os bichos em outras línguas?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · de preferência perto de bichos de verdade.",
        objetivos=["Ouvir uma rima inglesa sobre gansos e uma canção francesa sobre um gato perdido.", "Apontar o cartão do bicho que o adulto nomeia.",
                   "Brincar de imitar o bicho: cada língua escreve o som de um jeito.", "Reconhecer os bichos nas gravuras (gansos, gato, galo).", "Conhecer a origem latina de “cão”, “vaca”, “peixe” e “músculo”."],
        repertorio="<b>Em português:</b> gato, cachorro, vaca, cavalo, galo, pato, lebre, peixe, ratinho. <b>Rima em inglês:</b> os gansos passeadores, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>La Mère Michel</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>fēlēs</i>, <i>canis</i>, <i>vacca</i>, <i>equus</i>, <i>gallus</i>, <i>piscis</i>, <i>mūs</i>.",
        materiais="Os cartões da unidade recortados, bichos de brinquedo (ou de pelúcia), uma cesta de bichos e, se der, um passeio a uma praça, um sítio ou um aquário.",
        vida="Dizer o nome do bicho no idioma da semana ao ver um de verdade, na rua, num livro ou na tela, sem pedir que ela repita.",
        etapas=[["Escutar a rima dos gansos e a canção do gato perdido.", "Olhar as gravuras e achar os bichos.", "Mostrar o cartão e imitar o bicho."],
                ["Parear o cartão com o bicho de brinquedo.", "Ligar cada bicho ao seu som, na tabela.", "Brincar de “que bicho sou eu?”, só com o som."],
                ["Inventar uma história curta de dois bichos, usando as palavras da semana.", "Procurar na rua o bicho do cartão.", "Fazer o teatro de fantoches de <i>La Mère Michel</i>."]],
        indicadores=["Aponta o cartão do bicho que ouve nomear.", "Imita o som do bicho, nas três maneiras da tabela.", "Brinca de parear bicho e cartão sem ajuda.",
                     "Reconhece o gato e os gansos nas gravuras.", "Diz o nome de um bicho no idioma da semana ao vê-lo.", "Pergunta como o bicho faz, em outra língua."],
        interesse="ir a um lugar com bichos (um sítio, um zoológico, um aquário) e dizer o nome de cada um no idioma da semana.",
        dificil="só o cartão do gato e o som dele, <i>miau</i>, <i>meow</i> ou <i>miaou</i>.",
        alerta="Bichos de verdade: olhar e conversar de longe, sem puxar o rabo nem pôr o dedo perto da boca; lavar as mãos depois de mexer em qualquer animal."))

    pagina_verso(L, "Os gansos passeadores", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_gansos_prancha", 88, "inglês", INGLES, "en",
                 ["Some geese went out a-walking,", "To breakfast and to dine;", "They craned their necks, and plumed themselves—", "They numbered four from nine;", "With their cackle, cackle, cackle!", "They thought themselves so fine."],
                 ["Uns gansos saíram a passear,", "para o café e para o jantar;", "esticaram o pescoço e alisaram as penas —", "eram nove menos quatro;", "com o seu cá, cá, cá!", "achavam-se tão elegantes."],
                 "uma rima para dizer",
                 "Diga os versos esticando o pescoço, como os gansos, e faça o “<i>cackle, cackle, cackle</i>” com a voz. <i>Goose</i> é “ganso” e <i>geese</i> é o plural. “Nove menos quatro” são cinco: conte, na gravura, os gansos que passeiam. "
                 "A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); no livro, ela continua com uma velha que manda os gansos calar. O livro não traz melodia.", INGLES)

    pagina_verso(L, "La mère Michel", "canção tradicional francesa · a partitura é a original de 1883", "monvel_mere_michel", 148, "francês", FRANCES, "fr",
                 ["C’est la mèr’ Michel qui a perdu son chat,", "Qui cri’ par la f’nêtre à qui le lui rendra.", "Et l’ compèr’ Lustucru qui lui a répondu:", "Allez, la mèr’ Michel, vot’ chat n’est pas perdu."],
                 ["É a mãe Michel que perdeu o seu gato,", "que grita pela janela: “quem o devolve?”", "E o compadre Lustucru lhe respondeu:", "“Vá, mãe Michel, o seu gato não está perdido.”"],
                 "uma canção para cantar",
                 "A melodia é a da partitura impressa (a linha de cima, <i>chant</i>). <i>Chat</i> é “gato”; <i>mère</i> é “mãe” (da unidade 2) e <i>compère</i> é “compadre”. Na gravura, a mãe Michel grita da janela e Lustucru, o vizinho, "
                 "aparece na porta de uma casa de comida, com uma panela na mão. Na gravura não aparece o gato: ele só existe nos versos, e a graça é procurá-lo com a imaginação. "
                 "As outras estrofes continuam a conversa.", FRANCES)

    itens = [dict(pt="gato", mot="gato", en="cat", fr="chat", la="fēlēs", dica="<i>chat</i> vem de <i>cattus</i>, o gato doméstico dos últimos tempos de Roma"),
             dict(pt="cachorro", mot="cachorro", en="dog", fr="chien", la="canis", dica="<i>canis</i> deu “canino”"),
             dict(pt="vaca", pd="cartao_vaca", en="cow", fr="vache", la="vacca", dica="<i>vacca</i> deu “vaca”"),
             dict(pt="cavalo", pd="cartao_cavalo", en="horse", fr="cheval", la="equus", dica="<i>equus</i> deu “equino”; “cavalo” vem de <i>caballus</i>"),
             dict(pt="galo", pd="cartao_galo", en="rooster", fr="coq", la="gallus", dica="<i>gallus</i> deu “galo” e “galináceo”"),
             dict(pt="pato", mot="patinho", en="duck", fr="canard", la="anas", dica="<i>anas</i>: a ave que nada na lagoa"),
             dict(pt="lebre", mot="lebre", en="hare", fr="lièvre", la="lepus", dica="<i>lepus</i> deu “lebre” e “leporino”"),
             dict(pt="peixe", mot="peixe", en="fish", fr="poisson", la="piscis", dica="<i>piscis</i> deu “peixe” e “piscina”"),
             dict(pt="ratinho", mot="ratinho", en="mouse", fr="souris", la="mūs", dica="<i>mūs</i> deu “músculo” (que parecia um ratinho)")]
    cartoes(L, "os animais", itens, "Volume 7 · Os animais")

    sons = (("gato", "gato", "miau", "meow", "miaou"), ("cachorro", "cachorro", "au-au", "woof", "ouaf"), ("vaca", "pd:cartao_vaca", "mu", "moo", "meuh"),
            ("pato", "patinho", "quá-quá", "quack", "coin-coin"), ("galo", "pd:cartao_galo", "cocoricó", "cock-a-doodle-doo", "cocorico"))
    def icone(m):
        return pd(m[3:], "16mm", "max-height:16mm;object-fit:contain;margin:0 auto") if m.startswith("pd:") else img(m, "16mm")
    linhas = "".join(f'<tr><td style="width:20mm">{icone(m)}</td><td style="font-size:12.5pt;font-style:italic">{pt}</td><td style="font-size:12.5pt">{p}</td>'
                     f'<td lang="en" style="font-size:12.5pt">{e}</td><td lang="fr" style="font-size:12.5pt">{f}</td></tr>' for pt, m, p, e, f in sons)
    L.add(f"""<div class="miolo">{titulo("Como fala o bicho?", "o mesmo bicho, o mesmo som, escrito de três jeitos", 26)}
      <div class="centro" style="margin:2mm 0 1mm">{cena([("gato", 34, 10, 4), ("cachorro", 34, 50, 6), ("patinho", 28, 92, 10), ("lebre", 34, 126, 4)], 40)}</div>
      <table class="tab" style="margin-top:2mm"><tr><th></th><th>bicho</th><th>{rotulo("português", "--d-natureza")}</th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th></tr>{linhas}</table>
      {subtitulo_h("O jogo")}
      {passos_txt(["O adulto faz o som de um bicho, na maneira do idioma da semana, e a Marina mostra o cartão.", "Depois é a vez dela: ela faz um som e o adulto adivinha. Valem os sons dela, também.",
                   "Na rua, quando ouvirem um bicho de verdade, perguntem: “como ele faz, em inglês? e em francês?”."], 11)}</div>
      {adulto("os sons dos bichos",
              "Os bichos fazem o mesmo som em qualquer lugar; quem muda é a <b>maneira de escrever</b> esse som, que cada língua inventou. Por isso o cachorro faz <i>au-au</i> em português, <i>woof</i> em inglês e <i>ouaf</i> em francês. "
              "A tabela traz as grafias mais comuns; há outras (<i>bow-wow</i>, <i>ouah</i>). Brinque, sem corrigir.")}""", aba="--d-jogos")


# ================================================================== U6 AS CORES

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · As cores", aba=INGLES,
        pergunta="Como se chamam as cores em outras línguas, e onde elas estão no mundo?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · com uma caça às cores dentro ou fora de casa.",
        objetivos=["Ouvir uma rima inglesa que fala de verde, amarelo e vermelho e uma canção de roda francesa.", "Apontar o cartão da cor que o adulto nomeia.",
                   "Achar, na casa ou na rua, algo de cada cor.", "Dizer a cor do dia no idioma da semana.", "Conhecer a origem latina de “vermelho”, “verde” e “preto”."],
        repertorio="<b>Em português:</b> vermelho, azul, amarelo, verde, laranja, roxo, rosa, marrom, preto. <b>Rima em inglês:</b> cinco irmãzinhas e cinco malmequeres, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>Nous n’irons plus au bois</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>ruber</i>, <i>viridis</i>, <i>niger</i>, <i>purpureus</i>.",
        materiais="Os cartões da unidade recortados, uma cesta, fitas ou panos de todas as cores, giz de cera ou aquarela.",
        vida="Dizer a cor do dia ao se vestir e ao escolher o copo ou o prato, no idioma da semana: <i>red</i>, <i>blue</i> ou <i>rouge</i>, <i>bleu</i>.",
        etapas=[["Escutar a rima dos malmequeres e a canção do bosque.", "Olhar a gravura e dizer as cores que vê.", "Mostrar o cartão e dizer a cor."],
                ["Achar algo de cada cor na casa e pôr ao lado do cartão.", "Ordenar os cartões das cores como num arco-íris.", "Parear cada cartão com a fita da mesma cor."],
                ["Pintar um arco-íris e dizer as cores.", "Misturar duas tintas e dizer a cor que nasceu.", "Escolher a cor do dia e vestir algo dela."]],
        indicadores=["Aponta o cartão da cor que ouve.", "Acha um objeto da cor pedida.", "Pareia cartão e fita da mesma cor, sem ajuda.",
                     "Diz a cor do dia no idioma da semana, de brincadeira.", "Repete “green” ou “vert” ao olhar a gravura.", "Mistura duas tintas e se admira com o resultado."],
        interesse="misturar tintas e dar nome à cor nova, no idioma da semana (azul e amarelo dão verde).",
        dificil="só duas cores, a preferida dela e mais uma, com a caça às cores na sala.",
        alerta="Não pare para “testar” se ela sabe as cores, e não corrija a cor que ela disser: pergunte “onde você viu essa cor?”. Tintas e giz de cera só os que forem atóxicos."))

    pagina_verso(L, "Cinco irmãzinhas e cinco malmequeres", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_marias_cores", 84, "inglês", INGLES, "en",
                 ["Five little sisters walking in a row;", "Now, isn’t that the best way for little girls to go?", "Each had a round hat, each had a muff,", "And each had a new pelisse of soft green stuff.", "", "Five little marigolds standing in a row;", "Now, isn’t that the best way for marigolds to grow?", "Each with a green stalk, and all the five had got", "A bright yellow flower, and a new red pot."],
                 ["Cinco irmãzinhas caminhando em fila;", "não é essa a melhor maneira de as meninas andarem?", "Cada uma de chapéu redondo, cada uma de regalo,", "e cada uma com um casaco novo de lã verde.", "", "Cinco malmequeres plantados em fila;", "não é essa a melhor maneira de os malmequeres crescerem?", "Cada um com um talo verde, e todos os cinco com", "uma flor amarela brilhante e um vaso novo vermelho."],
                 "uma rima para dizer",
                 "Diga os versos apontando, na gravura, as meninas e os vasos. Aparecem três cores: <i>green</i> (verde), <i>yellow</i> (amarelo) e <i>red</i> (vermelho). <i>Muff</i> é um regalo de pele para aquecer as mãos; <i>marigold</i> é o malmequer. "
                 "A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); o livro não traz melodia. Conte as meninas e os vasos: são cinco de cada.", INGLES)

    pagina_verso(L, "Nous n’irons plus au bois", "canção tradicional francesa · a partitura é a original de 1883", "monvel_bois", 148, "francês", FRANCES, "fr",
                 ["Nous n’irons plus au bois,", "Les lauriers sont coupés.", "", "Et Jeanne, la bergère,", "Avec son blanc panier,", "Allant cueillir la fraise", "Et la fleur d’églantier."],
                 ["Não iremos mais ao bosque,", "os loureiros foram cortados.", "", "E Joana, a pastora,", "com o seu cesto branco,", "indo colher o morango", "e a flor da roseira-brava."],
                 "uma canção para cantar e procurar cores",
                 "A melodia é a da partitura impressa (a linha de cima, <i>chant</i>); o livro traz primeiro a estrofe de abertura, e as outras vão entrando na roda, uma criança de cada vez. Os versos escolhidos trazem <i>blanc</i> (branco) e <i>fraise</i> (morango, vermelho). "
                 "A gravura é cheia de cor: peça que ela ache o azul dos passarinhos, o rosa das flores e o verde das folhas, em português, e diga a cor no idioma da semana.", FRANCES)

    itens = [dict(pt="vermelho", mot="circulo_vermelho", en="red", fr="rouge", la="ruber", dica="<i>ruber</i> deu “rubi” e “rubro”"),
             dict(pt="azul", mot="circulo_azul", en="blue", fr="bleu", la="caeruleus", dica="“azul” vem do árabe; em latim, o azul do céu e do mar era <i>caeruleus</i>"),
             dict(pt="amarelo", mot="circulo_amarelo", en="yellow", fr="jaune", la="lūteus", dica="<i>lūteus</i>: amarelo-ouro"),
             dict(pt="verde", mot="circulo_verde", en="green", fr="vert", la="viridis", dica="<i>viridis</i> deu “verde”"),
             dict(pt="laranja", mot="circulo_laranja", en="orange", fr="orange", la=None, dica="a fruta e a cor chegaram depois dos romanos"),
             dict(pt="roxo", mot="circulo_roxo", en="purple", fr="violet", la="purpureus", dica="<i>purpureus</i>: a cor da púrpura, tinta caríssima em Roma"),
             dict(pt="rosa", mot="circulo_rosa", en="pink", fr="rose", la="roseus", dica="<i>roseus</i>: cor de rosa"),
             dict(pt="marrom", mot="circulo_marrom", en="brown", fr="marron", la=None, dica="os romanos não tinham uma palavra só para o marrom"),
             dict(pt="preto", mot="circulo_preto", en="black", fr="noir", la="niger", dica="<i>niger</i> deu “negro”")]
    cartoes(L, "as cores", itens, "Volume 7 · As cores")

    L.add(f"""<div class="miolo">{titulo("A caça às cores", "achar o que combina com cada cartão", 26)}
      <div class="centro" style="margin:2mm 0 2mm">{tira(["pote_vermelho", "pote_amarelo", "pote_azul"], "30mm", "6mm")}</div>
      {subtitulo_h("O jogo")}
      {passos_txt(["Cada um escolhe um cartão de cor e diz a cor no idioma da semana (por exemplo, “<i>blue</i>” ou “<i>bleu</i>”).", "Saiam pela casa (ou pela rua) para achar algo daquela cor: uma meia, uma folha, um brinquedo.",
                   "Ponham o que acharam ao lado do cartão e olhem juntos: “quantas coisas azuis?”.", "Para terminar, a Marina escolhe a <b>cor do dia</b> e veste ou usa algo dela até a hora de dormir."], 11.2)}
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:5mm">
        <div class="caixa" style="height:50mm"><div class="peq centro">uma coisa vermelha que achei</div></div>
        <div class="caixa" style="height:50mm"><div class="peq centro">uma coisa azul que achei</div></div>
        <div class="caixa" style="height:50mm"><div class="peq centro">uma coisa verde que achei</div></div></div></div>
      {adulto("cores",
              "A criança pequena aprende a cor <b>procurando-a</b>, não repetindo o nome. Evite perguntar “que cor é essa?”: diga você o nome e deixe que ela escolha. As cores laranja e marrom, em latim, não têm palavra clássica própria, e por isso "
              "os cartões deixam a linha em branco. Para a mistura, use as duas cores primárias da página: vermelho com amarelo dá laranja, azul com amarelo dá verde.")}""", aba="--d-jogos")


# ================================================================== U7 O CORPO

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · O corpo", aba=INGLES,
        pergunta="Como se chamam as partes do corpo em outras línguas, e como a gente as mostra?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · com muito movimento.",
        objetivos=["Ouvir uma rima inglesa para brincar com os dedos do pé e uma canção francesa de roda.", "Apontar a parte do corpo que o adulto nomeia, no próprio corpo e no cartão.",
                   "Brincar de “faça como eu digo”, com comandos simples.", "Fazer o gesto de cada verso (plantar com o pé, com a mão).", "Conhecer a origem latina de “mão”, “pé”, “olho” e “dente”."],
        repertorio="<b>Em português:</b> mão, pé, olho, orelha, nariz, boca, dente, osso, coração. <b>Rima em inglês:</b> <i>This little pig</i>, de Walter Crane (c. 1870). "
                   "<b>Canção em francês:</b> <i>Savez-vous planter les choux ?</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>manus</i>, <i>pēs</i>, <i>oculus</i>, <i>auris</i>, <i>nāsus</i>, <i>dēns</i>.",
        materiais="Os cartões da unidade recortados, um espelho, uma boneca ou ursinho para mostrar as partes do corpo, e espaço para se mexer.",
        vida="No banho e ao vestir, dizer a parte do corpo no idioma da semana: <i>foot</i> ou <i>pied</i> ao calçar a meia, <i>hand</i> ou <i>main</i> ao lavar as mãos.",
        etapas=[["Escutar a rima dos porquinhos e a canção das couves.", "Apontar a parte do corpo no espelho.", "Mostrar o cartão e tocar a parte do corpo."],
                ["Brincar de “faça como eu digo”.", "Parear cada cartão com a parte do ursinho.", "Fazer os gestos da canção das couves."],
                ["Inventar um verso novo: “plantamos com o cotovelo”.", "Pintar o contorno da mão e dar nome aos dedos.", "Ensinar o ursinho a tocar o nariz."]],
        indicadores=["Aponta a parte do corpo que ouve nomear.", "Toca a parte certa no ursinho ou no espelho.", "Faz os gestos de cada verso da canção das couves.",
                     "Diz “wee, wee, wee” ao fim da rima, rindo.", "Segue um comando simples no idioma da semana.", "Pergunta como se diz outra parte do corpo."],
        interesse="desenhar o contorno do corpo da Marina num papel grande e escrever, junto, o nome de cada parte no idioma da semana.",
        dificil="só a rima dos porquinhos, com a massagem nos dedos do pé.",
        alerta="O corpo da criança é dela: peça licença antes de tocar (“posso fazer cócegas no pé?”) e pare quando ela disser não, em qualquer idioma."))

    pagina_verso(L, "Este porquinho", "rima inglesa, de Walter Crane (c. 1870) · para dizer, brincando com os dedos do pé", "crane_porco_mae", 94, "inglês", INGLES, "en",
                 ["This little pig went to market,", "This little pig stayed at home,", "This little pig had roast beef,", "This little pig had none,", "And this little pig cried “Wee! wee! wee!”", "All the way home."],
                 ["Este porquinho foi ao mercado,", "este porquinho ficou em casa,", "este porquinho comeu rosbife,", "este porquinho não comeu nada,", "e este porquinho fez “uí! uí! uí!”", "o caminho todo para casa."],
                 "uma rima para os dedos do pé",
                 "Pegue o pé da Marina e, a cada verso, balance um dedo, começando pelo maior; no “<i>wee, wee, wee</i>”, faça cócegas até o calcanhar. <i>Toe</i> é “dedo do pé” e <i>pig</i>, “porco”. O texto foi montado a partir das legendas das pranchas do livro "
                 "<i>This Little Pig Went to Market</i> (Londres: Routledge, c. 1870), e a gravura de abertura mostra uma mãe com a criança no colo, a contar os dedos do pé. O livro não traz melodia.", INGLES,
                 extra=f'<div style="display:flex;justify-content:center;gap:4mm;margin-top:3mm">{pd("crane_porco_mercado", "38mm")}{pd("crane_porco_casa", "38mm")}{pd("crane_porco_nada", "38mm")}{pd("crane_porcos_mesa", "38mm")}</div>')

    pagina_verso(L, "Savez-vous planter les choux ?", "canção de roda francesa · a partitura é a original de 1883", "monvel_choux", 148, "francês", FRANCES, "fr",
                 ["Savez-vous planter les choux", "À la mode, à la mode,", "Savez-vous planter les choux", "À la mode de chez nous ?", "On les plante avec le pied,", "À la mode, à la mode,", "On les plante avec le pied,", "À la mode de chez nous."],
                 ["Vocês sabem plantar couves", "ao modo, ao modo?", "Vocês sabem plantar couves", "ao modo da nossa terra?", "Plantamos com o pé,", "ao modo, ao modo,", "plantamos com o pé,", "ao modo da nossa terra."],
                 "uma canção para cantar e mexer o corpo",
                 "A melodia é a da partitura impressa (a linha de cima, <i>chant</i>). A cada estrofe, nomeia-se outra parte do corpo e faz-se o gesto de plantar com ela: <i>le pied</i> (o pé), <i>la main</i> (a mão), <i>le coude</i> (o cotovelo), <i>le nez</i> (o nariz). "
                 "Comecem pelo pé e pela mão, e deixem que ela invente as próximas. Na gravura, as crianças plantam as couves de cabeça para baixo, com as borboletas em volta.", FRANCES)

    itens = [dict(pt="mão", mot="mao", en="hand", fr="main", la="manus", dica="<i>manus</i> deu “mão” e “manual”"),
             dict(pt="pé", mot="pe", en="foot", fr="pied", la="pēs", dica="<i>pēs</i> deu “pé”, “pedal” e “pedestre”"),
             dict(pt="olho", mot="olho", en="eye", fr="œil", la="oculus", dica="<i>oculus</i> deu “olho” e “óculos”"),
             dict(pt="orelha", mot="orelha", en="ear", fr="oreille", la="auris", dica="<i>auris</i> deu “auricular”; “orelha” vem de <i>auricula</i>"),
             dict(pt="nariz", mot="nariz", en="nose", fr="nez", la="nāsus", dica="<i>nāsus</i> deu “nasal”"),
             dict(pt="boca", mot="boca", en="mouth", fr="bouche", la="ōs", dica="<i>ōs</i> deu “oral”"),
             dict(pt="dente", mot="dente", en="tooth", fr="dent", la="dēns", dica="<i>dēns</i> deu “dente” e “dental”"),
             dict(pt="osso", mot="osso", en="bone", fr="os", la="os", dica="<i>os</i>, <i>ossis</i>: igual ao nosso “osso”"),
             dict(pt="coração", mot="coracao", en="heart", fr="cœur", la="cor", dica="<i>cor</i> deu “coração” e “cordial”")]
    cartoes(L, "o corpo", itens, "Volume 7 · O corpo", nota_latim=NOTA_LATIM)

    cmd = (("nariz", "Touch your nose!", "Touche ton nez !"), ("mao", "Clap your hands!", "Tape dans tes mains !"), ("pe", "Stamp your foot!", "Tape du pied !"),
           ("olho", "Close your eyes!", "Ferme les yeux !"), ("boca", "Open your mouth!", "Ouvre la bouche !"))
    linhas = "".join(f'<tr><td style="width:22mm">{img(m, "17mm")}</td><td lang="en" style="font-size:13pt">{e}</td><td lang="fr" style="font-size:13pt">{f}</td></tr>' for m, e, f in cmd)
    L.add(f"""<div class="miolo">{titulo("Faça como eu digo", "um jogo de comandos para o corpo todo", 26)}
      <div class="centro" style="margin:2mm 0 1mm">{tira(["mao", "pe", "olho", "orelha", "nariz"], "24mm", "3mm")}</div>
      <table class="tab" style="margin-top:3mm"><tr><th></th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th></tr>{linhas}</table>
      {subtitulo_h("O jogo")}
      {passos_txt(["O adulto diz um comando no idioma da semana e faz o gesto junto. A Marina faz o mesmo.", "Quando ela já reconhecer, o adulto diz o comando e <b>não faz o gesto</b>: quem entendeu faz sozinha.",
                   "Troquem: a Marina manda e o adulto obedece (e erra de propósito, para ela rir).", "No fim, uma parada: “<i>stop!</i>” ou “<i>stop !</i>” (a palavra é igual) e todos ficam imóveis como estátuas."], 11.2)}</div>
      {adulto("faça como eu digo",
              "Os comandos são curtos e vêm sempre com o gesto, para que ela entenda pelo corpo antes de entender pela palavra. Use um idioma de cada vez, e só os comandos da tabela que ela já entende; se um for difícil, volte ao gesto sozinho. "
              "Não peça que ela diga os comandos em voz alta: o objetivo é ouvir e agir.")}""", aba="--d-jogos")


# ================================================================== U8 A NATUREZA

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · A natureza", aba=INGLES,
        pergunta="Como se chamam, em outras línguas, o céu, as árvores e o tempo lá fora?",
        duracao="Três fins de semana · encontros de 5 a 10 minutos · ao ar livre, de preferência.",
        objetivos=["Ouvir uma rima inglesa para o vento e uma canção francesa do canto do cuco.", "Apontar o cartão do que o adulto nomeia, e achar a coisa lá fora.",
                   "Dizer a palavra ao ver o sol, a nuvem ou a chuva.", "Fazer o bingo da natureza num passeio.", "Conhecer a origem latina de “sol”, “lua”, “flor” e “estrela”."],
        repertorio="<b>Em português:</b> sol, lua, estrela, nuvem, chuva, árvore, flor, folha, pedra. <b>Rima em inglês:</b> o ventinho, de Kate Greenaway (1878). "
                   "<b>Canção em francês:</b> <i>Coucou</i>, tradicional, com a partitura de 1883. <b>Latim:</b> <i>sōl</i>, <i>lūna</i>, <i>stēlla</i>, <i>nūbēs</i>, <i>arbor</i>, <i>flōs</i>.",
        materiais="Os cartões da unidade recortados, a folha do bingo, um lápis, uma sacola para guardar folhas e pedrinhas, e roupa para o tempo que fizer.",
        vida="Olhar pela janela de manhã e dizer o tempo no idioma da semana: <i>sun</i>, <i>cloud</i>, <i>rain</i> ou <i>soleil</i>, <i>nuage</i>, <i>pluie</i>.",
        etapas=[["Escutar a rima do vento e a canção do cuco, ao ar livre.", "Olhar a gravura e achar o vento, as árvores, as nuvens.", "Mostrar o cartão e olhar para aquilo no céu."],
                ["Fazer o bingo da natureza num passeio.", "Parear o cartão com o que achou (a folha, a pedra).", "Ligar cada cartão ao tempo da manhã."],
                ["Fazer um cartaz do tempo da semana com os cartões.", "Inventar um verso para o vento: “little wind, blow…”.", "Imitar o canto do cuco na floresta (ou no jardim)."]],
        indicadores=["Aponta o céu, a nuvem ou a lua ao ouvir a palavra.", "Acha, no passeio, o que o cartão mostra.", "Faz o gesto do vento com os braços ao ouvir a rima.",
                     "Imita o cuco com a voz.", "Diz o tempo de hoje, no idioma da semana.", "Guarda uma folha ou uma pedra do passeio."],
        interesse="registrar o tempo todos os dias de uma semana num cartaz, com os cartões da unidade e uma palavra do idioma da semana.",
        dificil="só o cartão do sol ou da chuva, e olhar pela janela.",
        alerta="Protetor solar e chapéu ao sol, e agasalho ao vento. Não coma folhas, flores, sementes nem frutinhas encontradas, e não olhe direto para o sol."))

    pagina_verso(L, "O ventinho", "rima inglesa, de Kate Greenaway (1878) · para dizer, não para cantar", "greenaway_ventinho", 100, "inglês", INGLES, "en",
                 ["Little wind, blow on the hill-top,", "Little wind, blow down the plain;", "Little wind, blow up the sunshine,", "Little wind, blow off the rain."],
                 ["Ventinho, sopra no alto da colina,", "ventinho, sopra pela planície;", "ventinho, sopra para cima o sol,", "ventinho, sopra para longe a chuva."],
                 "uma rima para dizer",
                 "Diga os versos soprando de leve nos dois últimos, e peça que ela faça o vento com os braços. Aparecem <i>wind</i> (vento), <i>sunshine</i> (sol, “luz do sol”) e <i>rain</i> (chuva). "
                 "A rima é de <i>Under the Window</i>, de Kate Greenaway (1878, domínio público); o livro não traz melodia. A gravura mostra uma paisagem de salgueiros e, na moldura de baixo, uma menina com um cordeiro.", INGLES)

    pagina_verso(L, "Coucou", "canção tradicional francesa · a partitura é a original de 1883", "monvel_coucou", 148, "francês", FRANCES, "fr",
                 ["En passant dans un p’tit bois", "Où le coucou chantait,", "Dans son joli chant il disait :", "« Coucou, coucou, coucou, coucou »,", "Et moi de m’en coure, coure, cour’,", "Et moi de m’en courir !"],
                 ["Passando por um bosquezinho", "onde o cuco cantava,", "no seu belo canto ele dizia:", "“cu-cu, cu-cu, cu-cu, cu-cu”,", "e eu saí correndo, correndo, correndo,", "e eu saí correndo!"],
                 "uma canção para cantar",
                 "A melodia é a da partitura impressa (a linha de cima, <i>chant</i>). Aqui estão só os versos do canto do cuco e da corrida: na canção completa, o cantor entende outra coisa do que o cuco diz e foge, e as estrofes seguintes fazem a mesma brincadeira com os patos e com uma mulher. "
                 "A gravura mostra o menino que corre. <i>Coucou</i> é o cuco, e também o que se diz ao aparecer de repente, como o nosso “achou!”.", FRANCES)

    itens = [dict(pt="sol", mot="sol", en="sun", fr="soleil", la="sōl", dica="<i>sōl</i> deu “sol” e “solar”"),
             dict(pt="lua", mot="lua", en="moon", fr="lune", la="lūna", dica="<i>lūna</i> deu “lua” e “lunar”"),
             dict(pt="estrela", mot="estrela", en="star", fr="étoile", la="stēlla", dica="<i>stēlla</i> deu “estrela” e “estelar”"),
             dict(pt="nuvem", mot="nuvem", en="cloud", fr="nuage", la="nūbēs", dica="<i>nūbēs</i> deu “nuvem” e “nublado”"),
             dict(pt="chuva", mot="nuvem_chuva", en="rain", fr="pluie", la="pluvia", dica="<i>pluvia</i> deu “chuva” e “pluvial”"),
             dict(pt="árvore", mot="arvore_verao", en="tree", fr="arbre", la="arbor", dica="<i>arbor</i> deu “árvore” e “arbóreo”"),
             dict(pt="flor", mot="flor_rosa", en="flower", fr="fleur", la="flōs", dica="<i>flōs</i> deu “flor” e “floral”"),
             dict(pt="folha", mot="folha_carvalho", en="leaf", fr="feuille", la="folium", dica="<i>folium</i> deu “folha” e “folhagem”"),
             dict(pt="pedra", mot="pedra", en="stone", fr="pierre", la="lapis", dica="<i>lapis</i> é a pedra; “pedra” vem de <i>petra</i>")]
    cartoes(L, "a natureza", itens, "Volume 7 · A natureza", nota_latim=NOTA_LATIM)

    cel = "".join(f'<div class="caixa" style="height:42mm;text-align:center;padding:2mm"><div style="line-height:0">{img(m, "26mm")}</div><div class="peq" style="margin-top:2mm">achei ☐</div></div>'
                  for m in ("sol", "nuvem", "arvore_verao", "flor_rosa", "folha_carvalho", "pedra", "pena", "lua", "borboleta"))
    L.add(f"""<div class="miolo">{titulo("O bingo da natureza", "marcar o que a Marina achou no passeio", 26)}
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:5mm">{cel}</div>
      {subtitulo_h("O jogo")}
      {passos_txt(["Levem a folha no passeio. A cada coisa achada, a Marina marca o quadradinho.", "Quem achar diz a palavra no idioma da semana (“<i>sun!</i>”, “<i>nuage !</i>”); o outro mostra o cartão da unidade.",
                   "Em casa, contem quantas coisas ela achou e guardem a folha no caderno do volume."], 11)}</div>
      {adulto("o bingo",
              "Não há ganhador: o que vale é olhar. O sol, a nuvem e a lua nem sempre aparecem no mesmo dia, e tudo bem; marque o que houver. Se estiver chovendo, o bingo pode ser feito da janela. "
              "Para o idioma da semana, use só as palavras que ela já conhece dos cartões; se não souber nenhuma, deixe o idioma de fora e faça o bingo em português.")}""", aba="--d-jogos")


# ================================================================== LATIM: DE ONDE VÊM AS PALAVRAS

def latim(L):
    """Seis páginas de latim como cultura (docs/01, §4): lemas, números romanos e palavras-mãe. Nada aqui é cobrado."""
    L.unidade = "Latim"
    INICIO["Latim"] = L.proximo
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Latim · para o adulto e para olhar</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:3mm">De onde vêm as palavras</h1>
      <div class="centro" style="margin:2mm 0 4mm;line-height:0">{img("coroa_louros", "52mm")}</div>
      <p>Latim é a língua que os romanos falavam, há mais de dois mil anos. Hoje ninguém a fala em casa, mas ela está dentro do português, do francês (e de muitas palavras do inglês): <i>aqua</i> virou “água”, <i>lūna</i> virou “lua”,
      <i>māter</i> virou “mãe”. Por isso, na Marina, o latim aparece <b>como cultura</b>: um jeito de descobrir de onde vêm as palavras, e nunca uma matéria a decorar.</p>
      <p><b>Três portas</b> para entrar nele, {rotulo("latim", LATIM)} cada uma numa página:</p>
      <table class="tab">
        <tr><th>Lemas</th><td>frases curtas que as pessoas repetem há séculos, como <i>Festina lente</i> e <i>Per aspera ad astra</i>, nas duas páginas seguintes.</td></tr>
        <tr><th>Números romanos</th><td>do I ao X, os que ainda se veem em relógios, capítulos e reis.</td></tr>
        <tr><th>Palavras-mãe</th><td>nove cartões com palavras do dia a dia (livro, pena, sino…) e a palavra latina de onde vieram.</td></tr></table>
      <h2>Como usar</h2>
      <ul>
        <li>Leia o lema <b>uma vez</b>, devagar, e conte o que ele quer dizer. Não peça que ela repita.</li>
        <li>Vogal com um traço em cima (ā, ē, ī, ō, ū) é vogal longa: <i>lūna</i> se lê “lúúna”, com o primeiro som mais comprido.</li>
        <li>O latim não tem uma pronúncia única hoje; leia como achar mais natural e se divirta.</li>
        <li>O latim não entra no <b>diário de línguas</b> como meta: se ela repetir uma palavra sozinha, anote como curiosidade.</li>
      </ul>""", aba=LATIM)

    L.add(f"""<div class="miolo">{titulo("Festina lente", "“apressa-te devagar”, um lema de Roma", 28)}
      <div class="centro" style="margin:4mm 0 3mm">{cena([("tartaruga", 64, 12, 0), ("lebre", 62, 94, 6)], 66)}</div>
      <div class="centro" style="margin:2mm 0 4mm">{rotulo("latim", LATIM)}<br><span style="font-size:30pt;font-style:italic">Festīnā lentē</span></div>
      <p style="font-size:13pt;line-height:1.5;text-align:justify">{rotulo("latim", LATIM)} <i>Festīnā</i> quer dizer “apressa-te”, e <i>lentē</i> quer dizer “devagar”. Juntos formam uma ideia que parece enganosa: <b>fazer rápido, mas sem tropeçar</b>.
      O historiador romano Suetônio conta, na <i>Vida de Augusto</i>, que o imperador repetia essa frase como um conselho para quem governa. A mesma ideia está na fábula de Esopo da lebre e da tartaruga, que a Marina pode conhecer em outros volumes.</p>
      <p style="font-size:13pt;line-height:1.5;text-align:justify">Para a Marina, é só um brinquedo de palavras: <b>quem vai devagar também chega</b>. Na rotina, sirva de lema para a hora de se vestir, de comer e de guardar os brinquedos.</p></div>
      {adulto("uma corrida de bichos de brinquedo",
              "Faça a lebre e a tartaruga correrem na sala, e deixe a tartaruga chegar primeiro (ela vai com cuidado, a lebre se distrai). Depois, repita o lema uma vez: <i>festīnā lentē</i>. "
              "O lema é conhecido no mundo todo: aparece até em brasões e na marca de livros antigos. Não precisa dizer mais do que isso.")}""", aba=LATIM)

    L.add(f"""<div class="miolo">{titulo("Duas frases para guardar", "lemas latinos que atravessaram os séculos", 26)}
      <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8mm;margin-top:5mm">
        <div class="caixa" style="text-align:center;padding:4mm">
          <div style="line-height:0">{cena([("pedra", 32, 4, 30), ("estrela", 34, 40, 0)], 68, 76)}</div>
          <div style="font-size:19pt;font-style:italic;margin-top:2mm">Per aspera ad astra</div>
          <div class="peq" style="margin-top:2mm">{rotulo("latim", LATIM)}</div>
          <p style="font-size:11.5pt;line-height:1.45;margin-top:2mm"><i>Aspera</i> são as dificuldades, <i>astra</i> são as estrelas: “pelas dificuldades, até as estrelas”. Uma ideia antiga: o difícil também leva longe.</p></div>
        <div class="caixa" style="text-align:center;padding:4mm">
          <div style="line-height:0">{cena([("sol", 34, 2, 0), ("flor_rosa", 32, 42, 28)], 68, 76)}</div>
          <div style="font-size:19pt;font-style:italic;margin-top:2mm">Carpe diem</div>
          <div class="peq" style="margin-top:2mm">{rotulo("latim", LATIM)}</div>
          <p style="font-size:11.5pt;line-height:1.45;margin-top:2mm"><i>Carpe</i> é “colhe” e <i>diem</i> é “o dia”: “aproveita o dia”. É um verso do poeta Horácio, de dois mil anos atrás.</p></div></div>
      <div class="centro" style="margin-top:8mm">{tira(["folha", "raminho", "cruzeiro_do_sul", "lua"], "22mm", "4mm")}</div></div>
      {adulto("para olhar e conversar",
              "Escolha uma das frases por semana e conte o sentido com as suas palavras. <i>Per aspera ad astra</i> é um lema tradicional (aparece em brasões e em escudos de cidades); <i>carpe diem</i> vem das <i>Odes</i> de Horácio (I, 11). "
              "Na hora de um passeio com subida, diga “<i>per aspera ad astra</i>” antes de começar. Se ela perguntar o que é, a resposta é: “é de uma língua muito antiga, e quer dizer que o difícil leva às estrelas”.")}""", aba=LATIM)

    numeros = (("I", "um", "ūnus"), ("II", "dois", "duo"), ("III", "três", "trēs"), ("IV", "quatro", "quattuor"), ("V", "cinco", "quīnque"),
               ("VI", "seis", "sex"), ("VII", "sete", "septem"), ("VIII", "oito", "octō"), ("IX", "nove", "novem"), ("X", "dez", "decem"))
    linhas = "".join(f'<tr><td style="width:22mm;font-size:21pt;font-weight:600">{r}</td><td style="width:26mm;font-size:13pt">{p}</td><td style="width:36mm;font-size:13pt;font-style:italic">{la}</td>'
                     f'<td style="line-height:0">{"".join(img("estrela", "6.6mm", "display:inline-block;margin:0 .4mm") for _ in range(i + 1))}</td></tr>' for i, (r, p, la) in enumerate(numeros))
    L.add(f"""<div class="miolo">{titulo("Os números dos romanos", "do I ao X, com estrelas para contar", 26)}
      <table class="tab" style="margin-top:4mm"><tr><th>romano</th><th>português</th><th>{rotulo("latim", LATIM)}</th><th>estrelas</th></tr>{linhas}</table></div>
      {adulto("números romanos",
              "Os romanos escreviam os números com letras: <b>I</b> é um dedo, <b>V</b> é a mão aberta (cinco dedos) e <b>X</b> são duas mãos cruzadas (dez). IV é “um antes do V” (quatro) e IX é “um antes do X” (nove). "
              "Mostre onde eles aparecem hoje: num relógio de parede, nos capítulos de um livro, nos nomes de reis e papas. A criança de 2 ou 3 anos só vai olhar: conte as estrelas junto, no idioma que quiser.")}""", aba=LATIM)

    itens = [dict(pt="livro", mot="livro", en="book", fr="livre", la="liber", dica="<i>liber</i> era a casca da árvore em que os romanos escreviam"),
             dict(pt="pena", mot="pena", en="feather", fr="plume", la="penna", dica="<i>penna</i> deu “pena”, “caneta” (de pena) e “pluma”"),
             dict(pt="sino", mot="sino", en="bell", fr="cloche", la="signum", dica="<i>signum</i> é “sinal”: o sino dava o sinal"),
             dict(pt="uva", mot="uva", en="grape", fr="raisin", la="ūva", dica="<i>ūva</i> deu “uva”"),
             dict(pt="cesta", mot="cesta", en="basket", fr="panier", la="cista", dica="<i>cista</i> deu “cesta”"),
             dict(pt="vaso", mot="vaso", en="vase", fr="vase", la="vāsum", dica="<i>vāsum</i> deu “vaso”"),
             dict(pt="terra", mot="terra", en="earth", fr="terre", la="terra", dica="<i>terra</i> é igual em latim, em português e em francês"),
             dict(pt="caixa", mot="caixa", en="box", fr="boîte", la="capsa", dica="<i>capsa</i> deu “caixa” e “cápsula”"),
             dict(pt="cereja", mot="cereja", en="cherry", fr="cerise", la="cerasus", dica="<i>cerasus</i> deu “cereja” e “cerise”")]
    cartoes(L, "palavras-mãe", itens, "Volume 7 · Palavras-mãe",
            nota_latim="Latim: vogal com traço (ā, ē, ī, ō, ū) é longa · cada cartão mostra a palavra latina de onde veio a portuguesa; é curiosidade, ninguém precisa decorar")


# ================================================================== ENCERRAMENTO

def gravuras_usadas(L):
    """Nomes das gravuras de domínio público que aparecem nas páginas já montadas: os créditos saem do que de fato foi impresso."""
    nomes = []
    for _, h in L.paginas:
        for n in re.findall(r"dominio_publico/v1/([a-z0-9_]+?)_(?:branco|creme)\.jpg", h):
            if n not in nomes:
                nomes.append(n)
    return nomes


def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo

    for k in range(2):
        linhas = "".join('<tr><td style="width:34mm;height:44mm"><div class="peq">data e unidade</div></td><td style="width:34mm"><div class="peq">idioma e jogo</div></td>'
                         '<td><div class="peq">o que ela disse, fez ou pediu</div></td></tr>' for _ in range(5))
        L.add(f"""<div class="miolo">{titulo("Diário de línguas", "para o adulto · o que ela ouviu, fez e disse — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Data e unidade</th><th>Idioma e jogo</th><th>O que ela disse, fez ou pediu</th></tr>{linhas}</table></div>""", aba="--d-memoria")

    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ", 1)[1]}</td><td style="width:26mm">&nbsp;</td><td style="width:26mm">&nbsp;</td><td style="width:34mm">&nbsp;</td></tr>' for n, cor in UNIDADES)
    L.add(f"""<div class="miolo">{titulo("O mapa do volume", "marcar com a data o dia em que cada unidade foi brincada", 26)}
      <table class="tab" style="margin-top:5mm"><tr><th>Unidade</th><th>{rotulo("inglês", INGLES)}</th><th>{rotulo("francês", FRANCES)}</th><th>{rotulo("latim", LATIM)}</th></tr>{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["mao_acenando", "casa", "pao", "gato", "circulo_azul", "pe", "sol"], "20mm", "2mm")}</div></div>
      {adulto("o mapa",
              "Sem pressa e sem ordem fixa: cada unidade pode voltar muitas vezes, e o que ela já conhece é só um ponto de partida para o que vem depois. O latim é só curiosidade: se um dia ela disser uma palavra latina, escreva a data e a palavra, e pronto.")}""", aba="--d-jogos")

    por_livro = {}
    for n in gravuras_usadas(L):
        item, pg = fontes_v1.ITENS[n][:2]
        por_livro.setdefault(item, set()).add(pg)
    cred = "".join(f"<li>{fontes_v1.LIVROS[i]} — Internet Archive, <i>{i}</i>, folhas {', '.join('n' + str(p) for p in sorted(ps))}.</li>" for i, ps in por_livro.items())
    L.add(f"""<div class="miolo texto">{titulo("Rimas, canções e créditos", "Volume 7", 26)}
      <h2>Letras e partituras</h2>
      <p style="font-size:9pt">As rimas inglesas são de Kate Greenaway (1846–1901), em <i>Under the Window</i> (1878), e de <i>This Little Pig Went to Market</i> (Walter Crane, c. 1870): ambas em domínio público. As canções francesas são tradicionais e vêm de <i>Vieilles chansons pour les petits enfants</i> (1883),
      com os acompanhamentos de Charles-Marie Widor (1844–1937) e as gravuras de Louis-Maurice Boutet de Monvel (1850–1913), em domínio público. A melodia de cada canção é a da partitura reproduzida na página. As traduções são da coleção e <b>precisam de revisão por quem fale as línguas</b> antes da venda.
      Nenhuma letra de canção moderna, e nenhuma melodia que não esteja impressa numa partitura antiga, entra neste livro.</p>
      <h2>Ilustrações em domínio público</h2>
      <p style="font-size:8.6pt">Digitalizações do Internet Archive, só recortadas e reduzidas; nenhuma pintura foi retocada, e a cor depende da fotografia ou da digitalização. Cada página foi conferida por SHA-256 antes de entrar no livro.</p>
      <ul style="font-size:7.6pt;line-height:1.25">{cred}</ul>
      <h2>Fundamentos</h2><p style="font-size:9pt">Cantigas e rimas para guardar palavras (Susan Wise Bauer e Jessie Wise); ouvir muito antes de falar, com a família como ambiente (Shinichi Suzuki); o latim como cultura, sem cobrança (Charlotte Mason, Dorothy Sayers).
      Nenhum material reproduz métodos ou produtos comerciais.</p>
      <h2>Ilustrações da coleção</h2><p style="font-size:9pt">Mão, porta, janela, cama, casa, cadeira, lamparina, pão, queijo, leite, cores e demais desenhos: aquarela digital procedural da coleção ({len(MOTIVOS8)} motivos novos para este volume, e outros já usados antes). Tipografia: EB Garamond (licença OFL).</p></div>""")

    L.add(f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 7</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">jogos para recortar, projetos para fazer em casa<br>e um diário de observação, para guardar<br>tudo o que a Marina descobriu.</p>
      <div style="margin-top:12mm">{tira(["livro", "estrela", "sino", "pena"], "28mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 8 · Jogos e descobertas</p></div>""", cabecalho=False)


# ================================================================== MONTAGEM

UNIDADES_PRONTAS = (unidade1, unidade2, unidade3, unidade4, unidade5, unidade6, unidade7, unidade8)


def montar(unidades=None):
    L = Livro(7, "Primeiras línguas")
    capa(L); rosto(L); carta(L); como_usar(L)
    n_sum = L.add("", cabecalho=False)
    for u in (unidades or UNIDADES_PRONTAS):
        u(L)
    if not unidades:
        latim(L)
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume7-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
