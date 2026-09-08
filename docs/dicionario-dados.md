# Dicionario de dados - Banco de licitacoes

Este documento descreve a estrutura logica que sera implementada no PostgreSQL.
Os nomes fisicos usam `snake_case`, sem espacos ou acentos.

## Convencoes

- IDs simples usam `INTEGER` gerado automaticamente por identidade.
- Quantidades usam `NUMERIC(14,3)` para permitir unidades fracionarias.
- Valores monetarios usam `NUMERIC(14,2)` para evitar arredondamentos de ponto flutuante.
- CNPJ e armazenado somente com os 14 digitos, sem pontuacao.
- Chaves estrangeiras usam `ON DELETE RESTRICT` para preservar o historico.
- Quantidades devem ser maiores que zero; precos e valores devem ser maiores ou iguais a zero.

## `orgao`

Uma linha representa um orgao publico que pode realizar licitacoes.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_orgao` | `INTEGER` | Nao | PK | Identidade | Identificador interno do orgao. |
| `nome_orgao` | `VARCHAR(200)` | Nao |  |  | Nome oficial do orgao. |

## `licitacao`

Uma linha representa um processo licitatorio realizado por um orgao.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_licitacao` | `INTEGER` | Nao | PK | Identidade | Identificador interno da licitacao. |
| `id_orgao` | `INTEGER` | Nao | FK -> `orgao.id_orgao` |  | Orgao responsavel pela licitacao. |
| `numero` | `VARCHAR(30)` | Nao | UNIQUE com `id_orgao` e `exercicio` |  | Numero administrativo, podendo conter barras, hifens e zeros iniciais. |
| `objeto` | `TEXT` | Nao |  |  | Descricao do objeto da licitacao. |
| `exercicio` | `INTEGER` | Nao | CHECK entre `2000` e `2100` |  | Exercicio administrativo da licitacao. |
| `modalidade` | `VARCHAR(30)` | Nao |  |  | Modalidade do processo licitatorio. |
| `situacao` | `VARCHAR(30)` | Nao | CHECK de dominio | `'ABERTA'` | Situacao atual: `ABERTA`, `EM ANDAMENTO`, `HOMOLOGADA` ou `CANCELADA`. |
| `data_inicio` | `DATE` | Nao |  |  | Data de inicio da licitacao. |
| `data_encerramento` | `DATE` | Sim | CHECK de periodo |  | Data de encerramento; permanece nula enquanto nao houver encerramento. |

Restricoes da tabela:

- `UNIQUE (id_orgao, numero, exercicio)`.
- `data_encerramento IS NULL OR data_encerramento >= data_inicio`.

## `item`

Uma linha representa um item colocado em disputa em uma licitacao.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_item` | `INTEGER` | Nao | PK | Identidade | Identificador interno do item licitado. |
| `id_licitacao` | `INTEGER` | Nao | FK -> `licitacao.id_licitacao` |  | Licitacao a que o item pertence. |
| `descricao` | `TEXT` | Nao |  |  | Descricao do bem ou servico. |
| `quantidade_licitada` | `NUMERIC(14,3)` | Nao | CHECK `quantidade_licitada > 0` |  | Quantidade colocada em disputa. |
| `unidade_medida` | `VARCHAR(20)` | Nao |  |  | Unidade usada para medir a quantidade. |
| `valor_referencia` | `NUMERIC(14,2)` | Nao | CHECK `valor_referencia >= 0` |  | Valor unitario estimado pelo orgao. |

## `fornecedor`

Uma linha representa uma pessoa juridica apta a apresentar propostas e firmar contratos.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_fornecedor` | `INTEGER` | Nao | PK | Identidade | Identificador interno do fornecedor. |
| `nome_fornecedor` | `VARCHAR(200)` | Nao |  |  | Nome empresarial do fornecedor. |
| `cnpj` | `VARCHAR(14)` | Nao | UNIQUE e CHECK de formato |  | CNPJ com exatamente 14 digitos. |
| `rua` | `VARCHAR(200)` | Nao |  |  | Rua do endereco do fornecedor. |
| `cidade` | `VARCHAR(100)` | Nao |  |  | Cidade do endereco do fornecedor. |

## `proposta`

