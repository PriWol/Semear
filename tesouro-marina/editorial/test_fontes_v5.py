"""Testes das reproduções de obras do Volume 5 (ADR 0011 e 0018). Rodar: python3 -m unittest test_fontes_v5

Nenhum teste usa a rede: o arquivo de origem já está em cache numa pasta temporária.
"""
import http.client
import io
import json
import os
import tempfile
import unittest
import urllib.error
from unittest import mock

from PIL import Image

import fontes_v5

def _jpeg():
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), (200, 180, 150)).save(buf, "JPEG")
    return buf.getvalue()


IMAGEM = _jpeg()
SHA = fontes_v5._sha256(IMAGEM)
NOME = "durer_lebre"
ARQUIVO = fontes_v5.OBRAS[NOME][0]


class FalhaFechada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.antes = (fontes_v5.MANIFESTO, fontes_v5.FONTE, fontes_v5.SAIDA)
        fontes_v5.MANIFESTO = os.path.join(self.tmp.name, "manifesto.json")
        fontes_v5.FONTE = os.path.join(self.tmp.name, "obras")
        fontes_v5.SAIDA = os.path.join(self.tmp.name, "v5")
        os.makedirs(fontes_v5.FONTE)
        with open(os.path.join(fontes_v5.FONTE, NOME + ".orig"), "wb") as f:
            f.write(IMAGEM)
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        fontes_v5.MANIFESTO, fontes_v5.FONTE, fontes_v5.SAIDA = self.antes

    def _manifesto(self, dados):
        with open(fontes_v5.MANIFESTO, "w") as f:
            json.dump(dados, f)

    def test_arquivo_com_hash_certo_passa(self):
        self._manifesto({ARQUIVO: SHA})
        self.assertTrue(fontes_v5.baixar(NOME).endswith(NOME + ".orig"))

    def test_arquivo_com_hash_diferente_e_recusado(self):
        self._manifesto({ARQUIVO: "0" * 64})
        with self.assertRaisesRegex(ValueError, "SHA-256 diferente"):
            fontes_v5.baixar(NOME)

    def test_arquivo_sem_hash_e_recusado_fora_do_registrar(self):
        self._manifesto({})
        with self.assertRaisesRegex(ValueError, "sem SHA-256"):
            fontes_v5.baixar(NOME)

    def test_registrar_grava_o_hash_novo(self):
        self._manifesto({})
        fontes_v5.baixar(NOME, registrar=True)
        with open(fontes_v5.MANIFESTO) as f:
            self.assertEqual(json.load(f)[ARQUIVO], SHA)

    def test_arquivo_que_nao_e_imagem_e_recusado(self):
        lixo = b"nao sou uma imagem"
        with open(os.path.join(fontes_v5.FONTE, NOME + ".orig"), "wb") as f:
            f.write(lixo)
        self._manifesto({ARQUIVO: fontes_v5._sha256(lixo)})
        with self.assertRaisesRegex(ValueError, "não é uma imagem válida"):
            fontes_v5.baixar(NOME)

    def test_processar_reduz_e_grava_o_jpeg(self):
        self._manifesto({ARQUIVO: SHA})
        self.assertEqual(fontes_v5.processar(NOME), (8, 8))
        self.assertTrue(os.path.exists(os.path.join(fontes_v5.SAIDA, NOME + ".jpg")))

    def test_verificar_aponta_obra_sem_hash_ou_sem_imagem(self):
        self._manifesto({})
        self.assertEqual(fontes_v5.verificar(), 1)


