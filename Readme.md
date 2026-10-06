# Plataforma de Estudos

Projeto de extensão com exercícios visuais para crianças de 5 a 12 anos. A aplicação atual oferece atividades de Matemática e Geografia, com alternativas ilustradas e pontuação local.

## O que já funciona

- Escolha entre Matemática e Geografia.
- Exercícios com imagem, alternativas e feedback imediato.
- Pontuação de 10 pontos por resposta correta durante a sessão.
- Tela de resultado ao terminar a lista de questões.

## Estado atual

O frontend é feito em Python com Flet. Enquanto o backend e o banco de dados não são integrados, as questões são carregadas de dados locais em `UI/mock_data.py` e a pontuação é mantida apenas enquanto o aplicativo está aberto.

O login, a área do responsável e o progresso persistente ainda dependem da API e do banco de dados.

## Estrutura

```
Plataforma-estudos/
├── UI/
│   ├── assets/          # imagens das questões e alternativas
│   ├── components/      # componentes compartilhados
│   ├── views/           # telas da aplicação
│   ├── main.py          # ponto de entrada do frontend
│   └── mock_data.py     # dados locais temporários das questões
├── requirements.txt
└── Readme.md
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

No PowerShell, a partir da pasta do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python backend/server.py
```

Deixe esse primeiro terminal aberto: ele executa a API e cria o banco local
SQLite em `backend/data/plataforma.db`. Em um segundo PowerShell, ative o mesmo
ambiente virtual e execute o frontend:

```powershell
cd UI
python main.py
```

O aplicativo permite criar conta de aluno ou responsável. O responsável pode
vincular um aluno pelo e-mail depois que a conta do aluno for criada.

> A API Python/SQLite existe apenas nesta branch de contingência para permitir
> teste completo imediato. A equipe pode substituí-la pela implementação Spring
> Boot planejada sem alterar a interface do usuário.

No macOS ou Linux, ative o ambiente com `source .venv/bin/activate` antes de instalar as dependências.

## Equipe e responsabilidades

| Área | Responsável |
|---|---|
| Backend (Spring Boot) | Jonatas |
| Banco de dados | Duvenson |
| Frontend (Flet) | P. Neto e Flávio |
| Testes | Giovana |
| Conteúdo educacional | Vitor |
