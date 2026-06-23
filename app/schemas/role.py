from pydantic import BaseModel, ConfigDict

from app.schemas.types import StrNormalized


class RoleCreate(BaseModel):
    name: StrNormalized


class RoleUpdate(BaseModel):
    name: StrNormalized | None = None


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
