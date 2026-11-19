import httpx
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
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


# Lacuna CT-01-02 / CA-01.1: particao busca ausente; oraculo de contrato e encaminhamento.
def test_search_absent_v2(api, upstream):
    upstream["json"] = {"count": 0, "next": None, "previous": None, "results": []}
    response = api[0].get("/books")
    assert response.json() == {"count": 0, "next": None, "previous": None, "results": []}
    assert dict(upstream["requests"][0].url.params) == {}

# Lacunas CT-02-07/08 e DT-03: limites completos, oraculo quantitativo e admin.
@pytest.mark.parametrize("path", ["/news", "/news/admin"])
@pytest.mark.parametrize("limit,status", [(0, 422), (1, 200), (100, 200), (101, 422)])
def test_full_limit_boundaries_v2(api, path, limit, status):
    for i in range(3):
        seed_news(api[2], publicada=True, titulo=str(i))
    response = api[0].get(path + f"?limit={limit}", headers=api[1])
    assert response.status_code == status
    if status == 200:
        assert len(response.json()) == min(3, limit)

# Lacuna CT-02-04: tabela de decisao completa das flags, incluindo false/false e true/false.
def test_all_highlight_flags_v2(api):
    expected = []
    for published, highlighted in [(False, False), (False, True), (True, False), (True, True)]:
        identifier = seed_news(api[2], publicada=published, destaque=highlighted)
        if published and highlighted:
            expected.append(identifier)
    assert [row["id"] for row in api[0].get("/news/highlights").json()] == expected

# Lacuna CT-02-02: oraculo de dados da noticia publicada.
def test_public_detail_content_v2(api):
    identifier = seed_news(api[2], publicada=True, titulo="Publica", conteudo="Texto")
    result = api[0].get(f"/news/{identifier}")
    assert result.status_code == 200
    assert result.json()["id"] == identifier
    assert result.json()["titulo"] == "Publica"
    assert result.json()["conteudo"] == "Texto"

# Lacuna CT-03-07: ordem 0 explicitamente enviada; limite inferior valido.
def test_explicit_zero_order_v2(api):
    result = api[0].post("/news", headers=api[1], json={"titulo": "T", "conteudo": "C", "ordem": 0})
    assert result.status_code == 201
    assert result.json()["ordem"] == 0
    assert result.json()["publicada"] is False

# CA-01.4: particoes de formatos e defaults; caracterizacao antes de DT-01.
@pytest.mark.parametrize("formats,expected", [
    (None, None), ({}, None),
    ({"text/html": "https://example.invalid/a"}, "https://example.invalid/a"),
    ({"text/html; charset=utf-8": "https://example.invalid/b"}, "https://example.invalid/b"),
    ({"text/html; charset=iso-8859-1": "https://example.invalid/c"}, "https://example.invalid/c"),
])
def test_link_partitions_v2(api, upstream, formats, expected):
    upstream["json"] = {**BOOK, "title": None, "authors": None, "formats": formats}
    result = api[0].get("/books/84")
    assert result.status_code == 200
    assert result.json()["link_download"] == expected
    assert result.json()["titulo"] == "Sem título"
    assert result.json()["autores"] == []

# CA-01.4: resposta externa invalida; preservacao de erro e oraculo antes de DT-01/02.
@pytest.mark.parametrize("payload", [
    {}, {"id": 0}, {**BOOK, "title": []}, {**BOOK, "authors": {}},
    {**BOOK, "formats": []}, {**BOOK, "formats": {"text/html": 4}},
    {**BOOK, "authors": [None]},
])
def test_invalid_upstream_book_v2(api, upstream, payload):
    upstream["json"] = payload
    response = api[0].get("/books/84")
    assert response.status_code == 503
    assert "resposta inválida" in response.json()["detail"]

# CA-01.4: falhas de transporte distintas, sem rede real.
@pytest.mark.parametrize("error", [httpx.ReadTimeout, httpx.ConnectError])
def test_transport_error_v2(api, upstream, error):
    upstream["error"] = error
    assert api[0].get("/books/84").status_code == 503

