# Arquitetura Técnica e Contrato de Dados (planning-performance-analytics)

## 1. Visão Geral da Arquitetura
A arquitetura do projeto adota o padrão analítico desacoplado, leve e de execução local, eliminando dependências externas pesadas:

* **Camada de Geração Sintética (Python / Faker):** Simula contratos, cancelamentos com motivos de churn, ordens de atendimento funerário 24h e leads comerciais.
* **Camada de Armazenamento e Processamento (DuckDB / SQL):** Executa ingestão em formato colunar, consultas analíticas e transformações relacionais com baixo consumo de memória.
* **Camada de Apresentação e Simulação (Streamlit UI):** Interface com seletores de cenários, cartas de controle estatístico (CEP) e painéis executivos para rituais de governança.

O esquema dimensional segue o modelo de Constelação de Factos (*Fact Constellation*), partilhando dimensões conformadas (`dim_calendario`, `dim_unidades` e `dim_planos`) entre os diferentes processos de negócio da organização.

## 2. Modelo Relacional e Dicionário de Dados

### Tabela 1: `dim_calendario` (Dimensão Conformada de Tempo)
* `data` (DATE, PK): Data completa em formato YYYY-MM-DD.
* `ano` (INTEGER): Ano da competência (ex.: 2025, 2026).
* `mes` (INTEGER): Número do mês (1 a 12).
* `nome_mes` (VARCHAR): Designação do mês (ex.: 'Janeiro', 'Fevereiro').
* `trimestre` (INTEGER): Trimestre do ano (1 a 4).
* `ano_mes` (VARCHAR): Identificador de competência para agregações (ex.: '2026-03').
* `dia_semana` (INTEGER): Dia da semana numérico (1 = Domingo a 7 = Sábado).
* `flag_dia_util` (BOOLEAN): Indicador de dia útil bancário/comercial.

### Tabela 2: `dim_unidades` (Lojas Físicas e Centrais de Apoio)
* `id_unidade` (VARCHAR, PK): Identificador exclusivo da unidade física.
* `nome_cidade` (VARCHAR): Município de operação (ex.: Campina Grande, João Pessoa, Patos, Guarabira).
* `tipo_unidade` (VARCHAR): Perfil operacional ('Matriz Administrativa', 'Loja Conceito', 'Ponto de Apoio').
* `capex_implantacao` (DECIMAL(12,2)): Investimento inicial para reforma, infraestrutura e abertura.
* `opex_mensal_base` (DECIMAL(12,2)): Custo fixo mensal de funcionamento da loja (aluguel, equipe, utilidades).
* `data_inauguracao` (DATE, FK): Data de início das atividades (relacionada com `dim_calendario`).

### Tabela 3: `dim_planos` (Portfólio de Planos de Assistência)
* `id_plano` (VARCHAR, PK): Código de referência do plano.
* `nome_plano` (VARCHAR): Denominação comercial (ex.: Individual Essencial, Familiar Prata, Familiar Ouro Especial).
* `valor_mensalidade` (DECIMAL(10,2)): Valor de face cobrado mensalmente do associado.
* `limite_dependentes` (INTEGER): Quantidade de beneficiários contemplados no plano.
* `cobertura_cremacao` (BOOLEAN): Indicador de inclusão de serviço crematório.

### Tabela 4: `fct_contratos` (Processo: Gestão de Carteira e Receita Recorrente)
* `id_contrato` (VARCHAR, PK): Identificador único da matrícula contratual.
* `id_cliente` (VARCHAR): Código do titular responsável pelo pagamento.
* `id_unidade` (VARCHAR, FK): Unidade geográfica vinculada à carteira.
* `id_plano` (VARCHAR, FK): Plano de assistência contratado.
* `data_adesao` (DATE, FK): Data de assinatura do contrato (relacionada com `dim_calendario`).
* `status_contrato` (VARCHAR): Estado operacional ('Ativo', 'Cancelado', 'Inadimplente').
* `data_cancelamento` (DATE, FK, NULL): Data do encerramento (relacionada com `dim_calendario`).
* `motivo_cancelamento` (VARCHAR, NULL): Causa-raiz informada ('Preço', 'Atendimento', 'Mudança de Endereço', 'Financeiro').

### Tabela 5: `fct_atendimentos` (Processo: Acionamento Funerário e Sinistros 24h)
* `id_atendimento` (VARCHAR, PK): Identificador da ordem de atendimento funerário.
* `id_contrato` (VARCHAR, FK): Contrato de cobertura associado.
* `id_unidade` (VARCHAR, FK): Unidade operacional responsável pela execução do serviço.
* `data_acionamento` (DATE, FK): Data do acionamento (relacionada com `dim_calendario`).
* `timestamp_acionamento` (TIMESTAMP): Data e horário exatos do chamado de emergência.
* `timestamp_conclusao` (TIMESTAMP): Data e horário da conclusão do velório e sepultamento.
* `tempo_ciclo_horas` (DECIMAL(6,2)): Lead time operacional decorrido entre acionamento e finalização.
* `custo_direto_servico` (DECIMAL(10,2)): Despesa direta com paramentos, preparação, traslado e urna.

### Tabela 6: `fct_leads_crm` (Processo: Pipeline Comercial e Vendas em Loja)
* `id_lead` (VARCHAR, PK): Código identificador da oportunidade comercial.
* `id_unidade` (VARCHAR, FK): Loja responsável pela captação.
* `etapa_funil` (VARCHAR): Status no funil ('Sem Contato', '1º Contato', 'Qualificação', 'Negociação', 'Fechado', 'Desqualificado').
* `data_criacao` (DATE, FK): Data de ingresso da oportunidade (relacionada com `dim_calendario`).
* `dias_no_estagio` (INTEGER): Tempo de permanência do lead na etapa corrente.

## 3. Contrato de Dados (Governança e Confiabilidade)
1. **Integridade Dimensional e Calendário:** Todas as datas de adesão, cancelamento, acionamento e criação de leads devem ter chave válida correspondente na tabela `dim_calendario`.
2. **Integridade Referencial Estrita:** Proibida a existência de contratos, atendimentos ou leads sem unidade de referência cadastrada em `dim_unidades`.
3. **Consistência de Prazos Operacionais:** O atributo `tempo_ciclo_horas` deve ser rigorosamente maior que zero e menor que 72 horas em atendimentos funerários convencionais.
4. **Preenchimento Condicional de Cancelamento:** Registros com `status_contrato = 'Cancelado'` exigem obrigatoriamente preenchimento dos campos `data_cancelamento` e `motivo_cancelamento`.
5. **Precisão Numérica:** Todos os campos monetários operam com precisão de duas casas decimais (`DECIMAL(10,2)` ou `DECIMAL(12,2)`), eliminando erros de arredondamento de margem e receita.
6. **Rastreabilidade Temporal:** Consultas analíticas devem sempre expor a competência (`ano_mes`) derivada da `dim_calendario`, garantindo repetibilidade nos rituais de governança da liderança.

---

> Para o catálogo de dados completo, domínio de valores e dicionário de atributos detalhado, consulte [06 - Catálogo de Dados, Métricas e Glossário Corporativo](06_data_catalog_and_glossary.md).