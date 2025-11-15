"""add_user_table

Revision ID: a52393673471
Revises: 
Create Date: 2025-11-13 20:34:08.968963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a52393673471'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(length=1024), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('uq_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('uq_user_username'), 'user', ['username'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_user_id', table_name='user')
    op.drop_index('uq_user_username', table_name='user')
    op.drop_index('uq_user_email', table_name='user')
    op.drop_table('user')
