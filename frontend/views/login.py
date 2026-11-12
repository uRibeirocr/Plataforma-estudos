import flet as ft

import estado
import services
from components.utils import espaco, limpar_e_mostrar, titulo


def tela_login(page: ft.Page, mensagem_erro: str = ""):
    page.scroll = ft.ScrollMode.AUTO
    campo_nome = ft.TextField(label="Nome", width=300)
    campo_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    tipo = ft.Dropdown(
        label="Eu sou...",
        width=300,
        options=[
            ft.dropdown.Option("ALUNO", "Aluno"),
            ft.dropdown.Option("RESPONSAVEL", "Responsável"),
        ],
        value="ALUNO",
    )
    aviso = ft.Text(mensagem_erro, size=16, color=ft.Colors.RED_700, text_align=ft.TextAlign.CENTER)

    def validar() -> bool:
        campo_nome.error_text = None if campo_nome.value and campo_nome.value.strip() else "Digite seu nome"
        campo_senha.error_text = None if campo_senha.value else "Digite sua senha"
        page.update()
        return not (campo_nome.error_text or campo_senha.error_text)

    def entrar(e):
        if not validar():
            return
        try:
            services.entrar(campo_nome.value.strip(), campo_senha.value)
        except services.ApiError as exc:
            aviso.value = str(exc)
            page.update()
            return
        _ir_para_inicio(page)

    def criar_conta(e):
        if not validar():
            return
        try:
            services.cadastrar(campo_nome.value.strip(), campo_senha.value, tipo.value)
        except services.ApiError as exc:
            aviso.value = str(exc)
            page.update()
            return
        _ir_para_inicio(page)

    def jogar_offline(e):
        services.entrar_offline(campo_nome.value.strip() if campo_nome.value else "")
        _ir_para_inicio(page)

    limpar_e_mostrar(page, [
        ft.Image(src="logo.png", width=160, height=160),
        titulo("Pratica+", 32),
        ft.Text("Entre para continuar", size=18),
        espaco(15),
        campo_nome,
        campo_senha,
        tipo,
        aviso,
        espaco(10),
        ft.Row([
            ft.Button("Entrar", icon=ft.Icons.LOGIN, on_click=entrar),
            ft.Button("Criar conta", icon=ft.Icons.PERSON_ADD, on_click=criar_conta),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
        espaco(5),
        ft.Button("Jogar sem conta (offline)", icon=ft.Icons.PLAY_ARROW, on_click=jogar_offline),
        ft.Text("No modo offline o progresso não é salvo no servidor.", size=13,
                color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
    ])


def _ir_para_inicio(page: ft.Page):
    from views.inicio import tela_inicio
    from views.responsavel import tela_responsavel

    if estado.usuario().get("tipo") == "RESPONSAVEL":
        tela_responsavel(page)
    else:
        tela_inicio(page)


def sair(page: ft.Page):
    estado.encerrar_sessao()
    tela_login(page)
