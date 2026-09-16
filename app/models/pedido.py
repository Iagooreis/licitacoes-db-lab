from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Identity, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.contrato import Contrato
    from app.models.item_pedido import ItemPedido


class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    id_contrato: Mapped[int] = mapped_column(
        ForeignKey(
            "contrato.id_contrato",
            name="fk_pedido_contrato",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    solicitante: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    data_pedido: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date(),
    )
    contrato: Mapped["Contrato"] = relationship(
        back_populates="pedidos",
    )
    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido",
    )
