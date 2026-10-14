"""
Motivos do Volume 1 (casa, sentidos, céu, água, estações), pintados com o motor de aquarela.
Padrão: 600 × 600 px (≈ 5 cm a 300 dpi), salvo indicação.
"""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf, densify
from motivos import _contour

S = 600
SEPIA = "#5b4632"


def _ret(x0, y0, x1, y1, r=0):
    """Retângulo (com cantos arredondados opcionais) como polígono."""
    if r <= 0:
        return np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], float)
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for a in np.linspace(a0, a0 + 90, 10):
            pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    return np.array(pts)


# ------------------------------------------------------------------ casa

def xicara():
    a = Aquarela(S, S, seed=201)
    a.wash(ellipse(300, 470, 230, 50), "#c9d3dc", 0.4, color2="#e3e8ec", edge=1.0, outline=0.35)   # pires
    body = np.vstack([bezier((130, 230), (130, 420), (200, 470), (300, 470)),
                      bezier((300, 470), (400, 470), (470, 420), (470, 230)),
                      bezier((470, 230), (400, 255), (200, 255), (130, 230))])
    a.wash(body, "#e8eef3", 0.35, color2="#d6e0e8", edge=1.0, shade=(1, 0.5, 0.5), shade_color="#9fb2c4", outline=0.45)
    a.wash(ellipse(300, 232, 170, 26), "#9a6a3e", 0.45, edge=0.8)          # chá
    handle = np.vstack([bezier((462, 270), (560, 250), (570, 380), (455, 400), n=40),
                        bezier((455, 400), (530, 360), (525, 290), (462, 300), n=40)])
    a.wash(handle, "#e0e7ed", 0.4, edge=1.0, outline=0.45)
    for x in (200, 300, 400):                                               # florzinhas azuis
        for k in range(5):
            ang = k * 2 * math.pi / 5
            a.wash(ellipse(x + 11 * math.cos(ang), 355 + 11 * math.sin(ang), 8, 6, n=20, rot=ang), "#6f8fb8", 0.6,
                   layers=1, edge=0.8)
    return a


def colher():
    a = Aquarela(S, S, seed=202)
    bowl = polar(300, 175, lambda t: 95 * (1 - 0.18 * math.sin(t)) * (1 + 0.35 * max(0, math.sin(t)) ** 2), rot=0)
    bowl[:, 1] = 175 + (bowl[:, 1] - 175) * 1.25
    a.wash(bowl, "#b9c2c9", 0.45, color2="#dfe4e8", edge=1.1, light=(270, 140, 22), shade=(1, 0.6, 0.5), outline=0.45)
    cabo = np.vstack([bezier((285, 290), (290, 400), (270, 500), (275, 565), n=40),
                      bezier((275, 565), (300, 585), (330, 575), (328, 560), n=10),
                      bezier((328, 560), (320, 480), (312, 400), (315, 290), n=40)])
    a.wash(cabo, "#aeb8c0", 0.45, color2="#d5dbe0", edge=1.0, outline=0.45)
    return a


def prato():
    a = Aquarela(S, S, seed=203)
    a.wash(ellipse(300, 300, 265, 150), "#eef2f4", 0.35, color2="#dde4ea", edge=1.0, outline=0.45)
    a.wash(ellipse(300, 300, 175, 95), "#e3e9ee", 0.3, edge=0.9, shade=(1, 0.8, 0.4), shade_color="#a9b8c6")
    for k in range(14):   # barrado azul
        ang = k * 2 * math.pi / 14
        a.wash(ellipse(300 + 222 * math.cos(ang), 300 + 124 * math.sin(ang), 14, 8, n=20, rot=ang), "#5f7fa8",
               0.55, layers=1, edge=0.8)
    return a


def tigela():
    a = Aquarela(S, S, seed=204)
    body = np.vstack([bezier((80, 250), (90, 470), (200, 520), (300, 520)),
                      bezier((300, 520), (400, 520), (510, 470), (520, 250)),
                      bezier((520, 250), (400, 285), (200, 285), (80, 250))])
    a.wash(body, "#e8d7b0", 0.45, color2="#d6c08e", edge=1.0, shade=(1, 0.5, 0.5), outline=0.45)
    a.wash(ellipse(300, 250, 220, 42), "#f2e6c8", 0.35, edge=0.9, outline=0.4)
    a.wash(ellipse(300, 258, 190, 30), "#e9dcc0", 0.35, edge=0.6)       # mingau
    a.stroke(bezier((110, 330), (200, 360), (400, 360), (490, 330)), "#6f8f48", width=7, opacity=0.6)
    a.wash(ellipse(300, 535, 120, 14), "#c9b48a", 0.4, edge=0.8)
    return a


