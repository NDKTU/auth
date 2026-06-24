from sqlalchemy import select

from app.core.database import db_helper
from app.models.permission import Permission

ALL_PERMISSIONS = [
    "users:me",
    "users:read",
    "users:update",
    "users:update_password",
    "users:assign_roles",
    "roles:read",
    "roles:create",
    "roles:update",
    "roles:delete",
    "roles:assign_permissions",
    "permissions:read",
]


async def ensure_permissions() -> None:
    async with db_helper.session_factory() as session:
        existing = set((await session.execute(select(Permission.name))).scalars().all())
        new_perms = [Permission(name=n) for n in ALL_PERMISSIONS if n not in existing]
        if new_perms:
            session.add_all(new_perms)
            await session.commit()
