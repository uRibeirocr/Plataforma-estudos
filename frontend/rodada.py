"""Regras de uma rodada de exercícios, sem nenhuma dependência de interface.

Fica separada das telas para poder ser testada sem abrir o Flet.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from config import PONTOS_POR_ACERTO


@dataclass
class Erro:
    """Uma questão errada, guardada para a revisão no fim da rodada."""
    questao: dict
    escolhida_id: int
    correta_id: int


@dataclass
class Rodada:
    materia: str
    questoes: list[dict]
    indice: int = 0
    pontos: int = 0
    acertos: int = 0
    erros: list[Erro] = field(default_factory=list)
    respondida: bool = False  # a questão atual já foi respondida?

    # ----- estado -----
    @property
    def total(self) -> int:
        return len(self.questoes)

    @property
    def terminou(self) -> bool:
        return self.indice >= self.total

    @property
    def questao(self) -> dict | None:
        return None if self.terminou else self.questoes[self.indice]

    @property
    def ultima_questao(self) -> bool:
        return self.indice == self.total - 1

    @property
    def numero_atual(self) -> int:
        """Número (1..total) da questão na tela, para 'Questão 3 de 10'."""
        return min(self.indice + 1, self.total)

    @property
    def progresso(self) -> float:
        """0..1 — quanto da rodada já foi concluído (questões respondidas)."""
        if not self.total:
            return 0.0
        concluidas = self.indice + (1 if self.respondida else 0)
        return min(concluidas / self.total, 1.0)

    @property
    def respondidas(self) -> int:
        return self.acertos + len(self.erros)

    @property
    def percentual(self) -> float:
        return 0.0 if not self.respondidas else self.acertos / self.respondidas

    @property
    def estrelas(self) -> int:
        """0 a 3 estrelas conforme o aproveitamento da rodada."""
        p = self.percentual
        if p >= 0.9:
            return 3
        if p >= 0.7:
            return 2
        if p >= 0.4:
            return 1
        return 0

    # ----- ações -----
    def registrar(self, resultado: dict, escolhida_id: int) -> None:
        """Registra a resposta da questão atual. `resultado` vem de services.responder()."""
        if self.terminou or self.respondida:
            raise ValueError("A questão atual já foi respondida ou a rodada terminou.")
        if resultado["correta"]:
            self.acertos += 1
            self.pontos += resultado.get("pontos", PONTOS_POR_ACERTO)
        else:
            self.erros.append(Erro(self.questao, escolhida_id, resultado["correta_id"]))
        self.respondida = True

    def avancar(self) -> None:
        if not self.respondida:
            raise ValueError("Responda a questão antes de avançar.")
        self.indice += 1
        self.respondida = False

    def refazer_erros(self) -> "Rodada | None":
        """Nova rodada só com as questões erradas (None se não houve erros)."""
        if not self.erros:
            return None
        return Rodada(self.materia, [e.questao for e in self.erros])


def mensagem_estrelas(estrelas: int) -> str:
    return {
        3: "Incrível! Você mandou muito bem! 🏆",
        2: "Muito bom! Quase perfeito! 🎉",
        1: "Bom começo! Vamos treinar mais um pouco? 💪",
        0: "Não desanime! Tentando de novo você chega lá! 🌱",
    }[max(0, min(3, estrelas))]
