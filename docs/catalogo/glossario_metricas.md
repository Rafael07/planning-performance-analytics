# Catálogo de Dados, Métricas, Siglas e OKRs

Este catálogo constitui a **Fonte Única da Verdade (Single Source of Truth - SSOT)** do Projeto Integra-Dignidade.

---

## 1. Glossário Estratégico e Conceitos de Negócio

* **Assistência Familiar / Plano Funerário:** Modelo de negócio de receita recorrente mensal que garante cobertura integral de serviços funerários, cremação, traslado e benefícios em vida para titular e dependentes.
* **Grupo Digna:** Conglomerado regional de serviços póstumos e assistência familiar, com atuação em cemitérios, crematórios, planos funerários e rede de lojas físicas de apoio.
* **Lojas Físicas de Apoio:** Pontos de atendimento presencial geograficamente distribuídos, integrando relacionamento, conveniência e experiência do cliente (*Customer Experience - CX*).
* **Atmosphere Store (Atmosfera de Loja):** Conceito de varejo focado no design de ambiente, vitrine e iluminação para guiar a decisão do cliente sem inflar Capex e Opex.
* **Capex de Implantação:** Investimento inicial para reforma, montagem, tecnologia e abertura de uma nova unidade física.
* **Opex Mensal Base:** Custos operacionais fixos mensais de manutenção da loja (equipe, aluguel, utilidades, manutenção).
* **Acionamento Funerário 24h (Sinistro):** Chamado de emergência realizado pela família no momento do óbito, disparando o fluxo de assistência funerária.
* **A Ponta Operacional:** Equipes de linha de frente que executam os processos (atendentes, agentes funerários, motoristas e consultores). É onde os gargalos reais se manifestam.

---

## 2. Siglas e Frameworks Metodológicos

* **BSC (Balanced Scorecard):** Gestão estratégica que desdobra metas em perspectivas Financeira, Clientes, Processos Internos e Aprendizado/Crescimento.
* **BPM (Business Process Management):** Disciplina que integra estratégia e tecnologia para modelar, executar, monitorar e otimizar processos de ponta a ponta.
* **CEP (Controle Estatístico de Processo):** Aplicação de cartas de controle (Shewhart) para monitorar estabilidade e identificar causas especiais de variabilidade.
* **LSC / LIC:** Limites Superior e Inferior de Controle estatístico ($\mu \pm 3\sigma$).
* **5 Porquês (5 Whys):** Ferramenta de diagnóstico que investiga camadas sucessivas de causalidade até identificar a causa-raiz de um desvio na ponta.
* **CRM (Customer Relationship Management):** Plataforma de gestão do funil e pipeline de captação de clientes.
* **DoD (Definition of Done):** Critérios explícitos de aceite para conclusão de entregas em produção.
* **Pre-mortem:** Técnica que antecipa cenários hipotéticos de falha antes do início de um projeto para estruturar salvaguardas.
* **RACI:** Matriz de responsabilidade (Responsible, Accountable, Consulted, Informed).
* **SDD (Spec-Driven Development):** Desenvolvimento orientado por especificações contratuais antes da codificação.

---

## 3. Objetivos e Resultados-Chave (OKRs) do Projeto

* **Objetivo Geral (O1):** Estruturar uma plataforma governada de dados e controle de processos que elimine consolidações manuais e subsidie a expansão sustentável do Grupo Digna com margens protegidas.
  * **KR 1 (Velocidade):** Reduzir o tempo de consolidação das bases de 3 dias úteis para menos de 5 segundos via consultas colunares no DuckDB.
  * **KR 2 (Previsibilidade de Cenários):** Habilitar simulação paramétrica dinâmica e cálculo de breakeven para 100% dos estudos de expansão de lojas.
  * **KR 3 (Eficiência de Processo / BPM):** Monitorar 100% dos atendimentos funerários 24h via CEP 3-sigma, isolando causas especiais de variabilidade no lead time para condução de ritos de melhoria contínua.
  * **KR 4 (Governança e Rastreabilidade):** Disponibilizar 100% dos dicionários, contratos de dados e regras em documentação viva navegável (MkDocs).

---

## 4. Catálogo de Métricas e KPIs do Balanced Scorecard (BSC)

| Métrica / KPI | Sigla | Fórmula / Definição Matemática | Unidade | Periodicidade | Meta BSC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Monthly Recurring Revenue** | MRR | $\sum \text{mensalidade}$ dos contratos com status 'Ativo' | R$ | Mensal | R$ 200.000,00 |
| **Taxa de Churn Mensal** | Churn | $\frac{\text{Cancelados no Mês}}{\text{Ativos no Início do Mês}} \times 100$ | % | Mensal | $\le 1,8\%$ |
| **Taxa de Inadimplência** | Inad. | $\frac{\text{Contratos com Atraso } > 30\text{d}}{\text{Total Carteira Ativa + Inadimplente}} \times 100$ | % | Mensal | $\le 4,5\%$ |
| **Ticket Médio da Carteira** | - | $\frac{\text{MRR Consolidado}}{\text{Total Contratos Ativos}}$ | R$ | Mensal | $\ge \text{R\$\ } 52,00$ |
| **Lifetime Value** | LTV | $\frac{\text{Ticket Médio}}{\text{Taxa de Churn Decimal}}$ | R$ | Mensal | $\ge \text{R\$\ } 2.800,00$ |
| **Sinistralidade Anualizada** | - | $\frac{\text{Sinistros no Mês}}{\text{Média Contratos Ativos}} \times 12 \times 100$ | % a.a. | Mensal | $\le 2,2\%$ a.a. |
| **Breakeven de Loja** | - | $\frac{\text{Opex Mensal Base}}{\text{Ticket Médio} - \text{Custo Marginal}}$ | Contratos | Por Estudo | $\le 14$ meses |

