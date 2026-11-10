from pydantic import BaseModel, Field


class BookResponse(BaseModel):
    id: int = Field(description="Identificador do livro no Gutendex/Project Gutenberg")
    titulo: str = Field(description="Título do livro")
    autores: list[str] = Field(
        default_factory=list,
        description="Lista com os nomes dos autores",
    )
    url_capa: str | None = Field(
        default=None,
        description="URL da capa em image/jpeg, quando disponível",
    )
    link_download: str | None = Field(
        default=None,
        description="Link de download preferencial (EPUB ou HTML)",
    )


class BookListResponse(BaseModel):
    count: int = Field(description="Total de livros encontrados na consulta")
    next: str | None = Field(
        default=None,
        description="URL da próxima página no Gutendex (se houver)",
    )
    previous: str | None = Field(
        default=None,
        description="URL da página anterior no Gutendex (se houver)",
    )
    results: list[BookResponse] = Field(
        default_factory=list,
        description="Lista de livros já normalizados para o front-end",
    )
