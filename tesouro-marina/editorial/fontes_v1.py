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
    "goldengoosebookb00broo": "L. Leslie Brooke (1862–1940), <i>The Golden Goose Book</i> (Londres: F. Warne, 1905)",
    "LittleRedRiding00Cran": "Walter Crane, <i>Little Red Riding Hood</i> (Londres: Routledge, c. 1875)",
    "histoiredepierre00pott": "Beatrix Potter, <i>Histoire de Pierre Lapin</i> (Londres: F. Warne, 1921)",
    "aesopfables00aesoiala": "Arthur Rackham (1867–1939), <i>Æsop's Fables</i> (Londres: Heinemann, 1912)",
    "Thislittlepigwe00Cran": "Walter Crane, <i>This Little Pig Went to Market</i> (Londres: Routledge, c. 1870)",
    "fairytalesofbrot00grim": "Arthur Rackham, <i>The Fairy Tales of the Brothers Grimm</i> (Nova York: Doubleday, 1916)",
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

# ---- Volume 2
ITENS.update({
    "brooke_ursos_jardim":  ("goldengoosebookb00broo", 34, None, 1600),
    "brooke_mingau":        ("goldengoosebookb00broo", 37, None, 1600),
    "brooke_tigelas":       ("goldengoosebookb00broo", 40, None, 1600),
    "brooke_cama":          ("goldengoosebookb00broo", 43, None, 1600),
    "brooke_urso_porta":    ("goldengoosebookb00broo", 44, None, 1600),
    "brooke_cadeiras":      ("goldengoosebookb00broo", 47, None, 1600),
    "brooke_camas_ursos":   ("goldengoosebookb00broo", 50, None, 1600),
    "brooke_ursos_fim":     ("goldengoosebookb00broo", 53, None, 1600),
    "brooke_porcos_mae":    ("goldengoosebookb00broo", 58, None, 1600),
    "brooke_lobo_palha":    ("goldengoosebookb00broo", 61, None, 1600),
    "brooke_tijolos":       ("goldengoosebookb00broo", 64, None, 1600),
    "brooke_porco_saco":    ("goldengoosebookb00broo", 67, None, 1600),
    "brooke_porco_casa":    ("goldengoosebookb00broo", 68, None, 1600),
    "brooke_barril":        ("goldengoosebookb00broo", 74, None, 1600),
    "crane_mae":            ("LittleRedRiding00Cran", 1, None, 1700, (0, 0.17, 1, 1)),
    "crane_lobo_bosque":    ("LittleRedRiding00Cran", 2, None, 1700, (0, 0.27, 1, 1)),
    "crane_flores":         ("LittleRedRiding00Cran", 5, None, 1700, (0, 0.27, 1, 1)),
    "crane_vovo_janela":    ("LittleRedRiding00Cran", 7, None, 1700, (0, 0, 1, 0.60)),
    "crane_lobo_porta":     ("LittleRedRiding00Cran", 8, None, 1700),
    "crane_chapeu_porta":   ("LittleRedRiding00Cran", 10, None, 1700, (0, 0.17, 1, 1)),
    "crane_lobo_cama":      ("LittleRedRiding00Cran", 13, None, 1700, (0, 0.21, 1, 1)),
    "crane_cacador":        ("LittleRedRiding00Cran", 14, None, 1700, (0, 0.21, 1, 1)),
    "potter_familia":       ("histoiredepierre00pott", 14, None, 1400),
    "potter_mae_cesta":     ("histoiredepierre00pott", 20, None, 1400),
    "potter_irmas":         ("histoiredepierre00pott", 23, None, 1400),
    "potter_pedro_porteira": ("histoiredepierre00pott", 26, None, 1400),
    "potter_rabanetes":     ("histoiredepierre00pott", 29, None, 1400),
    "potter_mcgregor":      ("histoiredepierre00pott", 35, None, 1400),
    "potter_rede":          ("histoiredepierre00pott", 44, None, 1400),
    "potter_regador":       ("histoiredepierre00pott", 53, None, 1400),
    "potter_rato_ervilha":  ("histoiredepierre00pott", 65, None, 1400),
    "potter_gata_lago":     ("histoiredepierre00pott", 68, None, 1400),
    "potter_portao":        ("histoiredepierre00pott", 71, None, 1400),
    "potter_fuga":          ("histoiredepierre00pott", 74, None, 1400),
    "potter_espantalho":    ("histoiredepierre00pott", 77, None, 1400),
    "potter_mae_cha":       ("histoiredepierre00pott", 84, None, 1400),
    "potter_ceia":          ("histoiredepierre00pott", 87, None, 1400),
    "neill_ovo":            ("uglyducklingfrom00ande", 14, None, 1500),
    "neill_terreiro":       ("uglyducklingfrom00ande", 17, None, 1500),
    "neill_lago":           ("uglyducklingfrom00ande", 18, None, 1500),
    "neill_velha":          ("uglyducklingfrom00ande", 22, None, 1500),
    "neill_cisnes_voam":    ("uglyducklingfrom00ande", 25, None, 1500),
    "neill_voo":            ("uglyducklingfrom00ande", 26, None, 1500),
    "neill_cisne":          ("uglyducklingfrom00ande", 30, None, 1500),
    "rackham_lebre":        ("aesopfables00aesoiala", 7, None, 1500),
    "rackham_bremen":       ("fairytalesofbrot00grim", 45, (0.04, 0.20, 0.48, 0.72), 1400),
})

