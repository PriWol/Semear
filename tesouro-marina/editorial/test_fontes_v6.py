"""Testes das pranchas de naturalistas do Volume 6 (ADR 0011, 0017 e 0018). Rodar: python3 -m unittest test_fontes_v6"""
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
