import flet as ft
import estado
import services
from components.utils import limpar_e_mostrar


def abrir_inicio(page):
    if estado.sessao["usuario"]["role"] == "GUARDIAN":
        tela_responsavel(page)
    else:
        from views.inicio import tela_inicio
        tela_inicio(page)


def tela_login(page):
    modo_cadastro = {"ativo": False}
    nome = ft.TextField(label="Nome", width=320, visible=False)
    email = ft.TextField(label="E-mail", width=320)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=320)
    tipo = ft.Dropdown(label="Eu sou...", width=320, value="ALUNO", visible=False,
                       options=[ft.dropdown.Option("ALUNO", "Aluno"), ft.dropdown.Option("RESPONSAVEL", "Responsável")])
    erro = ft.Text(color=ft.Colors.RED_600)
    botao = ft.Button("Entrar", icon=ft.Icons.LOGIN)
    alternar = ft.TextButton("Ainda não tenho conta")

    def enviar(e):
        try:
            if modo_cadastro["ativo"]:
                resposta = services.cadastrar(nome.value or "", email.value or "", senha.value or "", tipo.value)
            else:
                resposta = services.entrar(email.value or "", senha.value or "")
            estado.sessao.update({"token": resposta["token"], "usuario": resposta["user"]})
            abrir_inicio(page)
        except services.ApiError as exc:
            erro.value = str(exc)
            page.update()

    def mudar_modo(e):
        modo_cadastro["ativo"] = not modo_cadastro["ativo"]
        nome.visible = modo_cadastro["ativo"]
        tipo.visible = modo_cadastro["ativo"]
        botao.text = "Criar conta" if modo_cadastro["ativo"] else "Entrar"
        alternar.text = "Já tenho conta" if modo_cadastro["ativo"] else "Ainda não tenho conta"
        erro.value = ""
        page.update()

    botao.on_click = enviar
    alternar.on_click = mudar_modo
    limpar_e_mostrar(page, [ft.Text("Plataforma de Estudos", size=32, weight=ft.FontWeight.BOLD), ft.Text("Entre ou crie uma conta para estudar"), ft.Container(height=16), nome, email, senha, tipo, erro, botao, alternar])


def tela_responsavel(page):
    campo = ft.TextField(label="E-mail do aluno para vincular", width=320)
    aviso = ft.Text(color=ft.Colors.RED_600)
    lista = ft.Column(spacing=10)

    def atualizar(e=None):
        try:
            alunos = services.alunos_vinculados()
            lista.controls = [ft.Text(f"{item['aluno']['name']}: {item['progresso']['pontuacao']} pontos | {item['progresso']['acertos']} acertos") for item in alunos] or [ft.Text("Nenhum aluno vinculado ainda.")]
            aviso.value = ""
        except services.ApiError as exc:
            aviso.value = str(exc)
        page.update()

    def vincular(e):
        try:
            services.vincular_aluno(campo.value or "")
            campo.value = ""
            atualizar()
        except services.ApiError as exc:
            aviso.value = str(exc)
            page.update()

    def sair(e):
        estado.sessao.update({"token": None, "usuario": None})
        tela_login(page)

    limpar_e_mostrar(page, [ft.Text(f"Olá, {estado.sessao['usuario']['name']}!", size=28, weight=ft.FontWeight.BOLD), ft.Text("Acompanhe os alunos vinculados."), campo, ft.Button("Vincular aluno", icon=ft.Icons.PERSON_ADD, on_click=vincular), aviso, lista, ft.Button("Atualizar", icon=ft.Icons.REFRESH, on_click=atualizar), ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=sair)])
    atualizar()
