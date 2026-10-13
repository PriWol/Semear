"""
Motivos botânicos e de céu, pintados com o motor de aquarela.
Cada função devolve uma Aquarela de 600×600 px (≈ 5 cm a 300 dpi).
Paleta da coleção: ver docs/02-padrao-editorial.md.
"""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf

S = 600
SEPIA = "#5b4632"
FOLHA = "#7f9a52"
FOLHA_ESC = "#4f6b3a"
OCRE = "#c9963f"


def _folha_com_nervura(a, base, tip, width, cor=FOLHA, cor2="#b7c46a", asym=0.05):
    a.wash(leaf(base, tip, width, asym=asym), cor, 0.5, color2=cor2, edge=0.8)
    mid = np.linspace(base, tip, 30)
    a.stroke(mid, FOLHA_ESC, width=2.2, opacity=0.45)


def maca():
    a = Aquarela(S, S, seed=11)
    # maçã: ombros largos, covinha no topo, base mais estreita
    def r(t):
        s = math.sin(t)  # s<0 topo
        base = 185 * (1 + 0.07 * math.cos(2 * t))
        base *= 1 - 0.10 * max(0, s) ** 2          # afunila embaixo
        base *= 1 - 0.22 * math.exp(-((t - 1.5 * math.pi) / 0.22) ** 2)  # covinha
        base *= 1 - 0.06 * math.exp(-((t - 0.5 * math.pi) / 0.3) ** 2)
        return base
    body = polar(300, 340, r)
    a.wash(body, "#e2b450", 0.30, edge=0.3, layers=2)
    a.wash(body, "#c43a2e", 0.55, color2="#9e2a2f", edge=1.0, light=(228, 270, 48),
           shade=(1, 0.5, 0.55), outline=0.35)
    for k, x0 in enumerate((215, 262, 340, 388)):  # estrias que seguem a forma
        bend = (x0 - 300) * 0.35
        a.stroke(bezier((x0 - bend * 0.2, 215), (x0 + bend, 300), (x0 + bend, 400), (x0 - bend * 0.3, 485)),
                 "#8e1f22", width=2.2, opacity=0.14)
    a.stroke(bezier((300, 198), (296, 160), (306, 125), (320, 98)), "#5b3a22", width=9, opacity=0.9)
    _folha_com_nervura(a, (318, 118), (455, 78), 72)
    return a


def pera():
    a = Aquarela(S, S, seed=12)
    body = np.vstack([bezier((300, 132), (350, 130), (362, 200), (368, 255)),
                      bezier((368, 255), (378, 320), (470, 360), (466, 450)),
                      bezier((466, 450), (462, 540), (380, 572), (300, 572)),
                      bezier((300, 572), (220, 572), (138, 540), (134, 450)),
                      bezier((134, 450), (130, 360), (222, 320), (232, 255)),
                      bezier((232, 255), (238, 200), (250, 130), (300, 132))])
    a.wash(body, "#d6c24c", 0.45, color2="#a3b046", edge=1.0, light=(225, 440, 34),
           shade=(1, 0.3, 0.6), shade_color="#8f9a3a", outline=0.35)
    a.wash(ellipse(390, 460, 50, 70), "#c87a40", 0.2, edge=0.0, soft=18, wobble=6)
    a.spatter((300, 450), 110, "#7b5a32", n=22, size=(1.2, 2.2), opacity=0.35)
    a.stroke(bezier((300, 135), (297, 105), (305, 85), (322, 62)), "#5b3a22", width=9, opacity=0.9)
    _folha_com_nervura(a, (318, 84), (432, 42), 52)
    return a


