package br.com.educavisual.api.controller;

import br.com.educavisual.api.dto.usuario.UsuarioCreateRequest;
import br.com.educavisual.api.dto.usuario.UsuarioResponse;
import br.com.educavisual.api.security.SecurityUtils;
import br.com.educavisual.api.service.UsuarioService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioService usuarioService;

    @PostMapping
    public ResponseEntity<UsuarioResponse> criar(@Valid @RequestBody UsuarioCreateRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(usuarioService.criar(request));
    }

    @GetMapping("/me")
    public ResponseEntity<UsuarioResponse> me() {
        return ResponseEntity.ok(usuarioService.buscar(SecurityUtils.usuarioIdAtual()));
    }
}
