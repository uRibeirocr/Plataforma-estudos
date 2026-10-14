package br.com.educavisual.api.config;

import br.com.educavisual.api.entity.Materia;
import br.com.educavisual.api.repository.MateriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@RequiredArgsConstructor
public class DataInitializer {

    @Bean
    CommandLineRunner seedMaterias(MateriaRepository materiaRepository) {
        return args -> {
            if (materiaRepository.findByNomeIgnoreCase("MATEMATICA").isEmpty()) {
                materiaRepository.save(Materia.builder()
                    .nome("MATEMATICA")
                    .descricao("Exercícios visuais de matemática com foco em tabuada.")
                    .ativo(true)
                    .build());
            }

            if (materiaRepository.findByNomeIgnoreCase("GEOGRAFIA").isEmpty()) {
                materiaRepository.save(Materia.builder()
                    .nome("GEOGRAFIA")
                    .descricao("Exercícios visuais para identificação de países e bandeiras.")
                    .ativo(true)
                    .build());
            }
        };
    }
}