def morango():
    a = Aquarela(S, S, seed=13)
    body = np.vstack([bezier((300, 120), (430, 95), (500, 190), (450, 300)),
                      bezier((450, 300), (410, 400), (340, 520), (300, 545)),
                      bezier((300, 545), (260, 520), (190, 400), (150, 300)),
                      bezier((150, 300), (100, 190), (170, 95), (300, 120))])
    a.wash(body, "#d3352d", 0.6, color2="#b51f2c", edge=1.0, light=(235, 230, 40),
           shade=(1, 0.6, 0.5), outline=0.35)
    mask = a._raster(body)
    rng = np.random.default_rng(3)
    for row in range(9):
        y = 175 + row * 41
        for k in range(9):
            x = 160 + k * 36 + (row % 2) * 18 + rng.normal(0, 7)
            y = 175 + row * 41 + rng.normal(0, 6)
            if mask[int(y), int(x)] > 0.5 and mask[int(y) + 10, int(x)] > 0.5 and y < 520:
                a.lift(ellipse(x, y, 7, 9, n=20), 0.6)
                a.wash(ellipse(x, y + 1, 3.2, 5, n=16), "#e8c45a", 0.8, edge=0.2, layers=1, wobble=0.4, soft=0.4)
    for ang in np.linspace(math.pi * 0.9, math.pi * 0.1, 6):
        tip = (300 - 150 * math.cos(ang), 128 + 55 * math.sin(ang * 2) * 0.5 + 25)
        a.wash(leaf((300, 120), tip, 38), "#6a8d40", 0.6, color2="#93ad55", edge=0.9)
    a.stroke(bezier((300, 118), (298, 85), (306, 60), (318, 38)), "#4f6b3a", width=10, opacity=0.85)
    return a


def cereja():
    a = Aquarela(S, S, seed=14)
    for cx, cy, s in ((205, 420, 1.0), (390, 448, 0.95)):
        a.wash(polar(cx, cy, lambda t: 100 * s * (1 - 0.1 * math.exp(-((t - 1.5 * math.pi) / 0.3) ** 2))),
               "#a0162a", 0.62, color2="#c4223a", edge=1.0, light=(cx - 35 * s, cy - 32 * s, 22 * s),
               shade=(1, 0.7, 0.6), outline=0.35)
        a.stroke(bezier((cx, cy - 90 * s), (cx + 10, cy - 200), (300, 140), (312, 82)), "#5f6e33", width=6, opacity=0.85)
    _folha_com_nervura(a, (312, 86), (470, 120), 78, asym=0.1)
    return a


def tulipa():
    a = Aquarela(S, S, seed=15)
    a.stroke(bezier((300, 590), (304, 470), (294, 380), (300, 300)), "#5f7f3c", width=12, opacity=0.85)
    a.wash(leaf((292, 585), (170, 330), 95, asym=0.2), FOLHA, 0.5, color2="#a8b860", outline=0.25)
    a.wash(leaf((308, 588), (440, 390), 80, asym=-0.2), "#6f8f48", 0.5, color2="#a8b860", outline=0.25)
    pet_l = np.vstack([bezier((300, 322), (180, 310), (178, 170), (232, 104)),
                       bezier((232, 104), (262, 160), (285, 172), (300, 162))])
    pet_r = pet_l * np.array([-1, 1]) + np.array([600, 0])
    a.wash(pet_l, "#d4545c", 0.55, color2="#e98a6e", edge=1.0, outline=0.3)
    a.wash(pet_r, "#c84653", 0.6, color2="#e07a66", edge=1.0, outline=0.3)
    mid = np.vstack([bezier((300, 326), (214, 312), (226, 160), (300, 92)),
                     bezier((300, 92), (374, 160), (386, 312), (300, 326))])
    a.wash(mid, "#de6268", 0.6, color2="#f0a080", edge=1.1, light=(272, 210, 26),
           shade=(1, 0.2, 0.5), outline=0.3)
    return a


def margarida():
    a = Aquarela(S, S, seed=16)
    a.stroke(bezier((300, 595), (310, 500), (290, 420), (300, 330)), "#5f7f3c", width=9, opacity=0.8)
    _folha_com_nervura(a, (302, 520), (430, 470), 46)
    cx, cy = 300, 255
    for i, ang in enumerate(np.linspace(0, 2 * math.pi, 21, endpoint=False)):
        ang += 0.05 * math.sin(i * 1.7)
        L = 178 + 14 * math.sin(i * 2.3)
        base = (cx + 40 * math.cos(ang), cy + 40 * math.sin(ang))
        tip = (cx + L * math.cos(ang), cy + L * math.sin(ang))
        a.wash(leaf(base, tip, 36), "#b9bccf", 0.16, edge=1.6, layers=2, granulation=0.8, outline=0.22)
    a.wash(ellipse(cx, cy, 54, 52), "#e3a52a", 0.7, color2="#c98a1f", edge=1.0, shade=(1, 1, 0.5))
    a.spatter((cx + 8, cy + 10), 36, "#9a5f1a", n=40, size=(1.2, 2.8), opacity=0.45)
    return a


