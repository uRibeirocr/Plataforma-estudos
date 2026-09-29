"""Dados locais das questões enquanto a API da equipe não está pronta.

As quatro perguntas já existentes no frontend e as imagens de Flávio foram
mantidas. As demais questões são carregadas do arquivo questoes.json.
"""
import json
from pathlib import Path


_EXISTENTES = [
    {
        "id": 1, "codigo": "EX01", "materia": "MATEMATICA",
        "pergunta": "Quantos carros temos no total na imagem?",
        "imagem_pergunta": "varios_carros.png",
        "alternativas": [
            {"id": 1, "texto": "10", "imagem": "matematica/EX01_A.png", "correta": False},
            {"id": 2, "texto": "16", "imagem": "matematica/EX01_B.png", "correta": True},
            {"id": 3, "texto": "12", "imagem": "matematica/EX01_C.png", "correta": False},
            {"id": 4, "texto": "20", "imagem": "matematica/EX01_D.png", "correta": False},
        ],
    },
    {
        "id": 2, "codigo": "EX02", "materia": "MATEMATICA",
        "pergunta": "Quantos macaquinhos estão a dormir?",
        "imagem_pergunta": "5_macacos.png",
        "alternativas": [
            {"id": 5, "texto": "3", "imagem": "matematica/EX02_A.png", "correta": False},
            {"id": 6, "texto": "5", "imagem": "matematica/EX02_B.png", "correta": True},
            {"id": 7, "texto": "6", "imagem": "matematica/EX02_C.png", "correta": False},
            {"id": 8, "texto": "8", "imagem": "matematica/EX02_D.png", "correta": False},
        ],
    },
    {
        "id": 3, "codigo": "EX03", "materia": "MATEMATICA",
        "pergunta": "Quantas girafas consegues contar?",
        "imagem_pergunta": "4_girafas.png",
        "alternativas": [
            {"id": 9, "texto": "2", "imagem": "matematica/EX03_A.png", "correta": False},
            {"id": 10, "texto": "6", "imagem": "matematica/EX03_B.png", "correta": False},
            {"id": 11, "texto": "4", "imagem": "matematica/EX03_C.png", "correta": True},
            {"id": 12, "texto": "5", "imagem": "matematica/EX03_D.png", "correta": False},
        ],
    },
    {
        "id": 4, "codigo": "EX04", "materia": "MATEMATICA",
        "pergunta": "Quantos tigres estão juntos?",
        "imagem_pergunta": "3_tigres.png",
        "alternativas": [
            {"id": 13, "texto": "1", "imagem": "matematica/EX04_A.png", "correta": False},
            {"id": 14, "texto": "4", "imagem": "matematica/EX04_B.png", "correta": False},
            {"id": 15, "texto": "3", "imagem": "matematica/EX04_C.png", "correta": True},
            {"id": 16, "texto": "5", "imagem": "matematica/EX04_D.png", "correta": False},
        ],
    },
]

_adicionais = json.loads((Path(__file__).parent / "questoes.json").read_text(encoding="utf-8"))
EXERCICIOS = {
    "MATEMATICA": _EXISTENTES + [q for q in _adicionais if q["materia"] == "MATEMATICA"],
    "GEOGRAFIA": [q for q in _adicionais if q["materia"] == "GEOGRAFIA"],
}
