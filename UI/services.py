"""Cliente da API Spring Boot da Plataforma de Estudos."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import estado

API_URL = os.getenv("PLATAFORMA_API_URL", "http://127.0.0.1:8080/api").rstrip("/")

class ApiError(RuntimeError):
    pass

def _request(method, path, data=None):
    headers = {"Accept": "application/json"}
    if estado.sessao.get("token"):
        headers["Authorization"] = f"Bearer {estado.sessao['token']}"
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    try:
        with urlopen(Request(f"{API_URL}{path}", data=body, headers=headers, method=method), timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
            message = payload.get("mensagem") or payload.get("erro") or "Erro na API."
        except (UnicodeDecodeError, json.JSONDecodeError):
            message = "Erro na API."
        raise ApiError(message) from exc
    except URLError as exc:
        raise ApiError("Não foi possível conectar à API. Inicie o backend com `mvn spring-boot:run` na pasta projetoFametro.") from exc

def _usuario(login):
    return {"id": login["id"], "name": login["nome"], "role": login["tipoUsuario"]}

def cadastrar(nome, senha, tipo):
    _request("POST", "/usuarios", {"nome": nome, "senha": senha, "tipoUsuario": tipo})
    return entrar(nome, senha)

def entrar(nome, senha):
    resposta = _request("POST", "/auth/login", {"nome": nome, "senha": senha})
    return {"token": resposta["token"], "user": _usuario(resposta)}

def materias():
    return _request("GET", "/materias")

def buscar_exercicios(materia_nome):
    materia = next((item for item in materias() if item["nome"] == materia_nome), None)
    if not materia:
        raise ApiError("Matéria não encontrada na API.")
    estado.estado_atual["materia_id"] = materia["id"]
    exercicios = _request("GET", f"/exercicios/materia/{materia['id']}")
    if not exercicios:
        raise ApiError("Ainda não há exercícios cadastrados para esta matéria.")
    return [{
        "id": item["id"],
        "pergunta": item.get("pergunta") or "Observe a imagem e escolha a alternativa correta.",
        "imagem_pergunta": item.get("imagemPergunta"),
        "alternativas": [{"id": alt["id"], "texto": alt.get("texto", ""), "imagem": alt.get("imagem")} for alt in item["alternativas"]],
    } for item in exercicios]

def responder(exercicio_id, alternativa_id):
    usuario = estado.sessao.get("usuario") or {}
    resposta = _request("POST", "/tentativas", {"usuarioId": usuario["id"], "exercicioId": exercicio_id, "alternativaId": alternativa_id})
    progresso = obter_progresso(usuario["id"], estado.estado_atual["materia_id"])
    return {"correta": resposta["correta"], "explicacao": "Resposta registrada com sucesso.", "progresso": {"pontuacao": progresso["pontuacao"]}}

def obter_progresso(aluno_id, materia_id):
    return _request("GET", f"/progresso/alunos/{aluno_id}/materias/{materia_id}")

def meu_progresso():
    usuario = estado.sessao.get("usuario") or {}
    return {materia["nome"]: obter_progresso(usuario["id"], materia["id"]) for materia in materias()}

def vincular_aluno(aluno_id):
    responsavel = estado.sessao.get("usuario") or {}
    return _request("POST", "/responsaveis/vinculos", {"responsavelId": responsavel["id"], "alunoId": int(aluno_id)})

def alunos_vinculados():
    responsavel = estado.sessao.get("usuario") or {}
    return _request("GET", f"/responsaveis/{responsavel['id']}/alunos")
