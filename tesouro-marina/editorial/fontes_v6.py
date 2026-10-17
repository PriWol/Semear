"""
Pranchas de naturalistas do Volume 6: arquivo de origem, tratamento e crédito.
As imagens vêm do Wikimedia Commons e são gravuras e litografias antigas (Merian, Gould, Hudson/Grönvold e uma prancha da coleção
Brasiliana Iconográfica). O que não existe como prancha antiga utilizável é desenhado pela coleção (motivos7.py), não baixado.
As regras de proveniência são as do Volume 5 (ADR 0018): SHA-256 do arquivo de origem e do JPEG tratado no mesmo manifesto
(dominio_publico/obras.sha256.json), falha fechada, e build dos PDFs sem rede (usa os JPEGs de dominio_publico/v6).
Este módulo reaproveita de fontes_v5.py o que não depende do volume: download com espera, conversão de cor e manifesto.
Uso:  python3 fontes_v6.py verificar | baixar [nomes] | registrar [nomes] | gerar [nomes] | jpegs [nomes] | creditos
"""
import html
import io
import os
import re
import sys

from PIL import Image

from fontes_v5 import AQUI, FONTE, LADO_MAX, PIXELS_MAX, _da_rede, _manifesto, _para_srgb, _registrar, _sha256, limite_de_pixels

SAIDA = os.path.join(AQUI, "dominio_publico", "v6")

# nome: (arquivo no Commons, autoria, obra, ano, acervo ou digitalização, licença conferida no Commons)
OBRAS = {
    "sabia": ("Turdus rufiventer - Coracina scutata, da Coleção Brasiliana Iconográfica.jpg",
              "autoria desconhecida", "<i>Turdus rufiventer</i> e <i>Coracina scutata</i>", "século XIX (data a confirmar)",
              "Brasiliana Iconográfica", "domínio público (marcação do Commons; autoria desconhecida)"),
    "bemtevi": ("Birds of La Plata (Plate) (7788867022).jpg",
                "Henrik Grönvold (1858–1940), em W. H. Hudson (1841–1922)", "<i>Bienteveo Tyrant</i> (<i>Pitangus bolivianus</i>), de <i>Birds of La Plata</i>",
                "1920", "Biodiversity Heritage Library", "domínio público"),
    "beijaflor": ("Heliothrix phaïnolæma + Till. bulbosa - Gould -Humm.jpg",
                  "John Gould (1804–1881) e Henry C. Richter (1821–1902)",
                  "<i>Heliothrix phaïnolæma</i>, de <i>A Monograph of the Trochilidae</i>, vol. 4", "1861",
                  "livro digitalizado, via Wikimedia Commons", "domínio público"),
    "merian_frangipani": ("Metamorphosis insectorum surinamensium (Pl. 8) BHL41398729.jpg",
                          "Maria Sibylla Merian (1647–1717)", "<i>Metamorphosis insectorum Surinamensium</i>, prancha 8", "1705",
                          "Biodiversity Heritage Library", "domínio público"),
}


def credito(nome):
    arq, autor, obra, ano, acervo, lic = OBRAS[nome]
    return (f"{autor}, {obra}, {ano}. {acervo}. Prancha em {lic}: Wikimedia Commons, <i>File:{html.escape(arq)}</i>. "
            f"As cores variam de uma reprodução para outra.")


def _chave_jpeg(nome):
    return f"v6/{nome}.jpg"


def _sha_jpeg(nome):
    with open(os.path.join(SAIDA, f"{nome}.jpg"), "rb") as f:
        return _sha256(f.read())


def registrar_jpegs(nomes=None):
    """Grava no manifesto o SHA-256 de cada JPEG tratado (o que entra no PDF), para uma troca ficar visível no diff."""
    for n in nomes or OBRAS:
        _registrar(_chave_jpeg(n), _sha_jpeg(n))


