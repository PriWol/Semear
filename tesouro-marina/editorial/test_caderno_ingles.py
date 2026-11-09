"""Conferência do caderno de inglês: todo motivo existe e as regras do ADR 0026 valem página a página (água, engasgo, rimas, acalmar, livros e créditos)."""
import ast
import os
import re
import unittest

import caderno
import caderno_ingles
import livro
from test_motivos7 import _motivos_citados

AQUI = os.path.dirname(os.path.abspath(__file__))
PAGINAS = 90   # o README e o ADR 0026 declaram este total
FRASE_AGUA = re.sub(r"<[^>]+>", "", caderno.AGUA).split(", ", 1)[1].split(",")[0]   # “nunca deixe a criança sozinha com água”
AGUA = re.compile(r"\b(?:água|molh\w+|lav\w+|banho|banheira|bacia|balde|chuva|poça|jarra|regador|despej\w+|encha\w*|torneira|piscina)\b", re.IGNORECASE)
EXCECOES = {   # a água só aparece de passagem: o tempo, lavar as mãos, o banho como parte do dia, letra de rima
    "What's the weather?", "Para o banho", "Mais para o banho", "Ler juntos: Where Is Baby's Belly Button?", "Mais para a mesa", "Collect a leaf",
    "Para a chuva e para o jardim", "Para a aranha e para olhar", "Feed the animals", "Soft hands", "I can do it!"}
LIVRO_E_TITULO = re.compile(r'<h1 class="titulo"[^>]*>([^<]+)')


def _texto(html):
    return re.sub(r"<[^>]+>", " ", html)


def _titulo(html):
    m = LIVRO_E_TITULO.search(html)
    return m.group(1).strip() if m else ""


