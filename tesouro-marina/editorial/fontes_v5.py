"""
Reproduções de obras de arte do Volume 5: arquivo de origem, tratamento e crédito.
As imagens vêm do Wikimedia Commons (https://commons.wikimedia.org) ou de acervos de museus com acesso aberto (Instituto
de Arte de Chicago e National Gallery of Art). Só entram obras cujo autor morreu há mais de 70 anos e que a fonte marca como
domínio público (ou CC0). O arquivo de origem de cada obra é conferido por SHA-256 (dominio_publico/obras.sha256.json);
as versões tratadas (JPEG) ficam em dominio_publico/v5 e é com elas que os PDFs são gerados, então o build dos PDFs não usa a rede.
Uso:  python3 fontes_v5.py verificar | baixar [nomes] | registrar [nomes] | gerar [nomes] | jpegs [nomes] | creditos
"""
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "dominio_publico", "v5")
FONTE = os.path.join(AQUI, "build", "obras")
MANIFESTO = os.path.join(AQUI, "dominio_publico", "obras.sha256.json")
LIMITE_BYTES = 60_000_000
ESPERA_MAX = 3600      # nunca espera mais de 1 h por pedido, mesmo que a fonte peça mais
ESPERA_TOTAL = 7200    # e desiste depois de 2 h de espera acumulada num mesmo pedido
LADO_MAX = 2000        # px do maior lado (≈ 170 mm a 300 dpi)
UA = "TesouroMarina/0.1 (educational, non-commercial; https://github.com/PriWol/Semear)"

# nome: (arquivo no Commons, autor, obra, ano, acervo, licença conferida no Commons)
OBRAS = {
    "durer_lebre": ("Albrecht Dürer - Hare, 1502 - Google Art Project.jpg",
                    "Albrecht Dürer (1471–1528)", "<i>A lebre jovem</i> (Feldhase)", "1502", "Albertina, Viena", "domínio público"),
    "durer_primulas": ("nga:21113c79-7136-4bce-9e8d-65b9254628bd",
                       "Albrecht Dürer (1471–1528)", "<i>Tufo de prímulas</i> (Tuft of Cowslips)", "1526",
                       "National Gallery of Art, Washington", "CC0 (acesso aberto do acervo)"),
    "kandinsky_quadrados": ("Vassily Kandinsky, 1913 - Color Study, Squares with Concentric Circles.jpg",
                            "Wassily Kandinsky (1866–1944)", "<i>Estudo de cores: quadrados com círculos concêntricos</i>", "1913",
                            "Städtische Galerie im Lenbachhaus, Munique", "domínio público"),
    "kandinsky_circulos": ("Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg",
                           "Wassily Kandinsky (1866–1944)", "<i>Vários círculos</i> (Several Circles)", "1926",
                           "Museu Solomon R. Guggenheim, Nova York", "domínio público"),
    "monet_medas": ("aic:a38e2828-ec6f-ece1-a30f-70243449197b",
                    "Claude Monet (1840–1926)", "<i>Medas de trigo (fim do verão)</i> (Stacks of Wheat, End of Summer)", "1890–91",
                    "Instituto de Arte de Chicago", "domínio público (acesso aberto do acervo)"),
    "monet_ninfeias": ("aic:3c27b499-af56-f0d5-93b5-a7f2f1ad5813",
                       "Claude Monet (1840–1926)", "<i>Ninfeias</i> (Water Lilies)", "1906", "Instituto de Arte de Chicago", "domínio público (acesso aberto do acervo)"),
    "vangogh_girassois": ("Vincent Willem van Gogh 128.jpg",
                          "Vincent van Gogh (1853–1890)", "<i>Girassóis</i> (Vase with Twelve Sunflowers)", "Arles, agosto de 1888",
                          "Neue Pinakothek, Munique", "domínio público (PD-Art, reprodução do Projeto Yorck)"),
    "cassatt_banho": ("aic:3b885ae0-4d46-5fe4-d70a-00474827f02c",
                      "Mary Cassatt (1844–1926)", "<i>O banho da criança</i> (The Child's Bath)", "1893", "Instituto de Arte de Chicago", "domínio público (acesso aberto do acervo)"),
    "cassatt_poltrona": ("nga:6dc9ca49-ea8c-4314-985a-ba2cfc3965cd",
                         "Mary Cassatt (1844–1926)", "<i>Menina na poltrona azul</i> (Little Girl in a Blue Armchair)", "1878",
                         "National Gallery of Art, Washington", "CC0 (acesso aberto do acervo)"),
    "cassatt_praia": ("nga:20818b10-1f66-4186-ac55-af70e3586084",
                      "Mary Cassatt (1844–1926)", "<i>Crianças brincando na praia</i> (Children Playing on the Beach)", "1884",
                      "National Gallery of Art, Washington", "CC0 (acesso aberto do acervo)"),
}


