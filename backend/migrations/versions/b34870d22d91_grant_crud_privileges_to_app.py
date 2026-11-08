from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b34870d22d91"
down_revision: Union[str, Sequence[str], None] = "bb40eef3ff09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Permite que a aplicação acesse o schema.
    op.execute("""
        GRANT USAGE ON SCHEMA public TO ebooks_app;
    """)

    # Libera operações CRUD nas tabelas existentes.
    op.execute("""
        GRANT SELECT, INSERT, UPDATE, DELETE
        ON TABLE public.admin, public.noticias
        TO ebooks_app;
    """)

    # Libera a utilização das sequências dos identificadores.
    op.execute("""
        GRANT USAGE, SELECT
        ON SEQUENCE public.admin_id_seq, public.noticias_id_seq
        TO ebooks_app;
    """)

    # Configura permissões para futuras tabelas criadas
    # pelo role ebooks_migrations.
    op.execute("""
        ALTER DEFAULT PRIVILEGES FOR ROLE ebooks_migrations
        IN SCHEMA public
        GRANT SELECT, INSERT, UPDATE, DELETE
        ON TABLES TO ebooks_app;
    """)

    op.execute("""
        ALTER DEFAULT PRIVILEGES FOR ROLE ebooks_migrations
        IN SCHEMA public
        GRANT USAGE, SELECT
        ON SEQUENCES TO ebooks_app;
    """)


def downgrade() -> None:
    # Reverte as permissões padrão.
    op.execute("""
        ALTER DEFAULT PRIVILEGES FOR ROLE ebooks_migrations
        IN SCHEMA public
        REVOKE SELECT, INSERT, UPDATE, DELETE
        ON TABLES FROM ebooks_app;
    """)

    op.execute("""
        ALTER DEFAULT PRIVILEGES FOR ROLE ebooks_migrations
        IN SCHEMA public
        REVOKE USAGE, SELECT
        ON SEQUENCES FROM ebooks_app;
    """)

    # Reverte as permissões das sequências existentes.
    op.execute("""
        REVOKE USAGE, SELECT
        ON SEQUENCE public.admin_id_seq, public.noticias_id_seq
        FROM ebooks_app;
    """)

    # Reverte as permissões das tabelas existentes.
    op.execute("""
        REVOKE SELECT, INSERT, UPDATE, DELETE
        ON TABLE public.admin, public.noticias
        FROM ebooks_app;
    """)

    op.execute("""
        REVOKE USAGE ON SCHEMA public FROM ebooks_app;
    """)