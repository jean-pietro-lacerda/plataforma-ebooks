# Resposta integral — rodada 1

## tests/conftest.py

```python
"""Infraestrutura isolada do Sprint 3: SQLite em memoria e Gutendex bloqueado por mock."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["MIGRATIONS_DATABASE_URL"] = ""
os.environ["JWT_SECRET_KEY"] = "sprint3-test-only-secret-not-for-production"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from app.db.base import Base
from app.db.database import get_db
from app.models.admin import Admin
from app.models.news import Noticia
from app.core.security import create_access_token

BOOK = {"id": 84, "title": "Frankenstein", "authors": [{"name": "Mary Shelley"}],
        "formats": {"image/jpeg": "https://example.invalid/cover.jpg",
                    "application/epub+zip": "https://example.invalid/book.epub"}}

@pytest.fixture
def upstream(monkeypatch):
    state = {"status": 200, "json": BOOK, "requests": []}
    original = httpx.AsyncClient
    def handle(request):
        state["requests"].append(request)
        if "error" in state:
            raise state["error"]("simulated", request=request)
        if "content" in state:
            return httpx.Response(state["status"], content=state["content"])
        return httpx.Response(state["status"], json=state["json"])
    def factory(*args, **kwargs):
        return original(*args, **kwargs, transport=httpx.MockTransport(handle))
    monkeypatch.setattr(httpx, "AsyncClient", factory)
    return state

@pytest.fixture
def api(upstream):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    sessions = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    with sessions() as db:
        db.add(Admin(id=1, usuario="sprint-admin", senha_hash="not-used-by-these-tests"))
        db.commit()
    def database():
        with sessions() as db:
            yield db
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = database
    try:
        with TestClient(app) as client:
            yield client, {"Authorization": "Bearer " + create_access_token("1")}, sessions
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()

def seed_news(sessions, **values):
    payload = {"titulo": "Noticia", "conteudo": "Conteudo", "publicada": False, "destaque": False, "ordem": 0, **values}
    with sessions() as db:
        row = Noticia(**payload)
        db.add(row)
        db.commit()
        return row.id
```

## tests/v1-llm/test_stories.py