class Utilitarios(unittest.TestCase):
    def test_retry_after_em_segundos_data_http_ou_ilegivel(self):
        self.assertEqual(fontes_v5._espera("120"), 120)
        self.assertEqual(fontes_v5._espera(None), 600)
        self.assertEqual(fontes_v5._espera("amanhã, talvez"), 600)
        self.assertEqual(fontes_v5._espera("Wed, 21 Oct 2015 07:28:00 GMT"), 0)   # data no passado: não espera
        self.assertEqual(fontes_v5._espera("999999"), fontes_v5.ESPERA_MAX)       # teto de 1 h

    def test_envio_sem_arquivo_falha_com_mensagem_clara(self):
        with self.assertRaisesRegex(FileNotFoundError, "build/obras"):
            fontes_v5._da_rede("envio:qualquer")

    def test_credito_de_obra_sem_acervo_nao_deixa_buraco(self):
        antes = dict(fontes_v5.OBRAS)
        try:
            fontes_v5.OBRAS["sem_acervo"] = ("envio:sem_acervo", "Autor (1800–1850)", "<i>X</i>", "1840", "", "domínio público")
            c = fontes_v5.credito("sem_acervo")
        finally:
            fontes_v5.OBRAS.clear(); fontes_v5.OBRAS.update(antes)
        self.assertNotIn("None", c)
        self.assertNotIn("..", c)
        self.assertNotIn("  ", c)

    def test_verificar_acusa_obra_enviada_a_mao_sem_fonte(self):
        with tempfile.TemporaryDirectory() as tmp:
            antes = (fontes_v5.SAIDA, fontes_v5.MANIFESTO, dict(fontes_v5.OBRAS), dict(fontes_v5.REFERENCIAS))
            try:
                fontes_v5.SAIDA = os.path.join(tmp, "v5")
                fontes_v5.MANIFESTO = os.path.join(tmp, "m.json")
                os.makedirs(fontes_v5.SAIDA)
                fontes_v5.OBRAS.clear()
                fontes_v5.OBRAS["x"] = ("envio:x", "Autor (1800–1850)", "<i>X</i>", "1840", "", "domínio público")
                with open(os.path.join(fontes_v5.SAIDA, "x.jpg"), "wb") as f:
                    f.write(IMAGEM)
                with open(fontes_v5.MANIFESTO, "w") as f:
                    json.dump({"envio:x": "0" * 64}, f)
                fontes_v5.registrar_jpegs(["x"])
                self.assertEqual(fontes_v5.verificar(), 1)          # sem acervo nem endereço
                fontes_v5.OBRAS["x"] = ("envio:x", "Autor (1800–1850)", "<i>X</i>", "1840", "Museu Y", "domínio público")
                fontes_v5.REFERENCIAS["x"] = ("inv. 1", "https://museu.example/1")
                self.assertEqual(fontes_v5.verificar(), 0)          # com acervo e endereço passa
                fontes_v5.OBRAS["x"] = ("commons:X.jpg", "Autor (1800–1850)", "<i>X</i>", "1840", "", "domínio público")
                fontes_v5.registrar_jpegs(["x"])
                with open(fontes_v5.MANIFESTO) as f:
                    m = json.load(f)
                m["commons:X.jpg"] = "0" * 64
                with open(fontes_v5.MANIFESTO, "w") as f:
                    json.dump(m, f)
                self.assertEqual(fontes_v5.verificar(), 1)          # obra de qualquer origem sem acervo é recusada
                fontes_v5.OBRAS["x"] = ("aic:x", "Autor (1800–1850)", "<i>X</i>", "1840", "Museu Y", "domínio público")
                fontes_v5.REFERENCIAS.pop("x", None)
                fontes_v5.registrar_jpegs(["x"])
                with open(fontes_v5.MANIFESTO) as f:
                    m = json.load(f)
                m["aic:x"] = "0" * 64
                with open(fontes_v5.MANIFESTO, "w") as f:
                    json.dump(m, f)
                self.assertEqual(fontes_v5.verificar(), 1)          # obra de museu sem inventário/endereço é recusada
            finally:
                fontes_v5.SAIDA, fontes_v5.MANIFESTO = antes[:2]
                fontes_v5.OBRAS.clear(); fontes_v5.OBRAS.update(antes[2])
                fontes_v5.REFERENCIAS.clear(); fontes_v5.REFERENCIAS.update(antes[3])

    def test_verificar_acusa_imagem_tratada_que_falta(self):
        with tempfile.TemporaryDirectory() as tmp:
            antes = (fontes_v5.SAIDA, fontes_v5.MANIFESTO)
            try:
                fontes_v5.SAIDA = os.path.join(tmp, "v5")   # pasta sem nenhum JPEG tratado
                self.assertEqual(fontes_v5.verificar(), 1)
            finally:
                fontes_v5.SAIDA, fontes_v5.MANIFESTO = antes


