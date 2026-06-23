from app.core.security import create_access_token, verify_password
from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def login(self, username: str, password: str) -> str:
        user = await self._user_repo.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        return create_access_token({"sub": str(user.id)})
