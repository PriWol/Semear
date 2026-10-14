"""Recorta a ilustração de uma página digitalizada (remove margens de papel e o número de página)."""
import sys
import numpy as np
from PIL import Image

def recortar(src, dst, margem=0.012, limiar=38, min_frac=0.04):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    papel = np.median(a[: h // 20].reshape(-1, 3), axis=0)  # cor do papel na faixa superior
    dif = np.abs(a - papel).sum(axis=2) > limiar
    linhas = np.where(dif.sum(axis=1) > w * min_frac)[0]
    cols = np.where(dif.sum(axis=0) > h * min_frac)[0]
    y0, y1, x0, x1 = linhas[0], linhas[-1], cols[0], cols[-1]
    m = int(max(h, w) * margem)
    box = (max(0, x0 - m), max(0, y0 - m), min(w, x1 + m), min(h, y1 + m))
    out = im.crop(box)
    # o papel amarelado da digitalização vira transparência: a ilustração passa a
    # "estar impressa" no papel da coleção (branco na impressão, creme na tela)
    t = np.clip(np.asarray(out).astype(float) / papel, 0, 1)
    alpha = np.clip((1 - t.min(axis=2)) * 1.08, 0, 1)
    alpha[alpha < 0.035] = 0
    cor = np.where(alpha[..., None] > 1e-3, 1 - (1 - t) / np.maximum(alpha[..., None], 1e-3), 1)
    rgba = np.dstack([np.clip(cor, 0, 1), alpha])
    out = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    out.save(dst, dpi=(300, 300), optimize=True)
    print(dst, out.size, f"{out.size[0] / 300 * 25.4:.0f} mm de largura a 300 dpi")

if __name__ == "__main__":
    recortar(*sys.argv[1:3])
