package br.com.educavisual.api.dto.tentativa;

import jakarta.validation.constraints.NotNull;

public record ResponderExercicioRequest(
    @NotNull Long usuarioId,
    @NotNull Long exercicioId,
    @NotNull Long alternativaId
) {}