```python
"""Resposta LLM rodada 1. Preservar sem edicoes; requisitos e tecnicas em cada teste."""
import pytest
from conftest import BOOK, seed_news

# Requisito CA-01.1; tecnica: particao de equivalencia (busca textual valida).
def test_search_normalized(api, upstream):
    client, _, _ = api
    upstream["json"] = {"count": 1, "next": None, "previous": None, "results": [BOOK]}
    response = client.get("/books?search=Frankenstein")
    assert response.status_code == 200
    assert set(response.json()) == {"count", "next", "previous", "results"}
    assert response.json()["results"][0]["titulo"] == "Frankenstein"
    assert dict(upstream["requests"][0].url.params)["search"] == "Frankenstein"

# Requisito CA-01.2; tecnica: valores-limite (0 e 1).
@pytest.mark.parametrize("page,status", [(0, 422), (1, 200)])
def test_book_page_boundary(api, upstream, page, status):
    upstream["json"] = {"count": 0, "results": []}
    response = api[0].get(f"/books?page={page}")
    assert response.status_code == status

# Requisito CA-01.3; tecnica: valores-limite (ID 0 e 1).
@pytest.mark.parametrize("identifier,status", [(0, 422), (1, 200)])
def test_book_id_boundary(api, upstream, identifier, status):
    upstream["json"] = {**BOOK, "id": identifier}
    response = api[0].get(f"/books/{identifier}")
    assert response.status_code == status
    if status == 200:
        assert response.json()["id"] == identifier

# Requisitos CA-01.3 e CA-01.4; tecnica: particoes (ausente e indisponivel).
@pytest.mark.parametrize("upstream_status,status", [(404, 404), (503, 503)])
def test_external_errors(api, upstream, upstream_status, status):
    upstream["status"] = upstream_status
    response = api[0].get("/books/84")
    assert response.status_code == status

# Requisito CA-01.4; tecnica: particao de equivalencia (links presentes).
def test_digital_links(api):
    result = api[0].get("/books/84")
    assert result.json()["link_download"] == BOOK["formats"]["application/epub+zip"]
    assert result.json()["url_pagina_oficial"] == "https://www.gutenberg.org/ebooks/84"

# Requisito CA-02.1; tecnica: tabela de decisao (publicada e rascunho).
def test_public_list_filters_drafts(api):
    public = seed_news(api[2], publicada=True)
    seed_news(api[2], publicada=False)
    response = api[0].get("/news")
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [public]

# Requisito CA-02.2; tecnica: particoes (rascunho e inexistente).
@pytest.mark.parametrize("exists", [True, False])
def test_public_detail_hidden(api, exists):
    identifier = seed_news(api[2]) if exists else 99999
    assert api[0].get(f"/news/{identifier}").status_code == 404

# Requisito CA-02.3; tecnica: tabela de decisao e ordenacao.
def test_highlight_order(api):
    b = seed_news(api[2], publicada=True, destaque=True, ordem=2)
    a = seed_news(api[2], publicada=True, destaque=True, ordem=1)
    seed_news(api[2], publicada=False, destaque=True, ordem=0)
    assert [item["id"] for item in api[0].get("/news/highlights").json()] == [a, b]

# Requisito CA-02.4; tecnica: valores-limite de offset e limit.
@pytest.mark.parametrize("offset,limit,status", [(-1, 10, 422), (0, 1, 200), (0, 101, 422)])
def test_news_pagination_bounds(api, offset, limit, status):
    assert api[0].get(f"/news?offset={offset}&limit={limit}").status_code == status

# Requisito CA-03.1; tecnica: particao invalida (ausencia de token).
def test_admin_requires_token(api):
    assert api[0].post("/news", json={"titulo": "T", "conteudo": "C"}).status_code == 401

# Requisito CA-03.2; tecnica: valores-limite do titulo (0, 1, 255, 256).
@pytest.mark.parametrize("length,status", [(0, 422), (1, 201), (255, 201), (256, 422)])
def test_title_length(api, length, status):
    response = api[0].post("/news", headers=api[1], json={"titulo": "T" * length, "conteudo": "C"})
    assert response.status_code == status
    if status == 201:
        assert response.json()["publicada"] is False

# Requisito CA-03.2; tecnica: particoes invalidas (conteudo vazio, ordem negativa).
@pytest.mark.parametrize("patch", [{"conteudo": ""}, {"ordem": -1}])
def test_invalid_news_fields(api, patch):
    body = {"titulo": "T", "conteudo": "C", **patch}
    assert api[0].post("/news", headers=api[1], json=body).status_code == 422

# Requisito CA-03.3; tecnica: transicao de estados (rascunho/publicada/rascunho).
def test_publish_and_unpublish(api):
    identifier = seed_news(api[2])
    assert api[0].get(f"/news/{identifier}").status_code == 404
    for published, status in [(True, 200), (False, 404)]:
        result = api[0].patch(f"/news/{identifier}", headers=api[1], json={"publicada": published})
        assert result.status_code == 200
        assert api[0].get(f"/news/{identifier}").status_code == status

# Requisito CA-03.3; tecnica: particao invalida (campo explicitamente nulo).
def test_update_null(api):
    identifier = seed_news(api[2])
    assert api[0].patch(f"/news/{identifier}", headers=api[1], json={"titulo": None}).status_code == 422

# Requisito CA-03.4; tecnica: particoes (existente e inexistente).
def test_delete_news(api):
    identifier = seed_news(api[2])
    result = api[0].delete(f"/news/{identifier}", headers=api[1])
    assert result.status_code == 204
    assert result.content == b""
    assert api[0].get(f"/news/{identifier}").status_code == 404
    assert api[0].delete("/news/99999", headers=api[1]).status_code == 404
```