Uma linha representa a oferta de um fornecedor para um item licitado. A combinacao de fornecedor e item identifica a proposta.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_fornecedor` | `INTEGER` | Nao | PK, FK -> `fornecedor.id_fornecedor` |  | Fornecedor que apresentou a proposta. |
| `id_item` | `INTEGER` | Nao | PK, FK -> `item.id_item` |  | Item para o qual a proposta foi apresentada. |
| `preco_unitario` | `NUMERIC(14,2)` | Nao | CHECK `preco_unitario >= 0` |  | Preco ofertado por unidade. |
| `quantidade_ofertada` | `NUMERIC(14,3)` | Nao | CHECK `quantidade_ofertada > 0` |  | Quantidade que o fornecedor se compromete a fornecer. |
| `situacao` | `VARCHAR(30)` | Nao | CHECK de dominio | `'APRESENTADA'` | Situacao: `APRESENTADA`, `CLASSIFICADA`, `DESCLASSIFICADA` ou `VENCEDORA`. |

Restricoes da tabela:

- `PRIMARY KEY (id_fornecedor, id_item)` impede proposta duplicada do mesmo fornecedor para o mesmo item.
- Um indice unico parcial em `id_item`, quando `situacao = 'VENCEDORA'`, impede duas propostas vencedoras para o mesmo item.

## `contrato`

Uma linha representa um contrato firmado com um fornecedor como resultado de uma licitacao.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_contrato` | `INTEGER` | Nao | PK | Identidade | Identificador interno do contrato. |
| `id_licitacao` | `INTEGER` | Nao | FK -> `licitacao.id_licitacao` |  | Licitacao que originou o contrato. |
| `id_fornecedor` | `INTEGER` | Nao | FK -> `fornecedor.id_fornecedor` |  | Fornecedor contratado. |
| `numero` | `VARCHAR(30)` | Nao | UNIQUE com `id_licitacao` |  | Numero administrativo do contrato. |
| `data_inicio` | `DATE` | Nao |  |  | Inicio da vigencia contratual. |
| `data_termino` | `DATE` | Nao | CHECK `data_termino >= data_inicio` |  | Termino da vigencia contratual. |
| `situacao` | `VARCHAR(20)` | Nao | CHECK de dominio | `'ATIVO'` | Situacao: `ATIVO`, `ENCERRADO` ou `CANCELADO`. |

Restricao da tabela: `UNIQUE (id_licitacao, numero)`.

## `item_contrato`

Uma linha representa as condicoes efetivamente contratadas para um item licitado.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_item_contrato` | `INTEGER` | Nao | PK | Identidade | Identificador interno do item contratado. |
| `id_contrato` | `INTEGER` | Nao | FK -> `contrato.id_contrato` |  | Contrato que contem o item. |
| `id_item` | `INTEGER` | Nao | FK -> `item.id_item`, UNIQUE |  | Item licitado que foi contratado. |
| `quantidade_contratada` | `NUMERIC(14,3)` | Nao | CHECK `quantidade_contratada > 0` |  | Quantidade formalizada no contrato. |
| `valor_unitario_contratado` | `NUMERIC(14,2)` | Nao | CHECK `valor_unitario_contratado >= 0` |  | Valor unitario efetivamente contratado. |

O `UNIQUE (id_item)` implementa a regra adotada de que um item licitado aparece em, no maximo, um contrato.

## `pedido`

Uma linha representa uma solicitacao feita durante a vigencia de um contrato.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_pedido` | `INTEGER` | Nao | PK | Identidade | Identificador interno do pedido. |
| `id_contrato` | `INTEGER` | Nao | FK -> `contrato.id_contrato` |  | Contrato consumido pelo pedido. |
| `data_pedido` | `DATE` | Nao |  | `CURRENT_DATE` | Data em que o pedido foi realizado. |
| `solicitante` | `VARCHAR(150)` | Nao |  |  | Pessoa ou setor solicitante. |

## `item_pedido`

Uma linha representa a quantidade de um item contratado consumida por um pedido.

| Coluna | Tipo | NULL | Chave/restricao | Default | Descricao |
|---|---|---|---|---|---|
| `id_pedido` | `INTEGER` | Nao | PK, FK -> `pedido.id_pedido` |  | Pedido que contem o item. |
| `id_item_contrato` | `INTEGER` | Nao | PK, FK -> `item_contrato.id_item_contrato` |  | Item contratado que esta sendo consumido. |
| `quantidade_pedida` | `NUMERIC(14,3)` | Nao | CHECK `quantidade_pedida > 0` |  | Quantidade consumida pelo pedido. |

A chave composta `PRIMARY KEY (id_pedido, id_item_contrato)` impede a repeticao do mesmo item dentro de um pedido.

## Regras entre tabelas

As regras abaixo dependem de dados existentes em mais de uma tabela. Elas nao podem ser implementadas por um `CHECK` simples e exigirao FKs compostas, indices, trigger ou controle transacional:

1. O item do contrato deve pertencer a mesma licitacao do contrato.
2. O fornecedor do contrato deve possuir a proposta vencedora para cada item contratado.
3. Um contrato somente pode ser criado para uma licitacao homologada.
4. O item do pedido deve pertencer ao mesmo contrato informado no pedido.
5. A data do pedido deve estar dentro da vigencia do contrato, e o contrato deve estar ativo.
6. A soma das quantidades pedidas nao pode ultrapassar a quantidade contratada.
7. A quantidade contratada nao deve ultrapassar a quantidade licitada.
8. A quantidade ofertada nao deve ultrapassar a quantidade licitada.

O saldo nao e armazenado como coluna. Ele e calculado por:

```text
quantidade_contratada - soma(quantidade_pedida)
```
