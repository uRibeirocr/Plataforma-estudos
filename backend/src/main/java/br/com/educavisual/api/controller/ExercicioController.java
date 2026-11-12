package br.com.educavisual.api.controller;

import br.com.educavisual.api.dto.exercicio.ExercicioResponse;
import br.com.educavisual.api.service.ExercicioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/exercicios")
@RequiredArgsConstructor
public class ExercicioController {

    private final ExercicioService exercicioService;

    @GetMapping("/{id}")
    public ResponseEntity<ExercicioResponse> buscar(@PathVariable Long id) {
        return ResponseEntity.ok(exercicioService.buscar(id));
    }

    /** Ex.: GET /api/exercicios/materia/1?limite=10&embaralhar=true monta uma rodada de 10 questões. */
    @GetMapping("/materia/{materiaId}")
    public ResponseEntity<List<ExercicioResponse>> listarPorMateria(
        @PathVariable Long materiaId,
        @RequestParam(required = false) Integer limite,
        @RequestParam(defaultValue = "false") boolean embaralhar) {
        return ResponseEntity.ok(exercicioService.listarPorMateria(materiaId, limite, embaralhar));
    }
}
