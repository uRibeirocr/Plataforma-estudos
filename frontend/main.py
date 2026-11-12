"""Ponto de entrada do app Flet:  python main.py  (de dentro da pasta frontend)."""
import flet as ft

import config
from views.login import tela_login


def main(page: ft.Page):
    page.title = "Pratica+"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    tela_login(page)


if __name__ == "__main__":
    ft.run(main, assets_dir=str(config.PASTA_ASSETS))
