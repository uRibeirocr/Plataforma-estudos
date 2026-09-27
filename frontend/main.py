import flet as ft
from mock_data import EXERCICIOS

# Estado simples do "jogo" (depois isso vai virar dados de verdade vindos do backend)
pontuacao = {"total": 0}
estado_atual = {"materia": None, "indice": 0}


def main(page: ft.Page):
    page.title = "Plataforma de Estudos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    tela_inicio(page)


def limpar_e_mostrar(page: ft.Page, controles):
    """Função auxiliar: limpa a tela atual e mostra uma lista nova de componentes."""
    page.controls.clear()
    page.controls.extend(controles)
    page.update()


def tela_inicio(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Bem-vindo(a)! 👋", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Escolha uma matéria para começar:", size=18),
        ft.Row(
            [
                ft.Button(
                    "Matemática",
                    icon=ft.Icons.CALCULATE,
                    on_click=lambda e: iniciar_materia(page, "MATEMATICA"),
                ),
                ft.Button(
                    "Geografia",
                    icon=ft.Icons.PUBLIC,
                    on_click=lambda e: iniciar_materia(page, "GEOGRAFIA"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    ])


def iniciar_materia(page: ft.Page, materia: str):
    estado_atual["materia"] = materia
    estado_atual["indice"] = 0
    pontuacao["total"] = 0
    mostrar_exercicio(page)


def mostrar_exercicio(page: ft.Page):
    materia = estado_atual["materia"]
    indice = estado_atual["indice"]
    lista_exercicios = EXERCICIOS[materia]

    # Acabaram os exercícios dessa matéria -> mostra resultado final
    if indice >= len(lista_exercicios):
        tela_resultado(page)
        return

    exercicio = lista_exercicios[indice]

    cards = [criar_card_alternativa(page, alt) for alt in exercicio["alternativas"]]

    limpar_e_mostrar(page, [
        ft.Row(
            [ft.Text(f"⭐ Pontos: {pontuacao['total']}", size=16, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.END,
        ),
        ft.Container(height=10),
        ft.Text(
            exercicio["pergunta"],
            size=26,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        # Aqui depois entra a imagem da pergunta (RN04/RN05), quando o Vitor mandar os assets:
        # ft.Image(src=exercicio["imagem_pergunta"], width=200, height=150),
        ft.Container(height=20),
        ft.ResponsiveRow(cards, alignment=ft.MainAxisAlignment.CENTER),
    ])


def criar_card_alternativa(page: ft.Page, alternativa: dict):
    """Monta um 'card' clicável de alternativa (RN06)."""

    def ao_clicar(e):
        verificar_resposta(page, alternativa)

    return ft.Container(
        col={"xs": 12, "sm": 6},
        content=ft.Column(
            [
                # Aqui depois entra a imagem da alternativa (RN05):
                # ft.Image(src=alternativa["imagem"], width=100, height=100),
                ft.Text(alternativa["texto"], size=20, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        margin=6,
        border=ft.Border.all(2, ft.Colors.BLUE_200),
        border_radius=14,
        bgcolor=ft.Colors.BLUE_50,
        ink=True,
        on_click=ao_clicar,
    )


def verificar_resposta(page: ft.Page, alternativa: dict):
    """RN07: identifica a alternativa escolhida, verifica se é correta, pontua (RN08)."""
    if alternativa["correta"]:
        pontuacao["total"] += 10
        mensagem = "Acertou! 🎉"
        cor = ft.Colors.GREEN
    else:
        mensagem = "Não foi essa, tenta a próxima! 💪"
        cor = ft.Colors.RED

    def continuar(e):
        estado_atual["indice"] += 1
        mostrar_exercicio(page)

    limpar_e_mostrar(page, [
        ft.Text(mensagem, size=28, color=cor, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(height=20),
        ft.Button("Continuar", icon=ft.Icons.ARROW_FORWARD, on_click=continuar),
    ])


def tela_resultado(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Você terminou! 🏆", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"Pontuação final: {pontuacao['total']} pontos", size=22),
        ft.Container(height=20),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
    ])


ft.run(main)
