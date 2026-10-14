package br.com.educavisual.api.dto.progresso;

public record ProgressoResponse(
    Long alunoId,
    Long materiaId,
    String materia,
    long tentativasRespondidas,
    long tentativasCorretas,
    long tentativasErradas,
    int pontuacao,
    double percentualAcertos
) {}
