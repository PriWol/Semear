"""
Reproduções de obras de arte do Volume 5: arquivo de origem, tratamento e crédito.
As imagens vêm do Wikimedia Commons (https://commons.wikimedia.org). Só entram obras cujo autor morreu há mais de
70 anos e que o Commons marca como domínio público (ou CC0). O arquivo de origem de cada obra é conferido por
SHA-256 (dominio_publico/obras.sha256.json); as versões tratadas (JPEG) ficam em dominio_publico/v5 e é com elas que
os PDFs são gerados, então o build dos PDFs não usa a rede.
Uso:  python3 fontes_v5.py verificar | baixar [nomes] | registrar [nomes] | gerar [nomes] | creditos
"""
import hashlib
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "dominio_publico", "v5")
FONTE = os.path.join(AQUI, "build", "obras")
MANIFESTO = os.path.join(AQUI, "dominio_publico", "obras.sha256.json")
LIMITE_BYTES = 60_000_000
LADO_MAX = 2000        # px do maior lado (≈ 170 mm a 300 dpi)
UA = "TesouroMarina/0.1 (educational, non-commercial; https://github.com/PriWol/Semear)"

# nome: (arquivo no Commons, autor, obra, ano, acervo, licença conferida no Commons)
OBRAS = {
    "durer_lebre": ("Albrecht Dürer - Hare, 1502 - Google Art Project.jpg",
                    "Albrecht Dürer (1471–1528)", "<i>A lebre jovem</i> (Feldhase)", "1502", "Albertina, Viena", "domínio público"),
    "durer_tufo": ("Albrecht Dürer - The Large Piece of Turf, 1503 - Google Art Project.jpg",
                   "Albrecht Dürer (1471–1528)", "<i>O grande tufo de relva</i> (Das große Rasenstück)", "1503", "Albertina, Viena", "domínio público"),
    "kandinsky_quadrados": ("Vassily Kandinsky, 1913 - Color Study, Squares with Concentric Circles.jpg",
                            "Wassily Kandinsky (1866–1944)", "<i>Estudo de cores: quadrados com círculos concêntricos</i>", "1913",
                            "Städtische Galerie im Lenbachhaus, Munique", "domínio público"),
    "kandinsky_circulos": ("Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg",
                           "Wassily Kandinsky (1866–1944)", "<i>Vários círculos</i> (Several Circles)", "1926",
                           "Museu Solomon R. Guggenheim, Nova York", "domínio público"),
    "monet_papoulas": ("Claude Monet - Poppy Field - Google Art Project.jpg",
                       "Claude Monet (1840–1926)", "<i>Os coquelicots</i> (Les Coquelicots)", "1873", "Musée d'Orsay, Paris", "domínio público"),
    "monet_ninfeias": ("Claude Monet - Water Lilies - 1906, Ryerson.jpg",
                       "Claude Monet (1840–1926)", "<i>Ninfeias</i> (Water Lilies)", "1906", "Instituto de Arte de Chicago", "domínio público"),
    "vangogh_girassois": ("Vincent Willem van Gogh, Dutch - Sunflowers - Google Art Project.jpg",
                          "Vincent van Gogh (1853–1890)", "<i>Girassóis</i> (Sunflowers)", "Arles, janeiro de 1889", "", "domínio público"),
    "cassatt_banho": ("Mary Cassatt - The Child's Bath - Google Art Project.jpg",
                      "Mary Cassatt (1844–1926)", "<i>O banho da criança</i> (The Child's Bath)", "1893", "Instituto de Arte de Chicago", "domínio público"),
    "cassatt_poltrona": ("Mary Cassatt, Little Girl in a Blue Armchair, 1878, NGA 61368.jpg",
                         "Mary Cassatt (1844–1926)", "<i>Menina na poltrona azul</i> (Little Girl in a Blue Armchair)", "1878",
                         "National Gallery of Art, Washington", "CC0 (acesso aberto do acervo)"),
    "cassatt_mae": ("Mary Cassatt - Mother About to Wash Her Sleepy Child - Google Art Project.jpg",
                    "Mary Cassatt (1844–1926)", "<i>Mãe prestes a lavar a filha sonolenta</i> (Mother About to Wash Her Sleepy Child)", "1880",
                    "Museu de Arte do Condado de Los Angeles (LACMA)", "domínio público"),
}


def credito(nome):
    arq, autor, obra, ano, acervo, lic = OBRAS[nome]
    onde = f" {acervo}." if acervo else ""
    return (f"{autor}, {obra}, {ano}.{onde} Reprodução em {lic}: Wikimedia Commons, <i>File:{arq}</i>. "
            f"As cores variam de uma reprodução para outra.")


def _sha256(dados):
    return hashlib.sha256(dados).hexdigest()


def _manifesto():
    if not os.path.exists(MANIFESTO):
        return {}
    with open(MANIFESTO, encoding="utf-8") as f:
        return json.load(f)