def vela():
    a = Aquarela(S, S, seed=205)
    a.wash(ellipse(300, 520, 170, 45), "#b8863a", 0.5, color2="#d4a352", edge=1.0, outline=0.4)   # castiçal
    a.wash(_ret(245, 220, 355, 515, 10), "#f3ead6", 0.35, color2="#e8dcc0", edge=1.0, shade=(1, 0, 0.5), outline=0.45)
    a.stroke([(300, 220), (302, 195)], "#3a2a1a", width=5, opacity=0.9)
    chama = np.vstack([bezier((300, 90), (330, 140), (335, 180), (300, 198), n=30),
                       bezier((300, 198), (265, 180), (270, 140), (300, 90), n=30)])
    a.wash(chama, "#f0b43a", 0.6, color2="#e8862e", edge=1.0)
    a.wash(ellipse(300, 172, 10, 18, n=24), "#f6e08a", 0.6, layers=1, edge=0.5)
    return a


def chave():
    a = Aquarela(S, S, seed=206)
    anel = polar(170, 300, lambda t: 95)
    a.wash(anel, "#c9a24a", 0.55, color2="#a8822e", edge=1.1, outline=0.45)
    a.lift(ellipse(170, 300, 45, 45), 0.95)
    a.wash(_ret(255, 280, 520, 322, 6), "#c39a42", 0.55, color2="#a8822e", edge=1.0, outline=0.45)
    a.wash(_ret(440, 318, 470, 390, 3), "#b8903a", 0.55, edge=1.0, outline=0.4)
    a.wash(_ret(490, 318, 518, 370, 3), "#b8903a", 0.55, edge=1.0, outline=0.4)
    return a


def livro():
    a = Aquarela(S, S, seed=207)
    capa = np.array([(120, 170), (470, 120), (500, 430), (150, 480)], float)
    a.wash(capa, "#7a3a34", 0.55, color2="#9a4a40", edge=1.0, outline=0.45, shade=(1, 0.5, 0.4))
    a.wash(np.array([(150, 480), (500, 430), (500, 455), (152, 505)], float), "#efe6cf", 0.4, edge=0.8, outline=0.4)
    a.wash(np.array([(470, 120), (500, 430), (515, 440), (486, 128)], float), "#e9dfc4", 0.4, edge=0.8, outline=0.35)
    a.wash(ellipse(310, 300, 85, 70, rot=-0.12), "#c9a24a", 0.4, edge=1.0)
    a.wash(ellipse(310, 300, 55, 44, rot=-0.12), "#7a3a34", 0.35, edge=0.8)
    return a


def mesa():
    a = Aquarela(S, S, seed=208)
    tampo = np.array([(70, 230), (530, 230), (560, 290), (40, 290)], float)
    a.wash(tampo, "#b4824c", 0.5, color2="#9a6a3a", edge=1.0, outline=0.45, granulation=0.9)
    a.wash(_ret(40, 290, 560, 318), "#8a5e34", 0.55, edge=1.0, outline=0.4)
    for x in (70, 500):
        a.wash(_ret(x, 318, x + 30, 540, 4), "#8a5e34", 0.55, edge=1.0, outline=0.4)
    for x in (130, 440):
        a.wash(_ret(x, 318, x + 24, 500, 4), "#a07446", 0.4, edge=0.9, outline=0.3)
    return a


