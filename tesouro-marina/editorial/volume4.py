"""
VOLUME 4 — O MUNDO DA MÚSICA
uso: python3 volume4.py
"""
import os
import subprocess
import sys

from livro import (Livro, VERSAO, adulto, cabeca_folha, cartoes, credito_pd, gerar_pdf, guia, historia, img, lista,
                   marcas_corte, memoria, observacao, passos, pd, poema, ponto_inicio, pontilhado, rodape_folha,
                   sequencia, texto, titulo, tracado)
from musica import linha_do_tempo, linha_pulso, musicograma, partitura_cores, pauta, tira_ritmo

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), "volume4")

UNIDADES = [
    ("Unidade 1 · Som e silêncio", "--d-musica"),
    ("Unidade 2 · Pulso", "--d-musica"),
    ("Unidade 3 · Forte e fraco, rápido e lento", "--d-musica"),
    ("Unidade 4 · Os instrumentos", "--d-jogos"),
    ("Unidade 5 · Vivaldi", "--d-natureza"),
    ("Unidade 6 · Bach", "--d-matematica"),
    ("Unidade 7 · Mozart", "--d-historias"),
    ("Unidade 8 · Saint-Saëns e Debussy", "--d-artes"),
]
INICIO = {}
ROXO = "#8a6f9e"


def inicio_unidade(L, i):
    L.unidade = UNIDADES[i][0]
    INICIO[L.unidade] = L.proximo


def lado(nome, w, direita=True):
    f = "right" if direita else "left"
    m = "0 0 3mm 5mm" if direita else "0 5mm 3mm 0"
    return pd(nome, w, f"float:{f};clear:both;margin:{m}")


def tira(itens, w="22mm", gap="2mm"):
    """Fila de motivos pequenos."""
    return '<div class="centro" style="line-height:0">' + "".join(img(m, w, f"display:inline-block;margin:0 {gap}") for m in itens) + "</div>"


def secao(L, rotulo):
    return rotulo


# ================================================================== ABERTURA

def capa(L):
    instr = "".join(img(m, "27mm", "display:inline-block;margin:0 1.5mm") for m in ("violino", "flauta", "trompete", "pandeiro", "harpa"))
    notas = "".join(img(m, "15mm", "display:inline-block;margin:0 3mm") for m in ("seminima", "colcheias", "seminima"))
    c = f"""
    <div style="position:absolute;top:24mm;left:0;right:0;text-align:center">
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O Grande Tesouro de</div>
      <div style="font-weight:500;font-size:62pt;line-height:.95;letter-spacing:.02em">Marina</div>
      <div style="font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sepia);margin-top:2mm">Currículo clássico para a infância</div></div>
    <div style="position:absolute;top:84mm;left:0;right:0;text-align:center">
      <div style="font-size:10pt;letter-spacing:.3em;text-transform:uppercase;color:var(--rosa)">Volume 4</div>
      <div style="font-weight:500;font-size:30pt;line-height:1.05;margin:2mm 0">O mundo<br>da música</div>
      <div class="vinheta-sep">❦</div></div>
    <div class="centro" style="position:absolute;top:140mm;left:0;right:0">{pd("opera_rei_cole", "92mm", "margin:0 auto")}</div>
    <div class="centro" style="position:absolute;top:236mm;left:0;right:0;line-height:0">{instr}</div>
    <div class="centro" style="position:absolute;top:268mm;left:0;right:0;line-height:0">{notas}</div>"""
    L.add(c, cabecalho=False, numero=False)


def rosto(L):
    c = f"""<div class="miolo centro" style="top:40mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">O Grande Tesouro de Marina</div>
      <div style="font-size:30pt;font-weight:500;margin:6mm 0 2mm">Volume 4</div>
      <div style="font-size:20pt;font-style:italic;color:var(--sepia)">O mundo da música</div>
      <div class="vinheta-sep" style="margin:10mm 0">❦</div>
      <div style="font-size:15pt">A música deste livro é da</div>
      <div style="margin:8mm auto 0;width:110mm;border-bottom:0.6pt solid var(--linha);height:12mm;font-size:24pt;font-style:italic">Marina</div>
      <div style="margin:12mm auto 0;width:150mm">{pd("opera_navios", "74mm", "margin:0 auto")}{credito_pd("opera_navios")}</div>
      <div style="margin-top:8mm;font-size:11pt;color:var(--sepia)">começamos em _____ de ______________ de ________</div></div>"""
    L.add(c, cabecalho=False, numero=False)


def carta(L):
    texto(L, """
      <div class="centro peq versal" style="letter-spacing:.2em">Carta à família</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:5mm">Escutar antes de explicar</h1>
      <p>Uma criança aprende a língua da família ouvindo-a muito, muitas vezes, antes de falar. Com a música pode ser igual. Este volume não tem
      aula de teoria nem pede que a Marina toque coisa alguma. Ele propõe <b>escutar</b>, <b>mover o corpo</b> e <b>cantar</b>, com poucas
      músicas e muita repetição: uma obra por unidade, ouvida muitas vezes, até virar amiga.</p>
      <h2>Três ideias</h2>
      <ul>
        <li><b>Uma obra, muitas vezes</b> (Suzuki). Em vez de uma playlist infinita, escolha uma peça e toque-a na semana toda: no almoço, no banho,
        no carro. A criança só reconhece depois de ouvir dezenas de vezes, e reconhecer é a alegria.</li>
        <li><b>O corpo entende primeiro</b> (Dalcroze). Marchar, balançar, correr, parar: o pulso, o forte e o fraco, o rápido e o lento vão
        para o corpo antes de ganhar nome. Os nomes (<i>pulso</i>, <i>forte</i>, <i>piano</i>) vêm depois, devagar.</li>
        <li><b>Silêncio também é música.</b> Sem pausa e sem silêncio não há ritmo nem escuta. Por isso começamos por aí.</li>
      </ul>
      <h2>O que este volume traz</h2>
      <p>Oito unidades: <i>som e silêncio</i>, <i>pulso</i>, <i>forte e fraco, rápido e lento</i>, <i>instrumentos</i>, e depois cinco compositores,
      um por vez: <b>Vivaldi</b> (as estações), <b>Bach</b> (a onda de notas), <b>Mozart</b> (o menino e a estrelinha), <b>Saint-Saëns</b> (os bichos) e
      <b>Debussy</b> (o luar). Cada compositor tem um <i>musicograma</i>, que é a música desenhada para o adulto acompanhar com o dedo; uma proposta de movimento;
      e uma escuta tranquila.</p>
      <h2>Sobre as gravações</h2>
      <p>Um livro impresso não toca. Para cada peça indicamos <b>a obra</b> (compositor, título, instrumentos); você escolhe a gravação que tiver ou
      encontrar na biblioteca da cidade. Toda gravação tem direitos próprios; as peças que ouvimos são de compositores mortos há mais de 70 anos.</p>
      <div class="centro" style="margin-top:8mm">""" + tira(["violino", "flauta", "tambor", "trompete", "harpa", "xilofone"], "22mm", "1.5mm") + "</div>")


def como_usar(L):
    texto(L, f"""
      <div class="centro peq versal" style="letter-spacing:.2em">Como usar este volume</div>
      <h1 class="titulo" style="font-size:24pt;margin-bottom:4mm">Uma caixa de música</h1>
      <p>Monte, antes de começar, uma <b>caixa de música</b>: um tambor (pode ser uma lata com tampa de plástico), um chocalho (a Unidade 1 ensina a fazer),
      um pandeiro, dois pauzinhos de madeira lisos, um sino pequeno, um lenço de seda para dançar e um aparelho de som simples. Quase todas as propostas usam essas coisas.</p>
      <table class="tab">
        <tr><th>Ritmo</th><td>Dois encontros por fim de semana, de 15 a 20 minutos. Uma unidade a cada dois fins de semana. Música para escutar fica ligada o resto da semana, baixinho.</td></tr>
        <tr><th>Escuta</th><td>Cada compositor tem <b>uma obra</b>. Toque-a no início e no fim de cada encontro e outras vezes durante a semana. Sem cobrar nada: ela pode ouvir brincando.</td></tr>
        <tr><th>Volume</th><td>Baixo. Se for preciso levantar a voz para falar por cima da música, está alto demais para uma criança de 2 anos.</td></tr>
        <tr><th>Pauta e notas</th><td>As partituras são para o <b>adulto</b>. Os desenhos de ritmo (<i>ta</i> e <i>ti-ti</i>) e os musicogramas são para mostrar à criança, sem explicar.</td></tr>
        <tr><th>Cantar</th><td>Cante você mesmo, sem medo de desafinar: a voz que ela mais quer ouvir é a sua. As melodias do caderno final cabem numa voz comum.</td></tr>
        <tr><th>Idiomas</th><td>Os cartões trazem o nome em inglês, francês e (quando existe) latim no verso. Cantigas francesas e inglesas aparecem no caderno final.</td></tr>
      </table>
      <h2>Segurança</h2>
      <p>Chocalhos têm de ter a tampa colada. Pauzinhos, só lisos e sem ponta. Sons muito altos e fones de ouvido: não para crianças desta idade.</p>
      <div class="centro" style="margin-top:5mm">{tira(["tambor", "chocalho", "pandeiro", "sino", "triangulo_inst"], "20mm")}</div>""")


def sumario(inicio):
    linhas = "".join(f'<tr><td><span class="bolinha" style="background:var({cor})"></span>{n.split(" · ")[0]}</td>'
                     f'<td style="font-size:13pt">{n.split(" · ", 1)[1]}</td><td class="pg">{inicio.get(n, "")}</td></tr>' for n, cor in UNIDADES)
    linhas += f'<tr><td></td><td style="font-size:13pt">Encerramento · Caderno de cantigas, diário de escuta e créditos</td><td class="pg">{inicio.get("Encerramento", "")}</td></tr>'
    return f"""<div class="miolo">{titulo("Sumário", "Volume 4 · O mundo da música", 30)}<table class="sumario">{linhas}</table>
      <div class="centro" style="margin-top:8mm">{tira(["violino", "flauta", "trompete", "harpa", "piano", "pandeiro"], "22mm", "1.5mm")}</div></div>"""


# ================================================================== U1 SOM E SILÊNCIO

def unidade1(L):
    inicio_unidade(L, 0)
    guia(L, dict(
        titulo="Unidade 1 · Som e silêncio", aba="--d-musica",
        pergunta="O que eu escuto? E quando tudo fica quieto? — a escuta como primeiro gesto da música.",
        duracao="Dois fins de semana · dois encontros · 15 minutos. Comece pela janela: “que sons tem agora?”.",
        objetivos=["Escutar com atenção e nomear sons do dia a dia.", "Associar o som ao bicho ou ao objeto que o faz.",
                   "Distinguir som e silêncio e controlar o corpo no silêncio (estátua).", "Fazer um instrumento simples (chocalho).",
                   "Ouvir a mesma canção várias vezes e reconhecê-la."],
        repertorio="<b>Cantiga:</b> <i>Ding, dong, bell</i> (tradicional inglesa, partitura de <i>The Baby's Opera</i>, de Walter Crane, 1877). "
                   "<b>Escuta:</b> o som de sinos de verdade e o silêncio da casa. <b>Línguas:</b> <i>sound · le son · sonus</i>; <i>silence · le silence · silentium</i>.",
        materiais="Cartões de sons; um sino; um tambor; um pote de plástico com tampa de rosca e arroz (chocalho); um lenço.",
        vida="Passeio sonoro pela casa e pelo quintal: parar, fechar os olhos, escutar, contar os sons.",
        etapas=[["Escutar a casa com os olhos fechados.", "Passeio sonoro.", "Sons dos cartões."],
                ["Parear som e bicho.", "Estátua musical.", "Fazer o chocalho."],
                ["Imitar os sons com a voz.", "Inventar um som novo.", "Tocar e parar: ela comanda."]],
        indicadores=["Fica quieta por alguns segundos para escutar.", "Diz de onde vem um som.", "Imita o som do galo, da vaca, do sino.",
                     "Para quando a música para.", "Toca o chocalho e o interrompe.", "Pede a canção do sino de novo."],
        interesse="gravar os sons da casa no celular e escutar com ela depois, adivinhando.",
        dificil="só o passeio sonoro de olhos abertos, apontando.",
        alerta="<b>Arroz, feijão e contas</b> só dentro de um pote bem fechado, com a tampa colada por um adulto."))

    cartoes(L, "Sons que conheço", [
        dict(pt="sino", mot="sino", en="bell", fr="la cloche", la="tintinnābulum", som="dlém, dlém", dica="Toque um sino de verdade. Quanto tempo o som dura até sumir?"),
        dict(pt="tambor", mot="tambor", en="drum", fr="le tambour", la="tympanum", som="tum, tum, tum", dica="Batidas fortes e fracas: ela escuta de olhos fechados."),
        dict(pt="galo", pd="cartao_galo", en="rooster", fr="le coq", la="gallus", som="cocoricó", dica="Quem canta de manhã? Imite junto, bem alto."),
        dict(pt="vaca", pd="cartao_vaca", en="cow", fr="la vache", la="vacca", som="múúú", dica="Um som grande e redondo, que sai da barriga."),
        dict(pt="gato", mot="gato", en="cat", fr="le chat", la="fēlēs", som="miau", dica="Um som fininho. Ela consegue fazer baixinho?"),
        dict(pt="pato", mot="patinho", en="duck", fr="le canard", la="anas", som="quá, quá", dica="Dois sons iguais, um depois do outro. Bata palmas no mesmo ritmo."),
        dict(pt="chuva", html=img("gota", "30mm"), en="rain", fr="la pluie", la="pluvia", som="plic, plic", dica="Pingos leves. Faça a chuva cair com os dedos na mesa, depois mais forte."),
        dict(pt="trovão", mot="m_trovao", en="thunder", fr="le tonnerre", la="tonitrus", som="bum, ruuum", dica="Som grande e longo. Faça com a voz e com o tambor."),
        dict(pt="cuco", mot="cuco", en="cuckoo", fr="le coucou", la="cuculus", som="cu-cu", dica="Dois sons, um agudo e um mais grave. O cuco volta na Unidade 8, com Saint-Saëns.")],
        "Volume 4 · Sons que conheço")

    c = f"""<div class="miolo">{titulo("Os sons do dia", "o que eu escuto agora?", 28)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm 6mm;margin-top:5mm">
        <div class="centro">{img("dia_amanhecer", "46mm", "margin:0 auto")}<div class="legenda-q">de manhã: o galo, a água, os passos</div></div>
        <div class="centro">{img("dia_meiodia", "46mm", "margin:0 auto")}<div class="legenda-q">ao meio-dia: panelas, vozes, a rua</div></div>
        <div class="centro">{img("dia_entardecer", "46mm", "margin:0 auto")}<div class="legenda-q">no fim da tarde: pássaros, o vento</div></div>
        <div class="centro">{img("dia_noite", "46mm", "margin:0 auto")}<div class="legenda-q">à noite: grilos, a casa dormindo</div></div></div></div>
      {adulto("escutar o dia",
              "Pare num momento qualquer do dia com a Marina, peça silêncio (“vamos escutar com a orelha de coelho”) e fiquem um minuto quietos. "
              "Depois pergunte: “o que a orelha escutou?”. Você diz um som, ela diz outro. Repita em horas diferentes (manhã, tarde, noite) e em lugares "
              "diferentes (cozinha, quintal, rua). Aos poucos ela percebe que <b>o silêncio nunca é vazio</b>: sempre há som, e escutar é uma atividade.")}"""
    L.add(c, aba="--d-musica")

    passos(L, "Estátua musical", "o som anda, o silêncio para",
           [(img("tambor", "26mm"), "Você toca o tambor: ela anda pela sala"),
            (img("pegada", "20mm") + img("pegada_esq", "20mm"), "Cada batida, um passo"),
            (img("sino", "24mm"), "Toque o sino: o som para… e ela vira estátua"),
            (img("lua", "24mm"), "Silêncio! Contem até três, quietinhas"),
            (img("tambor", "26mm"), "O tambor volta e ela volta a andar"),
            (img("estrela", "24mm"), "Troquem: agora ela toca e você é a estátua")],
           adulto("controlar o corpo no silêncio",
                  "Brincar de estátua é o primeiro exercício de música sem som: <b>parar junto com a música</b> exige escutar. No começo, avise antes de parar; depois, "
                  "pare de repente. Se ela rir e se jogar no chão, perfeito: a brincadeira funcionou. Quando for fácil, pare em lugares diferentes da música "
                  "(no meio de uma canção, no fim de uma frase). <b>Criar:</b> ela toca e comanda; é a vez dela de escolher quando parar."),
           aba="--d-musica")

    onda1 = "M30 74 q8 -12 16 0 t16 0 t16 0 t16 0 t16 0 t16 0 t16 0 t16 0"
    reta = "M30 146 L180 146"
    onda2a = "M30 218 q8 -12 16 0 t16 0 t16 0"
    onda2b = "M118 218 q8 -12 16 0 t16 0 t16 0"
    svg = (pontilhado(onda1) + pontilhado(reta) + pontilhado(onda2a) + pontilhado(onda2b)
           + ponto_inicio(30, 74) + ponto_inicio(30, 146) + ponto_inicio(30, 218)
           + f'<line x1="79" y1="212" x2="79" y2="224" stroke="var(--rosa)" stroke-width="0.6" stroke-dasharray="1 1"/>')
    c2 = f"""<div class="miolo">{titulo("Som e silêncio", "seguir a linha com o dedo", 28)}</div>
    <div style="position:absolute;left:30mm;top:56mm" class="peq it">um som que continua…</div>
    <div style="position:absolute;left:30mm;top:128mm" class="peq it">silêncio… (a voz fica quieta)</div>
    <div style="position:absolute;left:30mm;top:196mm" class="peq it">som, silêncio, som</div>
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>
    {adulto("traçar o som",
            "A linha ondulada é o <b>som</b>: ela segue com o dedo, fazendo “uuuu” com a voz enquanto o dedo anda. A linha reta de pontinhos é o <b>silêncio</b>: o dedo "
            "anda e a voz fica quieta. Na terceira, ela alterna: voz, quieta, voz. Depois repita com lápis grosso. Não precisa ficar bonito; o gesto longo e contínuo é o que "
            "prepara a mão para escrever.", estilo="top:236mm;bottom:auto")}"""
    L.add(c2, aba="--d-musica")

    historia(L, "Ding, dong, sino!", "cantiga inglesa · tradução da coleção · partitura original", f"""
      <div style="margin:2mm 0 3mm">{pd("opera_ding_dong", "105mm")}</div>
      <p style="font-size:14.5pt;line-height:1.55;text-align:center;font-style:italic">Ding, dong, sino!<br>O gatinho caiu no poço.<br>
      Quem o jogou? O pequeno Tomás Lin.<br>Quem o tirou? O pequeno Tomás Forte.<br>Ah, que menino bom foi esse!</p>""",
             adulto("um sino na partitura",
                    "A gravura de Walter Crane mostra o menino que toca o sino e o outro que puxa o gatinho do poço. Cante devagar e, em cada <i>ding</i> e <i>dong</i>, bata no sino ou "
                    "na tampa de uma panela. A partitura original, em inglês, está na própria página: é uma melodia antiga, curta, de poucas notas; vale cantar a que vocês "
                    "conhecem. A letra tradicional continua com um menino malvado; aqui adaptamos o fim para algo mais gentil.",
                    credito_pd("opera_ding_dong")), aba="--d-musica")

    passos(L, "Passeio sonoro", "um passeio de ouvidos",
           [(img("pegada", "20mm") + img("pegada_esq", "20mm"), "Andamos devagar pela casa, sem falar"),
            (img("palma", "24mm"), "Paramos. Mão na orelha: escutar"),
            (img("lua", "22mm"), "Fechamos os olhos por um momento"),
            (img("cuco", "24mm"), "Cada um conta quantos sons escutou"),
            (img("sino", "22mm"), "Cada som, um dedo. Quantos dedos?"),
            (img("caixa", "24mm"), "Ela escolhe um som para imitar com a voz")],
           adulto("escuta como atenção",
                  "Faça este passeio dentro de casa e, se puderem, no quintal ou no parque. A regra é uma só: <b>sem falar</b>. Mostre com a mão onde está um som (a geladeira, "
                  "um carro, um pássaro). Ao final, peça que ela imite um dos sons: é a primeira vez que ela <i>reproduz</i> um som que ouviu, e isso é a base de cantar."),
           aba="--d-vida")

    passos(L, "Vamos fazer um chocalho", "o primeiro instrumento da caixa de música",
           [(img("tigela", "24mm"), "Escolha um pote de plástico pequeno, com tampa de rosca"),
            (img("ervilha", "20mm"), "Ponha dentro um punhado pequeno de arroz (adulto)"),
            (img("rolha", "22mm"), "Feche a tampa e cole bem (cola quente, só o adulto)"),
            (img("florzinha_rosa", "20mm"), "Decore por fora com tiras de papel e fita"),
            (img("chocalho", "26mm"), "Sacuda devagar… e depressa!"),
            (img("cesta", "24mm"), "Guarde na caixa de música")],
           adulto("fazer e tocar",
                  "<b>Segurança:</b> a tampa precisa ficar colada e, por cima, fechada com fita; grãos soltos são risco de engasgo. Teste você mesmo antes de entregar. "
                  "Peça que ela toque junto com uma música que já conhece. <b>Criar:</b> faça um segundo chocalho com outro enchimento (feijão, miçangas grandes, areia) e compare os sons: "
                  "qual é mais fraco? qual é mais forte? É assim que ela descobre que o <i>material</i> muda o som."),
           aba="--d-vida")


