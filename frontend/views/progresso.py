import flet as ft

import config
import estado
import services
from components.utils import erro, espaco, limpar_e_mostrar, titulo


def cartao_progresso(p: dict) -> ft.Control:
    """Bloco de uma matéria (usado pelo aluno e pelo responsável)."""
    info = config.MATERIAS.get(p["materia"], {"titulo": p["materia"], "emoji": "📘"})
    dominados, total = p["exerciciosDominados"], p["totalExercicios"]
    return ft.Container(
        content=ft.Column([
            ft.Text(f"{info['emoji']}  {info['titulo']}", size=22, weight=ft.FontWeight.BOLD),
            ft.Text(f"⭐ {p['pontuacao']} pontos", size=18),
            ft.Text(f"Exercícios dominados: {dominados} de {total}", size=16),
            ft.ProgressBar(value=min(p["percentualConclusao"] / 100, 1.0), width=500),
            ft.Text(f"Acertos: {p['tentativasCorretas']}   Erros: {p['tentativasErradas']}   "
                    f"Aproveitamento: {round(p['percentualAcertos'])}%", size=14,
                    color=ft.Colors.GREY_700),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
        padding=15, margin=8, border=ft.Border.all(2, ft.Colors.BLUE_200),
        border_radius=14, bgcolor=ft.Colors.BLUE_50,
    )


def tela_progresso(page: ft.Page):
    from views.inicio import barra_navegacao

    page.scroll = ft.ScrollMode.AUTO
    controles = [barra_navegacao(page), espaco(10), titulo("Meu Progresso 📊", 32), espaco(10)]
    try:
        dados = services.meu_progresso()
    except services.ApiError as exc:
        controles.append(erro(str(exc)))
    else:
        controles.extend(cartao_progresso(p) for p in dados)
        if estado.sessao.get("offline"):
            controles.append(ft.Text("Modo offline: este progresso vale só enquanto o app estiver aberto.",
                                     size=14, color=ft.Colors.GREY_600))
    limpar_e_mostrar(page, controles)
