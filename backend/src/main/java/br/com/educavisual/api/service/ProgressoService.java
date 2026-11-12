package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.progresso.ProgressoResponse;
import br.com.educavisual.api.entity.Materia;
import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.enums.TipoUsuario;
import br.com.educavisual.api.exception.AcessoNegadoException;
import br.com.educavisual.api.exception.RegraNegocioException;
import br.com.educavisual.api.repository.ExercicioRepository;
import br.com.educavisual.api.repository.TentativaRepository;
import br.com.educavisual.api.security.AppUserPrincipal;
import br.com.educavisual.api.security.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProgressoService {

    private final TentativaRepository tentativaRepository;
    private final ExercicioRepository exercicioRepository;
    private final UsuarioService usuarioService;
    private final MateriaService materiaService;
    private final ResponsavelAlunoService responsavelAlunoService;

    @Transactional(readOnly = true)
    public ProgressoResponse obter(Long alunoId, Long materiaId) {
        validarAcesso(alunoId);
        Usuario aluno = buscarAluno(alunoId);
        return calcular(aluno, materiaService.buscarEntidade(materiaId));
    }

    /** Progresso de todas as matérias ativas, em uma única chamada. */
    @Transactional(readOnly = true)
    public List<ProgressoResponse> obterTodas(Long alunoId) {
        validarAcesso(alunoId);
        Usuario aluno = buscarAluno(alunoId);
        return materiaService.listarEntidadesAtivas().stream()
            .map(materia -> calcular(aluno, materia))
            .toList();
    }

    private Usuario buscarAluno(Long alunoId) {
        Usuario aluno = usuarioService.buscarEntidade(alunoId);
        if (aluno.getTipoUsuario() != TipoUsuario.ALUNO) {
            throw new RegraNegocioException("O progresso só pode ser consultado para um ALUNO.");
        }
        return aluno;
    }

    private ProgressoResponse calcular(Usuario aluno, Materia materia) {
        Long alunoId = aluno.getId();
        Long materiaId = materia.getId();

        long respondidas = tentativaRepository.countByUsuarioIdAndExercicioMateriaId(alunoId, materiaId);
        long corretas = tentativaRepository.countByUsuarioIdAndExercicioMateriaIdAndCorretaTrue(alunoId, materiaId);
        long erradas = tentativaRepository.countByUsuarioIdAndExercicioMateriaIdAndCorretaFalse(alunoId, materiaId);
        Integer pontos = tentativaRepository.somarPontuacaoPorUsuarioEMateria(alunoId, materiaId);
        double percentual = respondidas == 0 ? 0.0 : (corretas * 100.0) / respondidas;

        long exerciciosRespondidos = tentativaRepository.contarExerciciosRespondidos(alunoId, materiaId);
        long exerciciosDominados = tentativaRepository.contarExerciciosAcertados(alunoId, materiaId);
        long totalExercicios = exercicioRepository.countByMateriaIdAndAtivoTrue(materiaId);
        double conclusao = totalExercicios == 0 ? 0.0 : (exerciciosDominados * 100.0) / totalExercicios;

        return new ProgressoResponse(
            alunoId,
            materiaId,
            materia.getNome(),
            respondidas,
            corretas,
            erradas,
            pontos == null ? 0 : pontos,
            arredondar(percentual),
            exerciciosRespondidos,
            exerciciosDominados,
            totalExercicios,
            arredondar(conclusao)
        );
    }

    private static double arredondar(double valor) {
        return Math.round(valor * 100.0) / 100.0;
    }

    private void validarAcesso(Long alunoId) {
        AppUserPrincipal principal = SecurityUtils.principalAtual();

        if (principal.tipoUsuario() == TipoUsuario.ALUNO) {
            if (!principal.id().equals(alunoId)) {
                throw new AcessoNegadoException("O aluno só pode visualizar o próprio progresso.");
            }
            return;
        }

        if (principal.tipoUsuario() == TipoUsuario.RESPONSAVEL) {
            if (!responsavelAlunoService.possuiVinculo(principal.id(), alunoId)) {
                throw new AcessoNegadoException("O aluno não está vinculado a este responsável.");
            }
            return;
        }

        throw new AcessoNegadoException("Perfil sem permissão para consultar progresso.");
    }
}
