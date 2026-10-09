"""Planning & Performance Analytics - Plataforma Executiva (Projeto Integra-Dignidade).

Interface de inteligência analítica, simulação de sensibilidade de cenários,
controle estatístico de processos (CEP) e pipeline comercial para o Grupo Dignidade.
"""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from src.queries import (
    get_available_competencies,
    get_cep_data,
    get_churn_reasons,
    get_commercial_pace,
    get_executive_kpis,
    get_funnel_summary,
    get_monthly_evolution,
    get_strategic_scenarios_table,
    get_units_breakeven_analysis,
    get_units_list,
    simulate_parametric_scenario,
)


def fmt_brl(val: float | int | None) -> str:
    """Formata valor monetário no padrão brasileiro: R$ 185.107,86 ou -R$ 75.789,79"""
    if val is None or pd.isna(val):
        return "R$ 0,00"
    is_neg = val < 0
    formatted = f"{abs(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-R$ {formatted}" if is_neg else f"R$ {formatted}"


def fmt_delta_brl(val: float | int | None) -> str:
    """Formata variação monetária com sinal no padrão brasileiro: +R$ 7.821,86 ou -R$ 4.251,69"""
    if val is None or pd.isna(val):
        return "R$ 0,00"
    sign = "+" if val > 0 else ("-" if val < 0 else "")
    formatted = f"{abs(val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sign}R$ {formatted}"


def fmt_num_br(val: float | int | None, decimals: int = 0) -> str:
    """Formata números no padrão brasileiro com ponto de milhar: 3.501 ou 18,5"""
    if val is None or pd.isna(val):
        return "0"
    is_neg = val < 0
    abs_val = abs(val)
    if decimals == 0:
        formatted = f"{int(round(abs_val)):,}".replace(",", ".")
    else:
        fmt = f"{{val:,.{decimals}f}}"
        formatted = fmt.format(val=abs_val).replace(",", "X").replace(".", ",").replace("X", ".")
    sign = "-" if is_neg else ""
    return f"{sign}{formatted}"


def fmt_pct_br(val: float | int | None, decimals: int = 2, show_sign: bool = False) -> str:
    """Formata percentuais no padrão brasileiro: 1,80% ou +2,0%"""
    if val is None or pd.isna(val):
        return "0,0%"
    sign = "+" if (show_sign and val > 0) else ("-" if val < 0 else "")
    formatted = f"{abs(val):.{decimals}f}".replace(".", ",")
    return f"{sign}{formatted}%"


