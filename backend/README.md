# API de contingência

Esta API usa SQLite e a biblioteca padrão do Python. Ela foi criada na branch
`feat/sistema-completo-emergencia` para demonstrar o sistema completo sem
alterar a implementação Spring Boot planejada pela equipe.

## Executar

Na raiz do repositório:

```powershell
python backend/server.py
```

A API inicia em `http://127.0.0.1:8080`. O banco local é criado em
`backend/data/plataforma.db` e não é versionado.
