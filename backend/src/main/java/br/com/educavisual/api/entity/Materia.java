package br.com.educavisual.api.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "materias")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Materia {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 60)
    private String nome;

    @Column(nullable = false, length = 255)
    private String descricao;

    @Column(nullable = false)
    private Boolean ativo;
}
