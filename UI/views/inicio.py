import flet as ft
import estado
from components.utils import limpar_e_mostrar
from views.exercicio import mostrar_exercicio

def iniciar_materia(page: ft.Page, materia: str):
    """Prepara o jogo e chama o primeiro exercício."""
    estado.estado_atual["materia"] = materia
    estado.estado_atual["indice"] = 0
    estado.pontuacao["total"] = 0
    mostrar_exercicio(page)

def tela_inicio(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Bem-vindo(a)! 👋", size=32, weight=ft.FontWeight.BOLD),
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
    ])