"""Conferência do caderno de inglês: todo motivo existe, cada unidade traz acalmar, rimas e um livro, e os livros são só indicados."""
import ast
import os
import re
import unittest

import caderno_ingles
import livro
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))


class TestCadernoIngles(unittest.TestCase):
    def test_motivos_citados_existem(self):
        with open(os.path.join(AQUI, "caderno_ingles.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        self.assertGreater(len(usados), 15)
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_toda_unidade_pronta_tem_acalmar_rimas_e_um_livro(self):
        caderno_ingles.INICIO.clear()
        L = caderno_ingles.montar()
        por_unidade = {}
        for _, html in L.paginas:
            m = re.search(r"Unidade (\d) ·", html)
            if not m:
                continue
            d = por_unidade.setdefault(m.group(1), {"acalmar": 0, "cantar": 0, "ler": 0})
            d["acalmar"] += html.count(">Acalmar</span>")
            d["cantar"] += html.count(">Cantar e rimar</span>")
            d["ler"] += html.count(">Ler juntos</span>")
        self.assertEqual(len(por_unidade), len(caderno_ingles.UNIDADES_PRONTAS))
        for u, d in por_unidade.items():
            self.assertGreaterEqual(d["acalmar"], 2, f"unidade {u}")
            self.assertGreaterEqual(d["cantar"], 2, f"unidade {u}")
            self.assertEqual(d["ler"], 1, f"unidade {u}")

    def test_o_caderno_diz_que_o_portugues_e_a_lingua_materna_e_nao_promete_fluencia(self):
        caderno_ingles.INICIO.clear()
        html = caderno_ingles.montar().html()
        self.assertIn("língua materna da Marina é o português", html)
        self.assertIn("não promete fluência", html)


if __name__ == "__main__":
    unittest.main()
