"""Testa a checagem de área segura do pdf.js (ADR 0011). Rodar: python3 -m unittest test_pdf

Pula se o node ou o playwright não estiverem instalados, exceto no CI (variável CI definida), onde a
ausência seria uma falha de instalação e não pode passar em silêncio.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
PAGINA = ('<!doctype html><meta charset="utf-8"><style>@page{size:210mm 297mm;margin:0}'
          '.pagina{position:relative;width:210mm;height:297mm}</style><div class="pagina">{}</div>')


def _node_com_playwright():
    if not shutil.which("node"):
        return False
    r = subprocess.run(["node", "-e", "require('playwright')"], cwd=AQUI, capture_output=True)
    return r.returncode == 0


@unittest.skipUnless(os.environ.get("CI") or _node_com_playwright(), "node/playwright indisponíveis")
class AreaSegura(unittest.TestCase):
    def _rodar(self, corpo):
        with tempfile.TemporaryDirectory() as tmp:
            html, pdf = os.path.join(tmp, "p.html"), os.path.join(tmp, "p.pdf")
            with open(html, "w", encoding="utf-8") as f:
                f.write(PAGINA.replace("{}", corpo))
            r = subprocess.run(["node", os.path.join(AQUI, "pdf.js"), html, pdf], cwd=AQUI,
                               capture_output=True, text=True)
            return r.returncode, os.path.exists(pdf)

    def test_pagina_limpa_gera_o_pdf(self):
        self.assertEqual(self._rodar('<p style="position:absolute;left:20mm;top:20mm">dentro da margem</p>'), (0, True))

    def test_texto_perto_da_borda_recusa(self):
        self.assertEqual(self._rodar('<p style="position:absolute;left:2mm;top:50mm">na borda</p>'), (2, False))

    def test_imagem_perto_da_borda_recusa(self):
        self.assertEqual(self._rodar('<svg style="position:absolute;left:2mm;top:50mm" width="40" height="40"></svg>'),
                         (2, False))

    def test_camada_de_pagina_inteira_passa(self):
        for tag in ("svg", "img"):
            corpo = f'<{tag} style="position:absolute;left:0;top:0;width:210mm;height:297mm"></{tag}>'
            self.assertEqual(self._rodar(corpo), (0, True), tag)

    def test_camada_deslocada_nao_e_isenta(self):
        corpo = '<svg style="position:absolute;left:3mm;top:3mm;width:201mm;height:285mm"></svg>'
        self.assertEqual(self._rodar(corpo), (2, False))

    def test_img_perto_da_borda_recusa(self):
        corpo = '<img style="position:absolute;left:2mm;top:50mm;width:40px;height:40px">'
        self.assertEqual(self._rodar(corpo), (2, False))


if __name__ == "__main__":
    unittest.main()
