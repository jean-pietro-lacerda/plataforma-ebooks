from getpass import getpass

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models.admin import Admin


def main():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL não configurada.")

    usuario = input("Usuário do administrador: ").strip()

    if not usuario or len(usuario) > 100:
        raise ValueError("Usuário inválido.")

    senha = getpass("Senha (mínimo 12 caracteres): ")
    confirmacao = getpass("Confirme a senha: ")

    if len(senha) < 12 or len(senha) > 128:
        raise ValueError("A senha deve ter entre 12 e 128 caracteres.")

    if senha != confirmacao:
        raise ValueError("As senhas não são iguais.")

    with SessionLocal() as db:
        quantidade = db.scalar(
            select(func.count()).select_from(Admin)
        )

        if quantidade:
            print("Já existe um administrador. Operação cancelada.")
            return

        administrador = Admin(
            usuario=usuario,
            senha_hash=hash_password(senha),
        )

        db.add(administrador)

        try:
            db.commit()
            db.refresh(administrador)
        except SQLAlchemyError:
            db.rollback()
            raise

        print(f"Administrador criado com sucesso. ID: {administrador.id}")


if __name__ == "__main__":
    main()