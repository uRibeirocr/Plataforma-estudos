import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

import config
import estado
import services

QUESTAO_API = {
    "id": 7, "codigo": "M05", "tipo": "TABUADA", "pergunta": "Quanto é 4 × 2?",
    "imagemPergunta": "matematica/M05_pergunta.png", "materiaId": 1, "materia": "MATEMATICA",
    "ativo": True,
    "alternativas": [
        {"id": 17, "letra": "A", "texto": "8", "imagem": "matematica/M05_A.png"},
        {"id": 18, "letra": "B", "texto": "6", "imagem": "matematica/M05_B.png"},
    ],
}


class ApiFalsa(BaseHTTPRequestHandler):
    """Imita o contrato da API Java o suficiente para testar o cliente."""
    chamadas = []

    def log_message(self, *args):
        pass

    def _responder(self, status, corpo):
        dados = json.dumps(corpo).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _corpo(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(tamanho) or b"{}")

    def do_POST(self):
        corpo = self._corpo()
        ApiFalsa.chamadas.append(("POST", self.path, corpo, self.headers.get("Authorization")))
        if self.path == "/api/auth/login":
            if corpo["senha"] != "123456":
                return self._responder(401, {"status": 401, "message": "Usuário ou senha inválidos."})
            return self._responder(200, {"id": 3, "nome": corpo["nome"], "tipoUsuario": "ALUNO", "token": "jwt-x"})
        if self.path == "/api/usuarios":
            if len(corpo["senha"]) < 6:
                return self._responder(400, {"message": "Dados inválidos.",
                                              "fieldErrors": {"senha": "tamanho deve ser entre 6 e 100"}})
            return self._responder(201, {"id": 3, "nome": corpo["nome"], "tipoUsuario": corpo["tipoUsuario"]})
        if self.path == "/api/tentativas":
            acertou = corpo["alternativaId"] == 17
            return self._responder(201, {
                "id": 1, "usuarioId": corpo["usuarioId"], "exercicioId": corpo["exercicioId"],
                "alternativaId": corpo["alternativaId"], "correta": acertou, "pontuacao": 10 if acertou else 0,
                "alternativaCorretaId": 17, "explicacao": "4 × 2 = 8.", "imagemExplicacao": None})
        self._responder(404, {"message": "Recurso não encontrado."})

    def do_GET(self):
        ApiFalsa.chamadas.append(("GET", self.path, None, self.headers.get("Authorization")))
        if self.path == "/api/materias":
            return self._responder(200, [{"id": 1, "nome": "MATEMATICA"}, {"id": 2, "nome": "GEOGRAFIA"}])
        if self.path.startswith("/api/exercicios/materia/1"):
            return self._responder(200, [QUESTAO_API])
        if self.path.startswith("/api/exercicios/materia/2"):
            return self._responder(200, [])
        self._responder(404, {"message": "Recurso não encontrado."})


class ServicesApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = HTTPServer(("127.0.0.1", 0), ApiFalsa)
        threading.Thread(target=cls.servidor.serve_forever, daemon=True).start()
        cls.url_original = config.API_URL
        config.API_URL = f"http://127.0.0.1:{cls.servidor.server_port}/api"

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        config.API_URL = cls.url_original

    def setUp(self):
        estado.encerrar_sessao()
        services._materias_cache.clear()
        ApiFalsa.chamadas.clear()

    def test_login_guarda_token_e_envia_nas_proximas_chamadas(self):
        usuario = services.entrar("Ana", "123456")
        self.assertEqual(usuario, {"id": 3, "nome": "Ana", "tipo": "ALUNO"})
        self.assertEqual(estado.sessao["token"], "jwt-x")

        services.montar_rodada("MATEMATICA", 5)
        self.assertEqual(ApiFalsa.chamadas[-1][3], "Bearer jwt-x")

    def test_login_invalido_mostra_a_mensagem_da_api(self):
        with self.assertRaisesRegex(services.ApiError, "inválidos"):
            services.entrar("Ana", "errada")
        self.assertIsNone(estado.sessao["token"])

    def test_cadastro_invalido_inclui_erros_dos_campos(self):
        with self.assertRaisesRegex(services.ApiError, "senha: tamanho"):
            services.cadastrar("Ana", "123", "ALUNO")

    def test_montar_rodada_normaliza_e_pede_limite_e_embaralhar(self):
        services.entrar("Ana", "123456")
        questoes = services.montar_rodada("MATEMATICA", 10)
        self.assertEqual(questoes[0]["pergunta"], "Quanto é 4 × 2?")
        self.assertEqual(questoes[0]["alternativas"][0], {"id": 17, "letra": "A", "texto": "8",
                                                          "imagem": "matematica/M05_A.png"})
        self.assertNotIn("correta", questoes[0]["alternativas"][0])
        caminho = [c[1] for c in ApiFalsa.chamadas if "exercicios" in c[1]][0]
        self.assertIn("limite=10", caminho)
        self.assertIn("embaralhar=true", caminho)

    def test_materia_sem_exercicios(self):
        services.entrar("Ana", "123456")
        with self.assertRaisesRegex(services.ApiError, "Ainda não há exercícios"):
            services.montar_rodada("GEOGRAFIA", 10)

    def test_responder_traduz_a_resposta_da_api(self):
        services.entrar("Ana", "123456")
        questao = services.montar_rodada("MATEMATICA", 1)[0]
        errou = services.responder("MATEMATICA", questao, 18)
        self.assertEqual((errou["correta"], errou["pontos"], errou["correta_id"]), (False, 0, 17))
        acertou = services.responder("MATEMATICA", questao, 17)
        self.assertEqual((acertou["correta"], acertou["pontos"]), (True, 10))
        self.assertEqual(acertou["explicacao"], "4 × 2 = 8.")
        corpo = [c[2] for c in ApiFalsa.chamadas if c[1] == "/api/tentativas"][-1]
        self.assertEqual(corpo, {"usuarioId": 3, "exercicioId": 7, "alternativaId": 17})

    def test_api_fora_do_ar_vira_mensagem_amigavel(self):
        original = config.API_URL
        config.API_URL = "http://127.0.0.1:1/api"  # porta fechada
        try:
            with self.assertRaisesRegex(services.ApiError, "offline"):
                services.entrar("Ana", "123456")
        finally:
            config.API_URL = original


class ServicesOfflineTest(unittest.TestCase):
    def setUp(self):
        estado.encerrar_sessao()
        services.entrar_offline("Visitante")

    def test_rodada_offline_usa_o_conteudo_local_e_corrige_no_app(self):
        questoes = services.montar_rodada("GEOGRAFIA", 5)
        self.assertEqual(len(questoes), 5)
        q = questoes[0]
        certa = q["_correta_id"]
        errada = next(a["id"] for a in q["alternativas"] if a["id"] != certa)

        self.assertTrue(services.responder("GEOGRAFIA", q, certa)["correta"])
        r = services.responder("GEOGRAFIA", q, errada)
        self.assertEqual((r["correta"], r["pontos"], r["correta_id"]), (False, 0, certa))
        self.assertTrue(r["explicacao"])

        prog = {p["materia"]: p for p in services.meu_progresso()}
        self.assertEqual(prog["GEOGRAFIA"]["tentativasRespondidas"], 2)
        self.assertEqual(prog["GEOGRAFIA"]["pontuacao"], 10)
        self.assertEqual(prog["GEOGRAFIA"]["totalExercicios"], 50)
        self.assertEqual(prog["MATEMATICA"]["tentativasRespondidas"], 0)

    def test_todas_as_questoes(self):
        for materia in ("MATEMATICA", "GEOGRAFIA"):
            self.assertEqual(len(services.montar_rodada(materia, None)), 50)


if __name__ == "__main__":
    unittest.main()
