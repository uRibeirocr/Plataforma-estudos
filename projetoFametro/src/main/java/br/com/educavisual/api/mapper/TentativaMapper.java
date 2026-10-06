package br.com.educavisual.api.mapper;

import br.com.educavisual.api.dto.tentativa.TentativaResponse;
import br.com.educavisual.api.entity.Tentativa;

public final class TentativaMapper {

    private TentativaMapper() {}

    public static TentativaResponse toResponse(Tentativa tentativa) {
        return new TentativaResponse(
            tentativa.getId(),
            tentativa.getUsuario().getId(),
            tentativa.getExercicio().getId(),
            tentativa.getAlternativa().getId(),
            tentativa.getCorreta(),
            tentativa.getPontuacao(),
            tentativa.getExercicio().getImagemExplicacao()
        );
    }
}
