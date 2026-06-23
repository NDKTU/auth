from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Noto'g'ri yoki muddati o'tgan token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserNotAuthenticatedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi autentifikatsiyadan o'tmagan",
            headers={"WWW-Authenticate": "Bearer"},
        )
