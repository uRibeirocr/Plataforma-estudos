import flet as ft

import config
import estado
import services
from components.utils import erro, espaco, limpar_e_mostrar, titulo
from rodada import Rodada


def iniciar_materia(page: ft.Page, materia: str, quantidade):
    """Monta uma rodada e abre o primeiro exercício."""
    from views.exercicio import mostrar_exercicio

    try:
        questoes = services.montar_rodada(materia, quantidade)
    except services.ApiError as exc:
        tela_inicio(page, str(exc))
        return
    estado.rodada_atual["rodada"] = Rodada(materia, questoes)
    mostrar_exercicio(page)


def barra_navegacao(page: ft.Page) -> ft.Row:
    from views.login import sair
    from views.progresso import tela_progresso

    return ft.Row([
        ft.Button("Atividades", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
        ft.Button("Meu Progresso", icon=ft.Icons.BAR_CHART, on_click=lambda e: tela_progresso(page)),
        ft.Button("Sair", icon=ft.Icons.LOGOUT, on_click=lambda e: sair(page)),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True)


def tela_inicio(page: ft.Page, mensagem_erro: str = ""):
    page.scroll = ft.ScrollMode.AUTO
    nome = estado.usuario().get("nome", "")

    quantidade = ft.Dropdown(
        label="Quantas questões?",
        width=220,
        options=[ft.dropdown.Option(texto, texto) for texto, _ in config.OPCOES_QUANTIDADE],
        value=_texto_quantidade(estado.preferencias["quantidade"]),
    )

    def escolher(materia: str):
        valor = dict(config.OPCOES_QUANTIDADE)[quantidade.value]
        estado.preferencias["quantidade"] = valor
        iniciar_materia(page, materia, valor)

    botoes = [
        ft.Button(f"{info['emoji']}  {info['titulo']}", on_click=lambda e, m=materia: escolher(m))
        for materia, info in config.MATERIAS.items()
    ]

    limpar_e_mostrar(page, [
        barra_navegacao(page),
        espaco(15),
        titulo(f"Olá, {nome}! 👋", 32),
        ft.Text("Escolha uma matéria para começar:", size=18),
        espaco(10),
        quantidade,
        espaco(10),
        ft.Row(botoes, alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
        espaco(10),
        erro(mensagem_erro) if mensagem_erro else ft.Container(),
        ft.Text("Cada acerto vale 10 pontos. Errou? Sem problema, ninguém perde pontos!", size=14,
                color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
    ])


def _texto_quantidade(valor) -> str:
    for texto, v in config.OPCOES_QUANTIDADE:
        if v == valor:
            return texto
    return str(config.QUANTIDADE_PADRAO)
