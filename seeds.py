import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import db_helper
from app.core.security import hash_password
from app.core.startup import ALL_PERMISSIONS
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "moderator": [
        "users:me",
        "users:read",
        "users:update",
        "users:update_password",
        "roles:read",
    ],
    "user": [
        "users:me",
    ],
}


async def seed() -> None:
    async with db_helper.session_factory() as session:
        # fetch all permissions (created by app startup)
        permissions: dict[str, Permission] = {
            p.name: p
            for p in (await session.execute(select(Permission))).scalars().all()
        }

        # --- roles ---
        roles: dict[str, Role] = {}
        for name in ["moderator", "user"]:
            existing = (
                await session.execute(
                    select(Role).where(Role.name == name).options(selectinload(Role.permissions))
                )
            ).scalar_one_or_none()

            if existing is None:
                role = Role(name=name)
                session.add(role)
                await session.flush()
                roles[name] = role
                print(f"[+] role '{name}' created")
            else:
                roles[name] = existing
                print(f"[=] role '{name}' already exists")

        await session.commit()

        # --- assign permissions to roles ---
        for role_name, perm_names in ROLE_PERMISSIONS.items():
            role = roles[role_name]
            assigned = [permissions[p] for p in perm_names if p in permissions]
            role.permissions = assigned
            await session.commit()
            print(f"[+] role '{role_name}' → {len(assigned)} permissions assigned")

        # --- users ---
        users_data = [
            {"username": "moderator", "password": "moderator123", "role_names": ["moderator", "user"]},
            {"username": "john",      "password": "john123",      "role_names": ["user"]},
            {"username": "jane",      "password": "jane123",      "role_names": ["user"]},
        ]

        for data in users_data:
            existing = (
                await session.execute(
                    select(User)
                    .where(User.username == data["username"])
                    .options(selectinload(User.roles))
                )
            ).scalar_one_or_none()

            if existing is None:
                user = User(
                    username=data["username"],
                    hashed_password=hash_password(data["password"]),
                )
                user.roles = [roles[r] for r in data["role_names"]]
                session.add(user)
                print(f"[+] user '{data['username']}' created  roles={data['role_names']}")
            else:
                print(f"[=] user '{data['username']}' already exists")

        await session.commit()

    await db_helper.dispose()
    print("\nSeed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
