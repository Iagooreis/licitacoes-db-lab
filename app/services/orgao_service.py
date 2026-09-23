from sqlalchemy.orm import Session

from app.models import Orgao
from app.repositories import OrgaoRepository
from app.schemas import OrgaoCreate


class OrgaoService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = OrgaoRepository(session)

    def create(self, data: OrgaoCreate) -> Orgao:
        orgao = Orgao(
            nome_orgao=data.nome_orgao,
        )

        try:
            self.repository.add(orgao)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        self.session.refresh(orgao)

        return orgao

    def list_all(self) -> list[Orgao]:
        return self.repository.list_all()
