package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Exercicio;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ExercicioRepository extends JpaRepository<Exercicio, Long> {
    List<Exercicio> findAllByMateriaIdAndAtivoTrueOrderByIdAsc(Long materiaId);
    long countByMateriaIdAndAtivoTrue(Long materiaId);
    boolean existsByPergunta(String pergunta);
    Optional<Exercicio> findByPergunta(String pergunta);
    List<Exercicio> findAllByPerguntaOrderByIdAsc(String pergunta);
}
