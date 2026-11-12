import flet as ft


def limpar_e_mostrar(page: ft.Page, controles):
    """Troca o conteúdo da tela inteira."""
    page.controls.clear()
    page.controls.extend(controles)
    page.update()


def espaco(altura: int = 15) -> ft.Container:
    return ft.Container(height=altura)


def titulo(texto: str, tamanho: int = 30, cor=None) -> ft.Text:
    return ft.Text(texto, size=tamanho, weight=ft.FontWeight.BOLD,
                   text_align=ft.TextAlign.CENTER, color=cor)


def erro(texto: str) -> ft.Text:
    return ft.Text(texto, size=16, color=ft.Colors.RED_700, text_align=ft.TextAlign.CENTER)


def estrelas(quantidade: int, total: int = 3) -> str:
    return "⭐" * quantidade + "☆" * (total - quantidade)
