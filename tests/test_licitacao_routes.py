from fastapi.testclient import TestClient


def create_orgao(client: TestClient) -> int:
    response = client.post(
        "/orgaos",
        json={"nome_orgao": "Orgao das licitacoes"},
    )

    assert response.status_code == 201

    return response.json()["id_orgao"]


def test_create_and_get_licitacao(client: TestClient) -> None:
    id_orgao = create_orgao(client)

    create_response = client.post(
        "/licitacoes",
        json={
            "id_orgao": id_orgao,
            "numero": "900/2026",
            "objeto": "Compra para o teste da API",
            "exercicio": 2026,
            "modalidade": "PREGAO",
            "data_inicio": "2026-01-10",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["id_orgao"] == id_orgao
    assert created["situacao"] == "ABERTA"
    assert isinstance(created["id_licitacao"], int)

    get_response = client.get(
        f"/licitacoes/{created['id_licitacao']}",
    )

    assert get_response.status_code == 200
    assert get_response.json() == created


def test_list_licitacoes(client: TestClient) -> None:
    id_orgao = create_orgao(client)

    create_response = client.post(
        "/licitacoes",
        json={
            "id_orgao": id_orgao,
            "numero": "901/2026",
            "objeto": "Licitacao para testar listagem",
            "exercicio": 2026,
            "modalidade": "PREGAO",
            "data_inicio": "2026-01-10",
        },
    )

    id_licitacao = create_response.json()["id_licitacao"]

    response = client.get("/licitacoes")

    assert response.status_code == 200

    ids = {licitacao["id_licitacao"] for licitacao in response.json()}

    assert id_licitacao in ids


def test_create_licitacao_rejects_unknown_orgao(
    client: TestClient,
) -> None:
    response = client.post(
        "/licitacoes",
        json={
            "id_orgao": 999999999,
            "numero": "902/2026",
            "objeto": "Licitacao com orgao inexistente",
            "exercicio": 2026,
            "modalidade": "PREGAO",
            "data_inicio": "2026-01-10",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Orgao 999999999 nao encontrado",
    }


def test_get_licitacao_returns_404_when_not_found(
    client: TestClient,
) -> None:
    response = client.get("/licitacoes/999999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Licitacao 999999999 nao encontrada",
    }
