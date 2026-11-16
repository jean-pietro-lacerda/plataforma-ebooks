from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.database import get_db
from app.models.admin import Admin
from app.models.news import Noticia

@pytest.fixture(scope="session")
def admin_hash():
    return hash_password("TemporaryTest123!")

@pytest.fixture
def api(tmp_path, monkeypatch, admin_hash):
    monkeypatch.setattr(settings, "jwt_secret_key", "temporary-validation-secret-with-at-least-32-bytes")
    monkeypatch.setattr(settings, "news_upload_dir", str(tmp_path / "uploads"))
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with factory() as session:
        session.add(Admin(usuario="qa-admin", senha_hash=admin_hash))
        session.commit()

    def database():
        with factory() as session:
            yield session

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = database
    try:
        with TestClient(app) as client:
            result = client.post("/auth/login", json={"usuario": "qa-admin", "senha": "TemporaryTest123!"})
            assert result.status_code == 200
            yield {
                "client": client,
                "headers": {"Authorization": "Bearer " + result.json()["access_token"]},
                "factory": factory,
                "uploads": Path(settings.news_upload_dir),
            }
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        Base.metadata.drop_all(engine)
        engine.dispose()

def create(api, **values):
    payload = {"titulo": "Noticia de teste", "conteudo": "Conteudo de teste", **values}
    result = api["client"].post("/news", headers=api["headers"], json=payload)
    assert result.status_code == 201, result.text
    return result.json()

def image_bytes(fmt="PNG"):
    data = BytesIO()
    Image.new("RGB", (8, 8), (66, 118, 137)).save(data, format=fmt)
    return data.getvalue()

@pytest.mark.parametrize("method,path", [
    ("get", "/news/admin"), ("get", "/news/admin/1"),
    ("post", "/news"), ("patch", "/news/1"),
    ("delete", "/news/1"), ("post", "/news/1/image"),
])
def test_admin_endpoints_require_authentication(api, method, path):
    assert getattr(api["client"], method)(path).status_code == 401

@pytest.mark.parametrize("authorization", ["Bearer invalid", "Basic invalid", "Bearer"])
def test_invalid_authorization_is_rejected(api, authorization):
    result = api["client"].get("/news/admin", headers={"Authorization": authorization})
    assert result.status_code == 401

def test_news_lifecycle_publication_and_visibility(api):
    client, headers = api["client"], api["headers"]
    draft = create(api)
    item_id = draft["id"]
    assert draft["publicada"] is False and draft["data_publicacao"] is None
    assert draft["imagem_path"] is None
    assert client.get("/news").json() == []
    assert client.get("/news/highlights").json() == []
    assert client.get(f"/news/{item_id}").status_code == 404
    assert client.get("/news/admin", headers=headers).json()[0]["id"] == item_id
    assert client.get(f"/news/admin/{item_id}", headers=headers).status_code == 200
    published = client.patch(f"/news/{item_id}", headers=headers, json={"publicada": True, "destaque": True}).json()
    assert published["data_publicacao"]
    assert client.get(f"/news/{item_id}").status_code == 200
    assert client.get("/news/highlights").json()[0]["id"] == item_id
    result = client.patch(f"/news/{item_id}", headers=headers, json={"publicada": False})
    assert result.status_code == 200
    assert client.get(f"/news/{item_id}").status_code == 404
    assert client.get("/news/highlights").json() == []
    result = client.patch(f"/news/{item_id}", headers=headers, json={"publicada": True})
    assert result.json()["data_publicacao"] == published["data_publicacao"]
    result = client.delete(f"/news/{item_id}", headers=headers)
    assert result.status_code == 204 and result.content == b""
    assert client.get(f"/news/admin/{item_id}", headers=headers).status_code == 404

def test_pagination_and_highlights_order(api):
    a = create(api, titulo="A", publicada=True, destaque=True, ordem=2)
    b = create(api, titulo="B", publicada=True, destaque=True, ordem=1)
    c = create(api, titulo="C", publicada=True, destaque=True, ordem=1)
    draft = create(api, titulo="Draft", destaque=True, ordem=0)
    assert [x["id"] for x in api["client"].get("/news/highlights").json()] == [b["id"], c["id"], a["id"]]
    listing = api["client"].get("/news").json()
    assert [x["id"] for x in listing] == [c["id"], b["id"], a["id"]]
    assert api["client"].get("/news?offset=1&limit=1").json()[0]["id"] == b["id"]
    assert api["client"].get("/news/admin?limit=1", headers=api["headers"]).json()[0]["id"] == draft["id"]

@pytest.mark.parametrize("query", ["offset=-1", "limit=0", "limit=101", "offset=abc"])
def test_invalid_pagination(api, query):
    assert api["client"].get("/news?" + query).status_code == 422

