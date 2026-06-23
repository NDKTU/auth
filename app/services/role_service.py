from app.exceptions.role_exceptions import RoleAlreadyExistsException, RoleNotFoundException
from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, role_repo: RoleRepository) -> None:
        self._role_repo = role_repo

    async def create_role(self, data: RoleCreate) -> Role:
        existing = await self._role_repo.get_by_name(data.name)
        if existing:
            raise RoleAlreadyExistsException(data.name)
        return await self._role_repo.create(data.name)

    async def update_role(self, role_id: int, data: RoleUpdate) -> Role:
        role = await self._role_repo.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundException()
        if data.name and data.name != role.name:
            existing = await self._role_repo.get_by_name(data.name)
            if existing:
                raise RoleAlreadyExistsException(data.name)
        return await self._role_repo.update(role, **data.model_dump(exclude_none=True))

    async def delete_role(self, role_id: int) -> None:
        role = await self._role_repo.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundException()
        await self._role_repo.delete(role)
