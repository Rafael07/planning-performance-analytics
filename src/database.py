"""Módulo de Banco de Dados e Ingestão DuckDB (Projeto Integra-Dignidade).

Gerencia o esquema relacional colunar, DDL, integridade referencial,
ingestão de dados e criação de views analíticas de alta performance.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd

from src.data_generator import generate_all_datasets

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "acolher_analytics.duckdb"


def get_connection(db_path: Optional[str | Path] = None, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """Retorna uma conexão gerenciada ao banco DuckDB.
    
    Caso o arquivo do banco não exista ou esteja vazio (ex: novo clone do projeto),
    ele é automaticamente inicializado e populado com os datasets sintéticos.
    """
    target_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if not target_path.exists() or target_path.stat().st_size == 0:
        init_database(target_path)
    return duckdb.connect(str(target_path), read_only=read_only)


def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    """Cria as tabelas relacionais do modelo de Constelação de Fatos."""
    con.execute("""
    -- Dimensão Conformada de Tempo
    CREATE TABLE IF NOT EXISTS dim_calendario (
        data DATE PRIMARY KEY,
        ano INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        nome_mes VARCHAR NOT NULL,
        trimestre INTEGER NOT NULL,
        ano_mes VARCHAR NOT NULL,
        dia_semana INTEGER NOT NULL,
        flag_dia_util BOOLEAN NOT NULL
    );

    -- Dimensão de Unidades Físicas e Centrais
    CREATE TABLE IF NOT EXISTS dim_unidades (
        id_unidade VARCHAR PRIMARY KEY,
        nome_cidade VARCHAR NOT NULL,
        tipo_unidade VARCHAR NOT NULL,
        capex_implantacao DECIMAL(12,2) NOT NULL,
        opex_mensal_base DECIMAL(12,2) NOT NULL,
        data_inauguracao DATE NOT NULL
    );

    -- Dimensão de Portfólio de Planos
    CREATE TABLE IF NOT EXISTS dim_planos (
        id_plano VARCHAR PRIMARY KEY,
        nome_plano VARCHAR NOT NULL,
        valor_mensalidade DECIMAL(10,2) NOT NULL,
        limite_dependentes INTEGER NOT NULL,
        cobertura_cremacao BOOLEAN NOT NULL
    );

    -- Fato: Contratos e Gestão de Carteira
    CREATE TABLE IF NOT EXISTS fct_contratos (
        id_contrato VARCHAR PRIMARY KEY,
        id_cliente VARCHAR NOT NULL,
        id_unidade VARCHAR NOT NULL,
        id_plano VARCHAR NOT NULL,
        data_adesao DATE NOT NULL,
        status_contrato VARCHAR NOT NULL,
        data_cancelamento DATE,
        motivo_cancelamento VARCHAR
    );

    -- Fato: Acionamentos Funerários e Sinistros 24h
    CREATE TABLE IF NOT EXISTS fct_atendimentos (
        id_atendimento VARCHAR PRIMARY KEY,
        id_contrato VARCHAR NOT NULL,
        id_unidade VARCHAR NOT NULL,
        data_acionamento DATE NOT NULL,
        timestamp_acionamento TIMESTAMP NOT NULL,
        timestamp_conclusao TIMESTAMP NOT NULL,
        tempo_ciclo_horas DECIMAL(6,2) NOT NULL,
        custo_direto_servico DECIMAL(10,2) NOT NULL
    );

    -- Fato: Leads CRM e Funil de Captação em Loja
    CREATE TABLE IF NOT EXISTS fct_leads_crm (
        id_lead VARCHAR PRIMARY KEY,
        id_unidade VARCHAR NOT NULL,
        etapa_funil VARCHAR NOT NULL,
        data_criacao DATE NOT NULL,
        dias_no_estagio INTEGER NOT NULL
    );
    """)


def ingest_data(con: duckdb.DuckDBPyConnection) -> None:
    """Popula as tabelas do DuckDB a partir dos geradores sintéticos."""
    datasets = generate_all_datasets()

    for table_name, df in datasets.items():
        print(f"-> Ingerindo dados na tabela '{table_name}' ({len(df)} linhas)...")
        con.execute(f"DELETE FROM {table_name}")
        con.register(f"temp_{table_name}", df)
        con.execute(f"INSERT INTO {table_name} SELECT * FROM temp_{table_name}")
        con.unregister(f"temp_{table_name}")


def create_views(con: duckdb.DuckDBPyConnection) -> None:
    """Cria views analíticas padronizadas para consultas executivas imediatas."""
    con.execute("""
    -- View 1: Resumo Mensal Consolidado da Carteira
    CREATE OR REPLACE VIEW vw_kpis_mensais_carteira AS
    WITH base_mes AS (
        SELECT 
            c.ano_mes,
            c.ano,
            c.mes,
            MAX(c.nome_mes) AS nome_mes,
            COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Ativo') AS contratos_ativos,
            COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Cancelado') AS contratos_cancelados,
            COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Inadimplente') AS contratos_inadimplentes,
            COALESCE(SUM(p.valor_mensalidade) FILTER (WHERE ctr.status_contrato = 'Ativo'), 0) AS mrr
        FROM dim_calendario c
        LEFT JOIN fct_contratos ctr 
            ON ctr.data_adesao <= c.data 
            AND (ctr.data_cancelamento IS NULL OR ctr.data_cancelamento > c.data)
        LEFT JOIN dim_planos p ON ctr.id_plano = p.id_plano
        WHERE c.data IN (SELECT MAX(data) FROM dim_calendario GROUP BY ano_mes)
        GROUP BY c.ano_mes, c.ano, c.mes
    )
    SELECT 
        ano_mes,
        ano,
        mes,
        nome_mes,
        contratos_ativos,
        contratos_cancelados,
        contratos_inadimplentes,
        mrr,
        ROUND(mrr / NULLIF(contratos_ativos, 0), 2) AS ticket_medio,
        ROUND((contratos_inadimplentes * 100.0) / NULLIF(contratos_ativos + contratos_inadimplentes, 0), 2) AS taxa_inadimplencia_pct
    FROM base_mes
    ORDER BY ano_mes;

    -- View 2: Estatística de Controle de Processo (CEP) de Atendimentos
    CREATE OR REPLACE VIEW vw_cep_atendimentos AS
    WITH estatisticas_gerais AS (
        SELECT 
            AVG(tempo_ciclo_horas) AS media_horas,
            STDDEV_SAMP(tempo_ciclo_horas) AS desvio_padrao
        FROM fct_atendimentos
    )
    SELECT 
        a.id_atendimento,
        a.id_contrato,
        a.id_unidade,
        u.nome_cidade,
        u.tipo_unidade,
        a.data_acionamento,
        a.timestamp_acionamento,
        a.timestamp_conclusao,
        a.tempo_ciclo_horas,
        a.custo_direto_servico,
        ROUND(eg.media_horas, 2) AS media_controle,
        ROUND(eg.media_horas + 3 * eg.desvio_padrao, 2) AS limite_superior_controle,
        ROUND(GREATEST(0, eg.media_horas - 3 * eg.desvio_padrao), 2) AS limite_inferior_controle,
        CASE 
            WHEN a.tempo_ciclo_horas > (eg.media_horas + 3 * eg.desvio_padrao) THEN 'Causa Especial (Atraso Anômalo)'
            WHEN a.tempo_ciclo_horas < GREATEST(0, eg.media_horas - 3 * eg.desvio_padrao) THEN 'Causa Especial (Subnotificação)'
            ELSE 'Causa Comum (Estável)'
        END AS status_cep
    FROM fct_atendimentos a
    JOIN dim_unidades u ON a.id_unidade = u.id_unidade
    CROSS JOIN estatisticas_gerais eg;
    """)


def validate_contracts(con: duckdb.DuckDBPyConnection) -> bool:
    """Executa checagens de integridade referencial e contratos de dados."""
    print("-> Validando integridade relacional e contratos de dados...")

    # 1. Checagem de integridade de unidade em contratos
    orfaos_unidades = con.execute("""
        SELECT COUNT(*) FROM fct_contratos c 
        LEFT JOIN dim_unidades u ON c.id_unidade = u.id_unidade 
        WHERE u.id_unidade IS NULL
    """).fetchone()[0]

    # 2. Checagem de cancelamentos sem data ou motivo
    cancelados_invalidos = con.execute("""
        SELECT COUNT(*) FROM fct_contratos 
        WHERE status_contrato = 'Cancelado' 
          AND (data_cancelamento IS NULL OR motivo_cancelamento IS NULL)
    """).fetchone()[0]

    # 3. Checagem de lead time operacional (0 < tempo_ciclo_horas < 72)
    lead_time_invalido = con.execute("""
        SELECT COUNT(*) FROM fct_atendimentos 
        WHERE tempo_ciclo_horas <= 0 OR tempo_ciclo_horas >= 72
    """).fetchone()[0]

    if orfaos_unidades > 0:
        raise ValueError(f"Violação de contrato: {orfaos_unidades} contratos com unidade inexistente.")
    if cancelados_invalidos > 0:
        raise ValueError(f"Violação de contrato: {cancelados_invalidos} contratos cancelados sem data/motivo.")
    if lead_time_invalido > 0:
        raise ValueError(f"Violação de contrato: {lead_time_invalido} atendimentos com lead time fora do intervalo (0, 72h).")

    print("[OK] Todos os contratos de dados e integridades foram validados com 100% de conformidade!")
    return True


def init_database(db_path: Optional[str | Path] = None) -> None:
    """Rotina completa de inicialização do banco de dados DuckDB."""
    con = get_connection(db_path)
    try:
        create_schema(con)
        ingest_data(con)
        create_views(con)
        validate_contracts(con)
        print("-> Banco DuckDB inicializado com sucesso!")
    finally:
        con.close()


if __name__ == "__main__":
    init_database()