def folha():
    a = Aquarela(S, S, seed=17)
    base, tip = (170, 470), (455, 120)
    a.wash(leaf(base, tip, 250, asym=0.06), "#7d9a4a", 0.5, color2="#c9b24a", edge=1.0, bloom=0.5, outline=0.3)
    a.stroke(bezier((120, 530), (150, 505), (160, 490), base), "#6b5a2e", width=7, opacity=0.8)
    a.stroke(np.linspace(base, tip, 40), "#556e33", width=3, opacity=0.5)
    u = (np.array(tip) - base) / np.linalg.norm(np.array(tip) - base)
    v = np.array([-u[1], u[0]])
    for t in np.linspace(0.15, 0.78, 6):
        p = np.array(base) + (np.array(tip) - base) * t
        for sgn in (1, -1):
            q = p + u * 60 + v * sgn * 80 * math.sin(math.pi * t ** 0.85)
            a.stroke(bezier(p, p + u * 20 + v * sgn * 30, q - u * 10, q), "#556e33", width=1.8, opacity=0.35)
    return a


def bolota():
    a = Aquarela(S, S, seed=18)
    nut = np.vstack([bezier((180, 300), (160, 430), (240, 540), (300, 548)),
                     bezier((300, 548), (360, 540), (440, 430), (420, 300)),
                     bezier((420, 300), (380, 290), (220, 290), (180, 300))])
    a.wash(nut, "#b8823e", 0.55, color2="#8a5a2a", edge=1.0, light=(250, 400, 28),
           shade=(1, 0.4, 0.6), outline=0.35)
    a.wash(ellipse(300, 540, 9, 7, n=20), "#4b3018", 0.7, layers=1, edge=0.3)
    cup = np.vstack([bezier((150, 330), (150, 205), (450, 205), (450, 330)),
                     bezier((450, 330), (380, 302), (220, 302), (150, 330))])
    a.wash(cup, "#8f7a4a", 0.55, color2="#6b5a35", edge=0.9, granulation=1.0, outline=0.4)
    cm = a._raster(cup)
    for row in range(5):
        for k in range(12):
            x = 165 + k * 25 + (row % 2) * 12
            y = 312 - row * 20
            if cm[int(y) - 6, int(x)] > 0.5:
                a.stroke(bezier((x - 9, y - 2), (x - 5, y - 10), (x + 5, y - 10), (x + 9, y - 2)), "#4e3d22",
                         width=2, opacity=0.45, taper=False)
    a.stroke(bezier((300, 226), (300, 195), (310, 175), (328, 155)), "#5b3a22", width=11, opacity=0.85)
    return a


def cogumelo():
    a = Aquarela(S, S, seed=19)
    stem = np.vstack([bezier((250, 300), (240, 420), (220, 500), (230, 540)),
                      bezier((230, 540), (300, 560), (360, 550), (372, 540)),
                      bezier((372, 540), (370, 480), (352, 400), (350, 300))])
    a.wash(stem, "#e2d6ba", 0.45, color2="#cdbf9c", edge=0.9, shade=(1, 0, 0.6), outline=0.3)
    cap = np.vstack([bezier((105, 330), (110, 120), (490, 120), (495, 330)),
                     bezier((495, 330), (400, 300), (200, 300), (105, 330))])
    a.wash(cap, "#c33a2a", 0.62, color2="#d86a35", edge=1.1, light=(235, 205, 30),
           shade=(1, 0.4, 0.45), outline=0.35)
    for (x, y, r) in ((200, 232, 22), (292, 188, 18), (382, 222, 24), (330, 272, 14),
                      (162, 292, 12), (440, 288, 13), (250, 278, 12)):
        pts = ellipse(x, y, r, r * 0.78, n=40)
        a.lift(pts, 0.9)
        a.wash(pts, "#e9dfc6", 0.3, edge=0.8, layers=2, wobble=1.2)
    a.wash(ellipse(300, 552, 160, 16), "#7a9a4a", 0.3, edge=0.6, soft=3)
    return a


