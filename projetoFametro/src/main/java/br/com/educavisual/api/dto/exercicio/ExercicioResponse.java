package br.com.educavisual.api.dto.exercicio;

import br.com.educavisual.api.enums.TipoExercicio;

import java.util.List;

public record ExercicioResponse(
    Long id,
    TipoExercicio tipo,
    String pergunta,
    String imagemPergunta,
    Long materiaId,
    String materia,
    Boolean ativo,
    List<AlternativaResponse> alternativas
) {}
