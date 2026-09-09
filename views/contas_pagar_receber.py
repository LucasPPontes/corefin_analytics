import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db_connection import fetch_table

st.title("💳 Contas a Pagar & Contas a Receber")
st.markdown("Gestão de compromissos financeiros, carteira de clientes e pagamentos a fornecedores.")

df_pagar = fetch_table("silver_contas_pagar", schema="silver")
df_receber = fetch_table("silver_contas_receber", schema="silver")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Contas a Receber Total", "R$ 12.45M", "Carteira Ativa")
with c2:
    st.metric("Contas a Receber Vencidas", "R$ 305K", "2.45% Inadimplência", delta_color="inverse")
with c3:
    st.metric("Contas a Pagar Total", "R$ 8.90M", "Fornecedores & OPEX")
with c4:
    st.metric("DSO (Dias Médios de Recebimento)", "42 Dias", "-3 dias vs meta", delta_color="normal")

st.divider()

col_cp, col_cr = st.columns(2)

with col_cp:
    st.subheader("🔴 Status de Contas a Pagar")
    df_status_cp = pd.DataFrame({
        "Status": ["Pago", "A Vencer", "Vencido"],
        "Valor (R$ M)": [5.6, 2.8, 0.5]
    })
    fig_cp = px.bar(df_status_cp, x="Status", y="Valor (R$ M)", color="Status",
                    color_discrete_map={"Pago": "#10B981", "A Vencer": "#3B82F6", "Vencido": "#EF4444"})
    fig_cp.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig_cp, use_container_width=True)

with col_cr:
    st.subheader("🟢 Status de Contas a Receber")
    df_status_cr = pd.DataFrame({
        "Status": ["Recebido", "A Vencer", "Vencido"],
        "Valor (R$ M)": [8.2, 3.95, 0.305]
    })
    fig_cr = px.bar(df_status_cr, x="Status", y="Valor (R$ M)", color="Status",
                    color_discrete_map={"Recebido": "#10B981", "A Vencer": "#3B82F6", "Vencido": "#EF4444"})
    fig_cr.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig_cr, use_container_width=True)

st.subheader("📋 Amostra de Títulos em Aberto")
tab1, tab2 = st.tabs(["Contas a Receber", "Contas a Pagar"])

with tab1:
    if not df_receber.empty:
        st.dataframe(df_receber, use_container_width=True)
    else:
        sample_cr = pd.DataFrame([
            {"Cliente": "Alpha Corp", "Valor (R$)": 450000.0, "Vencimento": "2026-09-15", "Status": "A Vencer"},
            {"Cliente": "Beta Logística", "Valor (R$)": 120000.0, "Vencimento": "2026-08-30", "Status": "Vencido"},
            {"Cliente": "Gamma Tech", "Valor (R$)": 890000.0, "Vencimento": "2026-09-20", "Status": "A Vencer"},
        ])
        st.dataframe(sample_cr, use_container_width=True)

with tab2:
    if not df_pagar.empty:
        st.dataframe(df_pagar, use_container_width=True)
    else:
        sample_cp = pd.DataFrame([
            {"Fornecedor": "AWS Cloud Services", "Valor (R$)": 85000.0, "Vencimento": "2026-09-10", "Status": "A Vencer"},
            {"Fornecedor": "Dell Technologies", "Valor (R$)": 240000.0, "Vencimento": "2026-09-05", "Status": "Pago"},
            {"Fornecedor": "Oracle Software", "Valor (R$)": 150000.0, "Vencimento": "2026-08-25", "Status": "Vencido"},
        ])
        st.dataframe(sample_cp, use_container_width=True)
