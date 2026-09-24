from fastapi.testclient import TestClient


def test_create_orgao(client: TestClient) -> None:
    response = client.post(
        "/orgaos",
        json={
            "nome_orgao": "Orgao criado pelo teste",
        },
    )

    assert response.status_code == 201
    assert response.json()["nome_orgao"] == "Orgao criado pelo teste"
    assert isinstance(response.json()["id_orgao"], int)


def test_list_orgaos(client: TestClient) -> None:
    client.post(
        "/orgaos",
        json={"nome_orgao": "Orgao A da listagem"},
    )
    client.post(
        "/orgaos",
        json={"nome_orgao": "Orgao B da listagem"},
    )

    response = client.get("/orgaos")

    assert response.status_code == 200

    nomes = {orgao["nome_orgao"] for orgao in response.json()}

    assert "Orgao A da listagem" in nomes
    assert "Orgao B da listagem" in nomes


def test_create_orgao_rejects_blank_name(client: TestClient) -> None:
    response = client.post(
        "/orgaos",
        json={"nome_orgao": "   "},
    )

    assert response.status_code == 422
