package br.com.educavisual.api.security;

import br.com.educavisual.api.exception.AcessoNegadoException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public final class SecurityUtils {

    private SecurityUtils() {}

    public static AppUserPrincipal principalAtual() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof AppUserPrincipal principal)) {
            throw new AcessoNegadoException("Usuário não autenticado.");
        }
        return principal;
    }

    public static Long usuarioIdAtual() {
        return principalAtual().id();
    }

    public static boolean temRole(String role) {
        return principalAtual().getAuthorities().stream()
            .anyMatch(a -> a.getAuthority().equals("ROLE_" + role));
    }
}