class CreditoEscapado(unittest.TestCase):
    def test_inventario_e_endereco_de_museu_sao_escapados(self):
        antes = (dict(fontes_v5.OBRAS), dict(fontes_v5.REFERENCIAS))
        try:
            fontes_v5.OBRAS["x"] = ("aic:x", "Autor (1800–1850)", "<i>X</i>", "1840", "Museu", "domínio público")
            fontes_v5.REFERENCIAS["x"] = ("inv. 1 & 2", "https://museu.example/a?b=1&c=2")
            c = fontes_v5.credito("x")
        finally:
            fontes_v5.OBRAS.clear(); fontes_v5.OBRAS.update(antes[0])
            fontes_v5.REFERENCIAS.clear(); fontes_v5.REFERENCIAS.update(antes[1])
        self.assertIn("inv. 1 &amp; 2", c)
        self.assertIn("b=1&amp;c=2", c)

    def test_nome_de_arquivo_com_e_comercial_e_escapado(self):
        antes = dict(fontes_v5.OBRAS)
        try:
            fontes_v5.OBRAS["x"] = ("Dürer & Cia <1>.jpg", "Autor (1800–1850)", "<i>X</i>", "1840", "Museu", "domínio público")
            c = fontes_v5.credito("x")
        finally:
            fontes_v5.OBRAS.clear(); fontes_v5.OBRAS.update(antes)
        self.assertIn("Dürer &amp; Cia &lt;1&gt;.jpg", c)
        self.assertIn("<i>X</i>", c)


class LimiteDePixels(unittest.TestCase):
    def test_teto_sobe_so_dentro_do_bloco_e_volta(self):
        antes = Image.MAX_IMAGE_PIXELS
        with fontes_v5.limite_de_pixels():
            self.assertEqual(Image.MAX_IMAGE_PIXELS, fontes_v5.PIXELS_MAX)
        self.assertEqual(Image.MAX_IMAGE_PIXELS, antes)

    def test_teto_volta_mesmo_com_erro(self):
        antes = Image.MAX_IMAGE_PIXELS
        with self.assertRaises(RuntimeError):
            with fontes_v5.limite_de_pixels():
                raise RuntimeError("falha")
        self.assertEqual(Image.MAX_IMAGE_PIXELS, antes)

    def test_aviso_de_bomba_de_descompressao_vira_erro(self):
        import warnings
        with self.assertRaises(Image.DecompressionBombWarning):
            with fontes_v5.limite_de_pixels():
                warnings.warn("grande", Image.DecompressionBombWarning)


class PerfilDeCor(unittest.TestCase):
    """_para_srgb: perfil sRGB passa sem mexer nos pixels; outro perfil é convertido, não descartado."""

    @staticmethod
    def _imagem_com_perfil():
        from PIL import ImageCms
        im = Image.new("RGB", (4, 4), (200, 40, 40))
        im.info["icc_profile"] = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
        return im

    def test_srgb_nao_muda_os_pixels(self):
        im = self._imagem_com_perfil()
        self.assertEqual(fontes_v5._para_srgb(im).getpixel((0, 0)), (200, 40, 40))

    def test_outro_perfil_e_convertido(self):
        from PIL import ImageCms
        im = self._imagem_com_perfil()
        with mock.patch("fontes_v5.ImageCms.getProfileDescription", return_value="Adobe RGB (1998)"), \
                mock.patch("fontes_v5.ImageCms.profileToProfile", wraps=ImageCms.profileToProfile) as converte:
            saida = fontes_v5._para_srgb(im)
        converte.assert_called_once()
        self.assertEqual(saida.mode, "RGB")

    def test_perfil_corrompido_nao_aborta(self):
        im = Image.new("RGB", (2, 2), (10, 20, 30))
        im.info["icc_profile"] = b"lixo"
        with mock.patch("sys.stderr", new=io.StringIO()) as erro:
            saida = fontes_v5._para_srgb(im)
        self.assertEqual(saida.getpixel((0, 0)), (10, 20, 30))
        self.assertIn("aviso", erro.getvalue())

    def test_sem_perfil_so_converte_o_modo(self):
        self.assertEqual(fontes_v5._para_srgb(Image.new("L", (2, 2), 128)).mode, "RGB")


