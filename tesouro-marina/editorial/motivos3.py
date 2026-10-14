"""Motivos do Volume 2 (contos e fábulas), no mesmo motor de aquarela."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf, densify
from motivos2 import _ret

S = 600


def patinho(seed=301, cor="#f0cf45", cor2="#e2b83a", w=1.0):
    a = Aquarela(S, S, seed=seed)
    corpo = np.vstack([bezier((140, 360), (130, 470), (300, 520), (430, 470)),
                       bezier((430, 470), (500, 440), (520, 380), (470, 330)),
                       bezier((470, 330), (400, 300), (260, 300), (140, 360))])
    a.wash(corpo, cor, 0.5, color2=cor2, edge=1.1, outline=0.45, shade=(0.3, 1, 0.4))
    a.wash(np.vstack([bezier((470, 330), (530, 300), (540, 270), (520, 250)),
                      bezier((520, 250), (500, 330), (470, 330), (470, 330))]), cor, 0.5, edge=1.0, outline=0.4)  # rabinho
    a.wash(ellipse(200, 270, 82, 78), cor, 0.5, color2=cor2, edge=1.1, outline=0.45)
    bico = np.array([(128, 262), (70, 282), (130, 296)], float)
    a.wash(bico, "#e8862e", 0.65, edge=1.0, outline=0.4)
    a.wash(ellipse(185, 250, 10, 11, n=24), "#2a1e18", 0.9, layers=1, edge=0.4)
    a.lift(ellipse(182, 246, 3, 3, n=12), 0.9, soft=0.4)
    a.stroke(bezier((260, 400), (320, 380), (370, 390), (400, 420)), "#b8902a", width=3, opacity=0.4)
    for x in (260, 340):
        a.stroke([(x, 505), (x - 10, 560)], "#e8862e", width=7, opacity=0.8)
        a.wash(np.array([(x - 40, 560), (x + 15, 560), (x - 10, 548)], float), "#e8862e", 0.6, edge=1.0)
    return a


def ervilha():
    a = Aquarela(S, S, seed=311)
    vagem = np.vstack([bezier((70, 330), (150, 200), (450, 200), (540, 280)),
                       bezier((540, 280), (470, 330), (200, 400), (70, 330))])
    a.wash(vagem, "#8fae5a", 0.5, color2="#b7c46a", edge=1.1, outline=0.45)
    for k, x in enumerate((170, 240, 310, 380, 445)):
        y = 300 - 0.12 * (x - 300) + 4 * math.sin(k)
        a.wash(ellipse(x, y, 30, 30, n=50), "#5f8f3a", 0.6, color2="#7fa848", edge=1.1, light=(x - 9, y - 10, 6), outline=0.3)
    return a


def colchao(seed=312, cor="#c0716b", cor2="#d9a0a0", w=600, h=150):
    a = Aquarela(w, h, seed=seed)
    a.wash(_ret(12, 18, w - 12, h - 18, 34), cor, 0.42, color2=cor2, edge=1.1, outline=0.45)
    for x in range(60, w - 40, 60):
        a.wash(ellipse(x, h / 2, 6, 6, n=16), "#5b4632", 0.5, layers=1, edge=0.5)
    a.stroke(bezier((40, 40), (w / 3, 34), (2 * w / 3, 34), (w - 40, 40)), "#ffffff", width=6, opacity=0.25)
    return a


def pegada(seed=321, esquerda=False):
    a = Aquarela(300, 520, seed=seed)
    sola = np.vstack([bezier((150, 150), (240, 150), (250, 300), (215, 400)),
                      bezier((215, 400), (195, 490), (105, 490), (95, 410)),
                      bezier((95, 410), (85, 330), (60, 160), (150, 150))])
    a.wash(sola, "#8a6a4a", 0.55, color2="#6b4e34", edge=1.1, granulation=1.2)
    dedos = [(214, 140, 28), (176, 118, 21), (142, 113, 18), (112, 123, 15), (86, 142, 13)]
    for x, y, r in dedos:
        a.wash(ellipse(x, y, r, r * 1.15, n=30), "#8a6a4a", 0.55, layers=2, edge=1.0, granulation=1.2)
    if esquerda:
        a.dens = a.dens[:, ::-1]
    return a


def palha():
    a = Aquarela(S, S, seed=331)
    rng = np.random.default_rng(4)
    for k in range(90):
        t = rng.uniform(-1, 1)
        x0 = 300 + t * 60; x1 = 300 + t * 190 + rng.normal(0, 12)
        a.stroke(bezier((x0, 100 + abs(t) * 20), (x0 + t * 10, 250), (x1 - t * 30, 400), (x1, 530)),
                 rng.choice(["#d9b04a", "#c99a3a", "#e6c46a"]), width=3, opacity=0.55)
    a.wash(_ret(250, 290, 350, 330, 8), "#a0503a", 0.6, edge=1.0, outline=0.4)
    return a


def madeira():
    a = Aquarela(S, S, seed=332)
    for row, (n, y) in enumerate(((4, 440), (3, 340), (2, 240))):
        for k in range(n):
            x = 300 + (k - (n - 1) / 2) * 112
            a.wash(ellipse(x, y, 52, 52, n=60), "#c49a62", 0.5, color2="#a87a42", edge=1.1, outline=0.45, granulation=1.2)
            for r in (32, 18):
                a.stroke(ellipse(x, y, r, r, n=40), "#7a5530", width=2, opacity=0.4, taper=False)
    return a


def tijolos():
    a = Aquarela(S, S, seed=333)
    for row in range(6):
        for k in range(5):
            off = 0 if row % 2 == 0 else 50
            x0 = 40 + k * 104 + off - (50 if row % 2 else 0)
            if x0 < 20 or x0 + 96 > 580:
                continue
            y0 = 140 + row * 58
            a.wash(_ret(x0, y0, x0 + 96, y0 + 50, 4), "#b8584a", 0.5, color2="#c8705a", edge=1.0, outline=0.35, granulation=1.0)
    return a


def tartaruga():
    a = Aquarela(S, S, seed=341)
    casco = np.vstack([bezier((110, 380), (130, 180), (430, 180), (470, 380)),
                       bezier((470, 380), (380, 400), (200, 400), (110, 380))])
    a.wash(casco, "#7f8a4a", 0.55, color2="#9a9a5a", edge=1.1, outline=0.45, shade=(1, 0.5, 0.4), granulation=1.0)
    for (x, y) in ((290, 260), (200, 320), (380, 320), (290, 345), (210, 250), (370, 250)):
        a.stroke(polar(x, y, lambda t: 34, n=7), "#4f5a2e", width=3, opacity=0.5, taper=False)
    a.wash(ellipse(525, 360, 48, 36, rot=-0.3), "#9aa060", 0.5, edge=1.0, outline=0.45)
    a.wash(ellipse(545, 350, 6, 6, n=16), "#2a1e18", 0.9, layers=1, edge=0.4)
    for x in (150, 230, 360, 430):
        a.wash(ellipse(x, 405, 26, 34), "#9aa060", 0.5, edge=1.0, outline=0.4)
    a.wash(np.array([(110, 375), (60, 395), (112, 392)], float), "#9aa060", 0.5, edge=1.0, outline=0.4)
    return a


def rede():
    a = Aquarela(S, S, seed=351)
    for k in range(9):
        a.stroke(bezier((80 + k * 55, 80), (60 + k * 60, 250), (90 + k * 50, 400), (110 + k * 48, 540)), "#8a6a44", width=4, opacity=0.65)
        a.stroke(bezier((60, 100 + k * 55), (250, 80 + k * 58), (400, 110 + k * 52), (560, 90 + k * 55)), "#8a6a44", width=4, opacity=0.65)
    return a


def sapato():
    a = Aquarela(S, S, seed=361)
    corpo = np.vstack([bezier((90, 400), (80, 300), (180, 250), (260, 270)),
                       bezier((260, 270), (360, 300), (480, 300), (520, 360)),
                       bezier((520, 360), (540, 420), (480, 430), (400, 430)),
                       bezier((400, 430), (250, 430), (150, 430), (90, 400))])
    a.wash(corpo, "#4a3a2e", 0.55, color2="#6b5440", edge=1.1, outline=0.45, light=(420, 340, 20))
    a.wash(_ret(80, 425, 530, 450, 10), "#2e241c", 0.6, edge=1.0)
    a.stroke(bezier((250, 290), (280, 310), (300, 310), (330, 300)), "#c9a24a", width=6, opacity=0.8)
    return a


def gorro():
    a = Aquarela(S, S, seed=371)
    cone = np.vstack([bezier((130, 470), (180, 300), (300, 150), (440, 90)),
                      bezier((440, 90), (420, 250), (440, 380), (470, 470)),
                      bezier((470, 470), (350, 500), (250, 500), (130, 470))])
    a.wash(cone, "#c0322a", 0.6, color2="#d8503a", edge=1.1, outline=0.45, shade=(1, 0.2, 0.4))
    a.wash(ellipse(452, 92, 34, 34), "#f1e3c8", 0.5, edge=1.0, outline=0.4)
    return a


def tambor():
    a = Aquarela(S, S, seed=381)
    corpo = np.vstack([bezier((120, 230), (120, 330), (120, 420), (130, 460)),
                       bezier((130, 460), (300, 520), (300, 520), (470, 460)),
                       bezier((470, 460), (480, 420), (480, 330), (480, 230))])
    a.wash(corpo, "#c0716b", 0.5, color2="#b85a52", edge=1.1, outline=0.45, shade=(1, 0, 0.4))
    a.wash(ellipse(300, 230, 180, 50), "#efe6cf", 0.4, edge=1.0, outline=0.45)
    for k in range(7):
        x = 140 + k * 54
        a.stroke([(x, 270 + 12 * math.sin(k)), (x + 27, 440)], "#e8d7a0", width=4, opacity=0.6, taper=False)
    for ang in (-0.6, 0.6):
        a.stroke([(300 + 60 * math.sin(ang), 120), (300 + 230 * math.sin(ang), 30)], "#8a6a44", width=8, opacity=0.8)
    return a


def caminho():
    """Caminho largo pela floresta, para o labirinto de Chapeuzinho (fundo)."""
    a = Aquarela(900, 1200, seed=391)
    rng = np.random.default_rng(9)
    for _ in range(26):
        x, y = rng.uniform(40, 860), rng.uniform(40, 1160)
        a.wash(ellipse(x, y, 50, 60), "#7f9a52", 0.22, color2="#a8b860", edge=1.0, layers=2)
    return a


MOTIVOS3 = {
    "patinho": patinho, "patinho_cinza": lambda: patinho(302, "#9a948a", "#7d776e"),
    "ervilha": ervilha, "colchao_rosa": colchao,
    "colchao_azul": lambda: colchao(313, "#5f7f9c", "#8fa7bd"), "colchao_verde": lambda: colchao(314, "#7f9a52", "#a8b860"),
    "colchao_ocre": lambda: colchao(315, "#c9963f", "#e0b860"), "colchao_lilas": lambda: colchao(316, "#8a6f9e", "#b09ac0"),
    "pegada": pegada, "pegada_esq": lambda: pegada(322, True),
    "palha": palha, "madeira": madeira, "tijolos": tijolos, "tartaruga": tartaruga, "rede": rede,
    "gorro": gorro, "tambor": tambor,
}

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS3):
        MOTIVOS3[n]().image().save(os.path.join(out, f"{n}.png"))
