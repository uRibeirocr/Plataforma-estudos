package br.com.educavisual.api.config;

import br.com.educavisual.api.entity.Alternativa;
import br.com.educavisual.api.entity.Exercicio;
import br.com.educavisual.api.entity.Materia;
import br.com.educavisual.api.enums.TipoExercicio;
import br.com.educavisual.api.repository.AlternativaRepository;
import br.com.educavisual.api.repository.ExercicioRepository;
import br.com.educavisual.api.repository.MateriaRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * Carga inicial: cria as matérias e sincroniza os exercícios a partir de {@code seed/questoes.json}
 * (cópia de {@code conteudo/questoes.json} feita pelo Maven). É idempotente: rodar de novo atualiza
 * o que mudou no JSON, usando o campo {@code codigo} como chave, e nunca duplica registros.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    static final String ARQUIVO_SEED = "seed/questoes.json";

    private final MateriaRepository materiaRepository;
    private final ExercicioRepository exercicioRepository;
    private final AlternativaRepository alternativaRepository;
    private final ObjectMapper objectMapper;

    @Override
    @Transactional
    public void run(String... args) throws IOException {
        Materia matematica = garantirMateria("MATEMATICA",
            "Exercícios visuais de matemática com foco em contagem e tabuada.");
        Materia geografia = garantirMateria("GEOGRAFIA",
            "Exercícios visuais para identificação de países e bandeiras.");

        ClassPathResource recurso = new ClassPathResource(ARQUIVO_SEED);
        if (!recurso.exists()) {
            log.warn("Arquivo {} não encontrado no classpath; exercícios não foram carregados.", ARQUIVO_SEED);
            return;
        }

        Map<String, Materia> materias = Map.of("MATEMATICA", matematica, "GEOGRAFIA", geografia);
        int criados = 0;
        int atualizados = 0;
        try (InputStream in = recurso.getInputStream()) {
            for (JsonNode questao : objectMapper.readTree(in)) {
                Materia materia = materias.get(questao.path("materia").asText());
                if (materia == null) {
                    log.warn("Questão {} ignorada: matéria desconhecida.", questao.path("codigo").asText());
                    continue;
                }
                if (sincronizar(questao, materia)) {
                    criados++;
                } else {
                    atualizados++;
                }
            }
        }
        log.info("Conteúdo carregado: {} exercício(s) novo(s), {} atualizado(s).", criados, atualizados);
    }

    private Materia garantirMateria(String nome, String descricao) {
        return materiaRepository.findByNomeIgnoreCase(nome).orElseGet(() -> materiaRepository.save(
            Materia.builder().nome(nome).descricao(descricao).ativo(true).build()));
    }

    /** @return true se criou o exercício, false se apenas atualizou um já existente. */
    private boolean sincronizar(JsonNode q, Materia materia) {
        String codigo = q.path("codigo").asText();
        Exercicio exercicio = exercicioRepository.findByCodigo(codigo).orElse(null);
        boolean novo = exercicio == null;
        if (novo) {
            exercicio = new Exercicio();
            exercicio.setCodigo(codigo);
            exercicio.setAtivo(true);
        }
        exercicio.setMateria(materia);
        exercicio.setTipo("GEOGRAFIA".equals(materia.getNome()) ? TipoExercicio.BANDEIRA : TipoExercicio.TABUADA);
        exercicio.setPergunta(texto(q, "pergunta"));
        exercicio.setExplicacao(texto(q, "explicacao"));
        exercicio.setImagemPergunta(q.path("imagem_pergunta").asText(""));
        exercicio.setImagemExplicacao(texto(q, "imagem_explicacao"));
        exercicio = exercicioRepository.save(exercicio);

        Map<String, Alternativa> existentes = new HashMap<>();
        for (Alternativa a : alternativaRepository.findAllByExercicioIdOrderByIdAsc(exercicio.getId())) {
            existentes.put(a.getLetra(), a);
        }

        for (JsonNode alt : q.path("alternativas")) {
            String letra = alt.path("letra").asText();
            Alternativa alternativa = existentes.getOrDefault(letra, new Alternativa());
            alternativa.setExercicio(exercicio);
            alternativa.setLetra(letra);
            alternativa.setTexto(texto(alt, "texto"));
            alternativa.setImagem(alt.path("imagem").asText(""));
            alternativa.setCorreta(alt.path("correta").asBoolean(false));
            alternativaRepository.save(alternativa);
        }
        return novo;
    }

    private static String texto(JsonNode no, String campo) {
        JsonNode valor = no.path(campo);
        return valor.isMissingNode() || valor.isNull() ? null : valor.asText();
    }
}
