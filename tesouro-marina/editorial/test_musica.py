"""Testes da notação musical (musica.py). Rodar: python3 -m unittest test_musica

Conferem as regras que, se erradas, escreveriam a nota no lugar errado da pauta: posição na pauta, haste, colcheias ligadas.
"""
import re
import unittest

import musica


class Posicao(unittest.TestCase):
    def test_linhas_e_espacos_da_clave_de_sol(self):
        # E4 é a linha de baixo (0); cada passo é meio espaço
        self.assertEqual(musica.posicao("E4"), 0)
        self.assertEqual(musica.posicao("G4"), 2)    # segunda linha: a nota que a clave de sol envolve
        self.assertEqual(musica.posicao("B4"), 4)    # linha do meio
        self.assertEqual(musica.posicao("F5"), 8)    # linha de cima
        self.assertEqual(musica.posicao("C4"), -2)   # dó central, na linha suplementar

    def test_oitava_acima_soma_sete_passos(self):
        for n in "CDEFGAB":
            self.assertEqual(musica.posicao(n + "5") - musica.posicao(n + "4"), 7)


class Pauta(unittest.TestCase):
    def _notas(self, svg):
        return re.findall(r"<ellipse [^>]*rx=", svg)

    def test_uma_cabeca_por_nota_e_nenhuma_por_pausa(self):
        svg = musica.pauta([("C4", "q"), ("R", "q"), ("E4", "h"), "|", ("G4", "w")])
        self.assertEqual(len(self._notas(svg)), 3)

    def test_nota_aguda_leva_haste_para_baixo_e_grave_para_cima(self):
        grave = musica.pauta([("C4", "q")])
        agudo = musica.pauta([("C5", "q")])
        self.assertIn("x2=", grave)
        y = lambda s: [float(v) for v in re.findall(r'<line x1="[\d.]+" y1="([\d.]+)" x2="[\d.]+" y2="([\d.]+)" stroke="#3d3127"', s)[0]]
        y1, y2 = y(grave)
        self.assertLess(y2, y1)       # haste sobe
        y1, y2 = y(agudo)
        self.assertGreater(y2, y1)    # haste desce

    def test_colcheias_vizinhas_ganham_uma_trave(self):
        svg = musica.pauta([("C4", "e"), ("D4", "e"), ("E4", "q")])
        self.assertEqual(len(re.findall(r'stroke-width="1\.0\d*"', svg)), 1)   # a trave (0,45 × esp 2,3)

    def test_pauta_vazia_nao_quebra(self):
        self.assertIn("<svg", musica.pauta([]))

    def test_letra_ou_rotulos_de_tamanho_errado_sao_recusados(self):
        notas = [("C4", "q"), ("R", "q"), ("D4", "q")]
        musica.pauta(notas, letra=["a", "b"])             # pausa não leva sílaba: 2 notas, 2 sílabas
        with self.assertRaises(ValueError):
            musica.pauta(notas, letra=["a"])
        with self.assertRaises(ValueError):
            musica.pauta(notas, rotulos=["dó", "ré", "mi"])

    def test_pausa_so_aceita_duracoes_desenhadas(self):
        musica.pauta([("R", "q"), ("R", "h")])
        for dur in ("e", "w"):
            with self.assertRaises(ValueError):
                musica.pauta([("R", dur)])

    def test_letra_e_rotulos_aparecem_sob_as_notas(self):
        svg = musica.pauta([("C4", "q"), ("D4", "q")], letra=["bri", "lha"], rotulos=["dó", "ré"])
        for t in ("bri", "lha", "dó", "ré"):
            self.assertIn(f">{t}<", svg)


class Ritmo(unittest.TestCase):
    def test_tira_de_ritmo_tem_um_grupo_por_figura(self):
        svg = musica.tira_ritmo(["ta", "ti", "sh"])
        self.assertEqual(svg.count("<g transform"), 3)

    def test_entradas_vazias_dao_erro_claro(self):
        with self.assertRaises(ValueError):
            musica.tira_ritmo([])
        with self.assertRaises(ValueError):
            musica.musicograma([])

    def test_linha_do_tempo_respeita_o_ano_inicial(self):
        svg = musica.linha_do_tempo([("X", 1800, 1850, "#111111")], ano0=1800, ano1=1900)
        self.assertNotIn(">1700<", svg)
        self.assertIn(">1850<", svg)

    def test_musicograma_e_cores_respeitam_a_ordem(self):
        mg = musica.musicograma([("a", "#111111", "onda", 1), ("b", "#222222", "bloco", 1)])
        self.assertLess(mg.index("#111111"), mg.index("#222222"))
        cores = musica.partitura_cores([list("CG")])
        self.assertLess(cores.index(musica.CORES_NOTAS["C"]), cores.index(musica.CORES_NOTAS["G"]))


if __name__ == "__main__":
    unittest.main()
