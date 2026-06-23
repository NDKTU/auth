from fastapi import HTTPException, status


class RoleNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol topilmadi",
        )


class RoleAlreadyExistsException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"'{name}' nomli rol allaqachon mavjud",
        )
