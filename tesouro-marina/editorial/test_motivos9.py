"""Conferência dos motivos do Volume 8: nenhum nome de motivos9.py sobrescreve um motivo de volume anterior e todo motivo citado em volume8.py existe.
Estes testes falham até volume8.py e motivos9.py existirem (estória #112, PR A). Rodar: python3 -m unittest test_motivos9"""
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
from motivos9 import MOTIVOS9
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))


def _citados_no_volume8():
    with open(os.path.join(AQUI, "volume8.py"), encoding="utf-8") as f:
        return _motivos_citados(ast.parse(f.read()))


class TestMotivos9(unittest.TestCase):
    def test_nenhum_nome_colide_com_motivos_anteriores(self):
        # livro.TODOS funde as tabelas na ordem; uma colisão trocaria em silêncio a ilustração de um volume antigo
        anteriores = set().union(SUBJECTS, MOTIVOS2, ARTE_EXTRA, MOTIVOS3, MOTIVOS4, MOTIVOS5, MOTIVOS6, MOTIVOS7, MOTIVOS8)
        self.assertEqual(sorted(anteriores & set(MOTIVOS9)), [])

    def test_ha_motivos_novos_e_todos_estao_em_livro_todos(self):
        self.assertGreater(len(MOTIVOS9), 0)
        self.assertEqual(sorted(m for m in MOTIVOS9 if m not in livro.TODOS), [], "livro.py precisa importar MOTIVOS9 e incluí-lo em TODOS")

    def test_cada_motivo_tem_funcao_de_desenho(self):
        for nome, desenho in MOTIVOS9.items():
            self.assertTrue(nome and nome == nome.strip().lower() and " " not in nome, f"nome de motivo inválido: {nome!r}")
            self.assertTrue(callable(desenho) or isinstance(desenho, (str, dict, tuple, list)), nome)

    def test_motivos_do_volume_8_existem(self):
        usados = _citados_no_volume8()
        self.assertGreater(len(usados), 10)   # a varredura precisa achar de fato os motivos de cartões, cenas e tiras
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_todo_motivo_novo_e_usado_no_volume(self):
        # motivo pintado e esquecido pesa no repositório e no ADR sem aparecer em página nenhuma
        self.assertEqual(sorted(set(MOTIVOS9) - _citados_no_volume8()), [])

    def test_motivos_novos_sao_poucos(self):
        # o plano pede o número mínimo: a aquarela é a parte lenta do CI; só entra o que ainda não existe
        self.assertLessEqual(len(MOTIVOS9), 14)


if __name__ == "__main__":
    unittest.main()
