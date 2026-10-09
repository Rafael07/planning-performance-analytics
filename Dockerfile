# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Instala ferramentas do sistema e uv
COPY --from=ghcr.io/astral-sh/uv:0.5.27 /uv /bin/uv

WORKDIR /app

# Variáveis de ambiente
ENV UV_SYSTEM_PYTHON=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Copia arquivos de configuração e dependências
COPY pyproject.toml README.md ./

# Instala dependências usando uv
RUN uv pip install --system -e ".[docs]"

# Copia código fonte, specs e documentação
COPY src/ ./src/
COPY specs/ ./specs/
COPY mkdocs.yml ./
COPY app.py ./

# Inicializa o banco de dados colunar DuckDB e valida contratos
RUN python -m src.database

# Expõe a porta do Streamlit (8501) e do MkDocs (8000)
EXPOSE 8501 8000

# Comando padrão: inicia a aplicação executiva Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
