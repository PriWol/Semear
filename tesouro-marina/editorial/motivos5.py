"""Motivos do Volume 4 (instrumentos, notas e bichos da música), pintados com o motor de aquarela.
Padrão: 600 × 600 px (≈ 5 cm a 300 dpi)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf, densify
from motivos2 import _ret

S = 600
SEPIA = "#5b4632"


def _espelha(meia):
    """Polígono simétrico a partir da metade direita (de cima para baixo), em torno de x = 300."""
    esq = meia[::-1].copy()
    esq[:, 0] = 600 - esq[:, 0]
    return np.vstack([meia, esq])


def _gira(pts, graus, cx=300, cy=300):
    t = math.radians(graus)
    c, s = math.cos(t), math.sin(t)
    p = np.asarray(pts, float) - (cx, cy)
    return np.stack([cx + c * p[:, 0] - s * p[:, 1], cy + s * p[:, 0] + c * p[:, 1]], 1)


def _tubo(linha, w0, w1):
    """Polígono de largura variável ao longo de uma linha (pescoço, tromba, cauda)."""
    p = np.asarray(linha, float)
    d = np.gradient(p, axis=0)
    n = np.stack([-d[:, 1], d[:, 0]], 1)
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    w = np.linspace(w0, w1, len(p))[:, None] / 2
    return np.vstack([p + n * w, (p - n * w)[::-1]])


def _haste(a, p0, p1, larg, cor, op=0.8):
    a.stroke([p0, p1], cor, width=larg, opacity=op, taper=False)


# ------------------------------------------------------------------ cordas

def _corpo_violino(esc=1.0):
    k = esc
    meia = np.vstack([bezier((300, 215), (372, 205), (410, 272), (372, 312)),
                      bezier((372, 312), (345, 336), (335, 352), (366, 378)),
                      bezier((366, 378), (428, 412), (404, 498 * k), (300, 498 * k))])
    return _espelha(meia)


def violino(seed=501, cor="#b5703a", cor2="#8f4f26", esc=1.0):
    a = Aquarela(S, S, seed=seed)
    # arco atrás
    a.stroke([(70, 545), (545, 120)], "#8a6a44", width=7, opacity=0.8, taper=False)
    a.stroke([(78, 556), (553, 131)], "#efe6cf", width=4, opacity=0.65, taper=False)
    # braço e voluta
    a.wash(_ret(287, 70, 313, 235, 3), "#4a3322", 0.7, edge=1.0, outline=0.4)
    a.wash(ellipse(300, 52, 22, 26), "#8f4f26", 0.6, edge=1.0, outline=0.4)
    a.wash(_ret(278, 62, 322, 80, 3), "#4a3322", 0.7, edge=1.0, outline=0.4)
    corpo = _corpo_violino(esc)
    a.wash(corpo, cor, 0.6, color2=cor2, edge=1.1, light=(260, 330, 38), shade=(1, 0.4, 0.5), outline=0.45)
    for sgn in (-1, 1):   # cavas em f
        x = 300 + sgn * 38
        a.stroke(bezier((x - sgn * 4, 330), (x + sgn * 8, 350), (x - sgn * 8, 380), (x + sgn * 2, 408)), "#3a2a1c", width=7, opacity=0.8)
    a.wash(_ret(262, 392, 338, 402, 3), "#e8d7a0", 0.6, edge=1.0, outline=0.3)   # cavalete
    for k in range(4):
        x = 292 + k * 5.4
        a.stroke([(x, 90), (x, 485)], "#f1ead6", width=1.6, opacity=0.8, taper=False)
    a.wash(ellipse(300, 470, 24, 16), "#3a2a1c", 0.7, edge=1.0)   # queixeira
    return a


def violoncelo():
    a = Aquarela(S, S, seed=502)
    a.stroke([(40, 565), (560, 565)], "#8a6a44", width=7, opacity=0.8, taper=False)   # arco no chão
    a.stroke([(48, 576), (552, 576)], "#efe6cf", width=4, opacity=0.65, taper=False)
    a.wash(_ret(285, 40, 315, 235, 3), "#3a2718", 0.75, edge=1.0, outline=0.4)
    a.wash(ellipse(300, 28, 24, 30), "#7d4020", 0.65, edge=1.0, outline=0.4)
    corpo = _corpo_violino(1.0)
    corpo[:, 1] = 215 + (corpo[:, 1] - 215) * 1.05
    a.wash(corpo, "#a04c26", 0.65, color2="#6f3418", edge=1.1, light=(250, 320, 38), shade=(1, 0.4, 0.5), outline=0.45)
    for sgn in (-1, 1):
        x = 300 + sgn * 38
        a.stroke(bezier((x - sgn * 4, 330), (x + sgn * 8, 350), (x - sgn * 8, 380), (x + sgn * 2, 408)), "#2c2018", width=7, opacity=0.8)
    a.wash(_ret(262, 392, 338, 402, 3), "#e8d7a0", 0.6, edge=1.0, outline=0.3)
    for k in range(4):
        x = 292 + k * 5.4
        a.stroke([(x, 60), (x, 470)], "#f1ead6", width=1.6, opacity=0.8, taper=False)
    a.stroke([(300, 520), (300, 556)], "#8a6a44", width=6, opacity=0.9, taper=False)   # espigão
    return a


def harpa():
    a = Aquarela(S, S, seed=503)
    coluna = _ret(430, 120, 466, 520, 4)
    a.wash(coluna, "#c9963f", 0.6, color2="#a87a2a", edge=1.1, outline=0.45)
    a.wash(np.array([(150, 520), (150, 330), (205, 300), (205, 520)], float), "#b8802e", 0.55, edge=1.0, outline=0.4)
    a.wash(np.vstack([bezier((466, 125), (400, 55), (290, 70), (150, 330)), [(205, 305), (466, 160)]]), "#d9aa4a", 0.6, edge=1.0, outline=0.45)
    for k in range(9):
        t = k / 8
        x = 205 + (440 - 205) * t
        ytop = 305 - (305 - 140) * t - 18 * math.sin(math.pi * t)
        a.stroke([(x, ytop + 24), (x, 515)], "#7a6a52", width=2.6, opacity=0.8, taper=False)
    a.wash(_ret(140, 515, 480, 545, 5), "#8f6a30", 0.6, edge=1.0, outline=0.4)
    return a


def piano():
    a = Aquarela(S, S, seed=504)
    a.wash(np.array([(90, 250), (510, 250), (540, 150), (120, 150)], float), "#3b2f2b", 0.7, edge=1.0, outline=0.4)
    a.wash(_ret(90, 250, 510, 340, 4), "#4a3a34", 0.7, edge=1.0, outline=0.4)
    a.wash(_ret(100, 340, 500, 470, 2), "#f3ecd8", 0.35, edge=1.0, outline=0.45)
    for k in range(1, 8):
        x = 100 + k * 50
        a.stroke([(x, 340), (x, 470)], SEPIA, width=2.4, opacity=0.7, taper=False)
    for k in (0, 1, 3, 4, 5):
        x = 100 + (k + 1) * 50 - 16
        a.wash(_ret(x, 340, x + 32, 420, 3), "#2c2320", 0.85, edge=1.0)
    a.wash(_ret(150, 470, 450, 500, 4), "#4a3a34", 0.7, edge=1.0, outline=0.4)
    return a


# ------------------------------------------------------------------ madeiras e metais

def flauta():
    a = Aquarela(S, S, seed=505)
    tubo = _gira(_ret(40, 285, 560, 315, 14), -22)
    a.wash(tubo, "#aab7c4", 0.55, color2="#d2dae2", edge=1.1, light=(300, 270, 40), outline=0.45)
    for k in range(6):
        t = (120 + k * 70)
        p = _gira(np.array([(t, 300)], float), -22)[0]
        a.wash(ellipse(p[0], p[1] + 2, 15, 15, n=36), "#7f8d9b", 0.6, edge=1.0, outline=0.4)
    p = _gira(np.array([(90, 300)], float), -22)[0]
    a.wash(ellipse(p[0], p[1], 20, 12, n=36), "#5e6b78", 0.7, edge=1.0)
    return a


def clarinete():
    a = Aquarela(S, S, seed=506)
    tubo = _gira(_ret(60, 282, 440, 318, 8), -35)
    sino = _gira(np.array([(430, 280), (500, 250), (510, 350), (430, 320)], float), -35)
    a.wash(tubo, "#3e3029", 0.75, color2="#5a463a", edge=1.1, outline=0.4, light=(280, 280, 30))
    a.wash(sino, "#3e3029", 0.75, edge=1.0, outline=0.4)
    for k in range(5):
        p = _gira(np.array([(130 + k * 62, 300)], float), -35)[0]
        a.wash(ellipse(p[0], p[1], 11, 11, n=30), "#c3ccd4", 0.65, edge=1.0, outline=0.4)
    bico = _gira(np.array([(30, 285), (70, 290), (70, 310), (30, 316)], float), -35)
    a.wash(bico, "#6b5a46", 0.7, edge=1.0, outline=0.4)
    return a


def trompete():
    a = Aquarela(S, S, seed=507)
    ouro, ouro2 = "#d4a83c", "#b8862e"
    a.stroke(np.vstack([bezier((90, 330), (90, 250), (200, 250), (200, 330)), bezier((200, 330), (200, 390), (420, 390), (420, 330))]),
             ouro, width=22, opacity=0.8, taper=False)
    a.stroke(np.vstack([bezier((90, 330), (90, 410), (130, 440), (200, 440)), [(420, 440)]]), ouro2, width=22, opacity=0.8, taper=False)
    a.stroke([(420, 330), (420, 440)], ouro, width=22, opacity=0.8, taper=False)
    sino = np.array([(420, 300), (540, 220), (545, 460), (420, 350)], float)
    a.wash(densify(sino, 120), ouro, 0.6, color2=ouro2, edge=1.1, light=(480, 300, 30), outline=0.45)
    for x in (230, 270, 310):
        a.stroke([(x, 270), (x, 345)], "#8f6a30", width=10, opacity=0.8, taper=False)
        a.wash(ellipse(x, 262, 12, 8, n=24), "#efe0b0", 0.7, edge=1.0, outline=0.3)
    a.wash(ellipse(70, 330, 22, 16, n=30), "#8f6a30", 0.7, edge=1.0)
    return a


def trompa():
    a = Aquarela(S, S, seed=508)
    ouro, ouro2 = "#d4a83c", "#b8862e"
    t = np.linspace(0, 2.6 * 2 * math.pi, 220)
    r = 60 + t * 11.5
    esp = np.stack([260 + r * np.cos(t), 320 + r * np.sin(t) * 0.92], 1)
    a.stroke(esp, ouro, width=24, opacity=0.8, taper=False)
    a.stroke(esp[::2] + (0, 6), ouro2, width=8, opacity=0.5, taper=False)
    fim = esp[-1]
    sino = np.vstack([[fim + (-20, -30)], bezier(fim + (-20, -30), (fim[0] + 70, fim[1] - 90), (fim[0] + 120, fim[1] + 40), (fim[0] - 10, fim[1] + 70))])
    a.wash(densify(sino, 120), ouro, 0.6, color2=ouro2, edge=1.1, light=(fim[0] + 40, fim[1], 24), outline=0.45)
    return a


# ------------------------------------------------------------------ percussão

def pandeiro():
    a = Aquarela(S, S, seed=509)
    a.wash(ellipse(300, 300, 240, 240), "#9a6a3a", 0.6, color2="#7d5026", edge=1.1, outline=0.45)
    a.wash(ellipse(300, 300, 205, 205), "#efe3c4", 0.5, edge=1.0, outline=0.45, light=(240, 240, 70))
    for k in range(6):
        ang = k * math.pi / 3 + 0.25
        x, y = 300 + 222 * math.cos(ang), 300 + 222 * math.sin(ang)
        a.wash(ellipse(x, y, 30, 12, rot=ang + math.pi / 2, n=36), "#b9c3cc", 0.65, edge=1.0, outline=0.4)
        a.wash(ellipse(x, y, 8, 8, n=20), "#6f7a84", 0.7, edge=1.0)
    return a


def triangulo():
    a = Aquarela(S, S, seed=510)
    a.stroke(np.vstack([[(120, 470)], [(480, 470)], [(300, 150)], [(120, 470)]]), "#9aa8b5", width=20, opacity=0.8, taper=False)
    a.stroke([(125, 468), (478, 468), (302, 156)], "#d6dde4", width=7, opacity=0.65, taper=False)
    a.stroke(bezier((300, 150), (300, 100), (320, 70), (330, 60)), "#8a6a44", width=4, opacity=0.8, taper=False)
    a.stroke([(450, 530), (240, 330)], "#8a6a44", width=9, opacity=0.85)
    return a


def chocalho():
    a = Aquarela(S, S, seed=511)
    for cx, cor, c2, ang in ((210, "#c0716b", "#d98f84", -14), (390, "#5f8f8a", "#8fb5ae", 14)):
        cab = _gira(ellipse(cx, 220, 85, 110, n=100), ang, cx, 330)
        a.wash(cab, cor, 0.6, color2=c2, edge=1.1, light=(cx - 25, 190, 24), outline=0.45, shade=(1, 0.3, 0.5))
        cabo = _gira(_ret(cx - 13, 320, cx + 13, 520, 6), ang, cx, 330)
        a.wash(cabo, "#8a6a44", 0.7, edge=1.0, outline=0.4)
        for k in range(3):
            p = _gira(np.array([(cx - 50 + k * 50, 215 + 20 * math.sin(k))], float), ang, cx, 330)[0]
            a.wash(ellipse(p[0], p[1], 9, 9, n=20), "#f3ecd8", 0.7, edge=1.0)
    return a


def xilofone():
    a = Aquarela(S, S, seed=512)
    cores = ["#c43a2e", "#d8803a", "#e8b830", "#7f9a52", "#5f8f8a", "#4f74a8", "#8a6f9e"]
    for k, cor in enumerate(cores):
        x = 110 + k * 58
        alt = 330 - k * 24
        a.wash(_ret(x, 150 + k * 12, x + 46, 150 + k * 12 + alt - 30, 6), cor, 0.6, edge=1.1, outline=0.4)
        a.wash(ellipse(x + 23, 170 + k * 12, 5, 5, n=16), "#f3ecd8", 0.7, edge=1.0)
    a.stroke([(90, 190), (510, 400)], "#8a6a44", width=8, opacity=0.8, taper=False)
    a.stroke([(100, 380), (500, 380)], "#8a6a44", width=8, opacity=0.5, taper=False)
    for p0, p1 in (((120, 560), (210, 470)), ((520, 560), (410, 470))):
        a.stroke([p0, p1], "#8a6a44", width=8, opacity=0.8)
    return a


def tambor_caixa():   # tímpano
    a = Aquarela(S, S, seed=513)
    cuba = np.vstack([bezier((100, 300), (100, 450), (200, 540), (300, 540)), bezier((300, 540), (400, 540), (500, 450), (500, 300))])
    a.wash(cuba, "#b8802e", 0.6, color2="#8f5a26", edge=1.1, shade=(1, 0.3, 0.5), outline=0.45)
    a.wash(ellipse(300, 300, 200, 60), "#efe6cf", 0.4, edge=1.0, outline=0.45)
    a.stroke([(420, 140), (360, 270)], "#8a6a44", width=9, opacity=0.8)
    a.wash(ellipse(425, 135, 22, 22, n=30), "#efe0b0", 0.7, edge=1.0, outline=0.4)
    return a


# ------------------------------------------------------------------ notas

def seminima():
    a = Aquarela(S, S, seed=520)
    a.wash(ellipse(250, 450, 95, 70, rot=-0.45), "#4b3b5a", 0.8, color2="#6c5880", edge=1.1, outline=0.3)
    a.stroke([(335, 425), (335, 100)], "#4b3b5a", width=16, opacity=0.85, taper=False)
    return a


def colcheias():
    a = Aquarela(S, S, seed=521)
    for x in (170, 400):
        a.wash(ellipse(x, 450, 80, 58, rot=-0.45), "#4b3b5a", 0.8, color2="#6c5880", edge=1.1, outline=0.3)
        a.stroke([(x + 72, 430), (x + 72, 120)], "#4b3b5a", width=14, opacity=0.85, taper=False)
    a.wash(np.array([(242, 118), (472, 118), (472, 180), (242, 180)], float), "#4b3b5a", 0.8, edge=1.0)
    return a


# ------------------------------------------------------------------ bichos

def leao():
    a = Aquarela(S, S, seed=530)
    juba = polar(300, 300, lambda t: 250 + 24 * math.sin(11 * t) + 10 * math.sin(5 * t + 1))
    a.wash(juba, "#c9812e", 0.6, color2="#a8601e", edge=1.1, outline=0.45, shade=(1, 0.3, 0.4))
    a.wash(ellipse(300, 315, 150, 160), "#e8bf72", 0.6, color2="#d9a24a", edge=1.1, outline=0.45, light=(260, 260, 40))
    for sgn in (-1, 1):
        a.wash(ellipse(300 + sgn * 120, 160, 38, 38, n=40), "#d9a24a", 0.6, edge=1.0, outline=0.4)
        a.wash(ellipse(300 + sgn * 56, 285, 17, 12, n=30), "#3b2c1e", 0.8, edge=1.0)
        a.stroke([(300 + sgn * 78, 255), (300 + sgn * 38, 262)], SEPIA, width=5, opacity=0.7)
    a.wash(np.array([(262, 340), (338, 340), (300, 385)], float), "#7a4a3a", 0.8, edge=1.0, outline=0.4)
    a.stroke(bezier((300, 385), (300, 410), (260, 425), (235, 405)), SEPIA, width=5, opacity=0.8)
    a.stroke(bezier((300, 385), (300, 410), (340, 425), (365, 405)), SEPIA, width=5, opacity=0.8)
    return a


def elefante():
    a = Aquarela(S, S, seed=531)
    cz, cz2 = "#9aa3ad", "#7d8791"
    a.wash(ellipse(215, 290, 70, 95, rot=0.15), "#b5939a", 0.55, color2="#8f8a96", edge=1.1, outline=0.45)   # orelha, atrás da cabeça
    for x in (200, 265, 390, 455):
        a.wash(_ret(x - 28, 360, x + 28, 525, 14), cz2, 0.75, edge=1.0, outline=0.4)
    a.wash(ellipse(335, 315, 185, 130), cz, 0.65, color2=cz2, edge=1.1, outline=0.45, shade=(1, 0.5, 0.4), light=(290, 270, 40))
    a.wash(ellipse(170, 285, 82, 78), cz, 0.65, edge=1.1, outline=0.45)
    tromba = _tubo(bezier((110, 305), (60, 370), (60, 450), (105, 485)), 46, 22)
    a.wash(tromba, cz, 0.65, edge=1.1, outline=0.45)
    a.wash(ellipse(140, 268, 7, 7, n=16), "#2c2320", 0.85, edge=1.0)
    a.stroke(bezier((120, 330), (95, 345), (82, 348), (72, 346)), "#efe6cf", width=11, opacity=0.9)
    a.stroke(bezier((510, 290), (545, 330), (548, 400), (528, 435)), cz2, width=6, opacity=0.8)
    return a


def cisne():
    a = Aquarela(S, S, seed=532)
    a.wash(ellipse(300, 480, 270, 45), "#b8cfe0", 0.45, color2="#8fb0cc", edge=1.0, layers=3)
    corpo = np.vstack([bezier((165, 405), (195, 500), (410, 500), (480, 380)), bezier((480, 380), (505, 320), (460, 295), (420, 330)),
                       bezier((420, 330), (360, 385), (240, 365), (165, 405))])
    a.wash(densify(corpo, 160), "#eef0f4", 0.6, color2="#c4d0de", edge=1.1, outline=0.55, shade=(1, 0.6, 0.5))
    pesc = _tubo(np.vstack([bezier((215, 385), (120, 360), (120, 250), (185, 215)), bezier((185, 215), (245, 185), (225, 120), (180, 125))]), 50, 30)
    a.wash(densify(pesc, 200), "#eef0f4", 0.6, color2="#c4d0de", edge=1.1, outline=0.55)
    a.wash(np.array([(160, 112), (105, 130), (162, 142)], float), "#d9803a", 0.75, edge=1.0, outline=0.4)
    a.wash(ellipse(178, 120, 5, 5, n=16), "#2c2320", 0.85, edge=1.0)
    return a


def cuco():
    a = Aquarela(S, S, seed=533)
    a.stroke(bezier((40, 470), (200, 450), (400, 490), (560, 460)), "#7a5a3a", width=14, opacity=0.8)
    a.wash(ellipse(300, 330, 120, 95, rot=-0.3), "#8a96a4", 0.6, color2="#a9b3be", edge=1.1, outline=0.45, shade=(1, 0.5, 0.4))
    a.wash(ellipse(205, 260, 55, 52), "#8a96a4", 0.6, edge=1.1, outline=0.45)
    a.wash(np.array([(155, 255), (105, 275), (155, 285)], float), "#c9a23a", 0.7, edge=1.0, outline=0.4)
    a.wash(ellipse(200, 250, 6, 6, n=16), "#2c2320", 0.85, edge=1.0)
    a.wash(leaf((380, 370), (560, 430), 70, asym=0.1), "#6f7c8a", 0.6, edge=1.0, outline=0.4)
    a.wash(ellipse(300, 345, 70, 45, rot=-0.3), "#d8c9a8", 0.5, edge=1.0)
    for x in (270, 330):
        a.stroke([(x, 410), (x, 460)], "#c9812e", width=7, opacity=0.8, taper=False)
    return a


def gato():
    a = Aquarela(S, S, seed=534)
    a.stroke(bezier((420, 510), (570, 520), (570, 330), (480, 290)), "#d9803a", width=34, opacity=0.8, taper=False)
    a.wash(ellipse(310, 400, 140, 130), "#d9903a", 0.6, color2="#c4712a", edge=1.1, outline=0.45, shade=(1, 0.5, 0.4))
    a.wash(ellipse(250, 225, 95, 85), "#d9903a", 0.6, color2="#c4712a", edge=1.1, outline=0.45)
    for sgn in (-1, 1):
        a.wash(np.array([(250 + sgn * 85, 195), (250 + sgn * 70, 105), (250 + sgn * 20, 160)], float), "#d9903a", 0.6, edge=1.0, outline=0.45)
        a.wash(ellipse(250 + sgn * 36, 222, 13, 17, n=24), "#9fc07a", 0.7, edge=1.0)
        a.wash(ellipse(250 + sgn * 36, 222, 4, 14, n=20), "#2c2320", 0.85, edge=1.0)
    a.wash(np.array([(240, 252), (260, 252), (250, 264)], float), "#b86a6a", 0.8, edge=1.0)
    for sgn in (-1, 1):
        a.stroke([(250 + sgn * 18, 262), (250 + sgn * 70, 252)], SEPIA, width=2.4, opacity=0.7)
        a.stroke([(250 + sgn * 18, 268), (250 + sgn * 70, 276)], SEPIA, width=2.4, opacity=0.7)
    return a


def lobo():
    a = Aquarela(S, S, seed=535)
    cz, cz2 = "#8a8a90", "#62626a"
    for sgn in (-1, 1):
        a.wash(np.array([(300 + sgn * 70, 190), (300 + sgn * 150, 40), (300 + sgn * 215, 215)], float), cz2, 0.65, edge=1.0, outline=0.5)
        a.wash(np.array([(300 + sgn * 95, 185), (300 + sgn * 150, 85), (300 + sgn * 185, 195)], float), "#c4a8a0", 0.5, edge=1.0)
    cab = polar(300, 300, lambda t: 175 + 18 * math.sin(7 * t) + 8 * math.sin(3 * t))
    cab[:, 1] = 300 + (cab[:, 1] - 300) * 0.92
    a.wash(cab, cz, 0.65, color2=cz2, edge=1.1, outline=0.5, shade=(1, 0.4, 0.4))
    a.wash(ellipse(300, 400, 85, 100), "#cdc7b9", 0.6, color2="#b5ae9e", edge=1.0, outline=0.45)
    a.wash(ellipse(300, 330, 30, 22, n=30), "#2c2320", 0.88, edge=1.0)
    for sgn in (-1, 1):
        a.wash(ellipse(300 + sgn * 78, 255, 24, 13, rot=sgn * 0.35, n=30), "#e0b040", 0.85, edge=1.0, outline=0.3)
        a.wash(ellipse(300 + sgn * 78, 255, 6, 10, n=16), "#2c2320", 0.9, edge=1.0)
        a.stroke([(300 + sgn * 108, 225), (300 + sgn * 52, 238)], "#2c2320", width=6, opacity=0.8)
    a.stroke([(300, 350), (300, 410)], SEPIA, width=4, opacity=0.8)
    a.stroke(bezier((300, 410), (300, 450), (252, 460), (232, 440)), SEPIA, width=5, opacity=0.8)
    a.stroke(bezier((300, 410), (300, 450), (348, 460), (368, 440)), SEPIA, width=5, opacity=0.8)
    a.wash(np.array([(272, 436), (284, 470), (296, 436)], float), "#f6f1e6", 0.8, edge=1.0, outline=0.3)
    return a


def canguru():
    a = Aquarela(S, S, seed=536)
    cor, c2 = "#b88a56", "#946a3a"
    cauda = _tubo(bezier((235, 450), (150, 500), (80, 520), (40, 505)), 70, 10)
    a.wash(cauda, c2, 0.65, edge=1.0, outline=0.45)
    a.wash(ellipse(295, 360, 100, 150, rot=0.2), cor, 0.65, color2=c2, edge=1.1, outline=0.45, shade=(1, 0.4, 0.4))
    a.wash(ellipse(275, 470, 70, 52, rot=-0.2), c2, 0.65, edge=1.0, outline=0.45)       # coxa
    a.wash(np.array([(300, 505), (440, 505), (448, 535), (290, 535)], float), c2, 0.7, edge=1.0, outline=0.45)   # pé
    a.wash(ellipse(350, 175, 52, 62, rot=0.25), cor, 0.65, edge=1.1, outline=0.45)
    a.wash(leaf((355, 150), (400, 30), 40), cor, 0.65, edge=1.0, outline=0.45)
    a.wash(leaf((330, 145), (315, 30), 40), c2, 0.65, edge=1.0, outline=0.45)
    a.wash(ellipse(392, 205, 15, 11, n=24), "#5a3a2a", 0.8, edge=1.0)
    a.wash(ellipse(365, 160, 5, 5, n=16), "#2c2320", 0.85, edge=1.0)
    a.wash(ellipse(320, 395, 55, 62, rot=0.2), "#e8d1a8", 0.6, edge=1.0, outline=0.4)    # bolsa
    a.wash(ellipse(330, 372, 18, 24, rot=0.2), "#a87a46", 0.7, edge=1.0, outline=0.4)    # filhote
    a.wash(leaf((330, 360), (345, 310), 20), "#a87a46", 0.7, edge=1.0, outline=0.4)
    a.stroke(bezier((385, 275), (425, 300), (435, 320), (415, 338)), c2, width=11, opacity=0.85)
    return a


def burro():
    a = Aquarela(S, S, seed=537)
    cz, cz2 = "#a89a8a", "#8a7d70"
    cabeca = np.vstack([bezier((260, 200), (300, 150), (390, 160), (410, 230)), bezier((410, 230), (440, 330), (470, 400), (440, 450)),
                        bezier((440, 450), (410, 490), (330, 490), (300, 440)), bezier((300, 440), (260, 380), (220, 300), (260, 200))])
    a.wash(densify(cabeca, 200), cz, 0.6, color2=cz2, edge=1.1, outline=0.5, shade=(1, 0.4, 0.4))
    a.wash(leaf((300, 190), (255, 40), 58), cz, 0.6, edge=1.0, outline=0.45)
    a.wash(leaf((350, 180), (400, 35), 58), cz2, 0.6, edge=1.0, outline=0.45)
    a.wash(ellipse(425, 430, 45, 40), "#e3d6c2", 0.6, edge=1.0, outline=0.4)
    a.wash(ellipse(430, 420, 10, 8, n=20), "#3b2c1e", 0.8, edge=1.0)
    a.wash(ellipse(335, 255, 12, 12, n=20), "#2c2320", 0.85, edge=1.0)
    a.stroke(bezier((250, 200), (280, 130), (330, 125), (345, 135)), "#5a4a3a", width=12, opacity=0.8)
    return a


def cachorro():
    a = Aquarela(S, S, seed=538)
    cor, c2 = "#b88a56", "#7d5026"
    for sgn in (-1, 1):   # orelhas caídas, atrás da cabeça
        a.wash(ellipse(300 + sgn * 150, 270, 58, 125, rot=sgn * -0.18), c2, 0.65, edge=1.1, outline=0.45)
    a.wash(ellipse(300, 285, 135, 150), cor, 0.65, color2="#a07040", edge=1.1, outline=0.45, shade=(1, 0.4, 0.4))
    a.wash(ellipse(300, 370, 80, 70), "#eadbbc", 0.6, edge=1.0, outline=0.4)
    a.wash(ellipse(300, 335, 34, 24, n=30), "#2c2320", 0.88, edge=1.0)
    for sgn in (-1, 1):
        a.wash(ellipse(300 + sgn * 62, 250, 14, 16, n=24), "#2c2320", 0.88, edge=1.0)
        a.stroke([(300 + sgn * 92, 215), (300 + sgn * 40, 225)], c2, width=7, opacity=0.7)
    a.stroke([(300, 358), (300, 395)], SEPIA, width=4, opacity=0.8)
    a.stroke(bezier((300, 395), (300, 425), (258, 430), (240, 410)), SEPIA, width=4, opacity=0.8)
    a.stroke(bezier((300, 395), (300, 425), (342, 430), (360, 410)), SEPIA, width=4, opacity=0.8)
    a.wash(ellipse(300, 440, 24, 34, n=30), "#d9707a", 0.7, edge=1.0, outline=0.4)
    return a


def oboe():
    a = Aquarela(S, S, seed=514)
    tubo = _gira(_ret(70, 288, 450, 312, 8), -35)
    sino = _gira(np.array([(440, 280), (480, 265), (505, 335), (440, 320)], float), -35)
    a.wash(tubo, "#7a5238", 0.7, color2="#9a6a46", edge=1.1, outline=0.4, light=(280, 280, 30))
    a.wash(sino, "#6b4630", 0.75, edge=1.0, outline=0.4)
    for k in range(5):
        p = _gira(np.array([(140 + k * 60, 300)], float), -35)[0]
        a.wash(ellipse(p[0], p[1], 9, 9, n=30), "#c3ccd4", 0.65, edge=1.0, outline=0.4)
    palheta = _gira(np.array([(25, 292), (72, 296), (72, 304), (25, 302)], float), -35)
    a.wash(palheta, "#d9c48a", 0.7, edge=1.0, outline=0.4)
    return a


def coracao():
    a = Aquarela(S, S, seed=539)
    t = np.linspace(0, 2 * math.pi, 240)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    pts = np.stack([300 + x * 14.5, 285 + y * 14.5], 1)
    a.wash(pts, "#c0463e", 0.6, color2="#d8707a", edge=1.1, outline=0.45, light=(230, 220, 34), shade=(1, 0.5, 0.4))
    return a


MOTIVOS5 = {
    "violino": violino, "violoncelo": violoncelo, "harpa": harpa, "piano": piano, "flauta": flauta,
    "clarinete": clarinete, "trompete": trompete, "trompa": trompa, "pandeiro": pandeiro,
    "triangulo_inst": triangulo, "chocalho": chocalho, "xilofone": xilofone, "timpano": tambor_caixa,
    "seminima": seminima, "colcheias": colcheias, "leao": leao, "elefante": elefante, "cisne": cisne,
    "cuco": cuco, "coracao": coracao, "cachorro": cachorro, "oboe": oboe, "gato": gato, "lobo": lobo, "canguru": canguru, "burro": burro,
}
