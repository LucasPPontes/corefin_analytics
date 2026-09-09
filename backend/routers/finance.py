import os
import psycopg2
import pandas as pd
from fastapi import APIRouter, HTTPException
from scripts.run_medallion import run_medallion_pipeline

router = APIRouter(prefix="/api", tags=["finance"])

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres_password")
TARGET_DB = os.getenv("POSTGRES_DB", "corefin")

def get_db_connection():
    try:
        return psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=TARGET_DB,
            connect_timeout=3
        )
    except Exception:
        return None

def fetch_schema_table(schema: str, table: str):
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql_query(f'SELECT * FROM "{schema}"."{table}"', conn)
            conn.close()
            return df.to_dict(orient="records")
        except Exception:
            conn.close()
    return []

@router.post("/etl/run")
def trigger_medallion_etl():
    """Dispara a execução do Pipeline Medalhão (Bronze -> Silver -> Gold) no PostgreSQL."""
    try:
        run_medallion_pipeline()
        return {
            "status": "sucesso",
            "mensagem": "Pipeline Medalhão executado com sucesso nas camadas bronze, silver e gold do PostgreSQL!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar pipeline: {str(e)}")

@router.get("/kpis")
def get_kpis():
    """Retorna os KPIs executivos da camada Gold no PostgreSQL."""
    data = fetch_schema_table("gold", "gold_kpis_executivos")
    return {"status": "sucesso", "kpis": data}

@router.get("/dre")
def get_dre():
    """Retorna a DRE Gerencial da camada Gold no PostgreSQL."""
    data = fetch_schema_table("gold", "gold_dre_gerencial")
    return {"status": "sucesso", "dre": data}

@router.get("/fluxo-caixa")
def get_fluxo_caixa():
    """Retorna o fluxo de caixa diário consolidado da camada Gold."""
    data = fetch_schema_table("gold", "gold_fluxo_caixa_diario")
    return {"status": "sucesso", "fluxo_caixa": data}

@router.get("/risco")
def get_risco():
    """Retorna a matriz de risco e clientes críticos da camada Gold."""
    aging = fetch_schema_table("gold", "gold_matriz_risco_aging")
    criticos = fetch_schema_table("gold", "gold_clientes_criticos")
    return {"status": "sucesso", "aging_list": aging, "clientes_criticos": criticos}

@router.get("/gestao-bancaria")
def get_bancos():
    """Retorna posições bancárias e limites de crédito da camada Gold."""
    data = fetch_schema_table("gold", "gold_gestao_bancaria")
    return {"status": "sucesso", "bancos": data}

@router.get("/centros-custo")
def get_centros_custo():
    """Retorna variação orçamentária por centro de custo da camada Silver."""
    data = fetch_schema_table("silver", "silver_centros_custo")
    return {"status": "sucesso", "centros_custo": data}