def jarra():
    a = Aquarela(S, S, seed=209)
    body = np.vstack([bezier((220, 140), (170, 260), (150, 420), (210, 520)),
                      bezier((210, 520), (300, 545), (380, 540), (400, 520)),
                      bezier((400, 520), (450, 420), (430, 260), (380, 140)),
                      bezier((380, 140), (330, 128), (270, 128), (220, 140))])
    a.wash(body, "#dfe8ee", 0.35, color2="#c8d6e0", edge=1.0, outline=0.45, shade=(1, 0.3, 0.4), shade_color="#8fa7bd")
    agua = np.vstack([bezier((180, 300), (250, 315), (350, 315), (430, 300)),
                      bezier((430, 300), (450, 420), (420, 500), (400, 520)),
                      bezier((400, 520), (300, 545), (220, 530), (210, 520)),
                      bezier((210, 520), (165, 430), (170, 340), (180, 300))])
    a.wash(agua, "#7fa3c4", 0.35, color2="#a7c2d8", edge=1.0)
    a.wash(np.vstack([bezier((380, 150), (480, 120), (500, 160), (430, 175))]), "#d6e2ea", 0.35, edge=0.8, outline=0.35)
    alca = np.vstack([bezier((225, 190), (110, 200), (110, 390), (195, 400), n=40),
                      bezier((195, 400), (140, 360), (150, 240), (222, 225), n=40)])
    a.wash(alca, "#d2dde5", 0.4, edge=1.0, outline=0.45)
    return a


def sabonete():
    a = Aquarela(S, S, seed=210)
    a.wash(_ret(150, 260, 450, 420, 60), "#e9b9b0", 0.45, color2="#f2d2c8", edge=1.0, outline=0.45, shade=(0.3, 1, 0.5))
    for (x, y, r) in ((200, 200, 40), (270, 150, 28), (330, 205, 50), (420, 160, 34), (380, 100, 22), (470, 230, 26)):
        a.wash(ellipse(x, y, r, r, n=60), "#9fc2d8", 0.18, edge=2.2, layers=2, light=(x - r * 0.35, y - r * 0.35, r * 0.18))
    return a


def toalha():
    a = Aquarela(S, S, seed=211)
    a.stroke(bezier((90, 140), (250, 130), (350, 130), (510, 140)), "#8a6a44", width=10, opacity=0.8)
    pano = np.array([(150, 140), (450, 140), (470, 520), (130, 520)], float)
    a.wash(pano, "#f1ece0", 0.35, color2="#e6dfcd", edge=1.0, outline=0.45, shade=(1, 0.3, 0.3))
    for y in (440, 470):
        a.wash(np.array([(133, y), (467, y), (468, y + 16), (132, y + 16)], float), "#c0716b", 0.5, layers=2, edge=0.8)
    return a


# ------------------------------------------------------------------ sentidos

def sino():
    a = Aquarela(S, S, seed=221)
    body = np.vstack([bezier((300, 110), (200, 110), (190, 250), (175, 360)),
                      bezier((175, 360), (165, 420), (120, 440), (110, 460)),
                      bezier((110, 460), (300, 490), (300, 490), (490, 460)),
                      bezier((490, 460), (480, 440), (435, 420), (425, 360)),
                      bezier((425, 360), (410, 250), (400, 110), (300, 110))])
    a.wash(body, "#d4a83c", 0.55, color2="#b8862e", edge=1.1, light=(245, 250, 30), shade=(1, 0.4, 0.5), outline=0.45)
    a.wash(ellipse(300, 495, 30, 28), "#a8782a", 0.6, edge=1.0, outline=0.4)
    a.wash(polar(300, 85, lambda t: 30), "#c99a36", 0.5, edge=1.0, outline=0.4)
    a.lift(ellipse(300, 85, 14, 14), 0.9)
    for k, (r, op) in enumerate(((60, 0.4), (95, 0.3))):  # ondas de som
        for sgn in (-1, 1):
            cx = 300 + sgn * 235
            a.stroke(bezier((cx, 250 - r * 0.6), (cx + sgn * r * 0.4, 280), (cx + sgn * r * 0.4, 330), (cx, 360 + r * 0.6)),
                     "#8a6f9e", width=4, opacity=op)
    return a


def pena():
    a = Aquarela(S, S, seed=222)
    base, tip = np.array([170, 520]), np.array([470, 80])
    a.wash(leaf(base + (20, -30), tip, 150, asym=0.15), "#c9d6e0", 0.35, color2="#9fb6c9", edge=1.2, granulation=1.0, outline=0.3)
    a.stroke(np.linspace(base, tip, 50), "#6b5a44", width=4, opacity=0.7)
    u = (tip - base) / np.linalg.norm(tip - base)
    v = np.array([-u[1], u[0]])
    for t in np.linspace(0.15, 0.9, 16):
        p = base + (tip - base) * t
        w = 70 * math.sin(math.pi * (t - 0.1) / 0.85)
        for sgn in (1, -1):
            a.stroke(bezier(p, p + v * sgn * w * 0.5 + u * 10, p + v * sgn * w + u * 25, p + v * sgn * w + u * 40),
                     "#7f97ab", width=1.6, opacity=0.4, taper=False)
    return a


