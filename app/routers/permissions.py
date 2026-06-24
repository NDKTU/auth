from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.routers.dependencies import get_db, require_permission
from app.schemas.permission import PermissionRead
from app.services.permission_service import PermissionService


def _service(session: AsyncSession) -> PermissionService:
    return PermissionService(PermissionRepository(session), RoleRepository(session))


router = APIRouter()


@router.get("/", response_model=list[PermissionRead], dependencies=[Depends(require_permission("permissions:read"))])
async def list_permissions(session: AsyncSession = Depends(get_db)) -> list[PermissionRead]:
    return await _service(session).list_permissions()


@router.get("/{permission_id}", response_model=PermissionRead, dependencies=[Depends(require_permission("permissions:read"))])
async def get_permission(permission_id: int, session: AsyncSession = Depends(get_db)) -> PermissionRead:
    return await _service(session).get_permission(permission_id)
