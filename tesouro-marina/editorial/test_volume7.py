"""O PDF do Volume 7 é publicado a cada merge no main (publicar-tesouro.yml), então enquanto faltam unidades ele não pode
prometer o que não tem: sumário e carta só falam das unidades montadas. Rodar: python3 -m unittest test_volume7"""
import re
import unittest
from unittest import mock

import fontes_v1
import livro
import volume7
from livro import Livro


class EdicaoParcial(unittest.TestCase):
    def test_sumario_lista_so_as_unidades_montadas(self):
        html = volume7.sumario({"Unidade 1 · Cumprimentos": 6, "Encerramento": 12})
        self.assertIn("Cumprimentos", html)
        self.assertNotIn("A família", html)    # nenhuma linha para unidade que não existe no arquivo
        self.assertIn("Edição em produção", html)

    def test_sumario_completo_lista_as_oito_e_nao_avisa(self):
        inicio = {n: 6 + 6 * i for i, (n, _) in enumerate(volume7.UNIDADES)}
        html = volume7.sumario({**inicio, "Encerramento": 60})
        for _, nome in (n.split(" · ", 1) for n, _ in volume7.UNIDADES):
            self.assertIn(nome, html)
        self.assertNotIn("Edição em produção", html)

    def test_carta_nao_promete_oito_unidades_enquanto_faltam(self):
        L = Livro(7, "Primeiras línguas")
        volume7.carta(L)
        html = L.paginas[0][1]
        self.assertEqual(volume7.parcial(), len(volume7.UNIDADES_PRONTAS) < len(volume7.UNIDADES))
        if volume7.parcial():
            self.assertIn("edição em produção", html)
            self.assertNotIn("Oito unidades, uma para cada tema", html)
        else:
            self.assertIn("Oito unidades, uma para cada tema", html)


class VolumeCompleto(unittest.TestCase):
    """Monta o livro inteiro sem pintar nenhuma aquarela (livro.arte trocada por um nome falso): só a estrutura é conferida."""

    @classmethod
    def setUpClass(cls):
        cls.cartoes = []
        real = volume7.cartoes

        def gravar(L, t, itens, *a, **k):
            cls.cartoes.append((t, itens))
            return real(L, t, itens, *a, **k)

        with mock.patch.object(livro, "arte", lambda nome, colorir=False: "x.png"), mock.patch.object(volume7, "cartoes", gravar):
            volume7.INICIO.clear()
            cls.L = volume7.montar()
            cls.inicio = dict(volume7.INICIO)
            volume7.INICIO.clear()

    def test_o_livro_tem_64_paginas(self):
        self.assertEqual(len(self.L.paginas), 64)

    def test_cada_unidade_tem_6_paginas_e_o_latim_6(self):
        pontos = [self.inicio[n] for n, _ in volume7.UNIDADES] + [self.inicio["Latim"], self.inicio["Encerramento"]]
        self.assertEqual([b - a for a, b in zip(pontos, pontos[1:])], [6] * 9)   # as oito unidades e o latim
        self.assertEqual(64 - self.inicio["Encerramento"] + 1, 5)

    def test_nove_conjuntos_de_cartoes_com_nove_cartoes_cada(self):
        self.assertEqual(len(self.cartoes), 9)   # oito unidades e as palavras-mãe
        for t, itens in self.cartoes:
            self.assertEqual(len(itens), 9, t)
            self.assertEqual(len({i["pt"] for i in itens}), 9, f"{t}: palavra repetida")
            for i in itens:
                self.assertTrue(i["en"] and i["fr"], f"{t}/{i['pt']}: falta inglês ou francês")
                self.assertTrue("la" in i, f"{t}/{i['pt']}: falta a chave do latim (None quando não há palavra clássica)")

    def test_toda_gravura_usada_esta_no_catalogo_com_hash(self):
        nomes = set(volume7.gravuras_usadas(self.L))
        self.assertGreater(len(nomes), 20)
        self.assertEqual(sorted(n for n in nomes if n not in fontes_v1.ITENS), [])
        self.assertEqual(fontes_v1.verificar(), 0)

    def test_nenhum_verso_sai_sem_etiqueta_de_idioma(self):
        # toda rima ou canção vem por pagina_verso, e o bloco do original traz o rótulo do idioma
        html = "".join(h for _, h in self.L.paginas)
        blocos = re.findall(r'<p lang="(en|fr)"', html)
        rotulos = re.findall(r'letter-spacing:\.12em;color:#fff;background:var\(--d-(ingles|frances|latim)\)', html)
        self.assertGreaterEqual(len(rotulos), len(blocos))
        self.assertEqual(len(re.findall(r'<p lang="en"', html)), 8)   # uma rima inglesa por unidade
        self.assertEqual(len(re.findall(r'<p lang="fr"', html)), 8 + 1)   # uma canção por unidade, mais Frère Jacques na unidade 2


if __name__ == "__main__":
    unittest.main()