# CA-01.4: resposta nao JSON e objeto de tipo incorreto.
@pytest.mark.parametrize("content", [b"<html>error</html>", b"[]"])
def test_invalid_json_v2(api, upstream, content):
    upstream["content"] = content
    response = api[0].get("/books/84")
    assert response.status_code == 503
    assert "resposta inválida" in response.json()["detail"]

# CA-01.4: erros HTTP distintos, caracterizacao do mapeamento existente.
@pytest.mark.parametrize("status,expected", [(400, 400), (429, 503), (500, 503)])
def test_http_status_mapping_v2(api, upstream, status, expected):
    upstream["status"] = status
    assert api[0].get("/books/84").status_code == expected

# CA-01.1: particoes invalidas da lista; defaults next/previous.
@pytest.mark.parametrize("payload", [
    [], {}, {"count": -1, "results": []}, {"count": 1, "results": {}},
    {"count": 1, "results": [None]}, {"count": 0, "results": [], "next": []},
])
def test_invalid_list_v2(api, upstream, payload):
    upstream["json"] = payload
    response = api[0].get("/books")
    assert response.status_code == 503
    assert "resposta inválida" in response.json()["detail"]

# CA-01.2/03: tipo nao inteiro e inferior negativo, sem chamar upstream.
@pytest.mark.parametrize("path", ["/books?page=-1", "/books?page=abc", "/books/-1", "/books/abc"])
def test_rejected_identifiers_v2(api, upstream, path):
    assert api[0].get(path).status_code == 422
    assert upstream["requests"] == []

# CA-03.1: particoes adicionais de autenticacao.
@pytest.mark.parametrize("subject,expired", [("1", True), ("missing", False), ("999", False)])
def test_invalid_sessions_v2(api, subject, expired):
    token = jwt.encode({"sub": subject, "exp": datetime.now(timezone.utc) + timedelta(minutes=-1 if expired else 1)},
                       settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    assert api[0].get("/news/admin", headers={"Authorization": "Bearer " + token}).status_code == 401

# CA-03.1: formato/token invalido.
@pytest.mark.parametrize("header", ["Basic test", "Bearer invalid"])
def test_invalid_token_v2(api, header):
    assert api[0].get("/news/admin", headers={"Authorization": header}).status_code == 401

# CA-03.3: particao nula para cada campo, sem mutacao persistida.
@pytest.mark.parametrize("field", ["titulo", "conteudo", "publicada", "destaque", "ordem"])
def test_all_null_updates_v2(api, field):
    identifier = seed_news(api[2], titulo="Original")
    assert api[0].patch(f"/news/{identifier}", headers=api[1], json={field: None}).status_code == 422
    assert api[0].get(f"/news/admin/{identifier}", headers=api[1]).json()["titulo"] == "Original"

# CA-02.4: offset seleciona itens e ordenacao deterministica.
def test_offset_selects_items_v2(api):
    a = seed_news(api[2], publicada=True)
    b = seed_news(api[2], publicada=True)
    assert [r["id"] for r in api[0].get("/news?offset=1&limit=1").json()] == [a]
    assert api[0].get(f"/news/admin/{b}", headers=api[1]).json()["id"] == b

# CA-03.3: editar sem republicar preserva data; erro para inexistente.
def test_update_state_invariants_v2(api):
    identifier = seed_news(api[2])
    first = api[0].patch(f"/news/{identifier}", headers=api[1], json={"publicada": True}).json()
    second = api[0].patch(f"/news/{identifier}", headers=api[1], json={"titulo": "Alterada"}).json()
    assert first["data_publicacao"] is not None
    assert second["data_publicacao"] == first["data_publicacao"]
    assert second["titulo"] == "Alterada"
    assert api[0].patch("/news/99999", headers=api[1], json={"titulo": "X"}).status_code == 404
