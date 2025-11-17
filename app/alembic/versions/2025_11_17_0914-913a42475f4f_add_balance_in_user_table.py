"""add balance in user table

Revision ID: 913a42475f4f
Revises: 5c0f64e56d9c
Create Date: 2025-11-17 09:14:46.282910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '913a42475f4f'
down_revision: Union[str, None] = '5c0f64e56d9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=False, server_default='1000.00'))

def downgrade() -> None:
    op.drop_column('user', 'balance')