def lupa():
    a = Aquarela(S, S, seed=223)
    a.wash(ellipse(250, 250, 165, 165), "#7a5a3a", 0.6, edge=1.1, outline=0.45)
    a.lift(ellipse(250, 250, 140, 140), 0.97)
    a.wash(ellipse(250, 250, 140, 140), "#cfe0ea", 0.2, edge=1.4, light=(200, 200, 40))
    cabo = np.array([(355, 360), (385, 330), (540, 500), (505, 530)], float)
    a.wash(cabo, "#7a4a2a", 0.6, color2="#9a6a3a", edge=1.0, outline=0.45)
    # joaninha vista através da lente
    a.wash(ellipse(250, 265, 55, 45), "#c8352e", 0.65, edge=1.0, outline=0.4)
    a.stroke([(250, 222), (250, 308)], "#2a1e18", width=3, opacity=0.8)
    a.wash(ellipse(250, 218, 26, 18), "#2a1e18", 0.8, layers=1, edge=0.4)
    for (x, y) in ((228, 250), (272, 250), (232, 285), (268, 285)):
        a.wash(ellipse(x, y, 9, 9, n=20), "#2a1e18", 0.8, layers=1, edge=0.4)
    return a


def mel():
    a = Aquarela(S, S, seed=224)
    pote = np.vstack([bezier((190, 200), (130, 280), (130, 470), (200, 520)),
                      bezier((200, 520), (300, 545), (300, 545), (400, 520)),
                      bezier((400, 520), (470, 470), (470, 280), (410, 200)),
                      bezier((410, 200), (350, 185), (250, 185), (190, 200))])
    a.wash(pote, "#e8a83a", 0.55, color2="#d48a2a", edge=1.1, light=(230, 330, 34), shade=(1, 0.4, 0.4), outline=0.45)
    a.wash(_ret(180, 150, 420, 205, 12), "#e7dcc4", 0.45, edge=1.0, outline=0.45)
    a.wash(_ret(225, 310, 375, 400, 8), "#f3ead6", 0.5, edge=0.8, outline=0.35)
    a.stroke(bezier((360, 140), (370, 80), (420, 60), (470, 70)), "#8a6a44", width=12, opacity=0.8)
    return a


# ------------------------------------------------------------------ céu

def sol():
    a = Aquarela(S, S, seed=231)
    for k in range(12):
        ang = k * math.pi / 6
        p0 = (300 + 150 * math.cos(ang), 300 + 150 * math.sin(ang))
        p1 = (300 + 255 * math.cos(ang), 300 + 255 * math.sin(ang))
        a.wash(leaf(p0, p1, 46), "#efb33a", 0.5, color2="#f4cf5a", edge=1.1, layers=2)
    a.wash(ellipse(300, 300, 135, 135), "#f2c040", 0.55, color2="#e8962e", edge=1.1, outline=0.3)
    return a


def lua():
    a = Aquarela(S, S, seed=232)
    yy, xx = np.mgrid[0:S, 0:S]
    m = ((xx - 300) ** 2 + (yy - 300) ** 2 < 210 ** 2) & ((xx - 390) ** 2 + (yy - 250) ** 2 > 175 ** 2)
    pts = densify(_contour(m), 200)
    a.wash(pts, "#e9d68a", 0.5, color2="#f1e3a8", edge=1.1, outline=0.4, granulation=0.9)
    return a


def estrela(seed=233, cor="#efc04a"):
    a = Aquarela(S, S, seed=seed)
    pts = []
    for k in range(10):
        r = 240 if k % 2 == 0 else 100
        ang = -math.pi / 2 + k * math.pi / 5
        pts.append((300 + r * math.cos(ang), 315 + r * math.sin(ang)))
    a.wash(np.array(pts), cor, 0.55, color2="#f4dc7a", edge=1.1, outline=0.4)
    return a


