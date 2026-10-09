# Contrato de Dados e Garantias de Qualidade

## 1. O Conceito de Data Contract aplicado ao Planejamento

No ambiente corporativo, a maior causa de atrasos e retrabalho na consolidação de relatórios executivos é a quebra silenciosa de dados: campos nulos inesperados, IDs órfãos, divergência de granularidade e schemas instáveis.

Um **Contrato de Dados (Data Contract)** estabelece um acordo explícito entre os sistemas operacionais da ponta e a camada analítica de planejamento, assegurando qualidade antes de qualquer agregação de métricas.

---

## 2. Regras de Integridade e Validações Automatizadas

As seguintes checagens são executadas compulsoriamente na inicialização do banco (`src/database.py`):

1. **Integridade Referencial Estrita:** 
   Proibida a existência de contratos, atendimentos funerários ou leads CRM sem filial correspondente cadastrada em `dim_unidades`.
2. **Integridade de Cancelamento:** 
   Registros com `status_contrato = 'Cancelado'` exigem obrigatoriamente preenchimento dos campos `data_cancelamento` e `motivo_cancelamento`.
3. **Consistência de Lead Time Operacional:** 
   O atributo `tempo_ciclo_horas` deve ser estritamente maior que zero e menor que 72 horas em atendimentos funerários convencionais.
4. **Precisão Numérica Financeira:** 
   Todos os campos monetários operam com precisão explícita de duas casas decimais (`DECIMAL(10,2)` ou `DECIMAL(12,2)`), eliminando distorções de arredondamento em margem e receita.
5. **Rastreabilidade Temporal:** 
   Todas as agregações analíticas utilizam a competência padronizada (`ano_mes`) derivada da dimensão conformada de tempo.