# Configuração da página Streamlit
st.set_page_config(
    page_title="Integra-Dignidade | Planejamento & Performance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS Corporativa Premium
st.markdown(
    """
<style>
    /* Estilo geral e tipografia */
    .main { background-color: #f8fafc; }
    h1, h2, h3 { font-family: 'Inter', -apple-system, sans-serif; color: #0f172a; font-weight: 700; }
    
    /* Card de métricas customizado */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0f172a;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 4px;
    }
    .metric-sub-negative {
        font-size: 0.8rem;
        color: #ef4444;
        font-weight: 600;
        margin-top: 4px;
    }
    
    /* Banner de cabeçalho */
    .header-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 22px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        border-left: 5px solid #3b82f6;
    }
    .header-banner h2 { color: #ffffff; margin: 0 0 6px 0; font-size: 1.6rem; }
    .header-banner p { color: #94a3b8; margin: 0; font-size: 0.95rem; }
    
    /* Badge de status */
    .badge-status {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        background-color: #dbeafe;
        color: #1e40af;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Barra Lateral: Filtros Globais e Governança
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=300&auto=format&fit=crop&q=60",
        use_container_width=True,
    )
    st.markdown("### 🏛️ Grupo Dignidade")
    st.markdown("**Plataforma Integra-Dignidade**")
    st.caption("Planejamento Estratégico, Simulação & CEP")
    st.divider()

    competencias = get_available_competencies()
    comp_selecionada = st.selectbox(
        "📅 Competência de Referência:",
        options=competencias,
        index=0 if competencias else 0,
        help="Seleciona a competência contábil e operacional (ano_mes).",
    )

    unidades_raw = get_units_list()
    opcoes_unidades = {"TODAS": "Todas as Unidades (Consolidado)"}
    for u in unidades_raw:
        opcoes_unidades[u["id_unidade"]] = f"{u['nome_cidade']} ({u['tipo_unidade']})"

    unidade_selecionada = st.selectbox(
        "📍 Unidade Operacional:",
        options=list(opcoes_unidades.keys()),
        format_func=lambda x: opcoes_unidades[x],
        help="Filtra a visualização para uma filial física ou central.",
    )

    st.divider()
    st.markdown("#### 🛡️ Governança de Dados")
    st.markdown(
        """
    * **Motor Analítico:** DuckDB Colunar
    * **Contratos:** 100% Validados
    * **Metodologia:** SDD & CEP 3-sigma
    * **Versão:** v0.1.0-executivo
    """
    )
    st.caption("Apoio à Decisão da Diretoria Executiva")

# Banner Principal
st.markdown(
    """
<div class="header-banner">
    <h2>Sistema Integrado de Gestão Estratégica e Performance</h2>
    <p>Conectando os rituais de governança da diretoria à realidade operacional da ponta | Grupo Dignidade</p>
</div>
""",
    unsafe_allow_html=True,
)

# Abas de Navegação Estratégica
tab_bsc, tab_sim, tab_cep, tab_crm = st.tabs(
    [
        "📊 1. Visão Executiva & Metas (BSC)",
        "🎯 2. Simulador Paramétrico de Cenários",
        "⚙️ 3. Eficiência Operacional & CEP (BPM)",
        "📈 4. Pipeline Comercial & Lojas",
    ]
)

# -----------------------------------------------------------------------------
# ABA 1: VISÃO EXECUTIVA & BALANCED SCORECARD (BSC)
# -----------------------------------------------------------------------------
with tab_bsc:
    st.markdown("### Painel de Acompanhamento de Metas Corporativas")
    st.caption(
        f"Competência: **{comp_selecionada}** | Filtro: **{opcoes_unidades[unidade_selecionada]}**"
    )

    kpis = get_executive_kpis(comp_selecionada, unidade_selecionada)

    # Fileira de Métricas Executivas
    c1, c2, c3, c4, c5 = st.columns(5)

    delta_mrr = kpis["mrr"] - kpis["meta_mrr"]
    c1.metric(
        label="MRR (Receita Recorrente)",
        value=fmt_brl(kpis["mrr"]),
        delta=f"{fmt_delta_brl(delta_mrr)} vs Meta" if unidade_selecionada == "TODAS" else None,
    )

    delta_churn = round(kpis["meta_churn"] - kpis["churn_rate"], 2)
    c2.metric(
        label="Taxa de Churn Mensal",
        value=fmt_pct_br(kpis["churn_rate"]),
        delta=f"{fmt_pct_br(delta_churn, show_sign=True)} vs Meta (1,8%)",
        delta_color="normal",
    )

    delta_inad = round(kpis["meta_inadimplencia"] - kpis["taxa_inadimplencia"], 2)
    c3.metric(
        label="Inadimplência (> 30d)",
        value=fmt_pct_br(kpis["taxa_inadimplencia"]),
        delta=f"{fmt_pct_br(delta_inad, show_sign=True)} vs Meta (4,5%)",
        delta_color="normal",
    )

    c4.metric(
        label="Ticket Médio da Carteira",
        value=fmt_brl(kpis["ticket_medio"]),
        delta=f"{fmt_delta_brl(kpis['ticket_medio'] - kpis['meta_ticket_medio'])} vs Meta",
    )

    c5.metric(
        label="LTV da Carteira",
        value=fmt_brl(kpis["ltv"]),
        delta="Vida Útil Estimada",
        delta_color="off",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos da Visão Executiva
    col_chart_left, col_chart_right = st.columns([6, 4])

    with col_chart_left:
        st.markdown("##### 📈 Evolução Histórica de MRR e Base de Contratos Ativos")
        df_evolucao = get_monthly_evolution()
        if not df_evolucao.empty:
            fig_evol = go.Figure()
            fig_evol.add_trace(
                go.Bar(
                    x=df_evolucao["ano_mes"],
                    y=df_evolucao["mrr"],
                    name="MRR (R$)",
                    marker_color="#2563eb",
                    opacity=0.85,
                )
            )
            fig_evol.add_trace(
                go.Scatter(
                    x=df_evolucao["ano_mes"],
                    y=df_evolucao["contratos_ativos"],
                    name="Contratos Ativos",
                    yaxis="y2",
                    mode="lines+markers",
                    line=dict(color="#10b981", width=3),
                    marker=dict(size=6),
                )
            )
            fig_evol.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
                yaxis=dict(title="MRR (R$)", showgrid=True, gridcolor="#f1f5f9"),
                yaxis2=dict(
                    title="Contratos Ativos",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                ),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
            )
            st.plotly_chart(fig_evol, use_container_width=True)

    with col_chart_right:
        st.markdown("##### 🔍 Motivos de Cancelamento na Ponta (Voz do Cliente)")
        df_churn = get_churn_reasons(comp_selecionada, unidade_selecionada)
        if not df_churn.empty:
            fig_pie = px.bar(
                df_churn,
                x="total_cancelamentos",
                y="motivo_cancelamento",
                orientation="h",
                text="percentual",
                color="motivo_cancelamento",
                color_discrete_sequence=["#ef4444", "#f97316", "#3b82f6", "#64748b"],
            )
            fig_pie.update_traces(texttemplate="%{text}%", textposition="outside")
            fig_pie.update_layout(
                height=360,
                showlegend=False,
                margin=dict(l=20, r=40, t=30, b=20),
                xaxis=dict(
                    title="Volume de Cancelamentos", showgrid=True, gridcolor="#f1f5f9"
                ),
                yaxis=dict(title="", autorange="reversed"),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Nenhum cancelamento registrado para os filtros selecionados.")

    # Alerta Estratégico com a filosofia da liderança
    st.info(
        """
    💡 **Diretriz de Governança Estratégica:** *"O indicador apenas sinaliza que algo vai mal; quem está na ponta operacional explica o porquê."*
    Os motivos de cancelamento acima subsidiam os ritos quinzenais de revisão de processos com os gerentes de loja para correção de rotas comerciais.
    """
    )

# -----------------------------------------------------------------------------
# ABA 2: SIMULADOR PARAMÉTRICO DE CENÁRIOS & EXPANSÃO
# -----------------------------------------------------------------------------
with tab_sim:
    st.markdown("### Modelo de Simulação de Sensibilidade Paramétrica")
    st.markdown(
        """
    Subsidia a tomada de decisão sob incerteza da diretoria executiva, testando elasticidades de preço,
    impacto na taxa de cancelamento e custos de sinistro antes de qualquer repactuação de mercado.
    """
    )

    col_sim_controls, col_sim_results = st.columns([4, 6])

    with col_sim_controls:
        st.markdown("#### 🎛️ Variáveis de Decisão")

        var_preco = st.slider(
            "Reajuste Médio de Preço na Mensalidade (%):",
            min_value=-10.0,
            max_value=20.0,
            value=5.0,
            step=1.0,
            help="Simula aumento ou redução percentual no valor de face dos contratos ativos.",
        )

        elasticidade_churn = st.slider(
            "Elasticidade Estimada de Churn (% perda por +5% preço):",
            min_value=0.2,
            max_value=2.0,
            value=0.8,
            step=0.1,
            help="Premissa padrão: cada +5% de preço gera +0,8% de churn estrutural na carteira.",
        )

        var_sinistros = st.slider(
            "Flutuação de Sinistralidade Funerária (%):",
            min_value=-15.0,
            max_value=30.0,
            value=0.0,
            step=5.0,
            help="Simula oscilação na demanda de atendimentos funerários 24h.",
        )

        st.caption("Base de simulação: Competência 2026-09 | Parâmetros instantâneos.")

    sim_res = simulate_parametric_scenario(
        var_preco, elasticidade_churn, var_sinistros, unidade_selecionada
    )

    with col_sim_results:
        st.markdown("#### 📊 Resultado Financeiro Projetado")

        r1, r2 = st.columns(2)
        r1.metric(
            "MRR Projetado",
            fmt_brl(sim_res["mrr_projetado"]),
            delta=f"{fmt_delta_brl(sim_res['delta_mrr'])} ({fmt_pct_br(var_preco, decimals=1, show_sign=True)})",
        )
        r2.metric(
            "Carteira Ativa Projetada",
            f"{fmt_num_br(sim_res['ativos_projetados'])} contratos",
            delta=f"{fmt_num_br(sim_res['ativos_projetados'] - sim_res['base_ativos'])} associados",
            delta_color="normal",
        )

        r3, r4 = st.columns(2)
        r3.metric(
            "Custo Projetado de Sinistros",
            fmt_brl(sim_res["custo_sinistros_projetado"]),
            delta=fmt_delta_brl(sim_res["custo_sinistros_projetado"] - sim_res["base_custo_sinistros"]),
            delta_color="normal",
        )
        r4.metric(
            "Margem Operacional Projetada",
            fmt_brl(sim_res["margem_projetada"]),
            delta=f"{fmt_delta_brl(sim_res['delta_margem'])} ({fmt_pct_br(sim_res['delta_margem_pct'], decimals=1, show_sign=True)})",
            delta_color="normal",
        )

        # Gráfico de comparação antes vs projetado
        fig_sim_bar = go.Figure(
            data=[
                go.Bar(
                    name="Cenário Base (Atual)",
                    x=["MRR", "Custos Sinistros", "Margem Operacional"],
                    y=[
                        sim_res["base_mrr"],
                        sim_res["base_custo_sinistros"],
                        sim_res["margem_base"],
                    ],
                    marker_color="#94a3b8",
                ),
                go.Bar(
                    name="Cenário Simulado",
                    x=["MRR", "Custos Sinistros", "Margem Operacional"],
                    y=[
                        sim_res["mrr_projetado"],
                        sim_res["custo_sinistros_projetado"],
                        sim_res["margem_projetada"],
                    ],
                    marker_color="#2563eb",
                ),
            ]
        )
        fig_sim_bar.update_layout(
            barmode="group",
            height=260,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_sim_bar, use_container_width=True)

    st.divider()

    # Matriz Executiva dos 3 Cenários Estratégicos Pré-Configurados (Caso de Uso 02)
    st.markdown(
        "#### 📋 Matriz Executiva dos 3 Cenários Estratégicos (Caso de Uso 02 da Spec 03)"
    )
    st.caption(
        "Visão comparativa de sensibilidade (Estresse vs. Base vs. Otimista) para apoio à decisão da diretoria."
    )
    df_scenarios = get_strategic_scenarios_table(unidade_selecionada)
    st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

    st.divider()

    # Seção de Ponto de Equilíbrio (Breakeven) por Loja Física
    st.markdown("#### 🏢 Análise de Ponto de Equilíbrio (Breakeven) por Loja Física")
    st.caption(
        "Mede a disciplina na alocação de capital (Capex de implantação controlado e Opex mensal sustentável)."
    )

    df_breakeven = get_units_breakeven_analysis()
    df_breakeven_display = df_breakeven.copy()
    df_breakeven_display["capex_implantacao"] = df_breakeven_display["capex_implantacao"].apply(fmt_brl)
    df_breakeven_display["opex_mensal_base"] = df_breakeven_display["opex_mensal_base"].apply(fmt_brl)
    df_breakeven_display["contratos_ativos"] = df_breakeven_display["contratos_ativos"].apply(lambda x: f"{fmt_num_br(x)} contratos")
    df_breakeven_display["contratos_breakeven"] = df_breakeven_display["contratos_breakeven"].apply(lambda x: f"{fmt_num_br(x)} contratos")
    df_breakeven_display["saldo_acima_breakeven"] = df_breakeven_display["saldo_acima_breakeven"].apply(lambda x: f"{fmt_num_br(x)} contratos")

    st.dataframe(
        df_breakeven_display[
            [
                "id_unidade",
                "nome_cidade",
                "tipo_unidade",
                "capex_implantacao",
                "opex_mensal_base",
                "contratos_ativos",
                "contratos_breakeven",
                "saldo_acima_breakeven",
                "status_financeiro",
            ]
        ].rename(
            columns={
                "id_unidade": "ID",
                "nome_cidade": "Cidade",
                "tipo_unidade": "Perfil",
                "capex_implantacao": "Capex Implantação",
                "opex_mensal_base": "Opex Mensal",
                "contratos_ativos": "Contratos Ativos",
                "contratos_breakeven": "Breakeven (Meta)",
                "saldo_acima_breakeven": "Saldo Líquido",
                "status_financeiro": "Situação Operacional",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

# -----------------------------------------------------------------------------
# ABA 3: EFICIÊNCIA OPERACIONAL & CEP (A PONTE DE BPM)
# -----------------------------------------------------------------------------
with tab_cep:
    st.markdown("### Controle Estatístico de Processo (CEP) - Atendimento 24h")
    st.markdown(
        """
    **A conexão entre Engenharia de Dados e BPM:** Monitoramento contínuo da variabilidade do tempo de ciclo 
    (lead time) nos atendimentos funerários 24h. Aplicação dos limites estatísticos de três desvios padrão (3-sigma) 
    para isolar causas comuns de estabilidade das **causas especiais** que exigem intervenção de processo.
    """
    )

    cep_info = get_cep_data(unidade_selecionada)
    df_cep = cep_info["df"]

    # Métricas do Processo
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Lead Time Médio", f"{fmt_num_br(cep_info['media_horas'], decimals=1)} horas")
    m2.metric("Limite Superior (LSC 3σ)", f"{fmt_num_br(cep_info['lsc_horas'], decimals=1)} horas")
    m3.metric(
        "Estabilidade do Processo",
        f"{fmt_pct_br(cep_info['taxa_estabilidade_pct'], decimals=1)} em conformidade",
    )
    m4.metric(
        "Desvios de Causa Especial",
        f"{fmt_num_br(cep_info['total_anomalias'])} ocorrências",
        delta="Gargalos Operacionais",
        delta_color="inverse",
    )

    if not df_cep.empty:
        # Gráfico Carta de Controle Shewhart
        fig_cep = go.Figure()

        # Atendimentos normais
        normais = df_cep[df_cep["status_cep"] == "Causa Comum (Estável)"]
        fig_cep.add_trace(
            go.Scatter(
                x=normais["timestamp_acionamento"],
                y=normais["tempo_ciclo_horas"],
                mode="markers",
                name="Atendimento Estável (Causa Comum)",
                marker=dict(color="#3b82f6", size=7, opacity=0.7),
            )
        )

        # Atendimentos anômalos (Causas especiais)
        anomalos = df_cep[df_cep["status_cep"] != "Causa Comum (Estável)"]
        fig_cep.add_trace(
            go.Scatter(
                x=anomalos["timestamp_acionamento"],
                y=anomalos["tempo_ciclo_horas"],
                mode="markers",
                name="Anomalia (Causa Especial > 3σ)",
                marker=dict(color="#ef4444", size=11, symbol="diamond"),
            )
        )

        # Linha Média
        fig_cep.add_hline(
            y=cep_info["media_horas"],
            line_dash="dash",
            line_color="#10b981",
            annotation_text=f"Média: {fmt_num_br(cep_info['media_horas'], decimals=1)}h",
            annotation_position="bottom right",
        )

        # Linha LSC
        fig_cep.add_hline(
            y=cep_info["lsc_horas"],
            line_dash="dot",
            line_color="#ef4444",
            annotation_text=f"LSC (+3σ): {fmt_num_br(cep_info['lsc_horas'], decimals=1)}h",
            annotation_position="top right",
        )

        fig_cep.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis=dict(
                title="Lead Time Operacional (Horas)",
                showgrid=True,
                gridcolor="#f1f5f9",
            ),
            xaxis=dict(
                title="Momento do Acionamento 24h", showgrid=True, gridcolor="#f1f5f9"
            ),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_cep, use_container_width=True)

        # Rito dos 5 Porquês / Bizagi
        st.markdown(
            "#### 🔬 Protocolo de Investigação de Causa-Raiz (Rito dos 5 Porquês com a Ponta)"
        )
        st.caption(
            "Casos identificados fora do Limite Superior de Controle para discussão nos fóruns operacionais:"
        )

        anomalos_display = anomalos.copy()
        anomalos_display["custo_direto_servico"] = anomalos_display["custo_direto_servico"].apply(fmt_brl)
        anomalos_display["tempo_ciclo_horas"] = anomalos_display["tempo_ciclo_horas"].apply(lambda x: f"{fmt_num_br(x, decimals=1)}h")

        st.dataframe(
            anomalos_display[
                [
                    "id_atendimento",
                    "id_contrato",
                    "nome_cidade",
                    "timestamp_acionamento",
                    "tempo_ciclo_horas",
                    "custo_direto_servico",
                    "status_cep",
                ]
            ].rename(
                columns={
                    "id_atendimento": "Ordem de Serviço",
                    "id_contrato": "Contrato",
                    "nome_cidade": "Cidade",
                    "timestamp_acionamento": "Data/Hora Chamado",
                    "tempo_ciclo_horas": "Tempo de Ciclo (h)",
                    "custo_direto_servico": "Custo Direto",
                    "status_cep": "Classificação Estatística",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        with st.expander(
            "🔍 Protocolo Detalhado dos 5 Porquês por Causa-Raiz (Diagnóstico com a Ponta)",
            expanded=True,
        ):
            col_pq1, col_pq2, col_pq3 = st.columns(3)
            with col_pq1:
                st.markdown("##### 🏛️ Gargalo em Plantão de Cartório")
                st.markdown(
                    """
                * **1. Por que atrasou?** O funeral iniciou 12h após o acionamento inicial.
                * **2. Por que demorou?** Certidão de óbito reteve o processo de sepultamento.
                * **3. Por que reteve?** Cartório de plantão no fim de semana estava sobrecarregado.
                * **4. Por que sobrecarregado?** Documentos foram levados fisicamente em papel.
                * **5. Causa-Raiz (BPM):** Ausência de protocolo digital com os cartórios polo.
                * **Ação Corretiva:** Mapear no Bizagi o fluxo de declaração digital e celebrar convênio.
                """
                )
            with col_pq2:
                st.markdown("##### 🏥 Liberação Pericial no IML")
                st.markdown(
                    """
                * **1. Por que atrasou?** Lead time superou 32h no atendimento.
                * **2. Por que demorou?** Corpo aguardou emissão de laudo pericial.
                * **3. Por que aguardou?** Guia de encaminhamento estava sem carimbo legível.
                * **4. Por que sem carimbo?** Família não recebeu orientação no hospital.
                * **5. Causa-Raiz (BPM):** Triagem da central 24h não exigiu checklist prévio.
                * **Ação Corretiva:** Padronizar checklist obrigatório no script do atendente 24h.
                """
                )
            with col_pq3:
                st.markdown("##### 🚐 Indisponibilidade de Frota de Apoio")
                st.markdown(
                    """
                * **1. Por que atrasou?** Fila de espera para remoção intermunicipal.
                * **2. Por que demorou?** Veículo de traslado quebrou na rodovia estadual.
                * **3. Por que quebrou?** Revisão mecânica preventiva estava vencida.
                * **4. Por que estava vencida?** Não havia alerta automático de quilometragem.
                * **5. Causa-Raiz (BPM):** Controle de manutenção em planilha sem SLA.
                * **Ação Corretiva:** Automatizar gatilho de manutenção preventiva na frota.
                """
                )

        st.info(
            """
        📌 **Ação Prática de BPM:** Não se altera um processo por causa de variações comuns. Porém, os registros acima 
        representam **causas especiais de variabilidade** (ex.: demora na liberação de certidão em plantão de cartório, 
        fila de liberação em IML regional ou quebra mecânica de viatura de traslado). Estes pontos alimentam os 
        checkpoints semanais de remoção de gargalos operacionais.
        """
        )

# -----------------------------------------------------------------------------
# ABA 4: PIPELINE COMERCIAL & FUNIL DE LOJAS (CRM)
# -----------------------------------------------------------------------------
with tab_crm:
    st.markdown("### Visibilidade do Ritmo de Captação e Pipeline Comercial")
    st.markdown(
        """
    **Controle Operacional Ágil:** Acompanhamento do funil de oportunidades nas lojas físicas 
    para identificar gargalos de conversão e dias de estagnação (*aging*) por etapa.
    """
    )

    df_funnel = get_funnel_summary(unidade_selecionada)
    pace = get_commercial_pace(unidade_selecionada)

    # Indicadores de Ritmo Operacional de Vendas ("Bater Bumbo")
    st.markdown("#### 🥁 Ritmo Operacional de Captação ('Bater Bumbo na Operação')")
    st.caption(
        "Inputs diários e cadência de conversão necessários para cobrir os custos operacionais (Opex) da loja."
    )

    p1, p2, p3, p4 = st.columns(4)
    p1.metric(
        "Leads Fechados",
        f"{fmt_num_br(pace['leads_fechados'])} vendas",
        delta=f"{fmt_pct_br(pace['taxa_conversao_geral'], decimals=1)} conversão geral",
    )
    p2.metric(
        "Meta Semanal de Vendas",
        f"{fmt_num_br(pace['meta_semanal_vendas'])} contratos/sem",
        help="Volume de novos associados por semana necessário para cobrir o Opex da filial.",
    )
    p3.metric(
        "Ritmo Atual Observado",
        f"{fmt_num_br(pace['ritmo_semanal_atual'], decimals=1)} contratos/sem",
    )
    p4.metric(
        "Atingimento da Cadência",
        f"{fmt_pct_br(pace['atingimento_ritmo_pct'], decimals=1)}",
        delta=pace["status_ritmo"],
        delta_color="normal" if pace["atingimento_ritmo_pct"] >= 90.0 else "inverse",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    fcol_left, fcol_right = st.columns([6, 4])

    with fcol_left:
        st.markdown("##### 🧭 Funil de Conversão Comercial")
        if not df_funnel.empty:
            fig_fun = go.Figure(
                go.Funnel(
                    y=df_funnel["etapa_funil"],
                    x=df_funnel["total_leads"],
                    textinfo="value+percent initial",
                    marker=dict(
                        color=[
                            "#3b82f6",
                            "#60a5fa",
                            "#93c5fd",
                            "#f59e0b",
                            "#10b981",
                            "#ef4444",
                        ]
                    ),
                )
            )
            fig_fun.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
            )
            st.plotly_chart(fig_fun, use_container_width=True)

    with fcol_right:
        st.markdown("##### ⏳ Tempo Médio de Estagnação (Dias no Estágio)")
        if not df_funnel.empty:
            fig_aging = px.bar(
                df_funnel,
                x="etapa_funil",
                y="media_dias_estagio",
                color="media_dias_estagio",
                color_continuous_scale="Reds",
                text="media_dias_estagio",
            )
            fig_aging.update_traces(texttemplate="%{text} dias", textposition="outside")
            fig_aging.update_layout(
                height=380,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(title="Etapa do Funil"),
                yaxis=dict(
                    title="Média de Dias Parado", showgrid=True, gridcolor="#f1f5f9"
                ),
                coloraxis_showscale=False,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
            )
            st.plotly_chart(fig_aging, use_container_width=True)

    st.markdown("---")
    st.caption("Grupo Dignidade | Diretoria de Planejamento, Performance e Integração")