# ================================================================== U2 PULSO

def unidade2(L):
    inicio_unidade(L, 1)
    guia(L, dict(
        titulo="Unidade 2 · Pulso", aba="--d-musica",
        pergunta="Onde está a batida? — o pulso, o chão firme sobre o qual a música anda.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos, sempre com movimento.",
        objetivos=["Marchar, balançar e bater palmas no mesmo pulso da música.", "Sentir o pulso do próprio coração.",
                   "Distinguir pulso (a batida que não muda) de ritmo (as palavras sobre a batida).", "Ouvir e imitar <i>ta</i>, <i>ti-ti</i> e silêncio.",
                   "Embalar, ninar e dançar em roda."],
        repertorio="<b>Cantigas:</b> <i>Marcha, soldado</i> (tradicional brasileira); <i>Here we go round the mulberry bush</i> (<i>Aqui vamos nós em volta da amoreira</i>); "
                   "<i>Dance a baby, diddy</i>; <i>Hush-a-by baby</i> (partituras de <i>The Baby's Opera</i>, Walter Crane, 1877). <b>Línguas:</b> "
                   "<i>beat · la pulsation · pulsus</i> (o latim <i>pulsus</i> é a batida do coração).",
        materiais="Tambor, pandeiro ou colher e panela; lenço; um espaço para andar em roda; os cartões da unidade.",
        vida="Andar no ritmo: escada, calçada, caminhada ao mercado, pondo a mesa devagar e depressa.",
        etapas=[["Marchar e bater palmas.", "Pulso do coração.", "Embalar e ninar."],
                ["Ta e ti-ti.", "Ritmo das palavras (frutas).", "Roda da amoreira."],
                ["Inventar um passo novo.", "Ela toca, você marcha.", "Mudar a velocidade sem perder a batida."]],
        indicadores=["Anda no pulso quando há música.", "Acompanha palmas no mesmo ritmo.", "Sente e mostra o coração.",
                     "Imita <i>ta</i> e <i>ti-ti</i> depois de ouvir.", "Embala com calma.", "Pede de novo a roda."],
        interesse="marchar no pulso de músicas diferentes e comparar: esta é mais rápida? mais calma?",
        dificil="só marchar de mãos dadas, cantando.",
        alerta="<b>Se ela não acompanha o pulso:</b> é comum antes dos 4 anos. Continue com o movimento sem corrigir; o pulso vem com a repetição."))

    pegs = "".join(img("pegada" if k % 2 == 0 else "pegada_esq", "13mm", f"display:inline-block;margin:{'0' if k % 2 == 0 else '5mm'} 3.2mm 0") for k in range(8))
    c = f"""<div class="miolo">{titulo("Marcha, soldado", "uma batida de cada vez, todas iguais", 28)}
      <p class="centro" style="font-size:17pt;line-height:1.6;font-style:italic;margin:3mm 0 2mm">Marcha, soldado,<br>cabeça de papel;<br>quem não marchar direito<br>vai preso no quartel.</p>
      <div style="margin:2mm 0">{linha_pulso(8, 170, [0, 4])}</div>
      <div class="centro" style="line-height:0;margin-top:1mm;height:24mm">{pegs}</div>
      <div class="centro peq" style="margin-top:1mm">um passo para cada batida; os círculos cheios são os passos mais fortes</div>
      <h2 class="titulo" style="font-size:15pt;margin:4mm 0 1mm;text-align:left">O pulso na partitura <span class="peq it" style="font-weight:400">— para o adulto</span></h2>
      {pauta([("G4", "q")] * 4 + ["|"] + [("G4", "q")] * 4, 170, 2.3, letra=["Mar", "cha", "sol", "da", "do", "ca", "be", "ça"])}
      <div class="centro peq" style="margin-top:1mm">oito semínimas na mesma nota: o pulso escrito. Cada nota dura uma batida.</div>
      <div style="margin-top:3mm;display:grid;grid-template-columns:40mm 1fr;gap:6mm;align-items:center">{pd("opera_sinos", "40mm")}
        <div style="font-size:12.5pt;line-height:1.5;font-style:italic">“Laranjas e limões”, dizem os sinos de São Clemente. Outra cantiga para marchar: os sinos de Londres, num jogo em que as crianças passam, em fila, por baixo de um arco de braços.<div class="peq" style="font-style:normal;margin-top:1.5mm">Partitura e gravura de Walter Crane, em <i>The Baby's Opera</i>.</div></div></div></div>
      {adulto("o pulso",
              "<b>Pulso</b> é a batida regular, que não muda, como os passos de quem caminha. A música pode ser rápida ou lenta, mas o pulso embaixo é sempre igual. "
              "Marche com ela no ritmo de um passeio tranquilo e cante a cantiga; no primeiro passo de cada grupo de quatro, bata o pé um pouco mais forte (os círculos "
              "cheios da figura). <b>Criar:</b> ela puxa a fila, você segue o passo dela. A letra é tradicional; a melodia varia de lugar para lugar, por isso a partitura mostra só o pulso.", credito_pd("opera_sinos"))}"""
    L.add(c, aba="--d-musica")

    c = f"""<div class="miolo">{titulo("O pulso do meu coração", "o primeiro instrumento", 28)}
      <div class="centro" style="line-height:0;margin:5mm 0 3mm">{img("palma", "40mm", "display:inline-block;margin:0 6mm")}{img("coracao", "36mm", "display:inline-block;margin:0 6mm")}</div>
      <ol class="perguntas" style="font-size:12.5pt">
        <li>Ponha a mão no peito: o que você sente?</li><li>Bate sempre igual? Bate devagar ou depressa?</li>
        <li>Corra no lugar por um momento. E agora?</li><li>Fique quietinha. Ele volta a ficar devagar?</li>
        <li>Ponha a mão no peito de quem está ao seu lado.</li></ol>
      <h2 class="titulo" style="font-size:14pt;margin:5mm 0 1mm;text-align:left">Quando descanso</h2>{linha_pulso(6, 170)}
      <h2 class="titulo" style="font-size:14pt;margin:3mm 0 1mm;text-align:left">Quando corro</h2>{linha_pulso(15, 170)}
      <div class="centro peq it" style="margin-top:1mm">as batidas ficam mais juntas, mas continuam todas iguais</div></div>
      {adulto("o pulso mais antigo",
              "O coração é o pulso que ela ouviu antes de nascer. Deixe que ela encoste o ouvido no seu peito. Depois, com a mão dela no peito dela, bata junto o pulso "
              "com um dedo na mesa. Ao correr, o coração acelera; ao descansar, ele desacelera. É a primeira vez que ela <b>percebe</b> que o pulso pode mudar de velocidade "
              "sem deixar de ser pulso. O latim <i>pulsus</i> (“batida”) deu origem a <i>pulso</i>, em português.")}"""
    L.add(c, aba="--d-musica")

    jogo = [("elefante", "elefante passando", ["ta", "ta", "ta", "sh"]), ("ratinho", "ratinho correndo", ["ti", "ti", "ta", "sh"]), ("tartaruga", "tartaruga andando", ["ta", "sh", "ta", "sh"])]
    linhas_jogo = "".join(f'<tr><td style="width:36mm;text-align:center;vertical-align:middle">{img(m, "18mm", "margin:0 auto")}<div class="peq">{t}</div></td>'
                          f'<td style="vertical-align:middle">{tira_ritmo(r, 110, ROXO, True, 1.0)}</td></tr>' for m, t, r in jogo)
    c = f"""<div class="miolo">{titulo("Ta e ti-ti", "os desenhos do ritmo", 28)}
      <table class="tab" style="margin-top:4mm;font-size:12pt">
        <tr><td style="width:44mm">{tira_ritmo(["ta"], 26, ROXO, False, 1.15)}</td><td style="vertical-align:middle"><b>ta</b> — uma batida, um som. Como um passo.</td></tr>
        <tr><td>{tira_ritmo(["ti"], 26, ROXO, False, 1.15)}</td><td style="vertical-align:middle"><b>ti-ti</b> — duas batidas rápidas dentro de um passo. Como um ratinho correndo.</td></tr>
        <tr><td>{tira_ritmo(["sh"], 26, ROXO, False, 1.15)}</td><td style="vertical-align:middle"><b>sh</b> — silêncio. A mão para no ar, e ainda assim conta.</td></tr></table>
      <h2 class="titulo" style="font-size:15pt;margin:5mm 0 1mm;text-align:left">Bata e diga</h2>
      <div style="margin:0">{tira_ritmo(["ta", "ta", "ti", "ta"], 130, ROXO, True, 1.0)}</div>
      <div style="margin:0">{tira_ritmo(["ti", "ti", "ta", "sh"], 130, ROXO, True, 1.0)}</div>
      <h2 class="titulo" style="font-size:15pt;margin:3mm 0 1mm;text-align:left">Quem anda assim?</h2>
      <table class="tab">{linhas_jogo}</table></div>
      {adulto("ritmo sem escrever",
              "O <b>ritmo</b> é o desenho das batidas sobre o pulso. Mostre o desenho, <b>diga</b> o que está nele (“ta, ta, ti-ti, ta”) e <b>bata</b> palmas; ela repete. Só depois mostre o desenho. "
              "É o contrário do que se faz na escola, e é o que dá certo: primeiro o som, depois o símbolo. As hastes do desenho são as de uma partitura de verdade, sem a pauta. "
              "<b>Quem anda assim?</b> Bata cada ritmo e peça que ela adivinhe o bicho: o elefante é pesado (<i>ta, ta, ta</i>), o ratinho corre (<i>ti-ti, ti-ti, ta</i>). "
              "Nome da Marina: <i>Ma-ri-na</i> (ti-ti ta).")}"""
    L.add(c, aba="--d-musica")

    frutas = [("uva", "u-va", 2), ("pera", "pe-ra", 2), ("maca", "ma-çã", 2), ("morango", "mo-ran-go", 3), ("banana", "ba-na-na", 3),
              ("laranja", "la-ran-ja", 3), ("melancia", "me-lan-ci-a", 4), ("jabuticaba", "ja-bu-ti-ca-ba", 5)]
    cel = "".join(f'<div class="centro" style="border-bottom:0.4pt solid var(--linha);padding:2mm 0">{img(m, "21mm", "margin:0 auto")}'
                  f'<div style="font-size:12.5pt;font-weight:500">{s}</div>{tira_ritmo(["ta"] * n, 12 * n + 8, ROXO, False)}</div>' for m, s, n in frutas)
    c = f"""<div class="miolo">{titulo("O ritmo das palavras", "uma batida para cada pedaço", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm;margin-top:4mm">{cel}</div></div>
      {adulto("bater as palavras",
              "Cada pedaço da palavra (cada sílaba) é uma batida. Diga <i>u-va</i> batendo duas palmas, <i>ba-na-na</i> batendo três. Em seguida, deixe que ela escolha uma fruta e "
              "você adivinha qual é só pelo número de palmas. É a primeira leitura de ritmo e também ensina a separar sílabas, que a ajuda na alfabetização. "
              "<b>Criar:</b> palavras do dia a dia (nomes de pessoas, bichos, comidas).")}"""
    L.add(c, aba="--d-musica")

    historia(L, "Dança, neném, dança", "cantiga inglesa · tradução da coleção · partitura original", f"""
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin:1mm 0 3mm">{pd("opera_embalar", "80mm")}{pd("opera_ninar", "80mm")}</div>
      <p style="font-size:14.5pt;line-height:1.55;text-align:center;font-style:italic">Dança, neném, dança!<br>O que a mamãe vai fazer com ele?<br>
      Sentá-lo no colo, dar-lhe um mingau<br>e dançar, neném, dançar!</p>
      <div class="caixa" style="margin-top:6mm"><div class="versal" style="font-size:12pt;letter-spacing:.1em;margin-bottom:1.5mm">Três jeitos de embalar</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;font-size:11.5pt;line-height:1.35;text-align:center">
          <div>{linha_pulso(4, 48)}<b>balançar</b><br>o corpo vai e volta, devagar</div>
          <div>{linha_pulso(6, 48)}<b>ninar</b><br>cante baixinho, só “lá, lá, lá”</div>
          <div>{linha_pulso(8, 48)}<b>dançar</b><br>passinhos curtos no pulso</div></div></div>""",
             adulto("embalar e ninar",
                    "Senta-se com ela no colo e, a cada batida, balance suavemente para a direita e a esquerda: é o <b>pulso do embalo</b>. Cante bem devagar. Para ninar, a "
                    "partitura de <i>Hush-a-by baby</i> (a segunda gravura, também de Crane) tem uma melodia suave, mas a letra original é triste (o berço cai do galho); use só a "
                    "melodia e invente uma letra sua. Cantar baixinho, no pulso do balanço, é uma das músicas mais antigas e mais importantes da infância.",
                    credito_pd("opera_embalar", "opera_ninar")), aba="--d-musica")

    historia(L, "Aqui vamos nós, em volta da amoreira", "roda inglesa · tradução da coleção · gravura e partitura originais", f"""
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin:2mm 0 3mm">{pd("opera_amoreira_roda", "80mm")}{pd("opera_amoreira", "80mm")}</div>
      <p style="font-size:14pt;line-height:1.55;text-align:center;font-style:italic">Aqui vamos nós, em volta da amoreira,<br>da amoreira, da amoreira;<br>
      aqui vamos nós, em volta da amoreira,<br>numa manhã gelada.<br>Assim batemos palmas, assim batemos palmas,<br>numa manhã gelada.</p>
      <div class="caixa" style="margin-top:5mm"><div class="versal" style="font-size:12pt;letter-spacing:.1em;margin-bottom:1.5mm">Estrofes para inventar</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1mm 6mm;font-size:12pt;line-height:1.4;font-style:italic">
          <div>Assim batemos os pés…</div><div>Assim esfregamos as mãos…</div><div>Assim pulamos de lado…</div><div>Assim giramos devagar…</div>
          <div>Assim fazemos silêncio…</div><div>Assim… (ela escolhe!)</div></div></div>""",
             adulto("roda e movimento",
                    "De mãos dadas, andem em círculo, no pulso, cantando. Quando chegar o verso das palmas, soltem as mãos e batam palmas no mesmo pulso; voltem a girar. "
                    "Cada estrofe, uma ação nova (pular, bater os pés, esfregar as mãos). É a base de toda roda cantada, inclusive das nossas (<i>ciranda, cirandinha</i>), que "
                    "estão no caderno final. A gravura é uma pintura de Crane; a partitura original, em inglês, está ao lado.",
                    credito_pd("opera_amoreira_roda", "opera_amoreira")), aba="--d-musica")

    pegadas = "".join(
        f'<image href="build/arte/{"pegada" if k % 2 == 0 else "pegada_esq"}.png" x="{x - 7:.1f}" y="{y - 9:.1f}" width="14" height="18" transform="rotate({r} {x} {y})"/>'
        for k, (x, y, r) in enumerate(((36, 96, 80), (62, 83, 70), (88, 75, 90), (114, 79, 100), (140, 91, 110), (160, 110, 120),
                                       (166, 138, 150), (155, 164, 170), (130, 180, 190), (102, 184, 190), (74, 178, 195))))
    from livro import arte
    for n_ in ("pegada", "pegada_esq"):
        arte(n_)
    c = f"""<div class="miolo">{titulo("Passos no caminho", "um passo para cada pegada", 28)}</div>
    <svg class="svgpag" viewBox="0 0 210 297">{pegadas}{ponto_inicio(26, 100)}</svg>
    <div class="centro peq it" style="position:absolute;left:0;right:0;top:204mm">todos os passos têm o mesmo tamanho: esse é o pulso</div>
    {adulto("o pulso nos pés",
            "Coloque as pegadas no chão (recorte-as de papel ou desenhe com giz) a uma distância igual e ande por elas no pulso de uma música lenta. Depois, mude: espace mais as pegadas, "
            "e a música fica mais lenta; aproxime, e fica mais rápida. Mostre que <b>distância igual = pulso igual</b>. É também a prática de contar passos e de andar em fila. "
            "Marque o início (círculo verde) e a chegada com uma figura de que ela goste.", estilo="top:216mm;bottom:auto")}"""
    L.add(c, aba="--d-musica")