@pytest.mark.parametrize("payload", [
    {"titulo": ""}, {"titulo": "x" * 256}, {"titulo": None},
    {"conteudo": ""}, {"ordem": -1}, {"ordem": None},
])
def test_invalid_create_payload(api, payload):
    body = {"titulo": "Teste", "conteudo": "Conteudo", **payload}
    result = api["client"].post("/news", headers=api["headers"], json=body)
    assert result.status_code == 422
    assert api["client"].get("/news/admin", headers=api["headers"]).json() == []

@pytest.mark.parametrize("field", ["titulo", "conteudo", "publicada", "destaque", "ordem"])
def test_update_rejects_explicit_null(api, field):
    item = create(api)
    result = api["client"].patch(f"/news/{item['id']}", headers=api["headers"], json={field: None})
    assert result.status_code == 422
    assert api["client"].get(f"/news/admin/{item['id']}", headers=api["headers"]).json()["titulo"] == item["titulo"]

@pytest.mark.parametrize("fmt,mime", [("PNG", "image/png"), ("JPEG", "image/jpeg"), ("WEBP", "image/webp")])
def test_valid_image_upload_delivery_replacement_and_deletion(api, fmt, mime):
    item = create(api)
    data = image_bytes(fmt)
    path = f"/news/{item['id']}"
    result = api["client"].post(path + "/image", headers=api["headers"], files={"file": ("../../untrusted-name", data, mime)})
    assert result.status_code == 200, result.text
    filename = result.json()["imagem_path"]
    assert Path(filename).name == filename
    assert (api["uploads"] / filename).read_bytes() == data
    assert api["client"].get(path + "/image").status_code == 404
    assert api["client"].patch(path, headers=api["headers"], json={"publicada": True}).status_code == 200
    response = api["client"].get(path + "/image")
    assert response.status_code == 200 and response.content == data
    assert response.headers["content-type"].startswith(mime)
    assert response.headers["x-content-type-options"] == "nosniff"
    replacement = api["client"].post(path + "/image", headers=api["headers"], files={"file": ("replacement", data, mime)})
    assert replacement.status_code == 200 and replacement.json()["imagem_path"] != filename
    assert (api["uploads"] / filename).exists()
    assert api["client"].delete(path, headers=api["headers"]).status_code == 204
    assert api["client"].get(path + "/image").status_code == 404

@pytest.mark.parametrize("mime,data,expected", [
    ("text/plain", b"not an image", 415),
    ("image/png", b"not an image", 415),
    ("image/jpeg", image_bytes("PNG"), 415),
    ("image/png", b"x" * (5 * 1024 * 1024 + 1), 413),
])
def test_invalid_upload_does_not_write_files(api, mime, data, expected):
    item = create(api)
    result = api["client"].post(f"/news/{item['id']}/image", headers=api["headers"], files={"file": ("invalid", data, mime)})
    assert result.status_code == expected, result.text
    assert list(api["uploads"].glob("*")) == []
    assert api["client"].get(f"/news/admin/{item['id']}", headers=api["headers"]).json()["imagem_path"] is None

def test_failed_image_commit_rolls_back_and_removes_new_file(api, monkeypatch):
    item = create(api)
    def fail_commit(self):
        raise RuntimeError("simulated database failure")
    with monkeypatch.context() as patch:
        patch.setattr(Session, "commit", fail_commit)
        with pytest.raises(RuntimeError, match="simulated database failure"):
            api["client"].post(f"/news/{item['id']}/image", headers=api["headers"], files={"file": ("valid.png", image_bytes(), "image/png")})
    assert list(api["uploads"].glob("*")) == []
    with api["factory"]() as session:
        assert session.get(Noticia, item["id"]).imagem_path is None

def test_image_path_traversal_is_rejected(api, tmp_path):
    item = create(api, publicada=True)
    (tmp_path / "outside.png").write_bytes(image_bytes())
    with api["factory"]() as session:
        news = session.get(Noticia, item["id"])
        news.imagem_path = "../outside.png"
        session.commit()
    assert api["client"].get(f"/news/{item['id']}/image").status_code == 404

@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_cors_for_existing_local_frontend(api, method):
    result = api["client"].options("/news", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": method,
        "Access-Control-Request-Headers": "authorization,content-type",
    })
    assert result.status_code == 200
    assert result.headers["access-control-allow-origin"] == "http://localhost:5173"

def test_unknown_origin_is_not_allowed(api):
    result = api["client"].options("/news", headers={
        "Origin": "https://unknown.example",
        "Access-Control-Request-Method": "POST",
    })
    assert "access-control-allow-origin" not in result.headers

def test_app_initialization_and_openapi(api):
    assert api["client"].get("/health").json() == {"status": "ok"}
    schema = api["client"].get("/openapi.json")
    assert schema.status_code == 200
    expected = {"/auth/login", "/auth/me", "/books", "/books/{book_id}", "/news", "/news/highlights", "/news/admin", "/news/{news_id}/image"}
    assert expected <= set(schema.json()["paths"])
