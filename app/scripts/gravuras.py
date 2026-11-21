#!/usr/bin/env python3
"""
Gravuras botânicas de domínio público das telas do app (ADR 0035, estória #130/#24).

Roda SÓ na máquina de quem mantém o app, nunca no build nem no app: baixa a página original do
Internet Archive, confere o SHA-256 (falha fechada: se não bater, para), recorta só a planta e grava
dois WebP por gravura em app/public/gravuras/ (tinta clara e tinta escura sobre fundo transparente).
O app só lê esses arquivos locais; src/gravuras.ts registra o SHA-256 do original e dos WebP, e
tests/gravuras.test.ts confere os arquivos contra esse registro.

Uso (dentro de app/):
    pip install Pillow numpy
    python3 scripts/gravuras.py                 # baixa, confere, gera e imprime os SHA-256 dos WebP
    python3 scripts/gravuras.py --cache DIR     # onde guardar os originais (padrão: pasta temporária)

Ferramentas: Pillow (recorte, nivelamento do papel, canal alfa, WebP) e NumPy. O hash do WebP pode
mudar entre versões do Pillow/libwebp; se mudar, atualize sha256Webp em src/gravuras.ts depois de
olhar o resultado. O hash do ORIGINAL nunca pode mudar.
Download: https://archive.org/download/<item>/page/n<N>.jpg (mesmo método de tesouro-marina/editorial/fontes_v1.py).
"""
import argparse
import hashlib
import os
import sys
import tempfile
import time
import urllib.request

import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "public", "gravuras")

# Tintas dos tokens: --s-principal do tema claro (tokens.css) e do escuro (tokens-escuro.css, ADR 0033).
TINTA_CLARA = (0x35, 0x5E, 0x45)
TINTA_ESCURA = (0x8F, 0xBF, 0x9F)

# id: item, página (n<N>), SHA-256 do JPEG original, largura de saída (px),
# caixa do recorte (x0, y0, x1, y1) em frações da página, máscaras (mesmo formato) que apagam
# legendas e numerais de prancha, e pontos de preto/branco do nivelamento (0 a 1).
GRAVURAS = {
    "girassol": {
        "item": "mobot31753003651095",
        "pagina": 222,
        "sha256": "f02a39e3267a85dd057e53e8168064ba4700ad5bfc90c7f0abf6e4f27f726952",
        "largura": 520,
        "caixa": (0.03, 0.055, 0.985, 0.935),
        # legenda "Flos Solisprolifer." e a mancha de umidade abaixo dela
        "mascaras": [(0.407, 0.902, 0.814, 0.960)],
        "niveis": (0.10, 0.62),
    },
    "gladiolo": {
        "item": "mobot31753002806732",
        "pagina": 36,
        "sha256": "934fe988dc0f65c8a60e88a55173642e74a25c1727d3db22d6427adf26d63e04",
        "largura": 300,
        "caixa": (0.34, 0.085, 0.73, 0.875),
        "mascaras": [],
        "niveis": (0.08, 0.42),
    },
    "tulipas": {
        "item": "mobot31753003651095",
        "pagina": 78,
        "sha256": "9e42bd675444ec7beef20a9153f0df423d8c8d5919085b68a2336418c9f61580",
        "largura": 620,
        "caixa": (0.025, 0.04, 0.975, 0.885),
        # cinco legendas manuscritas e os numerais romanos entre as raízes
        "mascaras": [
            (0.0071, 0.7589, 0.1, 0.8321),
            (0.0071, 0.7735, 0.09, 0.8321),
            (0.0929, 0.7735, 0.2857, 0.8321),
            (0.2393, 0.7618, 0.2857, 0.7786),
            (0.0773, 0.7577, 0.1393, 0.7907),
            (0.1727, 0.7577, 0.2824, 0.7907),
            (0.1369, 0.7693, 0.1751, 0.7907),
            (0.3771, 0.7618, 0.6229, 0.8208),
            (0.7005, 0.783, 0.9607, 0.8235),
            (0.1821, 0.867, 0.4929, 0.9165),
            (0.5393, 0.8675, 0.8, 0.9221),
            (0.5, 0.7618, 0.5157, 0.7713),
            (0.325, 0.858, 0.3443, 0.867),
            (0.8464, 0.7747, 0.8607, 0.7848),
            # pontos soltos de texto que sobraram perto das raízes
            (0.0219, 0.7498, 0.0648, 0.7643),
            (0.7007, 0.7752, 0.7513, 0.7884),
            (0.8141, 0.7752, 0.8509, 0.7884),
            (0.8938, 0.7800, 0.9060, 0.7884),
            (0.2150, 0.8584, 0.2456, 0.8705),
            (0.4173, 0.8609, 0.4326, 0.8705),
            (0.5766, 0.8609, 0.5919, 0.8705),
        ],
        "niveis": (0.17, 0.60),
    },
}


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def baixar(item, pagina, destino):
    url = f"https://archive.org/download/{item}/page/n{pagina}.jpg"
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, open(destino, "wb") as f:
                f.write(r.read())
            return
        except OSError as erro:
            print(f"  tentativa {tentativa + 1} falhou ({erro}); esperando", file=sys.stderr)
            time.sleep(5 * (tentativa + 1))
    sys.exit(f"não foi possível baixar {url}")


