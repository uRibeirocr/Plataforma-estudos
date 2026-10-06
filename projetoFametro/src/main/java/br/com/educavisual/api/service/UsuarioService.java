package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.usuario.UsuarioCreateRequest;
import br.com.educavisual.api.dto.usuario.UsuarioResponse;
import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.exception.RegraNegocioException;
import br.com.educavisual.api.mapper.UsuarioMapper;
import br.com.educavisual.api.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public UsuarioResponse criar(UsuarioCreateRequest request) {
        if (usuarioRepository.existsByNomeIgnoreCase(request.nome())) {
            throw new RegraNegocioException("Já existe um usuário com esse nome.");
        }

        Usuario usuario = Usuario.builder()
            .nome(request.nome().trim())
            .senha(passwordEncoder.encode(request.senha()))
            .tipoUsuario(request.tipoUsuario())
            .build();

        return UsuarioMapper.toResponse(usuarioRepository.save(usuario));
    }

    @Transactional(readOnly = true)
    public Usuario buscarEntidade(Long id) {
        return usuarioRepository.findById(id)
            .orElseThrow(() -> new RecursoNaoEncontradoException("Usuário não encontrado."));
    }

    @Transactional(readOnly = true)
    public UsuarioResponse buscar(Long id) {
        return UsuarioMapper.toResponse(buscarEntidade(id));
    }
}