def nuvem_chuva(w=2200, h=520, seed=21):
    a = Aquarela(w, h, seed=seed)
    for cx in range(260, w, 560):
        for (dx, dy, r) in ((-140, 40, 120), (0, -10, 165), (150, 30, 125), (40, 80, 120), (-60, 90, 100)):
            a.wash(ellipse(cx + dx, 230 + dy, r * 1.25, r * 0.85, n=120), "#8fa7bd", 0.16, color2="#b8c6d6",
                   edge=0.9, layers=3, granulation=0.6)
    return a


SUBJECTS = {
    "maca": maca, "pera": pera, "morango": morango, "cereja": cereja,
    "tulipa": tulipa, "margarida": margarida, "folha": folha, "bolota": bolota,
    "cogumelo": cogumelo,
}

def banana():
    a = Aquarela(S, S, seed=31)
    def fruta(dx, dy, col, col2):
        outer = bezier((175, 110), (95, 380), (300, 560), (540, 455), n=90)
        inner = bezier((540, 455), (330, 445), (230, 330), (250, 110), n=90)
        pts = np.vstack([outer, inner, bezier((250, 110), (235, 100), (190, 100), (175, 110), n=10)])
        pts = pts + np.array([dx, dy])
        a.wash(pts, col, 0.45, color2=col2, edge=1.0, light=(230 + dx, 330 + dy, 26), outline=0.4)
        a.stroke(bezier((215 + dx, 120 + dy), (190 + dx, 330 + dy), (330 + dx, 470 + dy), (520 + dx, 452 + dy)),
                 "#b08a2a", width=3, opacity=0.35)
        return pts
    fruta(-45, -12, "#f0cf45", "#e2b83a")
    fruta(5, 12, "#f6d84a", "#e8c040")
    a.wash(ellipse(545, 467, 11, 9, n=20), "#4b3a1e", 0.75, layers=1, edge=0.4)
    a.stroke(bezier((200, 118), (190, 88), (198, 66), (222, 50)), "#6b6a2e", width=20, opacity=0.75)
    return a


def laranja():
    a = Aquarela(S, S, seed=32)
    body = polar(300, 330, lambda t: 200 * (1 + 0.03 * math.cos(3 * t)))
    a.wash(body, "#ec9a2e", 0.55, color2="#e07a22", edge=1.0, light=(232, 262, 40),
           shade=(1, 0.6, 0.5), shade_color="#c45f1a", outline=0.35)
    a.spatter((300, 330), 170, "#b8601a", n=160, size=(0.8, 1.8), opacity=0.25)
    a.wash(ellipse(300, 140, 18, 12, n=30), "#7d8a3a", 0.6, layers=2, edge=0.6)
    a.wash(leaf((305, 140), (440, 70), 70, asym=0.1), "#4f7a3a", 0.6, color2="#7f9a52", edge=1.0, outline=0.25)
    a.wash(leaf((295, 140), (200, 60), 56, asym=-0.1), "#5f8a42", 0.55, color2="#8fa852", edge=1.0, outline=0.25)
    return a


def uva():
    a = Aquarela(S, S, seed=33)
    rng = np.random.default_rng(5)
    rows = [5, 6, 5, 4, 3, 2, 1]
    berries = []
    for r, n in enumerate(rows):
        for k in range(n):
            x = 300 + (k - (n - 1) / 2) * 62 + rng.normal(0, 4)
            y = 175 + r * 56 + rng.normal(0, 3)
            berries.append((x, y))
    for (x, y) in sorted(berries, key=lambda p: -p[1]):
        a.wash(ellipse(x, y, 34, 36, n=60), "#6d4a8a", 0.5, color2="#8a5f9e", edge=1.1,
               light=(x - 12, y - 13, 8), shade=(1, 0.8, 0.5), outline=0.3, layers=2)
    a.stroke(bezier((300, 145), (302, 110), (312, 80), (300, 50)), "#6b5a2e", width=10, opacity=0.85)
    a.wash(np.vstack([leaf((310, 95), (480, 60), 120, asym=0.2)]), "#6f8f48", 0.5, color2="#a8b860", outline=0.25)
    a.stroke(bezier((300, 70), (250, 60), (240, 100), (215, 90)), "#7f9a52", width=3, opacity=0.6)
    return a


