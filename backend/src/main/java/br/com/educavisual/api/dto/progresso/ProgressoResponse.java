package br.com.educavisual.api.dto.progresso;

/**
 * Progresso do aluno em uma matéria.
 *
 * <p>"tentativas*" contam cada resposta enviada (refazer conta de novo). "exercicios*" contam
 * exercícios diferentes: respondidos pelo menos uma vez e dominados (acertados pelo menos uma vez).
 */
public record ProgressoResponse(
    Long alunoId,
    Long materiaId,
    String materia,
    long tentativasRespondidas,
    long tentativasCorretas,
    long tentativasErradas,
    int pontuacao,
    double percentualAcertos,
    long exerciciosRespondidos,
    long exerciciosDominados,
    long totalExercicios,
    double percentualConclusao
) {}
