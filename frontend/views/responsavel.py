import flet as ft

import estado
import services
from components.utils import erro, espaco, limpar_e_mostrar, titulo
from views.progresso import cartao_progresso


def tela_responsavel(page: ft.Page, mensagem: str = "", mensagem_erro: str = ""):
    """RN01: o responsável só acompanha o progresso dos alunos vinculados, não responde exercícios."""
    from views.login import sair

    page.scroll = ft.ScrollMode.AUTO
    campo_aluno = ft.TextField(label="Nome do aluno para vincular", width=300)

    def vincular(e):
        nome = (campo_aluno.value or "").strip()
        if not nome:
            campo_aluno.error_text = "Digite o nome do aluno"
            page.update()
            return
        try:
            services.vincular_aluno(nome)
        except services.ApiError as exc:
            tela_responsavel(page, mensagem_erro=str(exc))
            return
        tela_responsavel(page, mensagem=f"{nome} foi vinculado(a) com sucesso!")

    controles = [
        ft.Row([ft.Button("Atualizar", icon=ft.Icons.REFRESH, on_click=lambda e: tela_responsavel(page)),
                ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=lambda e: sair(page))],
               alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        espaco(10),
        titulo(f"Olá, {estado.usuario().get('nome', '')}!", 28),
        ft.Text("Acompanhe aqui o progresso dos alunos vinculados.", size=16),
        espaco(10),
        ft.Row([campo_aluno, ft.Button("Vincular", icon=ft.Icons.LINK, on_click=vincular)],
               alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True),
    ]
    if mensagem:
        controles.append(ft.Text(mensagem, size=16, color=ft.Colors.GREEN_700))
    if mensagem_erro:
        controles.append(erro(mensagem_erro))
    controles.append(espaco(10))

    try:
        alunos = services.alunos_vinculados()
        if not alunos:
            controles.append(ft.Text("Nenhum aluno vinculado ainda.", italic=True))
        for aluno in alunos:
            controles.append(ft.Text(f"👦 {aluno['nome']}", size=24, weight=ft.FontWeight.BOLD))
            controles.extend(cartao_progresso(p) for p in services.progresso_do_aluno(aluno["id"]))
    except services.ApiError as exc:
        controles.append(erro(str(exc)))

    limpar_e_mostrar(page, controles)
