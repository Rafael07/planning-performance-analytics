# Catálogo de Dados, Métricas e Glossário Corporativo (Projeto Integra-Dignidade)

Este documento é a fonte única da verdade (*Single Source of Truth - SSOT*) do projeto, compilando o vocabulário estratégico, conceitos setoriais, governança de OKRs, métricas do Balanced Scorecard (BSC), definições técnicas e o dicionário relacional de tabelas e atributos.

---

## 1. Glossário de Conceitos Estratégicos e de Negócio

* **Assistência Familiar / Plano Funerário:** Modelo de negócio de receita recorrente mensal (assinatura/mutualismo) que garante cobertura integral de serviços funerários, cremação, traslado e benefícios em vida para o titular e seus dependentes.
* **Grupo Dignidade:** Conglomerado regional de serviços póstumos e assistência familiar, com atuação em cemitérios, crematórios, planos funerários e rede de lojas físicas de apoio.
* **Lojas Físicas de Apoio:** Pontos de atendimento presencial distribuídos geograficamente. Historicamente utilizados para pagamento de mensalidades e resolução de pendências, reposicionados estrategicamente como espaços de relacionamento, decisão e experiência do cliente (*Customer Experience - CX*).
* **Atmosphere Store (Atmosfera de Loja):** Conceito de varejo (baseado em Pine & Gilmore, Verhoef et al.) focado no design de ambiente, vitrine e iluminação para guiar o fluxo do cliente e valorizar a marca sem inflar custos operacionais.
* **Capex de Implantação (Capital Expenditure):** Despesa de capital necessária para reforma, montagem, tecnologia e abertura de uma nova unidade física.
* **Opex Mensal Base (Operational Expenditure):** Custos operacionais fixos mensais para manter uma loja em funcionamento (equipe, aluguel, utilidades, manutenção).
* **Acionamento Funerário 24h (Sinistro):** Chamado de emergência realizado pela família do associado para a central de atendimento no momento do óbito, disparando o fluxo de preparação, traslado, paramentos, velório e sepultamento/cremação.
* **A Ponta Operacional:** Equipes de linha de frente que executam os processos (atendentes de balcão de loja, agentes funerários, motoristas de frota e operadores de teleatendimento). É onde os gargalos reais se manifestam.

---

## 2. Siglas e Frameworks Metodológicos

* **BSC (Balanced Scorecard):** Metodologia de gestão estratégica que desdobra a visão corporativa em metas e indicadores equilibrados sob quatro perspectivas: Financeira, Clientes/Mercado, Processos Internos e Aprendizado/Crescimento.
* **BPM (Business Process Management / Gestão por Processos):** Disciplina gerencial que integra estratégia e tecnologia para desenhar, modelar, executar, monitorar e otimizar processos de ponta a ponta, visando eficiência e eliminação de retrabalho.
* **CEP (Controle Estatístico de Processo):** Aplicação de métodos estatísticos (cartas de controle de Shewhart) para avaliar a estabilidade de processos repetitivos, distinguindo variações normais de causas especiais de desvio.
* **LSC / LIC (Limites Superior e Inferior de Controle):** Fronteiras estatísticas calculadas a partir da média aritmética ± 3 desvios padrão ($\mu \pm 3\sigma$). Pontos fora dos limites configuram anomalias que exigem intervenção imediata.
* **5 Porquês (5 Whys):** Ferramenta iterativa de diagnóstico que investiga cinco camadas sucessivas de causalidade até identificar a causa-raiz de uma falha de processo, conectando o desvio no dado ao gargalo humano/operacional na ponta.
* **CRM (Customer Relationship Management):** Plataforma ou sistema de gestão de relacionamento e pipeline de vendas para rastrear leads desde a captação até o fechamento do contrato.
* **DoD (Definition of Done / Critério de Aceite):** Conjunto explícito de condições e padrões de qualidade que uma entrega deve satisfazer para ser considerada concluída e aceita em produção.
* **Pre-mortem:** Técnica de gestão em que a equipe antecipa cenários hipotéticos de fracasso de um projeto antes de iniciá-lo, permitindo desenhar salvaguardas e planos de mitigação prévios.
* **RACI (Matriz de Responsabilidade):** Ferramenta que define papéis organizacionais: *Responsible* (quem executa), *Accountable* (quem responde pela entrega), *Consulted* (quem é consultado) e *Informed* (quem é comunicado).
* **SDD (Spec-Driven Development):** Metodologia de engenharia onde a especificação técnica formal precede a escrita do código, garantindo rastreabilidade, clareza lógica e alinhamento com os contratos de negócio.

