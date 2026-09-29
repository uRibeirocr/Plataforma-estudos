package br.com.educavisual.api.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(
    name = "responsavel_aluno",
    uniqueConstraints = @UniqueConstraint(
        name = "uk_responsavel_aluno",
        columnNames = {"responsavel_id", "aluno_id"}
    )
)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ResponsavelAluno {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "responsavel_id", nullable = false)
    private Usuario responsavel;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "aluno_id", nullable = false)
    private Usuario aluno;
}
