"""Testes das reproduções de obras do Volume 5 (ADR 0011). Rodar: python3 -m unittest test_fontes_v5

Nenhum teste usa a rede: o arquivo de origem já está em cache numa pasta temporária.
"""
import io
import json
import os
import tempfile
import unittest

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


class CatalogoReal(unittest.TestCase):
    """O catálogo versionado (não a pasta temporária): todo item está completo e registrado."""

    def test_toda_obra_tem_hash_e_imagem_tratada(self):
        self.assertEqual(fontes_v5.verificar(), 0)

    def test_todo_credito_diz_autor_licenca_e_arquivo(self):
        for nome, (arq, autor, obra, ano, _acervo, lic) in fontes_v5.OBRAS.items():
            c = fontes_v5.credito(nome)
            fonte = "Wikimedia Commons" if not arq.startswith(("aic:", "nga:")) else fontes_v5.REFERENCIAS[nome][1]
            for parte in (autor, obra, ano, lic, fonte):
                self.assertIn(parte, c, nome)

    def test_so_obras_de_autores_mortos_ha_mais_de_70_anos(self):
        import re
        for nome, o in fontes_v5.OBRAS.items():
            morte = int(re.search(r"–(\d{4})\)", o[1]).group(1))
            self.assertLess(morte, 2026 - 70, nome)

    def test_caminho_no_commons_vem_do_md5_do_nome(self):
        # caminho confirmado pela API do Commons para este arquivo
        self.assertEqual(
            fontes_v5._caminho_commons("Vassily Kandinsky, 1926 - Several Circles, Gugg 0910 25.jpg"),
            "0/0e/Vassily_Kandinsky%2C_1926_-_Several_Circles%2C_Gugg_0910_25.jpg")


if __name__ == "__main__":
    unittest.main()
