"""Motivos específicos de páginas (musicograma, chuva)."""
import math
import numpy as np
from aquarela import Aquarela, ellipse, bezier, leaf
from motivos import nuvem, _contour


def marca_passaros():
    a = Aquarela(600, 360, seed=101)
    rng = np.random.default_rng(2)
    # trinados: pontinhos saltitantes e pequenos arabescos
    for k in range(7):
        x0 = 60 + k * 72
        y0 = 200 + 60 * math.sin(k * 1.3)
        a.wash(ellipse(x0, y0, 20, 17, n=40), "#b8605a", 0.7, color2="#e0a090", edge=1.1, layers=2)
        a.stroke(bezier((x0 + 14, y0 - 4), (x0 + 30, y0 - 50), (x0 + 50, y0 - 10), (x0 + 58, y0 - 40)),
                 "#8a5a52", width=4.5, opacity=0.7)
    for k in range(18):
        x, y = rng.uniform(40, 560), rng.uniform(60, 320)
        a.wash(ellipse(x, y, 7, 7, n=16), "#c0716b", 0.75, layers=1, edge=0.6, wobble=0.6)
    return a


def marca_riacho():
    a = Aquarela(600, 360, seed=102)
    for k, y0 in enumerate((110, 175, 240)):
        xs = np.linspace(30, 570, 160)
        ys = y0 + 22 * np.sin(xs / 55 + k)
        top = np.stack([xs, ys - 13], 1)
        bot = np.stack([xs[::-1], ys[::-1] + 13], 1)
        a.wash(np.vstack([top, bot]), "#5f8fb0", 0.4, color2="#8fb6cc", edge=1.2, layers=2)
    return a


def marca_trovao():
    a = Aquarela(600, 360, seed=103)
    n = nuvem(600, 300, seed=104, cor="#5e6a78")
    a.dens[:300] += n.dens * 1.5
    zz = np.array([(330, 190), (285, 262), (325, 262), (270, 352), (370, 240), (330, 240), (375, 190)])
    a.wash(zz, "#d9a02a", 0.7, color2="#e8c040", edge=1.2, layers=2, wobble=1.0, outline=0.35)
    return a


def marca_tema():
    """O tema que sempre volta (ritornelo): uma guirlanda fechada."""
    a = Aquarela(600, 360, seed=105)
    cx, cy, R = 300, 180, 140
    for i, t in enumerate(np.linspace(0, 2 * math.pi, 16, endpoint=False)):
        p = np.array([cx + R * math.cos(t), cy + R * 0.85 * math.sin(t)])
        tang = np.array([-math.sin(t), 0.85 * math.cos(t)])
        tip = p + tang / np.linalg.norm(tang) * 80 + (p - [cx, cy]) * 0.12 * (1 if i % 2 else -1)
        a.wash(leaf(p, tip, 36), "#6f8f48", 0.5, color2="#a8b860", edge=1.0, layers=2, outline=0.2)
    for t in np.linspace(0, 2 * math.pi, 5, endpoint=False):
        x, y = cx + R * math.cos(t + 0.3), cy + R * 0.85 * math.sin(t + 0.3)
        a.wash(ellipse(x, y, 22, 22, n=30), "#d9707a", 0.6, color2="#eaa0a0", edge=1.1, layers=2)
    return a


ARTE_EXTRA = {
    "m_passaros": marca_passaros, "m_riacho": marca_riacho,
    "m_trovao": marca_trovao, "m_tema": marca_tema,
}
