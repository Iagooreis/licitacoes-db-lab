-- Exemplo 1: cadastrar um pedido e confirmar a transacao
BEGIN;

-- Cadastrar o pedido e guardar o ID gerado
INSERT INTO pedido (
    id_contrato,
    solicitante,
    data_pedido
)
VALUES (
    1,
    'Posto de Saude Central',
    '2026-09-01'
)
RETURNING id_pedido AS novo_id_pedido
\gset

-- Cadastrar os itens do novo pedido
INSERT INTO item_pedido (
    id_pedido,
    id_item_contrato,
    quantidade_pedida
)
VALUES
    (:novo_id_pedido, 1, 50),
    (:novo_id_pedido, 2, 25);

-- Conferir o saldo depois do pedido
SELECT
    ic.id_item_contrato,
    ic.quantidade_contratada,
    COALESCE(SUM(ip.quantidade_pedida), 0) AS quantidade_pedida,
    ic.quantidade_contratada
        - COALESCE(SUM(ip.quantidade_pedida), 0) AS saldo_disponivel
FROM item_contrato AS ic
LEFT JOIN item_pedido AS ip
  ON ip.id_item_contrato = ic.id_item_contrato
WHERE ic.id_item_contrato IN (1, 2)
GROUP BY
    ic.id_item_contrato,
    ic.quantidade_contratada
ORDER BY ic.id_item_contrato;

COMMIT;

-- Exemplo 2: cadastrar um pedido e desfazer a transacao
BEGIN;

INSERT INTO pedido (
    id_contrato,
    solicitante,
    data_pedido
)
VALUES (
    2,
    'Escola Municipal Norte',
    '2026-09-02'
)
RETURNING id_pedido AS pedido_rollback
\gset

INSERT INTO item_pedido (
    id_pedido,
    id_item_contrato,
    quantidade_pedida
)
VALUES
    (:pedido_rollback, 3, 100),
    (:pedido_rollback, 4, 5);

-- O pedido existe neste momento, dentro da transacao
SELECT *
FROM pedido
WHERE id_pedido = :pedido_rollback;

ROLLBACK;

-- Depois do ROLLBACK, o pedido nao deve mais existir
SELECT *
FROM pedido
WHERE id_pedido = :pedido_rollback;