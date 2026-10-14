package br.com.educavisual.api.mapper;

import br.com.educavisual.api.dto.usuario.UsuarioResponse;
import br.com.educavisual.api.entity.Usuario;

public final class UsuarioMapper {

    private UsuarioMapper() {}

    public static UsuarioResponse toResponse(Usuario usuario) {
        return new UsuarioResponse(
            usuario.getId(),
            usuario.getNome(),
            usuario.getTipoUsuario()
        );
    }
}
