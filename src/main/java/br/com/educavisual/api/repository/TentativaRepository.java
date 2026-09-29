package br.com.educavisual.api.repository;

import br.com.educavisual.api.entity.Tentativa;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TentativaRepository extends JpaRepository<Tentativa, Long> {

    List<Tentativa> findAllByUsuarioIdOrderByIdDesc(Long usuarioId);

    long countByUsuarioIdAndExercicioMateriaId(Long usuarioId, Long materiaId);

    long countByUsuarioIdAndExercicioMateriaIdAndCorretaTrue(Long usuarioId, Long materiaId);

    long countByUsuarioIdAndExercicioMateriaIdAndCorretaFalse(Long usuarioId, Long materiaId);

    @Query("""
        select coalesce(sum(t.pontuacao), 0)
        from Tentativa t
        where t.usuario.id = :usuarioId
          and t.exercicio.materia.id = :materiaId
        """)
    Integer somarPontuacaoPorUsuarioEMateria(@Param("usuarioId") Long usuarioId,
                                             @Param("materiaId") Long materiaId);
}
