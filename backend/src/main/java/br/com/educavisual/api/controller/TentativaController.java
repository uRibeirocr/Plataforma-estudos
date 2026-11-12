package br.com.educavisual.api.controller;

import br.com.educavisual.api.dto.tentativa.ResponderExercicioRequest;
import br.com.educavisual.api.dto.tentativa.TentativaResponse;
import br.com.educavisual.api.service.TentativaService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tentativas")
@RequiredArgsConstructor
public class TentativaController {

    private final TentativaService tentativaService;

    @PostMapping
    @PreAuthorize("hasRole('ALUNO')")
    public ResponseEntity<TentativaResponse> responder(@Valid @RequestBody ResponderExercicioRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(tentativaService.responder(request));
    }

    @GetMapping("/aluno/{alunoId}")
    @PreAuthorize("hasRole('ALUNO')")
    public ResponseEntity<List<TentativaResponse>> listarDoAluno(@PathVariable Long alunoId) {
        return ResponseEntity.ok(tentativaService.listarDoAluno(alunoId));
    }
}