# nº de inventário e página da obra no acervo, para as obras que não vêm do Commons
REFERENCIAS = {
    "monet_ninfeias": ("inv. 1933.1157", "https://www.artic.edu/artworks/16568"),
    "cassatt_banho": ("inv. 1910.2", "https://www.artic.edu/artworks/111442"),
    "cassatt_poltrona": ("inv. 1983.1.18", "https://www.nga.gov/artworks/61368"),
    "durer_primulas": ("inv. 1991.217.1", "https://www.nga.gov/artworks/74162"),
    "monet_medas": ("inv. 1985.1103", "https://www.artic.edu/artworks/64818"),
    "cassatt_praia": ("inv. 1970.17.19", "https://www.nga.gov/artworks/52163"),
}


def credito(nome):
    arq, autor, obra, ano, acervo, lic = OBRAS[nome]
    onde = f" {acervo}." if acervo else ""
    if nome in REFERENCIAS:
        inv, url = REFERENCIAS[nome]
        return (f"{autor}, {obra}, {ano}.{onde} Reprodução em {lic}: {inv}, {url}. "
                f"As cores variam de uma reprodução para outra.")
    if arq.startswith("envio:"):   # arquivo entregue pela dona do produto, sem endereço de origem registrado
        return f"{autor}, {obra}, {ano}.{onde} Reprodução em {lic}, arquivo fornecido pela editora. As cores variam de uma reprodução para outra."
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


def _chave_jpeg(nome):
    return f"v5/{nome}.jpg"


def _sha_jpeg(nome):
    with open(os.path.join(SAIDA, f"{nome}.jpg"), "rb") as f:
        return _sha256(f.read())


def registrar_jpegs(nomes=None):
    """Grava no manifesto o SHA-256 de cada JPEG tratado (o que de fato entra no PDF), para uma troca ficar visível no diff."""
    for n in nomes or OBRAS:
        _registrar(_chave_jpeg(n), _sha_jpeg(n))


def verificar():
    """Toda obra de OBRAS precisa ter o SHA-256 da origem e o do JPEG tratado no manifesto, e o JPEG tratado em v5/ tem de bater com ele."""
    man = _manifesto()
    faltam = sorted(o[0] for o in OBRAS.values() if o[0] not in man)
    sem_img = sorted(n for n in OBRAS if not os.path.exists(os.path.join(SAIDA, f"{n}.jpg")))
    trocadas = sorted(n for n in OBRAS if n not in sem_img and man.get(_chave_jpeg(n)) != _sha_jpeg(n))
    # CLAUDE.md: "só domínio público, com fonte registrada". Arquivo entregue à mão só vale com acervo e endereço de origem.
    sem_fonte = sorted(n for n, o in OBRAS.items() if o[0].startswith("envio:") and (not o[4] or n not in REFERENCIAS))
    if sem_fonte:
        print("obra enviada à mão sem acervo e endereço de origem registrados:\n  " + "\n  ".join(sem_fonte))
    if trocadas:
        print("JPEG tratado diferente do registrado (ou sem registro) no manifesto:\n  " + "\n  ".join(trocadas))
    if faltam or sem_img or trocadas or sem_fonte:
        if faltam:
            print("obras sem SHA-256 no manifesto:\n  " + "\n  ".join(faltam))
        if sem_img:
            print("obras sem imagem tratada em dominio_publico/v5:\n  " + "\n  ".join(sem_img))
        return 1
    print(f"ok: {len(OBRAS)} obras com SHA-256 registrado e imagem tratada")
    return 0


