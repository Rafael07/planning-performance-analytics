"""Módulo de Geração de Dados Sintéticos (Projeto Integra-Dignidade).

Gera bases relacionais sintéticas com integridade referencial estrita,
sazonalidade e distribuição probabilística realista para o setor de
planos de assistência familiar e funerários do Grupo Dignidade.
"""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("pt_BR")
random.seed(42)
np.random.seed(42)


def generate_dim_calendario(
    start_date: date = date(2024, 1, 1),
    end_date: date = date(2026, 12, 31),
) -> pd.DataFrame:
    """Gera a dimensão conformada de tempo contendo todos os dias civis."""
    meses_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    dates: List[date] = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += timedelta(days=1)

    records: List[Dict[str, Any]] = []
    for d in dates:
        # Python weekday: Monday is 0, Sunday is 6.
        # Spec: 1 = Domingo, 7 = Sábado
        dia_semana_spec = (d.weekday() + 1) % 7 + 1
        is_weekend = d.weekday() in (5, 6)

        records.append(
            {
                "data": d,
                "ano": d.year,
                "mes": d.month,
                "nome_mes": meses_pt[d.month],
                "trimestre": (d.month - 1) // 3 + 1,
                "ano_mes": f"{d.year}-{d.month:02d}",
                "dia_semana": dia_semana_spec,
                "flag_dia_util": not is_weekend,
            }
        )

    return pd.DataFrame(records)


def generate_dim_unidades() -> pd.DataFrame:
    """Gera o catálogo de unidades físicas e lojas do Grupo Dignidade."""
    unidades = [
        {
            "id_unidade": "UND-CG-01",
            "nome_cidade": "Campina Grande",
            "tipo_unidade": "Matriz Administrativa",
            "capex_implantacao": 380000.00,
            "opex_mensal_base": 45000.00,
            "data_inauguracao": date(2024, 1, 1),
        },
        {
            "id_unidade": "UND-JP-01",
            "nome_cidade": "João Pessoa",
            "tipo_unidade": "Loja Conceito",
            "capex_implantacao": 290000.00,
            "opex_mensal_base": 36000.00,
            "data_inauguracao": date(2024, 2, 1),
        },
        {
            "id_unidade": "UND-PATOS-01",
            "nome_cidade": "Patos",
            "tipo_unidade": "Ponto de Apoio",
            "capex_implantacao": 165000.00,
            "opex_mensal_base": 22000.00,
            "data_inauguracao": date(2024, 4, 1),
        },
        {
            "id_unidade": "UND-GUA-01",
            "nome_cidade": "Guarabira",
            "tipo_unidade": "Ponto de Apoio",
            "capex_implantacao": 150000.00,
            "opex_mensal_base": 19500.00,
            "data_inauguracao": date(2024, 7, 1),
        },
        {
            "id_unidade": "UND-JP-02",
            "nome_cidade": "João Pessoa",
            "tipo_unidade": "Ponto de Apoio",
            "capex_implantacao": 180000.00,
            "opex_mensal_base": 24000.00,
            "data_inauguracao": date(2025, 2, 1),
        },
    ]
    return pd.DataFrame(unidades)


def generate_dim_planos() -> pd.DataFrame:
    """Gera o portfólio de produtos e planos de assistência familiar."""
    planos = [
        {
            "id_plano": "PLN-IND-01",
            "nome_plano": "Individual Essencial",
            "valor_mensalidade": 39.90,
            "limite_dependentes": 0,
            "cobertura_cremacao": False,
        },
        {
            "id_plano": "PLN-FAM-PRATA",
            "nome_plano": "Familiar Prata",
            "valor_mensalidade": 59.90,
            "limite_dependentes": 3,
            "cobertura_cremacao": False,
        },
        {
            "id_plano": "PLN-FAM-OURO",
            "nome_plano": "Familiar Ouro Especial",
            "valor_mensalidade": 89.90,
            "limite_dependentes": 5,
            "cobertura_cremacao": True,
        },
        {
            "id_plano": "PLN-PREM-CREM",
            "nome_plano": "Dignidade Nobre Crematório",
            "valor_mensalidade": 119.90,
            "limite_dependentes": 5,
            "cobertura_cremacao": True,
        },
    ]
    return pd.DataFrame(planos)


