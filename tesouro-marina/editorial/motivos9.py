"""Motivos do Volume 8 (Jogos e descobertas): objetos dos jogos de brincar junto, pintados com o motor de aquarela.
Mesmo estilo e mesma escala dos motivos anteriores (600 × 600 px, ≈ 5 cm a 300 dpi). Só objetos, como em docs/03-ilustracao.md.
Poucos de propósito: a maior parte das figuras do volume já existe nos volumes anteriores (ADR 0031)."""
import numpy as np
from aquarela import Aquarela, ellipse, bezier, densify
from motivos2 import _ret
from motivos7 import _bez, _esp, _tra
from motivos8 import ROSA, AZUL, MADEIRA

S = 600


def bola(seed=2301):
    """Bola de pano macia, de gomos, para rolar de um para o outro."""
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 310, 225, 225, n=200), "#d9808a", 0.65, color2="#e8a2a8", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5), light=(220, 220, 60))
    for dx, cor in ((-95, "#f2c545"), (95, "#5f7f9c")):   # dois gomos de outra cor, vistos de lado
        a.wash(ellipse(300 + dx, 310, 38, 200, rot=0.12 * (1 if dx > 0 else -1)), cor, 0.6, edge=1.0, outline=0.35)
    a.wash(ellipse(300, 310, 38, 214), "#f6efe0", 0.55, edge=1.0, outline=0.35)
    return a


def ursinho(seed=2311):
    """Ursinho de pelúcia sentado, o bichinho da respiração."""
    a = Aquarela(S, S, seed=seed)
    cor, cor2 = "#b8845a", "#d0a478"
    for x in (160, 440):   # orelhas
        a.wash(ellipse(x, 120, 58, 58), cor, 0.75, color2=cor2, edge=1.0, outline=0.5)
        a.wash(ellipse(x, 126, 28, 28), "#e8c4a0", 0.6, edge=0.8)
    a.wash(ellipse(300, 410, 150, 165), cor, 0.75, color2=cor2, edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))   # corpo
    a.wash(ellipse(300, 440, 85, 105), "#e8c4a0", 0.6, edge=0.9, outline=0.35)                                # barriga
    for x in (150, 450):   # braços e pés
        a.wash(ellipse(x, 400, 48, 95, rot=0.25 if x < 300 else -0.25), cor, 0.75, color2=cor2, edge=1.0, outline=0.5)
    for x in (200, 400):
        a.wash(ellipse(x, 570, 62, 32), cor, 0.8, color2=cor2, edge=1.0, outline=0.5)
    a.wash(ellipse(300, 205, 140, 125), cor, 0.8, color2=cor2, edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))   # cabeça
    a.wash(ellipse(300, 245, 62, 46), "#e8c4a0", 0.7, edge=0.9, outline=0.4)                                  # focinho
    a.wash(ellipse(300, 228, 17, 12), "#3a2c20", 0.9, edge=0.7)
    for x in (250, 350):
        a.wash(ellipse(x, 175, 11, 15), "#3a2c20", 0.9, edge=0.7)
    _tra(a, _bez(((270, 262), (292, 282), (308, 282), (330, 262))), "#6a3a2c", 6, 0.8, True)
    a.wash(densify(np.array([(255, 335), (345, 335), (330, 365), (270, 365)], float), 60), ROSA, 0.7, edge=0.9, outline=0.4)   # laço
    return a


def lenco(seed=2321):
    """Lenço dobrado em triângulo, o do Corre, cotia."""
    a = Aquarela(S, S, seed=seed)
    tri = np.array([(70, 175), (530, 175), (300, 520)], float)
    a.wash(densify(tri, 240), "#c0716b", 0.7, color2="#d8928a", edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))
    for k, (x, y) in enumerate(((200, 245), (300, 245), (400, 245), (250, 325), (350, 325), (300, 405))):
        a.lift(ellipse(x, y, 17, 17, n=30), 0.9, 0.5)
    a.wash(ellipse(300, 160, 30, 20), "#a85a54", 0.5, edge=0.8, outline=0.3)
    return a


def garrafa_calma(seed=2331):
    """Garrafa da calma: água, cola e glitter parado no fundo."""
    a = Aquarela(S, S, seed=seed)
    corpo = np.vstack([_bez(((225, 200), (160, 250), (165, 330), (170, 420))), _bez(((170, 420), (172, 520), (190, 548), (300, 552)), ((300, 552), (410, 548), (428, 520), (430, 420))),
                       _bez(((430, 420), (435, 330), (440, 250), (375, 200)))])
    a.wash(densify(corpo, 260), "#cfe3ee", 0.55, color2="#e4eef4", edge=1.0, outline=0.55)
    a.wash(_ret(250, 70, 350, 135, 8), ROSA, 0.8, edge=1.0, outline=0.5)   # tampa
    a.wash(_ret(262, 135, 338, 205), "#cfe3ee", 0.5, edge=0.9, outline=0.5)
    rng = np.random.default_rng(8)
    for k in range(34):   # glitter
        x, y = rng.uniform(200, 400), rng.uniform(300, 535)
        a.wash(ellipse(x, y, 9, 9, n=14), ("#f2c545", "#c0716b", "#5f7f9c", "#7f9a52")[k % 4], 0.8, edge=0.7)
    a.lift(ellipse(215, 330, 10, 70), 0.6, 0.8)   # brilho no vidro
    return a


def cortina(seed=2341):
    """Cortina de esconde-esconde: pano aberto de um lado, com a ponta de um pé de fora."""
    a = Aquarela(S, S, seed=seed)
    a.wash(_ret(80, 65, 520, 95), MADEIRA[0], 0.8, edge=0.9, outline=0.45)   # varão
    pano = np.vstack([_bez(((120, 95), (130, 250), (110, 400), (125, 560))), np.array([(180, 575), (260, 560), (340, 575), (420, 560), (480, 575)]), _bez(((480, 560), (490, 400), (470, 250), (480, 95)))])
    a.wash(densify(pano, 260), AZUL, 0.7, color2="#86a3bd", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for x in (200, 300, 400):   # dobras
        _tra(a, np.array([(x, 110), (x - 8, 340), (x + 6, 560)]), "#4f6f8c", 6, 0.5, True)
    for x in (255, 345):   # os pés aparecendo embaixo
        a.wash(ellipse(x, 585, 34, 14), "#e4b48c", 0.85, edge=0.9, outline=0.4)
    return a


MOTIVOS9 = {"bola": bola, "ursinho": ursinho, "lenco": lenco, "garrafa_calma": garrafa_calma, "cortina": cortina}


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS9):
        MOTIVOS9[n]().rgba().save(os.path.join(out, f"{n}.png"))
