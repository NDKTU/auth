from fastapi import HTTPException, status


class PermissionDeniedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amalni bajarish uchun ruxsat yo'q",
        )


class PermissionNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruxsat topilmadi",
        )


class PermissionAlreadyExistsException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"'{name}' ruxsati allaqachon mavjud",
        )
