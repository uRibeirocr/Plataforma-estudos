package br.com.educavisual.api.security;

import br.com.educavisual.api.entity.Usuario;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

@Service
public class JwtService {

    private final SecretKey key;
    private final long expirationMs;

    public JwtService(@Value("${app.jwt.secret}") String secret,
                      @Value("${app.jwt.expiration-ms}") long expirationMs) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.expirationMs = expirationMs;
    }

    public String gerarToken(Usuario usuario) {
        Date now = new Date();
        Date expiration = new Date(now.getTime() + expirationMs);

        return Jwts.builder()
            .subject(usuario.getNome())
            .claim("userId", usuario.getId())
            .claim("role", usuario.getTipoUsuario().name())
            .issuedAt(now)
            .expiration(expiration)
            .signWith(key)
            .compact();
    }

    public String extrairNome(String token) {
        return claims(token).getSubject();
    }

    public boolean tokenValido(String token, String username) {
        Claims claims = claims(token);
        return claims.getSubject().equalsIgnoreCase(username)
            && claims.getExpiration().after(new Date());
    }

    private Claims claims(String token) {
        return Jwts.parser()
            .verifyWith(key)
            .build()
            .parseSignedClaims(token)
            .getPayload();
    }
}
