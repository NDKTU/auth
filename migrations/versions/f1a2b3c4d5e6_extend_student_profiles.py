"""extend_student_profiles

Revision ID: f1a2b3c4d5e6
Revises: e5f6a7b8c9d0
Create Date: 2026-06-24 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'e5f6a7b8c9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("student_profiles", sa.Column("short_name", sa.String(256), nullable=True))
    op.add_column("student_profiles", sa.Column("phone", sa.String(32), nullable=True))
    op.add_column("student_profiles", sa.Column("avg_gpa", sa.String(16), nullable=True))
    op.add_column("student_profiles", sa.Column("password_valid", sa.Boolean(), nullable=True))
    op.add_column("student_profiles", sa.Column("address", sa.String(512), nullable=True))
    op.add_column("student_profiles", sa.Column("validate_url", sa.String(512), nullable=True))
    op.add_column("student_profiles", sa.Column("hash", sa.String(128), nullable=True))
    op.add_column("student_profiles", sa.Column("gender", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("specialty", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("student_status", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("education_form", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("education_type", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("payment_form", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("group", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("faculty", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("education_lang", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("level", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("semester", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("country", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("province", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("district", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("social_category", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("poverty_level", sa.JSON(), nullable=True))
    op.add_column("student_profiles", sa.Column("accommodation", sa.JSON(), nullable=True))


def downgrade() -> None:
    for col in [
        "short_name", "phone", "avg_gpa", "password_valid", "address",
        "validate_url", "hash", "gender", "specialty", "student_status",
        "education_form", "education_type", "payment_form", "group", "faculty",
        "education_lang", "level", "semester", "country", "province", "district",
        "social_category", "poverty_level", "accommodation",
    ]:
        op.drop_column("student_profiles", col)