class PedirComLimite(unittest.TestCase):
    """_pedir: espera o Retry-After em 429, repete falhas de rede e 5xx poucas vezes, teto de tentativas e limite de tamanho (sem rede)."""

    @staticmethod
    def _erro(codigo, retry_after=None):
        import email.message
        h = email.message.Message()
        if retry_after is not None:
            h["Retry-After"] = str(retry_after)
        return urllib.error.HTTPError("https://exemplo/x", codigo, "erro", h, None)

    @staticmethod
    def _resposta(dados):
        class R(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False
        return R(dados)

    def test_429_dorme_retry_after_mais_15_e_tenta_de_novo(self):
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=[self._erro(429, 120), self._resposta(b"ok")]), \
                mock.patch("fontes_v5.time.sleep") as dorme:
            self.assertEqual(fontes_v5._pedir("https://exemplo/x", {}), b"ok")
        dorme.assert_called_once_with(135)

    def test_erro_que_nao_e_429_nao_tenta_de_novo(self):
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=self._erro(404)) as abre, \
                mock.patch("fontes_v5.time.sleep") as dorme:
            with self.assertRaises(urllib.error.HTTPError):
                fontes_v5._pedir("https://exemplo/x", {})
        self.assertEqual(abre.call_count, 1)
        dorme.assert_not_called()

    def test_queda_de_rede_e_5xx_tentam_de_novo_depois_de_espera_curta(self):
        falhas = [urllib.error.URLError("sem rede"), http.client.IncompleteRead(b"x"), self._erro(503), self._resposta(b"ok")]
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=falhas), \
                mock.patch("fontes_v5.time.sleep") as dorme:
            self.assertEqual(fontes_v5._pedir("https://exemplo/x", {}), b"ok")
        self.assertEqual(dorme.call_count, 3)

    def test_falha_de_rede_persistente_desiste_depois_das_tentativas(self):
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=urllib.error.URLError("sem rede")) as abre, \
                mock.patch("fontes_v5.time.sleep"):
            with self.assertRaises(urllib.error.URLError):
                fontes_v5._pedir("https://exemplo/x", {})
        self.assertEqual(abre.call_count, fontes_v5.TENTATIVAS_TRANSITORIAS + 1)

    def test_doze_429_seguidos_levam_a_runtime_error(self):
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=lambda *a, **k: (_ for _ in ()).throw(self._erro(429, 1))) as abre, \
                mock.patch("fontes_v5.time.sleep"):
            with self.assertRaises(RuntimeError):
                fontes_v5._pedir("https://exemplo/x", {})
        self.assertEqual(abre.call_count, 12)

    def test_espera_acumulada_tem_orcamento(self):
        # cada espera vale ESPERA_MAX + 15 (3615 s); duas já passam de ESPERA_TOTAL (2 h), então o pedido dorme uma vez e desiste antes da 2.ª
        with mock.patch("fontes_v5.urllib.request.urlopen", side_effect=lambda *a, **k: (_ for _ in ()).throw(self._erro(429, 99999))) as abre, \
                mock.patch("fontes_v5.time.sleep") as dorme:
            with self.assertRaisesRegex(RuntimeError, "espera acumulada"):
                fontes_v5._pedir("https://exemplo/x", {})
        self.assertEqual(dorme.call_count, 1)

    def test_resposta_maior_que_o_limite_e_recusada(self):
        grande = b"x" * (fontes_v5.LIMITE_BYTES + 1)
        with mock.patch("fontes_v5.urllib.request.urlopen", return_value=self._resposta(grande)):
            with self.assertRaisesRegex(ValueError, "maior que"):
                fontes_v5._pedir("https://exemplo/x", {})


