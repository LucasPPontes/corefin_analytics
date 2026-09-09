import os
import json
import pandas as pd
import psycopg2

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "corefin")

def get_db_connection():
    """Tenta estabelecer conexão nativa com o banco PostgreSQL 'corefin'."""
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB,
            connect_timeout=3
        )
        return conn
    except Exception:
        return None

def fetch_table(table_name: str, schema: str = "gold") -> pd.DataFrame:
    """Busca tabela do PostgreSQL; se falhar, obtém dados fallback do JSON corporativo."""
    conn = get_db_connection()
    if conn:
        try:
            query = f'SELECT * FROM "{schema}"."{table_name}"'
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception:
            conn.close()
            
    # Fallback inteligente usando dados JSON locais se o DB estiver offline
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "finance_corporate_data.json")
    if not os.path.exists(json_path):
        json_path = "/app/data/finance_corporate_data.json"
        
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                
            if table_name == "gold_kpis_executivos":
                ov = raw_data.get("overview", {})
                return pd.DataFrame([
                    {"indicador": "Receita Liquida Consolidada", "valor_formatado": "R$ 48.50M", "valor_numerico": ov.get("receita_total", 48500000.0), "categoria": "Financeiro"},
                    {"indicador": "EBITDA Consolidado", "valor_formatado": "R$ 11.64M", "valor_numerico": ov.get("ebitda", 11640000.0), "categoria": "Financeiro"},
                    {"indicador": "Margem EBITDA", "valor_formatado": "24.0%", "valor_numerico": ov.get("ebitda_margin", 24.0), "categoria": "Financeiro"},
                    {"indicador": "Lucro Liquido", "valor_formatado": "R$ 7.28M", "valor_numerico": ov.get("lucro_liquido", 7275000.0), "categoria": "Financeiro"},
                    {"indicador": "Saldo de Caixa", "valor_formatado": "R$ 14.85M", "valor_numerico": ov.get("saldo_caixa", 14850000.0), "categoria": "Liquidez"},
                ])
            elif table_name == "gold_fluxo_caixa_diario" or table_name == "silver_fluxo_caixa":
                return pd.DataFrame(raw_data.get("tesouraria", {}).get("fluxo_caixa_diario", []))
            elif table_name == "gold_dre_gerencial" or table_name == "silver_dre":
                return pd.DataFrame(raw_data.get("controladoria", {}).get("dre", []))
            elif table_name == "silver_contas_pagar":
                return pd.DataFrame(raw_data.get("tesouraria", {}).get("contas_pagar", []))
            elif table_name == "silver_contas_receber":
                return pd.DataFrame(raw_data.get("tesouraria", {}).get("contas_receber", []))
            elif table_name == "gold_gestao_bancaria" or table_name == "silver_bancos":
                return pd.DataFrame(raw_data.get("tesouraria", {}).get("bancos", []))
            elif table_name == "silver_centros_custo":
                return pd.DataFrame(raw_data.get("controladoria", {}).get("custos", {}).get("centros_custo", []))
            elif table_name == "gold_clientes_criticos" or table_name == "silver_clientes_criticos":
                return pd.DataFrame(raw_data.get("credito_cobranca", {}).get("clientes_criticos", []))
            elif table_name == "gold_matriz_risco_aging":
                return pd.DataFrame(raw_data.get("credito_cobranca", {}).get("aging_list", []))
        except Exception:
            pass

    return pd.DataFrame()