---

## 3. Objetivos e Resultados-Chave (OKRs) do Projeto

* **Objetivo Geral (O1):** Estruturar uma plataforma governada de dados e controle de processos que elimine consolidações manuais e subsidie a expansão sustentável do Grupo Dignidade com margens protegidas.
  * **KR 1 (Velocidade):** Reduzir o tempo de consolidação das bases de carteira e emissão de relatórios executivos de 3 dias úteis para menos de 5 segundos via consultas colunares no DuckDB.
  * **KR 2 (Previsibilidade de Cenários):** Habilitar simulação paramétrica dinâmica (elasticidade de preço, sensibilidade de churn e sinistralidade) e cálculo de breakeven para 100% dos estudos de expansão de lojas.
  * **KR 3 (Eficiência de Processo / BPM):** Monitorar 100% dos atendimentos funerários 24h via Controle Estatístico de Processos (CEP 3-sigma), isolando causas especiais de variabilidade no lead time para condução de ritos de melhoria contínua.
  * **KR 4 (Governança e Rastreabilidade):** Disponibilizar 100% dos dicionários, contratos de dados e regras em documentação viva navegável (MkDocs), garantindo auditabilidade e zero perda de aprendizado institucional.

---

## 4. Catálogo de Métricas e KPIs (Fórmulas e Regras)

### 4.1 Perspectiva Financeira e Receita Recorrente

| Métrica / KPI | Sigla | Fórmula / Definição Matemática | Unidade | Periodicidade | Meta de Referência |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Monthly Recurring Revenue** | MRR | $\sum \text{valor\_mensalidade}$ dos contratos com `status_contrato = 'Ativo'` no mês de competência | R$ (BRL) | Mensal | Crescimento $\ge 1,5\%$ a.m. |
| **Taxa de Cancelamento Mensal** | Churn Rate | $\frac{\text{Contratos Cancelados no Mês}}{\text{Contratos Ativos no Início do Mês}} \times 100$ | % | Mensal | $\le 1,8\%$ a.m. |
| **Taxa de Inadimplência** | Inadimplência | $\frac{\text{Contratos com Atraso } > 30\text{ dias}}{\text{Total da Carteira Ativa + Inadimplente}} \times 100$ | % | Mensal | $\le 4,5\%$ |
| **Ticket Médio da Carteira** | Ticket Médio | $\frac{\text{MRR Consolidado}}{\text{Total de Contratos Ativos}}$ | R$ (BRL) | Mensal | $\ge \text{R\$\ } 52,00$ |
| **Lifetime Value** | LTV | $\frac{\text{Ticket Médio}}{\text{Taxa de Churn Decimal}}$ | R$ (BRL) | Mensal | $\ge \text{R\$\ } 2.800,00$ |
| **Margem Operacional Líquida** | Margem Op. | $\text{MRR} - (\text{Custos de Sinistros} + \text{Opex Consolidado})$ | R$ (BRL) | Mensal | $\ge 28\%$ da receita |
| **Ponto de Equilíbrio de Loja** | Breakeven | $\frac{\text{Opex Mensal Base da Loja}}{\text{Ticket Médio} - \text{Custo Marginal de Cobertura}}$ | Contratos | Por Estudo | Prazo de retorno $\le 14$ meses |

