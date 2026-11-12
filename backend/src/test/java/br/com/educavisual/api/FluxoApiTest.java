package br.com.educavisual.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/** Testa a API de ponta a ponta (HTTP + segurança + banco H2 em memória + carga do conteúdo). */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class FluxoApiTest {

    @Autowired
    MockMvc mvc;

    @Autowired
    ObjectMapper om;

    // ---------- helpers ----------

    private JsonNode chamar(MockHttpServletRequestBuilder req, String token, int statusEsperado) throws Exception {
        if (token != null) {
            req = req.header("Authorization", "Bearer " + token);
        }
        String corpo = mvc.perform(req)
            .andExpect(status().is(statusEsperado))
            .andReturn().getResponse().getContentAsString(StandardCharsets.UTF_8);
        return corpo.isBlank() ? null : om.readTree(corpo);
    }

    private JsonNode enviar(String url, Object body, String token, int statusEsperado) throws Exception {
        return chamar(post(url).contentType(MediaType.APPLICATION_JSON).content(om.writeValueAsString(body)),
            token, statusEsperado);
    }

    private static String nomeUnico(String prefixo) {
        return prefixo + "-" + UUID.randomUUID().toString().substring(0, 8);
    }

    private JsonNode criarELogar(String nome, String tipo) throws Exception {
        enviar("/api/usuarios", Map.of("nome", nome, "senha", "123456", "tipoUsuario", tipo), null, 201);
        return enviar("/api/auth/login", Map.of("nome", nome, "senha", "123456"), null, 200);
    }

    private long idDaMateria(String token, String nome) throws Exception {
        for (JsonNode m : chamar(get("/api/materias"), token, 200)) {
            if (nome.equals(m.get("nome").asText())) {
                return m.get("id").asLong();
            }
        }
        throw new AssertionError("Matéria não encontrada: " + nome);
    }

    // ---------- testes ----------

    @Test
    void rotasProtegidasSemTokenRetornam401() throws Exception {
        JsonNode erro = chamar(get("/api/materias"), null, 401);
        assertEquals(401, erro.get("status").asInt());
    }

    @Test
    void healthEPublico() throws Exception {
        chamar(get("/actuator/health"), null, 200);
    }

    @Test
    void cadastroValidaDadosEImpedeNomeDuplicado() throws Exception {
        JsonNode invalido = enviar("/api/usuarios",
            Map.of("nome", nomeUnico("curta"), "senha", "123", "tipoUsuario", "ALUNO"), null, 400);
        assertTrue(invalido.get("fieldErrors").has("senha"));

        String nome = nomeUnico("dup");
        enviar("/api/usuarios", Map.of("nome", nome, "senha", "123456", "tipoUsuario", "ALUNO"), null, 201);
        enviar("/api/usuarios", Map.of("nome", nome.toUpperCase(), "senha", "123456", "tipoUsuario", "ALUNO"),
            null, 400);
    }

    @Test
    void loginComSenhaErradaRetorna401() throws Exception {
        String nome = nomeUnico("login");
        criarELogar(nome, "ALUNO");
        enviar("/api/auth/login", Map.of("nome", nome, "senha", "errada!"), null, 401);
    }

    @Test
    void conteudoCarregadoComMateriasEExerciciosSemGabarito() throws Exception {
        String token = criarELogar(nomeUnico("conteudo"), "ALUNO").get("token").asText();

        for (String materia : new String[]{"MATEMATICA", "GEOGRAFIA"}) {
            long id = idDaMateria(token, materia);
            JsonNode todos = chamar(get("/api/exercicios/materia/" + id), token, 200);
            assertEquals(50, todos.size(), "50 exercícios em " + materia);

            JsonNode primeiro = todos.get(0);
            assertFalse(primeiro.get("pergunta").asText().isBlank());
            assertEquals(4, primeiro.get("alternativas").size());
            // O gabarito não pode vazar antes da resposta.
            assertFalse(primeiro.get("alternativas").get(0).has("correta"));
            assertFalse(primeiro.has("explicacao"));
        }
    }

    @Test
    void limiteEEmbaralharMontamUmaRodada() throws Exception {
        String token = criarELogar(nomeUnico("rodada"), "ALUNO").get("token").asText();
        long id = idDaMateria(token, "MATEMATICA");

        JsonNode rodada = chamar(get("/api/exercicios/materia/" + id + "?limite=10&embaralhar=true"), token, 200);
        assertEquals(10, rodada.size());
        chamar(get("/api/exercicios/materia/" + id + "?limite=0"), token, 400);
        chamar(get("/api/exercicios/materia/999999"), token, 404);
    }

    @Test
    void alunoRespondeEProgressoAcompanha() throws Exception {
        JsonNode login = criarELogar(nomeUnico("aluno"), "ALUNO");
        String token = login.get("token").asText();
        long alunoId = login.get("id").asLong();
        long materiaId = idDaMateria(token, "MATEMATICA");

        JsonNode exercicio = chamar(get("/api/exercicios/materia/" + materiaId + "?limite=1"), token, 200).get(0);
        long exercicioId = exercicio.get("id").asLong();
        long primeiraAlternativa = exercicio.get("alternativas").get(0).get("id").asLong();

        // 1ª tentativa: sempre a primeira alternativa; a resposta revela o gabarito.
        JsonNode t1 = enviar("/api/tentativas", Map.of(
            "usuarioId", alunoId, "exercicioId", exercicioId, "alternativaId", primeiraAlternativa), token, 201);
        long gabarito = t1.get("alternativaCorretaId").asLong();
        assertNotNull(t1.get("explicacao"));
        assertEquals(t1.get("correta").asBoolean(), primeiraAlternativa == gabarito);
        assertEquals(t1.get("correta").asBoolean() ? 10 : 0, t1.get("pontuacao").asInt());

        // 2ª tentativa (pode refazer): a alternativa correta.
        JsonNode t2 = enviar("/api/tentativas", Map.of(
            "usuarioId", alunoId, "exercicioId", exercicioId, "alternativaId", gabarito), token, 201);
        assertTrue(t2.get("correta").asBoolean());
        assertEquals(10, t2.get("pontuacao").asInt());

        int esperado = t1.get("pontuacao").asInt() + t2.get("pontuacao").asInt();
        JsonNode progresso = chamar(get("/api/progresso/alunos/" + alunoId + "/materias/" + materiaId), token, 200);
        assertEquals(2, progresso.get("tentativasRespondidas").asInt());
        assertEquals(esperado, progresso.get("pontuacao").asInt());
        assertEquals(1, progresso.get("exerciciosRespondidos").asInt());
        assertEquals(1, progresso.get("exerciciosDominados").asInt());
        assertEquals(50, progresso.get("totalExercicios").asInt());

        JsonNode todas = chamar(get("/api/progresso/alunos/" + alunoId), token, 200);
        assertEquals(2, todas.size());

        JsonNode historico = chamar(get("/api/tentativas/aluno/" + alunoId), token, 200);
        assertEquals(2, historico.size());
        assertEquals(gabarito, historico.get(0).get("alternativaCorretaId").asLong());
    }

    @Test
    void alternativaDeOutroExercicioEhRejeitada() throws Exception {
        JsonNode login = criarELogar(nomeUnico("troca"), "ALUNO");
        String token = login.get("token").asText();
        long materiaId = idDaMateria(token, "MATEMATICA");

        JsonNode lista = chamar(get("/api/exercicios/materia/" + materiaId + "?limite=2"), token, 200);
        long exercicioA = lista.get(0).get("id").asLong();
        long alternativaDeB = lista.get(1).get("alternativas").get(0).get("id").asLong();

        enviar("/api/tentativas", Map.of(
            "usuarioId", login.get("id").asLong(), "exercicioId", exercicioA, "alternativaId", alternativaDeB),
            token, 400);
    }

    @Test
    void responsavelAcompanhaApenasAlunosVinculados() throws Exception {
        JsonNode aluno = criarELogar(nomeUnico("filho"), "ALUNO");
        JsonNode outroAluno = criarELogar(nomeUnico("outro"), "ALUNO");
        JsonNode responsavel = criarELogar(nomeUnico("mae"), "RESPONSAVEL");
        String tokenAluno = aluno.get("token").asText();
        String tokenResp = responsavel.get("token").asText();
        long alunoId = aluno.get("id").asLong();
        long respId = responsavel.get("id").asLong();

        // Antes do vínculo: sem acesso.
        chamar(get("/api/progresso/alunos/" + alunoId), tokenResp, 403);

        // Vincula pelo NOME do aluno (não exige saber o ID).
        enviar("/api/responsaveis/vinculos", Map.of("alunoNome", aluno.get("nome").asText()), tokenResp, 201);
        enviar("/api/responsaveis/vinculos", Map.of("alunoNome", aluno.get("nome").asText()), tokenResp, 400);

        JsonNode alunos = chamar(get("/api/responsaveis/" + respId + "/alunos"), tokenResp, 200);
        assertEquals(1, alunos.size());
        assertEquals(alunoId, alunos.get(0).get("id").asLong());

        chamar(get("/api/progresso/alunos/" + alunoId), tokenResp, 200);
        chamar(get("/api/progresso/alunos/" + outroAluno.get("id").asLong()), tokenResp, 403);

        // Aluno não vê o progresso de outro aluno.
        chamar(get("/api/progresso/alunos/" + outroAluno.get("id").asLong()), tokenAluno, 403);

        // Vínculo com nome inexistente.
        enviar("/api/responsaveis/vinculos", Map.of("alunoNome", "nao-existe-" + UUID.randomUUID()), tokenResp, 404);
    }

    @Test
    void perfisRespeitamSuasPermissoes() throws Exception {
        JsonNode responsavel = criarELogar(nomeUnico("resp"), "RESPONSAVEL");
        JsonNode aluno = criarELogar(nomeUnico("alu"), "ALUNO");
        String tokenResp = responsavel.get("token").asText();
        String tokenAluno = aluno.get("token").asText();
        long materiaId = idDaMateria(tokenResp, "GEOGRAFIA");
        JsonNode ex = chamar(get("/api/exercicios/materia/" + materiaId + "?limite=1"), tokenResp, 200).get(0);

        // Responsável não responde exercícios (RN01) -> 403 (e não 500).
        enviar("/api/tentativas", Map.of(
            "usuarioId", responsavel.get("id").asLong(),
            "exercicioId", ex.get("id").asLong(),
            "alternativaId", ex.get("alternativas").get(0).get("id").asLong()), tokenResp, 403);

        // Aluno não cria vínculos.
        enviar("/api/responsaveis/vinculos", Map.of("alunoNome", aluno.get("nome").asText()), tokenAluno, 403);

        // Aluno não responde no perfil de outra pessoa.
        enviar("/api/tentativas", Map.of(
            "usuarioId", responsavel.get("id").asLong(),
            "exercicioId", ex.get("id").asLong(),
            "alternativaId", ex.get("alternativas").get(0).get("id").asLong()), tokenAluno, 403);
    }

    @Test
    void corpoMalFormadoRetorna400() throws Exception {
        chamar(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content("{nao-e-json"), null, 400);
    }
}
