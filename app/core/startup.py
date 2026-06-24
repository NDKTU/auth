from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import db_helper
from app.core.security import hash_password
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User

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


async def ensure_admin() -> None:
    async with db_helper.session_factory() as session:
        # ensure admin role exists
        admin_role = (
            await session.execute(select(Role).where(Role.name == "admin"))
        ).scalar_one_or_none()

        if admin_role is None:
            admin_role = Role(name="admin")
            session.add(admin_role)
            await session.commit()

        # reload role with permissions + fetch all permissions
        admin_role = (
            await session.execute(
                select(Role).where(Role.id == admin_role.id).options(selectinload(Role.permissions))
            )
        ).scalar_one()
        all_perms = list((await session.execute(select(Permission))).scalars().all())

        admin_role.permissions = all_perms
        await session.commit()

        # ensure admin user exists
        admin_user = (
            await session.execute(
                select(User)
                .where(User.username == settings.admin.username)
                .options(selectinload(User.roles))
            )
        ).scalar_one_or_none()

        if admin_user is None:
            admin_user = User(
                username=settings.admin.username,
                hashed_password=hash_password(settings.admin.password),
            )
            admin_user.roles = [admin_role]
            session.add(admin_user)
            await session.commit()
        else:
            role_ids = {r.id for r in admin_user.roles}
            if admin_role.id not in role_ids:
                admin_user.roles.append(admin_role)
                await session.commit()
