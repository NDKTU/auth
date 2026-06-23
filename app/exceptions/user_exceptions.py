from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi",
        )


class UsernameAlreadyTakenException(HTTPException):
    def __init__(self, username: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"'{username}' foydalanuvchi nomi band",
        )


class WrongCurrentPasswordException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Joriy parol noto'g'ri",
        )
