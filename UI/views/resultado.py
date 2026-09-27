import flet as ft
import estado
from components.utils import limpar_e_mostrar
from views.inicio import tela_inicio

def tela_resultado(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Você terminou! 🏆", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
        ft.Text(f"Você conquistou: {estado.pontuacao['total']} pontos!", size=24),
        ft.Container(height=30),
        ft.Button("Jogar Novamente", icon=ft.Icons.RESTART_ALT, on_click=lambda e: tela_inicio(page)),
    ])