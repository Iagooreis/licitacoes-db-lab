from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Orgao


class OrgaoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, orgao: Orgao) -> Orgao:
        self.session.add(orgao)

        return orgao

    def list_all(self) -> list[Orgao]:
        statement = select(Orgao).order_by(Orgao.id_orgao)

        return list(self.session.scalars(statement))

    def get_by_id(self, id_orgao: int) -> Orgao | None:
        return self.session.get(Orgao, id_orgao)
