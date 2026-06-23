from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.exceptions.auth_exceptions import InvalidTokenException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.auth.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
    except JWTError:
        raise InvalidTokenException()
