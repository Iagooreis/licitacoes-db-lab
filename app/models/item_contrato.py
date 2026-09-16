from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.contrato import Contrato
    from app.models.item import Item
    from app.models.item_pedido import ItemPedido


class ItemContrato(Base):
    __tablename__ = "item_contrato"

    __table_args__ = (
        UniqueConstraint(
            "id_item",
            name="uq_item_contrato",
        ),
        CheckConstraint(
            "quantidade_contratada > 0",
            name="ck_item_contrato_quantidade",
        ),
        CheckConstraint(
            "valor_unitario_contratado >= 0",
            name="ck_item_contrato_valor",
        ),
        Index(
            "idx_item_contrato_contrato",
            "id_contrato",
        ),
    )

    id_item_contrato: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    id_contrato: Mapped[int] = mapped_column(
        ForeignKey(
            "contrato.id_contrato",
            name="fk_item_contrato_contrato",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    id_item: Mapped[int] = mapped_column(
        ForeignKey(
            "item.id_item",
            name="fk_item_contrato_item",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    quantidade_contratada: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )
    valor_unitario_contratado: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )
    contrato: Mapped["Contrato"] = relationship(
        back_populates="itens",
    )
    item: Mapped["Item"] = relationship(
        back_populates="item_contrato",
    )
    itens_pedido: Mapped[list["ItemPedido"]] = relationship(
        back_populates="item_contrato",
    )
