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
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.nio.file.Files;
import java.nio.file.Path;

@Configuration
@RequiredArgsConstructor
public class DataInitializer {

    @Bean
    CommandLineRunner seedData(MateriaRepository materias, ExercicioRepository exercicios,
                               AlternativaRepository alternativas, ObjectMapper objectMapper) {
        return args -> {
            Materia matematica = obterMateria(materias, "MATEMATICA", "Exercícios visuais de matemática com foco em tabuada.");
            Materia geografia = obterMateria(materias, "GEOGRAFIA", "Exercícios visuais para identificação de países e bandeiras.");

            criarExercicio(exercicios, alternativas, matematica, TipoExercicio.TABUADA,
                "Quantos carros temos no total na imagem?", "varios_carros.png", "16", "10", "16", "12", "20");
            criarExercicio(exercicios, alternativas, matematica, TipoExercicio.TABUADA,
                "Quantos macaquinhos estão a dormir?", "5_macacos.png", "5", "3", "5", "6", "8");
            criarExercicio(exercicios, alternativas, geografia, TipoExercicio.BANDEIRA,
                "Qual é a bandeira do Brasil?", "geografia/G01_pergunta.png", "A", "A", "B", "C", "D");
            criarExercicio(exercicios, alternativas, geografia, TipoExercicio.BANDEIRA,
                "Qual é a bandeira da Argentina?", "geografia/G02_pergunta.png", "B", "A", "B", "C", "D");

            carregarQuestoesDoFrontend(exercicios, alternativas, matematica, geografia, objectMapper);
        };
    }

    private Materia obterMateria(MateriaRepository materias, String nome, String descricao) {
        return materias.findByNomeIgnoreCase(nome).orElseGet(() -> materias.save(Materia.builder()
            .nome(nome).descricao(descricao).ativo(true).build()));
    }

    private void carregarQuestoesDoFrontend(ExercicioRepository exercicios, AlternativaRepository alternativas,
                                            Materia matematica, Materia geografia, ObjectMapper mapper) throws Exception {
        Path arquivo = localizarArquivoQuestoes();
        if (arquivo == null) {
            return;
        }
        for (JsonNode questao : mapper.readTree(Files.readString(arquivo))) {
            String pergunta = questao.path("pergunta").asText();
            if (exercicios.existsByPergunta(pergunta)) {
                continue;
            }
            boolean eGeografia = "GEOGRAFIA".equals(questao.path("materia").asText());
            Materia materia = eGeografia ? geografia : matematica;
            Exercicio exercicio = exercicios.save(Exercicio.builder()
                .tipo(eGeografia ? TipoExercicio.BANDEIRA : TipoExercicio.TABUADA)
                .pergunta(pergunta)
                .imagemPergunta(questao.path("imagem_pergunta").asText(""))
                .imagemExplicacao(questao.path("imagem_explicacao").isNull() ? null : questao.path("imagem_explicacao").asText())
                .materia(materia).ativo(true).build());
            for (JsonNode alternativa : questao.path("alternativas")) {
                alternativas.save(Alternativa.builder().exercicio(exercicio)
                    .imagem(alternativa.path("imagem").asText(""))
                    .texto(alternativa.path("texto").asText(""))
                    .correta(alternativa.path("correta").asBoolean())
                    .build());
            }
        }
    }

    private Path localizarArquivoQuestoes() {
        Path[] caminhos = {Path.of("../UI/questoes.json"), Path.of("UI/questoes.json")};
        for (Path caminho : caminhos) {
            if (Files.exists(caminho)) {
                return caminho;
            }
        }
        return null;
    }

    private void criarExercicio(ExercicioRepository exercicios, AlternativaRepository alternativas,
                                Materia materia, TipoExercicio tipo, String pergunta, String imagemPergunta,
                                String correta, String... opcoes) {
        if (exercicios.existsByPergunta(pergunta)) {
            return;
        }
        Exercicio exercicio = exercicios.save(Exercicio.builder()
            .tipo(tipo).pergunta(pergunta).imagemPergunta(imagemPergunta).materia(materia).ativo(true).build());
        for (String opcao : opcoes) {
            alternativas.save(Alternativa.builder().exercicio(exercicio).imagem("").texto(opcao)
                .correta(opcao.equals(correta)).build());
        }
    }
}