class TestCadernoIngles(unittest.TestCase):
    def setUp(self):
        livro.VERSAO["atual"] = "impressao"   # o estado global é de outros testes do mesmo processo
        self.L = caderno_ingles.montar()

    def test_motivos_citados_existem(self):
        with open(os.path.join(AQUI, "caderno_ingles.py"), encoding="utf-8") as f:
            usados = _motivos_citados(ast.parse(f.read()))
        self.assertGreater(len(usados), 40)
        self.assertEqual(sorted(m for m in usados if m not in livro.TODOS), [])

    def test_total_de_paginas_e_par_e_ha_oito_unidades(self):
        self.assertEqual(len(self.L.paginas), PAGINAS)
        self.assertEqual(len(self.L.paginas) % 2, 0)
        self.assertEqual(len(self.L.inicio), len(caderno_ingles.UNIDADES_PRONTAS) + 1)   # as unidades e o encerramento
        self.assertEqual(len(caderno_ingles.UNIDADES_PRONTAS), 8)

    def test_toda_unidade_tem_quatro_rimas_duas_de_acalmar_e_um_livro(self):
        por_unidade = {}
        for _, html in self.L.paginas:
            m = re.search(r"Unidade (\d) ·", html)
            if not m:
                continue
            d = por_unidade.setdefault(m.group(1), {"acalmar": 0, "rimas": 0, "ler": 0})
            d["acalmar"] += html.count(">Acalmar</span>")
            d["ler"] += html.count(">Ler juntos</span>")
            if ">Cantar e rimar</span>" in html:
                d["rimas"] += html.count('<h2 class="titulo"')
        self.assertEqual(sorted(por_unidade), [str(i) for i in range(1, 9)])
        for u, d in por_unidade.items():
            self.assertGreaterEqual(d["acalmar"], 2, f"unidade {u}")
            self.assertGreaterEqual(d["rimas"], 4, f"unidade {u}")
            self.assertEqual(d["ler"], 1, f"unidade {u}")

    def test_toda_atividade_que_cita_agua_traz_o_aviso_de_supervisao_na_propria_pagina(self):
        sem_aviso = []
        for n, html in self.L.paginas:
            if "por que isto importa" not in html:
                continue
            texto = _texto(html)
            if AGUA.search(texto) and FRASE_AGUA not in texto and _titulo(html) not in EXCECOES:
                sem_aviso.append(f"{n} ({_titulo(html)})")
        self.assertEqual(sem_aviso, [])

    def test_as_excecoes_do_aviso_de_agua_existem_e_nao_manipulam_agua(self):
        titulos = {_titulo(h) for _, h in self.L.paginas}
        self.assertEqual(sorted(EXCECOES - titulos), [], "exceção que não corresponde a nenhuma página")
        risco = re.compile(r"\b(?:bacia|balde|banheira|mangueira|tanque|jarra|regador|despej\w+ (?:a )?água|enchendo|encha)\b", re.IGNORECASE)
        self.assertEqual([_titulo(h) for _, h in self.L.paginas if _titulo(h) in EXCECOES and risco.search(_texto(h))], [])

    def test_toda_atividade_do_banho_traz_o_aviso_de_agua(self):
        banho = [(n, h) for n, h in self.L.paginas if "Unidade 2 ·" in h and "por que isto importa" in h and ">Cantar e rimar</span>" not in h and ">Ler juntos</span>" not in h]
        self.assertGreaterEqual(len(banho), 6)
        self.assertEqual([_titulo(h) for n, h in banho if FRASE_AGUA not in _texto(h)], [])   # sem exceções: toda atividade do banho, inclusive a da toalha

    def test_toda_atividade_de_comida_traz_o_aviso_de_engasgo(self):
        comida = [(n, h) for n, h in self.L.paginas if "Unidade 3 ·" in h and "por que isto importa" in h and ">Cantar e rimar</span>" not in h and ">Ler juntos</span>" not in h]
        self.assertGreaterEqual(len(comida), 6)
        self.assertEqual([_titulo(h) for _, h in comida if "engasgo" not in _texto(h) and "temperatura" not in _texto(h)], [])

    def test_toda_rima_aparece_nos_creditos_da_sua_origem(self):
        creditos = _texto(next(h for _, h in self.L.paginas if "De onde vêm as ideias e as rimas" in h))
        # trechos dos créditos: (início, fim)
        trecho = {"desconhecida": ("Tradicionais inglesas", "Com autoria conhecida"), "conhecida": ("Com autoria conhecida", "Escritas pela coleção"),
                  "coleção": ("Escritas pela coleção", "Livros")}
        rimas = []
        for _, html in self.L.paginas:
            rimas += re.findall(r'<h2 class="titulo"[^>]*>([^<]+)</h2>.*?<div class="peq"[^>]*>([^<]+)</div>', html, re.DOTALL)
        self.assertGreaterEqual(len(rimas), 32)
        faltam = []
        for titulo, origem in rimas:
            # a seção esperada vem do que a própria página da rima declara
            chave = "coleção" if origem.startswith("Rima escrita pela coleção") else "desconhecida" if "autoria desconhecida" in origem else "conhecida"
            inicio, fim = trecho[chave]
            if titulo.strip() not in creditos.split(inicio, 1)[1].split(fim, 1)[0]:
                faltam.append(f"{titulo.strip()} (esperada em “{inicio}”)")
        self.assertEqual(faltam, [])

    def test_todo_livro_lido_esta_na_lista_de_livros(self):
        lista = _texto(next(h for _, h in self.L.paginas if "Livros para ler juntos" in h))
        lidos = [_titulo(h).replace("Ler juntos:", "").strip() for _, h in self.L.paginas if ">Ler juntos</span>" in h]
        self.assertEqual(len(lidos), 8)
        self.assertEqual([t for t in lidos if t not in lista], [])

    def test_o_caderno_nao_traz_as_cantigas_vetadas_pelo_adr_0021(self):
        vetadas = ["Atirei o pau", "Boi da cara preta", "Cuca vem", "Marcha, soldado", "A canoa virou", "Parabéns", "Ladybird, ladybird", "Humpty Dumpty"]
        texto = _texto(" ".join(h for _, h in self.L.paginas))
        self.assertEqual([v for v in vetadas if v.lower() in texto.lower()], [])

    def test_o_caderno_diz_que_o_portugues_e_a_lingua_materna_e_nao_promete_fluencia(self):
        html = self.L.html()
        self.assertIn("língua materna da Marina é o português", html)
        self.assertIn("não promete fluência", html)


if __name__ == "__main__":
    unittest.main()
