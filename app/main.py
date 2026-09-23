from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies import SessionDep
from app.routes import orgao_router

app = FastAPI(
    title="API de Licitacoes",
    version="0.1.0",
)

app.include_router(orgao_router)


@app.get("/health", tags=["infraestrutura"])
def health_check(session: SessionDep) -> dict[str, str]:
    session.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "ok",
    }
