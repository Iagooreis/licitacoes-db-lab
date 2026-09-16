from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.item_contrato import ItemContrato
    from app.models.pedido import Pedido


class ItemPedido(Base):
    __tablename__ = "item_pedido"

    __table_args__ = (
        CheckConstraint(
            "quantidade_pedida > 0",
            name="ck_item_pedido_quantidade",
        ),
    )

    id_pedido: Mapped[int] = mapped_column(
        ForeignKey(
            "pedido.id_pedido",
            name="fk_item_pedido_pedido",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )
    id_item_contrato: Mapped[int] = mapped_column(
        ForeignKey(
            "item_contrato.id_item_contrato",
            name="fk_item_pedido_item_contrato",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )
    quantidade_pedida: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )
    pedido: Mapped["Pedido"] = relationship(
        back_populates="itens",
    )
    item_contrato: Mapped["ItemContrato"] = relationship(
        back_populates="itens_pedido",
    )
