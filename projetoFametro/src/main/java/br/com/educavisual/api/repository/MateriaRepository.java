package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Materia;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface MateriaRepository extends JpaRepository<Materia, Long> {
    Optional<Materia> findByNomeIgnoreCase(String nome);
    List<Materia> findAllByAtivoTrueOrderByNomeAsc();
}
