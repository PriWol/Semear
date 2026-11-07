"""Conferência do caderno de atividades: todo motivo citado existe, cada tipo tem ícone e o caderno monta sem erro."""
import ast
import os
import unittest

import caderno
import livro
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))


class TestCaderno(unittest.TestCase):
    def test_motivos_citados_existem(self):
        with open(os.path.join(AQUI, "caderno.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        usados |= {m for _, _, m in caderno.TIPOS.values()}
        self.assertGreater(len(usados), 15)
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_toda_unidade_pronta_monta_com_aviso_de_seguranca_onde_ha_agua(self):
        caderno.INICIO.clear()
        L = caderno.montar()
        html = L.html()
        self.assertIn("nunca deixe a criança sozinha com água", html)
        self.assertEqual(len(L.paginas) % 2, 0)
        self.assertEqual(len(caderno.INICIO), len(caderno.UNIDADES_PRONTAS))


if __name__ == "__main__":
    unittest.main()
