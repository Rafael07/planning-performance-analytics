# Regras de Negócio, Métricas de Gestão e Casos de Uso

## 1. Fórmulas e Regras de Negócio Principais

### 1.1 Indicadores de Receita Recorrente e Carteira de Clientes
* **MRR (Monthly Recurring Revenue / Receita Recorrente Mensal):**
  $$\text{MRR} = \sum_{\text{contrato} \in \text{Ativos}} \text{valor\_mensalidade}$$
  Calculado para a competência de referência (`dim_calendario.ano_mes`).
* **Taxa de Cancelamento Mensal (Churn Rate):**
  $$\text{Churn Rate (\%)} = \frac{\text{Contratos Cancelados no Mês}}{\text{Contratos Ativos no Início da Competência}} \times 100$$
* **Taxa de Inadimplência Corporativa:**
  $$\text{Inadimplência (\%)} = \frac{\text{Contratos com Atraso } > 30 \text{ dias}}{\text{Contratos Ativos} + \text{Contratos Inadimplentes}} \times 100$$
* **Ticket Médio da Carteira:**
  $$\text{Ticket Médio} = \frac{\text{MRR}}{\text{Contratos Ativos}}$$

---

### 1.2 Indicadores Operacionais e Controle Estatístico de Processo (CEP)
* **Taxa de Sinistralidade Anualizada:**
  $$\text{Sinistralidade (\% a.a.)} = \frac{\text{Atendimentos de Sinistro no Mês}}{\text{Média de Contratos Ativos}} \times 12 \times 100$$
* **Tempo Médio de Atendimento Operacional (Lead Time em Horas):**
  Média aritmética de `tempo_ciclo_horas` entre acionamento e sepultamento.
* **Limites de Controle Estatístico (3-sigma):**
  * Limite Superior de Controle (LSC): $\mu + 3\sigma$
  * Limite Inferior de Controle (LIC): $\max(0, \mu - 3\sigma)$
  * **Regra de Ação de BPM:** Pontos acima do LSC configuram causas especiais (demora em liberação de cartório de plantão, perícia no IML ou traslado intermunicipal). Disparam o rito dos **5 Porquês** com os supervisores operacionais para eliminação de gargalos.

---

### 1.3 Equação do Ponto de Equilíbrio Operacional por Loja (Breakeven)

$$\text{Breakeven (Contratos)} = \frac{\text{Opex Mensal Base da Loja}}{\text{Ticket Médio} - \text{Custo Marginal de Cobertura por Contrato}}$$

---

## 2. Modelo de Simulação Paramétrica (Análise de Sensibilidade)

O simulador recalcula o resultado mensal projetado com base em três premissas ajustáveis pelo usuário:
1. **Reajuste Médio de Preço:** Intervalo de -10% a +20% sobre o valor da mensalidade.
2. **Impacto Estimado no Churn:** Elasticidade configurável (padrão: cada +5% de preço gera +0,8% de churn estrutural).
3. **Flutuação de Sinistralidade:** Variação de -15% a +30% no volume de funerais atendidos.

### Formulação de Margem Operacional Projetada:
* $\text{MRR Projetado} = \text{Base Ativa Ajustada} \times (\text{Ticket Médio Base} \times (1 + \Delta_{\text{preço}}))$
* $\text{Custo Sinistros Projetado} = \text{Custo Base} \times (1 + \Delta_{\text{base}}) \times (1 + \Delta_{\text{sinistros}})$
* $\text{Margem Operacional Projetada} = \text{MRR Projetado} - (\text{Custo Sinistros Projetado} + \text{Opex Total})$
