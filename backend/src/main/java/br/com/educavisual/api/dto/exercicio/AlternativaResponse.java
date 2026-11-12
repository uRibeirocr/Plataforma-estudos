package br.com.educavisual.api.dto.exercicio;

/** Nunca expõe o gabarito: a correção só é revelada depois da tentativa. */
public record AlternativaResponse(
    Long id,
    String letra,
    String texto,
    String imagem
) {}
