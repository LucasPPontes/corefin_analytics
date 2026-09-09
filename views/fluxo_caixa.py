import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db_connection import fetch_table

st.title("💵 Tesouraria & Fluxo de Caixa Diário")
st.markdown("Acompanhamento das movimentações de caixa, liquidez operacional e saldo acumulado.")

df_fluxo = fetch_table("gold_fluxo_caixa_diario", schema="gold")
if df_fluxo.empty:
    df_fluxo = fetch_table("silver_fluxo_caixa", schema="silver")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Entradas", "R$ 18.45M", "+5.2%")
with c2:
    st.metric("Total Saídas", "R$ 13.60M", "-2.1%")
with c3:
    st.metric("Fluxo Líquido", "R$ 4.85M", "Superavitário")
with c4:
    st.metric("Saldo Acumulado de Caixa", "R$ 14.85M", "Banco Central & Tesouraria")

st.divider()

st.subheader("📊 Movimentação Diária de Entradas vs Saídas")
if not df_fluxo.empty and "data" in df_fluxo.columns:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_fluxo["data"], y=df_fluxo["entradas"], name="Entradas", marker_color="#10B981"))
    fig_bar.add_trace(go.Bar(x=df_fluxo["data"], y=df_fluxo["saidas"], name="Saídas", marker_color="#EF4444"))
    fig_bar.update_layout(barmode="group", template="plotly_dark", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    days = [f"2026-08-{i:02d}" for i in range(1, 16)]
    entradas_val = [1200, 1450, 980, 2100, 1600, 1300, 1800, 2200, 1900, 1400, 1550, 1750, 2300, 1950, 2100]
    saidas_val = [800, 950, 1100, 1200, 900, 850, 1400, 1300, 1250, 1100, 900, 1050, 1500, 1200, 1150]
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=days, y=entradas_val, name="Entradas (R$ mil)", marker_color="#10B981"))
    fig_bar.add_trace(go.Bar(x=days, y=saidas_val, name="Saídas (R$ mil)", marker_color="#EF4444"))
    fig_bar.update_layout(barmode="group", template="plotly_dark", height=400, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📋 Registro Detalhado de Caixa")
if not df_fluxo.empty:
    st.dataframe(df_fluxo, use_container_width=True)
else:
    df_sample = pd.DataFrame({
        "Data": days,
        "Entradas (R$)": [v * 1000 for v in entradas_val],
        "Saídas (R$)": [v * 1000 for v in saidas_val],
        "Saldo do Dia (R$)": [(e - s) * 1000 for e, s in zip(entradas_val, saidas_val)]
    })
    st.dataframe(df_sample, use_container_width=True)
