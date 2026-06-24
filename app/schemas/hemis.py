from pydantic import BaseModel


class HemisLoginRequest(BaseModel):
    login: str
    password: str


class HemisProfileData(BaseModel):
    hemis_id: int
    student_id_number: str
    passport_pin: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    third_name: str | None = None
    full_name: str | None = None
    university: str | None = None
    email: str | None = None
    birth_date: int | None = None
    image: str | None = None
    raw_data: dict
