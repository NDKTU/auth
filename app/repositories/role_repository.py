from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.permission import Permission
from app.models.role import Role

_WITH_PERMISSIONS = selectinload(Role.permissions)


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str) -> Role:
        role = Role(name=name)
        self._session.add(role)
        await self._session.commit()
        result = await self._session.execute(
            select(Role).where(Role.id == role.id).options(_WITH_PERMISSIONS)
        )
        return result.scalar_one()

    async def get_by_id(self, role_id: int) -> Role | None:
        result = await self._session.execute(
            select(Role).where(Role.id == role_id).options(_WITH_PERMISSIONS)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Role | None:
        result = await self._session.execute(
            select(Role).where(Role.name == name).options(_WITH_PERMISSIONS)
        )
        return result.scalar_one_or_none()

    async def update(self, role: Role, **fields) -> Role:
        for key, value in fields.items():
            if value is not None:
                setattr(role, key, value)
        await self._session.commit()
        result = await self._session.execute(
            select(Role).where(Role.id == role.id).options(_WITH_PERMISSIONS)
        )
        return result.scalar_one()

    async def list_all(self) -> list[Role]:
        result = await self._session.execute(select(Role).options(_WITH_PERMISSIONS))
        return list(result.scalars().all())

    async def get_by_ids(self, role_ids: list[int]) -> list[Role]:
        result = await self._session.execute(
            select(Role).where(Role.id.in_(role_ids)).options(_WITH_PERMISSIONS)
        )
        return list(result.scalars().all())

    async def assign_permissions(self, role: Role, permissions: list[Permission]) -> Role:
        role.permissions = permissions
        await self._session.commit()
        result = await self._session.execute(
            select(Role).where(Role.id == role.id).options(_WITH_PERMISSIONS)
        )
        return result.scalar_one()

    async def delete(self, role: Role) -> None:
        await self._session.delete(role)
        await self._session.commit()
