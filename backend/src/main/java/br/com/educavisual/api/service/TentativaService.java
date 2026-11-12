package br.com.educavisual.api.service;

import br.com.educavisual.api.dto.tentativa.ResponderExercicioRequest;
import br.com.educavisual.api.dto.tentativa.TentativaResponse;
import br.com.educavisual.api.entity.Alternativa;
import br.com.educavisual.api.entity.Exercicio;
import br.com.educavisual.api.entity.Tentativa;
import br.com.educavisual.api.entity.Usuario;
import br.com.educavisual.api.enums.TipoUsuario;
import br.com.educavisual.api.exception.AcessoNegadoException;
import br.com.educavisual.api.exception.RecursoNaoEncontradoException;
import br.com.educavisual.api.exception.RegraNegocioException;
import br.com.educavisual.api.mapper.TentativaMapper;
import br.com.educavisual.api.repository.AlternativaRepository;
import br.com.educavisual.api.repository.TentativaRepository;
import br.com.educavisual.api.security.SecurityUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class TentativaService {

    public static final int PONTOS_POR_ACERTO = 10;

    private final TentativaRepository tentativaRepository;
    private final AlternativaRepository alternativaRepository;
    private final UsuarioService usuarioService;
    private final ExercicioService exercicioService;

    @Transactional
    public TentativaResponse responder(ResponderExercicioRequest request) {
        Long autenticadoId = SecurityUtils.usuarioIdAtual();
        if (!autenticadoId.equals(request.usuarioId())) {
            throw new AcessoNegadoException("O aluno só pode responder exercícios em seu próprio perfil.");
        }

        Usuario usuario = usuarioService.buscarEntidade(request.usuarioId());
        if (usuario.getTipoUsuario() != TipoUsuario.ALUNO) {
            throw new RegraNegocioException("Apenas usuários do tipo ALUNO podem responder exercícios.");
        }

        Exercicio exercicio = exercicioService.buscarEntidade(request.exercicioId());
        if (!Boolean.TRUE.equals(exercicio.getAtivo())) {
            throw new RegraNegocioException("O exercício está inativo.");
        }

        Alternativa alternativa = alternativaRepository.findById(request.alternativaId())
            .orElseThrow(() -> new RecursoNaoEncontradoException("Alternativa não encontrada."));

        if (!alternativa.getExercicio().getId().equals(exercicio.getId())) {
            throw new RegraNegocioException("A alternativa não pertence ao exercício informado.");
        }

        boolean correta = Boolean.TRUE.equals(alternativa.getCorreta());
        int pontuacao = correta ? PONTOS_POR_ACERTO : 0;

        Tentativa tentativa = tentativaRepository.save(Tentativa.builder()
            .usuario(usuario)
            .exercicio(exercicio)
            .alternativa(alternativa)
            .correta(correta)
            .pontuacao(pontuacao)
            .build());

        Long corretaId = correta
            ? alternativa.getId()
            : alternativaRepository.findFirstByExercicioIdAndCorretaTrue(exercicio.getId())
                .map(Alternativa::getId)
                .orElse(null);

        return TentativaMapper.toResponse(tentativa, corretaId);
    }

    @Transactional(readOnly = true)
    public List<TentativaResponse> listarDoAluno(Long alunoId) {
        if (!SecurityUtils.usuarioIdAtual().equals(alunoId)) {
            throw new AcessoNegadoException("O aluno só pode consultar suas próprias tentativas.");
        }

        List<Tentativa> tentativas = tentativaRepository.findAllByUsuarioIdOrderByIdDesc(alunoId);
        List<Long> exercicioIds = tentativas.stream().map(t -> t.getExercicio().getId()).distinct().toList();

        Map<Long, Long> gabarito = new HashMap<>();
        if (!exercicioIds.isEmpty()) {
            alternativaRepository.findAllByExercicioIdInAndCorretaTrue(exercicioIds)
                .forEach(a -> gabarito.put(a.getExercicio().getId(), a.getId()));
        }

        return tentativas.stream()
            .map(t -> TentativaMapper.toResponse(t, gabarito.get(t.getExercicio().getId())))
            .toList();
    }
}
