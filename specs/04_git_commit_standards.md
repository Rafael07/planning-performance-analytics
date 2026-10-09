# Padrões de Git, Commits Semânticos e Fluxo de Versionamento

## 1. Visão Geral
Este documento estabelece as diretrizes para padronização de histórico, rastreabilidade e mensagens de commit do projeto, adotando a convenção de **Conventional Commits** e fluxo de branches focado em entrega incremental via Spec-Driven Development (SDD).

---

## 2. Estrutura da Mensagem de Commit

Todo commit deve seguir rigorosamente a sintaxe:

```text
<tipo>(<escopo>): <descrição no imperativo e em minúsculas>

[corpo opcional explicando o porquê da mudança]

[rodapé opcional com referências a issues ou breaking changes]
```

### 2.1 Tipos Permitidos (`<tipo>`)
* `feat`: Nova funcionalidade (ex.: nova view SQL, novo seletor no Streamlit).
* `fix`: Correção de bug ou cálculo incorreto de métrica.
* `spec`: Criação ou atualização de especificações na pasta `specs/`.
* `docs`: Alterações exclusivamente em documentação (ex.: README, MkDocs).
* `refactor`: Refatoração de código sem alteração de comportamento ou regra de negócio.
* `perf`: Otimização de performance de query SQL ou carregamento DuckDB.
* `test`: Adição ou correção de testes automatizados e validações de dados.
* `chore`: Mudanças de infraestrutura local, dependências no `pyproject.toml` ou configs de linters.

### 2.2 Escopos Recomendados (`<escopo>`)
* `data-gen`: Scripts de geração de dados sintéticos (`Faker`).
* `db`: DDL, conexão e tabelas do DuckDB.
* `queries`: Consultas analíticas, agregações e views de KPIs.
* `dashboard`: Telas, abas e componentes da interface Streamlit.
* `cep`: Implementação das cartas de controle estatístico e limites 3-sigma.
* `simulation`: Lógica paramétrica e matriz de sensibilidade.
* `deps`: Dependências e gerenciamento de ambiente (`uv`).

---

## 3. Regras de Estilo para Commits

1. **Descrição no imperativo:** Use *"adiciona..."*, *"corrige..."*, *"implementa..."*, e nunca *"adicionando..."* ou *"adicionei..."*.
2. **Sem ponto final no título:** O título deve ser objetivo e direto (máximo de 72 caracteres).
3. **Língua:** Mensagens em português (ou inglês, desde que mantida a consistência em 100% dos commits).
4. **Commits atômicos:** Cada commit deve conter apenas uma alteração lógica completa. Não misture refatoração de query com ajuste de layout da UI.

---

## 4. Exemplos Práticos de Commits

### Adição de funcionalidade vinculada à spec:
```text
feat(queries): adiciona calculo de breakeven por unidade operacional

Implementa a agregacao em SQL da margem operacional e custo marginal por
contrato, atendendo a secao 1.3 da spec 03_business_rules_use_cases.md.
```

### Correção de consistência:
```text
fix(data-gen): garante preenchimento de data_cancelamento quando churn

Ajusta gerador de fct_contratos para satisfazer a regra de integridade
do contrato de dados.
```

### Atualização de documentação ou spec:
```text
spec(domain): refina limites do controle estatistico para 3-sigma
docs(readme): atualiza instrucoes de inicializacao com uv
```

---

## 5. Estrutura de Branches

* `main`: Código estável, testado e validado contra todas as especificações.
* `feat/<nome-curto>`: Desenvolvimento de novas entregas (ex.: `feat/cep-dashboard`, `feat/duckdb-pipeline`).
* `fix/<nome-curto>`: Correções pontuais (ex.: `fix/lead-time-calc`).
* `spec/<nome-curto>`: Criação ou refinamento de artefatos de engenharia.