def verificar():
    """Toda prancha precisa ter acervo e SHA-256 da origem e do JPEG tratado no manifesto, e o JPEG em v6/ tem de bater com ele."""
    man = _manifesto()
    faltam = sorted(o[0] for o in OBRAS.values() if o[0] not in man)
    sem_img = sorted(n for n in OBRAS if not os.path.exists(os.path.join(SAIDA, f"{n}.jpg")))
    trocadas = sorted(n for n in OBRAS if n not in sem_img and man.get(_chave_jpeg(n)) != _sha_jpeg(n))
    sem_fonte = sorted(n for n, o in OBRAS.items() if not o[4] or not o[0] or o[0].startswith(("envio:", "aic:", "nga:")))
    if sem_fonte:
        print("prancha sem acervo, ou que não vem do Commons (o catálogo do Volume 6 só aceita Commons):\n  " + "\n  ".join(sem_fonte))
    if trocadas:
        print("JPEG tratado diferente do registrado (ou sem registro) no manifesto:\n  " + "\n  ".join(trocadas))
    if faltam:
        print("pranchas sem SHA-256 no manifesto:\n  " + "\n  ".join(faltam))
    if sem_img:
        print("pranchas sem imagem tratada em dominio_publico/v6:\n  " + "\n  ".join(sem_img))
    if faltam or sem_img or trocadas or sem_fonte:
        return 1
    print(f"ok: {len(OBRAS)} pranchas com SHA-256 registrado e imagem tratada")
    return 0


def baixar(nome, registrar=False):
    """Arquivo de origem em build/obras, conferido pelo SHA-256 registrado (falha fechada)."""
    arquivo = OBRAS[nome][0]
    os.makedirs(FONTE, exist_ok=True)
    p = os.path.join(FONTE, nome + ".orig")
    esperado = _manifesto().get(arquivo)
    if os.path.exists(p):
        with open(p, "rb") as f:
            dados = f.read()
    else:
        dados = _da_rede(arquivo)
    if esperado and _sha256(dados) != esperado:
        raise ValueError(f"{arquivo}: SHA-256 diferente do registrado (se o arquivo em build/obras/{nome}.orig for de uma tentativa antiga, apague-o e tente de novo)")
    if not esperado and not registrar:
        raise ValueError(f"{arquivo}: sem SHA-256 no manifesto; confira a imagem e rode: python3 fontes_v6.py registrar")
    try:
        with limite_de_pixels():
            Image.open(io.BytesIO(dados)).verify()
    except (Image.DecompressionBombError, Image.DecompressionBombWarning) as e:
        raise ValueError(f"{arquivo}: imagem maior que {PIXELS_MAX} pixels ({e})") from e
    except Exception as e:
        raise ValueError(f"{arquivo}: não é uma imagem válida ({e})") from e
    if not esperado:
        _registrar(arquivo, _sha256(dados))
    with open(p + ".tmp", "wb") as f:
        f.write(dados)
    os.replace(p + ".tmp", p)
    return p


def processar(nome):
    """Reduz ao tamanho de impressão e grava o JPEG tratado (cores fiéis à origem, em sRGB; sem retoque)."""
    with limite_de_pixels(), Image.open(baixar(nome)) as origem:
        im = _para_srgb(origem)
    if max(im.size) > LADO_MAX:
        k = LADO_MAX / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    os.makedirs(SAIDA, exist_ok=True)
    im.save(os.path.join(SAIDA, f"{nome}.jpg"), quality=90, dpi=(300, 300), optimize=True)
    registrar_jpegs([nome])
    return im.size


def linhas_creditos():
    """Linhas da tabela de CREDITOS.md (uma por prancha), a partir de OBRAS."""
    linhas = []
    for nome, (arq, autor, obra, ano, acervo, lic) in OBRAS.items():
        limpo = re.sub(r"<[^>]+>", lambda m: "*" if m.group(0) in ("<i>", "</i>") else "", obra)
        linhas.append(f"| `v6/{nome}.jpg` | {limpo}, {autor}, {ano} | {acervo} | Wikimedia Commons, `File:{arq}` | {lic} |")
    return "\n".join(linhas)


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    nomes = sys.argv[2:] or list(OBRAS)
    if comando == "verificar":
        sys.exit(verificar())
    elif comando in ("baixar", "registrar"):
        for n in nomes:
            baixar(n, registrar=(comando == "registrar"))
    elif comando == "jpegs":
        registrar_jpegs(nomes if sys.argv[2:] else None)
    elif comando == "creditos":
        print(linhas_creditos())
    elif comando == "gerar":
        for n in nomes:
            print(n, processar(n))
    else:
        sys.exit("uso: python3 fontes_v6.py verificar | baixar | registrar [nomes] | gerar [nomes] | jpegs [nomes] | creditos")
