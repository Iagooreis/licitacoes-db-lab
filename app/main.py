from fastapi import FastAPI

app = FastAPI(
    title="API de Licitacoes",
    version="0.1.0",
)


@app.get("/health", tags=["infraestrutura"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


