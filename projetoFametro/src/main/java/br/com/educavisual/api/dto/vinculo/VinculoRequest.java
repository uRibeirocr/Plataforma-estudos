package br.com.educavisual.api.dto.vinculo;

import jakarta.validation.constraints.NotNull;

public record VinculoRequest(
    @NotNull Long responsavelId,
    @NotNull Long alunoId
) {}