def generate_fct_contratos(
    df_unidades: pd.DataFrame,
    df_planos: pd.DataFrame,
    n_contratos: int = 4200,
) -> pd.DataFrame:
    """Gera matrículas contratuais com status de carteira e motivos de cancelamento."""
    unidades_dict = df_unidades.set_index("id_unidade")["data_inauguracao"].to_dict()
    unidades_ids = list(unidades_dict.keys())
    # Pesos de captação por filial (Matriz e João Pessoa captam mais)
    pesos_unidades = [0.35, 0.28, 0.15, 0.12, 0.10]

    planos_ids = df_planos["id_plano"].tolist()
    pesos_planos = [0.15, 0.45, 0.30, 0.10]  # Prata e Ouro dominam

    motivos_churn = ["Preço", "Financeiro", "Mudança de Endereço", "Atendimento"]
    pesos_churn = [0.42, 0.30, 0.18, 0.10]

    records: List[Dict[str, Any]] = []

    for i in range(1, n_contratos + 1):
        id_contrato = f"CTR-{2024 + (i % 3)}-{i:05d}"
        id_cliente = f"CLI-{10000 + i}"
        id_unidade = np.random.choice(unidades_ids, p=pesos_unidades)
        id_plano = np.random.choice(planos_ids, p=pesos_planos)

        data_inaug = unidades_dict[id_unidade]
        # Data de adesão entre a inauguração da loja e 30/09/2026
        max_date = date(2026, 9, 30)
        dias_disponiveis = (max_date - data_inaug).days
        if dias_disponiveis <= 1:
            dias_adesao = 1
        else:
            dias_adesao = random.randint(1, dias_disponiveis)
        data_adesao = data_inaug + timedelta(days=dias_adesao)

        # Distribuição de status da carteira: 83% Ativo, 11% Cancelado, 6% Inadimplente
        status = np.random.choice(
            ["Ativo", "Cancelado", "Inadimplente"],
            p=[0.83, 0.11, 0.06],
        )

        data_cancelamento = None
        motivo_cancelamento = None

        if status == "Cancelado":
            # Churn ocorre entre 45 dias após adesão e a data máxima observada
            dias_permanencia = random.randint(45, 450)
            data_cancel = data_adesao + timedelta(days=dias_permanencia)
            if data_cancel > max_date:
                data_cancel = max_date
            data_cancelamento = data_cancel
            motivo_cancelamento = np.random.choice(motivos_churn, p=pesos_churn)

        records.append(
            {
                "id_contrato": id_contrato,
                "id_cliente": id_cliente,
                "id_unidade": id_unidade,
                "id_plano": id_plano,
                "data_adesao": data_adesao,
                "status_contrato": status,
                "data_cancelamento": data_cancelamento,
                "motivo_cancelamento": motivo_cancelamento,
            }
        )

    return pd.DataFrame(records)


def generate_fct_atendimentos(
    df_contratos: pd.DataFrame,
    n_atendimentos: int = 750,
) -> pd.DataFrame:
    """Gera acionamentos de emergência 24h e sinistros funerários.
    
    Inclui tempos de ciclo (lead time) com distribuição realista e causas especiais
    de variabilidade para alimentar o Controle Estatístico de Processo (CEP).
    """
    records: List[Dict[str, Any]] = []

    # Seleciona contratos elegíveis (ativos ou cancelados que estiveram vigentes)
    contratos_amostra = df_contratos.sample(n=n_atendimentos, replace=True, random_state=42)

    for i, (_, row) in enumerate(contratos_amostra.iterrows(), start=1):
        id_atendimento = f"ATD-{2024 + (i % 3)}-{i:04d}"
        id_contrato = row["id_contrato"]
        id_unidade = row["id_unidade"]
        data_adesao = row["data_adesao"]
        data_cancel = row["data_cancelamento"]

        # Determina janela válida do evento
        limite_superior = data_cancel if pd.notnull(data_cancel) else date(2026, 9, 30)
        dias_janela = (limite_superior - data_adesao).days

        if dias_janela <= 5:
            data_acionamento = data_adesao + timedelta(days=random.randint(1, max(2, dias_janela)))
        else:
            data_acionamento = data_adesao + timedelta(days=random.randint(5, dias_janela))

        # Hora aleatória de acionamento (operação 24h ininterrupta)
        hora = random.randint(0, 23)
        minuto = random.randint(0, 59)
        ts_acionamento = datetime(
            data_acionamento.year,
            data_acionamento.month,
            data_acionamento.day,
            hora,
            minuto,
        )

        # Lead time (tempo_ciclo_horas):
        # 94% dos casos: média de 16h com desvio padrão de 2.8h (processo normal de velório/sepultamento)
        # 6% dos casos: causas especiais anômalas (27h a 44h devido a liberação em IML, cartório fechado no plantão ou traslado intermunicipal longo)
        is_causa_especial = random.random() < 0.06
        if is_causa_especial:
            lead_time = float(np.round(np.random.uniform(27.5, 42.0), 2))
        else:
            lead_time = float(np.round(np.clip(np.random.normal(16.0, 2.8), 8.0, 25.5), 2))

        ts_conclusao = ts_acionamento + timedelta(hours=lead_time)

        # Custo direto do serviço funerário (urna, tanatopraxia, ornamentação, traslado)
        custo_direto = float(np.round(np.random.normal(1480.0, 160.0), 2))
        custo_direto = max(1150.0, custo_direto)

        records.append(
            {
                "id_atendimento": id_atendimento,
                "id_contrato": id_contrato,
                "id_unidade": id_unidade,
                "data_acionamento": data_acionamento,
                "timestamp_acionamento": ts_acionamento,
                "timestamp_conclusao": ts_conclusao,
                "tempo_ciclo_horas": lead_time,
                "custo_direto_servico": custo_direto,
            }
        )

    return pd.DataFrame(records)


