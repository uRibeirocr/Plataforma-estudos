# Educa Visual API

Backend Java + Spring Boot criado a partir do diagrama de regras de negócio enviado.

## Tecnologias

- Java 21
- Spring Boot 3.5.6
- Spring Web
- Spring Data JPA
- Bean Validation
- Spring Security
- JWT (JJWT)
- BCrypt
- PostgreSQL (H2 em memória somente nos testes)
- Lombok
- Maven

## Estrutura

```text
src/main/java/br/com/educavisual/api
├── config
│   ├── DataInitializer.java
│   └── SecurityConfig.java
├── controller
│   ├── AuthController.java
│   ├── ExercicioController.java
│   ├── MateriaController.java
│   ├── ProgressoController.java
│   ├── ResponsavelAlunoController.java
│   ├── TentativaController.java
│   └── UsuarioController.java
├── dto
│   ├── auth
│   ├── exercicio
│   ├── materia
│   ├── progresso
│   ├── tentativa
│   ├── usuario
│   └── vinculo
├── entity
│   ├── Alternativa.java
│   ├── Exercicio.java
│   ├── Materia.java
│   ├── ResponsavelAluno.java
│   ├── Tentativa.java
│   └── Usuario.java
├── enums
│   ├── TipoExercicio.java
│   └── TipoUsuario.java
├── exception
├── mapper
├── repository
├── security
└── service
```

A pasta `service` foi adicionada mesmo não estando na lista inicial porque evita colocar regra de negócio em controller ou repository.

## Regras implementadas

- Existem somente os perfis `ALUNO` e `RESPONSAVEL`.
- As matérias `MATEMATICA` e `GEOGRAFIA` são criadas automaticamente no primeiro start.
- Exercícios possuem pergunta visual, explicação visual e alternativas visuais.
- O aluno escolhe uma alternativa.
- Alternativa correta vale `+10` pontos.
- Alternativa incorreta vale `0` pontos.
- Não existe perda de pontos.
- O mesmo exercício pode ser respondido novamente.
- Cada nova resposta cria uma nova `Tentativa`.
- O progresso é calculado por matéria.
- O responsável só pode consultar progresso de aluno vinculado a ele.
- O aluno só pode responder no próprio perfil e consultar o próprio histórico.

## Por que mantive a pasta `security`

Mesmo sendo um projeto pequeno, o modelo possui senha, perfis distintos e dados de progresso. Por isso foi incluída autenticação JWT, BCrypt e autorização por perfil. A camada está isolada e pode ser simplificada depois sem afetar as entidades/regras.

## Banco de dados

A aplicação usa PostgreSQL. Crie o banco em uma instância PostgreSQL disponível:

```sql
CREATE DATABASE educa_visual_db;
```

Configure as variáveis de ambiente antes de iniciar a API. Exemplo no PowerShell:

```powershell
$env:DB_URL = "jdbc:postgresql://localhost:5432/educa_visual_db"
$env:DB_USERNAME = "postgres"
$env:DB_PASSWORD = "sua_senha"
mvn spring-boot:run
```

`DB_URL` e `DB_USERNAME` possuem os valores padrão mostrados acima. `DB_PASSWORD` é obrigatória e deve conter a senha do usuário do PostgreSQL. Para um servidor remoto, ajuste o host, a porta e o nome do banco na URL.

O Hibernate cria/atualiza as tabelas ao iniciar (`ddl-auto: update`); o banco precisa existir e o usuário precisa ter permissão para criar e alterar tabelas. Os dados do H2 anterior não são migrados automaticamente.

Os testes usam o perfil `test` com H2 em memória, sem precisar de PostgreSQL ou credenciais locais. Esse teste não valida uma conexão real com PostgreSQL.

## Executar

Pré-requisitos:

- Java 21
- Maven 3.9+

```bash
mvn spring-boot:run
```

API:

```text
http://localhost:8080
```

## Fluxo básico de teste

### 1. Criar aluno

`POST /api/usuarios`

```json
{
  "nome": "Aluno Teste",
  "senha": "123456",
  "tipoUsuario": "ALUNO"
}
```

### 2. Criar responsável

`POST /api/usuarios`

```json
{
  "nome": "Responsavel Teste",
  "senha": "123456",
  "tipoUsuario": "RESPONSAVEL"
}
```

### 3. Login

`POST /api/auth/login`

```json
{
  "nome": "Aluno Teste",
  "senha": "123456"
}
```

A resposta contém um token JWT. Nos endpoints protegidos, envie:

```text
Authorization: Bearer SEU_TOKEN
```

### 4. Matérias

`GET /api/materias`

### 5. Exercícios de uma matéria

`GET /api/exercicios/materia/{materiaId}`

### 6. Responder exercício

`POST /api/tentativas`

```json
{
  "usuarioId": 1,
  "exercicioId": 1,
  "alternativaId": 2
}
```

Resposta de exemplo:

```json
{
  "id": 1,
  "usuarioId": 1,
  "exercicioId": 1,
  "alternativaId": 2,
  "correta": true,
  "pontuacao": 10,
  "imagemExplicacao": "/imagens/explicacoes/4x4.png"
}
```

### 7. Progresso

`GET /api/progresso/alunos/{alunoId}/materias/{materiaId}`

Exemplo:

```json
{
  "alunoId": 1,
  "materiaId": 1,
  "materia": "MATEMATICA",
  "tentativasRespondidas": 5,
  "tentativasCorretas": 4,
  "tentativasErradas": 1,
  "pontuacao": 40,
  "percentualAcertos": 80.0
}
```

## Observações importantes

1. Não foi criado perfil `ADMIN`, pois a RN01 define somente ALUNO e RESPONSAVEL.
2. Por isso, o projeto entrega a leitura dos conteúdos e a lógica de resposta/progresso, mas não expõe CRUD público de matéria/exercício/alternativa. Esses conteúdos podem ser inseridos por carga inicial, script SQL ou por um módulo administrativo futuro.
3. O endpoint de cadastro de usuários está público para facilitar desenvolvimento. Em produção, ele deve ser adaptado ao fluxo real de criação de contas.
4. A criação de vínculo responsável/aluno está disponível para o responsável autenticado. Em produção, recomenda-se um fluxo de convite/código de vínculo para impedir associação indevida por conhecimento de IDs.
5. URLs/caminhos de imagens são armazenados como `String`, de acordo com o diagrama. O armazenamento físico das imagens pode ser local, S3/MinIO ou outro serviço.