def colunas(rotulos, top=46, alt=84):
    n = len(rotulos)
    w = (178 - (n - 1) * 6) / n
    return "".join(f'<div style="position:absolute;left:{16 + i * (w + 6):.1f}mm;top:{top}mm;width:{w:.1f}mm;height:{alt}mm" class="caixa centro">'
                   f'<div style="font-size:16pt;font-weight:600">{r}</div></div>' for i, r in enumerate(rotulos))


def recortes(itens, top, w=30, h=38):
    cel = "".join(f'<div class="carta" style="width:{w}mm;height:{h}mm;display:inline-flex;margin:1mm;vertical-align:top">{html}<div class="peq">{n}</div></div>'
                  for html, n in itens)
    return f'<div class="centro" style="position:absolute;left:20mm;right:20mm;top:{top}mm">{cel}</div>'


# ================================================================== U3 FORTE E FRACO, RÁPIDO E LENTO

def unidade3(L):
    inicio_unidade(L, 2)
    guia(L, dict(
        titulo="Unidade 3 · Forte e fraco, rápido e lento", aba="--d-musica",
        pergunta="Como é esse som? — os contrastes que fazem a música andar: forte e fraco, rápido e lento, grave e agudo.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos, com o corpo inteiro.",
        objetivos=["Perceber e produzir sons fortes e fracos, rápidos e lentos, graves e agudos.", "Mover o corpo para mostrar o que escuta.",
                   "Ligar o contraste a um bicho ou a um personagem (elefante e ratinho, tartaruga e lebre).", "Traçar linhas que mostram intensidade e velocidade.",
                   "Aprender os primeiros nomes dos músicos: <i>forte</i>, <i>piano</i>, <i>lento</i>, <i>depressa</i>."],
        repertorio="<b>Fábula:</b> <i>A lebre e a tartaruga</i> (Esopo; gravura de Arthur Rackham, 1912). <b>Conto:</b> <i>Cachinhos Dourados e os três ursos</i> (gravuras de L. Leslie Brooke, 1905). "
                   "<b>Escuta:</b> <i>Tartarugas</i> e <i>O elefante</i>, de <i>O Carnaval dos Animais</i> (Saint-Saëns, 1886). "
                   "<b>Línguas:</b> <i>slow · lent · lentus</i>; <i>fast · vite · celer</i>; <i>loud/strong · fort · fortis</i>.",
        materiais="Tambor, pandeiro, lenço, um pedaço de papel e a voz; os cartões de contraste; fita crepe para marcar o chão.",
        vida="Falar baixo no quarto do bebê e alto no quintal; andar devagar na escada e depressa na calçada.",
        etapas=[["Andar devagar e depressa.", "Bater forte e fraco no tambor.", "Vozes de urso (grande, médio, pequeno)."],
                ["Cartões de contraste.", "Pesado e leve: classificar.", "Traçar ondas grandes e pequenas."],
                ["Ela comanda: “mais forte!”, “mais devagar!”.", "Inventar um bicho que anda rápido e fala baixo.", "Dançar os contrastes."]],
        indicadores=["Anda devagar e depressa sob comando.", "Toca forte e fraco no tambor.", "Usa as palavras <i>forte</i>, <i>fraco</i>, <i>devagar</i>, <i>depressa</i>.",
                     "Mostra com o corpo o que ouve (grande e pequeno).", "Liga o elefante ao som grave e o ratinho ao agudo.", "Pede “mais forte!”."],
        interesse="escutar <i>Tartarugas</i> e <i>O elefante</i>, de Saint-Saëns, e adivinhar quem é quem.",
        dificil="só “devagar e depressa” andando, sem tambor.",
        alerta="<b>Forte não é gritar.</b> Combine antes: forte é com o tambor e as palmas; a voz fica sempre confortável."))

    c = f"""<div class="miolo historia">{titulo("A lebre e a tartaruga", "uma fábula de Esopo para escutar a velocidade", 26)}
      {lado("rackham_lebre", "66mm")}
      <p style="font-size:15.5pt;line-height:1.5">A lebre vivia dizendo que ninguém corria tanto quanto ela. A tartaruga, devagar, disse: “Vamos apostar uma corrida.”</p>
      <p style="font-size:15.5pt;line-height:1.5">A lebre saiu <i>depressa-depressa-depressa</i>, parou, deitou na sombra e dormiu. A tartaruga seguiu <i>devagar… devagar… devagar…</i>
      sem parar nunca.</p>
      <p style="font-size:15.5pt;line-height:1.5;clear:both">Quando a lebre acordou, a tartaruga já estava cruzando a linha de chegada.</p>
      <div style="margin-top:3mm">
        <div style="display:flex;align-items:center;gap:5mm">{img("tartaruga", "20mm")}<div style="flex:1"><b>devagar</b>{linha_pulso(4, 130)}</div></div>
        <div style="display:flex;align-items:center;gap:5mm;margin-top:2mm">{img("ratinho", "20mm")}<div style="flex:1"><b>depressa</b>{linha_pulso(16, 130)}</div></div></div></div>
      {adulto("o andamento",
              "<b>Andamento</b> é a velocidade do pulso. Conte a fábula com o tambor: batidas bem espaçadas para a tartaruga, batidas juntinhas para a lebre. "
              "Os músicos dizem <i>lento</i> (devagar) e <i>allegro</i> ou <i>presto</i> (depressa), palavras italianas que você vai ver nas partituras. "
              "Saint-Saëns pôs uma <i>Tartaruga</i> em <i>O Carnaval dos Animais</i>: uma melodia conhecida que ele toca lentíssima. Para a lebre, qualquer <i>galope</i> rápido serve.",
              credito_pd("rackham_lebre").replace('class="credito"', 'class="credito"'))}"""
    L.add(c, aba="--d-musica")

    c = f"""<div class="miolo">{titulo("Três vozes de urso", "grande, média e pequena", 28)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:5mm;align-items:end">
        <div class="centro">{img("elefante", "46mm", "margin:0 auto")}<div class="legenda-q"><b>Papai Urso</b><br>voz grande, grave e forte<br>“Quem comeu o meu mingau?”</div></div>
        <div class="centro">{img("gato", "36mm", "margin:0 auto")}<div class="legenda-q"><b>Mamãe Ursa</b><br>voz média<br>“Quem comeu o meu mingau?”</div></div>
        <div class="centro">{img("cuco", "26mm", "margin:0 auto")}<div class="legenda-q"><b>Bebê Urso</b><br>voz pequena, aguda e fraca<br>“Quem comeu o meu mingau?”</div></div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:8mm">
        <div class="centro">{pd("brooke_mingau", "78mm")}</div><div class="centro">{pd("brooke_camas_ursos", "78mm")}</div></div></div>
      {adulto("grave e agudo, forte e fraco",
              "No conto de <i>Cachinhos Dourados</i>, as três vozes dos ursos já são uma aula de música: <b>grave</b> (som baixo, como o do papai) e <b>agudo</b> (som alto, como o do bebê) "
              "não têm a ver com volume. Diga a mesma frase com as três vozes e peça que ela aponte quem é. Depois separe: “agora grave e <i>fraco</i>”, “agora agudo e <i>forte</i>”. "
              "Esta é a descoberta mais difícil da página: as duas coisas são independentes. As ilustrações são de L. Leslie Brooke; os bichos do alto são da coleção.",
              credito_pd("brooke_mingau", "brooke_camas_ursos"))}"""
    L.add(c, aba="--d-musica")

    svg = (pontilhado("M30 78 q12 -20 24 0 t24 0 t24 0 t24 0 t24 0 t24 0", w=3.0)
           + pontilhado("M30 150 q4 -6 8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0")
           + pontilhado("M30 222 q12 -18 24 0 t24 0 q4 -6 8 0 t8 0 t8 0 t8 0 q12 -18 24 0 t24 0")
           + ponto_inicio(30, 78) + ponto_inicio(30, 150) + ponto_inicio(30, 222))
    c = f"""<div class="miolo">{titulo("Ondas grandes e pequenas", "seguir as linhas com o dedo e a voz", 26)}</div>
    <div style="position:absolute;left:30mm;top:50mm" class="peq it">ondas grandes: <b>forte</b> (voz grande)</div>
    <div style="position:absolute;left:30mm;top:122mm" class="peq it">ondas pequenas: <b>fraco</b> (voz pequena)</div>
    <div style="position:absolute;left:30mm;top:194mm" class="peq it">grande, grande, pequena, pequena, pequena, grande, grande</div>
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>
    {adulto("traçar a intensidade",
            "Ela segue a linha com o dedo e a voz: onda grande, voz grande e forte; onda pequena, voz pequena e fraca. Pare e comente: “aqui a voz estava grande”. "
            "Na terceira linha, o desenho muda de tamanho, e a voz muda com ele. É um musicograma: uma música desenhada. Os músicos escrevem a mesma ideia com "
            "<i>f</i> (<i>forte</i>) e <i>p</i> (<i>piano</i>); você vai ver essas letras em qualquer partitura.", estilo="top:236mm;bottom:auto")}"""
    L.add(c, aba="--d-musica")

    cartoes(L, "Contrastes", [
        dict(pt="devagar", mot="tartaruga", en="slow", fr="lent", la="lentus", dica="Ande como a tartaruga. Os músicos dizem <i>lento</i>."),
        dict(pt="depressa", mot="ratinho", en="fast", fr="vite", la="celer", dica="Ande como o ratinho. Os músicos dizem <i>allegro</i> ou <i>presto</i>."),
        dict(pt="forte", mot="tambor", en="loud", fr="fort", la="fortis", dica="Batidas grandes no tambor. Os músicos dizem <i>forte</i> (do latim <i>fortis</i>)."),
        dict(pt="fraco", mot="pena", en="soft", fr="doux", la="lēnis", dica="Bata como uma pena cai. Os músicos dizem <i>piano</i>."),
        dict(pt="agudo", mot="cuco", en="high", fr="aigu", la="acūtus", dica="Som fino, de cima: o passarinho. Faça com a voz bem alta."),
        dict(pt="grave", html=img("elefante", "40mm"), en="low", fr="grave", la="gravis", dica="Som pesado, de baixo: o elefante. Faça com a voz bem baixa."),
        dict(pt="longo", mot="violino", en="long", fr="long", la="longus", dica="Um som que não acaba logo, como o arco no violino."),
        dict(pt="curto", html=img("gota", "30mm"), en="short", fr="court", la="brevis", dica="Um som que acaba já, como um pingo."),
        dict(pt="silêncio", mot="lua", en="silence", fr="le silence", la="silentium", dica="Nada soa. Quieta, quieta, e a mão parada no ar.")],
        "Volume 4 · Contrastes")

    itens_grave = [(img("elefante", "22mm"), "elefante"), (img("leao", "22mm"), "leão"), (img("m_trovao", "24mm"), "trovão"),
                   (img("timpano", "22mm"), "tímpano"), (img("violoncelo", "22mm"), "violoncelo")]
    itens_agudo = [(img("cuco", "22mm"), "cuco"), (img("ratinho", "22mm"), "ratinho"), (img("flauta", "24mm"), "flauta"),
                   (img("triangulo_inst", "22mm"), "triângulo"), (img("gato", "20mm"), "gatinho")]
    c = f"""<div class="miolo">{titulo("Pesado e leve", "sons de baixo e sons de cima", 28)}</div>
    {colunas(["grave (som de baixo)", "agudo (som de cima)"], 46, 98)}
    {recortes(itens_grave + itens_agudo, 160, 32, 34)}
    <div class="centro peq" style="position:absolute;left:0;right:0;top:238mm">recortar os dez cartões e pôr cada um na coluna certa</div>
    {adulto("classificar por altura",
            "Diga o som de cada bicho ou instrumento com a voz (o elefante é <i>buum</i>, o ratinho é <i>pip</i>) e ela decide em qual coluna fica. Não há resposta única para o gato "
            "e o violoncelo: pergunte “por quê?”. <b>Com objetos:</b> bata em uma panela grande e em uma tampinha; qual é mais grave? <b>Criar:</b> ela inventa um bicho, e você diz em qual coluna ele fica.",
            estilo="top:246mm;bottom:auto;font-size:8.6pt")}"""
    L.add(c, aba="--d-musica")

    passos(L, "A dança dos contrastes", "o corpo conta o que o ouvido escuta",
           [(img("tartaruga", "26mm"), "Devagar: passos enormes, em câmera lenta"),
            (img("ratinho", "24mm"), "Depressa: passinhos miúdos e rápidos"),
            (img("elefante", "26mm"), "Forte e grave: pisadas pesadas, tambor"),
            (img("pena", "24mm"), "Fraco e leve: na ponta dos pés, sem barulho"),
            (img("cuco", "26mm"), "Agudo: braços para cima, voz fininha"),
            (img("lua", "22mm"), "Silêncio: estátua, sem respirar fundo")],
           adulto("dançar o que se ouve",
                  "Tocando o tambor (ou batendo palmas), mude uma coisa de cada vez: primeiro a <b>velocidade</b> (devagar, depressa), depois a <b>força</b> (forte, fraco), e só depois os dois juntos "
                  "(forte e devagar, fraco e depressa). Ela comanda também. Com Saint-Saëns, escute <i>O elefante</i> e <i>Tartarugas</i> e peça que ela dance: o corpo reconhece o andamento "
                  "e o peso antes de qualquer nome."),
           aba="--d-musica")


