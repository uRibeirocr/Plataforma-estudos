package br.com.educavisual.api.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "alternativas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Alternativa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Letra exibida ao aluno (A, B, C, D). */
    @Column(length = 5)
    private String letra;

    /** Texto opcional (ex.: o número "16"). Em geografia fica vazio para não revelar o país. */
    @Column(length = 200)
    private String texto;

    @Column(nullable = false, length = 500)
    private String imagem;

    @Column(nullable = false)
    private Boolean correta;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "exercicio_id", nullable = false)
    private Exercicio exercicio;
}
