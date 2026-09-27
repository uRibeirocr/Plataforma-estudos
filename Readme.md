# Plataforma de Estudos

Projeto de extensão: uma plataforma de estudo prático e ilustrativo para crianças de 5 a 12 anos, com exercícios de **Matemática (tabuada)** e **Geografia (bandeiras)**.

## Como funciona

- O sistema tem dois tipos de usuário: **Aluno** (responde exercícios e acompanha o progresso) e **Responsável** (apenas visualiza o progresso dos alunos vinculados).
- Cada exercício mostra uma pergunta com apoio visual (imagens) e alternativas em formato de card, também com imagens.
- Ao responder, o aluno ganha **+10 pontos** por resposta correta (sem perda de pontos no erro) e pode refazer exercícios já respondidos.
- Depois de responder, pode aparecer uma explicação visual (opcional).
- O sistema registra o progresso do aluno por matéria: questões respondidas, acertos, erros, pontuação e percentual de acertos.

## Equipe e responsabilidades

| Área | Responsável |
|---|---|
| Backend (Spring Boot) | Jojo |
| Banco de dados | Duv |
| Frontend (Flet) | Neto e Flávio |
| Testes | Giovana |
| Conteúdo educacional | Vitor |

## Estrutura do repositório

```
Plataforma-estudos/
├── backend/     -> API em Spring Boot
└── frontend/    -> App em Flet (Python)
```

## Rodando o frontend (Flet)

Dentro da pasta `frontend`:

```bash
pip install flet
python main.py
```

Por enquanto, o frontend usa dados mockados (fixos, em `mock_data.py`) enquanto o backend ainda está em desenvolvimento. Quando a API estiver pronta, esses dados serão substituídos por chamadas reais.
