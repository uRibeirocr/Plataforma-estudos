package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.ResponsavelAluno;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ResponsavelAlunoRepository extends JpaRepository<ResponsavelAluno, Long> {
    boolean existsByResponsavelIdAndAlunoId(Long responsavelId, Long alunoId);
    List<ResponsavelAluno> findAllByResponsavelIdOrderByAlunoNomeAsc(Long responsavelId);
}
