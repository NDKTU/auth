from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, JSON, String
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
    university: Mapped[str | None] = mapped_column(String(256), nullable=True)
    email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    birth_date: Mapped[int | None] = mapped_column(nullable=True)
    image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="student_profile")
