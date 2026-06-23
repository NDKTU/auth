from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.routers.dependencies import get_current_user, get_db
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import AssignRolesRequest, UserRead, UserUpdatePassword, UserUpdateUsername
from app.services.user_service import UserService

router = APIRouter()


def _service(session: AsyncSession) -> UserService:
    return UserService(UserRepository(session), RoleRepository(session))


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user


@router.get("/", response_model=PaginatedResponse[UserRead])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UserRead]:
    return await _service(session).list_users(page, size)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_db)) -> UserRead:
    return await _service(session).get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_username(
    user_id: int,
    data: UserUpdateUsername,
    session: AsyncSession = Depends(get_db),
) -> UserRead:
    return await _service(session).update_username(user_id, data)


@router.patch("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    user_id: int,
    data: UserUpdatePassword,
    session: AsyncSession = Depends(get_db),
) -> None:
    await _service(session).update_password(user_id, data)


@router.post("/{user_id}/roles", response_model=UserRead)
async def assign_roles(
    user_id: int,
    data: AssignRolesRequest,
    session: AsyncSession = Depends(get_db),
) -> UserRead:
    return await _service(session).assign_roles(user_id, data)
