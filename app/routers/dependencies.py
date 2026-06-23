from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db_helper
from app.core.security import decode_access_token
from app.exceptions.auth_exceptions import UserNotAuthenticatedException
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db(session: AsyncSession = Depends(db_helper.session_getter)) -> AsyncSession:
    return session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise UserNotAuthenticatedException()
    return user
