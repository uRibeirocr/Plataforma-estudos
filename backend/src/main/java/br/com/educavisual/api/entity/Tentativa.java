package br.com.educavisual.api.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "tentativas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Tentativa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "usuario_id", nullable = false)
    private Usuario usuario;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "exercicio_id", nullable = false)
    private Exercicio exercicio;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "alternativa_id", nullable = false)
    private Alternativa alternativa;

    @Column(nullable = false)
    private Boolean correta;

    @Column(nullable = false)
    private Integer pontuacao;
}
