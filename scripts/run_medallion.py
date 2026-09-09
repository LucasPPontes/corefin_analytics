import os
import time
import psycopg2
from scripts.seed_bronze import seed_bronze_layer

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres_password")
TARGET_DB = os.getenv("POSTGRES_DB", "corefin")

def get_connection(retries=10, delay=2):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                dbname=TARGET_DB
            )
            return conn
        except Exception as e:
            time.sleep(delay)
    raise Exception(f"Não foi possível conectar ao banco '{TARGET_DB}' no PostgreSQL.")

def process_silver_layer(conn):
    print("[Medalhão] Processando Camada SILVER no schema 'silver'...")
    cur = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS silver;")

    # 1. Silver Overview
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_overview (
            empresa VARCHAR(255),
            periodo VARCHAR(50),
            receita_total NUMERIC(15,2),
            ebitda NUMERIC(15,2),
            ebitda_margin NUMERIC(5,2),
            lucro_liquido NUMERIC(15,2),
            saldo_caixa NUMERIC(15,2),
            dso INT,
            inadimplencia_rate NUMERIC(5,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_overview;")
    cur.execute("""
        INSERT INTO silver.silver_overview (empresa, periodo, receita_total, ebitda, ebitda_margin, lucro_liquido, saldo_caixa, dso, inadimplencia_rate)
        SELECT empresa, periodo, receita_total, ebitda, ebitda_margin, lucro_liquido, saldo_caixa, dso, inadimplencia_rate
        FROM bronze.raw_overview;
    """)

    # 2. Silver Contas a Pagar
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_contas_pagar (
            id VARCHAR(50) PRIMARY KEY,
            fornecedor VARCHAR(255) NOT NULL,
            categoria VARCHAR(100),
            vencimento DATE,
            valor NUMERIC(15,2),
            status VARCHAR(50),
            is_pago BOOLEAN,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_contas_pagar;")
    cur.execute("""
        INSERT INTO silver.silver_contas_pagar (id, fornecedor, categoria, vencimento, valor, status, is_pago)
        SELECT id, TRIM(fornecedor), TRIM(categoria), vencimento, valor, TRIM(status), (LOWER(TRIM(status)) = 'pago')
        FROM bronze.raw_contas_pagar
        WHERE id IS NOT NULL;
    """)

    # 3. Silver Contas a Receber
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_contas_receber (
            id VARCHAR(50) PRIMARY KEY,
            cliente VARCHAR(255) NOT NULL,
            categoria VARCHAR(100),
            vencimento DATE,
            valor NUMERIC(15,2),
            status VARCHAR(50),
            is_recebido BOOLEAN,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_contas_receber;")
    cur.execute("""
        INSERT INTO silver.silver_contas_receber (id, cliente, categoria, vencimento, valor, status, is_recebido)
        SELECT id, TRIM(cliente), TRIM(categoria), vencimento, valor, TRIM(status), (LOWER(TRIM(status)) = 'recebido')
        FROM bronze.raw_contas_receber
        WHERE id IS NOT NULL;
    """)

    # 4. Silver Bancos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_bancos (
            banco VARCHAR(255) PRIMARY KEY,
            agencia VARCHAR(50),
            conta VARCHAR(50),
            saldo NUMERIC(15,2),
            limite NUMERIC(15,2),
            status VARCHAR(50),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_bancos;")
    cur.execute("""
        INSERT INTO silver.silver_bancos (banco, agencia, conta, saldo, limite, status)
        SELECT TRIM(banco), TRIM(agencia), TRIM(conta), saldo, limite, TRIM(status)
        FROM bronze.raw_bancos
        WHERE banco IS NOT NULL;
    """)

    # 5. Silver Fluxo de Caixa
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_fluxo_caixa (
            data DATE PRIMARY KEY,
            entradas NUMERIC(15,2),
            saidas NUMERIC(15,2),
            saldo_dia NUMERIC(15,2),
            saldo_acumulado NUMERIC(15,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_fluxo_caixa;")
    cur.execute("""
        INSERT INTO silver.silver_fluxo_caixa (data, entradas, saidas, saldo_dia, saldo_acumulado)
        SELECT data, entradas, saidas, saldo_dia, saldo_acumulado
        FROM bronze.raw_fluxo_caixa
        WHERE data IS NOT NULL;
    """)

    # 6. Silver DRE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_dre (
            linha VARCHAR(255) PRIMARY KEY,
            valor NUMERIC(15,2),
            percentual VARCHAR(50),
            categoria VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_dre;")
    cur.execute("""
        INSERT INTO silver.silver_dre (linha, valor, percentual, categoria)
        SELECT TRIM(linha), valor, TRIM(percentual), TRIM(categoria)
        FROM bronze.raw_dre
        WHERE linha IS NOT NULL;
    """)

    # 7. Silver Centros de Custo
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_centros_custo (
            centro_custo VARCHAR(255) PRIMARY KEY,
            orcado NUMERIC(15,2),
            realizado NUMERIC(15,2),
            variancia NUMERIC(15,2),
            status VARCHAR(50),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_centros_custo;")
    cur.execute("""
        INSERT INTO silver.silver_centros_custo (centro_custo, orcado, realizado, variancia, status)
        SELECT TRIM(centro_custo), orcado, realizado, variancia, TRIM(status)
        FROM bronze.raw_centros_custo
        WHERE centro_custo IS NOT NULL;
    """)

    # 8. Silver Clientes Críticos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS silver.silver_clientes_criticos (
            cliente VARCHAR(255) PRIMARY KEY,
            rating VARCHAR(50),
            limite_concedido NUMERIC(15,2),
            utilizado NUMERIC(15,2),
            em_atraso NUMERIC(15,2),
            dias_atraso INT,
            status_cobranca VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE silver.silver_clientes_criticos;")
    cur.execute("""
        INSERT INTO silver.silver_clientes_criticos (cliente, rating, limite_concedido, utilizado, em_atraso, dias_atraso, status_cobranca)
        SELECT TRIM(cliente), TRIM(rating), limite_concedido, utilizado, em_atraso, dias_atraso, TRIM(status_cobranca)
        FROM bronze.raw_clientes_criticos
        WHERE cliente IS NOT NULL;
    """)

    conn.commit()
    cur.close()
    print("[Medalhão] Camada SILVER processada com sucesso!")

def process_gold_layer(conn):
    print("[Medalhão] Processando Camada GOLD no schema 'gold'...")
    cur = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS gold;")

    # 1. Gold KPIs Executivos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_kpis_executivos (
            indicador VARCHAR(255) PRIMARY KEY,
            valor_formatado VARCHAR(100),
            valor_numerico NUMERIC(15,2),
            categoria VARCHAR(100),
            descricao TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_kpis_executivos;")
    cur.execute("""
        INSERT INTO gold.gold_kpis_executivos (indicador, valor_formatado, valor_numerico, categoria, descricao)
        VALUES 
            ('Receita Liquida Consolidada', 'R$ 48.50M', 48500000.00, 'Financeiro', 'Faturamento liquido total acumulado'),
            ('EBITDA Consolidado', 'R$ 11.64M', 11640000.00, 'Financeiro', 'Lucro antes de juros, impostos, depreciacao e amortizacao'),
            ('Margem EBITDA', '24.0%', 24.00, 'Financeiro', 'Margem percentual de EBITDA'),
            ('Lucro Liquido', 'R$ 7.28M', 7275000.00, 'Financeiro', 'Resultado liquido final do exercicio'),
            ('Saldo de Caixa', 'R$ 14.85M', 14850000.00, 'Liquidez', 'Posicao consolidada de disponibilidade em caixa e bancos'),
            ('DSO (Days Sales Outstanding)', '42 Dias', 42.00, 'Operacional', 'Prazo medio de recebimento de vendas');
    """)

    # 2. Gold Fluxo de Caixa Diário
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_fluxo_caixa_diario (
            data DATE PRIMARY KEY,
            entradas NUMERIC(15,2),
            saidas NUMERIC(15,2),
            saldo_liquido NUMERIC(15,2),
            saldo_acumulado NUMERIC(15,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_fluxo_caixa_diario;")
    cur.execute("""
        INSERT INTO gold.gold_fluxo_caixa_diario (data, entradas, saidas, saldo_liquido, saldo_acumulado)
        SELECT data, entradas, saidas, saldo_dia, saldo_acumulado
        FROM silver.silver_fluxo_caixa
        WHERE data IS NOT NULL;
    """)

    # 3. Gold DRE Gerencial
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_dre_gerencial (
            linha VARCHAR(255) PRIMARY KEY,
            valor NUMERIC(15,2),
            percentual VARCHAR(50),
            categoria VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_dre_gerencial;")
    cur.execute("""
        INSERT INTO gold.gold_dre_gerencial (linha, valor, percentual, categoria)
        SELECT linha, valor, percentual, categoria
        FROM silver.silver_dre
        WHERE linha IS NOT NULL;
    """)

    # 4. Gold Matriz de Risco & Aging List
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_matriz_risco_aging (
            faixa_atraso VARCHAR(100) PRIMARY KEY,
            valor_exposto NUMERIC(15,2),
            percentual_carteira NUMERIC(5,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_matriz_risco_aging;")
    cur.execute("""
        INSERT INTO gold.gold_matriz_risco_aging (faixa_atraso, valor_exposto, percentual_carteira)
        VALUES 
            ('Adimplente', 8200000.00, 65.80),
            ('1 a 30 dias', 850000.00, 6.80),
            ('31 a 60 dias', 420000.00, 3.40),
            ('61 a 90 dias', 180000.00, 1.45),
            ('> 90 dias', 80000.00, 0.65);
    """)

    # 5. Gold Clientes Críticos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_clientes_criticos (
            cliente VARCHAR(255) PRIMARY KEY,
            rating VARCHAR(50),
            limite_concedido NUMERIC(15,2),
            utilizado NUMERIC(15,2),
            em_atraso NUMERIC(15,2),
            dias_atraso INT,
            status_cobranca VARCHAR(100),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_clientes_criticos;")
    cur.execute("""
        INSERT INTO gold.gold_clientes_criticos (cliente, rating, limite_concedido, utilizado, em_atraso, dias_atraso, status_cobranca)
        SELECT cliente, rating, limite_concedido, utilizado, em_atraso, dias_atraso, status_cobranca
        FROM silver.silver_clientes_criticos
        WHERE cliente IS NOT NULL;
    """)

    # 6. Gold Gestão Bancária
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold.gold_gestao_bancaria (
            banco VARCHAR(255) PRIMARY KEY,
            saldo_atual NUMERIC(15,2),
            limite_credito NUMERIC(15,2),
            saldo_disponivel NUMERIC(15,2),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("TRUNCATE TABLE gold.gold_gestao_bancaria;")
    cur.execute("""
        INSERT INTO gold.gold_gestao_bancaria (banco, saldo_atual, limite_credito, saldo_disponivel)
        SELECT banco, saldo, limite, (saldo + limite)
        FROM silver.silver_bancos
        WHERE banco IS NOT NULL;
    """)

    conn.commit()
    cur.close()
    print("[Medalhão] Camada GOLD processada com sucesso!")

def run_medallion_pipeline():
    print("==================================================================")
    print("🚀 PIPELINE MEDALHÃO EM PYTHON (BRONZE -> SILVER -> GOLD) NO POSTGRESQL")
    print("==================================================================")
    
    # 1. Popula Camada Bronze
    seed_bronze_layer()

    # 2. Processa Silver & Gold
    conn = get_connection()
    process_silver_layer(conn)
    process_gold_layer(conn)
    conn.close()

    print("==================================================================")
    print("✅ PIPELINE MEDALHÃO CONCLUÍDO COM SUCESSO NO BANCO 'corefin'!")
    print("==================================================================")

if __name__ == "__main__":
    run_medallion_pipeline()
