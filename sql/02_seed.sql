TRUNCATE TABLE
    item_pedido,
    pedido,
    item_contrato,
    contrato,
    proposta,
    fornecedor,
    item,
    licitacao,
    orgao
RESTART IDENTITY;

INSERT INTO orgao (nome_orgao)
VALUES
    ('Secretaria Municipal de Saude'),
    ('Secretaria Municipal de Educacao');

INSERT INTO licitacao (
    id_orgao,
    numero,
    objeto,
    exercicio,
    modalidade,
    situacao,
    data_inicio,
    data_encerramento
)
VALUES
    (
        1,
        '001/2026',
        'Aquisicao de materiais hospitalares',
        2026,
        'PREGAO ELETRONICO',
        'HOMOLOGADA',
        '2026-01-10',
        '2026-02-10'
    ),
    (
        2,
        '002/2026',
        'Aquisicao de materiais escolares',
        2026,
        'PREGAO ELETRONICO',
        'HOMOLOGADA',
        '2026-02-15',
        '2026-03-15'
    ),
    (
        1,
        '003/2026',
        'Aquisicao de equipamentos de informatica',
        2026,
        'CONCORRENCIA',
        'ABERTA',
        '2026-08-01',
        NULL
    );

INSERT INTO item (
    id_licitacao,
    descricao,
    quantidade_licitada,
    unidade_medida,
    valor_referencia
)
VALUES
    (1, 'Luvas descartaveis',       1000, 'CAIXA',   20.00),
    (1, 'Kit para curativo',         500, 'KIT',     50.00),
    (1, 'Termometro digital',        200, 'UNIDADE', 100.00),
    (1, 'Mascara cirurgica',        3000, 'CAIXA',   12.00),

    (2, 'Caderno universitario',    2000, 'UNIDADE',  10.00),
    (2, 'Projetor multimidia',       100, 'UNIDADE', 2000.00),
    (2, 'Resma de papel A4',         800, 'RESMA',    35.00),

    (3, 'Notebook',                   50, 'UNIDADE', 4500.00),
    (3, 'Monitor de 24 polegadas',    80, 'UNIDADE', 1200.00),
    (3, 'Teclado USB',               120, 'UNIDADE',   90.00);

INSERT INTO fornecedor (
    nome_fornecedor,
    cnpj,
    rua,
    cidade
)
VALUES
    (
        'MedSupply Produtos Hospitalares',
        '00000001000101',
        'Rua das Flores, 100',
        'Sao Paulo'
    ),
    (
        'Vida Hospitalar Ltda',
        '00000002000102',
        'Avenida Central, 250',
        'Campinas'
    ),
    (
        'Educa Brasil Materiais',
        '00000003000103',
        'Rua da Escola, 30',
        'Curitiba'
    ),
    (
        'Tecnologia Alfa Ltda',
        '00000004000104',
        'Avenida Digital, 500',
        'Sao Paulo'
    ),
    (
        'Papelaria Central Ltda',
        '00000005000105',
        'Rua do Comercio, 75',
        'Belo Horizonte'
    );

INSERT INTO proposta (
    id_item,
    id_fornecedor,
    preco_unitario,
    quantidade_ofertada,
    situacao
)
VALUES
    (1, 1,   18.00, 1000, 'VENCEDORA'),
    (1, 2,   19.00, 1000, 'CLASSIFICADA'),

    (2, 1,   42.00,  500, 'VENCEDORA'),
    (2, 2,   45.00,  500, 'CLASSIFICADA'),

    (3, 2,   85.00,  200, 'VENCEDORA'),
    (3, 1,   92.00,  200, 'CLASSIFICADA'),

    (4, 2,   10.00, 3000, 'VENCEDORA'),
    (4, 1,   11.00, 3000, 'CLASSIFICADA'),

    (5, 3,    9.00, 2000, 'VENCEDORA'),
    (5, 5,    9.50, 2000, 'CLASSIFICADA'),

    (6, 3, 1700.00,  100, 'VENCEDORA'),
    (6, 4, 1800.00,  100, 'CLASSIFICADA'),

    (7, 5,   31.00,  800, 'VENCEDORA'),
    (7, 3,   33.00,  800, 'CLASSIFICADA'),

    (8, 4, 4200.00,   50, 'APRESENTADA');

INSERT INTO contrato (
    id_licitacao,
    id_fornecedor,
    numero,
    data_inicio,
    data_termino,
    situacao
)
VALUES
    (1, 1, 'C-001/2026', '2026-03-20', '2027-03-19', 'ATIVO'),
    (2, 3, 'C-002/2026', '2026-04-01', '2027-03-31', 'ATIVO'),
    (1, 2, 'C-003/2026', '2026-03-20', '2027-03-19', 'ATIVO');

INSERT INTO item_contrato (
    id_contrato,
    id_item,
    quantidade_contratada,
    valor_unitario_contratado
)
VALUES
    (1, 1,  800,   18.00),
    (1, 2,  500,   42.00),
    (2, 5, 1500,    9.00),
    (2, 6,   80, 1700.00),
    (3, 3,  150,   85.00);

INSERT INTO pedido (
    id_contrato,
    solicitante,
    data_pedido
)
VALUES
    (1, 'Almoxarifado da Saude',    '2026-04-05'),
    (1, 'Unidade de Pronto Atendimento', '2026-05-10'),
    (1, 'Hospital Municipal',       '2026-06-15'),
    (2, 'Escola Municipal Central', '2026-05-01'),
    (2, 'Secretaria de Educacao',   '2026-07-10');

INSERT INTO item_pedido (
    id_pedido,
    id_item_contrato,
    quantidade_pedida
)
VALUES
    (1, 1, 200),
    (1, 2,  50),
    (2, 1, 150),
    (3, 2, 100),
    (4, 3, 500),
    (4, 4,  10),
    (5, 4,  20);

    