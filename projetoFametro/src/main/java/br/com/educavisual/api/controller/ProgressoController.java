package br.com.educavisual.api.controller;

import br.com.educavisual.api.dto.progresso.ProgressoResponse;
import br.com.educavisual.api.service.ProgressoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/progresso")
@RequiredArgsConstructor
public class ProgressoController {

    private final ProgressoService progressoService;

    @GetMapping("/alunos/{alunoId}/materias/{materiaId}")
    public ResponseEntity<ProgressoResponse> obter(@PathVariable Long alunoId,
                                                   @PathVariable Long materiaId) {
        return ResponseEntity.ok(progressoService.obter(alunoId, materiaId));
    }
}
