"""Gera o site estático (versão web das atividades) em _site/.

Uso (da raiz do repositório):  python site/build_site.py [pasta_de_saida]
O site é 100% estático: index.html + questoes.json + assets/ (imagens). Não precisa de servidor.
"""
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from validar_conteudo import validar  # noqa: E402


def gerar(saida: Path) -> None:
    problemas = validar()
    if problemas:
        raise SystemExit("Conteúdo inválido:\n" + "\n".join(f"- {p}" for p in problemas))

    if saida.exists():
        shutil.rmtree(saida)
    saida.mkdir(parents=True)
    shutil.copy(RAIZ / "site" / "index.html", saida / "index.html")
    shutil.copy(RAIZ / "conteudo" / "questoes.json", saida / "questoes.json")
    shutil.copytree(RAIZ / "frontend" / "assets", saida / "assets")
    (saida / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Site gerado em {saida} ({sum(1 for _ in saida.rglob('*') if _.is_file())} arquivos)")


if __name__ == "__main__":
    gerar(Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "_site")
