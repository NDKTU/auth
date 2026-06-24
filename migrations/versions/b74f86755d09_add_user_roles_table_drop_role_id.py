"""add_user_roles_table_drop_role_id

Revision ID: b74f86755d09
Revises: 560fa27555ba
Create Date: 2026-06-24 09:36:43.148560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b74f86755d09'
down_revision: Union[str, Sequence[str], None] = '560fa27555ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
