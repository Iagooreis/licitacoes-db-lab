from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Identity, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.contrato import Contrato
    from app.models.proposta import Proposta


class Fornecedor(Base):
    __tablename__ = "fornecedor"

    __table_args__ = (
        UniqueConstraint(
            "cnpj",
            name="uq_fornecedor_cnpj",
        ),
        CheckConstraint(
            "cnpj ~ '^[0-9]{14}$'",
            name="ck_fornecedor_cnpj",
        ),
    )

    id_fornecedor: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    nome_fornecedor: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    cnpj: Mapped[str] = mapped_column(
        String(14),
        nullable=False,
    )
    rua: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    cidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    propostas: Mapped[list["Proposta"]] = relationship(
        back_populates="fornecedor",
    )
    contratos: Mapped[list["Contrato"]] = relationship(
        back_populates="fornecedor",
    )
