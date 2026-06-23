from math import ceil

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, username: str, hashed_password: str) -> User:
        user = User(username=username, hashed_password=hashed_password)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.id == user_id).options(selectinload(User.roles))
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.username == username).options(selectinload(User.roles))
        )
        return result.scalar_one_or_none()

    async def list_paginated(self, page: int, size: int) -> tuple[list[User], int]:
        offset = (page - 1) * size
        total = (await self._session.execute(select(func.count(User.id)))).scalar_one()
        users = list(
            (
                await self._session.execute(
                    select(User).options(selectinload(User.roles)).offset(offset).limit(size)
                )
            )
            .scalars()
            .all()
        )
        return users, total

    async def assign_roles(self, user: User, roles: list[Role]) -> User:
        user.roles = roles
        await self._session.commit()
        result = await self._session.execute(
            select(User).where(User.id == user.id).options(selectinload(User.roles))
        )
        return result.scalar_one()

    async def update_username(self, user: User, username: str) -> User:
        user.username = username
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def update_password(self, user: User, hashed_password: str) -> User:
        user.hashed_password = hashed_password
        await self._session.commit()
        await self._session.refresh(user)
        return user
