# Manual de Operação e Execução

## 1. Pré-Requisitos

* Python 3.13+ instalado (ou Docker)
* Gerenciador de pacotes `uv` (recomendado) ou `pip`
* Git configurado

---

## 2. Execução Local via `uv`

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/<seu-usuario>/planning-performance-analytics.git
cd planning-performance-analytics
```

### Passo 2: Instalar Dependências
```bash
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -e ".[docs]"
```

### Passo 3: Inicializar a Base DuckDB e Validar Contratos
```bash
uv run python -m src.database
```

### Passo 4: Executar a Aplicação Executiva
```bash
uv run streamlit run app.py
```
O painel estará acessível no navegador em `http://localhost:8501`.

### Passo 5: Servir a Documentação Técnica
```bash
uv run mkdocs serve
```
A documentação interativa estará acessível em `http://localhost:8000`.

---

## 3. Execução Conteinerizada via Docker

Para executar a solução completa com um único comando sem instalar ferramentas locais:

```bash
docker compose up --build
```

* **Aplicação Executiva (Streamlit):** [http://localhost:8501](http://localhost:8501)
* **Documentação Viva (MkDocs):** [http://localhost:8000](http://localhost:8000)
