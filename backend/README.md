# Educa Visual API

Backend Java 21 + Spring Boot 3.5 do Pratica+. Veja o [README da raiz](../README.md) para rodar o sistema completo.

## Tecnologias

Spring Web, Spring Data JPA, Bean Validation, Spring Security + JWT (JJWT), BCrypt, Actuator, H2 (dev) / PostgreSQL (prod), Lombok, Maven.

## Estrutura

```text
src/main/java/br/com/educavisual/api
├── config       DataInitializer (seed idempotente), SecurityConfig, WebConfig (/imagens/**)
├── controller   Auth, Usuario, Materia, Exercicio, Tentativa, Progresso, ResponsavelAluno
├── dto          records de entrada e saída, por assunto
├── entity       Usuario, Materia, Exercicio, Alternativa, Tentativa, ResponsavelAluno
├── enums        TipoUsuario, TipoExercicio
├── exception    exceções de negócio + GlobalExceptionHandler (JSON padronizado)
├── mapper       entidade -> DTO
├── repository   Spring Data JPA
├── security     JWT (serviço e filtro), UserDetails
└── service      regras de negócio
```

## Endpoints

`Authorization: Bearer <token>` em tudo, exceto onde indicado como público.

| Método e rota | Quem | O que faz |
|---|---|---|
| `POST /api/usuarios` | público | cria aluno ou responsável |
| `POST /api/auth/login` | público | devolve o token JWT |
| `GET /api/usuarios/me` | logado | dados do usuário atual |
| `GET /api/materias` | logado | matérias ativas |
| `GET /api/exercicios/materia/{id}?limite=10&embaralhar=true` | logado | monta uma rodada (sem gabarito) |
| `GET /api/exercicios/{id}` | logado | um exercício |
| `POST /api/tentativas` | aluno | responde; devolve `correta`, `pontuacao`, `alternativaCorretaId`, `explicacao` |
| `GET /api/tentativas/aluno/{id}` | aluno | histórico próprio |
| `GET /api/progresso/alunos/{id}` | aluno / responsável vinculado | progresso de todas as matérias |
| `GET /api/progresso/alunos/{id}/materias/{materiaId}` | idem | progresso de uma matéria |
| `POST /api/responsaveis/vinculos` | responsável | vincula aluno por `alunoNome` ou `alunoId` |
| `GET /api/responsaveis/{id}/alunos` | responsável | alunos vinculados |
| `GET /actuator/health`, `GET /imagens/**` | público | saúde e imagens |

Erros seguem sempre o formato `{timestamp, status, error, message, path, fieldErrors}` (401 sem/ com token inválido, 403 sem permissão, 400 validação, 404, 409).

## Conteúdo

As questões vêm de `../conteudo/questoes.json`, que o Maven copia para o classpath (`seed/questoes.json`). No start o `DataInitializer` cria as matérias e sincroniza os exercícios pelo campo `codigo`: rodar de novo atualiza o que mudou no JSON e nunca duplica.

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

Por padrão é usado H2 persistente em:

```text
./data/educa_visual_db
```

Console H2:

```text
http://localhost:8080/h2-console
```

JDBC URL:

```text
jdbc:h2:file:./data/educa_visual_db
```

Usuário: `sa`
Senha: vazia

Em produção use o perfil `prod` (PostgreSQL, veja o README da raiz). Para evoluir o esquema com segurança, adote migrations (Flyway/Liquibase).

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

`GET /api/exercicios/materia/{materiaId}?limite=10&embaralhar=true`

Devolve a pergunta e as alternativas (`id`, `letra`, `texto`, `imagem`), **sem o gabarito**.

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
  "alternativaCorretaId": 2,
  "explicacao": "4 × 4 = 16.",
  "imagemExplicacao": null
}
```

### 7. Progresso

`GET /api/progresso/alunos/{alunoId}` (todas as matérias) ou
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
  "percentualAcertos": 80.0,
  "exerciciosRespondidos": 4,
  "exerciciosDominados": 4,
  "totalExercicios": 50,
  "percentualConclusao": 8.0
}
```

## Observações importantes

1. Não foi criado perfil `ADMIN`, pois a RN01 define somente ALUNO e RESPONSAVEL.
2. Não há CRUD público de matéria/exercício/alternativa: o conteúdo entra pela carga inicial (`conteudo/questoes.json`) ou por um módulo administrativo futuro.
3. O endpoint de cadastro de usuários está público para facilitar desenvolvimento. Em produção, ele deve ser adaptado ao fluxo real de criação de contas.
4. A criação de vínculo responsável/aluno está disponível para o responsável autenticado, por nome ou ID do aluno. Em produção, recomenda-se um fluxo de convite/código de vínculo para impedir que alguém acompanhe um aluno só por saber o nome dele.
5. URLs/caminhos de imagens são armazenados como `String`, de acordo com o diagrama. O armazenamento físico das imagens pode ser local, S3/MinIO ou outro serviço.