def jabuticaba():
    a = Aquarela(S, S, seed=34)
    # galho com frutos presos direto na casca (caulifloria)
    branch = np.vstack([bezier((20, 330), (200, 300), (400, 330), (590, 280), n=80),
                        bezier((590, 312), (400, 362), (200, 334), (20, 366), n=80)])
    a.wash(branch, "#a08060", 0.5, color2="#7a6048", edge=1.0, granulation=1.0, outline=0.35)
    rng = np.random.default_rng(8)
    for (x, y, r) in ((110, 290, 42), (175, 392, 46), (255, 280, 44), (322, 395, 48), (395, 285, 40),
                      (450, 385, 44), (520, 262, 38), (230, 455, 40)):
        a.wash(ellipse(x, y, r, r * 0.97, n=60), "#2e2238", 0.55, color2="#4a3550", edge=1.0,
               light=(x - r * 0.35, y - r * 0.38, r * 0.2), shade=(1, 0.7, 0.4), outline=0.25, layers=2)
    return a


def melancia():
    a = Aquarela(S, S, seed=35)
    cx, cy, R = 300, 210, 260
    t = np.linspace(0, math.pi, 120)
    casca = np.vstack([np.stack([cx + R * np.cos(t), cy + R * np.sin(t)], 1), [(cx - R, cy)]])
    a.wash(casca, "#4f7a3a", 0.6, color2="#6f9a4a", edge=1.0, outline=0.4)
    r2 = R - 24
    branco = np.vstack([np.stack([cx + r2 * np.cos(t), cy + r2 * np.sin(t)], 1)])
    a.lift(branco, 0.9)
    a.wash(branco, "#e6e8c0", 0.3, edge=0.6, layers=2)
    r3 = R - 44
    polpa = np.vstack([np.stack([cx + r3 * np.cos(t), cy + 4 + r3 * np.sin(t)], 1)])
    a.wash(polpa, "#e2475a", 0.55, color2="#ef6b6b", edge=1.1, light=(cx - 60, cy + 70, 40), outline=0.3)
    rng = np.random.default_rng(4)
    for k in range(14):
        ang = rng.uniform(0.35, math.pi - 0.35)
        rr = rng.uniform(70, r3 - 40)
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        a.wash(ellipse(x, y, 7, 12, n=20, rot=ang - math.pi / 2), "#2a1e1a", 0.85, layers=1, edge=0.4, wobble=0.5)
    return a


def girassol():
    a = Aquarela(S, S, seed=36)
    a.stroke(bezier((300, 598), (300, 520), (310, 470), (300, 420)), "#5f7f3c", width=13, opacity=0.85)
    cx, cy = 300, 260
    for layer, (n, L, col) in enumerate(((18, 200, "#e0a020"), (18, 188, "#f0c040"))):
        for i, ang in enumerate(np.linspace(0, 2 * math.pi, n, endpoint=False) + layer * math.pi / n):
            base = (cx + 70 * math.cos(ang), cy + 70 * math.sin(ang))
            tip = (cx + L * math.cos(ang), cy + L * math.sin(ang))
            a.wash(leaf(base, tip, 52), col, 0.45, color2="#e8b02a", edge=1.1, layers=2, outline=0.2)
    a.wash(ellipse(cx, cy, 82, 80), "#5a3a1e", 0.65, color2="#7a4a22", edge=1.0, granulation=1.0)
    a.spatter((cx, cy), 72, "#2e1e10", n=120, size=(1.5, 3.2), opacity=0.45)
    return a


