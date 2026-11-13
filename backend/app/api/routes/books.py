from typing import Any

from fastapi import APIRouter, Path, Query, Request

from app.schemas.books import BookListResponse, BookResponse
from app.services.gutendex import fetch_book_by_id, fetch_books

router = APIRouter(
    prefix="/books",
    tags=["Livros (Gutendex)"],
)


def _forward_query_params(request: Request) -> dict[str, Any]:
    return {key: value for key, value in request.query_params.items()}


@router.get(
    "",
    response_model=BookListResponse,
    summary="Listar / pesquisar livros no Gutendex",
    description=(
        "Consulta o catálogo público do Gutendex e devolve apenas os campos "
        "úteis ao front-end. Parâmetros de query (ex.: `search`, `page`) "
        "são repassados integralmente à API externa."
    ),
    responses={
        503: {"description": "Gutendex indisponível, em timeout ou com erro"},
    },
)
async def list_books(
    request: Request,
    search: str | None = Query(
        default=None,
        description="Texto de busca repassado ao Gutendex (título, autor, etc.)",
    ),
    page: int | None = Query(default=None, ge=1),
) -> BookListResponse:
    params = _forward_query_params(request)
    if search is not None:
        params["search"] = search
    if page is not None:
        params["page"] = page
    return await fetch_books(params=params)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Detalhe de um livro no Gutendex",
    description=(
        "Obtém os detalhes de um livro pelo ID do Project Gutenberg/Gutendex "
        "e devolve o modelo enxuto da plataforma."
    ),
    responses={
        404: {"description": "Livro não encontrado no catálogo externo"},
        503: {"description": "Gutendex indisponível, em timeout ou com erro"},
    },
)
async def get_book(book_id: int = Path(gt=0)) -> BookResponse:
    return await fetch_book_by_id(book_id)
