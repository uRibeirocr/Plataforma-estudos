# login.py
import flet as ft
import estado
from UI import tela_inicio, limpar_e_mostrar


def tela_login(page: ft.Page):
    campo_nome = ft.TextField(label="Nome", width=300)
    campo_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    tipo_selecionado = ft.Dropdown(
        label="Eu sou...",
        width=300,
        options=[
            ft.dropdown.Option("ALUNO", "Aluno"),
            ft.dropdown.Option("RESPONSAVEL", "Responsável"),
        ],
        value="ALUNO",
    )

    def entrar(e):
        if not campo_nome.value:
            campo_nome.error_text = "Digite seu nome"
            page.update()
            return
        fazer_login(page, campo_nome.value, tipo_selecionado.value)

    limpar_e_mostrar(page, [
        ft.Text("Plataforma de Estudos", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Entre para continuar", size=18),
        ft.Container(height=20),
        campo_nome,
        campo_senha,
        tipo_selecionado,
        ft.Container(height=20),
        ft.Button("Entrar", icon=ft.Icons.LOGIN, on_click=entrar),
    ])


def fazer_login(page: ft.Page, nome: str, tipo: str):
    """Por enquanto não valida senha de verdade — isso vem do backend (Jojo) depois."""
    estado.usuario["nome"] = nome
    estado.usuario["tipo"] = tipo

    if tipo == "RESPONSAVEL":
        tela_progresso_responsavel(page)
    else:
        tela_inicio(page)


def tela_progresso_responsavel(page: ft.Page):
    """RN01: Responsável só visualiza o progresso, não responde exercícios."""
    limpar_e_mostrar(page, [
        ft.Text(f"Olá, {estado.usuario['nome']}!", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Aqui você vai acompanhar o progresso dos alunos vinculados.", size=16),
        ft.Container(height=20),
        ft.Text("(Em construção — depende dos dados reais do backend, RN11)", italic=True),
        ft.Container(height=20),
        ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=lambda e: sair(page)),
    ])


def sair(page: ft.Page):
    estado.usuario["nome"] = None
    estado.usuario["tipo"] = None
    tela_login(page)
