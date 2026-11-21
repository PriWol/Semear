"""O metadado Title de cada PDF não pode ficar vazio nem divergir do catálogo da Biblioteca (#113).
Rodar: python3 -m unittest test_pdf_titulos
"""
import json
import os
import re
import unittest

import caderno
import caderno_ingles
import livro

AQUI = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(AQUI, "..", "..", "app", "content", "tesouro.json")
TITLE = re.compile(r"<title>([^<]*)</title>")


def _title(html):
    return TITLE.search(html).group(1).strip()


class TitulosDosPdfs(unittest.TestCase):
    def setUp(self):
        livro.VERSAO["atual"] = "tela"
        with open(CATALOGO, encoding="utf-8") as f:
            self.cat = json.load(f)

    def test_cadernos_tem_o_nome_do_catalogo(self):
        montadores = {"atividades-2-anos": caderno.Caderno, "ingles-2-anos": caderno_ingles.CadernoIngles}
        achados = {c["id"]: c for c in self.cat["cadernos"]}
        self.assertEqual(set(montadores), set(achados))
        for id_, classe in montadores.items():
            c = achados[id_]
            self.assertEqual(_title(classe().html()), f'{c["titulo"]} · {c["subtitulo"]}', id_)

    def test_volumes_tem_titulo_com_o_numero(self):
        for v in self.cat["volumes"]:
            t = _title(livro.Livro(v["numero"], v["titulo"]).html())
            self.assertRegex(t, rf"Volume {v['numero']}$")

    def test_nenhum_titulo_vazio(self):
        self.assertTrue(_title(caderno.Caderno().html()))
        self.assertTrue(_title(caderno_ingles.CadernoIngles().html()))


if __name__ == "__main__":
    unittest.main()
