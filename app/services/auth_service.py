import secrets

from app.core.security import create_access_token, verify_password
from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.repositories.user_repository import UserRepository
from app.services.hemis_service import HemisService


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def login(self, username: str, password: str) -> str:
        user = await self._user_repo.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        return create_access_token({"sub": str(user.id)})

    async def hemis_login(self, login: str, password: str) -> str:
        profile = await HemisService().login(login, password)

        user = await self._user_repo.get_by_username(profile.student_id_number)
        if user is None:
            user = await self._user_repo.create(
                username=profile.student_id_number,
                hashed_password=secrets.token_hex(32),
            )

        await self._user_repo.upsert_student_profile(user.id, profile)

        return create_access_token({"sub": str(user.id)})
