from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep
from app.exceptions import LicitacaoNotFoundError, OrgaoNotFoundError
from app.models import Licitacao
from app.schemas import LicitacaoCreate, LicitacaoResponse
from app.services import LicitacaoService

router = APIRouter(
    prefix="/licitacoes",
    tags=["licitacoes"],
)


@router.post(
    "",
    response_model=LicitacaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_licitacao(
    data: LicitacaoCreate,
    session: SessionDep,
) -> Licitacao:
    service = LicitacaoService(session)

    try:
        return service.create(data)
    except OrgaoNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.get(
    "",
    response_model=list[LicitacaoResponse],
)
def list_licitacoes(session: SessionDep) -> list[Licitacao]:
    service = LicitacaoService(session)

    return service.list_all()


@router.get(
    "/{id_licitacao}",
    response_model=LicitacaoResponse,
)
def get_licitacao(
    id_licitacao: int,
    session: SessionDep,
) -> Licitacao:
    service = LicitacaoService(session)

    try:
        return service.get_by_id(id_licitacao)
    except LicitacaoNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
