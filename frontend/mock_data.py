# Dados mockados (fake), no formato que devem vir do backend (Spring Boot) no futuro.
# Estrutura baseada nas entidades Exercicio e Alternativa do diagrama.

EXERCICIOS = {
    "MATEMATICA": [
        {
            "id": 1,
            "pergunta": "Quanto é 3 x 4?",
            "imagem_pergunta": None,  # depois vira a URL/caminho da imagem
            "alternativas": [
                {"id": 1, "texto": "10", "correta": False},
                {"id": 2, "texto": "12", "correta": True},
                {"id": 3, "texto": "14", "correta": False},
                {"id": 4, "texto": "7", "correta": False},
            ],
        },
        {
            "id": 2,
            "pergunta": "Quanto é 5 x 6?",
            "imagem_pergunta": None,
            "alternativas": [
                {"id": 1, "texto": "30", "correta": True},
                {"id": 2, "texto": "35", "correta": False},
                {"id": 3, "texto": "25", "correta": False},
                {"id": 4, "texto": "11", "correta": False},
            ],
        },
        {
            "id": 3,
            "pergunta": "Quanto é 7 x 8?",
            "imagem_pergunta": None,
            "alternativas": [
                {"id": 1, "texto": "54", "correta": False},
                {"id": 2, "texto": "56", "correta": True},
                {"id": 3, "texto": "48", "correta": False},
                {"id": 4, "texto": "64", "correta": False},
            ],
        },
    ],
    "GEOGRAFIA": [
        {
            "id": 1,
            "pergunta": "Qual dessas é a bandeira do Brasil?",
            "imagem_pergunta": None,
            "alternativas": [
                {"id": 1, "texto": "🇧🇷 Brasil", "correta": True},
                {"id": 2, "texto": "🇦🇷 Argentina", "correta": False},
                {"id": 3, "texto": "🇵🇹 Portugal", "correta": False},
                {"id": 4, "texto": "🇺🇾 Uruguai", "correta": False},
            ],
        },
        {
            "id": 2,
            "pergunta": "Qual dessas é a bandeira do Japão?",
            "imagem_pergunta": None,
            "alternativas": [
                {"id": 1, "texto": "🇯🇵 Japão", "correta": True},
                {"id": 2, "texto": "🇰🇷 Coreia do Sul", "correta": False},
                {"id": 3, "texto": "🇨🇳 China", "correta": False},
                {"id": 4, "texto": "🇹🇭 Tailândia", "correta": False},
            ],
        },
    ],
}

# Quando o backend do Jojo estiver pronto, a ideia é criar um services.py
# com uma função buscar_exercicios(materia) que troca esse dicionário
# por uma chamada real, tipo: requests.get(f"http://localhost:8080/exercicios/{materia}").json()
