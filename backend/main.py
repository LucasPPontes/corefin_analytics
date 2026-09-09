from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.finance import router as finance_router

app = FastAPI(
    title="CoreFin Analytics - FastAPI Backend",
    description="API REST de Engenharia de Dados Financeiros e Orquestrador do Pipeline Medalhão (Bronze, Silver, Gold)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(finance_router)

@app.on_event("startup")
def startup_event():
    """Executa o pipeline medalhão ao inicializar a API se o PostgreSQL estiver acessível."""
    try:
        from scripts.run_medallion import run_medallion_pipeline
        run_medallion_pipeline()
    except Exception as e:
        print(f"[FastAPI Startup Notice] Conexão com o banco ainda pendente. {e}")

@app.get("/")
@app.get("/health")
def healthcheck():
    return {
        "status": "online",
        "app": "CoreFin Analytics Backend (FastAPI + PostgreSQL)",
        "version": "2.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, reload=True)
