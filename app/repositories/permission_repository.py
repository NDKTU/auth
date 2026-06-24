from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission


class PermissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str) -> Permission:
        permission = Permission(name=name)
        self._session.add(permission)
        await self._session.commit()
        await self._session.refresh(permission)
        return permission

    async def get_by_id(self, permission_id: int) -> Permission | None:
        result = await self._session.execute(
            select(Permission).where(Permission.id == permission_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Permission | None:
        result = await self._session.execute(
            select(Permission).where(Permission.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, permission_ids: list[int]) -> list[Permission]:
        result = await self._session.execute(
            select(Permission).where(Permission.id.in_(permission_ids))
        )
        return list(result.scalars().all())

    async def list_all(self) -> list[Permission]:
        result = await self._session.execute(select(Permission))
        return list(result.scalars().all())

    async def update(self, permission: Permission, **fields) -> Permission:
        for key, value in fields.items():
            if value is not None:
                setattr(permission, key, value)
        await self._session.commit()
        await self._session.refresh(permission)
        return permission

    async def delete(self, permission: Permission) -> None:
        await self._session.delete(permission)
        await self._session.commit()
