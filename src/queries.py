"""Módulo de Consultas Analíticas em SQL Puro (Projeto Integra-Dignidade).

Implementa todas as agregações, janelas estatísticas e transformações relacionais
necessárias para alimentar o Balanced Scorecard (BSC), a Simulação Paramétrica,
o Controle Estatístico de Processo (CEP) e o Funil Comercial de Lojas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

from src.database import get_connection


def get_available_competencies() -> List[str]:
    """Retorna lista ordenada das competências (ano_mes) disponíveis."""
    con = get_connection(read_only=True)
    try:
        df = con.execute("""
            SELECT DISTINCT ano_mes 
            FROM dim_calendario 
            WHERE ano_mes <= '2026-09'
            ORDER BY ano_mes DESC
        """).df()
        return df["ano_mes"].tolist()
    finally:
        con.close()


def get_units_list() -> List[Dict[str, str]]:
    """Retorna identificadores e nomes das unidades físicas."""
    con = get_connection(read_only=True)
    try:
        df = con.execute("""
            SELECT id_unidade, nome_cidade, tipo_unidade 
            FROM dim_unidades 
            ORDER BY id_unidade
        """).df()
        return df.to_dict(orient="records")
    finally:
        con.close()


def get_executive_kpis(ano_mes: str, id_unidade: Optional[str] = None) -> Dict[str, Any]:
    """Calcula os indicadores executivos consolidados para a competência selecionada."""
    con = get_connection(read_only=True)
    try:
        unit_filter = "AND ctr.id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        unit_filter_atd = "AND a.id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        unit_filter_can = "AND c_cancel.id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        
        params: List[Any] = [ano_mes]
        if id_unidade and id_unidade != "TODAS":
            params.append(id_unidade)

        query = f"""
        WITH ultimo_dia AS (
            SELECT MAX(data) AS data_limite
            FROM dim_calendario
            WHERE ano_mes = ?
        ),
        primeiro_dia AS (
            SELECT MIN(data) AS data_inicio
            FROM dim_calendario
            WHERE ano_mes = ?
        ),
        ativos_inicio AS (
            SELECT COUNT(DISTINCT ctr.id_contrato) AS total_ativos_inicio
            FROM fct_contratos ctr, primeiro_dia pd
            WHERE ctr.data_adesao < pd.data_inicio
              AND (ctr.data_cancelamento IS NULL OR ctr.data_cancelamento >= pd.data_inicio)
              {unit_filter}
        ),
        base_carteira AS (
            SELECT 
                COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Ativo') AS contratos_ativos,
                COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Inadimplente') AS contratos_inadimplentes,
                COALESCE(SUM(p.valor_mensalidade) FILTER (WHERE ctr.status_contrato = 'Ativo'), 0) AS mrr
            FROM fct_contratos ctr
            CROSS JOIN ultimo_dia ud
            JOIN dim_planos p ON ctr.id_plano = p.id_plano
            WHERE ctr.data_adesao <= ud.data_limite
              AND (ctr.data_cancelamento IS NULL OR ctr.data_cancelamento > ud.data_limite)
              {unit_filter}
        ),
        cancelamentos_mes AS (
            SELECT COUNT(DISTINCT c_cancel.id_contrato) AS cancelados_no_mes
            FROM fct_contratos c_cancel
            JOIN dim_calendario c ON c_cancel.data_cancelamento = c.data
            WHERE c.ano_mes = ?
              {unit_filter_can}
        ),
        atendimentos_mes AS (
            SELECT 
                COUNT(a.id_atendimento) AS sinistros_mes,
                COALESCE(SUM(a.custo_direto_servico), 0) AS custo_total_sinistros
            FROM fct_atendimentos a
            JOIN dim_calendario c ON a.data_acionamento = c.data
            WHERE c.ano_mes = ?
              {unit_filter_atd}
        )
        SELECT 
            bc.contratos_ativos,
            bc.contratos_inadimplentes,
            bc.mrr,
            ai.total_ativos_inicio,
            cm.cancelados_no_mes,
            am.sinistros_mes,
            am.custo_total_sinistros
        FROM base_carteira bc
        CROSS JOIN ativos_inicio ai
        CROSS JOIN cancelamentos_mes cm
        CROSS JOIN atendimentos_mes am
        """

        # Prepara lista de parâmetros para a query
        sql_params = [ano_mes, ano_mes]
        if id_unidade and id_unidade != "TODAS":
            sql_params.append(id_unidade)
        sql_params.append(ano_mes)
        if id_unidade and id_unidade != "TODAS":
            sql_params.append(id_unidade)
        sql_params.append(ano_mes)
        if id_unidade and id_unidade != "TODAS":
            sql_params.append(id_unidade)

        res = con.execute(query, sql_params).fetchone()

        contratos_ativos = res[0] or 0
        contratos_inadimplentes = res[1] or 0
        mrr = float(res[2] or 0.0)
        total_ativos_inicio = res[3] or 1
        cancelados_no_mes = res[4] or 0
        sinistros_mes = res[5] or 0
        custo_sinistros = float(res[6] or 0.0)

        ticket_medio = round(mrr / contratos_ativos, 2) if contratos_ativos > 0 else 0.0
        taxa_inadimplencia = round(
            (contratos_inadimplentes * 100.0) / (contratos_ativos + contratos_inadimplentes), 2
        ) if (contratos_ativos + contratos_inadimplentes) > 0 else 0.0
        
        churn_rate = round(
            (cancelados_no_mes * 100.0) / max(total_ativos_inicio, 1), 2
        )

        taxa_sinistralidade = round(
            (sinistros_mes * 12 * 100.0) / max(contratos_ativos, 1), 2
        )

        ltv = round(ticket_medio / (churn_rate / 100.0), 2) if churn_rate > 0 else 0.0

        return {
            "mrr": mrr,
            "contratos_ativos": contratos_ativos,
            "contratos_inadimplentes": contratos_inadimplentes,
            "ticket_medio": ticket_medio,
            "churn_rate": churn_rate,
            "taxa_inadimplencia": taxa_inadimplencia,
            "sinistralidade_anualizada": taxa_sinistralidade,
            "sinistros_mes": sinistros_mes,
            "custo_total_sinistros": custo_sinistros,
            "ltv": ltv,
            # Metas BSC corporativas de referência
            "meta_mrr": 200000.0,
            "meta_churn": 1.8,
            "meta_inadimplencia": 4.5,
            "meta_sinistralidade": 2.2,
            "meta_ticket_medio": 52.0,
        }
    finally:
        con.close()


def get_churn_reasons(ano_mes: Optional[str] = None, id_unidade: Optional[str] = None) -> pd.DataFrame:
    """Retorna estratificação dos motivos de cancelamento informados na ponta."""
    con = get_connection(read_only=True)
    try:
        where_clauses = ["motivo_cancelamento IS NOT NULL"]
        params: List[Any] = []

        if ano_mes:
            where_clauses.append("c.ano_mes = ?")
            params.append(ano_mes)
        if id_unidade and id_unidade != "TODAS":
            where_clauses.append("ctr.id_unidade = ?")
            params.append(id_unidade)

        where_stmt = " AND ".join(where_clauses)

        query = f"""
        SELECT 
            ctr.motivo_cancelamento,
            COUNT(*) AS total_cancelamentos,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS percentual
        FROM fct_contratos ctr
        JOIN dim_calendario c ON ctr.data_cancelamento = c.data
        WHERE {where_stmt}
        GROUP BY ctr.motivo_cancelamento
        ORDER BY total_cancelamentos DESC
        """
        return con.execute(query, params).df()
    finally:
        con.close()


def get_monthly_evolution() -> pd.DataFrame:
    """Retorna série temporal de evolução das principais métricas do negócio."""
    con = get_connection(read_only=True)
    try:
        query = """
        SELECT 
            ano_mes,
            nome_mes,
            ano,
            contratos_ativos,
            mrr,
            ticket_medio,
            taxa_inadimplencia_pct
        FROM vw_kpis_mensais_carteira
        WHERE ano_mes <= '2026-09'
        ORDER BY ano_mes
        """
        return con.execute(query).df()
    finally:
        con.close()


def simulate_parametric_scenario(
    preco_var_pct: float,
    churn_elasticity: float,
    sinistralidade_var_pct: float,
    id_unidade: Optional[str] = None,
) -> Dict[str, Any]:
    """Executa simulação de sensibilidade de margem operacional sob incerteza."""
    base_kpi = get_executive_kpis("2026-09", id_unidade)

    base_mrr = base_kpi["mrr"]
    base_ativos = base_kpi["contratos_ativos"]
    base_ticket = base_kpi["ticket_medio"]
    base_custo_sinistros = base_kpi["custo_total_sinistros"]

    # Obter Opex Total
    con = get_connection(read_only=True)
    try:
        if id_unidade and id_unidade != "TODAS":
            opex_total = con.execute(
                "SELECT COALESCE(opex_mensal_base, 0) FROM dim_unidades WHERE id_unidade = ?",
                [id_unidade],
            ).fetchone()[0]
        else:
            opex_total = con.execute("SELECT SUM(opex_mensal_base) FROM dim_unidades").fetchone()[0]
    finally:
        con.close()

    opex_total = float(opex_total or 0.0)

    # Elasticidade: impacto do aumento/redução de preço na base ativa
    # Se preço sobe 10% e elasticidade é 0.16 -> perda estrutural adicional na base
    fator_preco = 1.0 + (preco_var_pct / 100.0)
    variacao_base_churn = - (preco_var_pct * (churn_elasticity / 5.0)) / 100.0
    fator_base = max(0.5, 1.0 + variacao_base_churn)

    ativos_projetados = int(round(base_ativos * fator_base))
    ticket_projetado = round(base_ticket * fator_preco, 2)
    mrr_projetado = round(ativos_projetados * ticket_projetado, 2)

    # Variação de custo de sinistralidade
    fator_sinistralidade = 1.0 + (sinistralidade_var_pct / 100.0)
    custo_sinistros_projetado = round(base_custo_sinistros * fator_base * fator_sinistralidade, 2)

    # Margem Operacional = MRR - (Custos de Sinistros + Opex Base)
    margem_base = round(base_mrr - (base_custo_sinistros + opex_total), 2)
    margem_projetada = round(mrr_projetado - (custo_sinistros_projetado + opex_total), 2)
    delta_margem = round(margem_projetada - margem_base, 2)
    delta_margem_pct = round((delta_margem / abs(margem_base)) * 100.0, 2) if margem_base != 0 else 0.0

    return {
        "base_mrr": base_mrr,
        "mrr_projetado": mrr_projetado,
        "delta_mrr": round(mrr_projetado - base_mrr, 2),
        "base_ativos": base_ativos,
        "ativos_projetados": ativos_projetados,
        "base_ticket": base_ticket,
        "ticket_projetado": ticket_projetado,
        "opex_total": opex_total,
        "base_custo_sinistros": base_custo_sinistros,
        "custo_sinistros_projetado": custo_sinistros_projetado,
        "margem_base": margem_base,
        "margem_projetada": margem_projetada,
        "delta_margem": delta_margem,
        "delta_margem_pct": delta_margem_pct,
    }


def get_units_breakeven_analysis() -> pd.DataFrame:
    """Calcula o ponto de equilíbrio (breakeven em número de contratos) por unidade."""
    con = get_connection(read_only=True)
    try:
        query = """
        WITH metricas_unidades AS (
            SELECT 
                u.id_unidade,
                u.nome_cidade,
                u.tipo_unidade,
                u.capex_implantacao,
                u.opex_mensal_base,
                COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Ativo') AS contratos_ativos,
                COALESCE(SUM(p.valor_mensalidade) FILTER (WHERE ctr.status_contrato = 'Ativo'), 0) AS mrr_unidade,
                ROUND(COALESCE(SUM(p.valor_mensalidade) FILTER (WHERE ctr.status_contrato = 'Ativo'), 0) / 
                      NULLIF(COUNT(DISTINCT ctr.id_contrato) FILTER (WHERE ctr.status_contrato = 'Ativo'), 0), 2) AS ticket_medio_unidade
            FROM dim_unidades u
            LEFT JOIN fct_contratos ctr ON u.id_unidade = ctr.id_unidade
            LEFT JOIN dim_planos p ON ctr.id_plano = p.id_plano
            GROUP BY u.id_unidade, u.nome_cidade, u.tipo_unidade, u.capex_implantacao, u.opex_mensal_base
        ),
        custo_marginal AS (
            SELECT 
                AVG(custo_direto_servico * 0.002) AS custo_marginal_cobertura -- Custo marginal estimado por contrato/mês
            FROM fct_atendimentos
        )
        SELECT 
            m.id_unidade,
            m.nome_cidade,
            m.tipo_unidade,
            m.capex_implantacao,
            m.opex_mensal_base,
            m.contratos_ativos,
            m.mrr_unidade,
            m.ticket_medio_unidade,
            -- Breakeven = Opex / (Ticket Médio - Custo Marginal)
            ROUND(m.opex_mensal_base / NULLIF(m.ticket_medio_unidade - cm.custo_marginal_cobertura, 0), 0) AS contratos_breakeven,
            ROUND(m.contratos_ativos - (m.opex_mensal_base / NULLIF(m.ticket_medio_unidade - cm.custo_marginal_cobertura, 0)), 0) AS saldo_acima_breakeven,
            CASE 
                WHEN m.contratos_ativos >= (m.opex_mensal_base / NULLIF(m.ticket_medio_unidade - cm.custo_marginal_cobertura, 0)) THEN 'Operação Superavitária'
                ELSE 'Em Maturação / Abaixo do Breakeven'
            END AS status_financeiro
        FROM metricas_unidades m
        CROSS JOIN custo_marginal cm
        ORDER BY m.id_unidade
        """
        return con.execute(query).df()
    finally:
        con.close()


def get_cep_data(id_unidade: Optional[str] = None) -> Dict[str, Any]:
    """Retorna dados estatísticos de Controle de Processo (CEP 3-sigma) para atendimentos."""
    con = get_connection(read_only=True)
    try:
        where_clause = "WHERE id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        params = [id_unidade] if id_unidade and id_unidade != "TODAS" else []

        df_atendimentos = con.execute(f"""
            SELECT 
                id_atendimento,
                id_contrato,
                id_unidade,
                nome_cidade,
                tipo_unidade,
                data_acionamento,
                timestamp_acionamento,
                tempo_ciclo_horas,
                custo_direto_servico,
                media_controle,
                limite_superior_controle,
                limite_inferior_controle,
                status_cep
            FROM vw_cep_atendimentos
            {where_clause}
            ORDER BY timestamp_acionamento ASC
        """, params).df()

        total = len(df_atendimentos)
        anomalos = len(df_atendimentos[df_atendimentos["status_cep"] != "Causa Comum (Estável)"])
        conformidade_pct = round(((total - anomalos) / max(total, 1)) * 100.0, 2)

        return {
            "df": df_atendimentos,
            "total_atendimentos": total,
            "total_anomalias": anomalos,
            "taxa_estabilidade_pct": conformidade_pct,
            "media_horas": df_atendimentos["media_controle"].iloc[0] if not df_atendimentos.empty else 0.0,
            "lsc_horas": df_atendimentos["limite_superior_controle"].iloc[0] if not df_atendimentos.empty else 0.0,
            "lic_horas": df_atendimentos["limite_inferior_controle"].iloc[0] if not df_atendimentos.empty else 0.0,
        }
    finally:
        con.close()


def get_funnel_summary(id_unidade: Optional[str] = None) -> pd.DataFrame:
    """Retorna o funil comercial consolidado e o tempo de permanência nos estágios."""
    con = get_connection(read_only=True)
    try:
        where_clause = "WHERE id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        params = [id_unidade] if id_unidade and id_unidade != "TODAS" else []

        query = f"""
        WITH ordem_funil AS (
            SELECT 'Sem Contato' AS etapa, 1 AS ordem UNION ALL
            SELECT '1º Contato', 2 UNION ALL
            SELECT 'Qualificação', 3 UNION ALL
            SELECT 'Negociação', 4 UNION ALL
            SELECT 'Fechado', 5 UNION ALL
            SELECT 'Desqualificado', 6
        )
        SELECT 
            f.etapa_funil,
            COUNT(*) AS total_leads,
            ROUND(AVG(f.dias_no_estagio), 1) AS media_dias_estagio,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS percentual_total
        FROM fct_leads_crm f
        JOIN ordem_funil o ON f.etapa_funil = o.etapa
        {where_clause}
        GROUP BY f.etapa_funil, o.ordem
        ORDER BY o.ordem
        """
        return con.execute(query, params).df()
    finally:
        con.close()


def get_strategic_scenarios_table(id_unidade: Optional[str] = None) -> pd.DataFrame:
    """Gera tabela comparativa estruturada dos 3 cenários executivos formais (Estresse, Base, Otimista)."""
    cenarios_config = [
        {"nome": "1. Estresse (Pessimista)", "preco": -5.0, "elast": 1.5, "sinistros": 20.0},
        {"nome": "2. Base (Status Quo)", "preco": 0.0, "elast": 0.8, "sinistros": 0.0},
        {"nome": "3. Otimista (Expansão)", "preco": 8.0, "elast": 0.5, "sinistros": -5.0},
    ]

    linhas: List[Dict[str, Any]] = []

    for c in cenarios_config:
        res = simulate_parametric_scenario(c["preco"], c["elast"], c["sinistros"], id_unidade)
        linhas.append({
            "Cenário Estratégico": c["nome"],
            "Preço Mensalidade": f"{c['preco']:+.1f}%",
            "Sinistralidade": f"{c['sinistros']:+.1f}%",
            "MRR Projetado (R$)": f"R$ {res['mrr_projetado']:,.2f}",
            "Base Ativa": f"{res['ativos_projetados']:,} contratos",
            "Custo Sinistros (R$)": f"R$ {res['custo_sinistros_projetado']:,.2f}",
            "Margem Operacional (R$)": f"R$ {res['margem_projetada']:,.2f}",
            "Variação vs Base": f"{res['delta_margem_pct']:+.1f}%",
        })

    return pd.DataFrame(linhas)


def get_commercial_pace(id_unidade: Optional[str] = None) -> Dict[str, Any]:
    """Calcula o ritmo operacional de captação (bater bumbo) e cobertura de Opex."""
    con = get_connection(read_only=True)
    try:
        where_clause = "WHERE id_unidade = ?" if id_unidade and id_unidade != "TODAS" else ""
        params = [id_unidade] if id_unidade and id_unidade != "TODAS" else []

        leads_fechados = con.execute(f"""
            SELECT COUNT(*) 
            FROM fct_leads_crm 
            {where_clause} {"AND" if where_clause else "WHERE"} etapa_funil = 'Fechado'
        """, params).fetchone()[0]

        total_leads = con.execute(f"""
            SELECT COUNT(*) 
            FROM fct_leads_crm 
            {where_clause}
        """, params).fetchone()[0]

        # Estimativa de meta de ritmo de captação semanal baseada no Opex
        if id_unidade and id_unidade != "TODAS":
            opex = con.execute("SELECT opex_mensal_base FROM dim_unidades WHERE id_unidade = ?", [id_unidade]).fetchone()[0]
        else:
            opex = con.execute("SELECT SUM(opex_mensal_base) FROM dim_unidades").fetchone()[0]
        
        opex = float(opex or 0.0)
        meta_mensal_novas_vendas = max(15, int(round(opex / 1400.0)))
        meta_semanal = max(4, int(round(meta_mensal_novas_vendas / 4.0)))

        ritmo_semanal_atual = max(3, int(round(leads_fechados / 30.0)))
        atingimento_pct = round((ritmo_semanal_atual / meta_semanal) * 100.0, 1)

        return {
            "leads_fechados": leads_fechados,
            "total_leads": total_leads,
            "taxa_conversao_geral": round((leads_fechados * 100.0) / max(total_leads, 1), 1),
            "meta_semanal_vendas": meta_semanal,
            "ritmo_semanal_atual": ritmo_semanal_atual,
            "atingimento_ritmo_pct": atingimento_pct,
            "status_ritmo": "Cadência Saudável (Bate Meta)" if atingimento_pct >= 90.0 else "Atenção: Ritmo Abaixo da Meta",
        }
    finally:
        con.close()

