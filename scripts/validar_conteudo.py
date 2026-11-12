"""Valida conteudo/questoes.json: estrutura, gabarito único e imagens existentes.

Uso (a partir da raiz do repositório):  python scripts/validar_conteudo.py
Sai com código 1 se encontrar qualquer problema.
"""
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUESTOES = RAIZ / "conteudo" / "questoes.json"
ASSETS = RAIZ / "frontend" / "assets"
MATERIAS = {"MATEMATICA", "GEOGRAFIA"}


def validar() -> list[str]:
    erros: list[str] = []
    dados = json.loads(QUESTOES.read_text(encoding="utf-8"))

    for campo in ("id", "codigo", "pergunta"):
        repetidos = [k for k, v in Counter(q[campo] for q in dados).items() if v > 1]
        if repetidos:
            erros.append(f"valores repetidos em '{campo}': {repetidos}")
    ids_alt = [a["id"] for q in dados for a in q["alternativas"]]
    if len(ids_alt) != len(set(ids_alt)):
        erros.append("ids de alternativas repetidos")

    for q in dados:
        cod = q["codigo"]
        if q["materia"] not in MATERIAS:
            erros.append(f"{cod}: matéria inválida {q['materia']!r}")
        if not q.get("explicacao"):
            erros.append(f"{cod}: sem explicação")
        alts = q["alternativas"]
        if len(alts) != 4:
            erros.append(f"{cod}: esperado 4 alternativas, encontrado {len(alts)}")
        if sum(1 for a in alts if a["correta"]) != 1:
            erros.append(f"{cod}: deve haver exatamente 1 alternativa correta")
        if [a["letra"] for a in alts] != list("ABCD")[: len(alts)]:
            erros.append(f"{cod}: letras fora de ordem")
        imagens = [q["imagem_pergunta"], q.get("imagem_explicacao")] + [a["imagem"] for a in alts]
        for img in filter(None, imagens):
            if not (ASSETS / img).is_file():
                erros.append(f"{cod}: imagem ausente em frontend/assets/{img}")
    return erros


if __name__ == "__main__":
    problemas = validar()
    for p in problemas:
        print("ERRO:", p)
    total = len(json.loads(QUESTOES.read_text(encoding="utf-8")))
    print(f"{total} questões verificadas, {len(problemas)} problema(s).")
    sys.exit(1 if problemas else 0)
