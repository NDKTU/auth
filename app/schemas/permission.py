from pydantic import BaseModel, ConfigDict

from app.schemas.types import StrNormalized


class PermissionCreate(BaseModel):
    name: StrNormalized


class PermissionUpdate(BaseModel):
    name: StrNormalized | None = None


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AssignPermissionsRequest(BaseModel):
    permission_ids: list[int]
