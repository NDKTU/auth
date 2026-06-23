from pydantic import BaseModel

from app.schemas.types import StrStripped


class LoginRequest(BaseModel):
    username: StrStripped
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
