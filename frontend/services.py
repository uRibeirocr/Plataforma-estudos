"""Camada de dados do frontend.

Fala com a API Spring Boot (JWT). Quando a sessão está em modo offline, usa o conteúdo local
de conteudo/questoes.json, com correção feita no próprio app e nada salvo no servidor.
"""
from __future__ import annotations

import json
import random
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import config
import estado


class ApiError(RuntimeError):
    """Erro com mensagem já pronta para mostrar ao usuário."""


# ------------------------------------------------------------------ HTTP

def _mensagem_de_erro(corpo: bytes, status: int) -> str:
    try:
        payload = json.loads(corpo.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return f"Erro {status} na API."
    mensagem = payload.get("message") or payload.get("mensagem") or f"Erro {status} na API."
    campos = payload.get("fieldErrors") or {}
    if campos:
        mensagem += " " + "; ".join(f"{campo}: {texto}" for campo, texto in campos.items())
    return mensagem


def _requisicao(metodo: str, caminho: str, dados=None):
    cabecalhos = {"Accept": "application/json"}
    token = estado.sessao.get("token")
    if token:
        cabecalhos["Authorization"] = f"Bearer {token}"
    corpo = None
    if dados is not None:
        corpo = json.dumps(dados).encode("utf-8")
        cabecalhos["Content-Type"] = "application/json"

    req = Request(f"{config.API_URL}{caminho}", data=corpo, headers=cabecalhos, method=metodo)
    try:
        with urlopen(req, timeout=config.TIMEOUT_API) as resposta:
            bruto = resposta.read()
            return json.loads(bruto.decode("utf-8")) if bruto else None
    except HTTPError as exc:
        raise ApiError(_mensagem_de_erro(exc.read(), exc.code)) from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise ApiError(
            "Não foi possível conectar à API. Verifique se o servidor está ligado "
            f"({config.API_URL}) ou jogue no modo offline."
        ) from exc


# ------------------------------------------------------------------ conta

def cadastrar(nome: str, senha: str, tipo: str) -> dict:
    _requisicao("POST", "/usuarios", {"nome": nome, "senha": senha, "tipoUsuario": tipo})
    return entrar(nome, senha)


def entrar(nome: str, senha: str) -> dict:
    resposta = _requisicao("POST", "/auth/login", {"nome": nome, "senha": senha})
    usuario = {"id": resposta["id"], "nome": resposta["nome"], "tipo": resposta["tipoUsuario"]}
    estado.sessao.update({"token": resposta["token"], "usuario": usuario, "offline": False})
    _materias_cache.clear()
    return usuario


def entrar_offline(nome: str) -> dict:
    usuario = {"id": None, "nome": nome or "Visitante", "tipo": "ALUNO"}
    estado.sessao.update({"token": None, "usuario": usuario, "offline": True})
    return usuario


# ------------------------------------------------------------------ conteúdo

_materias_cache: dict[str, int] = {}
_conteudo_local: list[dict] | None = None


def _carregar_local() -> list[dict]:
    global _conteudo_local
    if _conteudo_local is None:
        arquivo = config.arquivo_questoes()
        if arquivo is None:
            raise ApiError("Conteúdo offline não encontrado (conteudo/questoes.json).")
        _conteudo_local = json.loads(arquivo.read_text(encoding="utf-8"))
    return _conteudo_local


def _id_da_materia(nome: str) -> int:
    if not _materias_cache:
        for materia in _requisicao("GET", "/materias"):
            _materias_cache[materia["nome"]] = materia["id"]
    if nome not in _materias_cache:
        raise ApiError("Matéria não encontrada na API.")
    return _materias_cache[nome]


def _normalizar_api(item: dict) -> dict:
    return {
        "id": item["id"],
        "codigo": item.get("codigo"),
        "pergunta": item.get("pergunta") or "Observe a imagem e escolha a alternativa correta.",
        "imagem_pergunta": item.get("imagemPergunta"),
        "alternativas": [
            {"id": a["id"], "letra": a.get("letra") or "", "texto": a.get("texto") or "",
             "imagem": a.get("imagem")}
            for a in item["alternativas"]
        ],
    }


def _normalizar_local(item: dict) -> dict:
    correta = next(a for a in item["alternativas"] if a["correta"])
    return {
        "id": item["id"],
        "codigo": item.get("codigo"),
        "pergunta": item["pergunta"],
        "imagem_pergunta": item.get("imagem_pergunta"),
        "alternativas": [
            {"id": a["id"], "letra": a.get("letra", ""), "texto": a.get("texto") or "",
             "imagem": a.get("imagem")}
            for a in item["alternativas"]
        ],
        # Só existe offline: gabarito e explicação ficam no próprio app.
        "_correta_id": correta["id"],
        "_explicacao": item.get("explicacao"),
        "_imagem_explicacao": item.get("imagem_explicacao"),
    }


def montar_rodada(materia: str, quantidade: int | None) -> list[dict]:
    """Sorteia `quantidade` questões da matéria (None = todas, embaralhadas)."""
    if estado.sessao.get("offline"):
        todas = [q for q in _carregar_local() if q["materia"] == materia]
        random.shuffle(todas)
        escolhidas = todas if quantidade is None else todas[:quantidade]
        questoes = [_normalizar_local(q) for q in escolhidas]
    else:
        params = "embaralhar=true" + (f"&limite={quantidade}" if quantidade else "")
        itens = _requisicao("GET", f"/exercicios/materia/{_id_da_materia(materia)}?{params}")
        questoes = [_normalizar_api(i) for i in itens]

    if not questoes:
        raise ApiError("Ainda não há exercícios cadastrados para esta matéria.")
    return questoes


def responder(materia: str, questao: dict, alternativa_id: int) -> dict:
    """Envia/corrige a resposta. Devolve correta, pontos, correta_id, explicacao e imagem_explicacao."""
    if estado.sessao.get("offline"):
        correta_id = questao["_correta_id"]
        acertou = alternativa_id == correta_id
        resultado = {
            "correta": acertou,
            "pontos": config.PONTOS_POR_ACERTO if acertou else 0,
            "correta_id": correta_id,
            "explicacao": questao.get("_explicacao"),
            "imagem_explicacao": questao.get("_imagem_explicacao"),
        }
        parcial = estado.progresso_local.setdefault(
            materia, {"respondidas": 0, "acertos": 0, "pontos": 0})
        parcial["respondidas"] += 1
        parcial["acertos"] += 1 if acertou else 0
        parcial["pontos"] += resultado["pontos"]
        return resultado

    usuario = estado.usuario()
    r = _requisicao("POST", "/tentativas", {
        "usuarioId": usuario["id"], "exercicioId": questao["id"], "alternativaId": alternativa_id})
    return {
        "correta": r["correta"],
        "pontos": r["pontuacao"],
        "correta_id": r["alternativaCorretaId"],
        "explicacao": r.get("explicacao"),
        "imagem_explicacao": r.get("imagemExplicacao"),
    }


# ------------------------------------------------------------------ progresso

def meu_progresso() -> list[dict]:
    """Lista de progresso por matéria do aluno logado (formato igual ao da API)."""
    if estado.sessao.get("offline"):
        return [_progresso_local(nome) for nome in config.MATERIAS]
    return _requisicao("GET", f"/progresso/alunos/{estado.usuario()['id']}")


def progresso_do_aluno(aluno_id: int) -> list[dict]:
    return _requisicao("GET", f"/progresso/alunos/{aluno_id}")


def _progresso_local(materia: str) -> dict:
    parcial = estado.progresso_local.get(materia, {"respondidas": 0, "acertos": 0, "pontos": 0})
    total = sum(1 for q in _carregar_local() if q["materia"] == materia)
    resp = parcial["respondidas"]
    return {
        "materia": materia,
        "tentativasRespondidas": resp,
        "tentativasCorretas": parcial["acertos"],
        "tentativasErradas": resp - parcial["acertos"],
        "pontuacao": parcial["pontos"],
        "percentualAcertos": round(100 * parcial["acertos"] / resp, 2) if resp else 0.0,
        "exerciciosRespondidos": resp,
        "exerciciosDominados": parcial["acertos"],
        "totalExercicios": total,
        "percentualConclusao": round(100 * parcial["acertos"] / total, 2) if total else 0.0,
    }


# ------------------------------------------------------------------ responsável

def vincular_aluno(nome_do_aluno: str) -> None:
    _requisicao("POST", "/responsaveis/vinculos", {"alunoNome": nome_do_aluno.strip()})


def alunos_vinculados() -> list[dict]:
    return _requisicao("GET", f"/responsaveis/{estado.usuario()['id']}/alunos")
