from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.fornecedor import Fornecedor
    from app.models.item import Item


class Proposta(Base):
    __tablename__ = "proposta"

    __table_args__ = (
        CheckConstraint(
            "preco_unitario >= 0",
            name="ck_proposta_preco",
        ),
        CheckConstraint(
            "quantidade_ofertada > 0",
            name="ck_proposta_quantidade",
        ),
        CheckConstraint(
            "situacao IN "
            "('APRESENTADA', 'CLASSIFICADA', 'DESCLASSIFICADA', 'VENCEDORA')",
            name="ck_proposta_situacao",
        ),
        Index(
            "uq_proposta_vencedora_item",
            "id_item",
            unique=True,
            postgresql_where=text("situacao = 'VENCEDORA'"),
        ),
    )

    id_item: Mapped[int] = mapped_column(
        ForeignKey("item.id_item", name="fk_proposta_item", ondelete="RESTRICT"),
        primary_key=True,
    )
    id_fornecedor: Mapped[int] = mapped_column(
        ForeignKey(
            "fornecedor.id_fornecedor",
            name="fk_proposta_fornecedor",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )
    preco_unitario: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )
    quantidade_ofertada: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )
    situacao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="APRESENTADA",
    )
    item: Mapped["Item"] = relationship(
        back_populates="propostas",
    )
    fornecedor: Mapped["Fornecedor"] = relationship(
        back_populates="propostas",
    )
