package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Exercicio;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ExercicioRepository extends JpaRepository<Exercicio, Long> {
    List<Exercicio> findAllByMateriaIdAndAtivoTrueOrderByIdAsc(Long materiaId);
    long countByMateriaIdAndAtivoTrue(Long materiaId);
    boolean existsByPergunta(String pergunta);
}
