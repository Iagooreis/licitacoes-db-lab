from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_session

app = FastAPI(
    title="API de Licitacoes",
    version="0.1.0",
)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/health", tags=["infraestrutura"])
def health_check(session: SessionDep) -> dict[str, str]:
    session.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "ok",
    }
