"""
Ilustrações de domínio público do Volume 1: página de origem, recorte e crédito.
As páginas vêm do Internet Archive (https://archive.org/download/<item>/page/n<N>.jpg).
caixa = (x0, y0, x1, y1) em frações da página; None = recorte automático pelo papel.
"""
import os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "dominio_publico", "v1")

LIVROS = {
    "underwindowpictv00greerich": "Kate Greenaway (1846–1901), <i>Under the Window</i> (Londres: George Routledge, 1878)",
    "tailorofgloucestpott": "Beatrix Potter (1866–1943), <i>The Tailor of Gloucester</i> (Nova York: F. Warne, 1903)",
    "taleofbenjaminbu00pottuoft": "Beatrix Potter, <i>The Tale of Benjamin Bunny</i> (Londres: F. Warne, 1904)",
    "taleofmrjeremyfi00pottuoft": "Beatrix Potter, <i>The Tale of Mr. Jeremy Fisher</i> (Londres: F. Warne, 1906)",
    "cecilyparsleysnu00pott": "Beatrix Potter, <i>Cecily Parsley's Nursery Rhymes</i> (Nova York: F. Warne, 1922)",
    "rcaldecottspictu00cald": "Randolph Caldecott (1846–1886), <i>R. Caldecott's Picture Book</i> (Londres: F. Warne, 1906)",
    "uglyducklingfrom00ande": "John R. Neill (1877–1943), <i>The Ugly Duckling</i> (Chicago: Reilly &amp; Britton, 1908)",
    "babysownaesop00craniala": "Walter Crane (1845–1915), <i>The Baby's Own Æsop</i> (Londres: Routledge, 1887)",
}

# nome: (item, página, caixa, largura máxima em px)
ITENS = {
    "greenaway_janela":   ("underwindowpictv00greerich", 18, (0.27, 0.125, 0.73, 0.31), 1400),
    "greenaway_cha":      ("underwindowpictv00greerich", 20, (0.04, 0.03, 0.96, 0.555), 1800),
    "greenaway_primavera": ("underwindowpictv00greerich", 24, (0.03, 0.02, 0.97, 0.865), 1800),
    "greenaway_girassois": ("underwindowpictv00greerich", 30, (0.05, 0.03, 0.97, 0.66), 1800),
    "greenaway_gansos":   ("underwindowpictv00greerich", 33, (0.08, 0.77, 0.93, 0.94), 1800),
    "greenaway_chuva":    ("underwindowpictv00greerich", 50, (0.04, 0.03, 0.96, 0.46), 1800),
    "greenaway_tina":     ("underwindowpictv00greerich", 55, (0.04, 0.03, 0.96, 0.64), 1800),
    "potter_ratos_costura": ("tailorofgloucestpott", 14, None, 1500),
    "potter_rato_xicara": ("tailorofgloucestpott", 35, None, 1500),
    "potter_neve":        ("tailorofgloucestpott", 56, None, 1500),
    "potter_toca":        ("taleofbenjaminbu00pottuoft", 13, None, 1500),
    "potter_gato_cesto":  ("taleofbenjaminbu00pottuoft", 48, None, 1500),
    "potter_benjamin":    ("taleofbenjaminbu00pottuoft", 9, None, 1500),
    "potter_sapo_lago":   ("taleofmrjeremyfi00pottuoft", 5, None, 1500),
    "potter_sapo_ninfeia": ("taleofmrjeremyfi00pottuoft", 17, None, 1500),
    "potter_sapo_chuva":  ("taleofmrjeremyfi00pottuoft", 24, None, 1500),
    "potter_cozinha":     ("cecilyparsleysnu00pott", 11, None, 1500),
    "potter_gansos":      ("cecilyparsleysnu00pott", 19, None, 1500),
    "potter_cavalo":      ("cecilyparsleysnu00pott", 22, None, 1500),
    "potter_porco":       ("cecilyparsleysnu00pott", 28, None, 1500),
    "potter_jardim_ratos": ("cecilyparsleysnu00pott", 52, None, 1500),
    "caldecott_outono":   ("rcaldecottspictu00cald", 132, (0.03, 0.02, 0.97, 0.90), 1800),
    "caldecott_vaca":     ("rcaldecottspictu00cald", 56, None, 1800),
    "caldecott_ordenha":  ("rcaldecottspictu00cald", 60, None, 1800),
    "caldecott_galo":     ("rcaldecottspictu00cald", 64, None, 1800),
    "cartao_galo":       ("rcaldecottspictu00cald", 64, None, 1000, (0.50, 0.22, 0.95, 0.80)),
    "cartao_vaca":       ("rcaldecottspictu00cald", 56, None, 1000, (0.27, 0.43, 1.00, 0.90)),
    "cartao_cavalo":     ("cecilyparsleysnu00pott", 22, None, 1000, (0.42, 0.25, 0.92, 0.80)),
    "neill_pata":         ("uglyducklingfrom00ande", 9, None, 1800),
}