# ================================================================== U4 OS INSTRUMENTOS

def unidade4(L):
    inicio_unidade(L, 3)
    guia(L, dict(
        titulo="Unidade 4 · Os instrumentos", aba="--d-jogos",
        pergunta="Quem está tocando? — a orquestra em quatro famílias: cordas, madeiras, metais e percussão.",
        duracao="Três fins de semana · três encontros · 15 a 20 minutos. É a unidade mais longa do volume.",
        objetivos=["Reconhecer, na imagem e no som, instrumentos de cada família.", "Ligar um personagem a um instrumento (<i>Pedro e o Lobo</i>).",
                   "Tocar instrumentos simples da caixa de música.", "Descobrir que materiais diferentes fazem sons diferentes.",
                   "Reconhecer a escala de dó e os nomes das notas: <i>dó ré mi fá sol lá si</i>."],
        repertorio="<b>Gravuras:</b> <i>Old King Cole</i> e <i>I saw three ships</i> (Walter Crane, <i>The Baby's Opera</i>, 1877). <b>Contos:</b> <i>Os Músicos de Bremen</i> (irmãos Grimm). "
                   "<b>Escuta:</b> <i>Pedro e o Lobo</i> (Prokofiev, 1936). <b>Línguas:</b> <i>drum · le tambour · tympanum</i>; <i>horn · le cor · cornū</i>; <i>trumpet · la trompette · tuba</i>.",
        materiais="Os cartões de instrumentos; as cartas de <i>Pedro e o Lobo</i>; objetos da casa para a orquestra (panela, colher, copos, pote com arroz).",
        vida="Montar uma orquestra com objetos da cozinha e tocar junto com uma música gravada.",
        etapas=[["Olhar os instrumentos nos cartões.", "Escutar <i>Pedro e o Lobo</i>.", "Brincar com a caixa de música."],
                ["Parear instrumento e personagem.", "Jogo da memória.", "Dividir em quatro famílias."],
                ["Montar a orquestra da casa.", "Inventar uma história com instrumentos.", "Tocar a escala no xilofone."]],
        indicadores=["Nomeia dois ou três instrumentos.", "Aponta o instrumento certo quando ouve a flauta ou a trompa.", "Liga o lobo às trompas.",
                     "Toca o chocalho no pulso.", "Joga a memória sem ajuda.", "Pede <i>Pedro e o Lobo</i> de novo."],
        interesse="visitar um concerto ou ensaio de uma orquestra jovem, ou ver uma gravação de <i>Pedro e o Lobo</i> com narrador.",
        dificil="só ouvir <i>Pedro e o Lobo</i> e apontar o pássaro (flauta) e o lobo (trompas)."))

    quatro = [("Cordas", "violino", "soam quando se raspa ou belisca uma corda", "violino, violoncelo, harpa, piano"),
              ("Madeiras", "flauta", "soam quando se sopra, e o ar vibra no tubo", "flauta, oboé, clarinete, fagote"),
              ("Metais", "trompete", "soam quando os lábios vibram no bocal", "trompete, trompa, trombone, tuba"),
              ("Percussão", "tambor", "soam quando se bate, sacode ou raspa", "tambor, pandeiro, triângulo, xilofone")]
    cel = "".join(f'<div class="centro caixa" style="padding:3mm 2mm"><div style="font-size:15pt;font-weight:600;color:var(--d-musica)">{n}</div>'
                  f'{img(m, "30mm", "margin:1mm auto")}<div style="font-size:10.5pt;line-height:1.3;font-style:italic">{como}</div>'
                  f'<div class="peq" style="margin-top:1.5mm">{ex}</div></div>' for n, m, como, ex in quatro)
    c = f"""<div class="miolo">{titulo("As quatro famílias", "uma orquestra tem muitos instrumentos, mas só quatro jeitos de soar", 26)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:5mm">{cel}</div>
      <div class="centro" style="margin-top:6mm">{pd("opera_navios", "52mm", "display:inline-block;margin:0 4mm")}{pd("opera_rei_cole", "52mm", "display:inline-block;margin:0 4mm")}</div></div>
      {adulto("as famílias",
              "<b>Cordas:</b> o violino, a viola, o violoncelo e o contrabaixo, tocados com arco; a harpa e o violão, beliscados; o piano, de cordas batidas por martelinhos. "
              "<b>Madeiras:</b> flautas e palhetas (oboé, clarinete, fagote). <b>Metais:</b> trompetes, trompas, trombones, tubas. <b>Percussão:</b> tudo o que se bate ou sacode. "
              "Nas gravuras de Walter Crane, uma mulher toca violino sobre um barco (<i>I saw three ships</i>) e três violinistas tocam para o rei (<i>Old King Cole</i>).",
              credito_pd("opera_navios", "opera_rei_cole"))}"""
    L.add(c, aba="--d-jogos")

    cartoes(L, "Instrumentos", [
        dict(pt="violino", mot="violino", en="violin", fr="le violon", som="agudo, que canta", dica="Escute <i>A Primavera</i>, de Vivaldi: os violinos fazem os pássaros."),
        dict(pt="violoncelo", mot="violoncelo", en="cello", fr="le violoncelle", som="grave, como uma voz", dica="Escute <i>O Cisne</i>, de Saint-Saëns: o violoncelo é o cisne."),
        dict(pt="harpa", mot="harpa", en="harp", fr="la harpe", som="gotas de notas", dica="As cordas são tocadas com os dedos, uma a uma."),
        dict(pt="piano", mot="piano", en="piano", fr="le piano", som="de grave a agudo", dica="Escute <i>Clair de lune</i>, de Debussy: só o piano, bem baixinho."),
        dict(pt="flauta", mot="flauta", en="flute", fr="la flûte", som="agudo, como um pássaro", dica="No <i>Pedro e o Lobo</i>, a flauta é o passarinho."),
        dict(pt="clarinete", mot="clarinete", en="clarinet", fr="la clarinette", som="macio e escuro", dica="No <i>Pedro e o Lobo</i>, o clarinete é o gato; em Saint-Saëns, o cuco."),
        dict(pt="trompete", mot="trompete", en="trumpet", fr="la trompette", la="tuba", som="brilhante e forte", dica="O trompete avisa: “atenção, vai começar!”"),
        dict(pt="trompa", mot="trompa", en="horn", fr="le cor", la="cornū", som="redondo e grave", dica="No <i>Pedro e o Lobo</i>, o lobo são três trompas juntas."),
        dict(pt="pandeiro", mot="pandeiro", en="tambourine", fr="le tambourin", la="tympanum", som="chacoalhado e batido", dica="Toque com a palma, com os dedos e sacudindo. Quantos sons diferentes?")],
        "Volume 4 · Instrumentos")

    historia(L, "Rei Cole e seus músicos", "cantiga inglesa · tradução e adaptação da coleção", f"""
      <div class="centro" style="margin:2mm 0 3mm">{pd("opera_rei_cole", "76mm", "display:inline-block;margin:0 3mm")}{pd("opera_rei_cole_pauta", "76mm", "display:inline-block;margin:0 3mm")}</div>
      <p style="font-size:14.5pt;line-height:1.55;text-align:center;font-style:italic">O velho Rei Cole era um rei muito alegre.<br>
      Mandou buscar a taça, mandou buscar os músicos:<br>três violinistas, e cada um tinha um violino,<br>e que lindo violino tinha cada um!<br>
      Tchim-tchim, tchim-tchim, tchim-tchim fizeram os violinos.<br>Não há músicos como os do velho Rei Cole.</p>""",
             adulto("três violinos",
                    "Na gravura de Walter Crane, os três violinistas tocam ao mesmo tempo; um deles se inclina, outro fecha os olhos. Mostre que os três instrumentos são do mesmo tipo e "
                    "soam juntos. Cante a cantiga em ritmo de marcha. A letra tradicional fala também de cachimbo; na adaptação, ficaram só a taça e os músicos. A partitura original, em inglês, está à direita.",
                    credito_pd("opera_rei_cole", "opera_rei_cole_pauta")), aba="--d-jogos")

    cantores = [("burro", "o burro", "grave e comprido: iô, iô", "1.º"), ("cachorro", "o cachorro", "forte e redondo: au, au", "2.º"),
                ("gato", "o gato", "fino e curto: miau", "3.º"), ("galo", "o galo", "agudo e longo: cocoricó", "4.º")]
    cel = "".join(f'<div class="centro">{pd("cartao_galo", "21mm", "margin:0 auto") if m == "galo" else img(m, "30mm", "margin:0 auto")}<div style="font-size:13pt;font-weight:600">{n}</div>'
                  f'<div class="legenda-q">{som}</div><div class="peq">{pos} a cantar</div></div>' for m, n, som, pos in cantores)
    c = f"""<div class="miolo">{titulo("Os músicos de Bremen", "quatro vozes, do grave ao agudo", 28)}
      <p style="font-size:14pt;line-height:1.5;margin:3mm 0 4mm;text-align:center">O burro, o cachorro, o gato e o galo, cada um velho e cansado, foram juntos a Bremen para serem músicos.
      Na estrada, à noite, viram uma casa de ladrões. Subiram uns nos outros, o burro embaixo e o galo em cima, e cantaram todos de uma vez:</p>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:2mm">{cel}</div>
      <div class="centro" style="margin-top:5mm">{pd("rackham_bremen", "50mm", "display:inline-block;margin:0 4mm")}</div></div>
      {adulto("ordenar do grave ao agudo",
              "O conto dos Músicos de Bremen está inteiro no Volume 2. Aqui interessa a cantoria: a voz do burro é a mais grave, a do galo a mais aguda; o cachorro e o gato ficam no meio. "
              "Cante com ela as quatro vozes em ordem (do mais grave ao mais agudo) e depois em ordem trocada. Com a pirâmide dos quatro bichos, o conto mostra, por si, a "
              "ideia da <b>escala</b>: sons ordenados de baixo para cima. A ilustração é de Arthur Rackham; o burro, o cachorro e o gato são da coleção.",
              credito_pd("rackham_bremen", "cartao_galo"))}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo historia">{titulo("Pedro e o Lobo", "um conto musical de Sergei Prokofiev (1936)", 28)}
      <p style="font-size:14.5pt;line-height:1.5">Pedro mora numa casa com um jardim e um lago, e o avô, que fica preocupado, avisa: “O lobo pode aparecer!”
      Um passarinho canta no galho, um pato nada no lago, o gato se esgueira pelo jardim. O lobo chega, e Pedro, com os caçadores, prende o lobo numa corda
      e o leva para o zoológico. Em Prokofiev, <b>cada personagem é um instrumento</b>, com a sua própria melodia.</p>
      <table class="tab" style="margin-top:3mm;font-size:12pt">
        <tr><td style="width:24mm">{img("gorro", "17mm", "margin:0 auto")}</td><td><b>Pedro</b></td><td>os instrumentos de corda: violinos, violas, violoncelos</td><td style="width:22mm">{img("violino", "17mm", "margin:0 auto")}</td></tr>
        <tr><td>{img("cuco", "17mm", "margin:0 auto")}</td><td><b>O passarinho</b></td><td>a flauta</td><td>{img("flauta", "20mm", "margin:0 auto")}</td></tr>
        <tr><td>{img("patinho", "17mm", "margin:0 auto")}</td><td><b>O pato</b></td><td>o oboé</td><td>{img("oboe", "20mm", "margin:0 auto")}</td></tr>
        <tr><td>{img("gato", "17mm", "margin:0 auto")}</td><td><b>O gato</b></td><td>o clarinete</td><td>{img("clarinete", "20mm", "margin:0 auto")}</td></tr>
        <tr><td style="font-size:20pt;text-align:center">♪</td><td><b>O avô</b></td><td>o fagote (um instrumento de madeira, grave e rouco)</td><td></td></tr>
        <tr><td>{img("lobo", "17mm", "margin:0 auto")}</td><td><b>O lobo</b></td><td>três trompas</td><td>{img("trompa", "20mm", "margin:0 auto")}</td></tr>
        <tr><td>{img("chapeu", "17mm", "margin:0 auto")}</td><td><b>Os caçadores</b></td><td>os tímpanos e o bumbo (os tiros)</td><td>{img("timpano", "20mm", "margin:0 auto")}</td></tr></table></div>
      {adulto("uma obra, muitas vezes",
              "<b>Esta é a obra da unidade.</b> Toque-a na semana toda, aos poucos: primeiro só o passarinho (flauta) e o lobo (trompas), depois os outros. Há gravações com narrador em português; "
              "escolha uma de que goste. Escute com ela olhando as figuras: “quem é este?”. Depois jogue a memória da página seguinte. A obra foi escrita em 1936, para um teatro de crianças em Moscou. "
              "Prokofiev (1891–1953) morreu há mais de 70 anos; as gravações, porém, têm direitos próprios.")}"""
    L.add(c, aba="--d-jogos")

    itens = [("pássaro", img("cuco", "26mm")), ("flauta", img("flauta", "36mm")), ("pato", img("patinho", "26mm")), ("oboé", img("oboe", "36mm")),
             ("gato", img("gato", "26mm")), ("clarinete", img("clarinete", "36mm")), ("lobo", img("lobo", "26mm")), ("trompa", img("trompa", "30mm")),
             ("Pedro", img("gorro", "26mm")), ("violino", img("violino", "28mm")), ("caçadores", img("chapeu", "26mm")), ("tímpano", img("timpano", "30mm"))]
    memoria(L, "Pedro e o Lobo", itens, [4, 9, 0, 7, 10, 2, 11, 5, 1, 8, 3, 6],
            adulto("personagem e instrumento",
                   "Aqui os pares não são iguais: cada <b>personagem</b> casa com o seu <b>instrumento</b> (o pássaro com a flauta, o lobo com a trompa…). Comece com as cartas viradas para cima, "
                   "procurando os pares; depois, se ela quiser, virada para baixo. Toque a música enquanto joga: ela ouve a flauta e procura o pássaro.",
                   estilo="bottom:19mm;top:auto"), verso_motivo="seminima")

    c = f"""<div class="miolo">{titulo("A escada dos sons", "o xilofone e a escala de dó", 28)}
      <div class="centro" style="margin:3mm 0">{img("xilofone", "62mm", "margin:0 auto")}</div>
      {pauta([("C4", "q"), ("D4", "q"), ("E4", "q"), ("F4", "q"), ("G4", "q"), ("A4", "q"), ("B4", "q"), ("C5", "q")], 170, 2.9, letra=["dó", "ré", "mi", "fá", "sol", "lá", "si", "dó"])}
      <div class="centro peq" style="margin-top:2mm">a escala de dó: oito notas, de baixo para cima</div>
      <h2 class="titulo" style="font-size:14pt;margin:5mm 0 1mm;text-align:left">De onde vêm os nomes</h2>
      <p style="font-size:11pt;line-height:1.4">Há quase mil anos, um monge chamado <b>Guido de Arezzo</b> usou o hino a São João para ensinar a cantar. Cada verso começa uma nota acima do anterior,
      e a primeira sílaba de cada verso virou o nome da nota: <i><b>Ut</b> queant laxis, <b>Re</b>sonare fibris, <b>Mi</b>ra gestorum, <b>Fa</b>muli tuorum, <b>Sol</b>ve polluti, <b>La</b>bii reatum</i>.
      Mais tarde, o <i>ut</i> virou <i>dó</i>, que é mais fácil de cantar.</p></div>
      {adulto("escala e xilofone",
              "Se você tem um xilofone de brinquedo (ou copos com níveis diferentes de água), toque as oito barras de baixo para cima e de cima para baixo, cantando os nomes. "
              "A palavra <b>escala</b> vem de <i>scala</i>, a escada: é como subir degraus de som. Ela não precisa saber os nomes; basta perceber que sobe e desce. "
              "<b>Criar:</b> ela inventa uma musiquinha tocando três barras à vontade.")}"""
    L.add(c, aba="--d-jogos")

    passos(L, "A orquestra da casa", "tudo o que faz barulho vira instrumento",
           [(img("tigela", "22mm") + img("colher", "16mm"), "Panela virada e colher de pau: o tambor"),
            (img("prato", "22mm"), "Duas tampas de panela: os pratos (adulto segura)"),
            (img("chocalho", "24mm"), "Pote com arroz bem fechado: o chocalho"),
            (img("xicara", "18mm") + img("xicara", "18mm") + img("xicara", "18mm"), "Copos com mais ou menos água: sons graves e agudos"),
            (img("palma", "22mm"), "Palmas e pés: a percussão do corpo"),
            (img("cuco", "22mm"), "A voz: o instrumento mais antigo de todos")],
           adulto("fazer música com o que se tem",
                  "Reúna os objetos e toque junto com uma música gravada que ela conhece (a de <i>Pedro e o Lobo</i> serve). Cada um escolhe um instrumento; vocês tocam fraco quando a música "
                  "fica fraca, forte quando fica forte. Para os copos, bata de leve com uma colher de metal: quanto mais água, mais grave o som. "
                  "<b>Segurança:</b> volume baixo, sem objetos pontiagudos e com o adulto sempre perto."),
           aba="--d-vida")