def ratinho():
    """Ratinho sentado de perfil — vinheta pequena (personagem afetivo)."""
    a = Aquarela(S, S, seed=37)
    body = np.vstack([bezier((170, 520), (120, 380), (220, 250), (330, 270)),
                      bezier((330, 270), (430, 290), (470, 420), (440, 520)),
                      bezier((440, 520), (350, 545), (250, 545), (170, 520))])
    a.wash(body, "#a89a8a", 0.45, color2="#8f8070", edge=1.0, shade=(1, 0.5, 0.5), outline=0.45, granulation=0.9)
    a.wash(ellipse(300, 470, 70, 55), "#efe6d6", 0.25, edge=0.3, soft=8)  # barriga clara
    head = np.vstack([bezier((300, 300), (300, 210), (380, 170), (470, 225)),
                      bezier((470, 225), (520, 255), (530, 272), (548, 286)),
                      bezier((548, 286), (520, 310), (460, 330), (400, 335)),
                      bezier((400, 335), (340, 335), (305, 330), (300, 300))])
    a.wash(ellipse(372, 192, 54, 62, rot=-0.3), "#b49a8e", 0.4, edge=1.0, outline=0.45)
    a.wash(ellipse(376, 198, 30, 38, rot=-0.3), "#e2a8a0", 0.4, edge=0.6)
    a.wash(head, "#ab9d8c", 0.42, color2="#958676", edge=1.0, outline=0.45, granulation=0.9)
    a.wash(ellipse(548, 286, 10, 9, n=24), "#c7807a", 0.8, layers=1, edge=0.5)
    a.wash(ellipse(470, 250, 9, 10, n=24), "#2a2018", 0.9, layers=1, edge=0.4)
    a.lift(ellipse(467, 246, 3, 3, n=12), 0.9, soft=0.5)
    for dy, ang in ((-6, -0.25), (2, 0.0), (10, 0.25)):
        a.stroke(bezier((540, 290 + dy), (575, 285 + dy + ang * 60), (590, 282 + dy + ang * 90), (598, 280 + dy + ang * 120)),
                 "#5b4632", width=1.4, opacity=0.5, taper=False)
    a.wash(ellipse(410, 530, 48, 14), "#a89a8a", 0.5, edge=0.8, outline=0.3)  # pé
    a.stroke(bezier((180, 515), (90, 540), (60, 470), (110, 430)), "#c9a8a0", width=7, opacity=0.6)
    return a


def raminho(w=900, h=300, seed=41, flores=True):
    """Ramo decorativo para cantos e vinhetas."""
    a = Aquarela(w, h, seed=seed)
    stem = bezier((20, h * 0.8), (w * 0.3, h * 0.55), (w * 0.6, h * 0.65), (w - 30, h * 0.35), n=120)
    a.stroke(stem, "#6b7a3e", width=5, opacity=0.75)
    rng = np.random.default_rng(seed)
    for i, t in enumerate(np.linspace(0.08, 0.9, 9)):
        p = stem[int(t * 119)]
        side = 1 if i % 2 else -1
        tip = p + np.array([rng.uniform(40, 80), side * rng.uniform(55, 85)])
        a.wash(leaf(p, tip, rng.uniform(26, 36)), "#7f9a52", 0.45, color2="#b7c46a", edge=1.0, layers=2, outline=0.2)
    if flores:
        for t in (0.25, 0.55, 0.95):
            p = stem[int(min(t, 0.99) * 119)] + np.array([0, -20])
            for k in range(5):
                ang = k * 2 * math.pi / 5
                a.wash(ellipse(p[0] + 15 * math.cos(ang), p[1] + 15 * math.sin(ang), 12, 9, n=30, rot=ang),
                       "#8fa9cf", 0.45, color2="#a9b9de", edge=1.0, layers=2)
            a.wash(ellipse(p[0], p[1], 5, 5, n=16), "#e3b23a", 0.8, layers=1)
    return a


def nuvem(w=700, h=330, seed=51, cor="#8fa7bd"):
    a = Aquarela(w, h, seed=seed)
    cx, cy = w / 2, h * 0.6
    lobes = ((-190, 40, 100), (-75, -20, 125), (70, -35, 135), (200, 30, 105), (0, 55, 150))
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.zeros((h, w), bool)
    for dx, dy, r in lobes:
        m |= ((xx - cx - dx) / (r * 1.05)) ** 2 + ((yy - cy - dy) / (r * 0.75)) ** 2 < 1
    m &= yy < cy + 95
    from PIL import Image as _I
    cont = _contour(m)
    a.wash(cont, cor, 0.2, color2="#c2cfdc", edge=1.2, layers=3, granulation=1.0, bloom=0.5)
    return a


