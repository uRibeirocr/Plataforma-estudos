# Dados mockados (fake), no formato que devem vir do backend (Spring Boot) no futuro.
# Estrutura baseada nas entidades Exercicio e Alternativa do diagrama.
# mock_data.py
EXERCICIOS = {
    "MATEMATICA": [
        {
            "id": 1,
            "pergunta": "Quantos carros temos no total na imagem?",
            "imagem_pergunta": "varios_carros.png", #
            "alternativas": [
                {"id": 1, "texto": "10", "correta": False},
                {"id": 2, "texto": "15", "correta": True},
                {"id": 3, "texto": "12", "correta": False},
                {"id": 4, "texto": "20", "correta": False},
            ],
        },
        {
            "id": 2,
            "pergunta": "Quantos macaquinhos estão a dormir?",
            "imagem_pergunta": "5_macacos.png", #
            "alternativas": [
                {"id": 1, "texto": "3", "correta": False},
                {"id": 2, "texto": "5", "correta": True},
                {"id": 3, "texto": "6", "correta": False},
                {"id": 4, "texto": "8", "correta": False},
            ],
        },
        {
            "id": 3,
            "pergunta": "Quantas girafas consegues contar?",
            "imagem_pergunta": "4_girafas.png", #[cite: 8]
            "alternativas": [
                {"id": 1, "texto": "2", "correta": False},
                {"id": 2, "texto": "6", "correta": False},
                {"id": 3, "texto": "4", "correta": True},
                {"id": 4, "texto": "5", "correta": False},
            ],
        },
        {
            "id": 4,
            "pergunta": "Quantos tigres estão juntos?",
            "imagem_pergunta": "3_tigres.png", #[cite: 8]
            "alternativas": [
                {"id": 1, "texto": "1", "correta": False},
                {"id": 2, "texto": "4", "correta": False},
                {"id": 3, "texto": "3", "correta": True},
                {"id": 4, "texto": "5", "correta": False},
            ],
        }
    ],
    "GEOGRAFIA": [
        {
            "id": 1,
            "pergunta": "Qual destas é a bandeira do Brasil?",
            "imagem_pergunta": None,
            "alternativas": [
                {"id": 1, "texto": "🇧🇷 Brasil", "correta": True},
                {"id": 2, "texto": "🇦🇷 Argentina", "correta": False},
                {"id": 3, "texto": "🇵🇹 Portugal", "correta": False},
                {"id": 4, "texto": "🇺🇾 Uruguai", "correta": False},
            ],
        },
        # Podes adicionar mais exercícios de geografia aqui
    ],
}

# Quando o backend do Jojo estiver pronto, a ideia é criar um services.py
# com uma função buscar_exercicios(materia) que troca esse dicionário
# por uma chamada real, tipo: requests.get(f"http://localhost:8080/exercicios/{materia}").json()