def guarda_chuva():
    a = Aquarela(S, S, seed=234)
    topo = np.vstack([bezier((70, 300), (90, 90), (510, 90), (530, 300), n=80)])
    rec = []
    for k in range(4):
        x0 = 70 + k * 115
        rec.append(bezier((x0 + 115, 300), (x0 + 95, 270), (x0 + 20, 270), (x0, 300), n=20))
    pts = np.vstack([topo] + rec)
    a.wash(pts, "#5f7f9c", 0.55, color2="#7f9cb8", edge=1.1, outline=0.45, shade=(1, 0.3, 0.4))
    a.stroke(bezier((300, 120), (300, 300), (300, 420), (300, 500)), "#5b4632", width=7, opacity=0.85)
    a.stroke(bezier((300, 500), (300, 545), (250, 550), (245, 515)), "#5b4632", width=8, opacity=0.85)
    for x in (185, 300, 415):
        a.stroke(bezier((300, 105), (x, 160), (x, 230), (x, 290)), "#3f5a74", width=2, opacity=0.4)
    return a


def chapeu():
    a = Aquarela(S, S, seed=235)
    a.wash(ellipse(300, 360, 260, 85), "#e2c27a", 0.5, color2="#d1aa5a", edge=1.0, outline=0.45, granulation=1.0)
    copa = np.vstack([bezier((180, 350), (180, 200), (420, 200), (420, 350)),
                      bezier((420, 350), (350, 375), (250, 375), (180, 350))])
    a.wash(copa, "#e6c985", 0.5, color2="#d1aa5a", edge=1.0, outline=0.45, shade=(1, 0.2, 0.4), granulation=1.0)
    fita = np.vstack([bezier((182, 325), (250, 345), (350, 345), (418, 325)),
                      bezier((418, 325), (420, 355), (420, 355), (418, 352)),
                      bezier((418, 352), (350, 372), (250, 372), (182, 352))])
    a.wash(fita, "#c0716b", 0.6, edge=1.0)
    return a


def bota():
    a = Aquarela(S, S, seed=236)
    cano = np.vstack([bezier((200, 90), (195, 250), (200, 350), (190, 430), n=40),
                      bezier((190, 430), (180, 500), (200, 530), (260, 535), n=30),
                      bezier((260, 535), (380, 540), (480, 545), (500, 505), n=30),
                      bezier((500, 505), (510, 460), (440, 430), (370, 420), n=30),
                      bezier((370, 420), (350, 380), (355, 250), (360, 90), n=40),
                      bezier((360, 90), (300, 80), (260, 80), (200, 90), n=20)])
    a.wash(cano, "#d8b03a", 0.55, color2="#e8c84a", edge=1.1, light=(245, 250, 30), outline=0.45, shade=(1, 0.3, 0.4))
    a.wash(np.vstack([bezier((185, 520), (300, 560), (420, 565), (505, 515), n=40),
                      bezier((505, 515), (505, 545), (500, 560), (490, 565), n=10),
                      bezier((490, 565), (400, 580), (280, 575), (185, 545), n=40)]), "#5b4632", 0.6, edge=1.0)
    return a


def luva():
    a = Aquarela(S, S, seed=237)
    mao = np.vstack([bezier((200, 470), (150, 330), (170, 160), (300, 140)),
                     bezier((300, 140), (420, 135), (440, 300), (420, 470))])
    a.wash(mao, "#5f8f8a", 0.55, color2="#7fa8a2", edge=1.0, outline=0.45)
    polegar = np.vstack([bezier((205, 360), (120, 340), (90, 250), (140, 220)),
                         bezier((140, 220), (190, 230), (200, 290), (215, 300))])
    a.wash(polegar, "#5f8f8a", 0.55, color2="#7fa8a2", edge=1.0, outline=0.45)
    a.wash(_ret(190, 460, 430, 540, 10), "#e9dfc4", 0.5, edge=1.0, outline=0.45)
    for x in range(205, 425, 22):
        a.stroke([(x, 465), (x, 535)], "#b9a88a", width=3, opacity=0.5, taper=False)
    return a


# ------------------------------------------------------------------ água

def peixe(seed=241, cor="#e8862e"):
    a = Aquarela(S, S, seed=seed)
    corpo = np.vstack([bezier((120, 300), (200, 170), (400, 170), (450, 300)),
                       bezier((450, 300), (400, 430), (200, 430), (120, 300))])
    a.wash(corpo, cor, 0.55, color2="#f0b43a", edge=1.1, outline=0.45, shade=(0, 1, 0.4))
    cauda = np.array([(440, 300), (560, 210), (530, 300), (560, 390)], float)
    a.wash(cauda, cor, 0.5, color2="#f0b43a", edge=1.1, outline=0.4)
    a.wash(ellipse(190, 280, 14, 14), "#2a1e18", 0.85, layers=1, edge=0.4)
    a.lift(ellipse(186, 276, 4, 4, n=12), 0.9, soft=0.4)
    for x in (260, 310, 360):
        a.stroke(bezier((x, 230), (x + 20, 270), (x + 20, 330), (x, 370)), "#b85a1e", width=2.2, opacity=0.35)
    return a