def _contour(mask):
    """Contorno ordenado de uma máscara binária (marching por ângulo a partir do centro)."""
    ys, xs = np.nonzero(mask)
    cx, cy = xs.mean(), ys.mean()
    angs = np.linspace(0, 2 * math.pi, 360, endpoint=False)
    pts = []
    for t in angs:
        r = 0
        while True:
            x, y = int(cx + (r + 1) * math.cos(t)), int(cy + (r + 1) * math.sin(t))
            if not (0 <= x < mask.shape[1] and 0 <= y < mask.shape[0]) or not mask[y, x]:
                break
            r += 1
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return np.array(pts)


def florzinha(seed=61, cor="#d9707a", cor2="#eaa0a0"):
    a = Aquarela(300, 420, seed=seed)
    a.stroke(bezier((150, 418), (155, 360), (145, 300), (150, 190)), "#5f7f3c", width=8, opacity=0.8)
    a.wash(leaf((150, 360), (250, 300), 44), "#7f9a52", 0.5, color2="#b7c46a", edge=1.0, outline=0.2)
    a.wash(leaf((150, 330), (55, 270), 40), "#6f8f48", 0.5, color2="#b7c46a", edge=1.0, outline=0.2)
    for k in range(6):
        ang = k * math.pi / 3 + 0.2
        a.wash(ellipse(150 + 52 * math.cos(ang), 150 + 52 * math.sin(ang), 46, 30, n=60, rot=ang),
               cor, 0.45, color2=cor2, edge=1.1, layers=2, outline=0.25)
    a.wash(ellipse(150, 150, 24, 24), "#e3a52a", 0.7, layers=2, edge=1.0)
    return a


def gota(seed=71):
    a = Aquarela(120, 170, seed=seed)
    pts = np.vstack([bezier((60, 10), (75, 60), (108, 95), (108, 120), n=40),
                     bezier((108, 120), (108, 150), (85, 162), (60, 162), n=30),
                     bezier((60, 162), (35, 162), (12, 150), (12, 120), n=30),
                     bezier((12, 120), (12, 95), (45, 60), (60, 10), n=40)])
    a.wash(pts, "#6f93b8", 0.45, color2="#9cb6d0", edge=1.2, layers=2, light=(45, 115, 10))
    return a


def cesta():
    a = Aquarela(S, 420, seed=81)
    body = np.vstack([bezier((80, 170), (90, 330), (170, 400), (300, 400)),
                      bezier((300, 400), (430, 400), (510, 330), (520, 170)),
                      bezier((520, 170), (400, 195), (200, 195), (80, 170))])
    a.wash(body, "#c49a5a", 0.5, color2="#a87a42", edge=1.0, granulation=1.0, shade=(1, 0.6, 0.5), outline=0.45)
    m = a._raster(body)
    for row in range(7):
        y = 205 + row * 28
        for k in range(16):
            x = 95 + k * 28 + (row % 2) * 14
            if m[int(min(y, 419)), int(min(x, 599))] > 0.5:
                a.stroke(bezier((x - 12, y), (x - 6, y - 7), (x + 6, y - 7), (x + 12, y)), "#7a5530",
                         width=2.2, opacity=0.45, taper=False)
    handle = bezier((110, 180), (120, -40), (480, -40), (490, 180), n=120)
    a.stroke(handle, "#9a7040", width=16, opacity=0.6)
    a.stroke(handle, "#6b4a28", width=3, opacity=0.4)
    rim = bezier((80, 172), (200, 200), (400, 200), (520, 172), n=80)
    a.stroke(rim, "#8a6034", width=14, opacity=0.6)
    return a


SUBJECTS.update({
    "banana": banana, "laranja": laranja, "uva": uva, "jabuticaba": jabuticaba, "melancia": melancia,
    "girassol": girassol, "ratinho": ratinho, "cesta": cesta, "gota": gota,
    "nuvem": nuvem, "raminho": raminho, "florzinha_rosa": florzinha,
    "florzinha_azul": lambda: florzinha(62, "#7f9cc9", "#a9bde0"),
    "florzinha_amarela": lambda: florzinha(63, "#e8b23a", "#f0cf6a"),
})


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    names = sys.argv[2:] or list(SUBJECTS)
    for n in names:
        SUBJECTS[n]().image().save(os.path.join(out, f"{n}.png"), dpi=(300, 300))
        print("ok", n)
