package br.com.educavisual.api.dto.materia;

public record MateriaResponse(
    Long id,
    String nome,
    String descricao,
    Boolean ativo
) {}
