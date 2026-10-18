"""Conferência dos motivos do Volume 6: nenhum nome de motivos7.py sobrescreve um motivo de volume anterior e todo motivo citado em volume6.py existe."""
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

AQUI = os.path.dirname(os.path.abspath(__file__))


def _motivos_citados(arvore):
    """Nomes de motivo em img("x"), tira(["x", ...]), cena([("x", ...), ...]) e dict(mot="x")."""
    nomes = set()

    def texto(n):
        return n.value if isinstance(n, ast.Constant) and isinstance(n.value, str) else None

    for no in ast.walk(arvore):
        if not isinstance(no, ast.Call):
            continue
        f = no.func.id if isinstance(no.func, ast.Name) else None
        if f == "img" and no.args and texto(no.args[0]):
            nomes.add(texto(no.args[0]))
        elif f == "tira" and no.args and isinstance(no.args[0], ast.List):
            nomes |= {texto(e) for e in no.args[0].elts if texto(e)}
        elif f == "cena" and no.args and isinstance(no.args[0], ast.List):
            for e in no.args[0].elts:
                if isinstance(e, ast.Tuple) and e.elts and texto(e.elts[0]):
                    nomes.add(texto(e.elts[0]))
        for kw in no.keywords:
            if kw.arg == "mot" and texto(kw.value):
                nomes.add(texto(kw.value))
    return nomes


class TestMotivos7(unittest.TestCase):
    def test_nenhum_nome_colide_com_motivos_anteriores(self):
        # livro.TODOS funde as tabelas na ordem; uma colisão trocaria em silêncio a ilustração de um volume antigo
        anteriores = set().union(SUBJECTS, MOTIVOS2, ARTE_EXTRA, MOTIVOS3, MOTIVOS4, MOTIVOS5, MOTIVOS6)
        self.assertEqual(sorted(anteriores & set(MOTIVOS7)), [])

    def test_motivos_do_volume_6_existem(self):
        with open(os.path.join(AQUI, "volume6.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        self.assertGreater(len(usados), 60)  # a varredura precisa achar de fato os motivos (não só o primeiro de cada chamada)
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_a_varredura_pega_todos_os_itens_de_uma_cena(self):
        achados = _motivos_citados(ast.parse('cena([("a", 1, 2, 3), ("b", 1, 2, 3)]); tira(["c", "d"]); img("e")'))
        self.assertEqual(achados, {"a", "b", "c", "d", "e"})


if __name__ == "__main__":
    unittest.main()