def bolhas():
    a = Aquarela(S, S, seed=242)
    rng = np.random.default_rng(3)
    for _ in range(9):
        x, y, r = rng.uniform(120, 480), rng.uniform(120, 480), rng.uniform(30, 85)
        a.wash(ellipse(x, y, r, r, n=70), "#8fb6cc", 0.16, edge=2.4, layers=2, light=(x - r * 0.4, y - r * 0.4, r * 0.18))
    return a


def pedra():
    a = Aquarela(S, S, seed=243)
    p = polar(300, 330, lambda t: 190 * (1 + 0.12 * math.cos(3 * t + 1) + 0.06 * math.sin(5 * t)))
    p[:, 1] = 330 + (p[:, 1] - 330) * 0.7
    a.wash(p, "#9a948a", 0.55, color2="#7d776e", edge=1.0, outline=0.45, shade=(1, 0.6, 0.5), granulation=1.4)
    return a


def rolha():
    a = Aquarela(S, S, seed=244)
    corpo = np.vstack([bezier((200, 180), (200, 300), (215, 420), (225, 470)),
                       bezier((225, 470), (300, 495), (300, 495), (375, 470)),
                       bezier((375, 470), (385, 420), (400, 300), (400, 180))])
    a.wash(corpo, "#c49a62", 0.5, color2="#a87a42", edge=1.0, outline=0.45, granulation=1.6)
    a.wash(ellipse(300, 180, 100, 30), "#b88a52", 0.5, edge=1.0, outline=0.45, granulation=1.6)
    a.spatter((300, 330), 120, "#7a5530", n=60, size=(1.5, 3.5), opacity=0.4)
    return a


# ------------------------------------------------------------------ estações

def arvore(estacao="verao", seed=251, w=600, h=700):
    a = Aquarela(w, h, seed=seed)
    tronco = np.vstack([bezier((270, 690), (285, 560), (280, 470), (260, 380)),
                        bezier((260, 380), (300, 430), (320, 430), (345, 380)),
                        bezier((345, 380), (320, 470), (318, 560), (335, 690))])
    a.wash(tronco, "#7a5a3a", 0.55, color2="#5a4030", edge=1.0, outline=0.45, granulation=1.2)
    for (p0, p1) in (((285, 420), (190, 300)), ((320, 410), (420, 280)), ((300, 400), (300, 230))):
        a.stroke(bezier(p0, (p0[0] + p1[0]) / 2, (p0[0] + p1[0]) / 2 + 10, p1), "#6b4e34", width=10, opacity=0.7)
    copa = [(300, 270, 200, 150), (180, 320, 110, 90), (420, 320, 110, 90), (300, 170, 130, 90)]
    rng = np.random.default_rng(seed)
    if estacao == "inverno":
        for (p0, p1) in (((200, 300), (130, 220)), ((420, 280), (480, 200)), ((300, 230), (330, 120)),
                         ((250, 330), (200, 380)), ((360, 320), (420, 360))):
            a.stroke(bezier(p0, p0, p1, p1), "#6b4e34", width=6, opacity=0.6)
        for (x, y, rx) in ((140, 222, 30), (480, 202, 26), (330, 122, 26), (300, 232, 40)):
            a.wash(ellipse(x, y, rx, 10), "#dfe8f0", 0.4, edge=1.2, layers=2, outline=0.25)
        a.wash(ellipse(300, 690, 300, 40), "#e3ebf2", 0.4, edge=1.0, layers=2)
        a.spatter((300, 300), 300, "#b9c9d8", n=70, size=(3, 6), opacity=0.35)
        return a
    cores = {"primavera": ("#8fae5a", "#b7c46a"), "verao": ("#4f7a3a", "#7f9a52"),
             "outono": ("#c8782e", "#d9a03a")}[estacao]
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.zeros((h, w), bool)
    for (x, y, rx, ry) in copa:
        m |= ((xx - x) / rx) ** 2 + ((yy - y) / ry) ** 2 < 1
    contorno_copa = densify(_contour(m), 260)
    a.wash(contorno_copa, cores[0], 0.45, color2=cores[1], edge=1.1, layers=3, outline=0.3, bloom=0.5)
    for (x, y, rx, ry) in copa[1:]:   # volumes internos, bem leves
        a.wash(ellipse(x, y + ry * 0.25, rx * 0.7, ry * 0.55, n=100), cores[0], 0.12, edge=0.6, layers=2)
    if estacao == "primavera":
        for _ in range(45):
            x, y = 300 + rng.normal(0, 120), 260 + rng.normal(0, 80)
            a.wash(ellipse(x, y, 9, 8, n=16), "#f0b8c0", 0.6, layers=1, edge=0.9)
    if estacao == "verao":
        for _ in range(9):
            x, y = 300 + rng.normal(0, 110), 280 + rng.normal(0, 60)
            a.wash(ellipse(x, y, 14, 14, n=24), "#c8352e", 0.65, layers=1, edge=0.9, light=(x - 4, y - 4, 3))
    if estacao == "outono":
        for _ in range(16):
            x, y = rng.uniform(80, 520), rng.uniform(420, 680)
            ang = rng.uniform(0, math.pi)
            a.wash(leaf((x, y), (x + 30 * math.cos(ang), y + 30 * math.sin(ang)), 16), "#c8602e", 0.6, layers=1, edge=0.9)
    a.wash(ellipse(300, 690, 280, 26), "#7f9a52" if estacao != "outono" else "#a8884a", 0.35, edge=0.8, layers=2)
    return a