def _espera(retry_after):
    """Segundos a esperar segundo o cabeçalho Retry-After (número de segundos ou data HTTP); 600 se vier ausente ou ilegível."""
    if not retry_after:
        return 600
    try:
        return min(ESPERA_MAX, max(0, int(retry_after)))
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime
        from datetime import datetime, timezone
        return min(ESPERA_MAX, max(0, int((parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds())))
    except (TypeError, ValueError):
        return 600


def _pedir(url, cabecalhos):
    esperado = 0
    for _ in range(12):   # a fonte pode limitar o ritmo de pedidos (429): espera o tempo que ela pede e tenta de novo
        try:
            req = urllib.request.Request(url, headers=cabecalhos)
            with urllib.request.urlopen(req, timeout=180) as r:
                dados = r.read(LIMITE_BYTES + 1)
            if len(dados) > LIMITE_BYTES:
                raise ValueError(f"{url}: resposta maior que {LIMITE_BYTES} bytes")
            return dados
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            # a fonte diz quanto esperar (Retry-After, em segundos); pedir antes disso só renova a espera
            espera = _espera(e.headers.get("Retry-After")) + 15
            if esperado + espera > ESPERA_TOTAL:
                raise RuntimeError(f"{url}: passaria de {ESPERA_TOTAL} s de espera acumulada (429 persistente)")
            esperado += espera
            print(f"{url}: 429, esperando {espera} s antes de tentar de novo", file=sys.stderr, flush=True)
            time.sleep(espera)
    raise RuntimeError(f"{url}: muitos pedidos recusados (429)")


def _da_rede(chave):
    """chave: nome do arquivo no Commons, 'aic:<id da imagem>' ou 'nga:<uuid da imagem>'."""
    if chave.startswith("envio:"):
        raise FileNotFoundError(f"{chave}: arquivo fornecido à mão; coloque-o em build/obras/<nome>.orig")
    if chave.startswith("aic:"):
        # IIIF do Instituto de Arte de Chicago (acesso aberto); a barreira do site recusa clientes sem User-Agent de navegador
        return _pedir(f"https://www.artic.edu/iiif/2/{chave[4:]}/full/1686,/0/default.jpg",
                      {"User-Agent": "Mozilla/5.0 (compatible; TesouroMarina/0.1; educational; +https://github.com/PriWol/Semear)",
                       "AIC-User-Agent": "TesouroMarina (educational; https://github.com/PriWol/Semear)"})
    if chave.startswith("nga:"):
        return _pedir(f"https://api.nga.gov/iiif/{chave[4:]}/full/!1800,1800/0/default.jpg", {"User-Agent": UA})
    return _pedir("https://upload.wikimedia.org/wikipedia/commons/" + _caminho_commons(chave), {"User-Agent": UA})


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
        with open(p, "rb") as f:
            dados = f.read()
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
    registrar_jpegs([nome])
    return im.size


def linhas_creditos():
    """Linhas da tabela de CREDITOS.md (uma por obra), a partir de OBRAS."""
    import re
    linhas = []
    for nome, (arq, autor, obra, ano, acervo, lic) in OBRAS.items():
        limpo = re.sub(r"<[^>]+>", lambda m: "*" if m.group(0) in ("<i>", "</i>") else "", obra)
        if nome in REFERENCIAS:
            inv, url = REFERENCIAS[nome]
            fonte = f"{acervo}, {inv}, {url}"
        elif arq.startswith("envio:"):
            fonte = "arquivo fornecido pela editora (acervo e endereço de origem a confirmar)"
        else:
            fonte = f"Wikimedia Commons, `File:{arq}`"
        linhas.append(f"| `v5/{nome}.jpg` | {limpo}, {autor}, {ano} | {acervo or 'a confirmar'} | {fonte} | {lic} |")
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
        sys.exit("uso: python3 fontes_v5.py verificar | baixar | registrar [nomes] | gerar [nomes] | jpegs [nomes] | creditos")
