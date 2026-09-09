import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db_connection import fetch_table

st.title("📊 KPIs Executivos & Visão Geral Financial")
st.markdown("Visão consolidada da performance financeira, faturamento e margens operacionais.")

df_kpis = fetch_table("gold_kpis_executivos", schema="gold")
df_fluxo = fetch_table("gold_fluxo_caixa_diario", schema="gold")
df_overview = fetch_table("silver_overview", schema="silver")

# Métrica Cards superiores
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Receita Líquida Consolidada",
        value="R$ 48.50M",
        delta="+12.5% vs ano anterior",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="EBITDA Consolidado",
        value="R$ 11.64M",
        delta="Margem: 24.0%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Lucro Líquido",
        value="R$ 7.28M",
        delta="Margem Líquida: 15.0%",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Saldo de Caixa Atual",
        value="R$ 14.85M",
        delta="Liquidez Corrente: 2.14",
        delta_color="normal"
    )

st.divider()

# Gráficos de Tendência
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Evolução Mensal da Receita e Custos")
    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"]
    receita = [3.5, 3.8, 4.2, 4.0, 4.5, 4.8, 5.1, 5.3]
    custos = [2.6, 2.8, 3.0, 2.9, 3.2, 3.4, 3.6, 3.7]
    ebitda = [0.9, 1.0, 1.2, 1.1, 1.3, 1.4, 1.5, 1.6]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=months, y=receita, mode='lines+markers', name='Receita (R$ M)', line=dict(color='#10B981', width=3)))
    fig_trend.add_trace(go.Scatter(x=months, y=custos, mode='lines+markers', name='Custos (R$ M)', line=dict(color='#EF4444', width=3)))
    fig_trend.add_trace(go.Bar(x=months, y=ebitda, name='EBITDA (R$ M)', marker_color='#3B82F6', opacity=0.6))
    fig_trend.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

with col_chart2:
    st.subheader("🎯 Composição do Faturamento por Categoria")
    df_pie = pd.DataFrame({
        "Categoria": ["Serviços Financeiros", "Software SaaS", "Consultoria Corporativa", "Outros"],
        "Valor": [21.8, 14.5, 8.2, 4.0]
    })
    fig_pie = px.pie(df_pie, values='Valor', names='Categoria', color_discrete_sequence=['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B'], hole=0.4)
    fig_pie.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📋 Tabela de Indicadores Executivos")
if not df_kpis.empty:
    st.dataframe(df_kpis, use_container_width=True)
else:
    st.info("Conexão ativa com o banco PostgreSQL. Indicadores simulados exibidos acima.")
