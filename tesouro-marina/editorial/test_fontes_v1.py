"""Testes da regra "falha fechada" do download de páginas (ADR 0011). Rodar: python3 -m unittest test_fontes_v1

Nenhum teste usa a rede: as páginas já estão em cache numa pasta temporária.
"""
import json
import os
import tempfile
import unittest

import fontes_v1

PAGINA = b"conteudo-de-uma-pagina"
SHA = fontes_v1._sha256(PAGINA)
CHAVE = "livro_n7"


class FalhaFechada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.antes = (fontes_v1.MANIFESTO, fontes_v1.FONTE, fontes_v1.REGISTRAR, dict(fontes_v1.ITENS))
        fontes_v1.MANIFESTO = os.path.join(self.tmp.name, "manifesto.json")
        fontes_v1.FONTE = os.path.join(self.tmp.name, "paginas")
        fontes_v1.REGISTRAR = False
        os.makedirs(fontes_v1.FONTE)
        open(os.path.join(fontes_v1.FONTE, CHAVE + ".jpg"), "wb").write(PAGINA)
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        fontes_v1.MANIFESTO, fontes_v1.FONTE, fontes_v1.REGISTRAR = self.antes[:3]
        fontes_v1.ITENS.clear()
        fontes_v1.ITENS.update(self.antes[3])

    def _manifesto(self, dados):
        json.dump(dados, open(fontes_v1.MANIFESTO, "w"))

    def test_pagina_com_hash_certo_passa(self):
        self._manifesto({CHAVE: SHA})
        self.assertTrue(fontes_v1.baixar("livro", 7).endswith(CHAVE + ".jpg"))

    def test_hash_diferente_e_recusado(self):
        self._manifesto({CHAVE: "0" * 64})
        with self.assertRaises(ValueError):
            fontes_v1.baixar("livro", 7)

    def test_pagina_sem_hash_e_recusada(self):
        self._manifesto({})
        with self.assertRaises(ValueError):
            fontes_v1.baixar("livro", 7)

    def test_sem_manifesto_nenhuma_pagina_passa(self):
        with self.assertRaises(ValueError):
            fontes_v1.baixar("livro", 7)

    def test_registrar_grava_o_hash_novo(self):
        self._manifesto({})
        fontes_v1.REGISTRAR = True
        fontes_v1.baixar("livro", 7)
        self.assertEqual(json.load(open(fontes_v1.MANIFESTO)), {CHAVE: SHA})

    def test_verificar_aponta_item_sem_hash(self):
        fontes_v1.ITENS.clear()
        fontes_v1.ITENS["x"] = ("livro", 7, None, 100)
        self._manifesto({})
        self.assertEqual(fontes_v1.verificar(), 1)
        self._manifesto({CHAVE: SHA})
        self.assertEqual(fontes_v1.verificar(), 0)


class ManifestoReal(unittest.TestCase):
    def test_todo_item_usado_tem_hash(self):
        self.assertEqual(fontes_v1.verificar(), 0)


if __name__ == "__main__":
    unittest.main()
