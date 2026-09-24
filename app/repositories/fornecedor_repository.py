from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Fornecedor


class FornecedorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, fornecedor: Fornecedor) -> Fornecedor:
        self.session.add(fornecedor)

        return fornecedor

    def list_all(self) -> list[Fornecedor]:
        statement = select(Fornecedor).order_by(Fornecedor.id_fornecedor)

        return list(self.session.scalars(statement))
