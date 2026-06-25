from app.core.security import create_access_token, hash_password, verify_password
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
        # Быстрый путь: локальная БД
        user = await self._user_repo.get_by_username(login)
        if user is not None and verify_password(password, user.hashed_password):
            return create_access_token({"sub": str(user.id)})

        # Медленный путь: обращение к HEMIS
        profile = await HemisService().login(login, password)
        hashed = hash_password(password)

        user = await self._user_repo.get_by_username(profile.student_id_number)
        if user is None:
            user = await self._user_repo.create(
                username=profile.student_id_number,
                hashed_password=hashed,
            )
        else:
            await self._user_repo.update_password(user, hashed)

        await self._user_repo.upsert_student_profile(user.id, profile)
        await self._user_repo.assign_student_role(user)
        return create_access_token({"sub": str(user.id)})
