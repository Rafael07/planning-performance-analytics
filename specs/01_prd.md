# PRD: Plataforma Integrada de Planejamento, Simulação de Cenários e Performance Operacional (Projeto Integra-Dignidade)

## 1. Visão Geral e Contexto
O Grupo Dignidade é um dos principais conglomerados regionais de assistência familiar e serviços funerários, atuando com planos de pagamento recorrente, unidades de atendimento presencial e suporte 24 horas. Em virtude do plano de expansão territorial e da necessidade de sustentar o crescimento com margens controladas, a liderança de Planejamento, Performance e Integração demanda uma plataforma unificada de dados. O objetivo é subsidiar tomadas de decisão sob incerteza, conectar a execução da ponta aos rituais de governança com a diretoria e eliminar consolidações manuais suscetíveis a falhas.

## 2. Declaração do Problema
* **Fragmentação e Lentidão Analítica:** A consolidação de indicadores comerciais, financeiros e operacionais ainda depende de cruzamentos manuais de relatórios e planilhas, consumindo tempo excessivo da equipe de planejamento antes dos comitês executivos.
* **Tomada de Decisão sob Incerteza sem Ferramenta Paramétrica:** A liderança não possui um ambiente ágil de simulação de cenários (análise de sensibilidade) para mensurar o impacto financeiro de oscilações no cancelamento (churn), inadimplência e sinistralidade na abertura de novas praças.
* **Variabilidade e Gargalos Operacionais Ocultos:** Dificuldade de identificar com precisão estatística desvios de processo e tempo de resposta no atendimento das unidades, gerando retrabalho e potenciais atritos na experiência do associado.

## 3. Objetivos de Negócio (OKRs do Projeto)
* **Objetivo Geral:** Estruturar a governança de indicadores corporativos, a previsibilidade de receita e o controle de processos operacionais para dar sustentabilidade ao plano de expansão.
  * **KR 1 (Velocidade):** Reduzir o tempo de consolidação das bases e projeção de relatórios de 3 dias úteis para menos de 5 segundos.
  * **KR 2 (Previsibilidade):** Habilitar simulação paramétrica de cenários (otimista, base e estresse) para 100% das novas unidades em processo de implantação.
  * **KR 3 (Eficiência de Processo):** Mapear 100% do tempo de ciclo de atendimento operacional via controle estatístico de processo (CEP), isolando causas especiais de atraso.

## 4. Personas e Stakeholders
* **Head de Planejamento, Performance e Integração:** Exige integridade de indicadores para desdobramento de metas no BSC, cadência nos rituais de gestão e previsibilidade de caixa.
* **Diretoria Executiva do Grupo Dignidade:** Focada em alocação eficiente de capital (Capex e Opex), retorno sobre investimento das filiais e manutenção da margem operacional líquida.
* **Supervisores Regionais e Operadores de Lojas:** Necessitam de acompanhamento diário de funil de vendas, regularização de cobrança e tempo de resposta nos acionamentos de atendimento funerário.

## 5. Requisitos Funcionais
* **RF01 - Ingestão e Modelagem Analítica Sintética:** Estruturar conjunto de dados que reflita a cadeia completa do negócio (planos de assistência familiar, contratos com status vigentes/cancelados/inadimplentes, atendimentos funerários 24h e funil de captação de clientes).
* **RF02 - Camada de Indicadores Executivos (KPIs de Negócio):** Calcular e consolidar dinamicamente MRR (Receita Recorrente Mensal), Churn Rate, LTV, Ticket Médio, Taxa de Inadimplência e Sinistralidade por unidade e por tipo de plano.
* **RF03 - Simulador de Cenários e Sensibilidade Paramétrica:** Disponibilizar controles interativos onde o usuário varia reajuste de mensalidades, elasticidade esperada de churn e oscilação de sinistralidade, calculando instantaneamente o impacto na margem de contribuição.
* **RF04 - Painel de Controle Estatístico de Processo (CEP):** Monitorar o tempo de ciclo (lead time) de atendimento com cálculo de limites superior e inferior (média ± 3 desvios padrão), sinalizando unidades com variabilidade anormal para investigação de causa-raiz.
* **RF05 - Gestão de Pipeline Comercial das Lojas:** Exibir a distribuição dos leads nas etapas de qualificação e o tempo de permanência em cada fase, auxiliando o ritmo de vendas.

## 6. Requisitos Não Funcionais
* **RNF01 - Portabilidade e Leveza de Execução:** Funcionamento local ágil sem exigir infraestrutura em nuvem dedicada ou bancos relacionais pesados para execução da prova de conceito.
* **RNF02 - Padronização Declarativa e Reprodutibilidade:** Transformações de negócio documentadas em SQL puro, garantindo total clareza lógica e facilidade de auditoria.
* **RNF03 - Baixa Latência de Resposta:** Tempo de atualização visual em painel inferior a 1 segundo para navegação e alteração de parâmetros.
* **RNF04 - Governança Documental e Rastreabilidade:** Todo o catálogo de dados, specs e regras de negócio devem ser publicados via MkDocs com tema Material, e os commits versionados seguindo Conventional Commits.

## 7. Critérios de Aceite e Qualidade de Encerramento (DoD)
* Base de dados relacional populada e validada sem inconsistências de chaves ou valores negativos impróprios.
* Painel gerencial navegável contendo visão de governança de metas, simulador de cenários e dispersão estatística de processos operacionais.
* Documentação compilada e navegável via MkDocs contendo registro de premissas, regras de cálculo e catálogo de indicadores.
* Histórico de versionamento Git 100% padronizado de acordo com a spec 04.