def paisagem(momento, w=900, h=640, seed=261):
    """Mesma paisagem em quatro momentos do dia: amanhecer, meio-dia, entardecer, noite."""
    a = Aquarela(w, h, seed=seed)
    ceu = {"amanhecer": ("#f2c8a0", "#c9d8e8"), "meiodia": ("#a9c6de", "#cfe0ee"),
           "entardecer": ("#e8a070", "#c88a9a"), "noite": ("#3f4f74", "#5a6a8e")}[momento]
    a.wash(np.array([(0, 0), (w, 0), (w, 470), (0, 470)], float), ceu[0], 0.45, color2=ceu[1], edge=0.3, layers=2,
           wobble=0.5)
    astro = {"amanhecer": (220, 400, 60, "#f0a040"), "meiodia": (450, 120, 62, "#f2c040"),
             "entardecer": (680, 390, 62, "#e8702e"), "noite": (680, 130, 50, "#efe2a8")}[momento]
    x, y, r, c = astro
    if momento == "noite":
        yy, xx = np.mgrid[0:h, 0:w]
        m = ((xx - x) ** 2 + (yy - y) ** 2 < r ** 2) & ((xx - x - 24) ** 2 + (yy - y + 12) ** 2 > (r * 0.85) ** 2)
        lua_pts = densify(_contour(m), 120)
        a.lift(lua_pts, 0.95)
        a.wash(lua_pts, c, 0.6, edge=1.1, layers=2)
    else:
        a.wash(ellipse(x, y, r, r), c, 0.65, edge=1.1, layers=2)
    if momento == "noite":
        rng = np.random.default_rng(1)
        for _ in range(16):
            sx, sy = rng.uniform(40, 860), rng.uniform(30, 380)
            a.lift(ellipse(sx, sy, 6, 6, n=12), 0.95, soft=0.6)
            a.wash(ellipse(sx, sy, 5, 5, n=12), "#f4e6a8", 0.6, layers=1, edge=0.4)
    morro1 = np.vstack([[(0, 640)], bezier((0, 420), (250, 330), (500, 420), (900, 380), n=80), [(900, 640)]])
    morro2 = np.vstack([[(0, 640)], bezier((0, 500), (300, 440), (600, 520), (900, 470), n=80), [(900, 640)]])
    escuro = momento == "noite"
    a.wash(morro1, "#5f7a4a" if not escuro else "#2e3a3a", 0.5, color2="#7f9a52" if not escuro else "#3a4a44",
           edge=0.8, layers=2, wobble=2)
    a.wash(morro2, "#7f9a52" if not escuro else "#34443a", 0.5, color2="#a8b860" if not escuro else "#3e4e40",
           edge=0.8, layers=2, wobble=2)
    casa = np.array([(160, 470), (250, 470), (250, 540), (160, 540)], float)
    a.wash(casa, "#efe6cf" if not escuro else "#5a5a5a", 0.5, edge=1.0, outline=0.4)
    a.wash(np.array([(150, 472), (205, 425), (260, 472)], float), "#a0503a" if not escuro else "#4a3a34", 0.55,
           edge=1.0, outline=0.4)
    janela = np.array([(195, 495), (215, 495), (215, 515), (195, 515)], float)
    if escuro:
        a.lift(janela, 0.95, soft=0.5)
    a.wash(janela,
           "#f2c040" if momento in ("noite", "entardecer") else "#6f8fb8", 0.7, edge=0.6, layers=1)
    return a


