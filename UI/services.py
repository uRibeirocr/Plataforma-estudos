"""Cliente HTTP da API local da Plataforma de Estudos."""
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
            message = json.loads(exc.read().decode("utf-8")).get("erro", "Erro na API.")
        except (UnicodeDecodeError, json.JSONDecodeError):
            message = "Erro na API."
        raise ApiError(message) from exc
    except URLError as exc:
        raise ApiError("Não foi possível conectar à API. Inicie `python backend/server.py`.") from exc

def cadastrar(name, email, password, role):
    return _request("POST", "/auth/register", {"name": name, "email": email, "password": password, "role": role})

def entrar(email, password):
    return _request("POST", "/auth/login", {"email": email, "password": password})

def buscar_exercicios(materia):
    return _request("GET", f"/questions?materia={materia}")

def responder(question_id, option_id):
    return _request("POST", "/attempts", {"question_id": question_id, "option_id": option_id})

def meu_progresso():
    return _request("GET", "/me/progress")

def vincular_aluno(email):
    return _request("POST", "/guardian/link", {"student_email": email})

def alunos_vinculados():
    return _request("GET", "/guardian/students")