class JpegTratado(unittest.TestCase):
    """O JPEG tratado é o que entra no PDF: uma troca silenciosa precisa ser acusada."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.antes = (fontes_v5.MANIFESTO, fontes_v5.SAIDA, dict(fontes_v5.OBRAS))
        fontes_v5.MANIFESTO = os.path.join(self.tmp.name, "manifesto.json")
        fontes_v5.SAIDA = os.path.join(self.tmp.name, "v5")
        os.makedirs(fontes_v5.SAIDA)
        nome = "durer_lebre"
        fontes_v5.OBRAS.clear()
        fontes_v5.OBRAS[nome] = self.antes[2][nome]
        with open(fontes_v5.MANIFESTO, "w") as f:
            json.dump({fontes_v5.OBRAS[nome][0]: "0" * 64}, f)
        with open(os.path.join(fontes_v5.SAIDA, nome + ".jpg"), "wb") as f:
            f.write(IMAGEM)
        self.nome = nome
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        fontes_v5.MANIFESTO, fontes_v5.SAIDA = self.antes[:2]
        fontes_v5.OBRAS.clear()
        fontes_v5.OBRAS.update(self.antes[2])

    def test_sem_hash_do_jpeg_e_acusado(self):
        self.assertEqual(fontes_v5.verificar(), 1)

    def test_com_hash_certo_passa_e_jpeg_trocado_e_acusado(self):
        fontes_v5.registrar_jpegs()
        self.assertEqual(fontes_v5.verificar(), 0)
        with open(os.path.join(fontes_v5.SAIDA, self.nome + ".jpg"), "wb") as f:
            f.write(IMAGEM + b"\x00")
        self.assertEqual(fontes_v5.verificar(), 1)


class CatalogoReal(unittest.TestCase):
    """O catálogo versionado (não a pasta temporária): todo item está completo e registrado."""

    def test_toda_obra_tem_hash_e_imagem_tratada(self):
        self.assertEqual(fontes_v5.verificar(), 0)

    def test_todo_credito_diz_autor_licenca_e_arquivo(self):
        for nome, (arq, autor, obra, ano, _acervo, lic) in fontes_v5.OBRAS.items():
            c = fontes_v5.credito(nome)
            fonte = ("arquivo fornecido pela editora" if arq.startswith("envio:") else
                     fontes_v5.REFERENCIAS[nome][1] if arq.startswith(("aic:", "nga:")) else "Wikimedia Commons")
            for parte in (autor, obra, ano, lic, fonte):
                self.assertIn(parte, c, nome)

    def test_so_obras_de_autores_mortos_ha_mais_de_70_anos(self):
        import re
        import datetime
        limite = datetime.date.today().year - 70   # morreu antes de 1.º de janeiro do ano em que se completam 70 anos
        for nome, o in fontes_v5.OBRAS.items():
            morte = int(re.search(r"–(\d{4})\)", o[1]).group(1))
            self.assertLess(morte, limite, nome)

    def test_creditos_md_bate_com_o_catalogo(self):
        caminho = os.path.join(os.path.dirname(fontes_v5.MANIFESTO), "CREDITOS.md")
        with open(caminho, encoding="utf-8") as f:
            creditos = f.read()
        for linha in fontes_v5.linhas_creditos().splitlines():
            self.assertIn(linha, creditos)

    def test_caminho_no_commons_vem_do_md5_do_nome(self):
        # caminho confirmado pela API do Commons para este arquivo
        self.assertEqual(
            fontes_v5._caminho_commons("Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg"),
            "0/0e/Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg")


if __name__ == "__main__":
    unittest.main()
