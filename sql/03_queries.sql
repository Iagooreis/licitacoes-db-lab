-- 1. Valor estimado de cada licitacao
SELECT
    l.id_licitacao,
    l.numero,
    l.objeto,
    ROUND(
        COALESCE(
            SUM(i.quantidade_licitada * i.valor_referencia),
            0
        ),
        2
    ) AS valor_estimado
FROM licitacao AS l
LEFT JOIN item AS i
       ON i.id_licitacao = l.id_licitacao
GROUP BY
    l.id_licitacao,
    l.numero,
    l.objeto
ORDER BY l.id_licitacao;

-- 2. Quantidade de fornecedores participantes por licitacao
SELECT
    l.id_licitacao,
    l.numero,
    COUNT(DISTINCT p.id_fornecedor) AS quantidade_fornecedores
FROM licitacao AS l
LEFT JOIN item AS i
       ON i.id_licitacao = l.id_licitacao
LEFT JOIN proposta AS p
       ON p.id_item = i.id_item
GROUP BY
    l.id_licitacao,
    l.numero
ORDER BY l.id_licitacao;

-- 3. Proposta vencedora de cada item
SELECT
    l.numero AS numero_licitacao,
    i.id_item,
    i.descricao,
    f.id_fornecedor,
    f.nome_fornecedor,
    p.preco_unitario,
    p.quantidade_ofertada
FROM item AS i
JOIN licitacao AS l
  ON l.id_licitacao = i.id_licitacao
LEFT JOIN proposta AS p
       ON p.id_item = i.id_item
      AND p.situacao = 'VENCEDORA'
LEFT JOIN fornecedor AS f
       ON f.id_fornecedor = p.id_fornecedor
ORDER BY
    l.id_licitacao,
    i.id_item;

-- 4. Diferenca entre valor de referencia e valor contratado
SELECT
    c.numero AS numero_contrato,
    i.id_item,
    i.descricao,
    i.valor_referencia,
    ic.valor_unitario_contratado,
    ROUND(
        i.valor_referencia - ic.valor_unitario_contratado,
        2
    ) AS diferenca_unitaria,
    ROUND(
        (i.valor_referencia - ic.valor_unitario_contratado)
        * ic.quantidade_contratada,
        2
    ) AS diferenca_total
FROM item_contrato AS ic
JOIN item AS i
  ON i.id_item = ic.id_item
JOIN contrato AS c
  ON c.id_contrato = ic.id_contrato
ORDER BY
    c.id_contrato,
    i.id_item;

-- 5. Valor total de cada contrato
SELECT
    c.id_contrato,
    c.numero,
    f.nome_fornecedor,
    ROUND(
        COALESCE(
            SUM(
                ic.quantidade_contratada
                * ic.valor_unitario_contratado
            ),
            0
        ),
        2
    ) AS valor_total_contrato
FROM contrato AS c
JOIN fornecedor AS f
  ON f.id_fornecedor = c.id_fornecedor
LEFT JOIN item_contrato AS ic
       ON ic.id_contrato = c.id_contrato
GROUP BY
    c.id_contrato,
    c.numero,
    f.nome_fornecedor
ORDER BY c.id_contrato;

-- 6. Quantidade e valor ja pedidos por item contratado
SELECT
    c.numero AS numero_contrato,
    i.id_item,
    i.descricao,
    i.unidade_medida,
    ic.quantidade_contratada,
    COALESCE(
        SUM(ip.quantidade_pedida),
        0
    ) AS quantidade_ja_pedida,
    ROUND(
        COALESCE(
            SUM(
                ip.quantidade_pedida
                * ic.valor_unitario_contratado
            ),
            0
        ),
        2
    ) AS valor_ja_pedido
FROM item_contrato AS ic
JOIN contrato AS c
  ON c.id_contrato = ic.id_contrato
JOIN item AS i
  ON i.id_item = ic.id_item
LEFT JOIN item_pedido AS ip
       ON ip.id_item_contrato = ic.id_item_contrato
GROUP BY
    c.id_contrato,
    c.numero,
    i.id_item,
    i.descricao,
    i.unidade_medida,
    ic.id_item_contrato,
    ic.quantidade_contratada,
    ic.valor_unitario_contratado
ORDER BY
    c.id_contrato,
    i.id_item;

-- 7. Saldo disponivel de cada item contratado
SELECT
    c.numero AS numero_contrato,
    i.id_item,
    i.descricao,
    i.unidade_medida,
    ic.quantidade_contratada,
    COALESCE(
        SUM(ip.quantidade_pedida),
        0
    ) AS quantidade_pedida,
    ic.quantidade_contratada
        - COALESCE(
            SUM(ip.quantidade_pedida),
            0
        ) AS saldo_disponivel
FROM item_contrato AS ic
JOIN contrato AS c
  ON c.id_contrato = ic.id_contrato
JOIN item AS i
  ON i.id_item = ic.id_item
LEFT JOIN item_pedido AS ip
  ON ip.id_item_contrato = ic.id_item_contrato
GROUP BY
    c.id_contrato,
    c.numero,
    i.id_item,
    i.descricao,
    i.unidade_medida,
    ic.id_item_contrato,
    ic.quantidade_contratada
ORDER BY
    c.id_contrato,
    i.id_item;

-- 8. Contratos que nunca tiveram pedido
SELECT
    c.id_contrato,
    c.numero,
    f.nome_fornecedor,
    c.data_inicio,
    c.data_termino,
    c.situacao
FROM contrato AS c
JOIN fornecedor AS f
  ON f.id_fornecedor = c.id_fornecedor
WHERE NOT EXISTS (
    SELECT 1
    FROM pedido AS p
    WHERE p.id_contrato = c.id_contrato
)
ORDER BY c.id_contrato;

-- 9. Fornecedor com maior valor contratado
SELECT
    f.id_fornecedor,
    f.nome_fornecedor,
    ROUND(
        SUM(
            ic.quantidade_contratada
            * ic.valor_unitario_contratado
        ),
        2
    ) AS valor_total_contratado
FROM fornecedor AS f
JOIN contrato AS c
  ON c.id_fornecedor = f.id_fornecedor
JOIN item_contrato AS ic
  ON ic.id_contrato = c.id_contrato
GROUP BY
    f.id_fornecedor,
    f.nome_fornecedor
ORDER BY valor_total_contratado DESC
LIMIT 1;

-- 10. Itens com economia superior a 10%
SELECT
    c.numero AS numero_contrato,
    i.id_item,
    i.descricao,
    i.valor_referencia,
    ic.valor_unitario_contratado,
    ROUND(
        (
            (i.valor_referencia - ic.valor_unitario_contratado)
            / i.valor_referencia
        ) * 100,
        2
    ) AS percentual_economia
FROM item_contrato AS ic
JOIN item AS i
  ON i.id_item = ic.id_item
JOIN contrato AS c
  ON c.id_contrato = ic.id_contrato
WHERE i.valor_referencia > 0
  AND (
        (i.valor_referencia - ic.valor_unitario_contratado)
        / i.valor_referencia
      ) > 0.10
ORDER BY percentual_economia DESC;