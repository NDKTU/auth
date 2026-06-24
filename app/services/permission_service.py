from math import ceil

from fastapi import HTTPException, status

from app.exceptions.permission_exceptions import (
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
)
from app.exceptions.role_exceptions import RoleNotFoundException
from app.models.permission import Permission
from app.models.role import Role
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository, role_repo: RoleRepository) -> None:
        self._permission_repo = permission_repo
        self._role_repo = role_repo

    async def list_permissions(self, page: int, size: int) -> PaginatedResponse[PermissionRead]:
        perms, total = await self._permission_repo.list_paginated(page, size)
        return PaginatedResponse(
            items=perms,
            total=total,
            page=page,
            size=size,
            total_pages=ceil(total / size) if total > 0 else 1,
        )

    async def get_permission(self, permission_id: int) -> Permission:
        permission = await self._permission_repo.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundException()
        return permission

    async def create_permission(self, data: PermissionCreate) -> Permission:
        existing = await self._permission_repo.get_by_name(data.name)
        if existing:
            raise PermissionAlreadyExistsException(data.name)
        return await self._permission_repo.create(data.name)

    async def update_permission(self, permission_id: int, data: PermissionUpdate) -> Permission:
        permission = await self.get_permission(permission_id)
        if data.name and data.name != permission.name:
            existing = await self._permission_repo.get_by_name(data.name)
            if existing:
                raise PermissionAlreadyExistsException(data.name)
        return await self._permission_repo.update(permission, **data.model_dump(exclude_none=True))

    async def delete_permission(self, permission_id: int) -> None:
        permission = await self.get_permission(permission_id)
        await self._permission_repo.delete(permission)

    async def assign_to_role(self, role_id: int, permission_ids: list[int]) -> Role:
        role = await self._role_repo.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundException()

        permissions = await self._permission_repo.get_by_ids(permission_ids)
        if len(permissions) != len(permission_ids):
            found_ids = {p.id for p in permissions}
            missing = [pid for pid in permission_ids if pid not in found_ids]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ruxsatlar topilmadi: {missing}",
            )

        return await self._role_repo.assign_permissions(role, permissions)
