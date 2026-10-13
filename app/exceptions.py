class CnpjAlreadyExistsError(Exception):
    def __init__(self, cnpj: str) -> None:
        super().__init__(
            f"Fornecedor com CNPJ {cnpj} ja cadastrado",
        )


class OrgaoNotFoundError(Exception):
    def __init__(self, id_orgao: int) -> None:
        super().__init__(
            f"Orgao {id_orgao} nao encontrado",
        )


class LicitacaoNotFoundError(Exception):
    def __init__(self, id_licitacao: int) -> None:
        super().__init__(
            f"Licitacao {id_licitacao} nao encontrada",
        )
