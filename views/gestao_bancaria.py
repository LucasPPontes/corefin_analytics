import streamlit as st
import plotly.express as px
import pandas as pd
from utils.db_connection import fetch_table

st.title("🏦 Gestão Bancária & Posição Financeira")
st.markdown("Consolidação de saldos mantidos em instituições financeiras e linhas de crédito corporativas.")

df_bancos = fetch_table("gold_gestao_bancaria", schema="gold")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Saldo Bancário Total", "R$ 14.85M", "Disponibilidades")
with c2:
    st.metric("Limite de Crédito Disponível", "R$ 10.00M", "Linhas pré-aprovadas")
with c3:
    st.metric("Instituições Parceiras", "4 Bancos", "Itaú, Bradesco, BTG, Santander")

st.divider()

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.subheader("💰 Distribuição de Saldos por Banco")
    df_bancos_sample = pd.DataFrame({
        "Instituição": ["Itaú Unibanco", "Bradesco Corporate", "BTG Pactual", "Santander Brasil"],
        "Saldo Atual (R$ M)": [6.2, 4.5, 2.8, 1.35]
    })
    fig_banco = px.bar(df_bancos_sample, x="Instituição", y="Saldo Atual (R$ M)", color="Instituição",
                       color_discrete_sequence=['#EC038B', '#CC092F', '#000000', '#EC0000'])
    fig_banco.update_layout(template="plotly_dark", height=380)
    st.plotly_chart(fig_banco, use_container_width=True)

with col_b2:
    st.subheader("💳 Limites de Crédito Operacionais")
    df_limite_sample = pd.DataFrame({
        "Instituição": ["Itaú Unibanco", "Bradesco Corporate", "BTG Pactual", "Santander Brasil"],
        "Limite Utilizado (R$ M)": [1.2, 0.8, 0.5, 0.2],
        "Limite Livre (R$ M)": [3.8, 2.2, 2.5, 0.8]
    })
    fig_lim = px.bar(df_limite_sample, x="Instituição", y=["Limite Utilizado (R$ M)", "Limite Livre (R$ M)"],
                     barmode="stack", color_discrete_sequence=['#EF4444', '#10B981'])
    fig_lim.update_layout(template="plotly_dark", height=380)
    st.plotly_chart(fig_lim, use_container_width=True)

st.subheader("📋 Posição Detalhada por Instituição")
if not df_bancos.empty:
    st.dataframe(df_bancos, use_container_width=True)
else:
    sample_bancos = pd.DataFrame([
        {"Banco": "Itaú Unibanco", "Agência": "0182", "Conta": "98234-1", "Saldo (R$)": 6200000.0, "Limite (R$)": 5000000.0, "Status": "Ativa"},
        {"Banco": "Bradesco Corporate", "Agência": "3400", "Conta": "12450-8", "Saldo (R$)": 4500000.0, "Limite (R$)": 3000000.0, "Status": "Ativa"},
        {"Banco": "BTG Pactual", "Agência": "0001", "Conta": "77812-3", "Saldo (R$)": 2800000.0, "Limite (R$)": 3000000.0, "Status": "Ativa"},
        {"Banco": "Santander Brasil", "Agência": "2100", "Conta": "44301-9", "Saldo (R$)": 1350000.0, "Limite (R$)": 1000000.0, "Status": "Ativa"},
    ])
    st.dataframe(sample_bancos, use_container_width=True)
