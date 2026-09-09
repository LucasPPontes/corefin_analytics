import streamlit as st

# 1. Configuração Global de Página
st.set_page_config(
    page_title="CoreFin Analytics - Dashboard Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilização CSS Customizada (Design System Sleek Dark & Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Top banner styling */
    .stAppViewHeader {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Card borders */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar badge header */
    .sidebar-header {
        text-align: center;
        padding: 10px;
        font-size: 1.2rem;
        font-weight: 700;
        color: #10B981;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Navegação Multi-páginas usando st.navigation (Estrutura solicitada pelo usuário)
pages = {
    "Visão Executiva": [
        st.Page("views/kpis_executivos.py", title="KPIs & Overview Executivo", icon="📊"),
        st.Page("views/dre_gerencial.py", title="DRE Gerencial", icon="📈"),
    ],
    "Tesouraria & Risco": [
        st.Page("views/fluxo_caixa.py", title="Fluxo de Caixa Diário", icon="💵"),
        st.Page("views/contas_pagar_receber.py", title="Contas a Pagar / Receber", icon="💳"),
        st.Page("views/risco_credito.py", title="Matriz de Risco & Aging List", icon="⚠️"),
        st.Page("views/gestao_bancaria.py", title="Gestão Bancária", icon="🏦"),
    ],
    "Controladoria & FP&A": [
        st.Page("views/centros_custo.py", title="Orçado vs Realizado", icon="🎯"),
    ]
}

# 4. Inicializar Navegação e Executar Página Selecionada
pg = st.navigation(pages)
pg.run()
