# Regras de Negócio, Métricas de Gestão e Casos de Uso (Projeto Integra-Dignidade)

## 1. Fórmulas e Regras de Negócio Principais

### 1.1 Indicadores de Receita Recorrente e Carteira de Clientes
* **MRR (Monthly Recurring Revenue / Receita Recorrente Mensal):**
  Soma do valor da mensalidade de todos os contratos com status 'Ativo' vinculados à competência de referência (`dim_calendario.ano_mes`).
* **Taxa de Cancelamento Mensal (Churn Rate):**
  Percentual de contratos cancelados no mês (`dim_calendario.ano_mes`) dividido pela base de contratos ativos no primeiro dia da competência.
* **Taxa de Inadimplência Corporativa:**
  Percentual de contratos com atraso superior a 30 dias sobre o total de contratos da carteira (ativos e inadimplentes) vinculados à competência.
* **Ticket Médio da Carteira:**
  Valor total do MRR dividido pelo total de contratos ativos na competência.

### 1.2 Indicadores Operacionais e Controle Estatístico de Processo (CEP)
* **Taxa de Sinistralidade Anualizada da Carteira:**
  Percentual calculado pela divisão do volume total de atendimentos de sinistro realizados na competência pela média de contratos ativos.
* **Tempo Médio de Atendimento Operacional (Lead Time em Horas):**
  Média aritmética simples do atributo `tempo_ciclo_horas` dos atendimentos concluídos dentro do período filtrado.
* **Limites de Controle Estatístico (CEP - Cartas de Variabilidade):**
  * Limite Superior de Controle (LSC): Média + 3 desvios padrão
  * Limite Inferior de Controle (LIC): Máximo entre zero e (Média - 3 desvios padrão)
  * Regra de Ação: Atendimentos com lead time acima do LSC configuram causa especial de variabilidade (gargalo de frota, atraso documental em cartório, etc.) e disparam o rito de análise de causa-raiz via método dos 5 Porquês com a equipe da ponta.

### 1.3 Equação do Ponto de Equilíbrio Operacional por Loja (Breakeven)
Determina o volume mínimo de contratos ativos que uma unidade física precisa manter para custear sua operação:
$$\text{Breakeven (Contratos)} = \frac{\text{Opex Mensal Base da Loja}}{\text{Ticket Médio} - \text{Custo Marginal de Cobertura por Contrato}}$$

## 2. Modelo de Simulação Paramétrica (Análise de Sensibilidade de Cenários)

O modelo dinâmico recalcula o resultado mensal projetado com base em três premissas ajustáveis pelo usuário:
1. **Reajuste Médio de Preço:** Intervalo de -10% a +20% sobre o valor base da mensalidade.
2. **Impacto Estimado no Churn:** Elasticidade configurável (por premissa padrão: cada +5% de aumento de preço acarreta +0,8% de churn estrutural adicional).
3. **Flutuação de Sinistralidade:** Variação sazonal ou extraordinária de -10% a +30% no volume de funerais atendidos.

### Lógica de Cálculo da Margem Operacional Projetada:
* **MRR Projetado:** Base Ativa Ajustada * (Ticket Médio Base * (1 + Variação de Preço))
* **Custo de Atendimentos Projetado:** (Volume de Sinistros Base * (1 + Flutuação de Sinistralidade)) * Custo Médio Unitário de Execução
* **Margem Operacional Projetada:** MRR Projetado - (Custo Total de Atendimentos Projetado + Opex Total Consolidado das Unidades)

## 3. Especificação dos Casos de Uso

### Caso de Uso 01: Ritual Executivo de Acompanhamento de Performance e Metas
* **Ator Principal:** Head de Planejamento / Diretoria Executiva.
* **Entrada de Dados:** Seleção de unidade geográfica e competência (`ano_mes`) via `dim_calendario`.
* **Saída Esperada:** Painel executivo com cards de MRR, Churn, Inadimplência e Sinistralidade comparados com as metas corporativas do Balanced Scorecard (BSC). Gráfico estratificado dos motivos de cancelamento informados pela ponta para embasamento de planos de ação corretivos.

### Caso de Uso 02: Simulação de Viabilidade de Expansão (Nova Loja Física)
* **Ator Principal:** Analista de Planejamento / Gestor de Novos Negócios.
* **Entrada de Dados:** Inserção do Capex estimado de montagem da nova unidade, Opex fixo mensal previsto e meta de captação inicial.
* **Saída Esperada:** Curva de tempo estimada até o atingimento do ponto de equilíbrio (breakeven da praça), com matriz de sensibilidade refletindo cenários pessimista, base e otimista.

### Caso de Uso 03: Monitoramento de Desperdício e Eficiência no Atendimento Funerário (CEP)
* **Ator Principal:** Analista de Processos / Supervisor da Central de Atendimento 24h.
* **Entrada de Dados:** Filtro por intervalo de datas de acionamento (`dim_calendario.data`) e cidade executora.
* **Saída Esperada:** Dispersão dos atendimentos em relação aos limites de controle estatístico (3 sigma), listando os casos com atrasos anômalos para subsidiar reuniões de melhoria contínua de processos (BPM).

### Caso de Uso 04: Controle de Pipeline e Ritmo de Vendas nas Lojas
* **Ator Principal:** Gestor de RevOps / Supervisão Comercial.
* **Entrada de Dados:** Filtro por unidade física de atendimento.
* **Saída Esperada:** Visão de funil de oportunidades comerciais indicando gargalos de conversão e dias de estagnação de leads em cada etapa (ex.: tempo excessivo na fase de 'Qualificação' ou 'Negociação'), orientando a liderança a desatar nós operacionais.

---

> Para o catálogo consolidado de fórmulas, KPIs, metas de referência do BSC e dicionário de termos, consulte [06 - Catálogo de Dados, Métricas e Glossário Corporativo](06_data_catalog_and_glossary.md).