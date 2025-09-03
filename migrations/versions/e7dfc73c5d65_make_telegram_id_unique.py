"""make telegram_id unique

Revision ID: e7dfc73c5d65
Revises: 
Create Date: 2025-09-02 17:20:02.728751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7dfc73c5d65'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_users_telegram_id", "users", ["telegram_id"])



def downgrade() -> None:
     op.drop_constraint("uq_users_telegram_id", "users", type_="unique")

