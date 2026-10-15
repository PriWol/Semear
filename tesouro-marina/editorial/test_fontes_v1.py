"""Testes da regra "falha fechada" do download de páginas (ADR 0011). Rodar: python3 -m unittest test_fontes_v1

Nenhum teste usa a rede: as páginas já estão em cache numa pasta temporária.
"""
import io
import json
import os
import tempfile
import unittest
from unittest import mock

from PIL import Image

import fontes_v1

def _jpeg():
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), (200, 180, 150)).save(buf, "JPEG")
    return buf.getvalue()


PAGINA = _jpeg()
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
        self.cache = os.path.join(fontes_v1.FONTE, CHAVE + ".jpg")
        with open(self.cache, "wb") as f:
            f.write(PAGINA)
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        fontes_v1.MANIFESTO, fontes_v1.FONTE, fontes_v1.REGISTRAR = self.antes[:3]
        fontes_v1.ITENS.clear()
        fontes_v1.ITENS.update(self.antes[3])

    def _manifesto(self, dados):
        with open(fontes_v1.MANIFESTO, "w") as f:
            json.dump(dados, f)

    def test_pagina_com_hash_certo_passa(self):
        self._manifesto({CHAVE: SHA})
        self.assertTrue(fontes_v1.baixar("livro", 7).endswith(CHAVE + ".jpg"))

    def test_hash_diferente_e_recusado(self):
        self._manifesto({CHAVE: "0" * 64})
        with mock.patch.object(fontes_v1, "_da_rede", return_value=PAGINA), self.assertRaises(ValueError):
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
        with mock.patch.object(fontes_v1, "_da_rede", return_value=PAGINA) as rede:
            fontes_v1.baixar("livro", 7)
        rede.assert_called_once()   # registrar ignora o cache
        with open(fontes_v1.MANIFESTO) as f:
            self.assertEqual(json.load(f), {CHAVE: SHA})

    def test_registrar_nao_rebaixa_pagina_ja_registrada(self):
        self._manifesto({CHAVE: SHA})
        fontes_v1.REGISTRAR = True
        with mock.patch.object(fontes_v1, "_da_rede") as rede:
            fontes_v1.baixar("livro", 7)
        rede.assert_not_called()

    def test_cache_corrompido_baixa_de_novo(self):
        self._manifesto({CHAVE: SHA})
        with open(self.cache, "wb") as f:
            f.write(b"lixo")
        with mock.patch.object(fontes_v1, "_da_rede", return_value=PAGINA) as rede:
            fontes_v1.baixar("livro", 7)
        rede.assert_called_once()
        with open(self.cache, "rb") as f:
            self.assertEqual(f.read(), PAGINA)

    def test_hash_e_conferido_antes_de_decodificar(self):
        self._manifesto({CHAVE: "0" * 64})
        with mock.patch.object(fontes_v1, "_da_rede", return_value=PAGINA), \
                mock.patch.object(fontes_v1.Image, "open") as abrir, self.assertRaises(ValueError):
            fontes_v1.baixar("livro", 7)
        abrir.assert_not_called()

    def test_resposta_maior_que_o_limite_e_recusada(self):
        resposta = mock.MagicMock()
        resposta.__enter__.return_value.read.return_value = b"x" * (fontes_v1.LIMITE_BYTES + 1)
        with mock.patch("urllib.request.urlopen", return_value=resposta), self.assertRaises(ValueError):
            fontes_v1._da_rede("livro", 7)

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
