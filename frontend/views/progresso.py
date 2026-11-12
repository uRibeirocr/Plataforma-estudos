import flet as ft

from components.utils import limpar_e_mostrar


def tela_progresso(page: ft.Page):

    limpar_e_mostrar(page, [

        ft.Row(
            [
                ft.Button(
                    "Atividades",
                    on_click=lambda e: _voltar_inicio(page)
                ),

                ft.Button(
                    "Meu Progresso",
                    on_click=lambda e: tela_progresso(page)
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),

        ft.Text(
            "Meu Progresso 📊",
            size=32,
            weight=ft.FontWeight.BOLD
        ),

        ft.Container(height=20),

        ft.Text(
            "Matemática",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        ft.Text("120 pontos"),

        ft.ProgressBar(
            value=0.6,
            width=500
        ),

        ft.Container(height=20),

        ft.Text(
            "Geografia",
            size=20,
            weight=ft.FontWeight.BOLD
        ),

        ft.Text("80 pontos"),

        ft.ProgressBar(
            value=0.4,
            width=500
        ),
    ])


def _voltar_inicio(page: ft.Page):

    from views.inicio import tela_inicio

    tela_inicio(page)