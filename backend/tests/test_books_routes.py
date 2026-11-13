import httpx
import pytest
from fastapi.testclient import TestClient

from app.services import gutendex
from main import app


BOOK = {
    "id": 84,
    "title": "Frankenstein",
    "authors": [{"name": "Mary Shelley"}],
    "formats": {
        "image/jpeg": "https://www.gutenberg.org/cover.jpg",
        "application/epub+zip": "https://www.gutenberg.org/ebooks/84.epub3.images",
    },
}


@pytest.fixture
def upstream(monkeypatch):
    requests = []
    state = {"status": 200, "json": BOOK}
    original_client = httpx.AsyncClient

    def handler(request):
        requests.append(request)
        if "error" in state:
            raise state["error"]("simulated", request=request)
        if "content" in state:
            return httpx.Response(state["status"], content=state["content"])
        return httpx.Response(state["status"], json=state["json"])

    def factory(*args, **kwargs):
        return original_client(*args, **kwargs, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(gutendex.httpx, "AsyncClient", factory)
    return state, requests


@pytest.fixture
def client(upstream):
    with TestClient(app) as test_client:
        yield test_client


def test_list_search_filters_and_pagination(client, upstream):
    state, requests = upstream
    next_url = "https://gutendex.com/books/?page=3&languages=en"
    state["json"] = {
        "count": 65,
        "next": next_url,
        "previous": "https://gutendex.com/books/?page=1&languages=en",
        "results": [BOOK],
    }
    response = client.get("/books?search=Frankenstein&languages=en&topic=fiction&page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 65
    assert data["next"] == next_url
    assert data["previous"] == state["json"]["previous"]
    assert data["results"][0]["titulo"] == "Frankenstein"
    assert data["results"][0]["url_pagina_oficial"] == "https://www.gutenberg.org/ebooks/84"
    assert dict(requests[0].url.params) == {
        "search": "Frankenstein", "languages": "en", "topic": "fiction", "page": "2"
    }


def test_book_details_preserve_existing_fields(client, upstream):
    response = client.get("/books/84")
    assert response.status_code == 200
    assert response.json() == {
        "id": 84,
        "titulo": "Frankenstein",
        "autores": ["Mary Shelley"],
        "url_capa": BOOK["formats"]["image/jpeg"],
        "link_download": BOOK["formats"]["application/epub+zip"],
        "url_pagina_oficial": "https://www.gutenberg.org/ebooks/84",
    }
    assert upstream[1][0].url.path == "/books/84/"


def test_optional_null_fields(client, upstream):
    upstream[0]["json"] = {"id": 84, "title": None, "authors": None, "formats": None}
    response = client.get("/books/84")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Sem título"
    assert response.json()["autores"] == []
    assert response.json()["link_download"] is None


def test_empty_list(client, upstream):
    upstream[0]["json"] = {"count": 0, "results": []}
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {"count": 0, "next": None, "previous": None, "results": []}


@pytest.mark.parametrize("path", [
    "/books/0", "/books/-1", "/books/abc",
    "/books?page=0", "/books?page=-1", "/books?page=abc", "/books?page=1.5",
])
def test_invalid_parameters_do_not_call_upstream(client, upstream, path):
    assert client.get(path).status_code == 422
    assert upstream[1] == []


@pytest.mark.parametrize("path,payload", [
    ("/books", []),
    ("/books", {}),
    ("/books", {"count": None, "results": []}),
    ("/books", {"count": -1, "results": []}),
    ("/books", {"count": 1, "results": {"id": 84}}),
    ("/books", {"count": 1, "results": [None]}),
    ("/books", {"count": 1, "results": [BOOK], "next": []}),
    ("/books/84", {}),
    ("/books/84", {**BOOK, "id": -1}),
    ("/books/84", {**BOOK, "title": []}),
    ("/books/84", {**BOOK, "authors": [None]}),
    ("/books/84", {**BOOK, "authors": {}}),
    ("/books/84", {**BOOK, "formats": []}),
    ("/books/84", {**BOOK, "formats": {"application/epub+zip": 123}}),
])
def test_invalid_upstream_payload_is_controlled(client, upstream, path, payload):
    upstream[0]["json"] = payload
    response = client.get(path)
    assert response.status_code == 503
    assert "resposta inválida" in response.json()["detail"]


@pytest.mark.parametrize("path", ["/books", "/books/84"])
def test_non_json_response_is_controlled(client, upstream, path):
    upstream[0]["content"] = b"<html>invalid response</html>"
    assert client.get(path).status_code == 503


@pytest.mark.parametrize("path,status,expected,detail", [
    ("/books/84", 404, 404, "Livro não encontrado"),
    ("/books?page=9999", 404, 404, "Página não encontrada"),
    ("/books?ids=abc", 400, 400, "Parâmetros inválidos"),
    ("/books", 429, 503, "HTTP 429"),
    ("/books", 500, 503, "HTTP 500"),
])
def test_upstream_http_errors(client, upstream, path, status, expected, detail):
    upstream[0]["status"] = status
    response = client.get(path)
    assert response.status_code == expected
    assert detail in response.json()["detail"]


@pytest.mark.parametrize("error", [httpx.ReadTimeout, httpx.ConnectError])
def test_network_errors(client, upstream, error):
    upstream[0]["error"] = error
    assert client.get("/books").status_code == 503


@pytest.mark.parametrize("origin", ["http://localhost:5173", "http://127.0.0.1:5173"])
def test_local_frontend_cors(client, origin):
    headers = {"Origin": origin, "Access-Control-Request-Method": "GET"}
    response = client.options("/books", headers=headers)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    response = client.get("/books/84", headers={"Origin": origin})
    assert response.headers["access-control-allow-origin"] == origin


def test_unknown_origin_is_not_allowed(client):
    response = client.options("/books", headers={
        "Origin": "https://unknown.example", "Access-Control-Request-Method": "GET"
    })
    assert "access-control-allow-origin" not in response.headers