# ---- Volume 3
ITENS.update({
    "crane_porco_mae":     ("Thislittlepigwe00Cran", 1, None, 1500, (0, 0.27, 1, 1)),
    "crane_porco_mercado": ("Thislittlepigwe00Cran", 2, None, 1500, (0, 0.235, 1, 1)),
    "crane_porco_casa":    ("Thislittlepigwe00Cran", 5, None, 1500, (0, 0.27, 1, 1)),
    "crane_porco_nada":    ("Thislittlepigwe00Cran", 8, None, 1500, (0, 0.27, 1, 1)),
    "crane_porco_chora":   ("Thislittlepigwe00Cran", 10, None, 1500, (0, 0.235, 1, 1)),
    "crane_porcos_mesa":   ("Thislittlepigwe00Cran", 14, None, 1500, (0, 0, 1, 0.88)),
})
FONTE = os.path.join(AQUI, "build", "paginas")   # páginas originais baixadas (não versionadas)


MANIFESTO = os.path.join(AQUI, "dominio_publico", "paginas.sha256.json")
LIMITE_BYTES = 30_000_000   # uma página digitalizada tem 1 a 4 MB; acima disso a resposta não é uma página


def _sha256(dados):
    import hashlib
    return hashlib.sha256(dados).hexdigest()


def baixar(item, n):
    """Baixa a página digitalizada do Internet Archive para build/paginas, se ainda não estiver lá.

    É a única chamada de rede do pipeline editorial; roda só no build dos PDFs, fora do app, e não
    envia dado nenhum. Cada página é conferida pelo SHA-256 registrado em paginas.sha256.json, para que
    uma página trocada, corrompida ou renumerada no acervo nunca entre num volume sem aviso.
    """
    import io
    import json
    import urllib.request
    os.makedirs(FONTE, exist_ok=True)
    chave = f"{item}_n{n}"
    p = os.path.join(FONTE, chave + ".jpg")
    esperado = json.load(open(MANIFESTO)).get(chave) if os.path.exists(MANIFESTO) else None
    if os.path.exists(p):
        dados = open(p, "rb").read()
    else:
        req = urllib.request.Request(f"https://archive.org/download/{item}/page/n{n}.jpg",
                                     headers={"User-Agent": "TesouroMarina/0.1 (educational, non-commercial)"})
        with urllib.request.urlopen(req, timeout=120) as r:
            dados = r.read(LIMITE_BYTES + 1)
        if len(dados) > LIMITE_BYTES:
            raise ValueError(f"{chave}: resposta maior que {LIMITE_BYTES} bytes")
        Image.open(io.BytesIO(dados)).verify()   # recusa o que não for uma imagem válida
    if esperado and _sha256(dados) != esperado:
        raise ValueError(f"{chave}: SHA-256 diferente do registrado em {os.path.basename(MANIFESTO)}")
    if not esperado:
        print(f"aviso: {chave} sem SHA-256 registrado; acrescente-o ao manifesto depois de conferir a imagem")
    if not os.path.exists(p):
        open(p, "wb").write(dados)
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
