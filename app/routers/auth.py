from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.limiter import limiter
from app.repositories.user_repository import UserRepository
from app.routers.dependencies import get_db
from app.schemas.auth import TokenResponse
from app.schemas.hemis import HemisLoginRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
@limiter.limit(lambda: f"{settings.rate_limit.login_per_minute}/minute")
async def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    service = AuthService(UserRepository(session))
    token = await service.login(form.username.strip(), form.password)
    return TokenResponse(access_token=token)


@router.post("/hemis", response_model=TokenResponse)
@limiter.limit(lambda: f"{settings.rate_limit.hemis_per_minute}/minute")
async def hemis_login(
    request: Request,
    data: HemisLoginRequest,
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    service = AuthService(UserRepository(session))
    token = await service.hemis_login(data.login, data.password)
    return TokenResponse(access_token=token)
