from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class NewsCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    conteudo: str = Field(min_length=1)
    publicada: bool = False
    destaque: bool = False
    ordem: int = Field(default=0, ge=0)


class NewsUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=255)
    conteudo: str | None = Field(default=None, min_length=1)
    publicada: bool | None = None
    destaque: bool | None = None
    ordem: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def reject_null_fields(self):
        if any(getattr(self, name) is None for name in self.model_fields_set):
            raise ValueError("Os campos enviados não podem ser nulos")
        return self


class NewsResponse(NewsCreate):
    id: int
    imagem_path: str | None
    data_publicacao: datetime | None

    model_config = ConfigDict(from_attributes=True)
