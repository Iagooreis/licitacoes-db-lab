from sqlalchemy.orm import Session

from app.exceptions import (
    LicitacaoAlreadyExistsError,
    LicitacaoNotFoundError,
    OrgaoNotFoundError,
)
from app.models import Licitacao
from app.repositories import LicitacaoRepository, OrgaoRepository
from app.schemas import LicitacaoCreate


class LicitacaoService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.licitacao_repository = LicitacaoRepository(session)
        self.orgao_repository = OrgaoRepository(session)

    def create(self, data: LicitacaoCreate) -> Licitacao:
        if self.orgao_repository.get_by_id(data.id_orgao) is None:
            raise OrgaoNotFoundError(data.id_orgao)

        if self.licitacao_repository.exists_by_orgao_numero_exercicio(
            data.id_orgao,
            data.numero,
            data.exercicio,
        ):
            raise LicitacaoAlreadyExistsError(
                data.id_orgao,
                data.numero,
                data.exercicio,
            )

        licitacao = Licitacao(
            id_orgao=data.id_orgao,
            numero=data.numero,
            objeto=data.objeto,
            exercicio=data.exercicio,
            modalidade=data.modalidade,
            situacao=data.situacao,
            data_inicio=data.data_inicio,
            data_encerramento=data.data_encerramento,
        )

        try:
            self.licitacao_repository.add(licitacao)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        self.session.refresh(licitacao)

        return licitacao

    def get_by_id(self, id_licitacao: int) -> Licitacao:
        licitacao = self.licitacao_repository.get_by_id(
            id_licitacao,
        )

        if licitacao is None:
            raise LicitacaoNotFoundError(id_licitacao)

        return licitacao

    def list_all(self) -> list[Licitacao]:
        return self.licitacao_repository.list_all()