### 4.2 Perspectiva Operacional e Eficiência (BPM / CEP)

| Métrica / KPI | Definição / Formulação | Unidade | Periodicidade | Gatilho de Ação |
| :--- | :--- | :--- | :--- | :--- |
| **Lead Time de Atendimento** | Média de `tempo_ciclo_horas` decorrido entre acionamento 24h e sepultamento | Horas | Diária / Mensal | Média alvo: 14 a 18 horas |
| **Limite Superior de Controle (LSC)** | $\mu + 3\sigma$ do lead time operacional de atendimento | Horas | Mensal | Qualquer atendimento acima do LSC dispara rito dos 5 Porquês |
| **Limite Inferior de Controle (LIC)** | $\max(0, \mu - 3\sigma)$ do lead time operacional | Horas | Mensal | Avaliar subnotificação ou anomalia de registro |
| **Taxa de Sinistralidade** | $\frac{\text{Atendimentos Realizados}}{\text{Média de Contratos Ativos}} \times 12 \times 100$ | % a.a. | Mensal | Faixa esperada: 1,8% a 2,4% a.a. |
| **Custo Médio por Sinistro** | $\frac{\sum \text{custo\_direto\_servico}}{\text{Total de Atendimentos Realizados}}$ | R$ (BRL) | Mensal | Alvo: R$ 1.350,00 a R$ 1.550,00 |

### 4.3 Perspectiva Comercial e Expansão (CRM de Lojas)

| Métrica / KPI | Definição / Formulação | Unidade | Periodicidade | Meta de Referência |
| :--- | :--- | :--- | :--- | :--- |
| **Volume de Leads no Pipeline** | Contagem total de oportunidades ativas no funil | Oportunidades | Semanal | Acompanhar ritmo semanal |
| **Taxa de Conversão do Funil** | $\frac{\text{Leads Fechados}}{\text{Total de Leads Ingressados}} \times 100$ | % | Mensal | $\ge 18\%$ |
| **Aging de Leads (Dias no Estágio)** | Média de dias que o lead permanece na etapa atual sem avanço | Dias | Semanal | $\le 5$ dias em Qualificação |

---

## 5. Arquitetura de Dados e Conceitos Técnicos

* **DuckDB:** Sistema de gerenciamento de banco de dados relacional colunar (*in-process OLAP*). Desenvolvido para operações analíticas vetorizadas de alta velocidade sem sobrecarga de infraestrutura de servidor.
* **Modelo Constelação de Fatos (*Fact Constellation*):** Padrão de modelagem dimensional no qual múltiplos processos de negócio distintos (Contratos, Atendimentos e CRM) são modelados em tabelas fato separadas, partilhando dimensões conformadas padronizadas (`dim_calendario`, `dim_unidades`, `dim_planos`).
* **Dimensão Conformada:** Dimensão padronizada que tem a mesma estrutura, granularidade e significado em todos os fatos com os quais se relaciona, garantindo integridade de cruzamentos no BSC.
* **Contrato de Dados (*Data Contract*):** Especificação formal entre quem gera e quem consome os dados, abrangendo nomes, tipos de dados, restrições de integridade, valores aceitáveis e garantias de qualidade.

---

## 6. Dicionário Relacional de Tabelas e Atributos

```text
                               ┌─────────────────┐
                               │ dim_calendario  │
                               └────────┬────────┘
                                        │ (1:N)
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌──────────────┐                ┌──────────────┐                ┌──────────────┐
│fct_contratos │                │fct_atendimen.│                │fct_leads_crm │
└───────▲──────┘                └───────▲──────┘                └───────▲──────┘
        │ (N:1)                         │ (N:1)                         │ (N:1)
        ├───────────────────────────────┼───────────────────────────────┤
        │                               │                               │
┌───────┴──────┐                ┌───────┴──────┐                        │
│  dim_planos  │                │ dim_unidades │────────────────────────┘
└──────────────┘                └──────────────┘
```

