import flet as ft
import estado
from components.utils import limpar_e_mostrar
from views.exercicio import mostrar_exercicio

def iniciar_materia(page: ft.Page, materia: str):
    """Prepara o jogo e chama o primeiro exercício."""
    import services
    try:
        estado.estado_atual.update({"materia": materia, "indice": 0, "questoes": services.buscar_exercicios(materia)})
        estado.pontuacao["total"] = services.meu_progresso()["pontuacao"]
        mostrar_exercicio(page)
    except services.ApiError as exc:
        limpar_e_mostrar(page, [ft.Text(str(exc), color=ft.Colors.RED_600), ft.Button("Voltar", on_click=lambda e: tela_inicio(page))])

def tela_inicio(page: ft.Page):
    from views.login import tela_login
    nome = estado.sessao.get("usuario", {}).get("name", "")

    def sair(e):
        estado.sessao.update({"token": None, "usuario": None})
        tela_login(page)

    limpar_e_mostrar(page, [
        ft.Text(f"Bem-vindo(a), {nome}! 👋", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Escolhe uma matéria para começar:", size=18),
        ft.Container(height=20),
        ft.Row(
            [
                ft.Button("Matemática", icon=ft.Icons.CALCULATE, on_click=lambda e: iniciar_materia(page, "MATEMATICA")),
                ft.Button("Geografia", icon=ft.Icons.PUBLIC, on_click=lambda e: iniciar_materia(page, "GEOGRAFIA")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        ft.Container(height=16),
        ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=sair),
    ])
