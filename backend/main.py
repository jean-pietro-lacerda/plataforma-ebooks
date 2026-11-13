from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.books import router as books_router

app = FastAPI(title="Plataforma de E-books API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
)

app.include_router(auth_router)
app.include_router(books_router)


@app.get("/health")
def health():
    return {"status": "ok"}

