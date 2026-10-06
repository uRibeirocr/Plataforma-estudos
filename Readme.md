# Plataforma de Estudos

Projeto de extensão com exercícios visuais para crianças de 5 a 12 anos. A aplicação atual oferece atividades de Matemática e Geografia, com alternativas ilustradas e pontuação local.

## O que já funciona

- Escolha entre Matemática e Geografia.
- Exercícios com imagem, alternativas e feedback imediato.
- Cadastro e login de aluno ou responsável.
- Pontuação persistente de 10 pontos por resposta correta.
- Progresso por matéria e vínculo de responsável a aluno.
- API Java com Spring Boot, autenticação JWT e banco H2 local.

## Estado atual

O frontend Flet está integrado à API Spring Boot em `projetoFametro`. O backend
cria Matemática, Geografia e carrega as 100 questões visuais de
`UI/questoes.json` no primeiro start, permitindo uma demonstração completa.

## Estrutura

```
Plataforma-estudos/
├── UI/
│   ├── assets/          # imagens das questões e alternativas
│   ├── components/      # componentes compartilhados
│   ├── views/           # telas da aplicação
│   ├── main.py          # ponto de entrada do frontend
│   └── mock_data.py     # dados locais temporários das questões
├── projetoFametro/    # API Java / Spring Boot
├── requirements.txt
└── Readme.md
```

## Como executar

Pré-requisitos: Python 3.10+, Java 21 e Maven 3.9+.

No PowerShell, a partir da pasta do repositório:

```powershell
cd projetoFametro
mvn spring-boot:run
```

Execute esse comando dentro da pasta `projetoFametro` e deixe o terminal aberto.
Ele inicia a API em `http://127.0.0.1:8080` e cria o banco H2 local. Em outro
PowerShell, na raiz do repositório, prepare e execute o frontend:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
cd UI
python main.py
```

O aplicativo permite criar conta de aluno ou responsável. Após criar um aluno,
anote o ID mostrado pelo backend para vinculá-lo à conta do responsável.

No macOS ou Linux, ative o ambiente com `source .venv/bin/activate` antes de instalar as dependências.

## Equipe e responsabilidades

| Área | Responsável |
|---|---|
| Backend (Spring Boot) | Jonatas |
| Banco de dados | Duvenson |
| Frontend (Flet) | P. Neto e Flávio |
| Testes | Giovana |
| Conteúdo educacional | Vitor |
