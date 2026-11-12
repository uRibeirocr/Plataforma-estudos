"""Configuração do frontend (valores podem ser trocados por variáveis de ambiente)."""
import os
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTA_ASSETS = AQUI / "assets"

# URL base da API Spring Boot (termina em /api).
API_URL = os.getenv("PLATAFORMA_API_URL", "http://127.0.0.1:8080/api").rstrip("/")
TIMEOUT_API = float(os.getenv("PLATAFORMA_API_TIMEOUT", "8"))

# Quantas questões por rodada (None = todas da matéria).
OPCOES_QUANTIDADE = [("5", 5), ("10", 10), ("20", 20), ("Todas", None)]
QUANTIDADE_PADRAO = 10

PONTOS_POR_ACERTO = 10

MATERIAS = {
    "MATEMATICA": {"titulo": "Matemática", "emoji": "🧮"},
    "GEOGRAFIA": {"titulo": "Geografia", "emoji": "🌎"},
}


def arquivo_questoes() -> Path | None:
    """Procura conteudo/questoes.json (modo offline) no repositório ou ao lado do app."""
    for candidato in (AQUI.parent / "conteudo" / "questoes.json", AQUI / "conteudo" / "questoes.json"):
        if candidato.is_file():
            return candidato
    return None
