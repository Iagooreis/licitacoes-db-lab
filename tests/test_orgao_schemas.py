import pytest
from pydantic import ValidationError

from app.models import Orgao
from app.schemas import OrgaoCreate, OrgaoResponse


def test_orgao_create_removes_surrounding_spaces() -> None:
    schema = OrgaoCreate(
        nome_orgao="  Secretaria de Saude  ",
    )

    assert schema.nome_orgao == "Secretaria de Saude"


def test_orgao_create_rejects_blank_name() -> None:
    with pytest.raises(ValidationError):
        OrgaoCreate(nome_orgao="   ")


def test_orgao_response_accepts_orm_model() -> None:
    orgao = Orgao(
        id_orgao=1,
        nome_orgao="Secretaria de Educacao",
    )

    response = OrgaoResponse.model_validate(orgao)

    assert response.model_dump() == {
        "id_orgao": 1,
        "nome_orgao": "Secretaria de Educacao",
    }
