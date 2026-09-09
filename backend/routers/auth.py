from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter(prefix="/api/auth", tags=["Autenticação & RBAC"])

# Banco de dados fictício de usuários corporativos e permissões RBAC
USERS_DB = {
    "diretor@corefin.com": {
        "email": "diretor@corefin.com",
        "name": "Carlos Silva (Fictício)",
        "password": "123",
        "role": "DIRETOR",
        "role_name": "C-Level / Diretor",
        "permissions": ["VISAO_GERAL", "TESOURARIA", "CONTROLADORIA", "FPA", "CREDITO"],
        "avatar": "bi-person-badge-fill"
    },
    "gerente@corefin.com": {
        "email": "gerente@corefin.com",
        "name": "Ana Oliveira (Fictício)",
        "password": "123",
        "role": "GERENTE",
        "role_name": "Gerente Financeiro",
        "permissions": ["VISAO_GERAL", "TESOURARIA", "CONTROLADORIA_SEM_DRE", "FPA", "CREDITO"],
        "avatar": "bi-person-workspace"
    },
    "tesouraria@corefin.com": {
        "email": "tesouraria@corefin.com",
        "name": "Mariana Santos (Fictício)",
        "password": "123",
        "role": "TESOURARIA",
        "role_name": "Analista de Tesouraria",
        "permissions": ["TESOURARIA"],
        "avatar": "bi-cash-coin"
    },
    "auditor@corefin.com": {
        "email": "auditor@corefin.com",
        "name": "Roberto Lima (Fictício)",
        "password": "123",
        "role": "AUDITOR",
        "role_name": "Auditor Fiscal",
        "permissions": ["CONTROLADORIA"],
        "avatar": "bi-journal-check"
    }
}

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    status: str
    token: str
    user: Dict

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    email = credentials.email.strip().lower()
    user = USERS_DB.get(email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    
    return {
        "status": "success",
        "token": f"jwt_token_{user['role'].lower()}_2026",
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "role_name": user["role_name"],
            "permissions": user["permissions"],
            "avatar": user["avatar"]
        }
    }

@router.get("/users")
def get_demo_users():
    """Retorna a lista de perfis cadastrados para demonstração do RBAC."""
    return [
        {
            "email": u["email"],
            "name": u["name"],
            "role": u["role"],
            "role_name": u["role_name"],
            "permissions": u["permissions"]
        }
        for u in USERS_DB.values()
    ]
