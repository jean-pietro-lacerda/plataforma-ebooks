from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.books import router as books_router

app = FastAPI(title="Plataforma de E-books API")

app.include_router(auth_router)
app.include_router(books_router)


@app.get("/health")
def health():
    return {"status": "ok"}
