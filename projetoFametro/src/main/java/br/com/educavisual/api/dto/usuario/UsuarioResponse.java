package br.com.educavisual.api.dto.usuario;

import br.com.educavisual.api.enums.TipoUsuario;

public record UsuarioResponse(
    Long id,
    String nome,
    TipoUsuario tipoUsuario
) {}
