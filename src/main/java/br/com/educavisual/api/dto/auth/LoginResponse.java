package br.com.educavisual.api.dto.auth;

import br.com.educavisual.api.enums.TipoUsuario;

public record LoginResponse(
    Long id,
    String nome,
    TipoUsuario tipoUsuario,
    String token
) {}
