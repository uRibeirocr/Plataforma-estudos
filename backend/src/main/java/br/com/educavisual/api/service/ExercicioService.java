package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.exercicio.ExercicioResponse;
import br.com.educavisual.api.entity.Alternativa;
import br.com.educavisual.api.entity.Exercicio;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.exception.RegraNegocioException;
import br.com.educavisual.api.mapper.ExercicioMapper;
import br.com.educavisual.api.repository.AlternativaRepository;
import br.com.educavisual.api.repository.ExercicioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ExercicioService {

    private static final int LIMITE_MAXIMO = 200;

    private final ExercicioRepository exercicioRepository;
    private final AlternativaRepository alternativaRepository;
    private final MateriaService materiaService;

    /**
     * Lista os exercícios ativos de uma matéria.
     *
     * @param limite     quantidade máxima de exercícios (null = todos)
     * @param embaralhar sorteia a ordem antes de aplicar o limite (útil para montar uma rodada)
     */
    @Transactional(readOnly = true)
    public List<ExercicioResponse> listarPorMateria(Long materiaId, Integer limite, boolean embaralhar) {
        materiaService.buscarEntidade(materiaId);

        if (limite != null && (limite < 1 || limite > LIMITE_MAXIMO)) {
            throw new RegraNegocioException("O limite deve estar entre 1 e " + LIMITE_MAXIMO + ".");
        }

        List<Exercicio> exercicios = new ArrayList<>(
            exercicioRepository.findAllByMateriaIdAndAtivoTrueOrderByIdAsc(materiaId));
        if (embaralhar) {
            Collections.shuffle(exercicios);
        }
        if (limite != null && limite < exercicios.size()) {
            exercicios = new ArrayList<>(exercicios.subList(0, limite));
        }

        // Uma única consulta para todas as alternativas (evita N+1).
        List<Long> ids = exercicios.stream().map(Exercicio::getId).toList();
        Map<Long, List<Alternativa>> porExercicio = ids.isEmpty()
            ? Map.of()
            : alternativaRepository.findAllByExercicioIdInOrderByIdAsc(ids).stream()
                .collect(Collectors.groupingBy(a -> a.getExercicio().getId()));

        return exercicios.stream()
            .map(e -> ExercicioMapper.toResponse(e, porExercicio.getOrDefault(e.getId(), List.of())))
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
