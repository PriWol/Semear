"""Motivos do Volume 7 (Primeiras línguas): gestos, porta, janela e cama dos cumprimentos, pintados com o motor de aquarela.
Mesmo estilo e mesma escala dos motivos anteriores (600 × 600 px, ≈ 5 cm a 300 dpi). Só mãos, objetos e astros, como em
docs/03-ilustracao.md: nada de pessoas inteiras nem de cenas (as cenas vêm das gravuras de domínio público)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, bezier, leaf, densify
from motivos2 import _ret
from motivos7 import PELE, _bez, _esp, _tra

S = 600
MADEIRA = ("#9a7650", "#b8946a")
AZUL = "#5f7f9c"
ROSA = "#c0716b"


def _punho(a, cx, cy):
    """Corpo de um punho fechado visto de frente (os dedos dobrados aparecem à esquerda do polegar)."""
    a.wash(ellipse(cx, cy, 150, 125), PELE[0], 0.8, color2=PELE[1], edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    for (dx, dy, rx) in ((-85, -62, 62), (-92, 0, 66), (-84, 62, 60)):
        a.wash(ellipse(cx + dx, cy + dy, rx, 36), PELE[0], 0.7, color2=PELE[1], edge=1.0, outline=0.5)


def _manga(a, y0=505, cor=ROSA):
    """Punho da manga, para a mão não flutuar."""
    a.wash(densify(np.array([(185, y0), (415, y0), (432, 592), (168, 592)], float), 160), cor, 0.7, color2="#d8928a", edge=1.0, outline=0.5)


# ------------------------------------------------------------------ gestos

def mao_acenando(seed=2001):
    a = Aquarela(S, S, seed=seed)
    ang = 0.22
    c0 = np.array([300, 395])

    def gira(x, y):
        d = np.array([x, y]) - c0
        return c0 + np.array([d[0] * math.cos(ang) - d[1] * math.sin(ang), d[0] * math.sin(ang) + d[1] * math.cos(ang)])

    for (x, y, rx, ry, rot) in ((160, 345, 32, 86, -0.95), (232, 200, 31, 96, -0.1), (300, 165, 32, 112, 0.0), (368, 190, 31, 100, 0.1), (428, 262, 28, 80, 0.3)):
        p = gira(x, y)
        a.wash(ellipse(p[0], p[1], rx, ry, rot=rot + ang), PELE[0], 0.8, color2=PELE[1], edge=1.0, outline=0.5)
    a.wash(ellipse(300, 395, 140, 140), PELE[0], 0.95, color2=PELE[1], edge=1.0, shade=(1, 0.5, 0.5))
    _manga(a, 520)
    for k, r in enumerate((205, 240, 275)):   # três arcos de movimento de cada lado
        for lado in (1, -1):
            p0 = (300 + lado * (r - 60), 190 - 20 * k)
            _tra(a, _bez(((300 + lado * (r - 70), 250 - 18 * k), (300 + lado * r, 200 - 15 * k), (300 + lado * (r + 5), 130 - 10 * k), (p0[0], p0[1] - 30))), AZUL, 7, 0.7, True)
    return a


def maos_juntas(seed=2011):
    """Palmas juntas, com as pontas dos dedos para cima e os dois braços abrindo para baixo."""
    a = Aquarela(S, S, seed=seed)
    a.wash(densify(leaf((205, 575), (302, 85), 150), 220), PELE[0], 0.75, color2=PELE[1], edge=1.0, outline=0.5)
    a.wash(densify(leaf((395, 575), (298, 85), 150), 220), PELE[0], 0.8, color2=PELE[1], edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))
    for k in range(3):   # dedos: pequenos traços junto das pontas
        _tra(a, np.array([(282 + 18 * k, 120), (284 + 18 * k, 205)]), "#b8845a", 5, 0.7, True)
    a.wash(ellipse(335, 395, 24, 62, rot=-0.35), "#e8c4a0", 0.7, edge=0.9, outline=0.4)   # polegar
    for lado in (1, -1):   # mangas
        m = np.array([(150, 520), (250, 560), (232, 595), (120, 595)], float)
        a.wash(densify(m if lado == 1 else _esp(m), 120), AZUL, 0.7, color2="#86a3bd", edge=1.0, outline=0.5)
    return a


def polegar_cima(seed=2021):
    a = Aquarela(S, S, seed=seed)
    _punho(a, 290, 400)
    a.wash(densify(leaf((395, 350), (392, 85), 100), 200), PELE[0], 0.85, color2=PELE[1], edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))
    a.wash(ellipse(392, 135, 27, 32), "#f3d9c4", 0.6, edge=0.7, outline=0.3)
    _manga(a, 515, "#7f9a52")
    return a


def dedo_nao(seed=2031):
    a = Aquarela(S, S, seed=seed)
    _punho(a, 300, 430)
    a.wash(densify(leaf((318, 360), (318, 60), 72), 200), PELE[0], 0.85, color2=PELE[1], edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))
    a.wash(ellipse(318, 98, 20, 26), "#f3d9c4", 0.6, edge=0.7, outline=0.3)
    for lado in (1, -1):   # o dedo balança de um lado para o outro
        for k, r in enumerate((110, 150)):
            _tra(a, _bez(((318 + lado * (r - 30), 215), (318 + lado * r, 170), (318 + lado * (r + 5), 120), (318 + lado * (r - 25), 75))), AZUL, 7, 0.7, True)
    _manga(a, 545, ROSA)
    return a


def carinha_feliz(seed=2041):
    a = Aquarela(S, S, seed=seed)
    a.wash(ellipse(300, 300, 235, 235), "#f2c545", 0.8, color2="#f8dc7a", edge=1.0, outline=0.55, shade=(1, 0.5, 0.5), light=(220, 200, 80))
    for x in (225, 375):
        a.wash(ellipse(x, 250, 22, 34), "#3a2c20", 0.9, edge=0.7)
        a.lift(ellipse(x - 6, 238, 7, 10, n=24), 0.8, 0.5)
    for x in (165, 435):
        a.wash(ellipse(x, 345, 38, 24), "#e8836a", 0.5, edge=0.6)
    _tra(a, _bez(((175, 335), (210, 460), (390, 460), (425, 335))), "#7a3a2c", 12, 0.85, True)
    return a


# ------------------------------------------------------------------ casa

def porta(seed=2101):
    a = Aquarela(S, S, seed=seed)
    a.wash(_ret(130, 540, 470, 580), "#b8b4a8", 0.6, color2="#d4d0c4", edge=1.0, outline=0.45)   # degrau de pedra
    arco = np.vstack([bezier((160, 540), (160, 380), (160, 190), (160, 170)), bezier((160, 170), (160, 70), (440, 70), (440, 170)), bezier((440, 170), (440, 190), (440, 380), (440, 540))])
    a.wash(densify(arco, 260), MADEIRA[0], 0.75, color2=MADEIRA[1], edge=1.0, outline=0.55)
    arco2 = np.vstack([bezier((190, 535), (190, 380), (190, 200), (190, 180)), bezier((190, 180), (190, 108), (410, 108), (410, 180)), bezier((410, 180), (410, 200), (410, 380), (410, 535))])
    a.wash(densify(arco2, 260), AZUL, 0.75, color2="#86a3bd", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(_ret(225, 225, 375, 330, 8), "#4f6f8c", 0.55, edge=0.9, outline=0.4)    # almofadas da porta
    a.wash(_ret(225, 365, 375, 510, 8), "#4f6f8c", 0.55, edge=0.9, outline=0.4)
    a.wash(ellipse(385, 380, 17, 17, n=30), "#d8a63a", 0.9, edge=0.8, outline=0.4)   # maçaneta
    _tra(a, _bez(((300, 135), (330, 135), (330, 185), (300, 185)), ((300, 185), (270, 185), (270, 135), (300, 135))), "#d8a63a", 8, 0.85, False)   # aldrava
    return a


def porta_aberta(seed=2111):
    a = Aquarela(S, S, seed=seed)
    a.wash(_ret(110, 545, 490, 585), "#b8b4a8", 0.6, color2="#d4d0c4", edge=1.0, outline=0.45)
    a.wash(_ret(150, 70, 450, 545), MADEIRA[0], 0.8, color2=MADEIRA[1], edge=1.0, outline=0.55)   # batente
    a.wash(_ret(178, 98, 422, 545), "#f6dc8c", 0.7, color2="#fff0c0", edge=1.0, outline=0.4)     # a luz de dentro
    a.wash(densify(np.array([(178, 98), (300, 128), (300, 520), (178, 545)], float), 160), "#5f8f8a", 0.8, color2="#86aea8", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))
    a.wash(ellipse(280, 330, 14, 14, n=30), "#d8a63a", 0.9, edge=0.8, outline=0.4)
    a.wash(densify(np.array([(300, 545), (422, 545), (470, 585), (270, 585)], float), 120), "#f6dc8c", 0.5, edge=0.6)   # luz no chão
    return a


def janela_sol(seed=2121):
    a = Aquarela(S, S, seed=seed)
    a.wash(_ret(110, 495, 490, 535), MADEIRA[1], 0.7, edge=1.0, outline=0.5)   # peitoril
    a.wash(_ret(150, 70, 450, 500), MADEIRA[0], 0.75, color2=MADEIRA[1], edge=1.0, outline=0.55)
    a.lift(_ret(175, 95, 425, 475), 0.97, 0.6)   # reserva o vidro: pigmento sobre pigmento ficaria marrom
    a.wash(_ret(175, 95, 425, 475), "#cfe3ee", 0.7, color2="#f6e7b5", edge=1.0, outline=0.4)
    a.wash(ellipse(355, 205, 56, 56, n=70), "#f2c545", 0.85, color2="#f8dc7a", edge=1.0, outline=0.45)
    for k in range(10):
        t = k * math.pi / 5
        _tra(a, np.array([(355 + 70 * math.cos(t), 205 + 70 * math.sin(t)), (355 + 98 * math.cos(t), 205 + 98 * math.sin(t))]), "#e6a830", 6, 0.8, True)
    _tra(a, np.array([(300, 95), (300, 475)]), MADEIRA[0], 14, 0.85, False)
    _tra(a, np.array([(175, 285), (425, 285)]), MADEIRA[0], 14, 0.85, False)
    cortina = np.array([(150, 70), (212, 82), (196, 280), (218, 480), (150, 495)], float)
    a.wash(densify(cortina, 160), ROSA, 0.7, color2="#d8928a", edge=1.0, outline=0.5)
    a.wash(densify(_esp(cortina), 160), ROSA, 0.7, color2="#d8928a", edge=1.0, outline=0.5)
    return a


def cama(seed=2131):
    a = Aquarela(S, S, seed=seed)
    cab = np.vstack([bezier((120, 345), (120, 180), (130, 120), (175, 105)), bezier((175, 105), (260, 80), (340, 80), (425, 105)),
                     bezier((425, 105), (470, 120), (480, 180), (480, 345))])
    a.wash(densify(cab, 220), MADEIRA[0], 0.75, color2=MADEIRA[1], edge=1.0, outline=0.55)   # cabeceira com o topo arredondado
    a.wash(_ret(160, 140, 440, 290, 20), MADEIRA[1], 0.4, edge=0.8, outline=0.35)
    a.lift(ellipse(300, 335, 140, 52), 0.95, 0.8)   # reserva o travesseiro
    a.wash(ellipse(300, 335, 140, 52), "#f6efe0", 0.55, color2="#e8e0d0", edge=1.0, outline=0.55, shade=(1, 0.5, 0.5))
    a.wash(_ret(115, 365, 485, 505, 14), AZUL, 0.75, color2="#86a3bd", edge=1.0, outline=0.5, shade=(1, 0.5, 0.5))   # cobertor
    a.lift(_ret(115, 365, 485, 408, 14), 0.9, 0.8)
    a.wash(_ret(115, 365, 485, 408, 14), "#f6efe0", 0.5, edge=0.9, outline=0.45)                                         # dobra do lençol
    for (x, y) in ((205, 455), (300, 472), (395, 452)):
        a.wash(ellipse(x, y, 17, 17, n=30), "#f2c545", 0.85, edge=0.7)
    a.wash(_ret(120, 503, 158, 565), MADEIRA[0], 0.8, edge=0.9, outline=0.45)
    a.wash(_ret(442, 503, 480, 565), MADEIRA[0], 0.8, edge=0.9, outline=0.45)
    return a


GESTOS = {"mao_acenando": mao_acenando, "maos_juntas": maos_juntas, "polegar_cima": polegar_cima, "dedo_nao": dedo_nao, "carinha_feliz": carinha_feliz}
CASA = {"porta": porta, "porta_aberta": porta_aberta, "janela_sol": janela_sol, "cama": cama}

MOTIVOS8 = {**GESTOS, **CASA}


if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n in sys.argv[2:] or list(MOTIVOS8):
        MOTIVOS8[n]().rgba().save(os.path.join(out, f"{n}.png"))
