# Padrões de Git, Commits Semânticos e Governança

## 1. Visão Geral

Este documento detalha o padrão de rastreabilidade de código e histórico adotado no projeto, fundamentado em **Conventional Commits** e entregas atômicas orientadas a especificações (Spec-Driven Development).

---

## 2. Estrutura da Mensagem de Commit

Todo commit no repositório segue rigorosamente a sintaxe:

```text
<tipo>(<escopo>): <descrição no imperativo e em minúsculas>

[corpo opcional explicando o porquê da mudança]
```

### 2.1 Tipos Permitidos
* `feat`: Nova funcionalidade implementada (queries, componentes da UI, simulador).
* `fix`: Correção de bug em fórmulas ou validação de integridade.
* `spec`: Criação ou atualização de especificações técnicas em `specs/`.
* `docs`: Alterações exclusivamente em documentação técnica (`docs/` ou `README.md`).
* `perf`: Otimização de tempo de execução de consulta SQL.
* `refactor`: Refatoração estrutural sem alteração de comportamento.
* `chore`: Configurações de infraestrutura, Docker e dependências no `pyproject.toml`.

### 2.2 Escopos Recomendados
* `db`: DDL, tabelas e conexões com DuckDB.
* `data-gen`: Módulo de geração de dados sintéticos via Faker.
* `queries`: Consultas em SQL puro e agregações.
* `dashboard`: Telas, gráficos e componentes do Streamlit.
* `cep`: Cartas de controle estatístico e limites 3-sigma.
* `simulation`: Simulação paramétrica e matriz de sensibilidade.
* `docker`: Dockerfile e docker-compose.
