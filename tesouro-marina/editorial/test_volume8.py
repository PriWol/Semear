"""Volume 8 "Jogos e descobertas" (versão menor, estória #112 PR A): estrutura, conteúdo que os cadernos de 2 anos prometem, privacidade e créditos.
Estes testes falham até volume8.py existir. Rodar: python3 -m unittest test_volume8"""
import re
import unittest
from unittest import mock

import caderno
import fontes_v1
import livro
import volume8
from livro import Livro

PAGINAS = 32   # plano do Dev B; o número final é o do pdfinfo e o PR B o usa em `paginas` do tesouro.json
BLOCOS = ["Esconder e achar", "Minha vez, sua vez", "Mandar e obedecer", "Calma", "Diário"]
ATIVIDADES = ["Esconde-esconde", "A caixa surpresa", "Minha vez, sua vez", "Siga a Marina", "A garrafa da calma", "Respirar com o bichinho"]
RIMAS = ["Corre, cotia", "Cadê? Achou!", "O barquinho de papel", "Um elefante"]
# rimas escritas pela coleção; as demais são tradicionais (a origem impressa em cada rima decide a coluna dos créditos)
RIMAS_DA_COLECAO = {"Cadê? Achou!", "O barquinho de papel"}


def _texto(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


class Base(unittest.TestCase):
    """Monta o livro inteiro sem pintar aquarela (livro.arte trocada por um nome falso): só a estrutura é conferida."""

    @classmethod
    def setUpClass(cls):
        cls.conjuntos = []
        reais = {n: getattr(volume8, n, None) for n in ("cartoes", "memoria")}

        def gravar(nome):
            def f(L, t, itens, *a, **k):
                cls.conjuntos.append((nome, t, itens))
                return reais[nome](L, t, itens, *a, **k)
            return f

        livro.VERSAO["atual"] = "impressao"   # o estado global é de outros testes do mesmo processo
        with mock.patch.object(livro, "arte", lambda nome, colorir=False: "x.png"), \
                mock.patch.object(volume8, "cartoes", gravar("cartoes"), create=True), \
                mock.patch.object(volume8, "memoria", gravar("memoria"), create=True):
            volume8.INICIO.clear()
            cls.L = volume8.montar()
            cls.inicio = dict(volume8.INICIO)
            volume8.INICIO.clear()
        cls.html = "".join(h for _, h in cls.L.paginas)
        cls.texto = _texto(cls.html)


class Estrutura(Base):
    def test_titulo_e_subtitulo_definitivos(self):
        self.assertEqual((self.L.volume, self.L.titulo_volume), (8, "Jogos e descobertas"))
        self.assertIn("Volume 8 · Jogos e descobertas", self.html)   # o caderno aponta exatamente para este nome (caderno.py, unidade 8)

    def test_total_de_paginas_e_par_e_multiplo_de_4(self):
        n = len(self.L.paginas)
        self.assertEqual(n, PAGINAS)
        self.assertEqual(n % 2, 0)
        self.assertEqual(n % 4, 0, "miolo redondo para encadernar")

    def test_toda_pagina_tem_numero_sequencial_sem_repeticao(self):
        self.assertEqual([n for n, _ in self.L.paginas], list(range(1, PAGINAS + 1)))
        for n, h in self.L.paginas[2:]:   # capa e rosto não levam número visível
            if 'class="num"' in h:
                self.assertIn(f'<span class="num">{n}</span>', h)

    def test_nao_ha_ids_html_duplicados(self):
        ids = re.findall(r'\bid="([^"]+)"', self.html)
        self.assertEqual(sorted({i for i in ids if ids.count(i) > 1}), [])

    def test_os_cinco_blocos_estao_no_sumario_e_em_ordem(self):
        pontos = [self.inicio[b] for b in self.inicio if any(k in b for k in BLOCOS)]
        self.assertGreaterEqual(len(pontos), 5)
        self.assertEqual(pontos, sorted(pontos))
        self.assertEqual(len(set(pontos)), len(pontos), "dois blocos começam na mesma página")
        self.assertLessEqual(max(pontos), PAGINAS)

    def test_sumario_honesto_lista_so_o_que_existe(self):
        n_sum = next(n for n, h in self.L.paginas if "Sumário" in h or "sumário" in h)
        sumario = _texto(dict(self.L.paginas)[n_sum])
        for b in BLOCOS:
            self.assertIn(b, sumario)
        for promessa in ("Meu livro de histórias", "A orquestra da casa", "O nosso jardim", "bonecos de vara", "cenários dobráveis"):
            self.assertNotIn(promessa, sumario, "ficam para a estória de evolução do volume")

    def test_a_carta_e_o_encerramento_dizem_que_e_a_primeira_versao(self):
        self.assertRegex(self.texto, r"(?i)primeira versão|versão menor|edição inicial")


class ConteudoPrometidoPelosCadernos(Base):
    def test_toda_atividade_da_unidade_8_do_caderno_tem_jogo_no_volume(self):
        for a in ATIVIDADES:
            self.assertIn(a, self.texto, a)

    def test_o_caderno_realmente_cita_essas_atividades_e_o_volume_8(self):
        cad = _texto("".join(h for _, h in caderno.montar().paginas))
        self.assertIn("Volume 8 · Jogos e descobertas", cad)
        for a in ATIVIDADES + RIMAS:
            self.assertIn(a, cad, f"o caderno deixou de citar {a}: revisar o volume 8")

    def test_brincar_junto_e_as_tres_ideias_aparecem(self):
        self.assertIn("Brincar junto", self.texto)
        for ideia in ("esperar a vez", "mandar e obedecer", "esconder e achar"):
            self.assertIn(ideia, self.texto.lower())

    def test_as_rimas_do_caderno_estao_no_volume(self):
        for r in RIMAS:
            self.assertIn(r, self.texto, r)

    def test_conjuntos_recortaveis_completos_e_sem_repeticao(self):
        por_nome = [(n, t, i) for n, t, i in self.conjuntos]
        self.assertGreaterEqual(len([c for c in por_nome if c[0] == "cartoes"]), 2)   # "O que está na caixa?" e "A chefe mandou"
        memorias = [c for c in por_nome if c[0] == "memoria"]
        self.assertEqual(len(memorias), 1)
        self.assertEqual(len(memorias[0][2]), 6, "jogo da memória de 6 pares (nível de 3 pares para 2 anos)")
        for nome, t, itens in por_nome:
            self.assertEqual(len({repr(i) for i in itens}), len(itens), f"{t}: item repetido")
            if nome == "cartoes":
                self.assertEqual(len(itens), 9, t)

    def test_niveis_para_2_3_e_4_anos_com_dois_anos_como_ponto_de_partida(self):
        for faixa in ("2 anos", "3 anos", "4 anos"):
            self.assertIn(faixa, self.texto)
        self.assertNotRegex(self.texto, r"\b(?:9|10|11|12) anos\b")

    def test_regras_comuns_sem_competicao(self):
        self.assertNotRegex(self.texto.lower(), r"\b(vencedor|vencedora|perdedor|perdedora|quem ganha|ganhou|perdeu|ranking)\b")

    def test_nota_de_seguranca_pecas_pequenas_e_esconderijos(self):
        self.assertRegex(self.texto, r"(?i)pe[çc]as pequenas|maiores que o punho")
        self.assertRegex(self.texto, r"(?i)geladeira|esconderijos? seguros?")

    def test_garrafa_da_calma_guarda_fora_do_alcance_e_supervisao_de_agua(self):
        pag = next(_texto(h) for _, h in self.L.paginas if "A garrafa da calma" in h and "por que isto importa" in h)
        self.assertIn("fora do alcance dela", pag)
        frase = re.sub(r"<[^>]+>", "", caderno.AGUA).split(", ", 1)[1].split(",")[0]
        self.assertIn(frase, pag)

    def test_a_chefe_mandou_tem_gesto_de_parar_e_esconde_esconde_tem_aviso_de_seguranca(self):
        self.assertRegex(self.texto, r"(?i)m[ãa]os no peito")
        self.assertRegex(self.texto, r"(?i)nada de geladeira|n[ãa]o se esconda em")


class RimasECreditos(Base):
    def _rimas(self):
        achadas = []
        for _, h in self.L.paginas:
            achadas += re.findall(r'<h2 class="titulo"[^>]*>([^<]+)</h2>.*?<div class="peq"[^>]*>([^<]+)</div>', h, re.DOTALL)
        return [(t.strip(), o.strip()) for t, o in achadas if t.strip() in RIMAS]

    def test_toda_rima_traz_a_origem_impressa(self):
        achadas = dict(self._rimas())
        self.assertEqual(sorted(achadas), sorted(RIMAS))
        for t, origem in achadas.items():
            esperado = caderno.COLECAO if t in RIMAS_DA_COLECAO else caderno.TRAD
            self.assertEqual(origem, esperado, f"{t}: origem diferente da do caderno")

    def test_toda_rima_aparece_na_pagina_de_creditos_na_coluna_da_sua_origem(self):
        creditos = _texto(next(h for _, h in self.L.paginas if "créditos" in h.lower() and "<h1" in h and "Rimas" in h))
        for t in RIMAS:
            self.assertIn(t, creditos, f"{t} sem crédito")
        self.assertRegex(creditos, r"(?i)dom[ií]nio p[úu]blico")
        self.assertRegex(creditos, r"(?i)escritas? pela cole[çc][ãa]o")
        self.assertRegex(creditos, r"(?i)tradicionais? brasileiras?")

    def test_sem_cantigas_vetadas_pelo_adr_0021(self):
        vetadas = ["Atirei o pau", "Boi da cara preta", "Cuca vem", "Marcha, soldado", "A canoa virou", "Parabéns"]
        self.assertEqual([v for v in vetadas if v.lower() in self.texto.lower()], [])

    def test_nenhuma_gravura_sem_hash_no_catalogo(self):
        nomes = set(volume8.gravuras_usadas(self.L))
        self.assertEqual(sorted(n for n in nomes if n not in fontes_v1.ITENS), [])
        self.assertEqual(fontes_v1.verificar(), 0)

    def test_creditos_dizem_que_as_ilustracoes_novas_sao_aquarela_da_colecao(self):
        self.assertRegex(self.texto, r"(?i)aquarela digital procedural da cole[çc][ãa]o")


class PrivacidadeEDiario(Base):
    def test_sem_dados_de_familia_ou_de_contato(self):
        self.assertNotRegex(self.html, r"[\w.+-]+@[\w-]+\.[\w.]+", "e-mail")
        self.assertNotRegex(self.texto, r"\(?\b\d{2}\)?\s?9?\d{4}[-\s]\d{4}\b", "telefone")
        self.assertNotRegex(self.texto, r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "CPF")
        self.assertNotRegex(self.texto, r"\b\d{1,2}/\d{1,2}/(?:19|20)\d{2}\b", "data de nascimento preenchida")
        self.assertNotRegex(self.html, r"(?i)localStorage|indexedDB|<script|https?://(?!www\.archive\.org|archive\.org)", "nada de script, armazenamento ou rede")

    def test_so_a_personagem_marina_e_nenhum_nome_de_crianca_real(self):
        # a coleção só nomeia a personagem; o diário e as fichas ficam em branco para a família escrever
        nomes_reais = {"Helena", "Alice", "Miguel", "Arthur", "Heitor", "Laura", "Valentina", "Sophia", "Davi", "Theo", "Lorenzo", "Manuela"}
        achados = [n for n in nomes_reais if re.search(rf"\b{n}\b", self.texto)]
        self.assertEqual(achados, [])
        self.assertIn("Marina", self.texto)

    def test_diario_tem_duas_paginas_em_branco_sem_avaliacao(self):
        paginas = [h for _, h in self.L.paginas if re.search(r'<h1 class="titulo"[^>]*>\s*Di[áa]rio', h)]
        self.assertEqual(len(paginas), 2)
        for h in paginas:
            t = _texto(h)
            self.assertRegex(t, r"(?i)o que vi")
            self.assertRegex(t, r"(?i)o que tentar depois")
            self.assertRegex(t, r"(?i)n[ãa]o [ée] avalia[çc][ãa]o")
            self.assertNotRegex(t.lower(), r"\b(aprovad\w+|reprovad\w+|pontua\w+|notas?|certo|errado|acertou|errou)\b")

    def test_nada_pre_preenchido_nos_campos_do_diario(self):
        for _, h in self.L.paginas:
            if re.search(r'<h1 class="titulo"[^>]*>\s*Di[áa]rio', h):
                for celula in re.findall(r"<td[^>]*>(.*?)</td>", h, re.DOTALL):
                    self.assertTrue("peq" in celula or not re.sub(r"<[^>]+>|&nbsp;|\s", "", celula), "célula do diário já preenchida")


class EdicaoParcial(unittest.TestCase):
    def test_sumario_lista_so_blocos_montados(self):
        html = volume8.sumario({"Bloco 1 · Esconder e achar": 6, "Encerramento": 30})
        self.assertIn("Esconder e achar", html)
        self.assertNotIn("Diário", html)   # nenhuma linha para bloco que não existe no arquivo

    def test_parcial_e_falso_com_o_volume_completo(self):
        self.assertFalse(volume8.parcial())


if __name__ == "__main__":
    unittest.main()
