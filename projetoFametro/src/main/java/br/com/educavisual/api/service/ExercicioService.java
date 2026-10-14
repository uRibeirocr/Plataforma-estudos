package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.exercicio.ExercicioResponse;
import br.com.educavisual.api.entity.Exercicio;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.mapper.ExercicioMapper;
import br.com.educavisual.api.repository.AlternativaRepository;
import br.com.educavisual.api.repository.ExercicioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ExercicioService {

    private final ExercicioRepository exercicioRepository;
    private final AlternativaRepository alternativaRepository;

    @Transactional(readOnly = true)
    public List<ExercicioResponse> listarPorMateria(Long materiaId) {
        return exercicioRepository.findAllByMateriaIdAndAtivoTrueOrderByIdAsc(materiaId).stream()
            .map(exercicio -> ExercicioMapper.toResponse(
                exercicio,
                alternativaRepository.findAllByExercicioIdOrderByIdAsc(exercicio.getId())
            ))
            .toList();
    }

    @Transactional(readOnly = true)
    public ExercicioResponse buscar(Long id) {
        Exercicio exercicio = buscarEntidade(id);
        return ExercicioMapper.toResponse(
            exercicio,
            alternativaRepository.findAllByExercicioIdOrderByIdAsc(id)
        );
    }

    @Transactional(readOnly = true)
    public Exercicio buscarEntidade(Long id) {
        return exercicioRepository.findById(id)
            .orElseThrow(() -> new RecursoNaoEncontradoException("Exercício não encontrado."));
    }
}
