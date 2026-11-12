# main.py
import flet as ft
from views.login import tela_login

def main(page: ft.Page):
    page.title = "Plataforma de Estudos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Inicia direto na tela principal, sem passar por login
    tela_login(page)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")