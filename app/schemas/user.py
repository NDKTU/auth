from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.role import RoleRead
from app.schemas.types import StrStripped


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    roles: list[RoleRead]
    created_at: datetime


class UserUpdateUsername(BaseModel):
    username: StrStripped


class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str


class AssignRolesRequest(BaseModel):
    role_ids: list[int]
