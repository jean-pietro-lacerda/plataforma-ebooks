from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, false
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Noticia(Base):
    __tablename__ = "noticias"

    id: Mapped[int] = mapped_column(primary_key=True)

    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    conteudo: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    imagem_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    publicada: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False
    )

    destaque: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False
    )

    ordem: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
        nullable=False
    )

    data_publicacao: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
