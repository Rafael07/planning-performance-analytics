# Planning & Performance Analytics (Projeto Integra-Dignidade)

Plataforma integrada de inteligência analítica, simulação de cenários paramétricos e controle estatístico de processos (CEP) para empresas de assistência familiar e planos funerários.

O projeto adota a metodologia **Spec-Driven Development (SDD)**, com regras de negócio, arquitetura e contratos de dados formalizados na pasta `specs/`.

---

## 1. Estrutura do Repositório

```text
.
├── README.md
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── mkdocs.yml
├── specs/
│   ├── 01_prd.md
│   ├── 02_architecture_and_contract.md
│   ├── 03_business_rules_use_cases.md
│   ├── 04_git_commit_standards.md
│   ├── 05_documentation_mkdocs.md
│   └── 06_data_catalog_and_glossary.md
├── docs/
│   ├── index.md
│   ├── negocio/
│   ├── engenharia/
│   ├── manual/
│   └── governanca/
├── data/
│   └── acolher_analytics.duckdb
├── src/
│   ├── __init__.py
│   ├── data_generator.py      # Geração de dados sintéticos via Faker
│   ├── database.py            # Criação do schema DDL e ingestão no DuckDB
│   └── queries.py             # Métricas, agregações e views analíticas em SQL
└── app.py                     # Interface executiva e simulador com Streamlit
```

---

## 2. Pilares Funcionais

* **Visão Executiva & Metas (BSC):** Monitoramento de MRR, Taxa de Churn, Inadimplência e Sinistralidade por unidade física e tipo de plano.
* **Simulador de Sensibilidade Paramétrica:** Projeção dinâmica do impacto de variações de preço, elasticidade de cancelamento e custos no resultado operacional da empresa.
* **Controle Estatístico de Processo (CEP):** Monitoramento da variabilidade do tempo de ciclo de atendimento com limites estatísticos de três desvios padrão.
* **Funil Comercial das Unidades:** Visão do pipeline de captação de clientes em lojas de apoio para acompanhamento do ritmo de vendas.

---

## 3. Tecnologias Utilizadas

* **Linguagem:** Python 3.13
* **Gerenciamento de Pacotes:** `uv` via `pyproject.toml`
* **Motor Analítico:** DuckDB (processamento colunar local de baixa latência)
* **Visualização & Interface:** Streamlit e Plotly
* **Geração Sintética:** Faker e NumPy
* **Container:** Docker
* **Documentação:** MkDocs

---

## 4. Instruções de Execução

### 0. Clonar o repositório
```bash
git clone https://github.com/Rafael07/planning-performance-analytics.git
cd planning-performance-analytics
```

### 1. Criar o ambiente virtual e instalar dependências
```bash
uv venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
uv pip install -e .
```

### 2. Gerar a base de dados sintética e popular o DuckDB (Opcional — Auto-inicializa na 1ª execução)
```bash
uv run python -m src.database
```

### 3. Iniciar o painel de apoio à decisão
```bash
uv run streamlit run app.py
```

### 4. Servir a documentação técnica (MkDocs)
```bash
uv run mkdocs serve
```

### 5. Execução Conteinerizada via Docker (Tudo em 1 comando)
```bash
docker compose up --build
```
* **Aplicação Executiva (Streamlit):** [http://localhost:8501](http://localhost:8501)
* **Documentação Viva (MkDocs):** [http://localhost:8000](http://localhost:8000)

---

## 5. Especificações do Projeto (SDD)

As diretrizes funcionais, contratos relacionais e formulações matemáticas estão documentados em:
* [01 - PRD Funcional](specs/01_prd.md)
* [02 - Arquitetura Técnica e Contrato de Dados](specs/02_architecture_and_contract.md)
* [03 - Regras de Negócio e Casos de Uso](specs/03_business_rules_use_cases.md)
* [04 - Padrões de Commit & Git](specs/04_git_commit_standards.md)
* [05 - Especificação da Documentação com MkDocs](specs/05_documentation_mkdocs.md)
* [06 - Catálogo de Dados, Métricas e Glossário](specs/06_data_catalog_and_glossary.md)