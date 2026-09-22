from pydantic import BaseModel, ConfigDict, Field


class OrgaoBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome_orgao: str = Field(
        min_length=1,
        max_length=200,
    )


class OrgaoCreate(OrgaoBase):
    pass


class OrgaoResponse(OrgaoBase):
    model_config = ConfigDict(from_attributes=True)

    id_orgao: int
