import flet as ft

def limpar_e_mostrar(page: ft.Page, controles):
    page.controls.clear()
    page.controls.extend(controles)
    page.update()