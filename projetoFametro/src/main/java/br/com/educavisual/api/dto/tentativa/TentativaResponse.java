package br.com.educavisual.api.dto.tentativa;

public record TentativaResponse(
    Long id,
    Long usuarioId,
    Long exercicioId,
    Long alternativaId,
    Boolean correta,
    Integer pontuacao,
    String imagemExplicacao
) {}
