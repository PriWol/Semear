"""O PDF do Volume 7 é publicado a cada merge no main (publicar-tesouro.yml), então enquanto faltam unidades ele não pode
prometer o que não tem: sumário e carta só falam das unidades montadas. Rodar: python3 -m unittest test_volume7"""
import unittest

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


if __name__ == "__main__":
    unittest.main()
