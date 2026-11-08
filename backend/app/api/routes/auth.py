from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.models.admin import Admin
from app.schemas.auth import (
    AdminResponse,
    LoginRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    statement = select(Admin).where(
        Admin.usuario == credentials.usuario
    )

    admin = db.scalar(statement)

    if admin is None or not verify_password(
        credentials.senha,
        admin.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=str(admin.id)
    )

    return TokenResponse(
        access_token=access_token
    )


@router.get("/me", response_model=AdminResponse)
def read_current_admin(
    current_admin: Admin = Depends(get_current_admin),
):
    return current_admin