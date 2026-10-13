from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas import LicitacaoCreate


def test_licitacao_uses_default_status() -> None:
    licitacao = LicitacaoCreate(
        id_orgao=1,
        numero="001/2026",
        objeto="Compra de medicamentos",
        exercicio=2026,
        modalidade="PREGAO",
        data_inicio=date(2026, 1, 10),
    )

    assert licitacao.situacao == "ABERTA"
    assert licitacao.data_encerramento is None


def test_licitacao_rejects_invalid_period() -> None:
    with pytest.raises(ValidationError):
        LicitacaoCreate(
            id_orgao=1,
            numero="001/2026",
            objeto="Compra de medicamentos",
            exercicio=2026,
            modalidade="PREGAO",
            data_inicio=date(2026, 2, 10),
            data_encerramento=date(2026, 2, 1),
        )
