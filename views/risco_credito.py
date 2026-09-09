import streamlit as st
import plotly.express as px
import pandas as pd
from utils.db_connection import fetch_table

st.title("⚠️ Matriz de Risco de Crédito & Aging List")
st.markdown("Monitoramento de exposição financeira por faixa de atraso e régua de cobrança dos clientes críticos.")

df_aging = fetch_table("gold_matriz_risco_aging", schema="gold")
df_clientes = fetch_table("gold_clientes_criticos", schema="gold")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Exposição Total de Risco", "R$ 4.25M", "Carteira Monitorada")
with c2:
    st.metric("Clientes Críticos em Régua", "4 Empresas", "Rating Baixo (CCC/D)")
with c3:
    st.metric("Inadimplência > 60 Dias", "R$ 180K", "Provisão PDD Ativa", delta_color="inverse")

st.divider()

col_ag, col_rating = st.columns(2)

with col_ag:
    st.subheader("⏳ Aging List (Distribuição por Faixa de Atraso)")
    df_aging_sample = pd.DataFrame({
        "Faixa Atraso": ["Adimplente", "1 a 30 dias", "31 a 60 dias", "61 a 90 dias", "> 90 dias"],
        "Valor Exposto (R$ M)": [8.2, 0.85, 0.42, 0.18, 0.08]
    })
    fig_aging = px.bar(df_aging_sample, x="Faixa Atraso", y="Valor Exposto (R$ M)",
                       color="Faixa Atraso",
                       color_discrete_sequence=['#10B981', '#F59E0B', '#F97316', '#EF4444', '#991B1B'])
    fig_aging.update_layout(template="plotly_dark", height=380)
    st.plotly_chart(fig_aging, use_container_width=True)

with col_rating:
    st.subheader("🛡️ Rating de Risco da Carteira")
    df_rating_sample = pd.DataFrame({
        "Rating": ["AAA (Excelente)", "AA (Baixo Risco)", "BBB (Médio Risco)", "CCC/D (Crítico)"],
        "Percentual": [55.0, 30.0, 10.0, 5.0]
    })
    fig_rating = px.pie(df_rating_sample, values="Percentual", names="Rating",
                        color_discrete_sequence=['#10B981', '#3B82F6', '#F59E0B', '#EF4444'], hole=0.3)
    fig_rating.update_layout(template="plotly_dark", height=380)
    st.plotly_chart(fig_rating, use_container_width=True)

st.subheader("🚨 Clientes Críticos sob Acompanhamento da Diretoria")
if not df_clientes.empty:
    st.dataframe(df_clientes, use_container_width=True)
else:
    sample_cc = pd.DataFrame([
        {"Cliente": "Alpha Corp", "Rating": "AAA", "Limite Concedido (R$)": 5000000.0, "Utilizado (R$)": 3200000.0, "Em Atraso (R$)": 150000.0, "Dias Atraso": 15, "Status Cobrança": "Em Negociação"},
        {"Cliente": "Delta Comércio", "Rating": "CCC", "Limite Concedido (R$)": 1500000.0, "Utilizado (R$)": 1400000.0, "Em Atraso (R$)": 320000.0, "Dias Atraso": 45, "Status Cobrança": "Notificação Extrajudicial"},
        {"Cliente": "Omega Serviços", "Rating": "D", "Limite Concedido (R$)": 800000.0, "Utilizado (R$)": 780000.0, "Em Atraso (R$)": 180000.0, "Dias Atraso": 78, "Status Cobrança": "Cobrança Jurídica"},
    ])
    st.dataframe(sample_cc, use_container_width=True)