def generate_fct_leads_crm(
    df_unidades: pd.DataFrame,
    n_leads: int = 1850,
) -> pd.DataFrame:
    """Gera o funil de captação de clientes em lojas físicas."""
    unidades_ids = df_unidades["id_unidade"].tolist()
    pesos_unidades = [0.35, 0.28, 0.15, 0.12, 0.10]

    etapas = [
        "Sem Contato",
        "1º Contato",
        "Qualificação",
        "Negociação",
        "Fechado",
        "Desqualificado",
    ]
    pesos_etapas = [0.12, 0.18, 0.22, 0.20, 0.16, 0.12]

    records: List[Dict[str, Any]] = []
    data_inicio = date(2025, 1, 1)
    data_fim = date(2026, 9, 30)
    total_dias = (data_fim - data_inicio).days

    for i in range(1, n_leads + 1):
        id_lead = f"LEAD-2025-{i:05d}"
        id_unidade = np.random.choice(unidades_ids, p=pesos_unidades)
        etapa = np.random.choice(etapas, p=pesos_etapas)

        data_criacao = data_inicio + timedelta(days=random.randint(0, total_dias))

        # Dias no estágio dependem da fase do pipeline
        if etapa in ("Fechado", "Desqualificado"):
            dias_estagio = random.randint(1, 15)
        elif etapa in ("Qualificação", "Negociação"):
            # Alguns leads com gargalo/aging alto
            dias_estagio = int(np.random.choice([random.randint(2, 6), random.randint(8, 28)], p=[0.75, 0.25]))
        else:
            dias_estagio = random.randint(1, 4)

        records.append(
            {
                "id_lead": id_lead,
                "id_unidade": id_unidade,
                "etapa_funil": etapa,
                "data_criacao": data_criacao,
                "dias_no_estagio": dias_estagio,
            }
        )

    return pd.DataFrame(records)


def generate_all_datasets() -> Dict[str, pd.DataFrame]:
    """Gera todos os DataFrames do modelo dimensional relacional."""
    print("-> Gerando dim_calendario...")
    df_cal = generate_dim_calendario()

    print("-> Gerando dim_unidades...")
    df_uni = generate_dim_unidades()

    print("-> Gerando dim_planos...")
    df_pla = generate_dim_planos()

    print("-> Gerando fct_contratos...")
    df_ctr = generate_fct_contratos(df_uni, df_pla)

    print("-> Gerando fct_atendimentos...")
    df_atd = generate_fct_atendimentos(df_ctr)

    print("-> Gerando fct_leads_crm...")
    df_crm = generate_fct_leads_crm(df_uni)

    return {
        "dim_calendario": df_cal,
        "dim_unidades": df_uni,
        "dim_planos": df_pla,
        "fct_contratos": df_ctr,
        "fct_atendimentos": df_atd,
        "fct_leads_crm": df_crm,
    }


if __name__ == "__main__":
    from src.database import init_database
    print("-> Iniciando geração de dados e carga no DuckDB...")
    init_database()