def _registrar(chave, sha):
    man = _manifesto()
    man[chave] = sha
    with open(MANIFESTO, "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, sort_keys=True, ensure_ascii=False)
    print(f"registrado: {chave}")


def verificar():
    """Toda obra de OBRAS precisa ter o SHA-256 do arquivo de origem no manifesto e a imagem tratada em v5/."""
    man = _manifesto()
    faltam = sorted(o[0] for o in OBRAS.values() if o[0] not in man)
    sem_img = sorted(n for n in OBRAS if not os.path.exists(os.path.join(SAIDA, f"{n}.jpg")))
    if faltam or sem_img:
        if faltam:
            print("obras sem SHA-256 no manifesto:\n  " + "\n  ".join(faltam))
        if sem_img:
            print("obras sem imagem tratada em dominio_publico/v5:\n  " + "\n  ".join(sem_img))
        return 1
    print(f"ok: {len(OBRAS)} obras com SHA-256 registrado e imagem tratada")
    return 0


def _da_rede(arquivo):
    url = "https://upload.wikimedia.org/wikipedia/commons/" + _caminho_commons(arquivo)
    for i in range(30):   # o Commons limita o ritmo de pedidos (429): espera e tenta de novo
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                dados = r.read(LIMITE_BYTES + 1)
            if len(dados) > LIMITE_BYTES:
                raise ValueError(f"{arquivo}: resposta maior que {LIMITE_BYTES} bytes")
            return dados
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(20 + 5 * i)
    raise RuntimeError(f"{arquivo}: muitos pedidos recusados (429)")


def _caminho_commons(arquivo):
    """Caminho do arquivo no servidor: /<h>/<hh>/<nome>, com h e hh vindos do MD5 do nome com sublinhados."""
    nome = arquivo.replace(" ", "_")
    h = hashlib.md5(nome.encode("utf-8")).hexdigest()
    return f"{h[0]}/{h[:2]}/{urllib.parse.quote(nome)}"


def baixar(nome, registrar=False):
    """Arquivo de origem em build/obras, conferido pelo SHA-256 registrado (falha fechada)."""
    arquivo = OBRAS[nome][0]
    os.makedirs(FONTE, exist_ok=True)
    p = os.path.join(FONTE, nome + ".orig")
    esperado = _manifesto().get(arquivo)
    if os.path.exists(p):
        dados = open(p, "rb").read()
    else:
        dados = _da_rede(arquivo)
    if esperado and _sha256(dados) != esperado:
        raise ValueError(f"{arquivo}: SHA-256 diferente do registrado em {os.path.basename(MANIFESTO)}")
    if not esperado and not registrar:
        raise ValueError(f"{arquivo}: sem SHA-256 no manifesto; confira a imagem e rode: python3 fontes_v5.py registrar")
    try:
        Image.open(io.BytesIO(dados)).verify()
    except Exception as e:
        raise ValueError(f"{arquivo}: não é uma imagem válida ({e})") from e
    if not esperado:
        _registrar(arquivo, _sha256(dados))
    with open(p + ".tmp", "wb") as f:
        f.write(dados)
    os.replace(p + ".tmp", p)
    return p


def processar(nome):
    """Reduz ao tamanho de impressão e grava o JPEG tratado (cores intactas, sem retoque)."""
    Image.MAX_IMAGE_PIXELS = 400_000_000
    im = Image.open(baixar(nome)).convert("RGB")
    if max(im.size) > LADO_MAX:
        k = LADO_MAX / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    os.makedirs(SAIDA, exist_ok=True)
    im.save(os.path.join(SAIDA, f"{nome}.jpg"), quality=90, dpi=(300, 300), optimize=True)
    return im.size


def linhas_creditos():
    """Linhas da tabela de CREDITOS.md (uma por obra), a partir de OBRAS."""
    import re
    linhas = []
    for nome, (arq, autor, obra, ano, acervo, lic) in OBRAS.items():
        limpo = re.sub(r"<[^>]+>", lambda m: "*" if m.group(0) in ("<i>", "</i>") else "", obra)
        linhas.append(f"| `v5/{nome}.jpg` | {limpo}, {autor}, {ano} | {acervo or 'ver legenda do Commons'} | `File:{arq}` | {lic} |")
    return "\n".join(linhas)


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    nomes = sys.argv[2:] or list(OBRAS)
    if comando == "verificar":
        sys.exit(verificar())
    elif comando in ("baixar", "registrar"):
        for n in nomes:
            baixar(n, registrar=(comando == "registrar"))
    elif comando == "creditos":
        print(linhas_creditos())
    elif comando == "gerar":
        for n in nomes:
            print(n, processar(n))
    else:
        sys.exit("uso: python3 fontes_v5.py verificar | baixar | registrar [nomes] | gerar [nomes] | creditos")
