from pydantic import BaseModel, ConfigDict


class StudentProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    hemis_id: int
    student_id_number: str
    passport_pin: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    third_name: str | None = None
    full_name: str | None = None
    short_name: str | None = None
    university: str | None = None
    email: str | None = None
    phone: str | None = None
    birth_date: int | None = None
    image: str | None = None
    avg_gpa: str | None = None
    password_valid: bool | None = None
    address: str | None = None
    validate_url: str | None = None
    hash: str | None = None
    gender: dict | None = None
    specialty: dict | None = None
    student_status: dict | None = None
    education_form: dict | None = None
    education_type: dict | None = None
    payment_form: dict | None = None
    group: dict | None = None
    faculty: dict | None = None
    education_lang: dict | None = None
    level: dict | None = None
    semester: dict | None = None
    country: dict | None = None
    province: dict | None = None
    district: dict | None = None
    social_category: dict | None = None
    poverty_level: dict | None = None
    accommodation: dict | None = None
