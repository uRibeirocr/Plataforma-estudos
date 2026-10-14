package br.com.educavisual.api.entity;

import br.com.educavisual.api.enums.TipoExercicio;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "exercicios")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Exercicio {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private TipoExercicio tipo;

    @Column(nullable = false, length = 500)
    private String imagemPergunta;

    @Column(length = 500)
    private String imagemExplicacao;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "materia_id", nullable = false)
    private Materia materia;

    @Column(nullable = false)
    private Boolean ativo;
}
