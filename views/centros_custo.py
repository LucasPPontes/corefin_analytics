import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db_connection import fetch_table

st.title("🎯 Controladoria & FP&A: Orçado vs Realizado")
st.markdown("Análise de variância orçamentária e acompanhamento de custos por centro de custo corporativo.")

df_custos = fetch_table("silver_centros_custo", schema="silver")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Orçamento Total", "R$ 18.50M", "Meta Anual FP&A")
with c2:
    st.metric("Realizado Total", "R$ 18.36M", "Executado")
with c3:
    st.metric("Variação Orçamentária", "R$ -140K", "-0.76% (Economia)", delta_color="normal")
with c4:
    st.metric("Status Global", "Dentro do Orçamento", "Conformidade 99.2%")

st.divider()

st.subheader("📊 Comparativo Orçado vs Realizado por Centro de Custo")

cost_centers = ["Tecnologia & TI", "Marketing & Growth", "Vendas & Comercial", "Recursos Humanos", "Operações & Logística", "Jurídico & Compliance"]
orcado_vals = [4.5, 3.2, 5.0, 1.8, 3.0, 1.0]
realizado_vals = [4.7, 3.1, 4.8, 1.85, 2.9, 1.01]

fig_cost = go.Figure()
fig_cost.add_trace(go.Bar(x=cost_centers, y=orcado_vals, name="Orçado (R$ M)", marker_color="#3B82F6"))
fig_cost.add_trace(go.Bar(x=cost_centers, y=realizado_vals, name="Realizado (R$ M)", marker_color="#10B981"))
fig_cost.update_layout(barmode="group", template="plotly_dark", height=400, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_cost, use_container_width=True)

st.subheader("📋 Tabela de Variância Orçamentária")
if not df_custos.empty:
    st.dataframe(df_custos, use_container_width=True)
else:
    sample_cc_table = pd.DataFrame([
        {"Centro de Custo": "Tecnologia & TI", "Orçado (R$)": 4500000.0, "Realizado (R$)": 4700000.0, "Desvio (R$)": 200000.0, "% Execução": "104.4%", "Status": "Atenção (Estouro)"},
        {"Centro de Custo": "Marketing & Growth", "Orçado (R$)": 3200000.0, "Realizado (R$)": 3100000.0, "Desvio (R$)": -100000.0, "% Execução": "96.8%", "Status": "Dentro do Orçamento"},
        {"Centro de Custo": "Vendas & Comercial", "Orçado (R$)": 5000000.0, "Realizado (R$)": 4800000.0, "Desvio (R$)": -200000.0, "% Execução": "96.0%", "Status": "Dentro do Orçamento"},
        {"Centro de Custo": "Recursos Humanos", "Orçado (R$)": 1800000.0, "Realizado (R$)": 1850000.0, "Desvio (R$)": 50000.0, "% Execução": "102.7%", "Status": "Atenção (Estouro)"},
        {"Centro de Custo": "Operações & Logística", "Orçado (R$)": 3000000.0, "Realizado (R$)": 2900000.0, "Desvio (R$)": -100000.0, "% Execução": "96.6%", "Status": "Dentro do Orçamento"},
        {"Centro de Custo": "Jurídico & Compliance", "Orçado (R$)": 1000000.0, "Realizado (R$)": 1010000.0, "Desvio (R$)": 10000.0, "% Execução": "101.0%", "Status": "Dentro do Orçamento"},
    ])
    st.dataframe(sample_cc_table, use_container_width=True)
