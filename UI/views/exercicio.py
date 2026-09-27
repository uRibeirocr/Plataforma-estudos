import flet as ft
import estado
import services
from components.utils import limpar_e_mostrar

def mostrar_exercicio(page: ft.Page):
    from views.resultado import tela_resultado # Importação local para evitar import circular
    from views.inicio import tela_inicio       # Importação local

    materia = estado.estado_atual["materia"]
    indice = estado.estado_atual["indice"]
    
    lista_exercicios = services.buscar_exercicios(materia)

    # Verifica se os exercícios acabaram
    if indice >= len(lista_exercicios):
        tela_resultado(page)
        return

    exercicio = lista_exercicios[indice]
    cards = [criar_card_alternativa(page, alt) for alt in exercicio["alternativas"]]

    # Monta a parte superior (Pontuação e Pergunta)
    componentes_tela = [
        ft.Row([ft.Text(f"⭐ Pontos: {estado.pontuacao['total']}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_600)], alignment=ft.MainAxisAlignment.END),
        ft.Container(height=10),
        ft.Text(exercicio["pergunta"], size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE_900),
        ft.Container(height=15),
    ]

    # Adiciona a imagem de forma dinâmica, caso exista na base de dados
    if exercicio.get("imagem_pergunta"):
        componentes_tela.append(
            ft.Image(
                src=exercicio["imagem_pergunta"], 
                width=350,
                height=250,
                fit="contain",
            )
        )

    # Monta a grelha de alternativas e o botão de voltar
    componentes_tela.extend([
        ft.Container(height=20),
        ft.ResponsiveRow(cards, alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=30),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
    ])

    limpar_e_mostrar(page, componentes_tela)


def criar_card_alternativa(page: ft.Page, alternativa: dict):
    def ao_clicar(e):
        verificar_resposta(page, alternativa)

    return ft.Container(
        col={"xs": 12, "sm": 6},
        content=ft.Column(
            [ft.Text(alternativa["texto"], size=20, text_align=ft.TextAlign.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20, margin=6,
        border=ft.Border.all(2, ft.Colors.BLUE_200),
        border_radius=14, bgcolor=ft.Colors.BLUE_50,
        ink=True, on_click=ao_clicar,
    )


def verificar_resposta(page: ft.Page, alternativa: dict):
    if alternativa["correta"]:
        estado.pontuacao["total"] += 10
        mensagem = "Acertou! 🎉"
        cor = ft.Colors.GREEN
    else:
        mensagem = "Não foi desta, tenta a próxima! 💪"
        cor = ft.Colors.RED

    def continuar(e):
        estado.estado_atual["indice"] += 1
        mostrar_exercicio(page)

    limpar_e_mostrar(page, [
        ft.Text(mensagem, size=28, color=cor, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(height=20),
        ft.Button("Continuar", icon=ft.Icons.ARROW_FORWARD, on_click=continuar),
    ])