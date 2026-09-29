package br.com.educavisual.api.mapper;

import br.com.educavisual.api.dto.materia.MateriaResponse;
import br.com.educavisual.api.entity.Materia;

public final class MateriaMapper {

    private MateriaMapper() {}

    public static MateriaResponse toResponse(Materia materia) {
        return new MateriaResponse(
            materia.getId(),
            materia.getNome(),
            materia.getDescricao(),
            materia.getAtivo()
        );
    }
}
