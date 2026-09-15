from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Identity,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.fornecedor import Fornecedor
    from app.models.item_contrato import ItemContrato
    from app.models.licitacao import Licitacao


class Contrato(Base):
    __tablename__ = "contrato"

    __table_args__ = (
        UniqueConstraint(
            "id_licitacao",
            "numero",
            name="uq_contrato",
        ),
        CheckConstraint(
            "data_termino >= data_inicio",
            name="ck_contrato_periodo",
        ),
        CheckConstraint(
            "situacao IN ('ATIVO', 'ENCERRADO', 'CANCELADO')",
            name="ck_contrato_situacao",
        ),
    )

    id_contrato: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    id_licitacao: Mapped[int] = mapped_column(
        ForeignKey(
            "licitacao.id_licitacao",
            name="fk_contrato_licitacao",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    id_fornecedor: Mapped[int] = mapped_column(
        ForeignKey(
            "fornecedor.id_fornecedor",
            name="fk_contrato_fornecedor",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    numero: Mapped[str] = mapped_column(String(30), nullable=False)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_termino: Mapped[date] = mapped_column(Date, nullable=False)
    situacao: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="ATIVO",
    )
    licitacao: Mapped["Licitacao"] = relationship(
        back_populates="contratos",
    )
    fornecedor: Mapped["Fornecedor"] = relationship(
        back_populates="contratos",
    )
    itens: Mapped[list["ItemContrato"]] = relationship(
        back_populates="contrato",
    )
