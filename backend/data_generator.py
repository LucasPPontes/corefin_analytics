import json
import os
from typing import Dict, Any

def generate_corporate_finance_data() -> Dict[str, Any]:
    """Gera massa de dados corporativos para Tesouraria, Controladoria, FP&A e Crédito/Cobrança."""
    
    months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    # 1. Visão Geral (Executive Overview)
    overview = {
        "empresa": "CoreFin Analytics (Fictício)",
        "periodo": "Q3 2026",
        "receita_total": 48500000.00,
        "ebitda": 11640000.00,
        "ebitda_margin": 24.0,
        "lucro_liquido": 7275000.00,
        "saldo_caixa": 14850000.00,
        "dso": 42,
        "inadimplencia_rate": 2.45,
        "kpis": [
            {"label": "Faturamento Mensal", "value": "R$ 16,16M", "change": "+12.5%", "trend": "up", "status": "good"},
            {"label": "EBITDA Consolidado", "value": "R$ 3,88M", "change": "+8.2%", "trend": "up", "status": "good"},
            {"label": "Margem Líquida", "value": "15.0%", "change": "+1.5 p.p.", "trend": "up", "status": "good"},
            {"label": "Liquidez Corrente", "value": "2.14", "change": "-0.05", "trend": "down", "status": "neutral"},
            {"label": "Inadimplência (Aging > 30d)", "value": "2.45%", "change": "-0.35 p.p.", "trend": "down", "status": "good"}
        ],
        "monthly_trend": [
            {"month": m, "receita": round(3500000 + i * 250000 + (i % 3) * 100000, 2), 
             "custos": round(2600000 + i * 180000, 2), 
             "ebitda": round(900000 + i * 70000 + (i % 3) * 100000, 2),
             "lucro": round(550000 + i * 45000, 2)}
            for i, m in enumerate(months)
        ]
    }
    
    # 2. Tesouraria (Treasury)
    tesouraria = {
        "kpis": {
            "saldo_atual": 14850000.00,
            "entradas_mes": 16200000.00,
            "saidas_mes": 12450000.00,
            "saldo_projetado_30d": 18600000.00,
            "pagar_hoje": 420000.00,
            "receber_hoje": 680000.00
        },
        "fluxo_caixa_diario": [
            {
                "dia": f"{i+1:02d}/08",
                "data_completa": f"2026-08-{i+1:02d}",
                "entradas": round(450000 + (i % 5) * 80000 + (i % 3) * 50000, 2),
                "saidas": round(320000 + (i % 4) * 60000 + (i % 2) * 90000, 2),
                "saldo_acumulado": round(14850000.00 + (i + 1) * 125000, 2)
            }
            for i in range(31)
        ],
        "contas_pagar": [
            {"id": "PAG-101", "fornecedor": "AWS Cloud Services (Fictício)", "categoria": "Infraestrutura IT", "vencimento": "2026-08-12", "valor": 145000.00, "status": "Pendente"},
            {"id": "PAG-102", "fornecedor": "Dell Compute Corp (Fictício)", "categoria": "Hardware/Equipamentos", "vencimento": "2026-08-15", "valor": 88000.00, "status": "Pendente"},
            {"id": "PAG-103", "fornecedor": "Folha de Pagamento - CLT (Fictício)", "categoria": "Recursos Humanos", "vencimento": "2026-08-20", "valor": 3450000.00, "status": "Agendado"},
            {"id": "PAG-104", "fornecedor": "Imobiliária Corporate Park (Fictício)", "categoria": "Aluguel & Condomínio", "vencimento": "2026-08-10", "valor": 120000.00, "status": "Pago"},
            {"id": "PAG-105", "fornecedor": "Oracle Software Brasil (Fictício)", "categoria": "Licenciamento ERP", "vencimento": "2026-08-05", "valor": 65000.00, "status": "Pago"},
            {"id": "PAG-106", "fornecedor": "Consultoria KPMG (Fictício)", "categoria": "Auditoria & Compliance", "vencimento": "2026-08-25", "valor": 95000.00, "status": "Pendente"}
        ],
        "contas_receber": [
            {"id": "REC-301", "cliente": "Banco Itaú BBA S.A. (Fictício)", "categoria": "Licença Enterprise", "vencimento": "2026-08-10", "valor": 450000.00, "status": "Recebido"},
            {"id": "REC-302", "cliente": "Magazine Luiza Tech (Fictício)", "categoria": "Contrato Anual SaaS", "vencimento": "2026-08-14", "valor": 280000.00, "status": "A pagar"},
            {"id": "REC-303", "cliente": "Ambev S.A. (Fictício)", "categoria": "Custom Development", "vencimento": "2026-08-18", "valor": 620000.00, "status": "A pagar"},
            {"id": "REC-304", "cliente": "Naturacosmetics S.A. (Fictício)", "categoria": "Suporte Premium", "vencimento": "2026-08-02", "valor": 115000.00, "status": "Em Atraso"},
            {"id": "REC-305", "cliente": "Rede D'Or São Luiz (Fictício)", "categoria": "Plataforma Analytics", "vencimento": "2026-08-22", "valor": 340000.00, "status": "A pagar"}
        ],
        "bancos": [
            {"banco": "Itaú Unibanco (Fictício)", "agencia": "0001", "conta": "48920-1", "saldo": 6850000.00, "tipo": "Conta Corrente", "limite_credito": 5000000.00, "rendimento_cdi": "100% CDI"},
            {"banco": "Bradesco Corporate (Fictício)", "agencia": "3920", "conta": "10293-8", "saldo": 3420000.00, "tipo": "Conta Corrente", "limite_credito": 3000000.00, "rendimento_cdi": "101% CDI"},
            {"banco": "BTG Pactual Asset (Fictício)", "agencia": "0001", "conta": "99210-4", "saldo": 3800000.00, "tipo": "Aplicação CDB/LF", "limite_credito": 0.0, "rendimento_cdi": "104% CDI"},
            {"banco": "Santander Brasil (Fictício)", "agencia": "1102", "conta": "55410-0", "saldo": 780000.00, "tipo": "Conta Operacional", "limite_credito": 2000000.00, "rendimento_cdi": "98% CDI"}
        ]
    }
    
    # 3. Controladoria (Controller / Accounting)
    controladoria = {
        "kpis": {
            "receita_bruta": 52400000.00,
            "deducoes_impostos": 3900000.00,
            "receita_liquida": 48500000.00,
            "margem_contribuição": 62.5,
            "margem_ebitda": 24.0,
            "margem_liquida": 15.0
        },
        "dre": [
            {"item": "(=) Receita Bruta de Vendas", "valor": 52400000.00, "porcentagem": 108.0, "nivel": 1, "tipo": "receita"},
            {"item": "(-) Impostos sobre Vendas (PIS/COFINS/ISS)", "valor": -3900000.00, "porcentagem": -8.0, "nivel": 2, "tipo": "deducao"},
            {"item": "(=) Receita Líquida", "valor": 48500000.00, "porcentagem": 100.0, "nivel": 1, "tipo": "total"},
            {"item": "(-) Custo dos Produtos/Serviços Vendidos (CPV)", "valor": -18187500.00, "porcentagem": -37.5, "nivel": 2, "tipo": "custo"},
            {"item": "(=) Lucro Bruto", "valor": 30312500.00, "porcentagem": 62.5, "nivel": 1, "tipo": "total"},
            {"item": "(-) Despesas Operacionais (OPEX)", "valor": -18672500.00, "porcentagem": -38.5, "nivel": 2, "tipo": "despesa"},
            {"item": "   - Vendas e Marketing", "valor": -7275000.00, "porcentagem": -15.0, "nivel": 3, "tipo": "subitem"},
            {"item": "   - Pesquisa e Desenvolvimento (R&D)", "valor": -5820000.00, "porcentagem": -12.0, "nivel": 3, "tipo": "subitem"},
            {"item": "   - General & Administrative (G&A)", "valor": -5577500.00, "porcentagem": -11.5, "nivel": 3, "tipo": "subitem"},
            {"item": "(=) EBITDA", "valor": 11640000.00, "porcentagem": 24.0, "nivel": 1, "tipo": "total"},
            {"item": "(-) Depreciação e Amortização", "valor": -1455000.00, "porcentagem": -3.0, "nivel": 2, "tipo": "despesa"},
            {"item": "(=) EBIT (Resultado Operacional)", "valor": 10185000.00, "porcentagem": 21.0, "nivel": 1, "tipo": "total"},
            {"item": "(+/-) Resultado Financeiro Líquido", "valor": -485000.00, "porcentagem": -1.0, "nivel": 2, "tipo": "financeiro"},
            {"item": "(=) LAIR / EBT", "valor": 9700000.00, "porcentagem": 20.0, "nivel": 1, "tipo": "total"},
            {"item": "(-) IRPJ e CSLL (Lucro Real)", "valor": -2425000.00, "porcentagem": -5.0, "nivel": 2, "tipo": "imposto"},
            {"item": "(=) Lucro Líquido do Exercício", "valor": 7275000.00, "porcentagem": 15.0, "nivel": 1, "tipo": "destaque"}
        ],
        "custos": {
            "proporcao": [
                {"name": "Custos Fixos (OPEX Fixo)", "value": 14200000.00, "fill": "#6366f1"},
                {"name": "Custos Variáveis (CPV Direto)", "value": 18187500.00, "fill": "#14b8a6"},
                {"name": "Despesas Comerciais Variáveis", "value": 4472500.00, "fill": "#f59e0b"}
            ],
            "centros_custo": [
                {"centro": "Engenharia & Produto", "orcado": 6000000.00, "realizado": 5820000.00, "variacao": -3.0},
                {"centro": "Operações & Cloud", "orcado": 17500000.00, "realizado": 18187500.00, "variacao": +3.9},
                {"centro": "Vendas & Growth", "orcado": 7000000.00, "realizado": 7275000.00, "variacao": +3.9},
                {"centro": "Financeiro & Jurídico", "orcado": 2800000.00, "realizado": 2650000.00, "variacao": -5.3},
                {"centro": "People & RH", "orcado": 3000000.00, "realizado": 2927500.00, "variacao": -2.4}
            ]
        },
        "orcamento_contas": [
            {"conta": "1.01.01 - Pessoal & Encargos", "orcado": 14500000.00, "realizado": 14280000.00, "desvio_pct": -1.5, "status": "Dentro da Meta"},
            {"conta": "1.01.02 - Serviços de Terceiros", "orcado": 3800000.00, "realizado": 4120000.00, "desvio_pct": +8.4, "status": "Alerta Acima"},
            {"conta": "1.02.01 - Licenças & Software IT", "orcado": 2200000.00, "realizado": 2150000.00, "desvio_pct": -2.2, "status": "Dentro da Meta"},
            {"conta": "1.02.02 - Infraestrutura Cloud & Data Center", "orcado": 5500000.00, "realizado": 5890000.00, "desvio_pct": +7.1, "status": "Alerta Acima"},
            {"conta": "1.03.01 - Mídia Performance & Marketing", "orcado": 3200000.00, "realizado": 3150000.00, "desvio_pct": -1.5, "status": "Dentro da Meta"},
            {"conta": "1.04.01 - Viagens & Representação", "orcado": 800000.00, "realizado": 680000.00, "desvio_pct": -15.0, "status": "Economia"}
        ],
        "relatorios_fiscais": [
            {"tributo": "PIS / COFINS (Regime Não-Cumulativo)", "base_calculo": 48500000.00, "aliquota": "9.25%", "valor_devido": 4486250.00, "vencimento": "2026-08-25", "status": "Calculado"},
            {"tributo": "ISSQN (Município de São Paulo)", "base_calculo": 32000000.00, "aliquota": "5.00%", "valor_devido": 1600000.00, "vencimento": "2026-08-10", "status": "Pago"},
            {"tributo": "IRPJ (Lucro Real Estimado)", "base_calculo": 9700000.00, "aliquota": "15.00% + 10%", "valor_devido": 2425000.00, "vencimento": "2026-08-31", "status": "Em Aberto"},
            {"tributo": "CSLL (Lucro Real Estimado)", "base_calculo": 9700000.00, "aliquota": "9.00%", "valor_devido": 873000.00, "vencimento": "2026-08-31", "status": "Em Aberto"}
        ]
    }
    
    # 4. FP&A (Financial Planning & Analysis)
    fpa = {
        "kpis": {
            "cagr_receita": 18.5,
            "roi_projetos": 22.4,
            "desvio_orcamentario_global": -1.2,
            "forecast_anual": 195000000.00,
            "run_rate_anual": 194000000.00
        },
        "cenarios": {
            "base": {
                "nome": "Cenário Base (Plan 2026)",
                "receita_anual": 195000000.00,
                "ebitda_anual": 46800000.00,
                "ebitda_margin": 24.0,
                "crescimento_yo_y": 18.5,
                "premissas": "Crescimento constante de 1.5% ao mês, inflação IPCA 4.2%, churn de clientes em 1.1%."
            },
            "otimista": {
                "nome": "Cenário Otimista (High Growth)",
                "receita_anual": 224250000.00,
                "ebitda_anual": 58305000.00,
                "ebitda_margin": 26.0,
                "crescimento_yo_y": 32.0,
                "premissas": "Expansão para mercado LATAM, upselling de 20% na base Enterprise, ganho de eficiência operacional."
            },
            "pessimista": {
                "nome": "Cenário Pessimista (Downside Risk)",
                "receita_anual": 165750000.00,
                "ebitda_anual": 33150000.00,
                "ebitda_margin": 20.0,
                "crescimento_yo_y": 5.0,
                "premissas": "Retração no setor de tecnologia, aumento do ciclo de vendas para 90 dias, churn de 2.5%."
            }
        },
        "variancia": [
            {"unidade": "Enterprise Software", "orcado": 28000000.00, "realizado": 29500000.00, "variacao_brl": 1500000.00, "variacao_pct": +5.36},
            {"unidade": "SMB & Mid-Market", "orcado": 12500000.00, "realizado": 11800000.00, "variacao_brl": -700000.00, "variacao_pct": -5.60},
            {"unidade": "Serviços Profissionais", "orcado": 5000000.00, "realizado": 4800000.00, "variacao_brl": -200000.00, "variacao_pct": -4.00},
            {"unidade": "Internacional (LATAM)", "orcado": 3000000.00, "realizado": 2400000.00, "variacao_brl": -600000.00, "variacao_pct": -20.00}
        ],
        "rolling_forecast": [
            {"periodo": "Q1 2026", "realizado": 42000000.00, "orcado": 41000000.00, "forecast": 42000000.00},
            {"periodo": "Q2 2026", "realizado": 46500000.00, "orcado": 45000000.00, "forecast": 46500000.00},
            {"periodo": "Q3 2026", "realizado": 48500000.00, "orcado": 49000000.00, "forecast": 48500000.00},
            {"periodo": "Q4 2026 (F)", "realizado": None, "orcado": 54000000.00, "forecast": 56000000.00},
            {"periodo": "Q1 2027 (F)", "realizado": None, "orcado": 58000000.00, "forecast": 60500000.00},
            {"periodo": "Q2 2027 (F)", "realizado": None, "orcado": 62000000.00, "forecast": 65000000.00}
        ]
    }
    
    # 5. Crédito e Cobrança (Credit & Collections)
    credito_cobranca = {
        "kpis": {
            "carteira_total_credito": 38500000.00,
            "limite_concedido_total": 55000000.00,
            "utilizacao_credito_pct": 70.0,
            "taxa_inadimplencia_30d": 2.45,
            "dso_dias": 42,
            "recuperacao_mes": 1850000.00
        },
        "matriz_risco": [
            {"rating": "AAA / AA (Baixíssimo Risco)", "clientes_cnt": 45, "saldo_brl": 18500000.00, "inadimplencia_esperada": "0.1%", "fill": "#10b981"},
            {"rating": "A (Risco Baixo)", "clientes_cnt": 82, "saldo_brl": 12200000.00, "inadimplencia_esperada": "0.8%", "fill": "#3b82f6"},
            {"rating": "B (Risco Moderado)", "clientes_cnt": 34, "saldo_brl": 5400000.00, "inadimplencia_esperada": "2.5%", "fill": "#f59e0b"},
            {"rating": "C (Risco Elevado)", "clientes_cnt": 12, "saldo_brl": 1800000.00, "inadimplencia_esperada": "8.0%", "fill": "#f97316"},
            {"rating": "D / E (Alto Risco / Crítico)", "clientes_cnt": 5, "saldo_brl": 600000.00, "inadimplencia_esperada": "25.0%", "fill": "#ef4444"}
        ],
        "aging_list": [
            {"faixa": "A Vencer (Adimplente)", "valor": 32100000.00, "pct": 83.37, "fill": "#10b981"},
            {"faixa": "1 a 30 dias de atraso", "valor": 3850000.00, "pct": 10.00, "fill": "#f59e0b"},
            {"faixa": "31 a 60 dias de atraso", "valor": 1450000.00, "pct": 3.76, "fill": "#f97316"},
            {"faixa": "61 a 90 dias de atraso", "valor": 650000.00, "pct": 1.69, "fill": "#ef4444"},
            {"faixa": "> 90 dias (Crítico)", "valor": 450000.00, "pct": 1.17, "fill": "#991b1b"}
        ],
        "regua_cobranca": [
            {"etapa": "Lembrete Pré-Vencimento (D-5)", "contas_cnt": 142, "montante_brl": 8900000.00, "eficiencia_pct": 94.5},
            {"etapa": "Notificação Inicial (D+3)", "contas_cnt": 28, "montante_brl": 2100000.00, "eficiencia_pct": 78.2},
            {"etapa": "Negociação Direta (D+15)", "contas_cnt": 14, "montante_brl": 1250000.00, "eficiencia_pct": 62.0},
            {"etapa": "Notificação Extrajudicial / Serasa (D+30)", "contas_cnt": 8, "montante_brl": 720000.00, "eficiencia_pct": 45.0},
            {"etapa": "Execução Jurídica / Recovery (D+60)", "contas_cnt": 4, "montante_brl": 450000.00, "eficiencia_pct": 22.0}
        ],
        "clientes_criticos": [
            {"cliente": "Distribuidora Varejo Global S.A. (Fictício)", "rating": "D", "limite_concedido": 800000.00, "utilizado": 750000.00, "em_atraso": 320000.00, "dias_atraso": 45, "status_cobranca": "Negociação de Acordo"},
            {"cliente": "Logística & Cargas Brasil Ltda (Fictício)", "rating": "C", "limite_concedido": 500000.00, "utilizado": 480000.00, "em_atraso": 180000.00, "dias_atraso": 62, "status_cobranca": "Notificação Extrajudicial"},
            {"cliente": "Indústria Metalúrgica Sul (Fictício)", "rating": "D", "limite_concedido": 300000.00, "utilizado": 290000.00, "em_atraso": 150000.00, "dias_atraso": 95, "status_cobranca": "Encaminhado p/ Jurídico"},
            {"cliente": "Serviços Digitais Alpha (Fictício)", "rating": "B", "limite_concedido": 600000.00, "utilizado": 420000.00, "em_atraso": 95000.00, "dias_atraso": 18, "status_cobranca": "Lembrete Enviado"},
            {"cliente": "Comércio de Alimentos Express (Fictício)", "rating": "C", "limite_concedido": 400000.00, "utilizado": 380000.00, "em_atraso": 110000.00, "dias_atraso": 38, "status_cobranca": "Segunda Notificação"}
        ]
    }
    
    return {
        "meta": {
            "empresa": "CoreFin Analytics (Fictício)",
            "moeda": "BRL",
            "ultima_atualizacao": "2026-08-08 06:00:00"
        },
        "overview": overview,
        "tesouraria": tesouraria,
        "controladoria": controladoria,
        "fpa": fpa,
        "credito_cobranca": credito_cobranca
    }

def save_data_to_json(filepath: str = "data/finance_corporate_data.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data = generate_corporate_finance_data()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dados financeiros corporativos salvos com sucesso em {filepath}")

if __name__ == "__main__":
    save_data_to_json()
