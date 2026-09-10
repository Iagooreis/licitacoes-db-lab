from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.orgao import Orgao


class Licitacao(Base):
    __tablename__ = "licitacao"

    __table_args__ = (
        UniqueConstraint(
            "id_orgao",
            "numero",
            "exercicio",
            name="uq_licitacao",
        ),
        CheckConstraint(
            "exercicio >= 2000 AND exercicio <= 2100",
            name="ck_licitacao_exercicio",
        ),
        CheckConstraint(
            "situacao IN "
            "('ABERTA', 'EM ANDAMENTO', 'HOMOLOGADA', 'CANCELADA')",
            name="ck_licitacao_situacao",
        ),
        CheckConstraint(
            "data_encerramento IS NULL "
            "OR data_encerramento >= data_inicio",
            name="ck_licitacao_data_encerramento",
        ),
    )

    id_licitacao: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True,
    )
    id_orgao: Mapped[int] = mapped_column(
        ForeignKey(
            "orgao.id_orgao",
            name="fk_licitacao_orgao",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    numero: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    objeto: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    exercicio: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    modalidade: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    situacao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="ABERTA",
    )
    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    data_encerramento: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    orgao: Mapped["Orgao"] = relationship(
        back_populates="licitacoes",
    )