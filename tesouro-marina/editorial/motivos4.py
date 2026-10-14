"""Motivos do Volume 3 (número, forma, padrão, medida)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, polar, bezier, densify
from motivos2 import _ret

S = 600
CORES = {"vermelho": ("#c43a2e", "#d8604a"), "azul": ("#4f74a8", "#7f9cc9"), "amarelo": ("#e8b830", "#f0cf5a"),
         "verde": ("#5f8f3a", "#8fae5a")}


def forma(tipo, cor, seed=401):
    a = Aquarela(S, S, seed=seed + hash(tipo + cor) % 97)
    c1, c2 = CORES[cor]
    if tipo == "circulo":
        pts = ellipse(300, 300, 230, 230, n=200)
    elif tipo == "quadrado":
        pts = densify(_ret(80, 80, 520, 520, 6), 200)
    elif tipo == "triangulo":
        pts = densify(np.array([(300, 60), (540, 500), (60, 500)], float), 200)
    elif tipo == "retangulo":
        pts = densify(_ret(40, 170, 560, 430, 6), 200)
    a.wash(pts, c1, 0.5, color2=c2, edge=1.1, outline=0.45)
    return a


def conta(cor, seed=411):
    a = Aquarela(300, 300, seed=seed + hash(cor) % 50)
    c1, c2 = CORES[cor]
    a.wash(ellipse(150, 150, 120, 110), c1, 0.55, color2=c2, edge=1.1, light=(110, 110, 18), outline=0.4)
    a.lift(ellipse(150, 150, 22, 22, n=30), 0.95)
    a.wash(ellipse(150, 150, 22, 22, n=30), "#5b4632", 0.25, layers=1, edge=1.2)
    return a


def barra(k, seed=421):
    """Barra de comprimento k (1 a 5): 1 = 120 px."""
    w = 120 * k
    a = Aquarela(w + 20, 110, seed=seed + k)
    cor = ("#c43a2e", "#d8604a") if k % 2 else ("#4f74a8", "#7f9cc9")
    a.wash(_ret(10, 15, w + 10, 95, 6), cor[0], 0.5, color2=cor[1], edge=1.1, outline=0.45)
    return a


def caixa():
    a = Aquarela(S, S, seed=431)
    frente = _ret(110, 260, 490, 520, 4)
    a.wash(densify(frente, 160), "#c49a62", 0.5, color2="#a87a42", edge=1.0, outline=0.45, granulation=1.0)
    tampa = np.array([(110, 260), (490, 260), (560, 190), (180, 190)], float)
    a.wash(densify(tampa, 160), "#8a6034", 0.45, edge=1.0, outline=0.45, granulation=1.0)
    lado = np.array([(490, 260), (560, 190), (560, 440), (490, 520)], float)
    a.wash(densify(lado, 160), "#a87a42", 0.5, edge=1.0, outline=0.45, granulation=1.0)
    return a


def palma():
    a = Aquarela(S, S, seed=441)
    mao = np.vstack([bezier((200, 560), (170, 420), (160, 330), (190, 300)),
                     bezier((190, 300), (215, 280), (235, 300), (240, 340)),
                     bezier((240, 340), (230, 200), (240, 110), (270, 105)),
                     bezier((270, 105), (300, 100), (305, 150), (305, 300)),
                     bezier((305, 300), (310, 120), (320, 70), (350, 72)),
                     bezier((350, 72), (380, 75), (380, 130), (370, 300)),
                     bezier((370, 300), (390, 150), (400, 110), (425, 115)),
                     bezier((425, 115), (455, 120), (450, 200), (430, 330)),
                     bezier((430, 330), (460, 260), (480, 250), (500, 265)),
                     bezier((500, 265), (520, 290), (470, 400), (420, 560))])
    a.wash(densify(mao, 300), "#e8b9a0", 0.45, color2="#dca088", edge=1.1, outline=0.45)
    return a


MOTIVOS4 = {"caixa": caixa, "palma": palma}
for t in ("circulo", "quadrado", "triangulo", "retangulo"):
    for c in CORES:
        MOTIVOS4[f"{t}_{c}"] = (lambda t=t, c=c: forma(t, c))
for c in CORES:
    MOTIVOS4[f"conta_{c}"] = (lambda c=c: conta(c))
for k in range(1, 6):
    MOTIVOS4[f"barra_{k}"] = (lambda k=k: barra(k))

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS4):
        MOTIVOS4[n]().image().save(os.path.join(out, f"{n}.png"))
