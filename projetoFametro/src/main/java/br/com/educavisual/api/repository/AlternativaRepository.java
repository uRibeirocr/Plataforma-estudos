package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Alternativa;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AlternativaRepository extends JpaRepository<Alternativa, Long> {
    List<Alternativa> findAllByExercicioIdOrderByIdAsc(Long exercicioId);
}
