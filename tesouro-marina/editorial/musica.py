"""
Notação musical para os volumes da coleção (SVG em milímetros): pauta com melodia e letra, tiras de ritmo,
musicogramas (a música desenhada como forma e cor) e linha de pulso.
A clave de sol é o recorte de uma partitura de Walter Crane (domínio público): ver dominio_publico/CREDITOS.md.
"""
import math

TINTA = "#3d3127"
SEPIA = "#6b5440"

# posição diatônica: E4 (linha de baixo) = 0; cada passo = meio espaço
_NOTAS = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
_PESO = {"w": 4.0, "h": 2.0, "q": 1.0, "e": 0.5}


def posicao(nome):
    """'E4' -> 0, 'G4' -> 2, 'C5' -> 5, 'C4' -> -2."""
    return _NOTAS[nome[0]] + 7 * (int(nome[1]) - 4) - 2


def pauta(compasso, larg=170, esp=2.3, letra=None, clave=True, cor_nota=TINTA, rotulos=None):
    """
    Uma pauta de 5 linhas. compasso: lista de ("C4", "q"), ("R", "q") (pausa) ou "|" (barra).
    letra: sílabas (uma por nota, pausas não levam sílaba). rotulos: texto sob cada nota (ex.: dó, ré...).
    Devolve o HTML de um <svg> com largura larg (mm).
    """
    notas = [i for i in compasso if i != "|" and i[0] != "R"]
    for nome_lista, lista in (("letra", letra), ("rotulos", rotulos)):
        if lista is not None and len(lista) != len(notas):   # sílaba sob a nota errada ensina a cantar errado
            raise ValueError(f"{nome_lista} tem {len(lista)} itens, mas a pauta tem {len(notas)} notas")
    for it in compasso:
        if it != "|" and it[0] == "R" and it[1] not in ("q", "h"):
            raise ValueError(f"pausa de duração {it[1]!r} não suportada (só 'q' e 'h')")
    ini = 12.5 if clave else 4
    topo = 6 * esp                       # espaço acima da pauta (para notas agudas e hastes)
    base = topo + 4 * esp                # linha de baixo
    alt = base + 7 * esp + (4.5 if letra else 0) + (4.5 if rotulos else 0)
    itens = [i for i in compasso]
    pesos = [(_PESO[i[1]] + 0.55) if i != "|" else 0.7 for i in itens]
    unit = (larg - ini - 4) / sum(pesos) if pesos else 0
    xs, x = [], ini
    for p in pesos:
        xs.append(x + p * unit / 2)
        x += p * unit
    partes = []
    for k in range(5):
        y = topo + k * esp
        partes.append(f'<line x1="0" y1="{y:.2f}" x2="{larg}" y2="{y:.2f}" stroke="{SEPIA}" stroke-width="0.22"/>')
    partes.append(f'<line x1="0" y1="{topo:.2f}" x2="0" y2="{base:.2f}" stroke="{SEPIA}" stroke-width="0.35"/>')
    partes.append(f'<line x1="{larg}" y1="{topo:.2f}" x2="{larg}" y2="{base:.2f}" stroke="{SEPIA}" stroke-width="0.35"/>')
    if clave:
        # a imagem tem 56 × 110 px; 15 px = 1 espaço; o topo da imagem fica 1,2 espaço acima da linha de cima
        w_img, h_img = 56 / 15 * esp, 110 / 15 * esp
        partes.append(f'<image href="dominio_publico/clave_sol.png" x="{1.2:.2f}" y="{topo - 1.2 * esp:.2f}" width="{w_img:.2f}" height="{h_img:.2f}"/>')
    lig, k = {}, 0       # colcheias vizinhas (sem barra no meio) ligam-se em pares por uma trave
    while k < len(itens):
        if itens[k] != "|" and itens[k][1] == "e" and itens[k][0] != "R" and k + 1 < len(itens) \
                and itens[k + 1] != "|" and itens[k + 1][1] == "e" and itens[k + 1][0] != "R":
            lig[k], lig[k + 1] = "ini", "fim"
            k += 2
        else:
            k += 1
    feixe = (0, 0)
    sil = iter(letra or [])
    rot = iter(rotulos or [])
    i = 0
    while i < len(itens):
        it = itens[i]
        x = xs[i]
        if it == "|":
            partes.append(f'<line x1="{x:.2f}" y1="{topo:.2f}" x2="{x:.2f}" y2="{base:.2f}" stroke="{SEPIA}" stroke-width="0.3"/>')
            i += 1
            continue
        nome, dur = it
        if nome == "R":     # pausa de semínima (zigue-zague) ou de mínima (retângulo sobre a 3.ª linha)
            if dur == "h":
                partes.append(f'<rect x="{x - esp * 0.55:.2f}" y="{topo + 1.5 * esp:.2f}" width="{esp * 1.1:.2f}" height="{esp * 0.5:.2f}" fill="{cor_nota}"/>')
            else:
                y0 = topo + 0.6 * esp
                d = (f"M{x - 0.35 * esp:.2f} {y0:.2f} L{x + 0.45 * esp:.2f} {y0 + 0.9 * esp:.2f} L{x - 0.4 * esp:.2f} {y0 + 1.9 * esp:.2f} "
                     f"L{x + 0.4 * esp:.2f} {y0 + 2.8 * esp:.2f}")
                partes.append(f'<path d="{d}" fill="none" stroke="{cor_nota}" stroke-width="{esp * 0.3:.2f}" stroke-linejoin="round" stroke-linecap="round"/>')
            i += 1
            continue
        pos = posicao(nome)
        y = base - pos * esp / 2
        rx, ry = esp * 0.62, esp * 0.46
        cheio = dur in ("q", "e")
        if pos <= -2:   # linha suplementar (C4)
            for p in range(-2, 0, 2):
                yy = base - p * esp / 2
                partes.append(f'<line x1="{x - esp:.2f}" y1="{yy:.2f}" x2="{x + esp:.2f}" y2="{yy:.2f}" stroke="{SEPIA}" stroke-width="0.25"/>')
        partes.append(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" transform="rotate(-20 {x:.2f} {y:.2f})" '
                      f'fill="{cor_nota if cheio else "#fbf6ea"}" stroke="{cor_nota}" stroke-width="{esp * 0.2:.2f}"/>')
        haste_acima = pos < 4
        if i in lig:   # colcheias ligadas por uma trave: as duas hastes vão para o mesmo lado
            par = i + 1 if lig[i] == "ini" else i - 1
            haste_acima = (pos + posicao(itens[par][0])) / 2 < 4
        if dur != "w":
            if haste_acima:
                hx, y2 = x + rx * 0.92, y - 3.3 * esp
            else:
                hx, y2 = x - rx * 0.92, y + 3.3 * esp
            partes.append(f'<line x1="{hx:.2f}" y1="{y:.2f}" x2="{hx:.2f}" y2="{y2:.2f}" stroke="{cor_nota}" stroke-width="{esp * 0.14:.2f}"/>')
            if dur == "e":
                papel = lig.get(i, "solo")
                if papel == "ini":
                    feixe = (hx, y2)
                elif papel == "fim":
                    partes.append(f'<line x1="{feixe[0]:.2f}" y1="{feixe[1]:.2f}" x2="{hx:.2f}" y2="{y2:.2f}" stroke="{cor_nota}" '
                                  f'stroke-width="{esp * 0.45:.2f}"/>')
                else:
                    sinal = 1 if haste_acima else -1
                    partes.append(f'<path d="M{hx:.2f} {y2:.2f} q{esp * 0.9:.2f} {sinal * esp * 0.7:.2f} {esp * 0.5:.2f} {sinal * esp * 1.7:.2f}" '
                                  f'fill="none" stroke="{cor_nota}" stroke-width="{esp * 0.2:.2f}"/>')
        baixo = base + 7 * esp
        if letra is not None:
            s = next(sil, "")
            partes.append(f'<text x="{x:.2f}" y="{base + 6.2 * esp:.2f}" text-anchor="middle" class="svg-letra">{s}</text>')
            baixo = base + 6.2 * esp
        if rotulos is not None:
            r = next(rot, "")
            partes.append(f'<text x="{x:.2f}" y="{base + 6.2 * esp + (4.2 if letra is not None else 0):.2f}" text-anchor="middle" class="svg-rotulo">{r}</text>')
        i += 1
    return (f'<svg viewBox="0 0 {larg} {alt:.2f}" style="width:{larg}mm;height:{alt:.2f}mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(partes) + "</svg>")


def tira_ritmo(padrao, larg=150, cor="#8a6f9e", rotulos=True, k=1.0):
    """
    Ritmo em hastes (como se faz com crianças): 'ta' = uma haste; 'ti-ti' = duas hastes ligadas; 'sh' = silêncio (pausa).
    padrao: lista com 'ta', 'ti', 'sh'.
    """
    if not padrao:
        raise ValueError("tira_ritmo precisa de ao menos uma figura")
    n = len(padrao)
    cel = larg / n
    altura = 22 if rotulos else 16
    p = []
    for idx, t in enumerate(padrao):
        cx = idx * cel + cel / 2
        p.append(f'<g transform="translate({cx:.1f},12) scale({k}) translate({-cx:.1f},-12)">')
        if t == "ta":
            p.append(f'<ellipse cx="{cx - 0.5:.1f}" cy="12.5" rx="2.6" ry="2" transform="rotate(-20 {cx - 0.5:.1f} 12.5)" fill="{cor}"/>')
            p.append(f'<line x1="{cx + 1.9:.1f}" y1="12.3" x2="{cx + 1.9:.1f}" y2="2" stroke="{cor}" stroke-width="0.7"/>')
            nome = "ta"
        elif t == "ti":
            for dx in (-3.2, 3.2):
                p.append(f'<ellipse cx="{cx + dx - 0.5:.1f}" cy="12.5" rx="2.6" ry="2" transform="rotate(-20 {cx + dx - 0.5:.1f} 12.5)" fill="{cor}"/>')
                p.append(f'<line x1="{cx + dx + 1.9:.1f}" y1="12.3" x2="{cx + dx + 1.9:.1f}" y2="2" stroke="{cor}" stroke-width="0.7"/>')
            p.append(f'<line x1="{cx - 3.2 + 1.9:.1f}" y1="2.2" x2="{cx + 3.2 + 1.9:.1f}" y2="2.2" stroke="{cor}" stroke-width="1.6"/>')
            nome = "ti-ti"
        else:
            p.append(f'<path d="M{cx - 1.5:.1f} 4 L{cx + 1.8:.1f} 7.5 L{cx - 1.6:.1f} 10.5 L{cx + 1.6:.1f} 14" fill="none" stroke="{SEPIA}" stroke-width="0.9" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
            nome = "(sh)"
        p.append("</g>")
        if rotulos:
            p.append(f'<text x="{cx:.1f}" y="19.5" text-anchor="middle" class="svg-rotulo">{nome}</text>')
    topo = 10 * (k - 1)
    return (f'<svg viewBox="0 {-topo:.1f} {larg} {altura + topo:.1f}" style="width:{larg}mm;height:{altura + topo:.1f}mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(p) + "</svg>")


def linha_pulso(n=8, larg=170, destaque=None, cor="#8a6f9e"):
    """Pulso como uma fila de passos/batidas: círculos iguais, com acento (forte) nos marcados em destaque."""
    destaque = destaque or []
    cel = larg / n
    p = []
    for k in range(n):
        cx = k * cel + cel / 2
        forte = k in destaque
        r = 4.2 if forte else 2.6
        p.append(f'<circle cx="{cx:.1f}" cy="6" r="{r}" fill="{cor if forte else "none"}" stroke="{cor}" stroke-width="0.7"/>')
    return (f'<svg viewBox="0 0 {larg} 12" style="width:{larg}mm;height:12mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(p) + "</svg>")


def musicograma(secoes, larg=174, alt=46):
    """
    A música desenhada. secoes: lista de (rótulo, cor, forma, peso) com forma em
    'onda' (legato, contínua), 'pontos' (staccato), 'zigue' (agitada), 'bloco' (forte e cheia), 'calma' (linha quase reta).
    Cada seção ocupa largura proporcional ao peso. Sem escala de tempo: o adulto acompanha com o dedo enquanto escutam.
    """
    if not secoes:
        raise ValueError("musicograma precisa de ao menos uma seção")
    total = sum(s[3] for s in secoes)
    x = 2
    util = larg - 4
    p = [f'<line x1="0" y1="{alt / 2:.1f}" x2="{larg}" y2="{alt / 2:.1f}" stroke="#bfae8f" stroke-width="0.25" stroke-dasharray="1 1.4"/>']
    for rotulo, cor, forma, peso in secoes:
        w = util * peso / total
        mid = alt / 2
        if forma == "onda":
            pts = " ".join(f"{x + w * t / 40:.1f},{mid - 9 * math.sin(t / 40 * 3 * math.pi * 2):.1f}" for t in range(41))
            p.append(f'<polyline points="{pts}" fill="none" stroke="{cor}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        elif forma == "pontos":
            n = max(3, int(w / 5.5))
            for k in range(n):
                cx = x + w * (k + 0.5) / n
                cy = mid - 10 * math.sin(k * 0.9)
                p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.7" fill="{cor}"/>')
        elif forma == "zigue":
            n = max(4, int(w / 3.2))
            pts = " ".join(f"{x + w * k / n:.1f},{mid + (13 if k % 2 else -13) * (0.6 + 0.4 * math.sin(k)):.1f}" for k in range(n + 1))
            p.append(f'<polyline points="{pts}" fill="none" stroke="{cor}" stroke-width="2" stroke-linejoin="round"/>')
        elif forma == "bloco":
            p.append(f'<rect x="{x + 1:.1f}" y="{mid - 15:.1f}" width="{w - 2:.1f}" height="30" rx="3" fill="{cor}" fill-opacity="0.55" stroke="{cor}" stroke-width="0.6"/>')
        else:   # calma
            pts = " ".join(f"{x + w * t / 20:.1f},{mid - 2 * math.sin(t / 20 * math.pi * 2):.1f}" for t in range(21))
            p.append(f'<polyline points="{pts}" fill="none" stroke="{cor}" stroke-width="2.2" stroke-linecap="round"/>')
        p.append(f'<text x="{x + w / 2:.1f}" y="{alt - 2:.1f}" text-anchor="middle" class="svg-rotulo">{rotulo}</text>')
        x += w
    return (f'<svg viewBox="0 0 {larg} {alt}" style="width:{larg}mm;height:{alt}mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(p) + "</svg>")


CORES_NOTAS = {"C": "#c43a2e", "D": "#d8803a", "E": "#e8b830", "F": "#7f9a52", "G": "#5f8f8a", "A": "#4f74a8", "B": "#8a6f9e"}
SOLFEJO = {"C": "dó", "D": "ré", "E": "mi", "F": "fá", "G": "sol", "A": "lá", "B": "si"}


def partitura_cores(frases, larg=170, por_linha=14):
    """
    A melodia em bolinhas coloridas, na ordem em que se toca, para seguir num xilofone ou em copos pintados da mesma cor.
    frases: lista de listas de notas ('C', 'G'...). Cada frase vira uma linha.
    """
    cel = larg / por_linha
    linhas = []
    for j, fr in enumerate(frases):
        y = 8 + j * 19
        for i, n in enumerate(fr):
            cx = cel / 2 + i * cel
            linhas.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="5.2" fill="{CORES_NOTAS[n[0]]}" fill-opacity="0.85" stroke="#5b4632" stroke-width="0.3"/>')
            linhas.append(f'<text x="{cx:.1f}" y="{y + 9.8:.1f}" text-anchor="middle" class="svg-rotulo">{SOLFEJO[n[0]]}</text>')
    alt = 8 + len(frases) * 19
    return (f'<svg viewBox="0 0 {larg} {alt}" style="width:{larg}mm;height:{alt}mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(linhas) + "</svg>")


def linha_do_tempo(itens, ano0=1670, ano1=1960, larg=174):
    """Barras de vida de cada compositor numa linha do tempo. itens: (nome, nasc, morte, cor)."""
    esc = (larg - 8) / (ano1 - ano0)
    p = []
    alt = 12 + len(itens) * 13
    for ano in range((ano0 // 50 + 1) * 50, ano1, 50):
        x = 4 + (ano - ano0) * esc
        p.append(f'<line x1="{x:.1f}" y1="4" x2="{x:.1f}" y2="{alt - 4}" stroke="#bfae8f" stroke-width="0.25" stroke-dasharray="1 1.2"/>')
        p.append(f'<text x="{x:.1f}" y="{alt - 0.5}" text-anchor="middle" class="svg-rotulo">{ano}</text>')
    for k, (nome, a, b, cor) in enumerate(itens):
        y = 8 + k * 13
        x0, x1 = 4 + (a - ano0) * esc, 4 + (b - ano0) * esc
        p.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="5" rx="2.5" fill="{cor}" fill-opacity="0.7" stroke="#5b4632" stroke-width="0.25"/>')
        p.append(f'<text x="{x0:.1f}" y="{y - 1.2}" class="svg-rotulo" style="font-style:normal;fill:#3d3127">{nome} ({a}–{b})</text>')
    return (f'<svg viewBox="0 0 {larg} {alt}" style="width:{larg}mm;height:{alt}mm;display:block;margin:0 auto" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(p) + "</svg>")
