from typing import TYPE_CHECKING

from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.licitacao import Licitacao


class Orgao(Base):
    __tablename__ = "orgao"

    id_orgao: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    nome_orgao: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    licitacoes: Mapped[list["Licitacao"]] = relationship(
        back_populates="orgao",
    )
