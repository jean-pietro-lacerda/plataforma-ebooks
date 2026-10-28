from fastapi import FastAPI

app = FastAPI(title="Plataforma de E-books API")

@app.get("/health")
def health():
    return {"status": "ok"}