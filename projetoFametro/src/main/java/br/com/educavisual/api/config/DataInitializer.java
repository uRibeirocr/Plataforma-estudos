package br.com.educavisual.api.config;

import br.com.educavisual.api.entity.Alternativa;
import br.com.educavisual.api.entity.Exercicio;
import br.com.educavisual.api.entity.Materia;
import br.com.educavisual.api.enums.TipoExercicio;
import br.com.educavisual.api.repository.AlternativaRepository;
import br.com.educavisual.api.repository.ExercicioRepository;
import br.com.educavisual.api.repository.MateriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@RequiredArgsConstructor
public class DataInitializer {

    @Bean
    CommandLineRunner seedData(MateriaRepository materias, ExercicioRepository exercicios,
                               AlternativaRepository alternativas) {
        return args -> {
            Materia matematica = materias.findByNomeIgnoreCase("MATEMATICA").orElseGet(() -> materias.save(Materia.builder()
                .nome("MATEMATICA").descricao("Exercícios visuais de matemática com foco em tabuada.").ativo(true).build()));
            Materia geografia = materias.findByNomeIgnoreCase("GEOGRAFIA").orElseGet(() -> materias.save(Materia.builder()
                .nome("GEOGRAFIA").descricao("Exercícios visuais para identificação de países e bandeiras.").ativo(true).build()));

            if (exercicios.count() == 0) {
                criarExercicio(exercicios, alternativas, matematica, TipoExercicio.TABUADA,
                    "Quantos carros temos no total na imagem?", "varios_carros.png", "16", "10", "16", "12", "20");
                criarExercicio(exercicios, alternativas, matematica, TipoExercicio.TABUADA,
                    "Quantos macaquinhos estão a dormir?", "5_macacos.png", "5", "3", "5", "6", "8");
                criarExercicio(exercicios, alternativas, geografia, TipoExercicio.BANDEIRA,
                    "Qual é a bandeira do Brasil?", "geografia/G01_pergunta.png", "A", "A", "B", "C", "D");
                criarExercicio(exercicios, alternativas, geografia, TipoExercicio.BANDEIRA,
                    "Qual é a bandeira da Argentina?", "geografia/G02_pergunta.png", "B", "A", "B", "C", "D");
            }
        };
    }

    private void criarExercicio(ExercicioRepository exercicios, AlternativaRepository alternativas,
                                Materia materia, TipoExercicio tipo, String pergunta, String imagemPergunta,
                                String correta, String... opcoes) {
        Exercicio exercicio = exercicios.save(Exercicio.builder()
            .tipo(tipo).pergunta(pergunta).imagemPergunta(imagemPergunta).materia(materia).ativo(true).build());
        for (String opcao : opcoes) {
            alternativas.save(Alternativa.builder().exercicio(exercicio).imagem("").texto(opcao)
                .correta(opcao.equals(correta)).build());
        }
    }
}
