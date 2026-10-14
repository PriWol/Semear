"""
Motor de aquarela procedural — O Grande Tesouro de Marina.

Simula aquarela transparente por camadas (velaturas): cada pincelada é um
polígono com borda irregular, depositado em várias camadas finas, com
acúmulo de pigmento na borda (efeito "anel de café"), variação molhado-
sobre-molhado e granulação do papel. O resultado é a TRANSMITÂNCIA do
pigmento sobre papel branco (RGB), para ser impresso sobre papel creme
ou composto com `mix-blend-mode: multiply`.

Limite honesto: serve bem a objetos simples e botânicos (frutos, folhas,
flores, céu, chuva, formas). NÃO substitui ilustração narrativa pintada
(personagens, animais, paisagens) — ver docs/03-ilustracao.md.
"""
from __future__ import annotations

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, map_coordinates

RNG = np.random.default_rng(7)


def hex2rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def densify(pts, n=160):
    """Reamostra um polígono fechado com n pontos igualmente espaçados."""
    pts = np.asarray(pts, float)
    closed = np.vstack([pts, pts[:1]])
    seg = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    s = np.r_[0, np.cumsum(seg)]
    t = np.linspace(0, s[-1], n, endpoint=False)
    return np.stack([np.interp(t, s, closed[:, 0]), np.interp(t, s, closed[:, 1])], 1)


def smooth_noise(h: int, w: int, scale: float, rng=None) -> np.ndarray:
    """Ruído suave em [-1, 1] com comprimento de correlação ~scale px."""
    rng = rng or RNG
    n = gaussian_filter(rng.standard_normal((h, w)), scale, mode="wrap")
    n /= (np.abs(n).max() + 1e-9)
    return n


