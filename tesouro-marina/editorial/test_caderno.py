"""Conferência do caderno de atividades: todo motivo citado existe, cada tipo tem ícone e o caderno monta sem erro."""
import ast
import os
import re
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
        self.assertEqual(len(caderno.INICIO), len(caderno.UNIDADES_PRONTAS) + 1)   # as unidades e o encerramento

    def test_toda_unidade_tem_rimas_e_ao_menos_duas_atividades_de_acalmar(self):
        caderno.INICIO.clear()
        L = caderno.montar()
        por_unidade = {}
        for _, html in L.paginas:
            m = re.search(r"Unidade (\d) ·", html)
            if not m:
                continue
            d = por_unidade.setdefault(m.group(1), {"acalmar": 0, "cantar": 0})
            d["acalmar"] += html.count(">Acalmar</span>")
            d["cantar"] += html.count(">Cantar e rimar</span>")
        self.assertEqual(sorted(por_unidade), [str(i) for i in range(1, 9)])
        for u, d in por_unidade.items():
            self.assertGreaterEqual(d["acalmar"], 2, f"unidade {u}")
            self.assertGreaterEqual(d["cantar"], 1, f"unidade {u}")


if __name__ == "__main__":
    unittest.main()
