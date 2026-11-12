package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Alternativa;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Collection;
import java.util.List;
import java.util.Optional;

public interface AlternativaRepository extends JpaRepository<Alternativa, Long> {
    List<Alternativa> findAllByExercicioIdOrderByIdAsc(Long exercicioId);
    List<Alternativa> findAllByExercicioIdInOrderByIdAsc(Collection<Long> exercicioIds);
    List<Alternativa> findAllByExercicioIdInAndCorretaTrue(Collection<Long> exercicioIds);
    Optional<Alternativa> findFirstByExercicioIdAndCorretaTrue(Long exercicioId);
}
