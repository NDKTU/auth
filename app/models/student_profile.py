from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    hemis_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    student_id_number: Mapped[str] = mapped_column(String(64), nullable=False)
    passport_pin: Mapped[str | None] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    second_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    third_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    short_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    university: Mapped[str | None] = mapped_column(String(256), nullable=True)
    email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    birth_date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    avg_gpa: Mapped[str | None] = mapped_column(String(16), nullable=True)
    password_valid: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    address: Mapped[str | None] = mapped_column(String(512), nullable=True)
    validate_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    hash: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # nested objects stored as JSON
    gender: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    specialty: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    student_status: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    education_form: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    education_type: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    payment_form: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    group: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    faculty: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    education_lang: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    level: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    semester: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    country: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    province: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    district: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    social_category: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    poverty_level: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    accommodation: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    raw_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="student_profile")
