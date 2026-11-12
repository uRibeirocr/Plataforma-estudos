# Pratica+ · Plataforma de Estudos

Projeto de extensão: plataforma de estudo prático e ilustrativo para crianças de 5 a 12 anos, com exercícios de **Matemática** (contagem e tabuada) e **Geografia** (bandeiras). São 100 questões com apoio visual (50 por matéria).

## Como funciona

- Dois perfis: **Aluno** (responde exercícios e acompanha o progresso) e **Responsável** (só visualiza o progresso dos alunos vinculados).
- Cada atividade é uma **rodada** de 5, 10, 20 ou todas as questões, sorteadas. A pergunta é lida em voz alta (opcional) e as alternativas são cards com imagem.
- Ao responder, o app mostra na hora a alternativa certa (verde) e a escolhida errada (vermelha), com uma explicação curta.
- Acerto vale **+10 pontos**; erro não tira pontos e qualquer exercício pode ser refeito.
- No fim da rodada: **estrelas (0 a 3)**, pontos, acertos e revisão das questões erradas, com o botão **"Refazer os erros"**.
- O progresso é guardado por matéria: tentativas, acertos, erros, pontos e quantos exercícios diferentes já foram dominados.

## Estrutura do repositório

```
Plataforma-estudos/
├── backend/            API Java 21 + Spring Boot (JWT, JPA, H2 em dev / PostgreSQL em produção)
├── frontend/           App Flet (Python): telas, lógica da rodada e cliente da API
│   ├── assets/         imagens das perguntas e alternativas
│   └── tests/          testes da lógica (sem precisar do Flet)
├── conteudo/           questoes.json: fonte única das 100 questões (API, app e site)
├── site/               versão web estática das atividades (gerada no GitHub Actions)
├── scripts/            validar_conteudo.py (confere gabaritos e imagens)
├── .github/workflows/  CI (API, conteúdo, frontend) e publicação do site
└── Dockerfile          imagem da API para deploy
```

## Rodando tudo localmente

Pré-requisitos: Java 21, Maven 3.9+ e Python 3.10+.

**1. API** (porta 8080; banco H2 local em `backend/data/`, criado e preenchido no primeiro start):

```bash
cd backend
mvn spring-boot:run
```

**2. App (Flet)**, em outro terminal:

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd frontend && python main.py
```

Na tela de login é possível **Entrar**, **Criar conta** (aluno ou responsável) ou **Jogar sem conta (offline)**, que usa `conteudo/questoes.json` direto e não precisa da API. O responsável vincula um aluno pelo **nome** dele. Para apontar o app para outra API: `PLATAFORMA_API_URL=https://minha-api/api python main.py`.

## Site estático (GitHub Pages)

`python site/build_site.py` gera `_site/` com a versão web das atividades (progresso salvo no navegador). O workflow `pages.yml` faz isso a cada push e publica no GitHub Pages quando a mudança chega no `main`. Ative uma vez em **Settings → Pages → Source: GitHub Actions**.

## Deploy da API

A API vira uma imagem Docker (`Dockerfile` na raiz) e pode rodar em qualquer host de contêiner (Render, Railway, Fly.io, Cloud Run...). O banco de produção pode ser o **PostgreSQL do Supabase**. Variáveis de ambiente:

| Variável | Para quê |
|---|---|
| `DATABASE_URL` | `jdbc:postgresql://HOST:5432/postgres` (Supabase: *Project Settings → Database*) |
| `DATABASE_USER` / `DATABASE_PASSWORD` | credenciais do banco |
| `JWT_SECRET` | segredo do token, **mínimo 32 caracteres** |
| `CORS_ALLOWED_ORIGINS` | origens web permitidas, separadas por vírgula (opcional) |
| `PORT` | porta (o padrão é 8080) |

A imagem já sobe com `SPRING_PROFILES_ACTIVE=prod`. O health check fica em `/actuator/health` e as imagens em `/imagens/**`.

## Testes e CI

```bash
mvn -f backend/pom.xml verify                                  # API: fluxo completo com banco em memória
python scripts/validar_conteudo.py                             # 100 questões: 1 gabarito, 4 alternativas, imagens existem
python -m unittest discover -s frontend/tests -t frontend      # lógica da rodada e cliente HTTP
```

O workflow `ci.yml` roda os três a cada push e pull request.

## Equipe e responsabilidades

| Área | Responsável |
|---|---|
| Backend (Spring Boot) | Jonatas |
| Banco de dados | Duvenson |
| Frontend (Flet) | P. Neto e Flávio |
| Testes | Giovana |
| Conteúdo educacional | Vitor |
