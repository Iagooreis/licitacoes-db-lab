from datetime import date
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LicitacaoBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_orgao: int = Field(gt=0)
    numero: str = Field(min_length=1, max_length=30)
    objeto: str = Field(min_length=1)
    exercicio: int = Field(ge=2000, le=2100)
    modalidade: str = Field(min_length=1, max_length=30)
    situacao: Literal[
        "ABERTA",
        "EM ANDAMENTO",
        "HOMOLOGADA",
        "CANCELADA",
    ] = "ABERTA"
    data_inicio: date
    data_encerramento: date | None = None

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if (
            self.data_encerramento is not None
            and self.data_encerramento < self.data_inicio
        ):
            raise ValueError(
                "Data de encerramento nao pode ser anterior a data de inicio",
            )

        return self


class LicitacaoCreate(LicitacaoBase):
    pass


class LicitacaoResponse(LicitacaoBase):
    model_config = ConfigDict(from_attributes=True)

    id_licitacao: int
