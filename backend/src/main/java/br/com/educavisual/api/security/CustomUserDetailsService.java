package br.com.educavisual.api.security;

import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private final UsuarioRepository usuarioRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Usuario usuario = usuarioRepository.findByNomeIgnoreCase(username)
            .orElseThrow(() -> new UsernameNotFoundException("Usuário não encontrado."));
        return AppUserPrincipal.from(usuario);
    }
}
