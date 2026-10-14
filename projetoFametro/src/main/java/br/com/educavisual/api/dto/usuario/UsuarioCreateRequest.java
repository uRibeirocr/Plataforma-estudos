package br.com.educavisual.api.dto.usuario;

import br.com.educavisual.api.enums.TipoUsuario;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record UsuarioCreateRequest(
    @NotBlank @Size(max = 120) String nome,
    @NotBlank @Size(min = 6, max = 100) String senha,
    @NotNull TipoUsuario tipoUsuario
) {}
