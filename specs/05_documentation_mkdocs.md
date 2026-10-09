# Especificação de Documentação com MkDocs e Material Theme

## 1. Objetivo
Definir a arquitetura, configuração e organização da documentação técnica e de negócio do projeto utilizando o **MkDocs** com o tema **Material for MkDocs**, permitindo que as specs se transformem em um site estático navegável, moderno e auditável.

---

## 2. Estrutura de Diretórios da Documentação

A pasta `docs/` concentrará os arquivos de conteúdo, estruturados em paralelo às especificações:

```text
.
├── mkdocs.yml                  # Configuração global do MkDocs
├── pyproject.toml              # Dependências (mkdocs-material, pymdown-extensions)
├── specs/                      # Fonte da verdade das especificações
└── docs/
    ├── index.md                # Visão geral e introdução ao projeto
    ├── negocio/
    │   ├── contexto_setor.md   # Modelo de negócio (Planos, Lojas, Sinistros)
    │   └── kpis_regras.md      # Fórmulas, MRR, Churn, Breakeven e CEP
    ├── engenharia/
    │   ├── arquitetura.md      # Pipeline: Faker -> DuckDB -> SQL -> Streamlit
    │   └── contrato_dados.md   # Dicionário de dados e constelação de fatos
    ├── catalogo/
    │   └── glossario_metricas.md # Catálogo de dados, métricas, siglas e OKRs
    ├── manual/
    │   └── operacao.md         # Como executar via uv e navegar pelo dashboard
    └── governanca/
        └── padroes_git.md      # Commits semânticos e boas práticas
```

---

## 3. Configuração do `mkdocs.yml`

O arquivo `mkdocs.yml` na raiz do repositório deve adotar a seguinte estrutura:

```yaml
site_name: Planning & Performance Analytics
site_description: Plataforma de Inteligência Analítica, Simulação e CEP para Gestão Estratégica
site_author: Rafael Rodrigues

theme:
  name: material
  language: pt-BR
  palette:
    # Modo Claro
    - scheme: default
      primary: indigo
      accent: blue
      toggle:
        icon: material/weather-sunny
        name: Alternar para modo escuro
    # Modo Escuro
    - scheme: slate
      primary: indigo
      accent: blue
      toggle:
        icon: material/weather-night
        name: Alternar para modo claro
  features:
    - navigation.instant
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.arithmatex:
      generic: true
  - admonition
  - tables
  - attr_list

extra_javascript:
  - [https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js](https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js)

nav:
  - Início: index.md
  - Negócio & Métricas:
      - Visão Geral do Setor: negocio/contexto_setor.md
      - Regras de Negócio e KPIs: negocio/kpis_regras.md
  - Engenharia & Dados:
      - Arquitetura da Solução: engenharia/arquitetura.md
      - Contrato de Dados: engenharia/contrato_dados.md
  - Catálogo & Governança:
      - Catálogo de Dados, Métricas e OKRs: catalogo/glossario_metricas.md
      - Padrões de Commit & Git: governanca/padroes_git.md
  - Execução:
      - Manual de Operação: manual/operacao.md
```

---

## 4. Dependências no `pyproject.toml`

Adicionar ao grupo opcional de documentação:

```toml
[project.optional-dependencies]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
    "pymdown-extensions>=10.7"
]
```

---

## 5. Fluxo de Trabalho e Comandos com `uv`

### 1. Instalar dependências de documentação
```bash
uv pip install -e ".[docs]"
```

### 2. Executar o servidor local de desenvolvimento (Hot-reload)
```bash
uv run mkdocs serve
```
Acessível via navegador em `http://127.0.0.1:8000`.

### 3. Compilar os arquivos estáticos de produção
```bash
uv run mkdocs build --clean
```
Os arquivos HTML compilados serão gerados na pasta `site/`.