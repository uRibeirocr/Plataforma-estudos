package br.com.educavisual.api.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(RecursoNaoEncontradoException.class)
    public ResponseEntity<ApiError> handleNotFound(RecursoNaoEncontradoException ex,
                                                    HttpServletRequest request) {
        return build(HttpStatus.NOT_FOUND, ex.getMessage(), request, Map.of());
    }

    @ExceptionHandler(RegraNegocioException.class)
    public ResponseEntity<ApiError> handleBusiness(RegraNegocioException ex,
                                                    HttpServletRequest request) {
        return build(HttpStatus.BAD_REQUEST, ex.getMessage(), request, Map.of());
    }

    @ExceptionHandler(AcessoNegadoException.class)
    public ResponseEntity<ApiError> handleForbidden(AcessoNegadoException ex,
                                                     HttpServletRequest request) {
        return build(HttpStatus.FORBIDDEN, ex.getMessage(), request, Map.of());
    }

    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<ApiError> handleBadCredentials(BadCredentialsException ex,
                                                          HttpServletRequest request) {
        return build(HttpStatus.UNAUTHORIZED, "Usuário ou senha inválidos.", request, Map.of());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiError> handleValidation(MethodArgumentNotValidException ex,
                                                      HttpServletRequest request) {
        Map<String, String> fields = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            fields.putIfAbsent(error.getField(), error.getDefaultMessage())
        );
        return build(HttpStatus.BAD_REQUEST, "Dados inválidos.", request, fields);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiError> handleUnexpected(Exception ex,
                                                      HttpServletRequest request) {
        return build(HttpStatus.INTERNAL_SERVER_ERROR,
            "Erro interno inesperado.", request, Map.of());
    }

    private ResponseEntity<ApiError> build(HttpStatus status,
                                           String message,
                                           HttpServletRequest request,
                                           Map<String, String> fieldErrors) {
        ApiError body = new ApiError(
            Instant.now(),
            status.value(),
            status.getReasonPhrase(),
            message,
            request.getRequestURI(),
            fieldErrors
        );
        return ResponseEntity.status(status).body(body);
    }
}
