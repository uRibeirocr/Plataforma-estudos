package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    Optional<Usuario> findByNomeIgnoreCase(String nome);
    boolean existsByNomeIgnoreCase(String nome);
}
