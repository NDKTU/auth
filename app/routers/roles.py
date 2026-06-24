from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.routers.dependencies import get_db, require_permission
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.schemas.permission import AssignPermissionsRequest
from app.services.permission_service import PermissionService
from app.services.role_service import RoleService

router = APIRouter()


@router.get("/", response_model=list[RoleRead], dependencies=[Depends(require_permission("roles:read"))])
async def list_roles(session: AsyncSession = Depends(get_db)) -> list[RoleRead]:
    return await RoleService(RoleRepository(session)).list_roles()


@router.get("/{role_id}", response_model=RoleRead, dependencies=[Depends(require_permission("roles:read"))])
async def get_role(role_id: int, session: AsyncSession = Depends(get_db)) -> RoleRead:
    return await RoleService(RoleRepository(session)).get_role(role_id)


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("roles:create"))])
async def create_role(data: RoleCreate, session: AsyncSession = Depends(get_db)) -> RoleRead:
    return await RoleService(RoleRepository(session)).create_role(data)


@router.patch("/{role_id}", response_model=RoleRead, dependencies=[Depends(require_permission("roles:update"))])
async def update_role(role_id: int, data: RoleUpdate, session: AsyncSession = Depends(get_db)) -> RoleRead:
    return await RoleService(RoleRepository(session)).update_role(role_id, data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_permission("roles:delete"))])
async def delete_role(role_id: int, session: AsyncSession = Depends(get_db)) -> None:
    await RoleService(RoleRepository(session)).delete_role(role_id)


@router.post("/{role_id}/permissions", response_model=RoleRead, dependencies=[Depends(require_permission("roles:assign_permissions"))])
async def assign_permissions(role_id: int, data: AssignPermissionsRequest, session: AsyncSession = Depends(get_db)) -> RoleRead:
    return await PermissionService(PermissionRepository(session), RoleRepository(session)).assign_to_role(role_id, data.permission_ids)
