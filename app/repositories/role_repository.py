from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, name: str) -> Role:
        role = Role(name=name)
        self._session.add(role)
        await self._session.commit()
        await self._session.refresh(role)
        return role

    async def get_by_id(self, role_id: int) -> Role | None:
        result = await self._session.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Role | None:
        result = await self._session.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    async def update(self, role: Role, **fields) -> Role:
        for key, value in fields.items():
            if value is not None:
                setattr(role, key, value)
        await self._session.commit()
        await self._session.refresh(role)
        return role

    async def get_by_ids(self, role_ids: list[int]) -> list[Role]:
        result = await self._session.execute(select(Role).where(Role.id.in_(role_ids)))
        return list(result.scalars().all())

    async def delete(self, role: Role) -> None:
        await self._session.delete(role)
        await self._session.commit()
