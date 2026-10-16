"""Motivos do Volume 5 (tintas, pincel, argila, papéis de colagem e bichos/plantas das obras), pintados com o motor de aquarela.
Padrão: 600 × 600 px (≈ 5 cm a 300 dpi)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, leaf, densify
from motivos2 import _ret

S = 600
TINTAS = {"vermelho": ("#c43a2e", "#d8604a"), "amarelo": ("#e8b830", "#f0cf5a"), "azul": ("#4f74a8", "#7f9cc9"),
          "laranja": ("#e07a28", "#eb9a52"), "roxo": ("#7a5a98", "#9a7ab4"), "verde": ("#5f8f3a", "#8fae5a"),
          "rosa": ("#d9808a", "#e8a2a8")}


def _s(txt):
    """Número estável a partir de um texto (hash() de str muda a cada execução e tiraria a repetibilidade)."""
    return sum(ord(c) * (i + 1) for i, c in enumerate(txt))


def pote(cor, seed=601):
    """Pote de guache com a tampa ao lado e a tinta à mostra."""
    a = Aquarela(S, S, seed=seed + _s(cor) % 40)
    c1, c2 = TINTAS[cor]
    corpo = np.vstack([bezier((130, 250), (120, 380), (130, 470), (170, 520)),
                       bezier((170, 520), (260, 570), (340, 570), (430, 520)),
                       bezier((430, 520), (470, 470), (480, 380), (470, 250))])
    a.wash(densify(corpo, 200), "#f2eadb", 0.35, color2="#e0d4be", edge=1.0, outline=0.5, shade=(1, 0.4, 0.4))
    a.wash(ellipse(300, 250, 170, 50), "#f2eadb", 0.3, edge=1.0, outline=0.5)
    a.wash(ellipse(300, 252, 150, 38), c1, 0.7, color2=c2, edge=1.1, light=(250, 244, 24), outline=0.4)
    a.wash(_ret(150, 380, 450, 450, 4), c1, 0.45, color2=c2, edge=0.8, soft=2)   # etiqueta da cor
    return a


def pincel(seed=611):
    a = Aquarela(S, S, seed=seed)
    cabo = np.array([(120, 540), (96, 516), (400, 170), (424, 194)], float)
    a.wash(densify(cabo, 120), "#9a6a3a", 0.6, color2="#b8884e", edge=1.0, outline=0.45)
    a.wash(densify(np.array([(398, 172), (424, 196), (450, 170), (426, 146)], float), 80), "#b8b8b8", 0.5, edge=1.0, outline=0.45)
    cerdas = np.vstack([bezier((428, 148), (470, 110), (520, 70), (548, 52)),
                        bezier((548, 52), (520, 100), (480, 150), (450, 168))])
    a.wash(densify(cerdas, 120), "#4f74a8", 0.7, color2="#7f9cc9", edge=1.0, outline=0.4)
    return a


def argila_bola(seed=621):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 310, 190, 170), "#b8764a", 0.6, color2="#a05a34", edge=1.0, granulation=1.0, light=(240, 250, 36),
           shade=(1, 0.6, 0.5), outline=0.45)
    return a


def argila_cobra(seed=631):
    a = Aquarela(S, S, seed=seed)
    linha = np.vstack([bezier((90, 400), (140, 260), (230, 260), (280, 360)), bezier((280, 360), (330, 460), (430, 460), (500, 330))])
    n = len(linha)
    d = np.gradient(linha, axis=0)
    nv = np.stack([-d[:, 1], d[:, 0]], 1)
    nv /= np.linalg.norm(nv, axis=1, keepdims=True)
    w = 44
    forma = np.vstack([linha + nv * w / 2, (linha - nv * w / 2)[::-1]])
    a.wash(densify(forma, 260), "#b8764a", 0.6, color2="#a05a34", edge=1.0, granulation=1.0, shade=(1, 0.6, 0.5), outline=0.45)
    return a


def argila_vaso(seed=641):
    """Vaso de beliscão: uma bola aberta com o polegar."""
    a = Aquarela(S, S, seed=seed)
    corpo = np.vstack([bezier((170, 250), (110, 360), (140, 500), (300, 520)),
                       bezier((300, 520), (460, 500), (490, 360), (430, 250))])
    a.wash(densify(corpo, 220), "#b8764a", 0.6, color2="#a05a34", edge=1.0, granulation=1.0, shade=(1, 0.5, 0.5), outline=0.45)
    a.wash(ellipse(300, 250, 130, 46), "#b8764a", 0.55, edge=1.0, outline=0.45)
    a.wash(ellipse(300, 256, 100, 30), "#6e3c22", 0.65, edge=1.0)
    return a


def tesoura(seed=651):
    a = Aquarela(S, S, seed=seed)
    a.wash(leaf((215, 400), (410, 50), 52), "#c8c8c8", 0.5, color2="#a8a8a8", edge=1.0, outline=0.5)
    a.wash(leaf((385, 400), (190, 50), 52), "#b4b4b4", 0.5, color2="#989898", edge=1.0, outline=0.5)
    for cx, rot in ((190, 0.35), (410, -0.35)):
        anel = ellipse(cx, 480, 62, 84, rot=rot)
        a.stroke(np.vstack([anel, anel[:3]]), "#c43a2e", width=22, opacity=0.8, taper=False)
    a.wash(ellipse(300, 300, 14, 14, n=24), "#5b4632", 0.7, edge=0.6)
    return a


def cola(seed=661):
    a = Aquarela(S, S, seed=seed)
    a.wash(densify(_ret(190, 230, 410, 540, 14), 200), "#f2eadb", 0.5, color2="#e0d4be", edge=1.0, outline=0.5)
    a.wash(densify(_ret(190, 300, 410, 440, 3), 160), "#4f74a8", 0.6, color2="#7f9cc9", edge=0.9)
    a.wash(densify(_ret(215, 140, 385, 232, 10), 160), "#c43a2e", 0.6, color2="#d8604a", edge=1.0, outline=0.45)
    return a


def papel(cor, seed=671):
    """Pedaço de papel rasgado, para a colagem."""
    a = Aquarela(S, S, seed=seed + _s(cor) % 60)
    c1, c2 = TINTAS[cor]
    rng = np.random.default_rng(_s(cor))
    f1, f2, f3 = (_s(cor) % 7) * 0.9, (_s(cor) % 5) * 1.3, (_s(cor) % 3) * 2.0
    forma = polar(300, 300, lambda t: 200 + 40 * math.sin(2 * t + f1) + 25 * math.sin(3 * t + f2) + 15 * math.sin(5 * t + f3) + rng.normal(0, 3), n=240)
    a.wash(densify(forma, 260), c1, 0.55, color2=c2, edge=0.8, granulation=0.7, outline=0.2)
    return a


def ninfeia(seed=681):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 340, 250, 120), "#6f9a5a", 0.55, color2="#4f7a4a", edge=1.0, outline=0.3)
    a.lift(np.array([(300, 340), (560, 330), (560, 300), (300, 330)], float), 0.0)
    for k, (dx, dy, esc) in enumerate(((0, 0, 1.0), (-60, 8, 0.8), (60, 8, 0.8))):
        for ang in np.linspace(-1.1, 1.1, 5):
            base = (300 + dx, 330 + dy)
            tip = (300 + dx + 110 * esc * math.sin(ang), 330 + dy - 150 * esc * math.cos(ang))
            a.wash(leaf(base, tip, 56 * esc), "#f2c2cf", 0.5, color2="#e49ab0", edge=1.0, layers=2, outline=0.25)
    a.wash(ellipse(300, 318, 30, 20), "#e8b830", 0.7, edge=0.9)
    return a


def lebre(seed=691):
    a = Aquarela(S, S, seed=seed)
    corpo = np.vstack([bezier((130, 470), (110, 330), (230, 250), (350, 280)),
                       bezier((350, 280), (460, 310), (490, 420), (470, 500)),
                       bezier((470, 500), (380, 530), (230, 530), (130, 470))])
    a.wash(densify(corpo, 240), "#a07a52", 0.55, color2="#8a6540", edge=1.0, granulation=0.9, shade=(1, 0.5, 0.5), outline=0.45)
    cab = np.vstack([bezier((330, 290), (320, 210), (390, 170), (460, 200)),
                     bezier((460, 200), (500, 218), (520, 240), (532, 258)),
                     bezier((532, 258), (500, 290), (420, 320), (360, 320)),
                     bezier((360, 320), (340, 320), (332, 308), (330, 290))])
    a.wash(densify(cab, 200), "#a98458", 0.55, color2="#8a6540", edge=1.0, outline=0.45, granulation=0.9)
    for rot, x in ((-0.2, 372), (0.15, 420)):
        a.wash(ellipse(x, 120, 26, 90, rot=rot), "#a07a52", 0.5, edge=1.0, outline=0.45)
        a.wash(ellipse(x, 124, 12, 66, rot=rot), "#e0a8a0", 0.4, edge=0.6)
    a.wash(ellipse(440, 226, 9, 9, n=24), "#2e1e10", 0.9, edge=0.5)
    a.wash(ellipse(150, 495, 26, 22), "#efe6d6", 0.45, edge=0.6)
    return a


def tufo(seed=701):
    a = Aquarela(S, S, seed=seed)
    rng = np.random.default_rng(7)
    for i in range(26):
        x0 = 300 + rng.uniform(-110, 110)
        x1 = x0 + rng.uniform(-150, 150)
        h = rng.uniform(250, 480)
        a.wash(leaf((x0, 560), (x1, 560 - h), rng.uniform(16, 30)), ("#5f8f3a", "#7aa04a", "#4f7a32")[i % 3], 0.5, edge=1.0, layers=2, outline=0.15)
    a.wash(ellipse(300, 566, 160, 24), "#6e4a2a", 0.55, edge=1.0, granulation=1.0)
    return a


MOTIVOS6 = {"pincel": pincel, "argila_bola": argila_bola, "argila_cobra": argila_cobra, "argila_vaso": argila_vaso,
            "tesoura": tesoura, "cola": cola, "ninfeia": ninfeia, "lebre": lebre, "tufo": tufo}
for c in ("vermelho", "amarelo", "azul"):
    MOTIVOS6[f"pote_{c}"] = (lambda c=c: pote(c))
for c in TINTAS:
    MOTIVOS6[f"papel_{c}"] = (lambda c=c: papel(c))
for c in ("laranja", "roxo"):
    MOTIVOS6[f"circulo_{c}"] = (lambda c=c: (lambda a: a)(_circulo(c)))


def _circulo(cor):
    a = Aquarela(S, S, seed=711 + _s(cor) % 50)
    c1, c2 = TINTAS[cor]
    a.wash(ellipse(300, 300, 230, 230, n=200), c1, 0.5, color2=c2, edge=1.1, outline=0.45)
    return a


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS6):
        MOTIVOS6[n]().image().save(os.path.join(out, f"{n}.png"))
