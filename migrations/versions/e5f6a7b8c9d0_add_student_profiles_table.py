"""add_student_profiles_table

Revision ID: e5f6a7b8c9d0
Revises: d3e4f5a6b7c8
Create Date: 2026-06-24 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, None] = 'd3e4f5a6b7c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "student_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("hemis_id", sa.Integer(), nullable=False),
        sa.Column("student_id_number", sa.String(length=64), nullable=False),
        sa.Column("passport_pin", sa.String(length=32), nullable=True),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("second_name", sa.String(length=128), nullable=True),
        sa.Column("third_name", sa.String(length=128), nullable=True),
        sa.Column("full_name", sa.String(length=256), nullable=True),
        sa.Column("university", sa.String(length=256), nullable=True),
        sa.Column("email", sa.String(length=256), nullable=True),
        sa.Column("birth_date", sa.Integer(), nullable=True),
        sa.Column("image", sa.String(length=512), nullable=True),
        sa.Column("raw_data", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hemis_id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("student_profiles")
