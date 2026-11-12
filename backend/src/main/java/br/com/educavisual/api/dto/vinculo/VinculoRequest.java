package br.com.educavisual.api.dto.vinculo;

/**
 * Pedido de vínculo responsável → aluno.
 *
 * <p>{@code responsavelId} é opcional (assume o usuário autenticado). Informe {@code alunoId}
 * ou {@code alunoNome}; o nome é mais prático para o responsável, que raramente sabe o ID.
 */
public record VinculoRequest(
    Long responsavelId,
    Long alunoId,
    String alunoNome
) {}
