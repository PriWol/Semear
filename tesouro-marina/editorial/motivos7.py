"""Motivos do Volume 6 (O livro da natureza): bichinhos, folhas, sementes, água, céu e corpo, pintados com o motor de aquarela.
Mesmo estilo e mesma escala dos motivos anteriores (600 × 600 px, ≈ 5 cm a 300 dpi). Só objetos simples, como em docs/03-ilustracao.md;
os animais maiores e as cenas ficam por conta das pranchas antigas (fontes_v6.py)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf, densify
from motivos2 import _ret

S = 600
CONTORNO = "#5b4632"


def _esp(pts):
    """Espelha uma forma em torno do eixo vertical (x = 300)."""
    p = np.asarray(pts, float).copy()
    p[:, 0] = 600 - p[:, 0]
    return p


def _tra(a, pts, cor, larg=8, op=0.8, taper=False):
    a.stroke(np.asarray(pts, float), cor, width=larg, opacity=op, taper=taper)


def _bez(*seg):
    return np.vstack([bezier(*s) for s in seg])


# ------------------------------------------------------------------ bichinhos

def borboleta(seed=801):
    a = Aquarela(S, S, seed=seed)
    sup = _bez(((312, 290), (360, 150), (470, 80), (530, 140)), ((530, 140), (565, 230), (470, 300), (330, 330)))
    inf = _bez(((322, 322), (430, 315), (525, 385), (470, 475)), ((470, 475), (420, 525), (340, 440), (318, 355)))
    for f in (lambda p: p, _esp):
        a.wash(densify(f(sup), 200), "#e8863a", 0.6, color2="#f0a65a", edge=1.0, outline=0.5, granulation=0.5)
        a.wash(densify(f(inf), 200), "#e5a73e", 0.6, color2="#f2c565", edge=1.0, outline=0.5, granulation=0.5)
        for (x, y, r) in ((470, 165, 26), (440, 235, 18), (440, 425, 22)):
            a.wash(ellipse(*f(np.array([[x, y]]))[0], r, r, n=40), "#fbf3de", 0.7, edge=0.7)
        a.wash(ellipse(*f(np.array([[500, 160]]))[0], 14, 14, n=40), "#3f5f8a", 0.7, edge=0.6)
    a.wash(ellipse(300, 330, 17, 100), "#4a3626", 0.8, edge=0.8, outline=0.4)
    a.wash(ellipse(300, 222, 20, 20, n=40), "#4a3626", 0.85, edge=0.7)
    _tra(a, bezier((292, 214), (276, 160), (250, 120), (232, 104)), "#4a3626", 5, 0.8, True)
    _tra(a, bezier((308, 214), (324, 160), (350, 120), (368, 104)), "#4a3626", 5, 0.8, True)
    return a


def joaninha(seed=811):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 340, 190, 170), "#c43a2e", 0.7, color2="#d8604a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(230, 250, 40))
    a.wash(ellipse(300, 195, 82, 60), "#2b2420", 0.85, edge=0.8, outline=0.3)
    _tra(a, np.array([(300, 175), (300, 505)]), "#2b2420", 6, 0.8)
    for (x, y, r) in ((225, 300, 26), (375, 300, 26), (210, 400, 24), (390, 400, 24), (255, 470, 18), (345, 470, 18)):
        a.wash(ellipse(x, y, r, r, n=40), "#2b2420", 0.9, edge=0.6)
    _tra(a, bezier((268, 150), (240, 100), (215, 75), (190, 62)), "#2b2420", 5, 0.8, True)
    _tra(a, bezier((332, 150), (360, 100), (385, 75), (410, 62)), "#2b2420", 5, 0.8, True)
    return a


def abelha(seed=821):
    a = Aquarela(S, S, seed=seed)
    for (x, rot) in ((270, -0.5), (340, 0.45)):
        a.wash(ellipse(x, 205, 62, 112, rot=rot), "#bcd6ea", 0.4, color2="#dbe9f4", edge=0.9, outline=0.4)
    a.wash(ellipse(325, 340, 160, 112), "#e8b830", 0.7, color2="#f0cf5a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for x in (270, 330, 390):
        a.wash(ellipse(x, 340, 17, 96 - abs(x - 330) * 0.5), "#3a2c20", 0.8, edge=0.7)
    a.wash(ellipse(160, 345, 66, 60), "#3a2c20", 0.85, edge=0.8, outline=0.3)
    a.wash(ellipse(145, 335, 9, 9, n=24), "#fbf3de", 0.8, edge=0.5)
    _tra(a, bezier((486, 340), (506, 340), (520, 340), (536, 340)), "#3a2c20", 9, 0.85, True)
    _tra(a, bezier((130, 296), (110, 250), (96, 232), (80, 222)), "#3a2c20", 5, 0.8, True)
    return a


def formiga(seed=831):
    a = Aquarela(S, S, seed=seed)
    cor = "#6a3a22"
    for (x0, y0, x1, y1, x2, y2) in ((330, 350, 400, 480, 360, 540), (310, 350, 300, 490, 270, 545), (295, 345, 215, 450, 170, 520)):
        _tra(a, _bez(((x0, y0), (x0 + (x1 - x0) * 0.4, y0 + 30), (x1, y1 - 10), (x1, y1)), ((x1, y1), (x1, y1 + 20), (x2, y2 - 10), (x2, y2))), cor, 7, 0.85)
    for (x0, y0, x1, y1, x2, y2) in ((330, 330, 400, 200, 360, 140), (310, 330, 300, 190, 270, 135), (295, 335, 215, 220, 170, 150)):
        _tra(a, _bez(((x0, y0), (x0 + (x1 - x0) * 0.4, y0 - 30), (x1, y1 + 10), (x1, y1)), ((x1, y1), (x1, y1 - 20), (x2, y2 + 10), (x2, y2))), cor, 7, 0.85)
    a.wash(ellipse(445, 345, 95, 72), cor, 0.75, color2="#8a5a38", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(320, 340, 46, 36), cor, 0.8, color2="#8a5a38", edge=1.0, outline=0.5)
    a.wash(ellipse(215, 335, 52, 46), cor, 0.8, color2="#8a5a38", edge=1.0, outline=0.5)
    _tra(a, bezier((180, 310), (140, 270), (120, 240), (100, 232)), cor, 5, 0.85, True)
    _tra(a, bezier((190, 300), (180, 250), (170, 215), (150, 195)), cor, 5, 0.85, True)
    return a


def caracol(seed=841):
    a = Aquarela(S, S, seed=seed)
    pe = _bez(((90, 520), (60, 440), (130, 400), (240, 410)), ((240, 410), (360, 420), (480, 420), (520, 470)), ((520, 470), (540, 520), (420, 535), (300, 535)), ((300, 535), (200, 535), (120, 545), (90, 520)))
    a.wash(densify(pe, 220), "#dcc89c", 0.55, color2="#c8ae78", edge=1.0, outline=0.5)
    _tra(a, bezier((130, 430), (115, 380), (108, 330), (100, 290)), "#c8ae78", 14, 0.8, True)
    _tra(a, bezier((165, 425), (165, 370), (160, 330), (168, 290)), "#c8ae78", 14, 0.8, True)
    for (x, y) in ((100, 285), (168, 285)):
        a.wash(ellipse(x, y, 11, 11, n=24), "#3a2c20", 0.9, edge=0.5)
    a.wash(ellipse(330, 290, 165, 160), "#c98a4a", 0.6, color2="#e0a864", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    t = np.linspace(0, 4.2 * math.pi, 160)
    r = 14 + 130 * t / (4.2 * math.pi)
    _tra(a, np.stack([330 + r * np.cos(t + 0.6), 295 + r * np.sin(t + 0.6)], 1), "#7a4a24", 7, 0.8)
    return a


def aranha(seed=851):
    a = Aquarela(S, S, seed=seed)
    cor = "#4a3626"
    for lado in (1, -1):
        for (yb, ye, xe, ym) in ((330, 190, 90, 200), (350, 285, 60, 270), (375, 400, 75, 420), (395, 520, 125, 520)):
            x0 = 300 + lado * 40
            p = _bez(((x0, yb), (300 + lado * 120, ym - 60), (300 + lado * 190, ym - 70), (300 + lado * 215, ym - 20)),
                     ((300 + lado * 215, ym - 20), (300 + lado * 235, ym + 20), (300 + lado * 232, ye + 40), (300 + lado * (300 - xe), ye + 60 if ye < 300 else ye)))
            _tra(a, p, cor, 7, 0.85)
    a.wash(ellipse(300, 395, 82, 100), cor, 0.8, color2="#6a5038", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(300, 285, 46, 40), cor, 0.85, color2="#6a5038", edge=1.0, outline=0.5)
    for dx in (-14, 14):
        a.wash(ellipse(300 + dx, 276, 8, 8, n=24), "#fbf3de", 0.8, edge=0.5)
    return a


def minhoca(seed=861):
    a = Aquarela(S, S, seed=seed)
    x = np.linspace(90, 510, 120)
    y = 340 + 70 * np.sin((x - 90) / 420 * 2.6 * math.pi)
    caminho = np.stack([x, y], 1)
    a.stroke(caminho, "#d98a80", width=46, opacity=0.9, taper=False)
    a.stroke(caminho[:60], "#c46f66", width=46, opacity=0.35, taper=False)
    k = 36
    d = np.gradient(caminho, axis=0)
    nv = np.stack([-d[:, 1], d[:, 0]], 1)
    nv /= np.linalg.norm(nv, axis=1, keepdims=True)
    for i in range(6, 118, 9):
        _tra(a, np.array([caminho[i] + nv[i] * 22, caminho[i] - nv[i] * 22]), "#b86a62", 3, 0.45)
    a.wash(ellipse(*caminho[-1], 22, 22, n=40), "#d98a80", 0.85, edge=0.8)
    return a


def lagarta(seed=871):
    a = Aquarela(S, S, seed=seed)
    n = 7
    for i in range(n):
        x = 520 - i * 62
        y = 350 + 28 * math.sin(i * 0.8)
        a.wash(ellipse(x, y, 54, 54, n=60), ("#7aa04a", "#8fb85a")[i % 2], 0.65, color2="#a9c872", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
        _tra(a, np.array([(x - 6, y + 50), (x - 8, y + 80)]), "#4f7a32", 6, 0.8, True)
    a.wash(ellipse(100, 380, 62, 58), "#d8704a", 0.75, color2="#e8946a", edge=1.0, outline=0.5)
    for dy in (-14, 14):
        a.wash(ellipse(82, 370 + dy * 0.2, 7, 7, n=24), "#2b2420", 0.9, edge=0.5)
    _tra(a, bezier((100, 330), (90, 290), (76, 265), (60, 250)), "#4f7a32", 5, 0.8, True)
    _tra(a, bezier((120, 332), (126, 290), (130, 262), (140, 245)), "#4f7a32", 5, 0.8, True)
    return a


def casulo(seed=881):
    a = Aquarela(S, S, seed=seed)
    _tra(a, np.array([(130, 120), (470, 120)]), "#7a5a3a", 20, 0.9)
    _tra(a, np.array([(300, 126), (300, 200)]), "#7a5a3a", 5, 0.85)
    forma = _bez(((300, 200), (380, 210), (400, 330), (340, 430)), ((340, 430), (320, 470), (305, 500), (300, 530)),
                 ((300, 530), (295, 500), (280, 470), (260, 430)), ((260, 430), (200, 330), (220, 210), (300, 200)))
    a.wash(densify(forma, 240), "#a9ac5a", 0.65, color2="#c9c070", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(240, 230, 40))
    for y in (270, 330, 390):
        _tra(a, bezier((250, y), (280, y + 14), (320, y + 14), (350, y)), "#7a8a40", 3, 0.55, True)
    for (x, y) in ((330, 250), (270, 300), (332, 360)):
        a.wash(ellipse(x, y, 8, 8, n=24), "#f0d870", 0.8, edge=0.5)
    return a


def libelula(seed=891):
    a = Aquarela(S, S, seed=seed)
    for (cy, rx, ry) in ((250, 190, 52), (330, 175, 46)):
        for lado in (1, -1):
            a.wash(ellipse(300 + lado * 125, cy + (0 if cy == 250 else 12), rx * 0.62, ry, rot=lado * (-0.12 if cy == 250 else 0.12)), "#a9cfe0", 0.35, color2="#cfe4ee", edge=0.9, outline=0.4)
    a.wash(ellipse(300, 330, 15, 190), "#3f7f8a", 0.8, color2="#5f9fa8", edge=0.9, outline=0.4)
    a.wash(ellipse(300, 195, 30, 28, n=40), "#2f5f6a", 0.85, edge=0.7)
    for dx in (-15, 15):
        a.wash(ellipse(300 + dx, 188, 12, 12, n=30), "#8fd0d8", 0.8, edge=0.6)
    return a


# ------------------------------------------------------------------ folhas e árvore

def _veias(a, base, tip, n=5, abertura=0.55, cor="#4f7a32", larg=3.0, escala=1.0):
    """Nervura central e nervuras laterais de uma folha (base e ponta em pixels)."""
    b, t = np.array(base, float), np.array(tip, float)
    _tra(a, np.array([b, t]), cor, larg + 1.5, 0.7, True)
    d = (t - b)
    comp = np.linalg.norm(d)
    u = d / comp
    nv = np.array([-u[1], u[0]])
    for i in range(1, n + 1):
        f = i / (n + 1) * 0.85
        pt = b + d * f
        alc = comp * 0.22 * escala * math.sin(math.pi * (0.25 + f * 0.7))
        for lado in (1, -1):
            _tra(a, np.array([pt, pt + u * alc * abertura + nv * lado * alc]), cor, larg, 0.55, True)


def folha_carvalho(seed=901):
    a = Aquarela(S, S, seed=seed)
    sv = np.linspace(0, 1, 60)
    larg = 150 * np.sin(np.pi * sv ** 0.8) * (1 + 0.32 * np.cos(2 * np.pi * 3.5 * sv))
    ys = 540 - 470 * sv
    dir_ = np.stack([300 + larg, ys], 1)
    esq = np.stack([300 - larg, ys], 1)[::-1]
    a.wash(densify(np.vstack([dir_, esq]), 260), "#6f9a3a", 0.6, color2="#9cbc5a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _veias(a, (300, 540), (300, 90), n=5, abertura=0.5)
    _tra(a, np.array([(300, 535), (300, 585)]), "#6e4a2a", 8, 0.85, True)
    return a


def folha_bordo(seed=911):
    a = Aquarela(S, S, seed=seed)
    cx, cy = 300, 340
    tips = [(-90, 235), (-90 + 55, 205), (-90 + 112, 150), (-90 - 55, 205), (-90 - 112, 150)]
    tips.sort(key=lambda x: x[0])
    pts = []
    for i, (ang, r) in enumerate(tips):
        a0 = math.radians(ang)
        pts.append((cx + r * math.cos(a0), cy + r * math.sin(a0)))
        nxt = tips[(i + 1) % len(tips)][0] + (360 if i == len(tips) - 1 else 0)
        am = math.radians((ang + nxt) / 2)
        pts.append((cx + 95 * math.cos(am), cy + 95 * math.sin(am)))
    a.wash(densify(np.array(pts), 300), "#d8702a", 0.65, color2="#e8a040", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for ang, r in tips:
        a0 = math.radians(ang)
        _tra(a, np.array([(cx, cy + 10), (cx + (r - 40) * math.cos(a0), cy + (r - 40) * math.sin(a0))]), "#a8481e", 3.5, 0.6, True)
    _tra(a, np.array([(300, 350), (300, 560)]), "#7a4a24", 9, 0.85, True)
    return a


def folha_coracao(seed=921):
    a = Aquarela(S, S, seed=seed)
    forma = _bez(((300, 470), (150, 540), (80, 280), (300, 70)), ((300, 70), (520, 280), (450, 540), (300, 470)))
    a.wash(densify(forma, 240), "#7aa04a", 0.62, color2="#a3c06a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _veias(a, (300, 470), (300, 90), n=4, abertura=0.8)
    _tra(a, np.array([(300, 470), (300, 570)]), "#6e4a2a", 8, 0.85, True)
    return a


def folha_fina(seed=931):
    a = Aquarela(S, S, seed=seed)
    a.wash(leaf((300, 540), (300, 50), 62), "#8fae5a", 0.6, color2="#b4cc7a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _veias(a, (300, 540), (300, 80), n=6, abertura=0.7, escala=0.32)
    return a


def folha_seca(seed=941):
    a = Aquarela(S, S, seed=seed)
    a.wash(leaf((250, 530), (390, 80), 140, asym=0.25), "#b8742a", 0.7, color2="#d49a48", edge=1.0, outline=0.5, granulation=0.8)
    _veias(a, (250, 530), (390, 90), n=5, abertura=0.6, cor="#7a4a1e", escala=0.38)
    a.wash(ellipse(330, 330, 20, 14), "#f5ead0", 0.8, edge=0.6)
    return a


def tronco(seed=951):
    a = Aquarela(S, S, seed=seed)
    esq = _bez(((235, 50), (230, 200), (215, 340), (165, 520)), ((165, 520), (150, 550), (120, 565), (80, 570)))
    dir_ = np.array([(600 - x, y) for x, y in esq])
    forma = np.vstack([esq, np.vstack([dir_[::-1], [(600 - 80, 570)][::-1]])])
    forma = np.vstack([esq, dir_[::-1]])
    a.wash(densify(forma, 260), "#8a6540", 0.65, color2="#a98458", edge=1.0, outline=0.5, granulation=1.0, shade=(1, 0.5, 0.5))
    a.wash(ellipse(300, 54, 66, 18), "#c9a778", 0.7, edge=0.9, outline=0.4)
    for x, (y0, y1) in ((260, (110, 300)), (300, (140, 420)), (335, (110, 340)), (225, (260, 480)), (370, (250, 500))):
        _tra(a, bezier((x, y0), (x - 8, (y0 + y1) / 2 - 20), (x + 8, (y0 + y1) / 2 + 20), (x, y1)), "#5b4026", 4, 0.55, True)
    a.wash(ellipse(285, 330, 22, 34), "#5b4026", 0.7, edge=0.7)
    return a


def raiz_arvore(seed=961):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 90, 240, 40), "#7a5a3a", 0.55, color2="#6e4a2a", edge=1.0, granulation=1.0)
    a.wash(leaf((300, 90), (250, 10), 38), "#7aa04a", 0.6, edge=1.0, outline=0.4)
    a.wash(leaf((300, 90), (352, 20), 38), "#8fae5a", 0.6, edge=1.0, outline=0.4)
    _tra(a, bezier((300, 90), (298, 220), (305, 360), (300, 560)), "#8a6540", 22, 0.9, True)
    for (x1, y1, x2, y2, x3, y3) in ((300, 150, 170, 230, 90, 320), (300, 190, 430, 260, 520, 350), (300, 280, 200, 340, 150, 440),
                                    (300, 320, 410, 380, 470, 470), (300, 420, 250, 470, 215, 540)):
        _tra(a, bezier((x1, y1), ((x1 + x2) / 2, y1 + 10), ((x2 + x3) / 2, y2), (x3, y3)), "#8a6540", 11, 0.85, True)
    return a


def pinha(seed=971):
    a = Aquarela(S, S, seed=seed)
    for i, y in enumerate(range(520, 90, -42)):
        larg = 130 * math.sin(math.pi * (y - 70) / 480) + 25
        n = max(3, int(larg / 22))
        for k in range(n):
            x = 300 + (k - (n - 1) / 2) * (larg * 2 / n) + (i % 2) * 12
            a.wash(ellipse(x, y, larg / n * 1.6, 28), ("#8a5a32", "#a8743e")[(i + k) % 2], 0.6, edge=0.9, outline=0.5, granulation=0.8)
    _tra(a, np.array([(300, 95), (300, 50)]), "#6e4a2a", 9, 0.85, True)
    return a


def flor_rosa(seed=981):
    a = Aquarela(S, S, seed=seed)
    _tra(a, bezier((300, 590), (300, 480), (290, 400), (300, 320)), "#6f9a3a", 9, 0.85, True)
    for ang in np.linspace(-2.5, -0.6, 5):
        tip = (300 + 190 * math.cos(ang), 300 + 190 * math.sin(ang))
        a.wash(leaf((300, 310), tip, 92), "#e08ab4", 0.55, color2="#eeaecc", edge=1.0, layers=2, outline=0.4)
    a.wash(ellipse(300, 305, 48, 48, n=60), "#f0cf5a", 0.75, color2="#f7e08a", edge=0.9, outline=0.3)
    a.wash(leaf((300, 460), (180, 410), 40), "#7aa04a", 0.6, edge=1.0, outline=0.4)
    a.wash(leaf((300, 480), (420, 430), 40), "#8fae5a", 0.6, edge=1.0, outline=0.4)
    return a


# ------------------------------------------------------------------ sementes e plantas

def feijao(seed=1001):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 310, 185, 112, rot=-0.25), "#8a4a32", 0.7, color2="#a8644a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(220, 250, 40), granulation=0.5)
    a.wash(ellipse(250, 330, 36, 14, rot=-0.25), "#efe3c8", 0.8, edge=0.7)
    a.wash(ellipse(360, 260, 40, 16, rot=-0.25), "#c78a70", 0.5, edge=0.8, soft=2)
    return a


def feijao_raiz(seed=1011):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(250, 190, 150, 92, rot=-0.25), "#8a4a32", 0.7, color2="#a8644a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _tra(a, bezier((330, 235), (390, 300), (350, 400), (400, 540)), "#dccaa0", 20, 0.95, True)
    for (x, y, dx, dy) in ((372, 330, 70, 20), (366, 390, -40, 30), (390, 450, 60, 25), (392, 500, -50, 20)):
        _tra(a, np.array([(x, y), (x + dx, y + dy)]), "#dccaa0", 7, 0.9, True)
    return a


def feijao_broto(seed=1021):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(240, 470, 120, 76, rot=-0.2), "#8a4a32", 0.7, color2="#a8644a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _tra(a, bezier((300, 440), (330, 330), (300, 260), (330, 160)), "#8fae5a", 18, 0.9, True)
    a.wash(leaf((330, 170), (210, 100), 56), "#7aa04a", 0.6, color2="#a3c06a", edge=1.0, outline=0.45)
    a.wash(leaf((330, 170), (450, 90), 56), "#8fae5a", 0.6, color2="#b4cc7a", edge=1.0, outline=0.45)
    _tra(a, bezier((190, 520), (150, 560), (130, 575), (110, 590)), "#dccaa0", 12, 0.9, True)
    return a


def vaso(seed=1031):
    a = Aquarela(S, S, seed=seed)
    corpo = np.array([(165, 260), (435, 260), (400, 540), (200, 540)], float)
    a.wash(densify(corpo, 160), "#c0703e", 0.65, color2="#d89060", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), granulation=0.8)
    a.wash(densify(_ret(140, 200, 460, 270, 10), 160), "#cc7e4a", 0.65, color2="#e0a070", edge=1.0, outline=0.5)
    a.wash(ellipse(300, 205, 150, 22), "#6e4a2a", 0.7, edge=0.9, granulation=1.0)
    return a


def plantinha(seed=1041):
    a = Aquarela(S, S, seed=seed)
    _tra(a, bezier((300, 330), (296, 280), (304, 230), (300, 160)), "#6f9a3a", 12, 0.9, True)
    for (tip, w, c) in (((180, 190), 48, "#7aa04a"), ((425, 170), 52, "#8fae5a"), ((200, 280), 42, "#8fae5a"), ((410, 270), 44, "#7aa04a")):
        a.wash(leaf((300, 300 if tip[1] > 240 else 200), tip, w), c, 0.6, color2="#b4cc7a", edge=1.0, outline=0.45)
    a.wash(leaf((300, 170), (300, 70), 40), "#9cbc5a", 0.6, edge=1.0, outline=0.45)
    corpo = np.array([(190, 400), (410, 400), (385, 575), (215, 575)], float)
    a.wash(densify(corpo, 160), "#c0703e", 0.65, color2="#d89060", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(densify(_ret(170, 350, 430, 405, 8), 160), "#cc7e4a", 0.65, edge=1.0, outline=0.5)
    a.wash(ellipse(300, 354, 125, 14), "#6e4a2a", 0.7, edge=0.9)
    return a


def regador(seed=1051):
    a = Aquarela(S, S, seed=seed)
    a.wash(densify(np.array([(130, 250), (400, 250), (385, 500), (150, 500)], float), 160), "#7f9cc9", 0.6, color2="#a8bee0", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(265, 250, 135, 22), "#5f7ca8", 0.6, edge=1.0, outline=0.5)
    _tra(a, _bez(((395, 420), (440, 420), (470, 330), (505, 235))), "#7f9cc9", 26, 0.9, True)
    a.wash(ellipse(512, 222, 40, 18, rot=-1.0), "#5f7ca8", 0.7, edge=0.9, outline=0.45)
    _tra(a, _bez(((150, 300), (60, 290), (60, 450), (150, 440))), "#5f7ca8", 18, 0.85, False)
    _tra(a, _bez(((190, 250), (230, 130), (330, 130), (350, 250))), "#5f7ca8", 18, 0.85, False)
    for (x, y) in ((545, 280), (560, 330), (530, 350)):
        a.wash(leaf((x, y - 22), (x - 5, y + 24), 11), "#8fb4e0", 0.7, edge=0.7)
    return a


# ------------------------------------------------------------------ aves

def ovo(seed=1061):
    a = Aquarela(S, S, seed=seed)
    forma = polar(300, 320, lambda t: 175 - 18 * math.sin(t) * (1 if math.sin(t) < 0 else 0.0) + 0 * t, n=200)
    forma = np.array([(300 + 150 * math.cos(t) * (1.0 - 0.18 * math.sin(t)), 320 + 200 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 200, endpoint=False)])
    a.wash(densify(forma, 220), "#cfe3dc", 0.6, color2="#e4f0ea", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(230, 250, 40))
    rng = np.random.default_rng(3)
    for _ in range(14):
        x, y = 300 + rng.uniform(-90, 90), 320 + rng.uniform(-120, 130)
        a.wash(ellipse(x, y, rng.uniform(6, 13), rng.uniform(5, 10), n=24), "#7a6a52", 0.55, edge=0.6)
    return a


def ninho(seed=1071):
    a = Aquarela(S, S, seed=seed)
    rng = np.random.default_rng(5)
    a.wash(ellipse(300, 440, 250, 90), "#a07a4a", 0.6, color2="#8a6540", edge=1.0, outline=0.5, granulation=1.0)
    for dx, y in ((-60, 340), (30, 330), (110, 345)):
        pass
    for (x, y, rot) in ((230, 340, 0.15), (330, 332, -0.1)):
        forma = np.array([(x + 52 * math.cos(t) * (1 - 0.15 * math.sin(t)), y + 68 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 120, endpoint=False)])
        a.wash(densify(forma, 140), "#cfe3dc", 0.65, color2="#e4f0ea", edge=1.0, outline=0.5)
        for _ in range(5):
            a.wash(ellipse(x + rng.uniform(-30, 30), y + rng.uniform(-40, 40), 5, 4, n=16), "#7a6a52", 0.55, edge=0.6)
    a.wash(ellipse(425, 345, 46, 62), "#cfe3dc", 0.65, color2="#e4f0ea", edge=1.0, outline=0.5)
    for _ in range(70):
        x0, y0 = 300 + rng.uniform(-240, 240), 400 + rng.uniform(-30, 120)
        ang = rng.uniform(-0.5, 0.5)
        _tra(a, np.array([(x0, y0), (x0 + 90 * math.cos(ang), y0 + 90 * math.sin(ang))]), ("#7a5a3a", "#9a7a4a", "#6e4a2a")[int(rng.integers(0, 3))], 5, 0.7, True)
    return a


# ------------------------------------------------------------------ céu e água

def _lua(c, lado, seed):
    """Fase da lua. c = -1 (nova) … 0 (quarto) … +1 (cheia); lado 'e' = iluminada à esquerda (lua crescente no céu do Brasil), 'd' = à direita."""
    a = Aquarela(S, S, seed=seed)
    R = 200
    a.wash(ellipse(300, 300, R, R, n=200), "#c8d0dc", 0.5, color2="#dde3ea", edge=0.9, outline=0.45)
    if c > -0.98:
        th = np.linspace(0, math.pi, 90)
        limbo = np.stack([300 - R * np.sin(th), 300 - R * np.cos(th)], 1)
        term = np.stack([300 + c * R * np.sin(th), 300 - R * np.cos(th)], 1)[::-1]
        forma = np.vstack([limbo, term])
        if lado == "d":
            forma = _esp(forma)
        a.wash(densify(forma, 260), "#f0d878", 0.8, color2="#f7e8a0", edge=0.9, outline=0.3, granulation=0.6)
    return a


def lua_nova(seed=1101): return _lua(-1.0, "e", seed)
def lua_crescente(seed=1102): return _lua(-0.55, "e", seed)
def lua_quarto_crescente(seed=1103): return _lua(0.0, "e", seed)
def lua_gibosa_crescente(seed=1104): return _lua(0.55, "e", seed)
def lua_cheia(seed=1105): return _lua(1.0, "e", seed)
def lua_gibosa_minguante(seed=1106): return _lua(0.55, "d", seed)
def lua_quarto_minguante(seed=1107): return _lua(0.0, "d", seed)
def lua_minguante(seed=1108): return _lua(-0.55, "d", seed)


def arco_iris(seed=1111):
    a = Aquarela(S, S, seed=seed)
    cores = ("#d8503a", "#e8883a", "#e8c43a", "#7aa04a", "#4f74a8", "#6a5a98")
    for i, c in enumerate(cores):
        r = 255 - i * 30
        t = np.linspace(math.pi, 2 * math.pi, 80)
        _tra(a, np.stack([300 + r * np.cos(t), 450 + r * np.sin(t)], 1), c, 28, 0.75, False)
    for (x, y) in ((88, 460), (512, 460)):
        a.wash(ellipse(x, y, 90, 42), "#f2f4f6", 0.55, color2="#e0e6ec", edge=1.0, outline=0.3)
        a.wash(ellipse(x + (30 if x < 300 else -30), y - 26, 62, 38), "#f6f8fa", 0.55, edge=1.0, outline=0.3)
    return a


def nuvem_chuva(seed=1121):
    a = Aquarela(S, S, seed=seed)
    for (x, y, rx, ry) in ((200, 230, 110, 80), (310, 190, 130, 105), (420, 240, 105, 78), (310, 270, 190, 70)):
        a.wash(ellipse(x, y, rx, ry), "#9aa8ba", 0.5, color2="#b8c4d2", edge=1.0, outline=0.4)
    for (x, y) in ((170, 400), (240, 470), (310, 410), (380, 480), (450, 400), (270, 545), (400, 555)):
        a.wash(leaf((x, y - 34), (x - 6, y + 28), 20), "#5f8fc4", 0.65, color2="#8fb4e0", edge=0.9, outline=0.3)
    return a


def poca(seed=1131):
    a = Aquarela(S, S, seed=seed)
    forma = polar(300, 330, lambda t: 230 + 38 * math.sin(2 * t + 0.4) + 22 * math.sin(3 * t + 1.1), n=220)
    forma[:, 1] = 330 + (forma[:, 1] - 330) * 0.52
    a.wash(densify(forma, 240), "#8fb4d8", 0.55, color2="#b4cfe8", edge=1.0, outline=0.45)
    for rx, ry in ((70, 28), (115, 46)):
        a.stroke(np.vstack([ellipse(300, 330, rx, ry, n=80), ellipse(300, 330, rx, ry, n=80)[:3]]), "#f4f8fc", width=6, opacity=0.75, taper=False)
    a.wash(leaf((380, 300), (470, 270), 24), "#7aa04a", 0.65, edge=0.9, outline=0.4)
    return a


def barquinho(seed=1141):
    a = Aquarela(S, S, seed=seed)
    for (x, y) in ((140, 520), (300, 540), (460, 520)):
        a.stroke(bezier((x - 110, y), (x - 55, y - 30), (x + 55, y + 30), (x + 110, y)), "#6f98c4", width=18, opacity=0.75, taper=True)
    casco = np.array([(110, 360), (490, 360), (400, 470), (200, 470)], float)
    a.wash(densify(casco, 160), "#f4ead4", 0.7, color2="#e4d6b8", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    vela = np.array([(300, 120), (440, 355), (160, 355)], float)
    a.wash(densify(vela, 160), "#f9f2e2", 0.7, color2="#ead9bc", edge=1.0, outline=0.5)
    _tra(a, np.array([(300, 130), (300, 355)]), "#b8a888", 3, 0.6, True)
    return a


def _estrela(a, x, y, r, cor="#f0c84a", rot=-math.pi / 2):
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    a.wash(np.array(pts, float), cor, 0.8, color2="#f7e088", edge=0.9, outline=0.4)


def cruzeiro_do_sul(seed=1151):
    a = Aquarela(S, S, seed=seed)
    est = ((330, 105, 52), (300, 505, 62), (465, 320, 46), (160, 265, 44))
    for (x, y, r) in est:
        _estrela(a, x, y, r)
    _estrela(a, 375, 395, 24, "#f7e08a")
    _tra(a, np.array([(330, 150), (302, 440)]), "#c8b890", 3, 0.5, True)
    _tra(a, np.array([(205, 275), (418, 316)]), "#c8b890", 3, 0.5, True)
    return a


def terra(seed=1161):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 300, 240, 240, n=220), "#5f8fc4", 0.65, color2="#8fb4e0", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(220, 250, 40))
    for forma in (_bez(((200, 160), (260, 110), (330, 140), (350, 210)), ((350, 210), (330, 260), (290, 240), (260, 290)), ((260, 290), (220, 330), (190, 260), (200, 160))),
                  _bez(((340, 330), (400, 310), (440, 360), (410, 440)), ((410, 440), (380, 500), (340, 450), (330, 400)), ((330, 400), (325, 360), (330, 340), (340, 330))),
                  _bez(((140, 380), (190, 370), (210, 420), (170, 470)), ((170, 470), (140, 460), (120, 420), (140, 380)))):
        a.wash(densify(forma, 140), "#7aa04a", 0.65, color2="#a3c06a", edge=1.0, outline=0.4)
    a.stroke(np.stack([300 + 240 * np.cos(np.linspace(0, math.pi, 80)), 300 + 36 * np.sin(np.linspace(0, math.pi, 80))], 1), "#fbf3de", width=4, opacity=0.8, taper=False)
    return a


# ------------------------------------------------------------------ corpo

PELE = ("#e4b48c", "#efc7a4")


def mao(seed=1201):
    a = Aquarela(S, S, seed=seed)
    for (x, y, rx, ry, rot) in ((160, 345, 32, 86, -0.95), (232, 200, 31, 96, -0.1), (300, 165, 32, 112, 0.0), (368, 190, 31, 100, 0.1), (428, 262, 28, 80, 0.3)):
        a.wash(ellipse(x, y, rx, ry, rot=rot), PELE[0], 0.8, color2=PELE[1], edge=1.0, outline=0.5)
    a.wash(ellipse(300, 395, 140, 140), PELE[0], 0.95, color2=PELE[1], edge=1.0, outline=0.0, shade=(1, 0.5, 0.5))
    for (x, y) in ((232, 112), (300, 62), (368, 100), (428, 196), (150, 270)):
        a.wash(ellipse(x, y, 17, 14, n=30), "#f3d9c4", 0.6, edge=0.7, outline=0.25)
    return a

def pe(seed=1211):
    a = Aquarela(S, S, seed=seed)
    sola = _bez(((250, 560), (160, 500), (170, 300), (240, 250)), ((240, 250), (330, 200), (430, 260), (440, 360)),
                ((440, 360), (450, 500), (400, 570), (320, 575)), ((320, 575), (300, 577), (270, 570), (250, 560)))
    a.wash(densify(sola, 240), PELE[0], 0.65, color2=PELE[1], edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for (x, y, r) in ((200, 190, 44), (268, 130, 36), (330, 112, 32), (386, 128, 29), (432, 170, 25)):
        a.wash(ellipse(x, y, r, r * 1.1, n=40), PELE[0], 0.65, color2=PELE[1], edge=1.0, outline=0.5)
    return a


def olho(seed=1221):
    a = Aquarela(S, S, seed=seed)
    forma = _bez(((60, 300), (180, 150), (420, 150), (540, 300)), ((540, 300), (420, 450), (180, 450), (60, 300)))
    a.wash(densify(forma, 240), "#f6f1e6", 0.7, color2="#e8e0d0", edge=1.0, outline=0.55)
    a.wash(ellipse(300, 300, 108, 108, n=80), "#5f8a6a", 0.75, color2="#86ae8a", edge=1.0, outline=0.45)
    a.wash(ellipse(300, 300, 46, 46, n=60), "#1f1a16", 0.9, edge=0.7)
    a.wash(ellipse(268, 268, 18, 18, n=30), "#fbf6ec", 0.9, edge=0.5)
    for ang in np.linspace(-2.7, -0.45, 7):
        x0, y0 = 300 + 215 * math.cos(ang), 300 + 150 * math.sin(ang) + 10
        _tra(a, np.array([(x0, y0), (x0 + 28 * math.cos(ang), y0 + 38 * math.sin(ang))]), "#3a2c20", 5, 0.8, True)
    return a


def orelha(seed=1231):
    a = Aquarela(S, S, seed=seed)
    forma = _bez(((300, 80), (450, 70), (500, 220), (440, 330)), ((440, 330), (410, 400), (380, 470), (330, 520)), ((330, 520), (270, 570), (190, 520), (210, 450)),
                 ((210, 450), (160, 420), (120, 300), (140, 200)), ((140, 200), (160, 110), (230, 80), (300, 80)))
    a.wash(densify(forma, 280), PELE[0], 0.65, color2=PELE[1], edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _tra(a, _bez(((290, 160), (400, 160), (420, 290), (360, 380)), ((360, 380), (330, 420), (280, 440), (270, 470))), "#b8845a", 8, 0.8, True)
    _tra(a, _bez(((230, 250), (250, 200), (300, 220), (290, 290)), ((290, 290), (280, 340), (240, 350), (240, 400))), "#b8845a", 7, 0.75, True)
    a.wash(ellipse(270, 400, 24, 40, rot=0.3), "#a87a52", 0.55, edge=0.8)
    return a


def nariz(seed=1241):
    a = Aquarela(S, S, seed=seed)
    forma = _bez(((300, 90), (340, 90), (350, 250), (400, 360)), ((400, 360), (460, 380), (470, 470), (410, 500)), ((410, 500), (360, 530), (240, 530), (190, 500)),
                 ((190, 500), (130, 470), (140, 380), (200, 360)), ((200, 360), (250, 250), (260, 90), (300, 90)))
    a.wash(densify(forma, 260), PELE[0], 0.6, color2=PELE[1], edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for (x, ang) in ((250, 0.4), (350, -0.4)):
        a.wash(ellipse(x, 465, 28, 18, rot=ang), "#5b3a26", 0.85, edge=0.7)
    return a


def boca(seed=1251):
    """Sorriso aberto. A aquarela só escurece, então os dentes ficam em branco de papel, contornados, entre os lábios e o fundo da boca."""
    a = Aquarela(S, S, seed=seed)
    labio_sup = _bez(((70, 282), (190, 205), (410, 205), (530, 282)), ((530, 282), (410, 252), (190, 252), (70, 282)))
    labio_inf = _bez(((70, 282), (150, 505), (450, 505), (530, 282)), ((530, 282), (450, 440), (150, 440), (70, 282)))
    for forma in (labio_sup, labio_inf):
        a.wash(densify(forma, 240), "#c0505a", 0.85, color2="#d8707a", edge=1.0, outline=0.5)
    interior = _bez(((108, 290), (200, 346), (400, 346), (492, 290)), ((492, 290), (452, 432), (148, 432), (108, 290)))
    a.wash(densify(interior, 220), "#7a2a30", 0.9, edge=0.8, outline=0.3)
    a.wash(ellipse(300, 392, 82, 26), "#d8707a", 0.8, edge=0.9)
    cima = bezier((108, 288), (230, 256), (370, 256), (492, 288))
    baixo = bezier((108, 290), (200, 346), (400, 346), (492, 290))
    a.stroke(cima, "#8a7a62", width=4, opacity=0.8, taper=False)
    a.stroke(baixo, "#8a7a62", width=4, opacity=0.8, taper=False)
    for t in np.linspace(0.12, 0.88, 7):
        k = int(t * 59)
        _tra(a, np.array([cima[k], baixo[k]]), "#8a7a62", 3, 0.7, True)
    return a


def dente(seed=1261):
    a = Aquarela(S, S, seed=seed)
    forma = _bez(((150, 190), (200, 90), (300, 150), (300, 150)), ((300, 150), (300, 150), (400, 90), (450, 190)),
                 ((450, 190), (480, 300), (430, 380), (420, 480)), ((420, 480), (410, 560), (350, 570), (340, 490)),
                 ((340, 490), (330, 420), (270, 420), (260, 490)), ((260, 490), (250, 570), (190, 560), (180, 480)),
                 ((180, 480), (170, 380), (120, 300), (150, 190)))
    a.wash(densify(forma, 300), "#f6f1e6", 0.8, color2="#e6ecee", edge=1.0, outline=0.55, shade=(1, 0.5, 0.5), light=(220, 250, 40))
    _tra(a, bezier((200, 210), (190, 260), (200, 300), (215, 330)), "#fbf8f0", 8, 0.8, True)
    return a


def escova_dentes(seed=1271):
    a = Aquarela(S, S, seed=seed)
    cabo = _bez(((70, 360), (80, 332), (360, 332), (390, 345)), ((390, 345), (398, 365), (392, 392), (365, 400)), ((365, 400), (300, 415), (100, 410), (75, 400)), ((75, 400), (60, 390), (60, 370), (70, 360)))
    a.wash(densify(cabo, 220), "#4f74a8", 0.8, color2="#7f9cc9", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(densify(_ret(372, 322, 545, 405, 16), 160), "#4f74a8", 0.8, color2="#7f9cc9", edge=1.0, outline=0.5)
    for x in range(388, 540, 15):
        _tra(a, np.array([(x, 322), (x, 258)]), "#5f9a7a" if (x // 15) % 2 else "#8cc4a4", 9, 0.9, True)
    pasta = _bez(((385, 252), (420, 218), (470, 250), (505, 222)), ((505, 222), (530, 240), (525, 262), (500, 262)), ((500, 262), (450, 272), (420, 268), (385, 262)))
    a.wash(densify(pasta, 140), "#cfe6f2", 0.9, edge=0.9, outline=0.45)
    return a



# ------------------------------------------------------------------ estações

def casaco(seed=1301):
    a = Aquarela(S, S, seed=seed)
    corpo = np.array([(200, 150), (300, 120), (400, 150), (430, 520), (170, 520)], float)
    a.wash(densify(corpo, 200), "#c0716b", 0.7, color2="#d8928a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for lado in (1, -1):
        m = np.array([(200, 150), (110, 200), (90, 440), (150, 450), (190, 260)], float)
        a.wash(densify(m if lado == 1 else _esp(m), 160), "#b8625c", 0.7, color2="#d08078", edge=1.0, outline=0.5)
    a.wash(densify(np.array([(260, 128), (300, 190), (340, 128), (320, 118), (300, 135), (280, 118)], float), 100), "#8a4a46", 0.8, edge=0.9, outline=0.4)
    _tra(a, np.array([(300, 190), (300, 520)]), "#7a3a36", 5, 0.8)
    for y in (260, 340, 420):
        a.wash(ellipse(320, y, 16, 16, n=30), "#f0e0c0", 0.85, edge=0.7, outline=0.4)
    return a


def sandalia(seed=1311):
    a = Aquarela(S, S, seed=seed)
    sola = _bez(((230, 540), (170, 460), (180, 200), (260, 90)), ((260, 90), (330, 40), (440, 110), (430, 250)), ((430, 250), (425, 400), (400, 520), (330, 560)), ((330, 560), (290, 575), (250, 565), (230, 540)))
    a.wash(densify(sola, 240), "#e8c43a", 0.7, color2="#f2d870", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _tra(a, bezier((330, 170), (260, 250), (230, 300), (225, 320)), "#c43a2e", 18, 0.85, True)
    _tra(a, bezier((330, 170), (370, 250), (390, 290), (395, 310)), "#c43a2e", 18, 0.85, True)
    a.wash(ellipse(330, 170, 20, 20, n=30), "#a82c22", 0.85, edge=0.7)
    return a


def floco_neve(seed=1321):
    a = Aquarela(S, S, seed=seed)
    for k in range(6):
        ang = k * math.pi / 3 - math.pi / 2
        u = np.array([math.cos(ang), math.sin(ang)])
        nv = np.array([-u[1], u[0]])
        _tra(a, np.array([(300, 300) + u * 10, (300, 300) + u * 250]), "#6f9ac8", 11, 0.85, True)
        for f, c in ((0.45, 70), (0.7, 52)):
            base = np.array([300, 300]) + u * 250 * f
            for lado in (1, -1):
                _tra(a, np.array([base, base + u * c * 0.8 + nv * lado * c * 0.7]), "#8fb4de", 8, 0.85, True)
    a.wash(ellipse(300, 300, 26, 26, n=30), "#8fb4de", 0.8, edge=0.8)
    return a


def sorvete(seed=1331):
    a = Aquarela(S, S, seed=seed)
    cone = np.array([(190, 330), (410, 330), (300, 580)], float)
    a.wash(densify(cone, 160), "#d9a05a", 0.7, color2="#e8c080", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for k in range(4):
        _tra(a, np.array([(210 + k * 55, 340), (275 + k * 12, 560 - k * 30)]), "#b07a38", 3.5, 0.6, True)
    a.wash(ellipse(300, 285, 125, 60), "#f0a0b0", 0.7, color2="#f6c0cc", edge=1.0, outline=0.5)
    a.wash(ellipse(300, 205, 105, 90), "#f6e2b8", 0.7, color2="#fff0d0", edge=1.0, outline=0.5)
    a.wash(ellipse(300, 125, 18, 18, n=30), "#c43a2e", 0.85, edge=0.7, outline=0.4)
    return a


def caneca_quente(seed=1341):
    a = Aquarela(S, S, seed=seed)
    corpo = np.array([(150, 270), (400, 270), (385, 500), (165, 500)], float)
    a.wash(densify(corpo, 160), "#c0716b", 0.7, color2="#d8928a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(275, 270, 125, 20), "#7a4a30", 0.8, edge=0.9, outline=0.4)
    _tra(a, _bez(((398, 320), (500, 300), (500, 450), (390, 440))), "#c0716b", 22, 0.85, False)
    for x in (230, 285, 340):
        _tra(a, _bez(((x, 230), (x - 22, 190), (x + 22, 150), (x, 100))), "#b8bcc4", 9, 0.7, True)
    return a


# ------------------------------------------------------------------ objetos do diário

def caderno(seed=1401):
    a = Aquarela(S, S, seed=seed)
    capa = np.array([(150, 90), (450, 90), (450, 520), (150, 520)], float)
    a.wash(densify(capa, 200), "#4f6b3a", 0.75, color2="#6f8a52", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(densify(_ret(215, 170, 425, 300, 6), 160), "#f2ead8", 0.8, edge=0.9, outline=0.4)
    a.wash(leaf((320, 270), (320, 185), 26), "#7aa04a", 0.7, edge=0.9, outline=0.3)
    for y in range(120, 500, 52):
        a.wash(ellipse(150, y, 22, 12, n=30), "#d8d0c0", 0.8, edge=0.8, outline=0.4)
    return a


def lapis_cor(seed=1411):
    a = Aquarela(S, S, seed=seed)
    for (cor, ang, ox) in (("#c43a2e", -0.45, 220), ("#e8b830", -0.05, 300), ("#4f74a8", 0.35, 380)):
        c, sn = math.cos(ang), math.sin(ang)
        base = np.array([ox, 560]); topo = base + np.array([sn * 420, -c * 420])
        nv = np.array([c, sn])
        corpo = np.array([base + nv * 26, base - nv * 26, topo - nv * 26, topo + nv * 26])
        a.wash(densify(corpo, 120), cor, 0.7, edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
        ponta = np.array([topo + nv * 26, topo - nv * 26, topo + np.array([sn * 60, -c * 60])])
        a.wash(densify(ponta, 80), "#e8d2a8", 0.8, edge=0.9, outline=0.45)
        a.wash(densify(np.array([topo + np.array([sn * 40, -c * 40]) + nv * 8, topo + np.array([sn * 40, -c * 40]) - nv * 8, topo + np.array([sn * 60, -c * 60])]), 60), cor, 0.85, edge=0.7)
    return a


def teia(seed=1421):
    a = Aquarela(S, S, seed=seed)
    cor = "#9d9482"
    for k in range(10):
        ang = k * math.pi / 5
        _tra(a, np.array([(300, 300), (300 + 255 * math.cos(ang), 300 + 255 * math.sin(ang))]), cor, 4, 0.8, True)
    for r in (50, 95, 145, 200, 250):
        pts = [(300 + r * math.cos(k * math.pi / 5) * (1 - 0.04 * math.sin(k * 3)), 300 + r * math.sin(k * math.pi / 5)) for k in range(11)]
        for i in range(10):
            _tra(a, bezier(pts[i], (pts[i][0] * 0.5 + pts[i + 1][0] * 0.5 + 6, pts[i][1] * 0.5 + pts[i + 1][1] * 0.5 + 6), (pts[i][0] * 0.5 + pts[i + 1][0] * 0.5 - 6, pts[i][1] * 0.5 + pts[i + 1][1] * 0.5 + 4), pts[i + 1]), cor, 3.5, 0.75, True)
    for (x, y) in ((345, 270), (280, 215), (390, 345), (225, 345)):
        a.wash(ellipse(x, y, 9, 9, n=24), "#9cc4e4", 0.7, edge=0.6, outline=0.2)
    return a


def bebedouro(seed=1431):
    a = Aquarela(S, S, seed=seed)
    a.wash(densify(np.array([(255, 330), (345, 330), (370, 540), (230, 540)], float), 120), "#b8a890", 0.65, color2="#d0c4ac", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(300, 548, 130, 24), "#b8a890", 0.65, edge=1.0, outline=0.5)
    a.wash(ellipse(300, 300, 215, 62), "#b8a890", 0.65, color2="#d0c4ac", edge=1.0, outline=0.5)
    a.wash(ellipse(300, 298, 190, 46), "#9cc0e0", 0.65, color2="#c0d8ee", edge=1.0, outline=0.4)
    a.stroke(ellipse(300, 298, 70, 18, n=60), "#f4f8fc", width=5, opacity=0.8, taper=False)
    return a


def casinha(seed=1441):
    a = Aquarela(S, S, seed=seed)
    a.wash(densify(_ret(160, 250, 440, 540, 6), 160), "#b8844e", 0.7, color2="#d09c64", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), granulation=0.8)
    a.wash(densify(np.array([(120, 270), (300, 90), (480, 270)], float), 140), "#8a5a38", 0.7, color2="#a8744a", edge=1.0, outline=0.5)
    a.wash(ellipse(300, 390, 52, 52, n=60), "#3a2c20", 0.9, edge=0.8, outline=0.4)
    _tra(a, np.array([(300, 470), (300, 520)]), "#6e4a2a", 10, 0.85, True)
    a.wash(densify(_ret(280, 460, 320, 480, 3), 60), "#6e4a2a", 0.85, edge=0.7)
    return a


def orvalho_folha(seed=1451):
    a = Aquarela(S, S, seed=seed)
    a.wash(leaf((120, 500), (500, 120), 150), "#7aa04a", 0.65, color2="#a3c06a", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    _veias(a, (120, 500), (500, 120), n=5, abertura=0.7, escala=0.5)
    for (x, y, r) in ((300, 270, 22), (350, 210, 16), (230, 360, 18), (390, 330, 14), (310, 400, 12)):
        a.wash(ellipse(x, y, r, r * 1.15, n=40), "#cfe4f4", 0.7, color2="#e6f2fa", edge=0.9, outline=0.4, light=(230, 250, 40))
    return a


def osso(seed=1281):
    a = Aquarela(S, S, seed=seed)
    haste = np.array([(190, 255), (410, 255), (410, 345), (190, 345)], float)
    a.wash(densify(haste, 100), "#efe6d2", 0.85, color2="#e0d4b8", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for (x, y) in ((150, 245), (150, 355), (450, 245), (450, 355)):
        a.wash(ellipse(x, y, 52, 52, n=60), "#efe6d2", 0.85, color2="#e0d4b8", edge=1.0, outline=0.5)
    return a


def besouro(seed=1291):
    a = Aquarela(S, S, seed=seed)
    cor = "#2f3a30"
    for (y, d) in ((300, 1), (360, 1), (420, 1)):
        for lado in (1, -1):
            _tra(a, _bez(((300 + lado * 90, y), (300 + lado * 160, y - 25), (300 + lado * 215, y + 5), (300 + lado * 240, y + 60))), cor, 7, 0.85, True)
    a.wash(ellipse(300, 390, 135, 170), "#2f5f50", 0.8, color2="#4f8070", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(220, 250, 40))
    _tra(a, np.array([(300, 232), (300, 556)]), cor, 5, 0.8, True)
    a.wash(ellipse(300, 205, 62, 48), cor, 0.85, edge=0.9, outline=0.35)
    _tra(a, bezier((270, 175), (240, 130), (215, 110), (190, 100)), cor, 5, 0.85, True)
    _tra(a, bezier((330, 175), (360, 130), (385, 110), (410, 100)), cor, 5, 0.85, True)
    return a


BICHOS = {"besouro": besouro, "borboleta": borboleta, "joaninha": joaninha, "abelha": abelha, "formiga": formiga, "caracol": caracol,
          "aranha": aranha, "minhoca": minhoca, "lagarta": lagarta, "casulo": casulo, "libelula": libelula}

PLANTAS = {"folha_carvalho": folha_carvalho, "folha_bordo": folha_bordo, "folha_coracao": folha_coracao, "folha_fina": folha_fina, "folha_seca": folha_seca,
           "tronco": tronco, "raiz_arvore": raiz_arvore, "pinha": pinha, "flor_rosa": flor_rosa, "feijao": feijao, "feijao_raiz": feijao_raiz,
           "feijao_broto": feijao_broto, "vaso": vaso, "plantinha": plantinha, "regador": regador, "ovo": ovo, "ninho": ninho}

CEU = {"lua_nova": lua_nova, "lua_crescente": lua_crescente, "lua_quarto_crescente": lua_quarto_crescente, "lua_gibosa_crescente": lua_gibosa_crescente,
       "lua_cheia": lua_cheia, "lua_gibosa_minguante": lua_gibosa_minguante, "lua_quarto_minguante": lua_quarto_minguante, "lua_minguante": lua_minguante,
       "arco_iris": arco_iris, "nuvem_chuva": nuvem_chuva, "poca": poca, "barquinho": barquinho, "cruzeiro_do_sul": cruzeiro_do_sul, "terra": terra}

CORPO = {"osso": osso, "mao": mao, "pe": pe, "olho": olho, "orelha": orelha, "nariz": nariz, "boca": boca, "dente": dente, "escova_dentes": escova_dentes}
ESTACOES = {"casaco": casaco, "sandalia": sandalia, "floco_neve": floco_neve, "sorvete": sorvete, "caneca_quente": caneca_quente}
OBJETOS = {"caderno": caderno, "lapis_cor": lapis_cor, "teia": teia, "bebedouro": bebedouro, "casinha": casinha, "orvalho_folha": orvalho_folha}

MOTIVOS7 = {**BICHOS, **PLANTAS, **CEU, **CORPO, **ESTACOES, **OBJETOS}


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS7):
        MOTIVOS7[n]().rgba().save(os.path.join(out, f"{n}.png"))
