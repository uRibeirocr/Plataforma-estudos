package br.com.educavisual.api.controller;

import br.com.educavisual.api.dto.usuario.UsuarioResponse;
import br.com.educavisual.api.dto.vinculo.VinculoRequest;
import br.com.educavisual.api.service.ResponsavelAlunoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/responsaveis")
@RequiredArgsConstructor
@PreAuthorize("hasRole('RESPONSAVEL')")
public class ResponsavelAlunoController {

    private final ResponsavelAlunoService responsavelAlunoService;

    @PostMapping("/vinculos")
    public ResponseEntity<Void> vincular(@Valid @RequestBody VinculoRequest request) {
        responsavelAlunoService.vincular(request);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @GetMapping("/{responsavelId}/alunos")
    public ResponseEntity<List<UsuarioResponse>> listarAlunos(@PathVariable Long responsavelId) {
        return ResponseEntity.ok(responsavelAlunoService.listarAlunos(responsavelId));
    }
}
