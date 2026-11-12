import flet as ft

import estado
import leitor_voz
import services
from components.utils import espaco, limpar_e_mostrar


def mostrar_exercicio(page: ft.Page, resultado: dict | None = None, escolhida_id: int | None = None,
                      erro_envio: str = ""):
    """Mostra a questão atual.

    Sem `resultado`: o aluno ainda vai responder. Com `resultado`: mostra o feedback, marcando a
    alternativa correta (verde) e a escolhida errada (vermelha), com a explicação.
    """
    from views.inicio import tela_inicio
    from views.resultado import tela_resultado

    page.scroll = ft.ScrollMode.AUTO
    rodada = estado.rodada_atual["rodada"]
    if rodada is None:
        tela_inicio(page)
        return
    if rodada.terminou:
        tela_resultado(page)
        return

    questao = rodada.questao
    if resultado is None and estado.preferencias["voz"] and not erro_envio:
        leitor_voz.falar_texto(questao["pergunta"])

    def responder(alternativa_id: int):
        try:
            res = services.responder(rodada.materia, questao, alternativa_id)
        except services.ApiError as exc:
            mostrar_exercicio(page, None, None, str(exc))
            return
        rodada.registrar(res, alternativa_id)
        mostrar_exercicio(page, res, alternativa_id)

    def continuar(e):
        rodada.avancar()
        mostrar_exercicio(page)

    def alternar_voz(e):
        estado.preferencias["voz"] = not estado.preferencias["voz"]
        mostrar_exercicio(page, resultado, escolhida_id)

    cards = [
        _card_alternativa(alt, resultado, escolhida_id, responder)
        for alt in questao["alternativas"]
    ]

    topo = ft.Row([
        ft.Text(f"Questão {rodada.numero_atual} de {rodada.total}", size=16, color=ft.Colors.GREY_700),
        ft.Text(f"⭐ Pontos: {rodada.pontos}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_600),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    controles = [
        topo,
        ft.ProgressBar(value=rodada.progresso, width=600),
        espaco(10),
        ft.Text(questao["pergunta"], size=26, weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE_900),
    ]

    if leitor_voz.disponivel():
        controles.append(ft.Row([
            ft.Button("Ouvir de novo", icon=ft.Icons.VOLUME_UP,
                      on_click=lambda e: leitor_voz.falar_texto(questao["pergunta"])),
            ft.Button("Voz ligada" if estado.preferencias["voz"] else "Voz desligada",
                      icon=ft.Icons.RECORD_VOICE_OVER, on_click=alternar_voz),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, wrap=True))

    if questao.get("imagem_pergunta"):
        controles.append(ft.Image(src=questao["imagem_pergunta"], width=350, height=250,
                                  fit=ft.BoxFit.CONTAIN))

    if erro_envio:
        controles.append(ft.Text(erro_envio, size=16, color=ft.Colors.RED_700, text_align=ft.TextAlign.CENTER))

    controles.extend([espaco(10), ft.ResponsiveRow(cards, alignment=ft.MainAxisAlignment.CENTER)])

    if resultado is not None:
        controles.extend(_bloco_feedback(resultado, rodada.ultima_questao))
        controles.append(ft.Button(
            "Ver resultado" if rodada.ultima_questao else "Próxima",
            icon=ft.Icons.ARROW_FORWARD, on_click=continuar))

    controles.extend([
        espaco(20),
        ft.Button("Voltar ao início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)),
    ])
    limpar_e_mostrar(page, controles)


def _bloco_feedback(resultado: dict, ultima: bool) -> list:
    if resultado["correta"]:
        mensagem, cor = "Acertou! 🎉  +10 pontos", ft.Colors.GREEN_700
    else:
        mensagem, cor = "Não foi desta! A resposta certa está em verde. 💪", ft.Colors.RED_700
    itens = [
        espaco(10),
        ft.Text(mensagem, size=24, color=cor, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
    ]
    if resultado.get("explicacao"):
        itens.append(ft.Text(resultado["explicacao"], size=18, text_align=ft.TextAlign.CENTER))
    if resultado.get("imagem_explicacao"):
        itens.append(ft.Image(src=resultado["imagem_explicacao"], width=300, height=200,
                              fit=ft.BoxFit.CONTAIN))
    itens.append(espaco(10))
    return itens


def _card_alternativa(alt: dict, resultado: dict | None, escolhida_id: int | None, ao_clicar):
    """Card clicável de uma alternativa; depois de responder, vira só visual (verde/vermelho)."""
    borda, fundo = ft.Colors.BLUE_200, ft.Colors.BLUE_50
    if resultado is not None:
        if alt["id"] == resultado["correta_id"]:
            borda, fundo = ft.Colors.GREEN_600, ft.Colors.GREEN_100
        elif alt["id"] == escolhida_id:
            borda, fundo = ft.Colors.RED_600, ft.Colors.RED_100
        else:
            borda, fundo = ft.Colors.GREY_300, ft.Colors.GREY_100

    conteudo = []
    if alt.get("imagem"):
        conteudo.append(ft.Image(src=alt["imagem"], width=190, height=105, fit=ft.BoxFit.CONTAIN))
    rotulo = alt.get("letra", "")
    if alt.get("texto"):
        rotulo = f"{rotulo}) {alt['texto']}" if rotulo else alt["texto"]
    if rotulo:
        conteudo.append(ft.Text(rotulo, size=18, text_align=ft.TextAlign.CENTER))

    clicavel = resultado is None
    return ft.Container(
        col={"xs": 6, "sm": 6},
        content=ft.Column(conteudo, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=10, margin=6,
        border=ft.Border.all(3 if resultado is not None and borda != ft.Colors.GREY_300 else 2, borda),
        border_radius=14, bgcolor=fundo,
        ink=clicavel,
        on_click=(lambda e, a=alt: ao_clicar(a["id"])) if clicavel else None,
    )
