# teste_login.py  (arquivo só para teste local, não precisa subir pro GitHub)
import flet as ft
from views.login import tela_login


def main(page: ft.Page):
    page.title = "Teste da tela de login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    tela_login(page)


ft.run(main, assets_dir="assets")
