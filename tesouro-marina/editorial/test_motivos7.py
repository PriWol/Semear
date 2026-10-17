"""Conferência do registro de motivos do Volume 6: todo motivo usado por volume6.py existe e nenhum nome colide com os anteriores."""
import re
import unittest

import livro
import motivos7


class TestMotivos7(unittest.TestCase):
    def test_nenhum_nome_colide_com_motivos_anteriores(self):
        anteriores = set(livro.TODOS) - set(motivos7.MOTIVOS7)
        self.assertFalse(anteriores & set(motivos7.MOTIVOS7))

    def test_motivos_do_volume_6_existem(self):
        with open("volume6.py", encoding="utf-8") as f:
            src = f.read()
        usados = set(re.findall(r'(?:img|tira|cena)\(\[?\(?"([a-z_0-9]+)"', src))
        usados |= set(re.findall(r'mot="([a-z_0-9]+)"', src))
        faltam = sorted(m for m in usados if m not in livro.TODOS and not m.startswith(("dominio", "prancha")))
        self.assertEqual(faltam, [])


if __name__ == "__main__":
    unittest.main()
