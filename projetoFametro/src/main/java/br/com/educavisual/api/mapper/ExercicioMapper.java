package br.com.educavisual.api.mapper;

import br.com.educavisual.api.dto.exercicio.AlternativaResponse;
import br.com.educavisual.api.dto.exercicio.ExercicioResponse;
import br.com.educavisual.api.entity.Alternativa;
import br.com.educavisual.api.entity.Exercicio;

import java.util.List;

public final class ExercicioMapper {

    private ExercicioMapper() {}

    public static ExercicioResponse toResponse(Exercicio exercicio, List<Alternativa> alternativas) {
        List<AlternativaResponse> alternativasResponse = alternativas.stream()
            .map(a -> new AlternativaResponse(a.getId(), a.getImagem()))
            .toList();

        return new ExercicioResponse(
            exercicio.getId(),
            exercicio.getTipo(),
            exercicio.getImagemPergunta(),
            exercicio.getMateria().getId(),
            exercicio.getMateria().getNome(),
            exercicio.getAtivo(),
            alternativasResponse
        );
    }
}
