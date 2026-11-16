from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import warnings

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.core.config import settings

MAX_IMAGE_SIZE = 5 * 1024 * 1024
IMAGE_FORMATS = {"image/jpeg": ("JPEG", ".jpg"), "image/png": ("PNG", ".png"), "image/webp": ("WEBP", ".webp")}


def apply_news_changes(news, values):
    for key, value in values.items():
        setattr(news, key, value)
    if news.publicada and news.data_publicacao is None:
        news.data_publicacao = datetime.now(timezone.utc)


def save_image(upload: UploadFile) -> Path:
    expected = IMAGE_FORMATS.get(upload.content_type)
    if expected is None:
        raise HTTPException(415, "Use imagens JPEG, PNG ou WebP")
    data = upload.file.read(MAX_IMAGE_SIZE + 1)
    if len(data) > MAX_IMAGE_SIZE:
        raise HTTPException(413, "A imagem deve ter no máximo 5 MiB")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                if image.format != expected[0]:
                    raise ValueError("Formato incompatível")
                image.verify()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(415, "Imagem inválida")
    directory = Path(settings.news_upload_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (uuid4().hex + expected[1])
    try:
        path.write_bytes(data)
    except OSError:
        path.unlink(missing_ok=True)
        raise
    return path