def original(nome, g, cache):
    destino = os.path.join(cache, f"{nome}.jpg")
    if not os.path.exists(destino):
        print(f"baixando {nome} (item {g['item']}, n{g['pagina']})")
        baixar(g["item"], g["pagina"], destino)
    real = sha256(destino)
    if real != g["sha256"]:
        # Falha fechada: arquivo diferente do verificado nunca vira imagem do app.
        sys.exit(f"SHA-256 DIVERGENTE em {nome}: esperado {g['sha256']}, veio {real}")
    return destino


def fracao_para_pixels(caixa, largura, altura):
    x0, y0, x1, y1 = caixa
    return (round(x0 * largura), round(y0 * altura), round(x1 * largura), round(y1 * altura))


def tinta_para_alfa(cinza, niveis):
    """Cinza (0 a 255) vira opacidade da tinta: 0 = papel, 1 = tinta cheia.

    O papel varia (manchas, tom de cada exemplar); dividir pelo papel estimado (máximo local suavizado)
    deixa o fundo uniforme e o traço fino da gravura intacto."""
    pequeno = cinza.resize((cinza.width // 16, cinza.height // 16), Image.BILINEAR)
    papel = pequeno.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(5))
    papel = np.asarray(papel.resize(cinza.size, Image.BICUBIC), dtype=np.float32)
    razao = np.clip(np.asarray(cinza, dtype=np.float32) / np.maximum(papel, 1.0), 0, 1)
    tinta = 1.0 - razao
    preto, branco = niveis
    return np.clip((tinta - preto) / (branco - preto), 0, 1)


def tratar(nome, g, caminho):
    pagina = Image.open(caminho).convert("L")
    larg, alt = pagina.size
    corte = fracao_para_pixels(g["caixa"], larg, alt)
    alfa = tinta_para_alfa(pagina, g["niveis"])  # sobre a página inteira, para o papel ser bem estimado
    for m in g["mascaras"]:
        x0, y0, x1, y1 = fracao_para_pixels(m, larg, alt)
        alfa[y0:y1, x0:x1] = 0.0
    x0, y0, x1, y1 = corte
    alfa = alfa[y0:y1, x0:x1]
    img = Image.fromarray((alfa * 255).astype(np.uint8), "L")
    alt_saida = round(img.height * g["largura"] / img.width)
    img = img.resize((g["largura"], alt_saida), Image.LANCZOS)
    # margem pequena em volta, para a haste não encostar na borda
    margem = 6
    folha = Image.new("L", (img.width + 2 * margem, img.height + 2 * margem), 0)
    folha.paste(img, (margem, margem))
    return folha


def gravar(alfa, tinta, destino):
    rgba = Image.new("RGBA", alfa.size, tinta + (0,))
    rgba.putalpha(alfa)
    rgba.save(destino, "WEBP", quality=50, alpha_quality=30, method=6)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", default=os.path.join(tempfile.gettempdir(), "semear-gravuras"))
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    os.makedirs(SAIDA, exist_ok=True)
    for nome, g in GRAVURAS.items():
        alfa = tratar(nome, g, original(nome, g, args.cache))
        for sufixo, tinta in (("", TINTA_CLARA), ("-escuro", TINTA_ESCURA)):
            destino = os.path.join(SAIDA, f"{nome}{sufixo}.webp")
            gravar(alfa, tinta, destino)
            print(f"{nome}{sufixo}.webp  {os.path.getsize(destino)} bytes  {alfa.width}x{alfa.height}  sha256 {sha256(destino)}")


if __name__ == "__main__":
    main()
