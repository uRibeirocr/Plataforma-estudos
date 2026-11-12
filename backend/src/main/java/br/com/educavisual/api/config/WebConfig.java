package br.com.educavisual.api.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Path;

/** Serve as imagens dos exercícios em {@code /imagens/**} para clientes web (somente leitura). */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final Path imagensDir;

    public WebConfig(@Value("${app.imagens-dir:../frontend/assets}") String imagensDir) {
        this.imagensDir = Path.of(imagensDir).toAbsolutePath().normalize();
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        String local = imagensDir.toUri().toString();
        if (!local.endsWith("/")) {
            local += "/";
        }
        registry.addResourceHandler("/imagens/**").addResourceLocations(local);
    }
}
