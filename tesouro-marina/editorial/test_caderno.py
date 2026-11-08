"""Conferência do caderno de atividades: todo motivo citado existe e as regras do ADR 0021 valem página a página (segurança com água, rimas e acalmar por unidade)."""
import ast
import os
import re
import unittest

import caderno
import livro
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))
FRASE_AGUA = re.sub(r"<[^>]+>", "", caderno.AGUA).split(", ", 1)[1].split(",")[0]   # “nunca deixe a criança sozinha com água”, tirada da constante do caderno
PAGINAS = 84   # o README e o ADR 0021 declaram este total
# toda página de atividade que fala de água; só as de EXCECOES (abaixo) ficam sem o aviso de supervisão
ATIVIDADE_COM_AGUA = re.compile(r"\b(?:água|molh\w+|lav\w+|banho|chuva|poça|bacia|balde|banheira|mangueira|tanque|jarra|regador|despej\w+)\b", re.IGNORECASE)
EXCECOES = {   # a água só aparece de passagem: lavar as mãos, o banho como parte do dia, a chuva como tempo, ou letra de rima
    "Passeio dos cinco sentidos", "O dia em três tempos", "Voz de bicho", "O toucinho que sumiu", "Dançar e derreter", "Pintar com o dedo",
    "Massagem nas mãos", "Caça-folhas", "Bichinho de perto", "Bichos de quintal", "Água e formigas", "Para limpar as mãos", "Mais duas, para contar e rir"}


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
            titulo = re.search(r'<h1 class="titulo"[^>]*>([^<]+)', html).group(1).strip()
            if ATIVIDADE_COM_AGUA.search(texto) and FRASE_AGUA not in texto and titulo not in EXCECOES:
                sem_aviso.append(f"{n} ({titulo})")
        self.assertEqual(sem_aviso, [], "páginas de atividade com água sem o aviso de supervisão")

    def test_as_excecoes_do_aviso_de_agua_ainda_existem(self):
        titulos = {re.search(r'<h1 class="titulo"[^>]*>([^<]+)', h).group(1).strip() for _, h in self.L.paginas if '<h1 class="titulo"' in h}
        self.assertEqual(sorted(EXCECOES - titulos), [], "exceção que não corresponde a nenhuma página")

    def test_toda_atividade_da_semana_de_exemplo_existe_no_caderno(self):
        titulos = set()
        for _, h in self.L.paginas:
            titulos |= {x.strip() for x in re.findall(r'<h[12] class="titulo"[^>]*>([^<]+)', h)}
        semana = next(h for _, h in self.L.paginas if "Uma semana de exemplo" in h)
        celulas = re.findall(r"<td[^>]*>(?:<b>[^<]*</b>|([^<]+))</td>", semana)
        atividades = [a.strip() for c in celulas if c for a in c.split(" · ")]
        self.assertGreaterEqual(len(atividades), 20)
        self.assertEqual(sorted(a for a in atividades if a not in titulos), [], "atividade da semana que não existe no caderno")

    def test_toda_unidade_tem_rimas_e_ao_menos_duas_atividades_de_acalmar(self):
        por_unidade = {}
        for _, html in self.L.paginas:
            m = re.search(r"Unidade (\d) ·", html)
            if not m:
                continue
            d = por_unidade.setdefault(m.group(1), {"acalmar": 0, "rimas": 0})
            d["acalmar"] += html.count(">Acalmar</span>")
            if ">Cantar e rimar</span>" in html:   # `rimas()` traz um título h2 por rima
                d["rimas"] += html.count('<h2 class="titulo"')
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
