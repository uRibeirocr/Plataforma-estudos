# ui.py
import flet as ft
import estado
import services

def limpar_e_mostrar(page: ft.Page, controles):
    page.controls.clear()
    page.controls.extend(controles)
    page.update()

def tela_inicio(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Bem-vindo(a)! 👋", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Escolha uma matéria para começar:", size=18),
        ft.Row(
            [
                ft.Button("Matemática", icon=ft.Icons.CALCULATE, on_click=lambda e: iniciar_materia(page, "MATEMATICA")),
                ft.Button("Geografia", icon=ft.Icons.PUBLIC, on_click=lambda e: iniciar_materia(page, "GEOGRAFIA")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
    ])

def iniciar_materia(page: ft.Page, materia: str):
    estado.estado_atual["materia"] = materia
    estado.estado_atual["indice"] = 0
    estado.pontuacao["total"] = 0
    mostrar_exercicio(page)

def mostrar_exercicio(page: ft.Page):
    materia = estado.estado_atual["materia"]
    indice = estado.estado_atual["indice"]
    
    # Busca os dados usando o Service, e não o mock direto
    lista_exercicios = services.buscar_exercicios(materia)

    if indice >= len(lista_exercicios):
        tela_resultado(page)
        return

    exercicio = lista_exercicios[indice]
    cards = [criar_card_alternativa(page, alt) for alt in exercicio["alternativas"]]

    limpar_e_mostrar(page, [
        ft.Row([ft.Text(f"⭐ Pontos: {estado.pontuacao['total']}", size=16, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.END),
        ft.Container(height=10),
        ft.Text(exercicio["pergunta"], size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(height=20),
        ft.ResponsiveRow(cards, alignment=ft.MainAxisAlignment.CENTER),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
    ])

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
        mensagem = "Não foi essa, tenta a próxima! 💪"
        cor = ft.Colors.RED

    def continuar(e):
        estado.estado_atual["indice"] += 1
        mostrar_exercicio(page)

    limpar_e_mostrar(page, [
        ft.Text(mensagem, size=28, color=cor, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        ft.Container(height=20),
        ft.Button("Continuar", icon=ft.Icons.ARROW_FORWARD, on_click=continuar),
    ])

def tela_resultado(page: ft.Page):
    limpar_e_mostrar(page, [
        ft.Text("Você terminou! 🏆", size=32, weight=ft.FontWeight.BOLD),
        ft.Text(f"Pontuação final: {estado.pontuacao['total']} pontos", size=22),
        ft.Container(height=20),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
    ])