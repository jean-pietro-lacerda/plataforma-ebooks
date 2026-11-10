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
    formats = raw.get("formats") or {}
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
    )


def normalize_book_list(raw: dict[str, Any]) -> BookListResponse:
    return BookListResponse(
        count=raw.get("count", 0),
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
            return response.json()

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
                detail="Livro não encontrado no catálogo externo.",
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
    return normalize_book_list(raw)


async def fetch_book_by_id(book_id: int) -> BookResponse:
    raw = await _get_json(f"/books/{book_id}/")
    return normalize_book(raw)
