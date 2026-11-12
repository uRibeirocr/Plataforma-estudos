import unittest

from rodada import Rodada, mensagem_estrelas


def questoes(n):
    return [{"id": i, "pergunta": f"q{i}", "alternativas": []} for i in range(n)]


def certo(pontos=10):
    return {"correta": True, "pontos": pontos, "correta_id": 1}


def errado():
    return {"correta": False, "pontos": 0, "correta_id": 2}


class RodadaTest(unittest.TestCase):
    def test_fluxo_completo_com_acertos_e_erros(self):
        r = Rodada("MATEMATICA", questoes(4))
        self.assertEqual((r.total, r.numero_atual, r.progresso), (4, 1, 0.0))

        r.registrar(certo(), 1)
        self.assertEqual(r.progresso, 0.25)  # respondida conta como concluída
        r.avancar()
        r.registrar(errado(), 9)
        r.avancar()
        r.registrar(certo(), 1)
        r.avancar()
        r.registrar(certo(), 1)
        r.avancar()

        self.assertTrue(r.terminou)
        self.assertIsNone(r.questao)
        self.assertEqual((r.acertos, r.pontos, len(r.erros)), (3, 30, 1))
        self.assertEqual(r.percentual, 0.75)
        self.assertEqual(r.estrelas, 2)
        self.assertEqual(r.progresso, 1.0)

    def test_nao_aceita_resposta_dupla_nem_avancar_sem_responder(self):
        r = Rodada("GEOGRAFIA", questoes(2))
        with self.assertRaises(ValueError):
            r.avancar()
        r.registrar(certo(), 1)
        with self.assertRaises(ValueError):
            r.registrar(certo(), 1)

    def test_refazer_erros(self):
        r = Rodada("MATEMATICA", questoes(3))
        r.registrar(errado(), 9)
        r.avancar()
        r.registrar(certo(), 1)
        r.avancar()
        r.registrar(errado(), 9)
        r.avancar()
        nova = r.refazer_erros()
        self.assertEqual([q["id"] for q in nova.questoes], [0, 2])
        self.assertEqual((nova.indice, nova.pontos, nova.acertos), (0, 0, 0))

    def test_sem_erros_nao_ha_o_que_refazer(self):
        r = Rodada("MATEMATICA", questoes(1))
        r.registrar(certo(), 1)
        self.assertIsNone(r.refazer_erros())

    def test_estrelas(self):
        def com(acertos, total):
            r = Rodada("M", questoes(total))
            for i in range(total):
                r.registrar(certo() if i < acertos else errado(), 1)
                r.avancar()
            return r.estrelas

        self.assertEqual(com(10, 10), 3)
        self.assertEqual(com(9, 10), 3)
        self.assertEqual(com(7, 10), 2)
        self.assertEqual(com(4, 10), 1)
        self.assertEqual(com(3, 10), 0)
        for n in range(4):
            self.assertTrue(mensagem_estrelas(n))

    def test_ultima_questao(self):
        r = Rodada("M", questoes(2))
        self.assertFalse(r.ultima_questao)
        r.registrar(certo(), 1)
        r.avancar()
        self.assertTrue(r.ultima_questao)

    def test_rodada_vazia(self):
        r = Rodada("M", [])
        self.assertTrue(r.terminou)
        self.assertEqual((r.progresso, r.percentual, r.estrelas), (0.0, 0.0, 0))


if __name__ == "__main__":
    unittest.main()
