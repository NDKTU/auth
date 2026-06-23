from math import ceil

from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    UsernameAlreadyTakenException,
    WrongCurrentPasswordException,
)
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.user import AssignRolesRequest, UserRead, UserUpdatePassword, UserUpdateUsername


class UserService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository) -> None:
        self._user_repo = user_repo
        self._role_repo = role_repo

    async def get_user(self, user_id: int) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        return user

    async def list_users(self, page: int, size: int) -> PaginatedResponse[UserRead]:
        users, total = await self._user_repo.list_paginated(page, size)
        return PaginatedResponse(
            items=users,
            total=total,
            page=page,
            size=size,
            total_pages=ceil(total / size) if total > 0 else 1,
        )

    async def assign_roles(self, user_id: int, data: AssignRolesRequest) -> User:
        user = await self.get_user(user_id)
        roles = await self._role_repo.get_by_ids(data.role_ids)
        if len(roles) != len(data.role_ids):
            found_ids = {r.id for r in roles}
            missing = [rid for rid in data.role_ids if rid not in found_ids]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rollar topilmadi: {missing}",
            )
        return await self._user_repo.assign_roles(user, roles)

    async def update_username(self, user_id: int, data: UserUpdateUsername) -> User:
        user = await self.get_user(user_id)
        existing = await self._user_repo.get_by_username(data.username)
        if existing and existing.id != user_id:
            raise UsernameAlreadyTakenException(data.username)
        return await self._user_repo.update_username(user, data.username)

    async def update_password(self, user_id: int, data: UserUpdatePassword) -> User:
        user = await self.get_user(user_id)
        if not verify_password(data.current_password, user.hashed_password):
            raise WrongCurrentPasswordException()
        return await self._user_repo.update_password(user, hash_password(data.new_password))
