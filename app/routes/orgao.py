from fastapi import APIRouter, status

from app.dependencies import SessionDep
from app.models import Orgao
from app.schemas import OrgaoCreate, OrgaoResponse
from app.services import OrgaoService

router = APIRouter(
    prefix="/orgaos",
    tags=["orgaos"],
)


@router.post(
    "",
    response_model=OrgaoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_orgao(
    data: OrgaoCreate,
    session: SessionDep,
) -> Orgao:
    service = OrgaoService(session)

    return service.create(data)