class Aquarela:
    def __init__(self, w: int, h: int, seed: int = 1):
        self.w, self.h = w, h
        self.rng = np.random.default_rng(seed)
        # densidade óptica acumulada por canal (0 = papel limpo)
        self.dens = np.zeros((h, w, 3))
        self.paper = 0.5 + 0.5 * smooth_noise(h, w, 1.2, self.rng)  # fibra fina
        # grão de papel prensado a frio: vales acumulam pigmento (granulação)
        g = 0.65 * smooth_noise(h, w, 2.2, self.rng) + 0.35 * smooth_noise(h, w, 5, self.rng)
        self.grain = g / (np.abs(g).max() + 1e-9)

    # ---------- geometria ----------
    def _raster(self, pts, blur=0.0) -> np.ndarray:
        img = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(img).polygon([tuple(p) for p in pts], fill=255)
        if blur:
            img = img.filter(ImageFilter.GaussianBlur(float(blur)))
        return np.asarray(img, dtype=float) / 255

    def _wobble(self, pts, amp, freq=5, phase=None):
        """Desloca o contorno ao longo da normal com ruído periódico suave."""
        pts = np.asarray(pts, dtype=float)
        n = len(pts)
        t = np.linspace(0, 2 * math.pi, n, endpoint=False)
        ph = self.rng.uniform(0, 2 * math.pi, 4) if phase is None else phase
        d = (np.sin(freq * t + ph[0]) * 0.5 + np.sin(2.3 * freq * t + ph[1]) * 0.3
             + np.sin(5.1 * freq * t + ph[2]) * 0.2)
        d += self.rng.normal(0, 0.18, n)
        d = np.convolve(np.r_[d[-3:], d, d[:3]], np.ones(5) / 5, "same")[3:-3]
        tang = np.roll(pts, -1, 0) - np.roll(pts, 1, 0)
        nrm = np.stack([tang[:, 1], -tang[:, 0]], 1)
        nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9)
        return pts + nrm * (d * amp)[:, None]

    # ---------- pinceladas ----------
    def _mask(self, pts, wobble_amp, layers, soft):
        acc = np.zeros((self.h, self.w))
        for i in range(layers):
            m = self._raster(self._wobble(pts, wobble_amp * (0.5 + i / layers)), blur=soft)
            acc += m / layers
        return acc

    def wash(self, pts, color, opacity=0.55, color2=None, edge=0.9,
             wobble=None, layers=3, granulation=0.5, bloom=0.0,
             light=None, soft=0.7, shade=None, shade_color=None, outline=0.0):
        """Aguada sobre um polígono, com orla escura nítida.

        color2  — segundo pigmento misturado molhado-sobre-molhado
        light   — (x, y, raio): reserva de branco do papel (brilho)
        shade   — (dx, dy, força): segunda velatura em crescente (sombra própria)
        outline — força do contorno a lápis sépia, interrompido
        """
        pts = np.asarray(pts, dtype=float)
        if len(pts) < 60:
            pts = densify(pts, 160)
        size = float(np.ptp(pts, axis=0).max())
        amp = wobble if wobble is not None else max(1.0, size * 0.008)
        mask = self._mask(pts, amp, layers, soft)
        # orla: pigmento migra para a borda ao secar — fina e nítida
        rim = np.clip(mask - gaussian_filter(mask, max(1.5, size * 0.012)), 0, 1)
        rim2 = np.clip(mask - gaussian_filter(mask, max(3, size * 0.04)), 0, 1)
        var = (1 + 0.22 * smooth_noise(self.h, self.w, max(3, size * 0.07), self.rng)
               + 0.12 * smooth_noise(self.h, self.w, max(2, size * 0.02), self.rng))
        a = mask * opacity * var + (rim * 1.6 + rim2 * 0.5) * opacity * edge
        if bloom:
            b = smooth_noise(self.h, self.w, size * 0.06, self.rng)
            a *= 1 - bloom * np.clip(b, 0, 1)
        if light is not None:
            lx, ly, lr = light
            hl = self._raster(self._wobble(ellipse(lx, ly, lr * 1.3, lr * 0.75, n=90, rot=-0.7), lr * 0.08),
                              blur=lr * 0.12)
            hl_soft = gaussian_filter(hl, lr * 0.6)
            a *= 1 - np.clip(hl * 0.45 + hl_soft * 0.35, 0, 0.7)
        a *= 1 + granulation * self.grain
        a = np.clip(a, 0, 2)
        col = hex2rgb(color)
        if color2 is not None:
            mix = np.clip(0.5 + 0.7 * smooth_noise(self.h, self.w, size * 0.15, self.rng), 0, 1)
            col2 = hex2rgb(color2)
            colmap = col[None, None, :] * (1 - mix[..., None]) + col2[None, None, :] * mix[..., None]
        else:
            colmap = np.broadcast_to(col, (self.h, self.w, 3))
        self.dens += a[..., None] * -np.log(np.clip(colmap, 0.03, 1))
        if shade is not None:
            dx, dy, k = shade
            c = pts.mean(0)
            shifted = (pts - c) * 1.04 + c - np.array([dx, dy]) * size * 0.22
            other = self._mask(shifted, amp * 3, 2, size * 0.03)
            cres = mask * (1 - other)
            crim = np.clip(cres - gaussian_filter(cres, max(1.5, size * 0.015)), 0, 1)
            sa = (cres * 0.9 + crim * 0.8) * opacity * k * (1 + granulation * self.grain)
            sc = hex2rgb(shade_color or color) * 0.72
            self.dens += sa[..., None] * -np.log(np.clip(sc, 0.03, 1))
        if outline:
            self.outline(pts, strength=outline)
        return mask

    def lift(self, pts, amount=0.85, soft=1.0):
        """Levantar pigmento com pincel úmido / reserva (pintas, brilhos)."""
        m = self._raster(self._wobble(np.asarray(pts, float), 1.0), blur=soft)
        self.dens *= (1 - amount * m)[..., None]

    def inside(self, pts, x, y):
        from matplotlib.path import Path
        return Path(pts).contains_point((x, y))

    def outline(self, pts, strength=0.45, color="#5b4632", width=2.2):
        """Contorno a lápis/pena, com falhas, como nas pranchas botânicas."""
        pts = self._wobble(np.asarray(pts, float), 1.2)
        n = len(pts)
        i = int(self.rng.integers(0, n))
        while i < n * 1.9:
            seg = int(self.rng.integers(n // 8, n // 3))
            idx = np.arange(i, i + seg) % n
            self.stroke(pts[idx], color, width=width, opacity=strength)
            i += seg + int(self.rng.integers(n // 30, n // 10))

    def stroke(self, path, color, width=3.0, opacity=0.75, taper=True):
        """Traço fino a pincel/pena (contorno delicado, nervuras, cabinhos)."""
        path = np.asarray(path, dtype=float)
        img = Image.new("L", (self.w, self.h), 0)
        d = ImageDraw.Draw(img)
        n = len(path)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            wv = width * (math.sin(math.pi * t) * 0.7 + 0.3 if taper else 1)
            wv *= 1 + self.rng.normal(0, 0.08)
            d.line([tuple(path[i]), tuple(path[i + 1])], fill=255, width=max(1, int(round(wv))))
            r = wv / 2
            d.ellipse([path[i][0] - r, path[i][1] - r, path[i][0] + r, path[i][1] + r], fill=255)
        m = np.asarray(img.filter(ImageFilter.GaussianBlur(0.7)), dtype=float) / 255
        m *= 0.85 + 0.15 * self.paper
        self.dens += (m * opacity)[..., None] * -np.log(np.clip(hex2rgb(color), 0.03, 1))

    def spatter(self, center, radius, color, n=40, size=(1.5, 5), opacity=0.5):
        """Respingos/pontinhos (sementes, pólen, textura)."""
        img = Image.new("L", (self.w, self.h), 0)
        d = ImageDraw.Draw(img)
        for _ in range(n):
            ang = self.rng.uniform(0, 2 * math.pi)
            r = radius * math.sqrt(self.rng.uniform(0, 1))
            x, y = center[0] + r * math.cos(ang), center[1] + r * math.sin(ang)
            s = self.rng.uniform(*size)
            d.ellipse([x - s, y - s, x + s, y + s], fill=255)
        m = np.asarray(img.filter(ImageFilter.GaussianBlur(0.8)), dtype=float) / 255
        self.dens += (m * opacity)[..., None] * -np.log(np.clip(hex2rgb(color), 0.03, 1))

    def image(self) -> Image.Image:
        rgb = np.exp(-self.dens)
        return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")

    def rgba(self) -> Image.Image:
        """Versão com transparência (alfa = cobertura), para fundos não brancos."""
        rgb = np.exp(-self.dens)
        alpha = 1 - rgb.min(axis=2)
        alpha = np.clip(alpha * 1.15, 0, 1)
        safe = np.where(alpha[..., None] > 1e-3,
                        1 - (1 - rgb) / np.maximum(alpha[..., None], 1e-3), 1)
        out = np.dstack([np.clip(safe, 0, 1), alpha])
        return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


# ---------- utilitários de forma ----------

def ellipse(cx, cy, rx, ry, n=180, rot=0.0):
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    x, y = rx * np.cos(t), ry * np.sin(t)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + c * x - s * y, cy + s * x + c * y], 1)


def polar(cx, cy, rfun, n=240, rot=0.0):
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = np.array([rfun(a) for a in t])
    return np.stack([cx + r * np.cos(t + rot), cy + r * np.sin(t + rot)], 1)


def bezier(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def leaf(base, tip, width, n=120, asym=0.0):
    """Folha lanceolada entre base e ponta."""
    base, tip = np.asarray(base, float), np.asarray(tip, float)
    axis = tip - base
    L = np.linalg.norm(axis)
    u = axis / L
    v = np.array([-u[1], u[0]])
    t = np.linspace(0, 1, n // 2)
    prof = np.sin(np.pi * t ** 0.85) * width / 2
    left = base + np.outer(t * L, u) + np.outer(prof * (1 + asym), v)
    right = base + np.outer(t[::-1] * L, u) - np.outer(prof[::-1] * (1 - asym), v)
    return np.vstack([left, right])