### 6.1 Tabela: `dim_calendario` (Dimensão Conformada de Tempo)
Granularidade: 1 registro por dia civil.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `data` | `DATE` | `PRIMARY KEY` | Data civil em formato padrão ISO (`YYYY-MM-DD`). |
| `ano` | `INTEGER` | `NOT NULL` | Ano civil da competência (ex.: 2024, 2025, 2026). |
| `mes` | `INTEGER` | `NOT NULL` | Número ordinal do mês (1 a 12). |
| `nome_mes` | `VARCHAR(20)` | `NOT NULL` | Descrição do mês em português ('Janeiro', 'Fevereiro', ..., 'Dezembro'). |
| `trimestre` | `INTEGER` | `NOT NULL` | Trimestre civil de 1 a 4. |
| `ano_mes` | `VARCHAR(7)` | `NOT NULL` | Chave de competência agregadora no formato `YYYY-MM` (ex.: '2026-03'). |
| `dia_semana` | `INTEGER` | `NOT NULL` | Dia da semana numérico (1 = Domingo, 7 = Sábado). |
| `flag_dia_util` | `BOOLEAN` | `NOT NULL` | `TRUE` para dias de expediente comercial/bancário; `FALSE` para sábados e domingos. |

---

### 6.2 Tabela: `dim_unidades` (Dimensão de Lojas Físicas e Centrais)
Granularidade: 1 registro por unidade operacional do Grupo Dignidade.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `id_unidade` | `VARCHAR(16)` | `PRIMARY KEY` | Código alfanumérico identificador da filial (ex.: 'UND-CG-01', 'UND-JP-01'). |
| `nome_cidade` | `VARCHAR(60)` | `NOT NULL` | Cidade-polo de atuação (ex.: 'Campina Grande', 'João Pessoa', 'Patos', 'Guarabira'). |
| `tipo_unidade` | `VARCHAR(30)` | `NOT NULL` | Categoria da unidade: 'Matriz Administrativa', 'Loja Conceito', 'Ponto de Apoio'. |
| `capex_implantacao`| `DECIMAL(12,2)` | `NOT NULL, >= 0` | Montante total investido na abertura física, mobiliário e vitrine da unidade. |
| `opex_mensal_base` | `DECIMAL(12,2)` | `NOT NULL, > 0`  | Custo operacional mensal recorrente para funcionamento da filial física. |
| `data_inauguracao` | `DATE` | `FK -> dim_calendario.data` | Data formal de abertura da filial física. |

---

### 6.3 Tabela: `dim_planos` (Dimensão de Portfólio de Planos)
Granularidade: 1 registro por plano comercializado.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `id_plano` | `VARCHAR(16)` | `PRIMARY KEY` | Código único do produto (ex.: 'PLN-IND-01', 'PLN-FAM-PRATA', 'PLN-FAM-OURO'). |
| `nome_plano` | `VARCHAR(60)` | `NOT NULL` | Denominação comercial (ex.: 'Individual Essencial', 'Familiar Prata', 'Familiar Ouro'). |
| `valor_mensalidade`| `DECIMAL(10,2)` | `NOT NULL, > 0`  | Valor nominal da mensalidade recorrente cobrada do associado. |
| `limite_dependentes`| `INTEGER` | `NOT NULL, >= 0` | Número máximo de beneficiários elegíveis além do titular (0 a 6). |
| `cobertura_cremacao`| `BOOLEAN` | `NOT NULL` | `TRUE` se contempla processo crematório na cobertura contratual; `FALSE` caso contrário. |

---

