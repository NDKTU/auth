from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.role_repository import RoleRepository
from app.routers.dependencies import get_db
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreate,
    session: AsyncSession = Depends(get_db),
) -> RoleRead:
    service = RoleService(RoleRepository(session))
    return await service.create_role(data)


@router.patch("/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    session: AsyncSession = Depends(get_db),
) -> RoleRead:
    service = RoleService(RoleRepository(session))
    return await service.update_role(role_id, data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(get_db),
) -> None:
    service = RoleService(RoleRepository(session))
    await service.delete_role(role_id)
