package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.auth.LoginRequest;
import br.com.educavisual.api.dto.auth.LoginResponse;
import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.repository.UsuarioRepository;
import br.com.educavisual.api.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final AuthenticationManager authenticationManager;
    private final UsuarioRepository usuarioRepository;
    private final JwtService jwtService;

    public LoginResponse login(LoginRequest request) {
        authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.nome(), request.senha())
        );

        Usuario usuario = usuarioRepository.findByNomeIgnoreCase(request.nome())
            .orElseThrow(() -> new RecursoNaoEncontradoException("Usuário não encontrado."));

        return new LoginResponse(
            usuario.getId(),
            usuario.getNome(),
            usuario.getTipoUsuario(),
            jwtService.gerarToken(usuario)
        );
    }
}
