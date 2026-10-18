"""Conferência dos motivos do Volume 7: nenhum nome de motivos8.py sobrescreve um motivo de volume anterior e todo motivo citado em volume7.py existe."""
import ast
import os
import unittest

import livro
from arte_extra import ARTE_EXTRA
from motivos import SUBJECTS
from motivos2 import MOTIVOS2
from motivos3 import MOTIVOS3
from motivos4 import MOTIVOS4
from motivos5 import MOTIVOS5
from motivos6 import MOTIVOS6
from motivos7 import MOTIVOS7
from motivos8 import MOTIVOS8
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))


class TestMotivos8(unittest.TestCase):
    def test_nenhum_nome_colide_com_motivos_anteriores(self):
        # livro.TODOS funde as tabelas na ordem; uma colisão trocaria em silêncio a ilustração de um volume antigo
        anteriores = set().union(SUBJECTS, MOTIVOS2, ARTE_EXTRA, MOTIVOS3, MOTIVOS4, MOTIVOS5, MOTIVOS6, MOTIVOS7)
        self.assertEqual(sorted(anteriores & set(MOTIVOS8)), [])

    def test_motivos_do_volume_7_existem(self):
        with open(os.path.join(AQUI, "volume7.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        self.assertGreater(len(usados), 10)  # a varredura precisa achar de fato os motivos (não só o primeiro de cada chamada): só os cartões da unidade 1 já passam de 9
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_todo_motivo_novo_e_usado_no_volume(self):
        # motivo pintado e esquecido pesa no repositório e no ADR sem aparecer em página nenhuma
        with open(os.path.join(AQUI, "volume7.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        self.assertEqual(sorted(set(MOTIVOS8) - usados), [])


if __name__ == "__main__":
    unittest.main()
