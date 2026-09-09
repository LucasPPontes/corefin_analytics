import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.db_connection import fetch_table

st.title("📈 Demonstração do Resultado do Exercício (DRE)")
st.markdown("Estrutura gerencial e demonstração de resultados contábeis e operacionais.")

df_dre = fetch_table("gold_dre_gerencial", schema="gold")
if df_dre.empty:
    df_dre = fetch_table("silver_dre", schema="silver")

# DRE Waterfall Chart
st.subheader("💧 DRE Gerencial - Waterfall (Ponte de Resultado)")

measures = ["absolute", "relative", "total", "relative", "total", "relative", "total"]
x_labels = ["Receita Bruta", "Deduções/Impostos", "Receita Líquida", "Custos (CPV)", "Lucro Bruto", "Despesas Operacionais", "EBITDA"]
y_values = [55.0, -6.5, 0, -18.5, 0, -18.36, 0]

fig_waterfall = go.Figure(go.Waterfall(
    name="DRE 2026",
    orientation="v",
    measure=["absolute", "relative", "total", "relative", "total", "relative", "total"],
    x=x_labels,
    textposition="outside",
    text=["R$ 55.0M", "-R$ 6.5M", "R$ 48.5M", "-R$ 18.5M", "R$ 30.0M", "-R$ 18.36M", "R$ 11.64M"],
    y=[55.0, -6.5, 48.5, -18.5, 30.0, -18.36, 11.64],
    connector={"line": {"color": "#94A3B8"}},
    decreasing={"marker": {"color": "#EF4444"}},
    increasing={"marker": {"color": "#10B981"}},
    totals={"marker": {"color": "#3B82F6"}}
))

fig_waterfall.update_layout(template="plotly_dark", height=450, margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_waterfall, use_container_width=True)

st.divider()

st.subheader("📄 Tabela Detalhada da DRE Gerencial")
if not df_dre.empty:
    st.dataframe(df_dre, use_container_width=True)
else:
    dre_data = pd.DataFrame([
        {"Linha DRE": "1. Receita Operacional Bruta", "Valor (R$)": 55000000.0, "% Receita": "113.4%"},
        {"Linha DRE": "2. Deduções e Impostos sobre Vendas", "Valor (R$)": -6500000.0, "% Receita": "-13.4%"},
        {"Linha DRE": "3. Receita Operacional Líquida", "Valor (R$)": 48500000.0, "% Receita": "100.0%"},
        {"Linha DRE": "4. Custo dos Produtos/Serviços Vendidos (CPV)", "Valor (R$)": -18500000.0, "% Receita": "-38.1%"},
        {"Linha DRE": "5. Lucro Bruto", "Valor (R$)": 30000000.0, "% Receita": "61.9%"},
        {"Linha DRE": "6. Despesas Operacionais (OPEX)", "Valor (R$)": -18360000.0, "% Receita": "-37.9%"},
        {"Linha DRE": "7. EBITDA Consolidado", "Valor (R$)": 11640000.0, "% Receita": "24.0%"},
        {"Linha DRE": "8. Depreciação e Amortização", "Valor (R$)": -2100000.0, "% Receita": "-4.3%"},
        {"Linha DRE": "9. Resultado Financeiro Líquido", "Valor (R$)": -800000.0, "% Receita": "-1.6%"},
        {"Linha DRE": "10. Lucro Líquido do Exercício", "Valor (R$)": 7275000.0, "% Receita": "15.0%"},
    ])
    st.dataframe(dre_data, use_container_width=True)