# ================================================================== U5 VIVALDI

def unidade5(L):
    inicio_unidade(L, 4)
    guia(L, dict(
        titulo="Unidade 5 · Vivaldi", aba="--d-natureza",
        pergunta="A música pode contar o que a gente vê? — as estações do ano em quatro concertos de violino.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos. Uma obra só: <i>A Primavera</i>.",
        objetivos=["Ouvir <i>A Primavera</i>, de Vivaldi, várias vezes até reconhecê-la.", "Reconhecer quando a música é o tema, os pássaros, o riacho e o trovão.",
                   "Mover o corpo de acordo com cada parte.", "Ligar as quatro estações às quatro árvores.", "Contar com desenho o que a música mostrou."],
        repertorio="<b>Obra:</b> Antonio Vivaldi (1678–1741), <i>As Quatro Estações</i> (publicadas em 1725), concerto n.º 1, <i>A Primavera</i>, primeiro movimento (<i>allegro</i>), para violino solista, orquestra de cordas e cravo. "
                   "<b>Línguas:</b> <i>spring · le printemps · vēr</i>; <i>storm · l'orage · tempestās</i>.",
        materiais="Uma gravação de <i>A Primavera</i> (o primeiro movimento dura cerca de 3 minutos); lenços coloridos; papel e giz de cera.",
        vida="Ouvir a obra ao acordar e ao fim do dia; passear e achar sinais da estação (pássaros, riachos, nuvens).",
        etapas=[["Ouvir a obra inteira, sentadas.", "Aprender o tema (a primavera chegou).", "Achar pássaros e trovão."],
                ["Mover o corpo em cada parte.", "Seguir o musicograma com o dedo.", "As quatro árvores."],
                ["Inventar uma sexta parte.", "Desenhar o que a música mostrou.", "Escolher um instrumento para cada parte."]],
        indicadores=["Reconhece o tema quando volta.", "Faz “pi-pi” com os dedos nos pássaros.", "Se encolhe ou bate palmas no trovão.",
                     "Segue o musicograma com o dedo.", "Pede <i>A Primavera</i> de novo.", "Diz o nome da estação ao ver a árvore."],
        interesse="escutar, nas semanas seguintes, <i>O Verão</i>, <i>O Outono</i> e <i>O Inverno</i>, um por vez, na estação que combina.",
        dificil="só ouvir a obra deitadas, olhando o musicograma."))

    c = f"""<div class="miolo">{titulo("Vivaldi e a cidade dos barcos", "Veneza, 1678 · um padre ruivo que tocava violino", 25)}
      <div class="centro" style="margin:3mm 0">{pd("opera_navios", "74mm", "margin:0 auto")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Antonio Vivaldi nasceu em Veneza, uma cidade de canais e barcos. O pai era violinista e ensinou o filho a tocar.
      Vivaldi virou padre, e o cabelo ruivo lhe deu o apelido de <i>il Prete Rosso</i>, o padre ruivo. Passou boa parte da vida ensinando música a meninas num orfanato da cidade, o Ospedale della Pietà,
      onde escrevia concertos para elas tocarem. Hoje, mais de 300 anos depois, <i>As Quatro Estações</i> estão entre as músicas mais ouvidas do mundo.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Cada estação é um <b>concerto</b>: um violino que “conversa” com uma orquestra de cordas. Vivaldi escreveu um soneto para cada concerto, dizendo o que a música mostra; por exemplo,
      na <i>Primavera</i> há pássaros que cantam, um riacho que corre, e um trovão que interrompe tudo antes de a primavera voltar.</p></div>
      {adulto("uma obra, muitas vezes",
              "<b>Esta é a obra da unidade.</b> O primeiro movimento de <i>A Primavera</i> dura cerca de 3 minutos, uma boa medida para esta idade. Toque-a na semana toda. "
              "Ela vai reconhecer primeiro o tema (que volta quatro vezes), depois os pássaros, depois o trovão. Mostre o violino dos cartões (Unidade 4), os violinos da gravura de Walter Crane "
              "(uma mulher toca violino num barco) e, se puder, o violino de verdade de algum conhecido.", credito_pd("opera_navios"))}"""
    L.add(c, aba="--d-natureza")

    c = f"""<div class="miolo">{titulo("A Primavera", "musicograma do primeiro movimento · acompanhar com o dedo", 28)}
      <div style="margin-top:5mm">{musicograma([("tema", ROXO, "onda", 3), ("pássaros", "#5f8f8a", "pontos", 2), ("tema", ROXO, "onda", 2), ("riacho", "#5f7f9c", "calma", 2),
                                                  ("tema", ROXO, "onda", 2), ("trovão", "#b8503a", "bloco", 1), ("tema", ROXO, "onda", 2), ("pássaros", "#5f8f8a", "pontos", 2)], 174, 46)}</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:5mm;text-align:center;font-size:11pt">
        <div>{img("m_tema", "26mm", "margin:0 auto")}<b>o tema</b><br>a primavera chegou, alegre</div>
        <div>{img("m_passaros", "26mm", "margin:0 auto")}<b>os pássaros</b><br>trinados dos violinos</div>
        <div>{img("m_riacho", "26mm", "margin:0 auto")}<b>o riacho</b><br>cordas suaves, ondulando</div>
        <div>{img("m_trovao", "26mm", "margin:0 auto")}<b>o trovão</b><br>notas rápidas e fortes</div></div>
      <div class="caixa" style="margin-top:6mm;font-size:12.5pt;line-height:1.55;font-style:italic;text-align:center">
        Chegou a primavera, e os pássaros a saúdam com canto alegre;<br>os riachos correm, murmurando, ao sopro do vento;<br>
        vêm o trovão e o relâmpago, e cobrem o céu de escuro;<br>passada a tempestade, os pássaros voltam ao seu canto.
        <div class="peq" style="font-style:normal;margin-top:2mm">O que o soneto de Vivaldi conta, em palavras da coleção.</div></div></div>
      {adulto("ler o musicograma",
              "Este é um <b>musicograma</b>: a música desenhada. Ponha a gravação e vá com o dedo da esquerda para a direita, parando em cada parte. A ordem é a do primeiro movimento: "
              "o tema (alegre, que volta várias vezes), os pássaros (violinos agudos e rápidos, em trinados), o riacho (cordas suaves), a trovoada (notas rápidas e fortes), e a volta do tema e dos pássaros. "
              "As proporções são aproximadas: o desenho serve para acompanhar, não para medir. Vivaldi escreveu um soneto que descreve essas partes; as figuras vêm da coleção.")}"""
    L.add(c, aba="--d-natureza")

    passos(L, "Mover a Primavera", "o corpo acompanha cada parte",
           [(img("m_tema", "24mm"), "Tema: marchar e bater palmas leves"),
            (img("m_passaros", "24mm"), "Pássaros: dedinhos voando, “piu, piu”"),
            (img("m_riacho", "24mm"), "Riacho: braços em onda, devagar"),
            (img("m_trovao", "24mm"), "Trovão: tambor nas pernas, forte!"),
            (img("m_tema", "24mm"), "Tema de novo: palmas leves"),
            (img("m_passaros", "24mm"), "Os pássaros voltam: dedinhos voando")],
           adulto("movimento e escuta",
                  "Dalcroze dizia: o corpo escuta antes da cabeça. Faça os gestos com ela, em silêncio, antes de pôr a música, e depois com a música. Não é uma coreografia: "
                  "ela pode inventar outros gestos. O trovão é a parte de que muitas crianças mais gostam; avise antes para que ela não se assuste. "
                  "<b>Criar:</b> ela escolhe a ordem dos gestos, e você toca o tambor."),
           aba="--d-natureza")

    est = [("arvore_primavera", "Primavera", "flores, pássaros, riachos"), ("arvore_verao", "Verão", "calor, cuco, tempestade"),
           ("arvore_outono", "Outono", "colheita, festa, dança"), ("arvore_inverno", "Inverno", "frio, tremer, a lareira")]
    cel = "".join(f'<div class="centro caixa">{img(m, "38mm", "margin:0 auto")}<div style="font-size:15pt;font-weight:600">{n}</div><div class="legenda-q">{t}</div></div>' for m, n, t in est)
    c = f"""<div class="miolo">{titulo("Quatro árvores, quatro estações", "Vivaldi escreveu quatro concertos, um para cada", 25)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">{cel}</div></div>
      {adulto("as outras estações",
              "Cada concerto de Vivaldi tem três movimentos. Para esta idade basta escutar o <b>primeiro</b> de cada um, no tempo certo do ano: <i>O Verão</i> mostra o calor e uma tempestade "
              "forte; <i>O Outono</i>, a festa da colheita; <i>O Inverno</i>, o frio, os dentes batendo e os passos no gelo, antes de se aquecer ao fogo. Escolha, a cada dois fins de semana, uma estação. "
              "No Brasil as estações são menos marcadas que na Europa, mas as quatro árvores servem para conversar sobre o que muda ao longo do ano.")}"""
    L.add(c, aba="--d-natureza")

    c = f"""<div class="miolo">{titulo("O que a música me mostrou", "desenhar depois de escutar", 28)}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">
        <div class="caixa" style="height:70mm"><div class="peq centro">o tema</div></div><div class="caixa" style="height:70mm"><div class="peq centro">os pássaros</div></div>
        <div class="caixa" style="height:70mm"><div class="peq centro">o riacho</div></div><div class="caixa" style="height:70mm"><div class="peq centro">o trovão</div></div></div></div>
      {adulto("escutar e desenhar",
              "Escute <i>A Primavera</i> mais uma vez e, com giz de cera, deixe que ela desenhe o que quiser em cada quadro. Não pergunte “o que é isto?”; peça que conte. "
              "Escreva ao lado, com a letra dela ou a sua, o que ela disser, e a data. Guarde: é um registro do que ela ouviu naquela semana.")}"""
    L.add(c, aba="--d-artes")


# ================================================================== U6 BACH

