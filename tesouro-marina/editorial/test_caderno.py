"""Conferência do caderno de atividades: todo motivo citado existe e as regras do ADR 0021 valem página a página (segurança com água, rimas e acalmar por unidade)."""
import ast
import os
import re
import unittest

import caderno
import livro
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))
PAGINAS = 84   # o README e o ADR 0021 declaram este total
ATIVIDADE_COM_AGUA = re.compile(r"bacia|balde|despej\w+ (?:a )?água|enchendo|banheira|mangueira|tanque|regador|poça|jarra")


def _texto(html):
    return re.sub(r"<[^>]+>", " ", html)


class TestCaderno(unittest.TestCase):
    def setUp(self):
        livro.VERSAO["atual"] = "impressao"   # o estado global é de outros testes do mesmo processo
        self.L = caderno.montar()

    def test_motivos_citados_existem(self):
        with open(os.path.join(AQUI, "caderno.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        usados |= {m for _, _, m in caderno.TIPOS.values()}
        self.assertGreater(len(usados), 15)
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_total_de_paginas_e_par(self):
        self.assertEqual(len(self.L.paginas), PAGINAS)
        self.assertEqual(len(self.L.paginas) % 2, 0)

    def test_toda_atividade_que_cita_agua_traz_o_aviso_de_supervisao_na_propria_pagina(self):
        sem_aviso = []
        for n, html in self.L.paginas:
            if "por que isto importa" not in html:   # só as páginas de atividade
                continue
            texto = _texto(html)
            if ATIVIDADE_COM_AGUA.search(texto) and "sozinha com água" not in texto:
                sem_aviso.append(n)
        self.assertEqual(sem_aviso, [], "páginas de atividade com água sem o aviso de supervisão")

    def test_toda_unidade_tem_rimas_e_ao_menos_duas_atividades_de_acalmar(self):
        por_unidade = {}
        for _, html in self.L.paginas:
            m = re.search(r"Unidade (\d) ·", html)
            if not m:
                continue
            d = por_unidade.setdefault(m.group(1), {"acalmar": 0, "rimas": 0})
            d["acalmar"] += html.count(">Acalmar</span>")
            if ">Cantar e rimar</span>" in html:   # `rimas()` traz um título h2 por rima; `rima()` traz uma só
                d["rimas"] += html.count('<h2 class="titulo"') or 1
        self.assertEqual(sorted(por_unidade), [str(i) for i in range(1, 9)])
        for u, d in por_unidade.items():
            self.assertGreaterEqual(d["acalmar"], 2, f"unidade {u}")
            self.assertGreaterEqual(d["rimas"], 4, f"unidade {u}: o ADR 0021 promete 4 ou mais rimas por unidade")

    def test_cada_montagem_tem_o_seu_sumario(self):
        outra = caderno.montar()
        self.assertEqual(self.L.inicio, outra.inicio)
        self.assertEqual(len(self.L.inicio), len(caderno.UNIDADES_PRONTAS) + 1)   # as unidades e o encerramento


if __name__ == "__main__":
    unittest.main()
