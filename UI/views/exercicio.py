import flet as ft
import estado
import services
from components.utils import limpar_e_mostrar
from leitor_voz import falar_texto

def mostrar_exercicio(page: ft.Page):
    from views.resultado import tela_resultado
    from views.inicio import tela_inicio

    page.scroll = ft.ScrollMode.AUTO

    materia = estado.estado_atual["materia"]
    indice = estado.estado_atual["indice"]
    lista_exercicios = services.buscar_exercicios(materia)

    if indice >= len(lista_exercicios):
        tela_resultado(page)
        return

    exercicio = lista_exercicios[indice]
    
    # ==========================================
    #   CHAMA A VOZ PARA LER A PERGUNTA ATUAL
    # ==========================================
    falar_texto(exercicio["pergunta"])

    cards = [criar_card_alternativa(page, alt) for alt in exercicio["alternativas"]]
    
    # ... (o resto do seu código de componentes_tela continua exatamente igual a partir daqui) ...
    componentes_tela = [
        ft.Row([ft.Text(f"⭐ Pontos: {estado.pontuacao['total']}", size=18,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_600)],
               alignment=ft.MainAxisAlignment.END),
        ft.Container(height=10),
        ft.Text(exercicio["pergunta"], size=26, weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE_900),
        ft.Container(height=15),
    ]
    
    cards = [criar_card_alternativa(page, alt) for alt in exercicio["alternativas"]]
    componentes_tela = [
        ft.Row([ft.Text(f"⭐ Pontos: {estado.pontuacao['total']}", size=18,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_600)],
               alignment=ft.MainAxisAlignment.END),
        ft.Container(height=10),
        ft.Text(exercicio["pergunta"], size=26, weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE_900),
        ft.Container(height=15),
    ]
    if exercicio.get("imagem_pergunta"):
        componentes_tela.append(
            ft.Image(src=exercicio["imagem_pergunta"], width=350, height=250,
                     fit=ft.BoxFit.CONTAIN)
        )
    componentes_tela.extend([
        ft.Container(height=20),
        ft.ResponsiveRow(cards, alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=30),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME,
                  on_click=lambda e: tela_inicio(page)),
    ])
    limpar_e_mostrar(page, componentes_tela)


def criar_card_alternativa(page: ft.Page, alternativa: dict):
    """Mostra a imagem da alternativa já ligada ao gabarito do mock."""
    conteudo = []
    if alternativa.get("imagem"):
        conteudo.append(ft.Image(src=alternativa["imagem"], width=190,
                                height=105, fit=ft.BoxFit.CONTAIN))
    # Geografia mostra só a letra para não revelar o país antes da resposta.
    rotulo = alternativa.get("texto") or alternativa.get("letra", "")
    if rotulo:
        conteudo.append(ft.Text(rotulo, size=18,
                                text_align=ft.TextAlign.CENTER))
    return ft.Container(
        col={"xs": 6, "sm": 6},
        content=ft.Column(conteudo,
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=10, margin=6,
        border=ft.Border.all(2, ft.Colors.BLUE_200),
        border_radius=14, bgcolor=ft.Colors.BLUE_50,
        ink=True, on_click=lambda e: verificar_resposta(page, alternativa),
    )


def verificar_resposta(page: ft.Page, alternativa: dict):
    if alternativa["correta"]:
        estado.pontuacao["total"] += 10
        mensagem, cor = "Acertou! 🎉", ft.Colors.GREEN
    else:
        mensagem, cor = "Não foi desta, tenta a próxima! 💪", ft.Colors.RED

    def continuar(e):
        estado.estado_atual["indice"] += 1
        mostrar_exercicio(page)

    controles = [
        ft.Text(mensagem, size=28, color=cor, weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER),
    ]
    exercicio = services.buscar_exercicios(estado.estado_atual["materia"])[estado.estado_atual["indice"]]
    if exercicio.get("explicacao"):
        controles.append(ft.Text(exercicio["explicacao"], size=17,
                                  text_align=ft.TextAlign.CENTER))
    controles.extend([
        ft.Container(height=20),
        ft.Button("Continuar", icon=ft.Icons.ARROW_FORWARD, on_click=continuar),
    ])
    limpar_e_mostrar(page, controles)
