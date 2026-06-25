from math import ceil

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import app.models.permission  # noqa: F401 — must be imported before mapper resolution
import app.models.student_profile  # noqa: F401
from app.core.config import settings
from app.models.role import Role
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.hemis import HemisProfileData

_ROLES_WITH_PERMISSIONS = selectinload(User.roles).selectinload(Role.permissions)


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
            select(User).where(User.id == user_id).options(_ROLES_WITH_PERMISSIONS)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.username == username).options(_ROLES_WITH_PERMISSIONS)
        )
        return result.scalar_one_or_none()

    async def list_paginated(self, page: int, size: int) -> tuple[list[User], int]:
        offset = (page - 1) * size
        exclude = User.username != settings.admin.username
        total = (await self._session.execute(select(func.count(User.id)).where(exclude))).scalar_one()
        users = list(
            (
                await self._session.execute(
                    select(User).where(exclude).options(_ROLES_WITH_PERMISSIONS).offset(offset).limit(size)
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
            select(User).where(User.id == user.id).options(_ROLES_WITH_PERMISSIONS)
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

    async def upsert_student_profile(self, user_id: int, profile: HemisProfileData) -> None:
        existing = (
            await self._session.execute(
                select(StudentProfile).where(StudentProfile.user_id == user_id)
            )
        ).scalar_one_or_none()

        fields = profile.model_dump(exclude={"hemis_id"})
        fields["hemis_id"] = profile.hemis_id

        if existing is None:
            sp = StudentProfile(user_id=user_id, **fields)
            self._session.add(sp)
        else:
            for key, value in fields.items():
                setattr(existing, key, value)

        await self._session.commit()

    async def assign_student_role(self, user: User) -> None:
        user = (await self._session.execute(
            select(User).where(User.id == user.id).options(selectinload(User.roles))
        )).scalar_one()

        student_role = (await self._session.execute(
            select(Role).where(Role.name == "student")
        )).scalar_one_or_none()

        if student_role is None:
            return

        if student_role.id not in {r.id for r in user.roles}:
            user.roles.append(student_role)
            await self._session.commit()

    async def get_student_profile(self, user_id: int) -> StudentProfile | None:
        result = await self._session.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()
