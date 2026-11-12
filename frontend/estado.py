"""Estado compartilhado entre as telas (sessão, rodada em andamento, preferências)."""

# Sessão: preenchida no login. "offline" = jogando sem API (nada é salvo no servidor).
sessao = {"token": None, "usuario": None, "offline": False}

# Rodada em andamento (objeto rodada.Rodada) e matéria escolhida.
rodada_atual = {"rodada": None}

# Progresso local, usado só no modo offline: {"MATEMATICA": {"respondidas":..,"acertos":..,"pontos":..}}
progresso_local = {}

# Preferências do aluno.
preferencias = {"voz": True, "quantidade": 10}


def usuario() -> dict:
    return sessao.get("usuario") or {}


def esta_logado() -> bool:
    return sessao.get("usuario") is not None


def encerrar_sessao():
    sessao.update({"token": None, "usuario": None, "offline": False})
    rodada_atual["rodada"] = None
    progresso_local.clear()
