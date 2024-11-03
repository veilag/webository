"""request table

Revision ID: 7ec8fadb3539
Revises: fcf1099c39f0
Create Date: 2024-11-03 16:29:22.416810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec8fadb3539'
down_revision: Union[str, None] = 'fcf1099c39f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
