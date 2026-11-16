from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.core.config import settings
from app.db.database import get_db
from app.models.news import Noticia
from app.schemas.news import NewsCreate, NewsResponse, NewsUpdate
from app.services.news import apply_news_changes, save_image

router = APIRouter(prefix="/news", tags=["Notícias"])
admin_only = [Depends(get_current_admin)]


def find_news(db, news_id, public=False):
    news = db.get(Noticia, news_id)
    if news is None or (public and not news.publicada):
        raise HTTPException(404, "Notícia não encontrada")
    return news


@router.get("", response_model=list[NewsResponse])
def list_news(db: Session = Depends(get_db), offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)):
    return db.scalars(select(Noticia).where(Noticia.publicada.is_(True)).order_by(Noticia.data_publicacao.desc(), Noticia.id.desc()).offset(offset).limit(limit)).all()


@router.get("/highlights", response_model=list[NewsResponse])
def list_highlights(db: Session = Depends(get_db)):
    return db.scalars(select(Noticia).where(Noticia.publicada.is_(True), Noticia.destaque.is_(True)).order_by(Noticia.ordem, Noticia.id)).all()


@router.get("/admin", response_model=list[NewsResponse], dependencies=admin_only)
def list_admin_news(db: Session = Depends(get_db), offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)):
    return db.scalars(select(Noticia).order_by(Noticia.id.desc()).offset(offset).limit(limit)).all()


@router.get("/admin/{news_id}", response_model=NewsResponse, dependencies=admin_only)
def get_admin_news(news_id: int, db: Session = Depends(get_db)):
    return find_news(db, news_id)


@router.get("/{news_id}", response_model=NewsResponse)
def get_news(news_id: int, db: Session = Depends(get_db)):
    return find_news(db, news_id, public=True)


@router.post("", response_model=NewsResponse, status_code=201, dependencies=admin_only)
def create_news(payload: NewsCreate, db: Session = Depends(get_db)):
    news = Noticia()
    apply_news_changes(news, payload.model_dump())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


@router.patch("/{news_id}", response_model=NewsResponse, dependencies=admin_only)
def update_news(news_id: int, payload: NewsUpdate, db: Session = Depends(get_db)):
    news = find_news(db, news_id)
    apply_news_changes(news, payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(news)
    return news


@router.delete("/{news_id}", status_code=204, dependencies=admin_only)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    db.delete(find_news(db, news_id))
    db.commit()
    return Response(status_code=204)


@router.post("/{news_id}/image", response_model=NewsResponse, dependencies=admin_only)
def upload_image(news_id: int, file: UploadFile, db: Session = Depends(get_db)):
    news = find_news(db, news_id)
    try:
        path = save_image(file)
    finally:
        file.file.close()
    news.imagem_path = path.name
    try:
        db.commit()
    except Exception:
        db.rollback()
        path.unlink(missing_ok=True)
        raise
    db.refresh(news)
    return news


@router.get("/{news_id}/image")
def get_image(news_id: int, db: Session = Depends(get_db)):
    news = find_news(db, news_id, public=True)
    if not news.imagem_path or Path(news.imagem_path).name != news.imagem_path:
        raise HTTPException(404, "Imagem não encontrada")
    path = Path(settings.news_upload_dir) / news.imagem_path
    if not path.is_file():
        raise HTTPException(404, "Imagem não encontrada")
    return FileResponse(path, headers={"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})