def unidade6(L):
    inicio_unidade(L, 5)
    guia(L, dict(
        titulo="Unidade 6 · Bach", aba="--d-matematica",
        pergunta="Como uma melodia sobe e desce? — a escada de notas e a onda que não para.",
        duracao="Dois fins de semana · dois encontros · 15 minutos.",
        objetivos=["Escutar o <i>Prelúdio em dó maior</i> várias vezes até reconhecê-lo.", "Perceber que as notas sobem e descem.", "Seguir com a mão uma linha que sobe e desce.",
                   "Tocar cinco notas (dó ré mi fá sol) com os cinco dedos.", "Ligar música e matemática: o padrão que se repete."],
        repertorio="<b>Obra:</b> Johann Sebastian Bach (1685–1750), <i>Prelúdio em dó maior</i>, do primeiro livro de <i>O Cravo Bem Temperado</i> (BWV 846, 1722), para teclado. "
                   "<b>Línguas:</b> <i>wave · l'onde · unda</i>; <i>to climb · monter · ascendere</i>.",
        materiais="Uma gravação do <i>Prelúdio em dó maior</i> (cerca de 2 minutos e meio); um piano ou teclado, se houver; lápis grosso.",
        vida="Subir e descer a escada de casa cantando uma nota a cada degrau.",
        etapas=[["Escutar com o dedo no ar.", "Acompanhar a onda de notas.", "Subir e descer a escada."],
                ["Traçar a escada.", "Cinco dedos, cinco notas.", "Comparar com Vivaldi."],
                ["Inventar uma onda nova.", "Tocar no teclado, se houver.", "Cantar subindo e descendo."]],
        indicadores=["Mostra com a mão quando a música sobe.", "Acompanha a onda sem se distrair.", "Canta uma escala curta.",
                     "Segue a linha com o dedo e a voz.", "Toca cinco notas, uma por dedo.", "Pede de novo o <i>Prelúdio</i>."],
        interesse="ouvir uma das <i>Suítes para violoncelo solo</i> de Bach: um único instrumento, uma voz só.",
        dificil="só ouvir o <i>Prelúdio</i>, com o dedo seguindo a onda no ar."))

    c = f"""<div class="miolo">{titulo("Bach e a casa cheia de música", "Eisenach, 1685 · uma casa cheia de filhos e de música", 25)}
      <div class="centro" style="margin:3mm 0">{pd("opera_pastor", "78mm", "margin:0 auto")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Johann Sebastian Bach nasceu numa família de músicos. Quando criança, aprendeu violino e canto e, mais tarde, tornou-se um dos maiores organistas da sua época.
      Casou-se duas vezes e teve vinte filhos; vários viraram músicos. Escreveu muita música para a igreja e também para a casa: um caderno de pequenas peças para a segunda mulher, Anna Magdalena,
      e os filhos aprenderem a tocar cravo.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Em 1722 escreveu o primeiro livro de <i>O Cravo Bem Temperado</i>, com um prelúdio e uma fuga em cada tom.
      O primeiro prelúdio, em dó maior, é feito de uma <b>onda de notas</b>: quase toda a peça é um acorde desmanchado, nota por nota, sempre no mesmo desenho.</p></div>
      {adulto("uma obra, muitas vezes",
              "<b>Esta é a obra da unidade.</b> O <i>Prelúdio em dó maior</i> tem cerca de 2 minutos e meio. É boa para a hora do almoço ou do banho: não tem sobressaltos. "
              "Muita gente a acha calma, como água corrente. A gravura é de Walter Crane (<i>Over the hills and far away</i>): um menino toca flauta, como as crianças de toda a época de Bach.",
              credito_pd("opera_pastor"))}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("O Prelúdio: uma onda de notas", "o mesmo desenho, de novo e de novo", 26)}
      <div style="margin-top:4mm">{musicograma([("onda", "#5f7f9c", "onda", 3), ("onda", "#5f7f9c", "onda", 3), ("muda de lugar", "#8a6f9e", "onda", 3), ("onda", "#5f7f9c", "onda", 3),
                                                  ("mais agitada", "#c0716b", "zigue", 2), ("volta a calma", "#5f7f9c", "calma", 3)], 174, 42)}</div>
      <h2 class="titulo" style="font-size:14pt;margin:5mm 0 1mm;text-align:left">O desenho de uma onda <span class="peq it" style="font-weight:400">— simplificado a partir do início, para o adulto</span></h2>
      {pauta([("C4", "e"), ("E4", "e"), ("G4", "e"), ("C5", "e"), ("E5", "e"), ("C5", "e"), ("G4", "e"), ("E4", "e")], 170, 2.9, rotulos=["dó", "mi", "sol", "dó", "mi", "dó", "sol", "mi"])}
      <div class="centro peq" style="margin-top:2mm">sobe cinco notas (dó, mi, sol, dó, mi) e desce de volta; no <i>Prelúdio</i> de verdade, esse desenho se repete em cada compasso, sobre outro acorde</div></div>
      {adulto("o padrão",
              "Bach faz com som o que a matemática faz com número: um <b>padrão</b> que se repete e muda de lugar. Sem explicar, mostre com a mão uma onda no ar (sobe, sobe, desce, desce) enquanto a música toca. "
              "A pauta mostra o começo simplificado: cinco notas subindo e três descendo; o original é mais rápido e tem a nota grave do baixo, mas a ideia é a mesma. "
              "As notas são do acorde de dó maior (dó, mi, sol), que se encontram na escada do xilofone (página 40).")}"""
    L.add(c, aba="--d-matematica")

    svg = (pontilhado("M30 152 L30 130 L52 130 L52 108 L74 108 L74 86 L96 86 L96 64 L118 64", w=2.8)
           + pontilhado("M118 64 L118 86 L140 86 L140 108 L162 108 L162 130 L184 130 L184 152", w=2.8)
           + ponto_inicio(30, 152)
           + pontilhado("M30 205 q20 -44 40 0 t40 0 t40 0 t40 0", w=2.8) + ponto_inicio(30, 205))
    c = f"""<div class="miolo">{titulo("Sobe e desce", "seguir as linhas com o dedo e a voz", 28)}</div>
    <div style="position:absolute;left:30mm;top:160mm" class="peq it">uma escada: sobe, sobe, sobe… e desce, desce, desce</div>
    <div style="position:absolute;left:30mm;top:176mm" class="peq it">uma onda: sobe e desce sem parar</div>
    <svg class="svgpag" viewBox="0 0 210 297">{svg}</svg>
    {adulto("traçar a escada",
            "O dedo e a voz sobem juntos nos degraus (voz cada vez mais aguda) e descem juntos (voz cada vez mais grave). Na onda, a voz “passeia”. Depois com lápis grosso, devagar. "
            "Esta página prepara a mão para o traçado de letras e ensina que <b>subir e descer</b> existem também no som. Se houver uma escada em casa, cante uma nota em cada degrau: o som sobe com o corpo.",
            estilo="top:248mm;bottom:auto")}"""
    L.add(c, aba="--d-matematica")

    c = f"""<div class="miolo">{titulo("Cinco dedos, cinco notas", "dó, ré, mi, fá, sol", 28)}
      <div class="centro" style="margin:3mm 0;line-height:0">{img("palma", "44mm", "display:inline-block")}</div>
      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2mm;text-align:center;font-size:12pt;margin-bottom:3mm">
        <div><b>polegar</b><br>dedo 1 · dó</div><div><b>indicador</b><br>dedo 2 · ré</div><div><b>médio</b><br>dedo 3 · mi</div><div><b>anelar</b><br>dedo 4 · fá</div><div><b>mindinho</b><br>dedo 5 · sol</div></div>
      <div class="peq centro" style="margin-bottom:1mm">subindo</div>
      {pauta([("C4", "q"), ("D4", "q"), ("E4", "q"), ("F4", "q"), ("G4", "q")], 170, 2.7, rotulos=["1", "2", "3", "4", "5"])}
      <div class="peq centro" style="margin:3mm 0 1mm">descendo</div>
      {pauta([("G4", "q"), ("F4", "q"), ("E4", "q"), ("D4", "q"), ("C4", "q")], 170, 2.7, rotulos=["5", "4", "3", "2", "1"])}</div>
      {adulto("posição de cinco dedos",
              "Num teclado ou piano, ponha o polegar da mão direita no dó que fica à esquerda de um grupo de duas teclas pretas (o <b>dó central</b> está perto do meio do teclado) e cada dedo numa tecla branca seguinte. "
              "Toque devagar, uma de cada vez, cantando os nomes. Sem teclado, a mão aberta sobre a mesa serve: cada dedo bate quando se canta a nota. "
              "É o primeiro passo dos cinco dedos de qualquer pianista, e tem a mesma escada da página anterior.")}"""
    L.add(c, aba="--d-matematica")

    passos(L, "Ondas no ar", "escutar com as mãos",
           [(img("palma", "22mm"), "Uma mão aberta, na altura do peito"),
            (img("m_riacho", "26mm"), "Quando a música sobe, a mão sobe"),
            (img("m_riacho", "26mm", "transform:scaleY(-1)"), "Quando a música desce, a mão desce"),
            (img("nuvem", "24mm"), "Com um lenço, a onda fica mais comprida"),
            (img("chave", "20mm"), "Depois, com os dois braços: uma onda grande"),
            (img("lua", "22mm"), "Fechamos os olhos e deixamos a onda passar")],
           adulto("seguir a música com o corpo",
                  "Ponha o <i>Prelúdio</i> baixinho e sente-se com ela. Mostre a onda com a mão e deixe que ela acompanhe. No começo ela imitará você; depois, o corpo dela vai achar o próprio jeito. "
                  "<b>Criar:</b> ela faz a onda e você a acompanha com a voz (“uuuiii!”). A mesma ideia vale para qualquer música sem palavras."),
           aba="--d-artes")


# ================================================================== U7 MOZART

def unidade7(L):
    inicio_unidade(L, 6)
    guia(L, dict(
        titulo="Unidade 7 · Mozart", aba="--d-historias",
        pergunta="Uma música pode usar roupas diferentes? — o mesmo tema, doze jeitos de dizer.",
        duracao="Dois fins de semana · dois encontros · 15 a 20 minutos.",
        objetivos=["Cantar e reconhecer o tema da <i>Estrelinha</i>.", "Perceber que o mesmo tema pode ser mais rápido, mais lento, forte, fraco.",
                   "Associar cores às notas e tocar a melodia num xilofone (ou copos) colorido.", "Fazer uma variação própria da melodia.", "Ouvir a obra inteira e reconhecer o tema."],
        repertorio="<b>Melodia:</b> <i>Brilha, brilha, estrelinha</i> (canção tradicional francesa, <i>Ah! vous dirai-je, Maman</i>). "
                   "<b>Obra:</b> Wolfgang Amadeus Mozart (1756–1791), <i>Doze variações sobre “Ah! vous dirai-je, Maman”</i> (K. 265), para piano. "
                   "<b>Línguas:</b> <i>star · l'étoile · stēlla</i>; <i>twinkle · scintiller · micāre</i>.",
        materiais="Um xilofone de brinquedo (ou copos de vidro com água, só com adulto) e fita colorida para marcar as notas; uma gravação das <i>Variações</i>.",
        vida="Cantar a estrelinha na hora de dormir e a cada passeio noturno.",
        etapas=[["Cantar a estrelinha.", "Escutar a obra de Mozart.", "Mostrar as cores das notas."],
                ["Tocar com as cores.", "Brincar com os doze jeitos.", "Comparar tema e variações."],
                ["Inventar uma variação (forte, fraca, rápida).", "Cantar com outras sílabas.", "Dançar o tema."]],
        indicadores=["Canta o tema inteiro ou quase.", "Reconhece o tema na obra de Mozart.", "Toca as cores na ordem.",
                     "Diz “agora devagar”, “agora forte”.", "Inventa uma variação.", "Pede para cantar de novo."],
        interesse="ouvir uma sonata de Mozart para piano (a <i>Sonata K. 545</i>) e procurar o tema que se repete.",
        dificil="só cantar a estrelinha, devagar e baixinho."))

    c = f"""<div class="miolo">{titulo("Wolfgang, o menino de Salzburgo", "1756 · quem compôs aos cinco anos", 25)}
      <div class="centro" style="margin:4mm 0;line-height:0">{img("piano", "50mm", "display:inline-block;margin:0 5mm")}{img("violino", "36mm", "display:inline-block;margin:0 5mm")}{img("seminima", "20mm", "display:inline-block;margin:0 5mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Wolfgang Amadeus Mozart nasceu em Salzburgo, na Áustria, em 1756. O pai, Leopold, era violinista e professor de música. A irmã mais velha, Maria Anna, a Nannerl, tocava cravo, e o pequeno Wolfgang,
      sentado ao lado, escutava as aulas dela. Aos três anos, já procurava no teclado as notas que ouvia; aos cinco, escreveu as primeiras peças. Com seis, tocava para nobres e para a imperatriz de Viena, de viagem pela Europa com a irmã e o pai.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Morreu cedo, aos 35 anos, mas escreveu mais de 600 obras: óperas, concertos, sinfonias, música de câmara. Entre elas,
      <i>doze variações</i> sobre uma canção popular francesa, que hoje cantamos como <i>Brilha, brilha, estrelinha</i>.</p></div>
      {adulto("o menino e a música",
              "Conte a história a ela como se fosse de uma criança que ela pode conhecer: “o Wolfgang gostava de escutar a irmã, e um dia começou a tocar as mesmas notas”. "
              "Não é preciso falar de gênio: o que importa é que <b>ele escutou muito, mexeu no teclado e brincou</b>. Mozart (1756–1791) morreu há mais de 200 anos; a melodia da canção é muito mais antiga que as variações.")}"""
    L.add(c, aba="--d-historias")

    frase1 = [("C4", "q"), ("C4", "q"), ("G4", "q"), ("G4", "q"), ("A4", "q"), ("A4", "q"), ("G4", "h"), "|", ("F4", "q"), ("F4", "q"), ("E4", "q"), ("E4", "q"), ("D4", "q"), ("D4", "q"), ("C4", "h")]
    frase2 = [("G4", "q"), ("G4", "q"), ("F4", "q"), ("F4", "q"), ("E4", "q"), ("E4", "q"), ("D4", "h"), "|", ("G4", "q"), ("G4", "q"), ("F4", "q"), ("F4", "q"), ("E4", "q"), ("E4", "q"), ("D4", "h")]
    nomes1 = ["dó", "dó", "sol", "sol", "lá", "lá", "sol", "fá", "fá", "mi", "mi", "ré", "ré", "dó"]
    nomes2 = ["sol", "sol", "fá", "fá", "mi", "mi", "ré", "sol", "sol", "fá", "fá", "mi", "mi", "ré"]
    c = f"""<div class="miolo">{titulo("Brilha, brilha, estrelinha", "uma melodia francesa que Mozart usou", 26)}
      <div style="margin-top:3mm">{pauta(frase1, 172, 2.6, rotulos=nomes1)}</div>
      <div style="margin-top:2mm">{pauta(frase2, 172, 2.6, rotulos=nomes2)}</div>
      <div style="margin-top:2mm">{pauta(frase1, 172, 2.6, rotulos=nomes1)}</div>
      <p class="centro" style="font-size:14pt;line-height:1.55;font-style:italic;margin-top:5mm">Brilha, brilha, estrelinha,<br>lá no céu a cintilar;<br>quero ver você brilhar,<br>brilha, brilha, estrelinha.</p></div>
      {adulto("a melodia",
              "A melodia tem três partes: a primeira e a terceira são iguais (dó dó sol sol lá lá sol / fá fá mi mi ré ré dó); a do meio sobe e desce (sol sol fá fá mi mi ré, duas vezes). "
              "Cante devagar, mostrando as notas na pauta com o dedo. A letra em português tem várias versões; use a que sua família canta. Para ela, o importante é <b>cantar junto</b>. "
              "Quando conhecer bem, escute a obra de Mozart: o tema aparece inteiro, e depois ganha “roupas”.")}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo">{titulo("O mesmo tema, doze roupas", "Mozart escreveu doze variações sobre a estrelinha", 25)}
      <div style="margin-top:4mm">{musicograma([("tema", ROXO, "onda", 2), ("1", "#c0716b", "pontos", 1), ("2", "#5f8f8a", "zigue", 1), ("3", "#8a6f9e", "onda", 1), ("4", "#b8503a", "bloco", 1),
                                                  ("5", "#5f7f9c", "calma", 1), ("6", "#c0716b", "pontos", 1), ("…", "#bfae8f", "calma", 1), ("12", "#b8503a", "bloco", 1), ("tema", ROXO, "onda", 2)], 174, 40)}</div>
      <div class="caixa" style="margin-top:5mm"><div class="versal" style="font-size:12pt;letter-spacing:.1em;margin-bottom:1.5mm">Doze jeitos de cantar a estrelinha</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1mm 5mm;font-size:12pt;line-height:1.5">
          <div>1. bem devagar</div><div>2. bem depressa</div><div>3. forte</div><div>4. fraco</div><div>5. só com “lá-lá-lá”</div><div>6. só com “miau”</div>
          <div>7. de olhos fechados</div><div>8. batendo palmas</div><div>9. sussurrando</div><div>10. como um elefante</div><div>11. como um ratinho</div><div>12. do jeito dela</div></div></div>
      <div class="centro" style="margin-top:5mm;line-height:0">{pd("opera_sixpence", "52mm", "margin:0 auto")}</div></div>
      {adulto("variações: o tema e as roupas",
              "Uma <b>variação</b> é a mesma melodia vestida de outro jeito. O livro de cantigas de Walter Crane que usamos nesta coleção se chama <i>The Baby's Opera: a book of old rhymes, with new dresses</i>, "
              "“velhas rimas com roupas novas”: é a mesma ideia. Cante com ela de cada um dos doze jeitos, um por dia, ou todos na mesma tarde. Ao escutar a obra de Mozart, pergunte: “é a mesma "
              "música? o que mudou?”. A página do <i>Sixpence</i> é a partitura de outra cantiga de Crane.",
              credito_pd("opera_sixpence"))}"""
    L.add(c, aba="--d-historias")

    c = f"""<div class="miolo">{titulo("Dó, ré, mi, com cores", "tocar a estrelinha num xilofone colorido", 26)}
      <div class="centro" style="margin:2mm 0;line-height:0">{img("xilofone", "48mm", "margin:0 auto")}</div>
      <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:1.5mm;text-align:center;font-size:11pt;margin:2mm 0 4mm">
        <div style="background:#c43a2e;color:#fff;border-radius:2mm;padding:1mm">dó</div><div style="background:#d8803a;color:#fff;border-radius:2mm;padding:1mm">ré</div>
        <div style="background:#e8b830;border-radius:2mm;padding:1mm">mi</div><div style="background:#7f9a52;color:#fff;border-radius:2mm;padding:1mm">fá</div>
        <div style="background:#5f8f8a;color:#fff;border-radius:2mm;padding:1mm">sol</div><div style="background:#4f74a8;color:#fff;border-radius:2mm;padding:1mm">lá</div>
        <div style="background:#8a6f9e;color:#fff;border-radius:2mm;padding:1mm">si</div></div>
      {partitura_cores([list("CCGGAAG"), list("FFEEDDC"), list("GGFFEED"), list("GGFFEED"), list("CCGGAAG"), list("FFEEDDC")], 150, 7)}</div>
      {adulto("uma partitura de cores",
              "Cole fita colorida nas barras do xilofone (ou nas bordas dos copos de vidro afinados com água, só com adulto), uma cor para cada nota, e toque seguindo as bolinhas da esquerda para a direita, "
              "uma linha por vez. É a melodia da página anterior, com cores no lugar de notas. Quando ela souber de cor, tire as cores e veja se continua tocando. "
              "<b>Criar:</b> ela escolhe a ordem das cores e você canta o que ela tocou.")}"""
    L.add(c, aba="--d-historias")

    caixas = "".join(f'<div class="caixa" style="height:44mm"><div class="peq centro">{t}</div></div>' for t in
                     ["1 · devagar", "2 · depressa", "3 · forte", "4 · fraco", "5 · lá-lá-lá", "6 · miau", "7 · olhos fechados", "8 · palmas", "9 · sussurro", "10 · elefante", "11 · ratinho", "12 · dela"])
    c = f"""<div class="miolo">{titulo("Doze roupas para a estrelinha", "um risco, um desenho ou uma cor para cada jeito", 25)}
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3.5mm;margin-top:5mm">{caixas}</div></div>
      {adulto("registrar a brincadeira",
              "Depois de cantar cada jeito, ela faz um risco, um desenho ou uma mancha de cor no quadro correspondente, como quiser. É um registro da música que ela inventou, e, daqui a alguns meses, "
              "é bonito ver. Não corrija nem peça “mais bonito”. Escreva ao lado, com data, o que ela disser de cada quadro.")}"""
    L.add(c, aba="--d-historias")


