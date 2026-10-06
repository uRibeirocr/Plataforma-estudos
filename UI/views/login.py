import flet as ft

import estado
import services
from components.utils import limpar_e_mostrar


def abrir_inicio(page):
    if estado.sessao["usuario"]["role"] == "RESPONSAVEL":
        tela_responsavel(page)
    else:
        from views.inicio import tela_inicio
        tela_inicio(page)


def tela_login(page):
    cadastro = {"ativo": False}
    nome = ft.TextField(label="Nome", width=320)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320)
    tipo = ft.Dropdown(label="Eu sou...", width=320, value="ALUNO", visible=False,
                       options=[ft.dropdown.Option("ALUNO", "Aluno"), ft.dropdown.Option("RESPONSAVEL", "Responsável")])
    aviso = ft.Text(color=ft.Colors.RED_600, width=320)
    botao = ft.Button("Entrar", icon=ft.Icons.LOGIN)
    alternar = ft.TextButton("Ainda não tenho conta")

    def enviar(e):
        if not nome.value or not senha.value:
            aviso.value = "Preencha nome e senha."
            page.update()
            return
        try:
            resposta = services.cadastrar(nome.value.strip(), senha.value, tipo.value) if cadastro["ativo"] else services.entrar(nome.value.strip(), senha.value)
            estado.sessao.update({"token": resposta["token"], "usuario": resposta["user"]})
            abrir_inicio(page)
        except services.ApiError as exc:
            aviso.value = str(exc)
            page.update()

    def mudar_modo(e):
        cadastro["ativo"] = not cadastro["ativo"]
        tipo.visible = cadastro["ativo"]
        botao.text = "Criar conta" if cadastro["ativo"] else "Entrar"
        alternar.text = "Já tenho uma conta" if cadastro["ativo"] else "Ainda não tenho conta"
        aviso.value = ""
        page.update()

    botao.on_click = enviar
    alternar.on_click = mudar_modo
    limpar_e_mostrar(page, [
        ft.Image(src="logo.png", width=120, height=120),
        ft.Text("Plataforma de Estudos", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Entre ou crie uma conta para estudar"), ft.Container(height=16),
        nome, senha, tipo, aviso, botao, alternar,
    ])


def tela_responsavel(page):
    campo_id = ft.TextField(label="ID do aluno para vincular", width=320, keyboard_type=ft.KeyboardType.NUMBER)
    aviso = ft.Text(color=ft.Colors.RED_600)
    lista = ft.Column(spacing=8)

    def atualizar(e=None):
        try:
            alunos = services.alunos_vinculados()
            lista.controls = [ft.Text(f"{item['nome']} (ID {item['id']})") for item in alunos] or [ft.Text("Nenhum aluno vinculado ainda.")]
            aviso.value = ""
        except services.ApiError as exc:
            aviso.value = str(exc)
        page.update()

    def vincular(e):
        try:
            services.vincular_aluno(campo_id.value)
            campo_id.value = ""
            atualizar()
        except (ValueError, services.ApiError) as exc:
            aviso.value = "Informe um ID de aluno válido." if isinstance(exc, ValueError) else str(exc)
            page.update()

    def sair(e):
        estado.sessao.update({"token": None, "usuario": None})
        tela_login(page)

    limpar_e_mostrar(page, [
        ft.Text(f"Olá, {estado.sessao['usuario']['name']}!", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Acompanhe os alunos vinculados."), campo_id,
        ft.Button("Vincular aluno", icon=ft.Icons.PERSON_ADD, on_click=vincular),
        aviso, lista, ft.Button("Atualizar", icon=ft.Icons.REFRESH, on_click=atualizar),
        ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=sair),
    ])
    atualizar()
