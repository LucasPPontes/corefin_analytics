import os
import json
import time
import psycopg2
from psycopg2.extras import execute_values

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres_password")
TARGET_DB = os.getenv("POSTGRES_DB", "corefin")

def get_connection(retries=15, delay=3):
    """Conecta ao PostgreSQL com retry exponencial até o serviço estar pronto."""
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                dbname=TARGET_DB
            )
            print(f"[Seed Bronze] Conectado com sucesso ao PostgreSQL '{TARGET_DB}'!")
            return conn
        except Exception as e:
            print(f"[Seed Bronze] Aguardando PostgreSQL ({i+1}/{retries})... Erro: {e}")
            time.sleep(delay)
    raise Exception("Não foi possível conectar ao PostgreSQL.")

def seed_bronze_layer():
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "finance_corporate_data.json")
    if not os.path.exists(json_path):
        json_path = "/app/data/finance_corporate_data.json"
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    conn.commit()

    print("==================================================================")
    print("🥉 INGESTÃO DA CAMADA BRONZE (SCHEMA bronze) NO POSTGRESQL")
    print("==================================================================")

    # 1. Table: bronze.raw_overview
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_overview (
            empresa TEXT,
            periodo TEXT,
            receita_total NUMERIC(15,2),
            ebitda NUMERIC(15,2),
            ebitda_margin NUMERIC(5,2),
            lucro_liquido NUMERIC(15,2),
            saldo_caixa NUMERIC(15,2),
            dso INT,
            inadimplencia_rate NUMERIC(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_overview;")
    ov = data.get("overview", {})
    cur.execute("""
        INSERT INTO bronze.raw_overview (empresa, periodo, receita_total, ebitda, ebitda_margin, lucro_liquido, saldo_caixa, dso, inadimplencia_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        ov.get("empresa", "CoreFin Analytics"),
        ov.get("periodo", "Q3 2026"),
        ov.get("receita_total", 48500000.0),
        ov.get("ebitda", 11640000.0),
        ov.get("ebitda_margin", 24.0),
        ov.get("lucro_liquido", 7275000.0),
        ov.get("saldo_caixa", 14850000.0),
        ov.get("dso", 42),
        ov.get("inadimplencia_rate", 2.45)
    ))

    # 2. Table: bronze.raw_contas_pagar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_contas_pagar (
            id TEXT,
            fornecedor TEXT,
            categoria TEXT,
            vencimento DATE,
            valor NUMERIC(15,2),
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_contas_pagar;")
    pagar = data.get("tesouraria", {}).get("contas_pagar", [])
    if pagar:
        records = [(r.get("id"), r.get("fornecedor"), r.get("categoria"), r.get("vencimento"), r.get("valor"), r.get("status")) for r in pagar]
        execute_values(cur, "INSERT INTO bronze.raw_contas_pagar (id, fornecedor, categoria, vencimento, valor, status) VALUES %s", records)

    # 3. Table: bronze.raw_contas_receber
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_contas_receber (
            id TEXT,
            cliente TEXT,
            categoria TEXT,
            vencimento DATE,
            valor NUMERIC(15,2),
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_contas_receber;")
    receber = data.get("tesouraria", {}).get("contas_receber", [])
    if receber:
        records = [(r.get("id"), r.get("cliente"), r.get("categoria"), r.get("vencimento"), r.get("valor"), r.get("status")) for r in receber]
        execute_values(cur, "INSERT INTO bronze.raw_contas_receber (id, cliente, categoria, vencimento, valor, status) VALUES %s", records)

    # 4. Table: bronze.raw_bancos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_bancos (
            banco TEXT,
            agencia TEXT,
            conta TEXT,
            saldo NUMERIC(15,2),
            limite NUMERIC(15,2),
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_bancos;")
    bancos = data.get("tesouraria", {}).get("bancos", [])
    if bancos:
        records = [
            (
                r.get("banco"),
                r.get("agencia"),
                r.get("conta"),
                r.get("saldo", 0.0),
                r.get("limite_credito", r.get("limite", 0.0)),
                r.get("status", "Ativa")
            )
            for r in bancos
        ]
        execute_values(cur, "INSERT INTO bronze.raw_bancos (banco, agencia, conta, saldo, limite, status) VALUES %s", records)

    # 5. Table: bronze.raw_fluxo_caixa
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_fluxo_caixa (
            data DATE,
            entradas NUMERIC(15,2),
            saidas NUMERIC(15,2),
            saldo_dia NUMERIC(15,2),
            saldo_acumulado NUMERIC(15,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_fluxo_caixa;")
    fluxo = data.get("tesouraria", {}).get("fluxo_caixa_diario", [])
    if fluxo:
        records = []
        for r in fluxo:
            d_val = r.get("data_completa", r.get("data"))
            e_val = float(r.get("entradas", 0.0))
            s_val = float(r.get("saidas", 0.0))
            s_dia = r.get("saldo_dia", e_val - s_val)
            s_acum = r.get("saldo_acumulado", 0.0)
            records.append((d_val, e_val, s_val, s_dia, s_acum))
        execute_values(cur, "INSERT INTO bronze.raw_fluxo_caixa (data, entradas, saidas, saldo_dia, saldo_acumulado) VALUES %s", records)

    # 6. Table: bronze.raw_dre
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_dre (
            linha TEXT,
            valor NUMERIC(15,2),
            percentual TEXT,
            categoria TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_dre;")
    dre = data.get("controladoria", {}).get("dre", [])
    if dre:
        records = [
            (
                r.get("item", r.get("linha")),
                r.get("valor"),
                str(r.get("porcentagem", r.get("percentual", "0%"))),
                r.get("tipo", r.get("categoria", "DRE"))
            )
            for r in dre
        ]
        execute_values(cur, "INSERT INTO bronze.raw_dre (linha, valor, percentual, categoria) VALUES %s", records)

    # 7. Table: bronze.raw_centros_custo
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_centros_custo (
            centro_custo TEXT,
            orcado NUMERIC(15,2),
            realizado NUMERIC(15,2),
            variancia NUMERIC(15,2),
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_centros_custo;")
    custos = data.get("controladoria", {}).get("custos", {}).get("centros_custo", [])
    if custos:
        records = []
        for r in custos:
            cc_nome = r.get("centro", r.get("centro_custo"))
            o_val = float(r.get("orcado", 0.0))
            r_val = float(r.get("realizado", 0.0))
            v_val = r.get("variacao", r.get("variancia", r_val - o_val))
            st_val = r.get("status", "Dentro do Orçamento" if r_val <= o_val else "Atenção (Estouro)")
            records.append((cc_nome, o_val, r_val, v_val, st_val))
        execute_values(cur, "INSERT INTO bronze.raw_centros_custo (centro_custo, orcado, realizado, variancia, status) VALUES %s", records)

    # 8. Table: bronze.raw_clientes_criticos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bronze.raw_clientes_criticos (
            cliente TEXT,
            rating TEXT,
            limite_concedido NUMERIC(15,2),
            utilizado NUMERIC(15,2),
            em_atraso NUMERIC(15,2),
            dias_atraso INT,
            status_cobranca TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE bronze.raw_clientes_criticos;")
    cc_list = data.get("credito_cobranca", {}).get("clientes_criticos", [])
    if cc_list:
        records = [(r.get("cliente"), r.get("rating"), r.get("limite_concedido"), r.get("utilizado"), r.get("em_atraso"), r.get("dias_atraso"), r.get("status_cobranca")) for r in cc_list]
        execute_values(cur, "INSERT INTO bronze.raw_clientes_criticos (cliente, rating, limite_concedido, utilizado, em_atraso, dias_atraso, status_cobranca) VALUES %s", records)

    conn.commit()
    cur.close()
    conn.close()
    print("==================================================================")
    print("✅ CAMADA BRONZE POPULADA COM SUCESSO NO POSTGRESQL!")
    print("==================================================================")

if __name__ == "__main__":
    seed_bronze_layer()
