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

    /** Código estável do conteúdo (ex.: M05, G12). Usado para sincronizar o seed sem duplicar. */
    @Column(unique = true, length = 20)
    private String codigo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private TipoExercicio tipo;

    /** Enunciado em texto (também usado pelo leitor de voz do frontend). */
    @Column(length = 500)
    private String pergunta;

    /** Explicação em texto, exibida somente depois que o aluno responde. */
    @Column(length = 1000)
    private String explicacao;

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
