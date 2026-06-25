from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db_helper
from app.core.security import decode_access_token
from app.exceptions.auth_exceptions import UserNotAuthenticatedException
from app.exceptions.permission_exceptions import PermissionDeniedException
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


async def get_db(session: AsyncSession = Depends(db_helper.session_getter)) -> AsyncSession:
    return session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise UserNotAuthenticatedException()
    return user


def require_permission(permission: str) -> Callable:
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        user_permissions = {
            perm.name
            for role in current_user.roles
            for perm in role.permissions
        }
        if permission not in user_permissions:
            raise PermissionDeniedException()
        return current_user

    return checker