---

## 5. Dicionário Relacional de Tabelas e Atributos

### 5.1 Tabela `dim_calendario` (Dimensão Conformada de Tempo)
* `data` (DATE, PK): Data civil padrão ISO (`YYYY-MM-DD`).
* `ano` (INTEGER, NOT NULL): Ano civil (ex.: 2024, 2025, 2026).
* `mes` (INTEGER, NOT NULL): Mês ordinal (1 a 12).
* `nome_mes` (VARCHAR, NOT NULL): Descrição do mês em português ('Janeiro' a 'Dezembro').
* `trimestre` (INTEGER, NOT NULL): Trimestre civil (1 a 4).
* `ano_mes` (VARCHAR, NOT NULL): Chave agregadora de competência (`YYYY-MM`).
* `dia_semana` (INTEGER, NOT NULL): Dia da semana (1 = Domingo, 7 = Sábado).
* `flag_dia_util` (BOOLEAN, NOT NULL): Indicador de dia útil comercial/bancário.

### 5.2 Tabela `dim_unidades` (Lojas Físicas e Centrais)
* `id_unidade` (VARCHAR, PK): Código exclusivo da filial (ex.: 'UND-CG-01', 'UND-JP-01').
* `nome_cidade` (VARCHAR, NOT NULL): Cidade de atuação (Campina Grande, João Pessoa, Patos, Guarabira).
* `tipo_unidade` (VARCHAR, NOT NULL): 'Matriz Administrativa', 'Loja Conceito', 'Ponto de Apoio'.
* `capex_implantacao` (DECIMAL(12,2), NOT NULL): Investimento inicial de abertura e vitrine.
* `opex_mensal_base` (DECIMAL(12,2), NOT NULL): Custo fixo mensal de manutenção da loja.
* `data_inauguracao` (DATE, FK): Data de inauguração física da unidade.

### 5.3 Tabela `dim_planos` (Portfólio de Planos)
* `id_plano` (VARCHAR, PK): Identificador do plano ('PLN-IND-01', 'PLN-FAM-PRATA', 'PLN-FAM-OURO', 'PLN-PREM-CREM').
* `nome_plano` (VARCHAR, NOT NULL): Denominação comercial.
* `valor_mensalidade` (DECIMAL(10,2), NOT NULL): Valor nominal da mensalidade recorrente.
* `limite_dependentes` (INTEGER, NOT NULL): Número de dependentes cobertos (0 a 5).
* `cobertura_cremacao` (BOOLEAN, NOT NULL): Flag indicando se inclui cremação.

### 5.4 Tabela `fct_contratos` (Processo: Gestão de Carteira)
* `id_contrato` (VARCHAR, PK): Número unívoco da matrícula contratual.
* `id_cliente` (VARCHAR, NOT NULL): Código do titular do plano.
* `id_unidade` (VARCHAR, FK): Filial física responsável pela carteira.
* `id_plano` (VARCHAR, FK): Plano contratado.
* `data_adesao` (DATE, FK): Data de assinatura do contrato.
* `status_contrato` (VARCHAR, NOT NULL): 'Ativo', 'Cancelado', 'Inadimplente'.
* `data_cancelamento` (DATE, FK, NULL): Data formal de cancelamento.
* `motivo_cancelamento` (VARCHAR, NULL): Causa informada na ponta ('Preço', 'Financeiro', 'Mudança de Endereço', 'Atendimento').

### 5.5 Tabela `fct_atendimentos` (Processo: Acionamento Funerário 24h e Sinistros)
* `id_atendimento` (VARCHAR, PK): Número da ordem de serviço funerária.
* `id_contrato` (VARCHAR, FK): Contrato que acionou o benefício.
* `id_unidade` (VARCHAR, FK): Unidade operacional responsável pela execução.
* `data_acionamento` (DATE, FK): Data do chamado de emergência.
* `timestamp_acionamento` (TIMESTAMP, NOT NULL): Momento exato do chamado.
* `timestamp_conclusao` (TIMESTAMP, NOT NULL): Momento da conclusão do sepultamento/cremação.
* `tempo_ciclo_horas` (DECIMAL(6,2), NOT NULL): Lead time operacional em horas (0 a 72h).
* `custo_direto_servico` (DECIMAL(10,2), NOT NULL): Custo direto (urna, preparação, paramentos, traslado).

### 5.6 Tabela `fct_leads_crm` (Processo: Pipeline Comercial de Lojas)
* `id_lead` (VARCHAR, PK): Identificador da oportunidade comercial.
* `id_unidade` (VARCHAR, FK): Loja responsável pela captação.
* `etapa_funil` (VARCHAR, NOT NULL): 'Sem Contato', '1º Contato', 'Qualificação', 'Negociação', 'Fechado', 'Desqualificado'.
* `data_criacao` (DATE, FK): Data de cadastro do lead.
* `dias_no_estagio` (INTEGER, NOT NULL): Tempo de estagnação na fase corrente.
