"""Testes das pranchas de naturalistas do Volume 6 (ADR 0011, 0018 e 0019). Rodar: python3 -m unittest test_fontes_v6"""
import json
import os
import tempfile
import unittest

from PIL import Image

import fontes_v5
import fontes_v6


class Isolado(unittest.TestCase):
    """Troca saída, manifesto e catálogo por uma pasta temporária e restaura tudo no fim."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.antes = (fontes_v6.SAIDA, fontes_v5.MANIFESTO, dict(fontes_v6.OBRAS))
        fontes_v6.SAIDA = os.path.join(self.tmp.name, "v6")
        fontes_v5.MANIFESTO = os.path.join(self.tmp.name, "m.json")
        os.makedirs(fontes_v6.SAIDA)
        fontes_v6.OBRAS.clear()
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        fontes_v6.SAIDA, fontes_v5.MANIFESTO = self.antes[:2]
        fontes_v6.OBRAS.clear()
        fontes_v6.OBRAS.update(self.antes[2])
        self.tmp.cleanup()

    def _obra(self, nome="x", arq="X.jpg", acervo="Acervo Y"):
        fontes_v6.OBRAS[nome] = (arq, "Autor (1800–1850)", "<i>X</i>", "1840", acervo, "domínio público")
        Image.new("RGB", (4, 4), (10, 20, 30)).save(os.path.join(fontes_v6.SAIDA, f"{nome}.jpg"))
        fontes_v6.registrar_jpegs([nome])
        man = fontes_v5._manifesto()
        man[arq] = "0" * 64
        with open(fontes_v5.MANIFESTO, "w") as f:
            json.dump(man, f)


class FalhaFechada(Isolado):
    def test_obra_completa_passa(self):
        self._obra()
        self.assertEqual(fontes_v6.verificar(), 0)

    def test_obra_sem_acervo_e_recusada(self):
        self._obra(acervo="")
        self.assertEqual(fontes_v6.verificar(), 1)

    def test_obra_que_nao_vem_do_commons_e_recusada(self):
        self._obra(arq="envio:x")
        self.assertEqual(fontes_v6.verificar(), 1)

    def test_origem_sem_hash_e_recusada(self):
        self._obra()
        with open(fontes_v5.MANIFESTO) as f:
            man = json.load(f)
        del man["X.jpg"]
        with open(fontes_v5.MANIFESTO, "w") as f:
            json.dump(man, f)
        self.assertEqual(fontes_v6.verificar(), 1)

    def test_jpeg_trocado_depois_do_registro_e_recusado(self):
        self._obra()
        Image.new("RGB", (4, 4), (200, 0, 0)).save(os.path.join(fontes_v6.SAIDA, "x.jpg"))
        self.assertEqual(fontes_v6.verificar(), 1)

    def test_jpeg_que_falta_e_recusado(self):
        self._obra()
        os.remove(os.path.join(fontes_v6.SAIDA, "x.jpg"))
        self.assertEqual(fontes_v6.verificar(), 1)


class CreditoEscapado(Isolado):
    def test_nome_de_arquivo_com_e_comercial_e_escapado(self):
        self._obra(arq="Dürer & Cia <1>.jpg")
        c = fontes_v6.credito("x")
        self.assertIn("Dürer &amp; Cia &lt;1&gt;.jpg", c)
        self.assertIn("<i>X</i>", c)


class Recortes(unittest.TestCase):
    def test_todo_recorte_e_de_uma_prancha_do_catalogo_e_tem_caixa_valida(self):
        for nome, (x0, y0, x1, y1) in fontes_v6.RECORTES.items():
            self.assertIn(nome, fontes_v6.OBRAS)
            self.assertLess(x0, x1)
            self.assertLess(y0, y1)
            self.assertGreaterEqual(min(x0, y0), 0)

    def test_credito_de_prancha_recortada_avisa_que_e_recorte(self):
        for nome in fontes_v6.RECORTES:
            self.assertIn("Recorte do original", fontes_v6.credito(nome))

    def _com_prancha_falsa(self, caixa, lado=100):
        """Executa processar("x") numa pasta temporária, com uma prancha de lado×lado e o recorte `caixa`."""
        with tempfile.TemporaryDirectory() as tmp:
            antes = (fontes_v6.SAIDA, fontes_v5.MANIFESTO, dict(fontes_v6.OBRAS), dict(fontes_v6.RECORTES), fontes_v5.FONTE, fontes_v6.FONTE)
            try:
                fontes_v6.SAIDA = os.path.join(tmp, "v6")
                fontes_v5.MANIFESTO = os.path.join(tmp, "m.json")
                fontes_v5.FONTE = fontes_v6.FONTE = os.path.join(tmp, "orig")
                os.makedirs(fontes_v6.FONTE)
                fontes_v6.OBRAS.clear()
                fontes_v6.OBRAS["x"] = ("X.jpg", "Autor (1800–1850)", "<i>X</i>", "1840", "Acervo", "domínio público")
                fontes_v6.RECORTES.clear()
                fontes_v6.RECORTES["x"] = caixa
                Image.new("RGB", (lado, lado), (30, 60, 90)).save(os.path.join(fontes_v6.FONTE, "x.orig"), "JPEG")
                with open(os.path.join(fontes_v6.FONTE, "x.orig"), "rb") as f:
                    sha = fontes_v5._sha256(f.read())
                with open(fontes_v5.MANIFESTO, "w") as f:
                    json.dump({"X.jpg": sha}, f)
                return fontes_v6.processar("x")
            finally:
                fontes_v6.SAIDA, fontes_v5.MANIFESTO = antes[:2]
                fontes_v6.OBRAS.clear(); fontes_v6.OBRAS.update(antes[2])
                fontes_v6.RECORTES.clear(); fontes_v6.RECORTES.update(antes[3])
                fontes_v5.FONTE, fontes_v6.FONTE = antes[4], antes[5]

    def test_processar_recorta_a_prancha_e_registra_o_jpeg(self):
        self.assertEqual(self._com_prancha_falsa((10, 20, 60, 70)), (50, 50))

    def test_processar_recusa_recorte_fora_da_imagem(self):
        for caixa in ((10, 20, 160, 70), (-5, 20, 60, 70), (60, 20, 10, 70), (10, 20, 60, 20)):
            with self.subTest(caixa=caixa), self.assertRaisesRegex(ValueError, "fora da imagem"):
                self._com_prancha_falsa(caixa)


class CatalogoReal(unittest.TestCase):
    """O catálogo versionado (não a pasta temporária): todo item está completo e registrado."""

    def test_toda_prancha_tem_hash_e_imagem_tratada(self):
        self.assertEqual(fontes_v6.verificar(), 0)

    def test_todo_credito_diz_autoria_licenca_e_arquivo(self):
        for nome, (arq, autor, obra, ano, acervo, lic) in fontes_v6.OBRAS.items():
            c = fontes_v6.credito(nome)
            for parte in (autor, obra, ano, acervo, lic, "Wikimedia Commons"):
                self.assertIn(parte, c, nome)

    def test_creditos_md_bate_com_o_catalogo(self):
        caminho = os.path.join(os.path.dirname(fontes_v5.MANIFESTO), "CREDITOS.md")
        with open(caminho, encoding="utf-8") as f:
            creditos = f.read()
        for linha in fontes_v6.linhas_creditos().splitlines():
            self.assertIn(linha, creditos)


if __name__ == "__main__":
    unittest.main()
