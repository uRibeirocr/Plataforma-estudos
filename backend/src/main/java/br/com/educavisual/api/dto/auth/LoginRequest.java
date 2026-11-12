package br.com.educavisual.api.dto.auth;

import jakarta.validation.constraints.NotBlank;

public record LoginRequest(
    @NotBlank String nome,
    @NotBlank String senha
) {}
