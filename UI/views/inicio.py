import flet as ft

import estado
import services
from components.utils import limpar_e_mostrar
from views.exercicio import mostrar_exercicio


def iniciar_materia(page: ft.Page, materia: str):
    try:
        estado.estado_atual.update({"materia": materia, "indice": 0, "questoes": services.buscar_exercicios(materia)})
        progresso = services.obter_progresso(estado.sessao["usuario"]["id"], estado.estado_atual["materia_id"])
        estado.pontuacao["total"] = progresso["pontuacao"]
        mostrar_exercicio(page)
    except services.ApiError as exc:
        limpar_e_mostrar(page, [ft.Text(str(exc), color=ft.Colors.RED_600), ft.Button("Voltar", on_click=lambda e: tela_inicio(page))])


def tela_inicio(page: ft.Page):
    from views.login import tela_login
    nome = estado.sessao.get("usuario", {}).get("name", "")

    def sair(e):
        estado.sessao.update({"token": None, "usuario": None})
        tela_login(page)

    def progresso(e):
        try:
            dados = services.meu_progresso()
            controles = [ft.Text("Meu progresso", size=30, weight=ft.FontWeight.BOLD)]
            for materia, item in dados.items():
                controles.append(ft.Text(f"{materia.title()}: {item['pontuacao']} pontos | {item['tentativasCorretas']} acertos em {item['tentativasRespondidas']} tentativas"))
            controles.append(ft.Button("Voltar", icon=ft.Icons.ARROW_BACK, on_click=lambda e: tela_inicio(page)))
            limpar_e_mostrar(page, controles)
        except services.ApiError as exc:
            limpar_e_mostrar(page, [ft.Text(str(exc), color=ft.Colors.RED_600), ft.Button("Voltar", on_click=lambda e: tela_inicio(page))])

    limpar_e_mostrar(page, [
        ft.Text(f"Bem-vindo(a), {nome}! 👋", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Escolha uma matéria para começar:", size=18), ft.Container(height=20),
        ft.Row([
            ft.Button("Matemática", icon=ft.Icons.CALCULATE, on_click=lambda e: iniciar_materia(page, "MATEMATICA")),
            ft.Button("Geografia", icon=ft.Icons.PUBLIC, on_click=lambda e: iniciar_materia(page, "GEOGRAFIA")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ft.Container(height=16), ft.Button("Meu progresso", icon=ft.Icons.BAR_CHART, on_click=progresso),
        ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=sair),
    ])
