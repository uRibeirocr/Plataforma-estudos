import flet as ft

import estado
from components.utils import espaco, estrelas, limpar_e_mostrar, titulo
from rodada import mensagem_estrelas


def tela_resultado(page: ft.Page):
    from views.exercicio import mostrar_exercicio
    from views.inicio import iniciar_materia, tela_inicio

    page.scroll = ft.ScrollMode.AUTO
    rodada = estado.rodada_atual["rodada"]
    if rodada is None:
        tela_inicio(page)
        return

    refazer = rodada.refazer_erros()

    def jogar_erros(e):
        estado.rodada_atual["rodada"] = refazer
        mostrar_exercicio(page)

    controles = [
        titulo("Você terminou! 🏆", 36, ft.Colors.GREEN_700),
        ft.Text(estrelas(rodada.estrelas), size=44),
        ft.Text(mensagem_estrelas(rodada.estrelas), size=20, text_align=ft.TextAlign.CENTER),
        espaco(10),
        ft.Text(f"Você conquistou {rodada.pontos} pontos!", size=24),
        ft.Text(f"Acertos: {rodada.acertos} de {rodada.respondidas} "
                f"({round(rodada.percentual * 100)}%)", size=18),
    ]

    if rodada.erros:
        controles.extend([espaco(15), ft.Text("Para revisar:", size=20, weight=ft.FontWeight.BOLD)])
        for erro in rodada.erros:
            certa = next((a for a in erro.questao["alternativas"] if a["id"] == erro.correta_id), None)
            resposta = ""
            if certa:
                resposta = " ".join(p for p in (certa.get("letra"), certa.get("texto")) if p)
            controles.append(ft.Text(f"• {erro.questao['pergunta']}  →  resposta certa: {resposta}",
                                     size=16, text_align=ft.TextAlign.CENTER))

    botoes = []
    if refazer:
        botoes.append(ft.Button(f"Refazer os {len(refazer.questoes)} erros", icon=ft.Icons.REPLAY,
                                on_click=jogar_erros))
    botoes.append(ft.Button("Nova rodada", icon=ft.Icons.RESTART_ALT,
                            on_click=lambda e: iniciar_materia(page, rodada.materia,
                                                               estado.preferencias["quantidade"])))
    botoes.append(ft.Button("Início", icon=ft.Icons.HOME, on_click=lambda e: tela_inicio(page)))

    controles.extend([espaco(25),
                      ft.Row(botoes, alignment=ft.MainAxisAlignment.CENTER, spacing=15, wrap=True)])
    limpar_e_mostrar(page, controles)
