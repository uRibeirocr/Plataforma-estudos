package br.com.educavisual.api.security;

import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.enums.TipoUsuario;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

public record AppUserPrincipal(
    Long id,
    String nome,
    String senha,
    TipoUsuario tipoUsuario
) implements UserDetails {

    public static AppUserPrincipal from(Usuario usuario) {
        return new AppUserPrincipal(
            usuario.getId(),
            usuario.getNome(),
            usuario.getSenha(),
            usuario.getTipoUsuario()
        );
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_" + tipoUsuario.name()));
    }

    @Override
    public String getPassword() {
        return senha;
    }

    @Override
    public String getUsername() {
        return nome;
    }
}
