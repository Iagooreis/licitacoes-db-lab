from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.item_contrato import ItemContrato
    from app.models.licitacao import Licitacao
    from app.models.proposta import Proposta


class Item(Base):
    __tablename__ = "item"

    __table_args__ = (
        CheckConstraint(
            "quantidade_licitada > 0",
            name="ck_item_quantidade",
        ),
        CheckConstraint(
            "valor_referencia >= 0",
            name="ck_item_valor_referencia",
        ),
        Index(
            "idx_item_licitacao",
            "id_licitacao",
        ),
    )

    id_item: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    id_licitacao: Mapped[int] = mapped_column(
        ForeignKey(
            "licitacao.id_licitacao",
            name="fk_item_licitacao",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    quantidade_licitada: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )
    unidade_medida: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    valor_referencia: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    licitacao: Mapped["Licitacao"] = relationship(
        back_populates="itens",
    )
    propostas: Mapped[list["Proposta"]] = relationship(
        back_populates="item",
    )
    item_contrato: Mapped["ItemContrato | None"] = relationship(
        back_populates="item",
    )