# ================================================================== U8 SAINT-SAËNS E DEBUSSY

def unidade8(L):
    inicio_unidade(L, 7)
    guia(L, dict(
        titulo="Unidade 8 · Saint-Saëns e Debussy", aba="--d-artes",
        pergunta="A música pode ser um bicho? Pode ser luz? — o zoológico de Saint-Saëns e o luar de Debussy.",
        duracao="Três fins de semana · três encontros · 15 a 20 minutos. Cada compositor, uma obra.",
        objetivos=["Reconhecer o leão, a tartaruga, o elefante e o cisne na música.", "Ligar cada bicho ao instrumento que o representa.",
                   "Escutar <i>Clair de lune</i> com atenção, em silêncio, sem se mexer.", "Pintar ouvindo música.", "Comparar os dois compositores: um alegre e brincalhão, o outro calmo e luminoso."],
        repertorio="<b>Obra 1:</b> Camille Saint-Saëns (1835–1921), <i>O Carnaval dos Animais</i> (1886), suíte para orquestra de câmara. <b>Obra 2:</b> Claude Debussy (1862–1918), <i>Clair de lune</i> (da <i>Suite bergamasque</i>, publicada em 1905), para piano. "
                   "<b>Línguas:</b> <i>lion · le lion · leō</i>; <i>swan · le cygne · cygnus</i>; <i>moon · la lune · lūna</i>.",
        materiais="Gravações de <i>O Carnaval dos Animais</i> e de <i>Clair de lune</i>; os cartões dos bichos; aquarela ou tinta guache azul, roxa e amarela; papel grosso.",
        vida="Visitar um zoológico ou olhar bichos num livro, imitando como cada um se move.",
        etapas=[["Escutar um bicho por vez.", "Adivinhar quem é.", "Escutar <i>Clair de lune</i> no escuro."],
                ["Parear bicho e instrumento.", "O passeio pelo zoológico.", "Mover o cisne e o elefante."],
                ["Pintar o luar ouvindo.", "Inventar um bicho com música.", "Comparar os dois compositores."]],
        indicadores=["Reconhece o leão e o cisne.", "Anda como o elefante e como a tartaruga.", "Fica quieta durante <i>Clair de lune</i>.",
                     "Diz “é o cuco!” ao ouvir o clarinete.", "Pinta com a música tocando.", "Pede “o bicho” e “a lua” de novo."],
        interesse="assistir a uma gravação de <i>O Carnaval dos Animais</i> com orquestra, para ver os instrumentos de verdade.",
        dificil="só o cisne e a lua, os dois momentos mais calmos."))

    c = f"""<div class="miolo">{titulo("O Carnaval dos Animais", "Saint-Saëns, 1886 · uma brincadeira de músico", 25)}
      <div class="centro" style="margin:3mm 0;line-height:0">{tira(["leao", "elefante", "cisne", "canguru", "cuco", "burro"], "26mm", "1.5mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Camille Saint-Saëns era um músico francês sério, que escreveu óperas, sinfonias e música religiosa. Mas, no carnaval de 1886, escreveu para os amigos uma brincadeira:
      uma suíte com <b>catorze</b> pedacinhos, cada um um bicho, ou uma pessoa. Tinha tanto medo de que a brincadeira prejudicasse a sua fama de músico sério que proibiu a execução em público.
      Só depois da sua morte a obra inteira foi publicada, e hoje é uma das mais amadas pelas crianças.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Os bichos são: o leão, as galinhas e os galos, os burros, as tartarugas, o elefante, os cangurus, os peixes do aquário, as pessoas de orelhas compridas, o cuco no fundo do bosque,
      os pássaros do viveiro, os pianistas (que praticam escalas), os fósseis e o cisne, e o final. Escolha poucos de cada vez.</p>
      <div class="caixa" style="margin-top:4mm"><div class="versal" style="font-size:12pt;letter-spacing:.1em;margin-bottom:1.5mm">Os catorze pedaços</div>
        <ol style="columns:2;column-gap:8mm;font-size:11.5pt;line-height:1.5;padding-left:6mm">
          <li>Introdução e marcha real do leão</li><li>Galinhas e galos</li><li>Burros selvagens (os hemiones)</li><li>Tartarugas</li><li>O elefante</li><li>Cangurus</li><li>Aquário</li>
          <li>Pessoas de orelhas compridas</li><li>O cuco no fundo do bosque</li><li>Viveiro de pássaros</li><li>Pianistas</li><li>Fósseis</li><li>O cisne</li><li>Final</li></ol></div></div>
      {adulto("uma obra, muitas vezes",
              "<b>Esta é a obra da unidade.</b> Toque um pedaço de cada vez, começando pelo <b>Leão</b> (a marcha real, com os pianos e as cordas) e pelo <b>Cisne</b> (violoncelo, calmo). "
              "Cada movimento dura 1 a 2 minutos. A suíte inteira, 25 minutos, é para quando ela pedir. Pergunte sempre: “quem é este bicho?” e “como a música mostra isso?”. "
              "<b>Os animais da coleção</b> (leão, elefante, cisne, canguru, cuco, burro) são imagens originais.")}"""
    L.add(c, aba="--d-artes")

    cartoes(L, "Os bichos de Saint-Saëns", [
        dict(pt="leão", mot="leao", en="lion", fr="le lion", la="leō", som="pianos e cordas, graves e solenes", dica="A marcha real do leão: ande como um rei, de cabeça erguida."),
        dict(pt="galo", pd="cartao_galo", en="rooster", fr="le coq", la="gallus", som="piano, clarinete e violinos", dica="As galinhas e os galos: bicadas curtas e rápidas, <i>pic-pic</i>."),
        dict(pt="tartaruga", mot="tartaruga", en="tortoise", fr="la tortue", la="testūdō", som="cordas, lentíssimas", dica="Uma melodia conhecida (o cancã), tocada tão devagar que parece outra."),
        dict(pt="elefante", mot="elefante", en="elephant", fr="l'éléphant", la="elephantus", som="contrabaixo, o mais grave", dica="Uma valsa pesada. O elefante dança de leve, mas é muito grande."),
        dict(pt="canguru", mot="canguru", en="kangaroo", fr="le kangourou", som="dois pianos, saltando", dica="Notas curtas, uma pausa, outro pulo. Pule com as duas pernas."),
        dict(pt="peixe", mot="peixe_azul", en="fish", fr="le poisson", la="piscis", som="flauta e cordas, ondulando", dica="O aquário: a música escorre como a água. Mova os braços devagar."),
        dict(pt="cuco", mot="cuco", en="cuckoo", fr="le coucou", la="cuculus", som="clarinete (o cuco) e piano", dica="Só duas notas, bem longe. Onde está o cuco?"),
        dict(pt="cisne", mot="cisne", en="swan", fr="le cygne", la="cygnus", som="violoncelo e dois pianos", dica="O mais famoso de todos: o cisne desliza na água, calmo e silencioso."),
        dict(pt="burro", mot="burro", en="donkey", fr="l'âne", la="asinus", som="violinos agudos e rápidos", dica="As “orelhas compridas”: <i>ió, ió</i>, subindo e descendo depressa.")],
        "Volume 4 · Saint-Saëns")

    c = f"""<div class="miolo">{titulo("Passeio pelo zoológico", "seguir com o dedo, um bicho por vez", 26)}
      <div style="margin-top:5mm">{musicograma([("leão", "#c9812e", "bloco", 2), ("galos", "#c43a2e", "pontos", 2), ("tartarugas", "#5f8f8a", "calma", 3), ("elefante", "#7d8791", "bloco", 2),
                                                  ("cangurus", "#b88a56", "pontos", 2), ("aquário", "#5f7f9c", "onda", 3), ("cuco", "#8a96a4", "pontos", 2), ("cisne", "#c4d0de", "onda", 3)], 174, 46)}</div>
      <div class="centro" style="margin-top:3mm;line-height:0">{tira(["leao", "elefante", "cisne"], "34mm", "4mm")}</div>
      <div class="caixa" style="margin-top:4mm;font-size:11.5pt;line-height:1.45"><b>Como escutar:</b> escolha um bicho, ponha só aquele pedaço da gravação e deixe que ela diga quem é antes de você mostrar o desenho.
      Depois, ouçam dois seguidos (por exemplo, o leão e o cisne) e comparem: qual é forte? qual é calmo? qual é lento? qual é agudo?</div></div>
      {adulto("o passeio e o contraste",
              "O desenho segue a ordem da suíte (com alguns bichos a menos). Cada forma lembra o bicho: o leão é um bloco forte; os galos são pontos picados; as tartarugas, uma linha calma; os cangurus, pontos que pulam; "
              "o aquário, uma onda; o cuco, dois pontos distantes; o cisne, uma onda larga. A ideia é voltar às palavras da Unidade 3: <i>forte, fraco, rápido, lento, grave, agudo</i>.")}"""
    L.add(c, aba="--d-artes")

    observacao(L, "O Cisne", "o violoncelo conta a história",
               img("cisne", "62mm", "margin:0 auto") + f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:3mm;font-size:11.5pt;font-style:italic">
                 <div>{img("violoncelo", "26mm", "margin:0 auto")}<div>o violoncelo canta a melodia: o cisne</div></div>
                 <div>{img("piano", "34mm", "margin:0 auto")}<div>dois pianos fazem a água ondular</div></div></div>''',
               ["Que bicho é este? Como ele se move?", "A música é rápida ou lenta? Forte ou fraca?", "O violoncelo é um som grave ou agudo?",
                "Faça o cisne com os braços: devagar, devagar.", "Quando a música acaba, tudo fica quieto. Escute o silêncio."],
               adulto("o cisne",
                      "<b>O Cisne</b> (<i>Le Cygne</i>) é o único pedaço de <i>O Carnaval dos Animais</i> que Saint-Saëns deixou publicar em vida, em 1887. É uma melodia longa, tocada pelo violoncelo, enquanto os dois pianos "
                      "fazem a água ondular. Deixe que ela escute até o fim sem falar. Depois conversem sobre o que viu. É uma ótima música para a hora de acalmar."),
               aba="--d-artes")

    c = f"""<div class="miolo">{titulo("Debussy e o luar", "Paris, 1862 · um músico que escrevia com luz", 26)}
      <div class="centro" style="margin:5mm 0;line-height:0">{img("lua", "52mm", "display:inline-block;margin:0 8mm")}{img("estrela", "30mm", "display:inline-block;margin:0 8mm")}</div>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto">Claude Debussy era francês e queria que a música soasse como a luz na água, como a névoa, como o vento. Morava em Paris, e pintores franceses da mesma época,
      como Monet, faziam algo parecido com tinta: mostravam como o mundo <i>parece</i>, não só como ele <i>é</i>.</p>
      <p style="font-size:12.5pt;line-height:1.5;text-align:justify;hyphens:auto"><b>Clair de lune</b> (“luar”) é uma peça para piano, de uns cinco minutos, que ele escreveu quando era jovem e publicou em 1905. O nome vem de um poema do poeta francês Paul Verlaine, que fala de
      um luar triste e belo, com pássaros que sonham nas árvores. É a música da unidade para ouvir <b>no escuro</b>, com uma vela acesa, deitadas, sem falar.</p>
      <div style="margin-top:5mm">{musicograma([("começa baixinho", "#8a6f9e", "calma", 3), ("as notas correm como água", "#5f7f9c", "onda", 3), ("brilha mais", "#c9963f", "onda", 2), ("volta o começo", "#8a6f9e", "calma", 2), ("some", "#bfae8f", "calma", 2)], 174, 38)}</div>
      <div class="centro peq" style="margin-top:1mm">um desenho aproximado do caminho da música: calmo, corrente, mais brilhante, calmo de novo</div></div>
      {adulto("escuta no escuro",
              "<b>Esta é a segunda obra da unidade.</b> Apague a luz, acenda uma vela com cuidado (ou use uma luz fraca) e ponha <i>Clair de lune</i> baixinho. Fiquem juntas, deitadas, até o fim. "
              "Quando a música acabar, ela pode querer falar ou ficar quieta: respeite. Debussy morreu em 1918; a gravação, claro, tem direitos próprios. Não é preciso explicar a música; "
              "perguntar “o que você viu?” é suficiente.")}"""
    L.add(c, aba="--d-artes")

    pecas = [("elefante", "O berço do elefante", "uma canção de ninar para o elefante de brinquedo da filha dele, o Jimbo"),
             ("flauta", "O pequeno pastor", "uma flauta de pastor, que toca uma melodia simples no campo"),
             ("estrela", "Serenata para a boneca", "uma canção de boa-noite para a boneca, tocada devagar e com carinho"),
             ("nuvem", "A neve está dançando", "flocos que caem e rodopiam, notas leves, rápidas e repetidas"),
             ("livro", "Doutor Gradus ad Parnassum", "uma brincadeira com os exercícios de piano que as crianças têm de estudar")]
    cel = "".join(f'<tr><td style="width:36mm;text-align:center">{img(m, "24mm", "margin:0 auto")}</td><td><b style="font-size:13pt">{t}</b><br><span style="font-size:11.5pt">{d}</span></td></tr>' for m, t, d in pecas)
    c = f"""<div class="miolo">{titulo("O canto das crianças", "Children's Corner · Debussy, 1908", 26)}
      <p class="centro" style="font-size:12.5pt;line-height:1.5;margin:3mm 0 4mm">Debussy escreveu uma suíte para a sua filha Claude-Emma, que tinha 3 anos e se chamava “Chouchou”.
      A suíte tem seis peças; estas são as mais adequadas para uma criança pequena.</p>
      <table class="tab">{cel}</table>
      <div class="caixa" style="margin-top:5mm"><div class="versal" style="font-size:12pt;letter-spacing:.1em;margin-bottom:2mm">Uma peça por semana</div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;text-align:center;font-size:10.5pt">
          <div>semana 1<br><b>O berço do elefante</b><div style="border:0.5pt solid var(--linha);height:14mm;margin-top:1.5mm;border-radius:2mm"></div></div>
          <div>semana 2<br><b>O pequeno pastor</b><div style="border:0.5pt solid var(--linha);height:14mm;margin-top:1.5mm;border-radius:2mm"></div></div>
          <div>semana 3<br><b>A neve está dançando</b><div style="border:0.5pt solid var(--linha);height:14mm;margin-top:1.5mm;border-radius:2mm"></div></div>
          <div>semana 4<br><b>Serenata para a boneca</b><div style="border:0.5pt solid var(--linha);height:14mm;margin-top:1.5mm;border-radius:2mm"></div></div>
          <div>semana 5<br><b>Doutor Gradus…</b><div style="border:0.5pt solid var(--linha);height:14mm;margin-top:1.5mm;border-radius:2mm"></div></div></div>
        <div class="peq centro" style="margin-top:2mm">marcar com um desenho, uma estrela ou uma cor, quando ela pedir a peça de novo</div></div></div>
      {adulto("música feita para uma criança",
              "Esta é uma das poucas suítes escritas por um grande compositor para o dia a dia de uma criança pequena. Os títulos são em inglês porque a filha tinha uma governanta inglesa e estava "
              "na moda. Para esta idade, basta escutar <b>uma peça por semana</b>: “O berço do elefante”, “O pequeno pastor” e “A neve está dançando” são as melhores para começar. "
              "Escolha a gravação que tiver; não precisa ser a de piano de maior fama.")}"""
    L.add(c, aba="--d-artes")

    passos(L, "Pintar o luar", "uma aquarela feita ouvindo Debussy",
           [(img("jarra", "22mm"), "Molhe o papel com um pincel largo e água limpa"),
            (img("lua", "22mm"), "Ponha <i>Clair de lune</i> bem baixinho"),
            (img("circulo_azul", "20mm"), "Pinte faixas de azul no papel molhado"),
            (img("circulo_amarelo", "20mm"), "Um toque de amarelo no meio: a lua"),
            (img("gota", "20mm"), "Deixe a tinta escorrer e se misturar sozinha"),
            (img("estrela", "22mm"), "Quando secar, ela dá um nome ao quadro")],
           adulto("pintar ouvindo",
                  "Não é para desenhar uma lua: é deixar que a música conduza o pincel. Prepare aquarela ou guache bem aguados, papel grosso e um pano. Fique ao lado, sem dirigir. "
                  "Quando a pintura secar, pergunte o nome que ela quer dar. Este é o fim do volume: a mesma ideia de Debussy e dos pintores franceses do seu tempo, que o Volume 5 (as artes) vai continuar.",
                  ), aba="--d-artes")


# ================================================================== ENCERRAMENTO

def encerramento(L):
    L.unidade = "Encerramento"
    INICIO["Encerramento"] = L.proximo

    hot1 = [("E4", "q"), ("D4", "q"), ("C4", "h"), "|", ("E4", "q"), ("D4", "q"), ("C4", "h"), "|", ("C4", "e"), ("C4", "e"), ("C4", "e"), ("C4", "e"), ("D4", "e"), ("D4", "e"), ("D4", "e"), ("D4", "e"), "|", ("E4", "q"), ("D4", "q"), ("C4", "h")]
    mary = [("E4", "q"), ("D4", "q"), ("C4", "q"), ("D4", "q"), "|", ("E4", "q"), ("E4", "q"), ("E4", "h"), "|", ("D4", "q"), ("D4", "q"), ("D4", "h"), "|", ("E4", "q"), ("G4", "q"), ("G4", "h")]
    clair = [("C4", "q"), ("C4", "q"), ("C4", "q"), ("D4", "q"), "|", ("E4", "h"), ("D4", "h"), "|", ("C4", "q"), ("E4", "q"), ("D4", "q"), ("D4", "q"), "|", ("C4", "w")]
    c = f"""<div class="miolo">{titulo("Caderno de cantigas", "para o adulto cantar · melodias tradicionais, em dó maior", 26)}
      <h2 class="titulo" style="font-size:14pt;margin:5mm 0 1mm;text-align:left">Hot cross buns <span class="peq it" style="font-weight:400">— só três notas: mi, ré, dó</span></h2>
      {pauta(hot1, 172, 2.4, letra=["Hot", "cross", "buns", "hot", "cross", "buns", "One", "a", "pen", "ny", "two", "a", "pen", "ny", "hot", "cross", "buns"])}
      <h2 class="titulo" style="font-size:14pt;margin:6mm 0 1mm;text-align:left">Mary had a little lamb <span class="peq it" style="font-weight:400">— <i>Maria tinha um carneirinho</i></span></h2>
      {pauta(mary, 172, 2.4, letra=["Ma", "ry", "had", "a", "lit", "tle", "lamb", "lit", "tle", "lamb", "lit", "tle", "lamb"])}
      <h2 class="titulo" style="font-size:14pt;margin:6mm 0 1mm;text-align:left">Au clair de la lune <span class="peq it" style="font-weight:400">— primeira frase; a melodia volta no fim da estrofe</span></h2>
      {pauta(clair, 172, 2.4, letra=["Au", "clair", "de", "la", "lu", "ne", "mon", "a", "mi", "Pier", "rot"])}
      <p class="centro" style="font-size:12pt;line-height:1.5;font-style:italic;margin-top:4mm">Au clair de la lune, mon ami Pierrot,<br>prête-moi ta plume pour écrire un mot.<br>
      Ma chandelle est morte, je n'ai plus de feu;<br>ouvre-moi ta porte, pour l'amour de Dieu.</p></div>
      {adulto("cantar o que se tem",
              "Estas três cantigas são tradicionais (domínio público) e têm poucas notas, boas para a voz de quem não se considera cantor. Cante com <i>lá, lá, lá</i> se esquecer a letra. "
              "<b>Hot cross buns</b> usa só três notas e é a mais fácil para começar. <b>Au clair de la lune</b> é francesa e vira a primeira canção de ninar de muitas crianças. "
              "Para tocar num teclado, as notas usam só as teclas brancas, de dó a sol.")}"""
    L.add(c, aba="--d-musica")

    cantigas = [("Ciranda, cirandinha", "Ciranda, cirandinha,<br>vamos todos cirandar;<br>vamos dar a meia-volta,<br>volta e meia vamos dar."),
                ("Sapo cururu", "Sapo cururu<br>na beira do rio;<br>quando o sapo grita, ó maninha,<br>é porque tem frio."),
                ("Meu limão, meu limoeiro", "Meu limão, meu limoeiro,<br>meu pé de jacarandá;<br>uma vez, tindolelê,<br>outra vez, tindolalá."),
                ("A canoa virou", "A canoa virou<br>por deixarem ela virar;<br>foi por causa da Maria<br>que não soube remar."),
                ("Alecrim dourado", "Alecrim, alecrim dourado,<br>que nasceu no campo<br>sem ser semeado.")]
    cel = "".join(f'<div style="break-inside:avoid;margin-bottom:3mm"><div style="font-weight:600;font-size:12pt;color:var(--musgo)">{n}</div>'
                  f'<div style="font-size:11.5pt;line-height:1.4;font-style:italic">{t}</div></div>' for n, t in cantigas)
    c = f"""<div class="miolo">{titulo("Cantigas do Brasil", "a letra, e uma pauta em branco para a melodia da sua família", 25)}
      <div style="columns:2;column-gap:8mm;margin-top:4mm">{cel}</div>
      <div style="margin-top:4mm">{pauta([], 172, 2.4)}</div><div style="margin-top:3mm">{pauta([], 172, 2.4)}</div><div style="margin-top:3mm">{pauta([], 172, 2.4)}</div></div>
      {adulto("cantar as nossas",
              "As cantigas de roda brasileiras viajaram de boca em boca e têm <b>muitas melodias</b>, que variam de região para região e de família para família. Por isso o caderno registra só a letra: cante como sua "
              "família canta. As pautas em branco são para você escrever a melodia que cantam em casa, nota por nota (ou pôr a letra e o ritmo com as hastes das páginas 18 e 19). Para a criança, o que fica "
              "é o <b>jeito da família</b>, a voz de quem canta para ela.")}"""
    L.add(c, aba="--d-musica")

    itens = [("Vivaldi", 1678, 1741, "#5f8f8a"), ("Bach", 1685, 1750, "#5f7f9c"), ("Mozart", 1756, 1791, "#c0716b"),
             ("Saint-Saëns", 1835, 1921, "#c9963f"), ("Debussy", 1862, 1918, "#8a6f9e"), ("Prokofiev", 1891, 1953, "#7f9a52")]
    c = f"""<div class="miolo">{titulo("Os músicos desta coleção", "quando viveram", 28)}
      <div style="margin-top:8mm">{linha_do_tempo(itens)}</div>
      <table class="tab" style="margin-top:8mm;font-size:11pt">
        <tr><td style="width:32mm"><b>Vivaldi</b></td><td><i>A Primavera</i> · violinos, pássaros, riacho, trovão</td></tr>
        <tr><td><b>Bach</b></td><td><i>Prelúdio em dó maior</i> · uma onda de notas que sobe e desce</td></tr>
        <tr><td><b>Mozart</b></td><td><i>Variações sobre “Ah! vous dirai-je, Maman”</i> · a estrelinha e suas roupas</td></tr>
        <tr><td><b>Saint-Saëns</b></td><td><i>O Carnaval dos Animais</i> · o leão, o elefante, o cisne</td></tr>
        <tr><td><b>Debussy</b></td><td><i>Clair de lune</i> e <i>Children's Corner</i> · o luar e a música de criança</td></tr>
        <tr><td><b>Prokofiev</b></td><td><i>Pedro e o Lobo</i> · cada personagem um instrumento</td></tr></table></div>
      {adulto("o tempo na música",
              "Mostre a ela as barras como ruas compridas de tempo: Vivaldi e Bach viveram há mais de 300 anos, Mozart há mais de 200, Saint-Saëns e Debussy há pouco mais de 100. "
              "A diferença de tempo entre eles é enorme, mas as músicas vivem juntas na sua casa. Se ela perguntar “eles ainda estão vivos?”, é a ocasião de falar de como a música continua depois de quem a escreveu.")}"""
    L.add(c, aba="--d-musica")

    for k in range(2):
        linhas = "".join(f'<tr><td style="width:40mm;height:46mm"><div class="peq">data</div></td><td style="width:44mm"><div class="peq">obra</div></td><td><div class="peq">o que ela fez, disse ou pediu</div></td></tr>'
                         for _ in range(5))
        c = f"""<div class="miolo">{titulo("Diário de escuta", "para o adulto · o que ela ouviu, fez e disse — não é avaliação", 26)}
          <table class="tab diario"><tr><th>Data</th><th>Obra</th><th>O que ela fez, disse ou pediu</th></tr>{linhas}</table></div>"""
        L.add(c, aba="--d-memoria")

    usados = ["opera_"]
    import fontes_v1
    por_livro = {}
    for n, (item, pg, *_r) in fontes_v1.ITENS.items():
        if n.startswith("opera_") or n in ("cartao_galo", "cartao_vaca", "rackham_lebre", "rackham_bremen") or n.startswith("brooke_mingau") or n.startswith("brooke_camas_ursos"):
            por_livro.setdefault(item, set()).add(pg)
    cred = "".join(f"<li>{fontes_v1.LIVROS[i]} — Internet Archive, <i>{i}</i>, páginas {', '.join('n' + str(p) for p in sorted(ps))}.</li>" for i, ps in por_livro.items())
    c = f"""<div class="miolo texto">{titulo("Repertório e créditos", "Volume 4", 26)}
      <h2>Obras para escutar</h2><p style="font-size:9.6pt">Vivaldi, <i>As Quatro Estações</i>: <i>A Primavera</i> (concerto n.º 1, primeiro movimento) · Bach, <i>Prelúdio em dó maior</i> (BWV 846) · Mozart, <i>Variações sobre “Ah! vous dirai-je, Maman”</i> (K. 265) ·
      Saint-Saëns, <i>O Carnaval dos Animais</i> · Debussy, <i>Clair de lune</i> e <i>Children's Corner</i> · Prokofiev, <i>Pedro e o Lobo</i>. Os compositores morreram há mais de 70 anos; cada gravação tem direitos próprios, e indicamos só as obras.</p>
      <h2>Cantigas</h2><p style="font-size:9.6pt">Cantigas tradicionais de domínio público (<i>Marcha, soldado</i>, <i>Ciranda, cirandinha</i>, <i>Sapo cururu</i>, <i>Meu limão, meu limoeiro</i>, <i>A canoa virou</i>, <i>Alecrim dourado</i>,
      <i>Hot cross buns</i>, <i>Mary had a little lamb</i>, <i>Au clair de la lune</i>). Tradução e adaptação da coleção: <i>Ding, dong, bell</i>, <i>Dance a baby, diddy</i>, <i>Here we go round the mulberry bush</i>, <i>Old King Cole</i>. As partituras impressas em inglês
      são as originais de Walter Crane.</p>
      <h2>Fundamentos</h2><p style="font-size:9.6pt">Escuta repetida e música no ambiente da família (Shinichi Suzuki); o corpo como primeiro instrumento (Émile Jaques-Dalcroze); pulso, ritmo e voz antes da notação (tradição de educação musical infantil). Nenhum material reproduz métodos ou produtos comerciais.</p>
      <h2>Ilustrações em domínio público</h2><p style="font-size:9pt">Digitalizações do Internet Archive, com recorte e ajuste do tom do papel; nenhuma pintura foi retocada. A clave de sol é o recorte de uma partitura de <i>The Baby's Opera</i> (Walter Crane).</p>
      <ul style="font-size:8.6pt;line-height:1.35">{cred}</ul>
      <p style="font-size:9pt">Instrumentos, bichos e notas: aquarela digital procedural da coleção. Tipografia: EB Garamond (licença OFL).</p></div>"""
    L.add(c)

    c = f"""<div class="miolo centro" style="top:50mm">
      <div style="font-size:12pt;letter-spacing:.25em;text-transform:uppercase;color:var(--sepia)">Até logo, Volume 4</div>
      <div style="font-size:26pt;font-weight:500;margin:6mm 0">No próximo livro…</div>
      <p style="font-size:15pt;line-height:1.6;font-style:italic">a cor e a linha, a luz de um jardim,<br>o guache, a tinta, o papel que a Marina pinta,<br>
      e os mestres da pintura que viram o mundo de outro jeito.</p>
      <div style="margin-top:12mm">{tira(["circulo_vermelho", "circulo_amarelo", "circulo_azul"], "30mm", "3mm")}</div>
      <p class="peq" style="margin-top:8mm">Volume 5 · O mundo das artes</p></div>"""
    L.add(c, cabecalho=False)


# ================================================================== MONTAGEM

def montar(unidades=None):
    L = Livro(4, "O mundo da música")
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
    for versao, nome in (("impressao", "volume4-impressao"), ("tela", "volume4-tela")):
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
    subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(SAIDA, "volume4-tela.pdf"), os.path.join(insp, "p")], check=True)


if __name__ == "__main__":
    main()
