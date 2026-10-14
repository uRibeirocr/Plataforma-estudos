package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.usuario.UsuarioResponse;
import br.com.educavisual.api.dto.vinculo.VinculoRequest;
import br.com.educavisual.api.entity.ResponsavelAluno;
import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.enums.TipoUsuario;
import br.com.educavisual.api.exception.AcessoNegadoException;
import br.com.educavisual.api.exception.RegraNegocioException;
import br.com.educavisual.api.mapper.UsuarioMapper;
import br.com.educavisual.api.repository.ResponsavelAlunoRepository;
import br.com.educavisual.api.security.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ResponsavelAlunoService {

    private final ResponsavelAlunoRepository responsavelAlunoRepository;
    private final UsuarioService usuarioService;

    @Transactional
    public void vincular(VinculoRequest request) {
        if (!SecurityUtils.usuarioIdAtual().equals(request.responsavelId())) {
            throw new AcessoNegadoException("O responsável só pode criar vínculos em seu próprio perfil.");
        }

        Usuario responsavel = usuarioService.buscarEntidade(request.responsavelId());
        Usuario aluno = usuarioService.buscarEntidade(request.alunoId());

        if (responsavel.getTipoUsuario() != TipoUsuario.RESPONSAVEL) {
            throw new RegraNegocioException("O usuário informado como responsável não possui esse perfil.");
        }
        if (aluno.getTipoUsuario() != TipoUsuario.ALUNO) {
            throw new RegraNegocioException("O usuário vinculado precisa ser do tipo ALUNO.");
        }
        if (responsavelAlunoRepository.existsByResponsavelIdAndAlunoId(responsavel.getId(), aluno.getId())) {
            throw new RegraNegocioException("Este aluno já está vinculado ao responsável.");
        }

        responsavelAlunoRepository.save(ResponsavelAluno.builder()
            .responsavel(responsavel)
            .aluno(aluno)
            .build());
    }

    @Transactional(readOnly = true)
    public List<UsuarioResponse> listarAlunos(Long responsavelId) {
        if (!SecurityUtils.usuarioIdAtual().equals(responsavelId)) {
            throw new AcessoNegadoException("O responsável só pode consultar seus próprios alunos vinculados.");
        }

        return responsavelAlunoRepository.findAllByResponsavelIdOrderByAlunoNomeAsc(responsavelId).stream()
            .map(ResponsavelAluno::getAluno)
            .map(UsuarioMapper::toResponse)
            .toList();
    }

    @Transactional(readOnly = true)
    public boolean possuiVinculo(Long responsavelId, Long alunoId) {
        return responsavelAlunoRepository.existsByResponsavelIdAndAlunoId(responsavelId, alunoId);
    }
}