### 6.4 Tabela: `fct_contratos` (Processo: Gestão de Carteira e Receita Recorrente)
Granularidade: 1 registro por matrícula contratual ativa, cancelada ou inadimplente.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `id_contrato` | `VARCHAR(24)` | `PRIMARY KEY` | Número da matrícula contratual unívoca (ex.: 'CTR-2024-0001'). |
| `id_cliente` | `VARCHAR(24)` | `NOT NULL` | Identificador único do titular responsável financeiro. |
| `id_unidade` | `VARCHAR(16)` | `FK -> dim_unidades.id_unidade` | Loja geográfica gestora da carteira do cliente. |
| `id_plano` | `VARCHAR(16)` | `FK -> dim_planos.id_plano` | Plano de assistência contratado. |
| `data_adesao` | `DATE` | `FK -> dim_calendario.data` | Data de contratação do plano. |
| `status_contrato` | `VARCHAR(20)` | `NOT NULL` | Estado do contrato: 'Ativo', 'Cancelado', 'Inadimplente'. |
| `data_cancelamento`| `DATE` | `FK -> dim_calendario.data, NULL` | Data formal de rescisão. Obrigatória se `status_contrato = 'Cancelado'`. |
| `motivo_cancelamento`| `VARCHAR(40)`| `NULL` | Razão declarada na ponta: 'Preço', 'Atendimento', 'Mudança de Endereço', 'Financeiro'. |

---

### 6.5 Tabela: `fct_atendimentos` (Processo: Acionamento Funerário 24h e Sinistros)
Granularidade: 1 registro por ordem de serviço de atendimento funerário.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `id_atendimento` | `VARCHAR(24)` | `PRIMARY KEY` | Código identificador da ordem de serviço funerária (ex.: 'ATD-2024-0001'). |
| `id_contrato` | `VARCHAR(24)` | `FK -> fct_contratos.id_contrato`| Contrato de plano de assistência que acionou a cobertura. |
| `id_unidade` | `VARCHAR(16)` | `FK -> dim_unidades.id_unidade` | Unidade física responsável pelo atendimento funerário. |
| `data_acionamento` | `DATE` | `FK -> dim_calendario.data` | Data de abertura do chamado de emergência. |
| `timestamp_acionamento`| `TIMESTAMP` | `NOT NULL` | Data e hora exatas da solicitação do funeral. |
| `timestamp_conclusao`  | `TIMESTAMP` | `NOT NULL` | Data e hora da conclusão dos serviços de sepultamento/cremação. |
| `tempo_ciclo_horas`    | `DECIMAL(6,2)` | `NOT NULL, > 0 e < 72` | Lead time operacional decorrido entre acionamento e sepultamento (em horas). |
| `custo_direto_servico` | `DECIMAL(10,2)`| `NOT NULL, > 0` | Custo direto de execução (urna funerária, preparação, traslado e paramentos). |

---

### 6.6 Tabela: `fct_leads_crm` (Processo: Pipeline Comercial e Captação em Loja)
Granularidade: 1 registro por oportunidade de venda captada em loja física.

| Coluna | Tipo de Dado | Restrição | Descrição e Regra de Domínio |
| :--- | :--- | :--- | :--- |
| `id_lead` | `VARCHAR(24)` | `PRIMARY KEY` | Identificador único da oportunidade de negócio (ex.: 'LEAD-2025-0001'). |
| `id_unidade` | `VARCHAR(16)` | `FK -> dim_unidades.id_unidade` | Loja física responsável pelo atendimento comercial. |
| `etapa_funil` | `VARCHAR(30)` | `NOT NULL` | Fase atual: 'Sem Contato', '1º Contato', 'Qualificação', 'Negociação', 'Fechado', 'Desqualificado'. |
| `data_criacao` | `DATE` | `FK -> dim_calendario.data` | Data de captação e cadastro da oportunidade. |
| `dias_no_estagio` | `INTEGER` | `NOT NULL, >= 0` | Número de dias corridos em que o lead permanece na etapa atual sem avanço. |