FONTE = os.path.join(AQUI, "build", "paginas")   # páginas originais baixadas (não versionadas)


def baixar(item, n):
    """Baixa a página digitalizada do Internet Archive, se ainda não estiver em build/paginas."""
    import urllib.request
    os.makedirs(FONTE, exist_ok=True)
    p = os.path.join(FONTE, f"{item}_n{n}.jpg")
    if not os.path.exists(p):
        req = urllib.request.Request(f"https://archive.org/download/{item}/page/n{n}.jpg",
                                     headers={"User-Agent": "TesouroMarina/0.1 (educational, non-commercial)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(p, "wb").write(r.read())
    return p


def papel_para_alfa(im, papel):
    t = np.clip(np.asarray(im).astype(float) / papel, 0, 1)
    alpha = np.clip((1 - t.min(axis=2)) * 1.08, 0, 1)
    alpha[alpha < 0.035] = 0
    cor = np.where(alpha[..., None] > 1e-3, 1 - (1 - t) / np.maximum(alpha[..., None], 1e-3), 1)
    return Image.fromarray((np.dstack([np.clip(cor, 0, 1), alpha]) * 255).astype(np.uint8), "RGBA")


def processar(nome, previa=False):
    item, n, caixa, wmax, *resto = ITENS[nome]
    im = Image.open(baixar(item, n)).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    # cor do papel: mediana das bordas da página
    borda = np.concatenate([a[: h // 25].reshape(-1, 3), a[-h // 25:].reshape(-1, 3),
                            a[:, : w // 25].reshape(-1, 3), a[:, -w // 25:].reshape(-1, 3)])
    papel = np.median(borda, axis=0)
    if caixa is None:
        dif = np.abs(a - papel).sum(axis=2) > 40
        lin = np.where(dif.sum(axis=1) > w * 0.05)[0]
        col = np.where(dif.sum(axis=0) > h * 0.05)[0]
        m = int(max(h, w) * 0.01)
        box = (max(0, col[0] - m), max(0, lin[0] - m), min(w, col[-1] + m), min(h, lin[-1] + m))
    else:
        box = tuple(int(v * s) for v, s in zip(caixa, (w, h, w, h)))
    out = im.crop(box)
    if resto:   # recorte secundário, em frações da ilustração já recortada (cartões)
        sx0, sy0, sx1, sy1 = resto[0]
        out = out.crop((int(sx0 * out.width), int(sy0 * out.height), int(sx1 * out.width), int(sy1 * out.height)))
    if out.width > wmax:
        out = out.resize((wmax, round(out.height * wmax / out.width)), Image.LANCZOS)
    if previa:
        return out
    rgba = papel_para_alfa(out, papel)
    os.makedirs(SAIDA, exist_ok=True)
    # duas versões achatadas (JPEG, leves no PDF): papel branco (impressão) e creme (tela)
    for sufixo, cor in (("branco", (255, 255, 255)), ("creme", (251, 246, 234))):
        fundo = Image.new("RGB", rgba.size, cor)
        fundo.paste(rgba, mask=rgba.split()[3])
        fundo.save(os.path.join(SAIDA, f"{nome}_{sufixo}.jpg"), quality=88, dpi=(300, 300), optimize=True)
    return rgba


def credito(nome):
    item, n, *_ = ITENS[nome]
    return f"{LIVROS[item]}. Domínio público. Internet Archive, <i>{item}</i>, p. n{n}."


if __name__ == "__main__":
    nomes = sys.argv[2:] or list(ITENS)
    if sys.argv[1] == "previa":
        ims = [processar(n, previa=True) for n in nomes]
        for n, im in zip(nomes, ims):
            im.thumbnail((360, 360)); im.save(f"/tmp/claude-0/-home-user-Semear/fa0e4220-4fa6-5daf-9d76-d3166136e335/scratchpad/pd/pv_{n}.jpg")
    else:
        for n in nomes:
            im = processar(n); print(n, im.size)
