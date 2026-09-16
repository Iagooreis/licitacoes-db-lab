import pytest
from sqlalchemy import inspect

from app.models import (
    Contrato,
    Fornecedor,
    Item,
    ItemContrato,
    ItemPedido,
    Licitacao,
    Orgao,
    Pedido,
    Proposta,
)


@pytest.mark.parametrize(
    ("model", "expected_relationships"),
    [
        (Orgao, {"licitacoes"}),
        (Licitacao, {"orgao", "itens", "contratos"}),
        (Item, {"licitacao", "propostas", "item_contrato"}),
        (Fornecedor, {"propostas", "contratos"}),
        (Proposta, {"item", "fornecedor"}),
        (Contrato, {"licitacao", "fornecedor", "itens", "pedidos"}),
        (ItemContrato, {"contrato", "item", "itens_pedido"}),
        (Pedido, {"contrato", "itens"}),
        (ItemPedido, {"pedido", "item_contrato"}),
    ],
)
def test_model_relationships(
    model: type,
    expected_relationships: set[str],
) -> None:
    relationships = set(inspect(model).relationships.keys())

    assert relationships == expected_relationships


def test_order_relationships_are_bidirectional() -> None:
    contrato = Contrato()
    pedido = Pedido()
    item_contrato = ItemContrato()
    item_pedido = ItemPedido()

    contrato.pedidos.append(pedido)
    pedido.itens.append(item_pedido)
    item_contrato.itens_pedido.append(item_pedido)

    assert pedido.contrato is contrato
    assert item_pedido.pedido is pedido
    assert item_pedido.item_contrato is item_contrato