def contorno(funcao, *args, **kw):
    """Versão para colorir: só o contorno a lápis, mais escuro, sem aguada."""
    import aquarela
    original = aquarela.Aquarela.wash

    def so_contorno(self, pts, *a, **k):
        pts = np.asarray(pts, float)
        if len(pts) < 60:
            pts = densify(pts, 160)
        opacidade = a[1] if len(a) > 1 else k.get("opacity", 0.55)
        if opacidade >= 0.2:   # aguadas muito leves (volumes internos) não viram linha
            fechado = np.vstack([pts, pts[:1]])   # linha contínua: para colorir, o contorno precisa fechar
            self.stroke(fechado, "#4a3a2a", width=4.2, opacity=0.9, taper=False)
        return None

    aquarela.Aquarela.wash = so_contorno
    try:
        out = funcao(*args, **kw)
    finally:
        aquarela.Aquarela.wash = original
    return out


def maca_cortada():
    """Maçã cortada ao meio, atravessada: a estrela de cinco sementes."""
    a = Aquarela(S, S, seed=212)
    a.wash(polar(300, 300, lambda t: 250 * (1 + 0.04 * math.cos(5 * t))), "#c43a2e", 0.55, color2="#9e2a2f",
           edge=1.1, outline=0.45)
    a.lift(polar(300, 300, lambda t: 232 * (1 + 0.04 * math.cos(5 * t))), 0.95)
    a.wash(polar(300, 300, lambda t: 232 * (1 + 0.04 * math.cos(5 * t))), "#f4ecc8", 0.4, color2="#ece0b0", edge=0.9)
    estrela = []
    for k in range(10):
        r = 105 if k % 2 == 0 else 38
        ang = -math.pi / 2 + k * math.pi / 5
        estrela.append((300 + r * math.cos(ang), 300 + r * math.sin(ang)))
    a.wash(np.array(estrela), "#d8c890", 0.45, edge=1.2, outline=0.35)
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        x, y = 300 + 70 * math.cos(ang), 300 + 70 * math.sin(ang)
        a.wash(ellipse(x, y, 11, 20, n=30, rot=ang + math.pi / 2), "#4a2e1a", 0.8, layers=1, edge=0.6)
    return a


MOTIVOS2 = {
    "xicara": xicara, "colher": colher, "prato": prato, "tigela": tigela, "vela": vela, "chave": chave,
    "livro": livro, "maca_cortada": maca_cortada, "mesa": mesa, "jarra": jarra, "sabonete": sabonete, "toalha": toalha,
    "sino": sino, "pena": pena, "lupa": lupa, "mel": mel,
    "sol": sol, "lua": lua, "estrela": estrela, "guarda_chuva": guarda_chuva, "chapeu": chapeu,
    "bota": bota, "luva": luva,
    "peixe": peixe, "peixe_azul": lambda: peixe(245, "#5f8fb0"), "bolhas": bolhas, "pedra": pedra, "rolha": rolha,
    "arvore_primavera": lambda: arvore("primavera", 251), "arvore_verao": lambda: arvore("verao", 252),
    "arvore_outono": lambda: arvore("outono", 253), "arvore_inverno": lambda: arvore("inverno", 254),
    "dia_amanhecer": lambda: paisagem("amanhecer"), "dia_meiodia": lambda: paisagem("meiodia"),
    "dia_entardecer": lambda: paisagem("entardecer"), "dia_noite": lambda: paisagem("noite"),
}

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS2):
        MOTIVOS2[n]().image().save(os.path.join(out, f"{n}.png"))
        print("ok", n, flush=True)
