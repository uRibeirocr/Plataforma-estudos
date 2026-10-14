package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.materia.MateriaResponse;
import br.com.educavisual.api.entity.Materia;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.mapper.MateriaMapper;
import br.com.educavisual.api.repository.MateriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MateriaService {

    private final MateriaRepository materiaRepository;

    @Transactional(readOnly = true)
    public List<MateriaResponse> listarAtivas() {
        return materiaRepository.findAllByAtivoTrueOrderByNomeAsc().stream()
            .map(MateriaMapper::toResponse)
            .toList();
    }

    @Transactional(readOnly = true)
    public Materia buscarEntidade(Long id) {
        return materiaRepository.findById(id)
            .orElseThrow(() -> new RecursoNaoEncontradoException("Matéria não encontrada."));
    }
}
