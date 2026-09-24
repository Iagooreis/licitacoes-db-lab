from fastapi import APIRouter, status

from app.dependencies import SessionDep
from app.models import Fornecedor
from app.schemas import FornecedorCreate, FornecedorResponse
from app.services import FornecedorService

router = APIRouter(
    prefix="/fornecedores",
    tags=["fornecedores"],
)


@router.post(
    "",
    response_model=FornecedorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_fornecedor(
    data: FornecedorCreate,
    session: SessionDep,
) -> Fornecedor:
    service = FornecedorService(session)

    return service.create(data)


@router.get(
    "",
    response_model=list[FornecedorResponse],
)
def list_fornecedores(session: SessionDep) -> list[Fornecedor]:
    service = FornecedorService(session)

    return service.list_all()
