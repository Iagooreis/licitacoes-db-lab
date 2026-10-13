from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Licitacao


class LicitacaoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, licitacao: Licitacao) -> Licitacao:
        self.session.add(licitacao)

        return licitacao

    def list_all(self) -> list[Licitacao]:
        statement = select(Licitacao).order_by(Licitacao.id_licitacao)

        return list(self.session.scalars(statement))

    def get_by_id(self, id_licitacao: int) -> Licitacao | None:
        return self.session.get(Licitacao, id_licitacao)
