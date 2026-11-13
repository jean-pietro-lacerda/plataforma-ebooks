from typing import Any, NoReturn

import httpx
from fastapi import HTTPException, status

from app.schemas.books import BookListResponse, BookResponse

GUTENDEX_BASE_URL = "https://gutendex.com"
GUTENDEX_TIMEOUT = httpx.Timeout(60.0, connect=10.0)

_DOWNLOAD_MIME_PREFERENCE = (
    "application/epub+zip",
    "text/html",
    "text/html; charset=utf-8",
)


def _pick_cover_url(formats: dict[str, str]) -> str | None:
    return formats.get("image/jpeg")


def _pick_download_url(formats: dict[str, str]) -> str | None:
    for mime in _DOWNLOAD_MIME_PREFERENCE:
        url = formats.get(mime)
        if url:
            return url

    for mime, url in formats.items():
        if mime.startswith("text/html"):
            return url

    return None


def normalize_book(raw: dict[str, Any]) -> BookResponse:
    if not isinstance(raw, dict) or type(raw.get("id")) is not int or raw["id"] <= 0:
        raise ValueError("Identificador de livro inválido na resposta externa")
    if raw.get("title") is not None and not isinstance(raw["title"], str):
        raise ValueError("Título inválido na resposta externa")
    if raw.get("authors") is not None and not isinstance(raw["authors"], list):
        raise ValueError("Autores inválidos na resposta externa")
    formats = raw.get("formats")
    if formats is None:
        formats = {}
    if not isinstance(formats, dict) or any(
        not isinstance(mime, str) or not isinstance(url, str)
        for mime, url in formats.items()
    ):
        raise ValueError("Formatos inválidos na resposta externa")
    authors = [
        author.get("name", "").strip()
        for author in (raw.get("authors") or [])
        if author.get("name")
    ]

    return BookResponse(
        id=raw["id"],
        titulo=raw.get("title") or "Sem título",
        autores=authors,
        url_capa=_pick_cover_url(formats),
        link_download=_pick_download_url(formats),
        url_pagina_oficial=f"https://www.gutenberg.org/ebooks/{raw['id']}",
    )


def normalize_book_list(raw: dict[str, Any]) -> BookListResponse:
    if (
        type(raw.get("count")) is not int
        or raw["count"] < 0
        or not isinstance(raw.get("results"), list)
    ):
        raise ValueError("Listagem inválida na resposta externa")
    return BookListResponse(
        count=raw["count"],
        next=raw.get("next"),
        previous=raw.get("previous"),
        results=[normalize_book(item) for item in (raw.get("results") or [])],
    )


def _raise_service_unavailable(detail: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=detail,
    )


async def _get_json(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{GUTENDEX_BASE_URL}{path}"

    try:
        async with httpx.AsyncClient(timeout=GUTENDEX_TIMEOUT) as client:
            response = await client.get(url, params=params or None)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("Objeto JSON esperado na resposta externa")
            return data

    except ValueError:
        _raise_service_unavailable("O serviço de livros (Gutendex) retornou uma resposta inválida.")

    except httpx.TimeoutException:
        _raise_service_unavailable(
            "O serviço de livros (Gutendex) demorou demais para responder. "
            "Tente novamente em instantes."
        )

    except httpx.HTTPStatusError as exc:
        upstream_status = exc.response.status_code

        if upstream_status == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Página não encontrada no catálogo externo."
                    if path == "/books/"
                    else "Livro não encontrado no catálogo externo."
                ),
            ) from exc

        if upstream_status == status.HTTP_400_BAD_REQUEST:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parâmetros inválidos para a consulta ao catálogo externo.",
            ) from exc

        _raise_service_unavailable(
            f"O serviço de livros (Gutendex) retornou erro HTTP {upstream_status}."
        )

    except httpx.RequestError:
        _raise_service_unavailable(
            "Não foi possível contactar o serviço de livros (Gutendex). "
            "Verifique a conectividade ou tente mais tarde."
        )


async def fetch_books(params: dict[str, Any] | None = None) -> BookListResponse:
    raw = await _get_json("/books/", params=params)
    try:
        return normalize_book_list(raw)
    except (KeyError, TypeError, AttributeError, ValueError):
        _raise_service_unavailable("O serviço de livros (Gutendex) retornou uma resposta inválida.")


async def fetch_book_by_id(book_id: int) -> BookResponse:
    raw = await _get_json(f"/books/{book_id}/")
    try:
        return normalize_book(raw)
    except (KeyError, TypeError, AttributeError, ValueError):
        _raise_service_unavailable("O serviço de livros (Gutendex) retornou uma resposta inválida.")
