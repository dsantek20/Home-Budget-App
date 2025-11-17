"""add incomes table

Revision ID: dee5f1aabb58
Revises: 52bbc3e14a1b
Create Date: 2025-11-17 13:04:20.178332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dee5f1aabb58'
down_revision: Union[str, None] = '52bbc3e14a1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('incomes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('income_date', sa.Date(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('category_id', sa.UUID(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incomes_id'), 'incomes', ['id'], unique=False)
    op.create_index(op.f('ix_incomes_user_id'), 'incomes', ['user_id'], unique=False)
    op.create_index(op.f('ix_incomes_category_id'), 'incomes', ['category_id'], unique=False)
    op.create_index(op.f('ix_incomes_income_date'), 'incomes', ['income_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_incomes_income_date'), table_name='incomes')
    op.drop_index(op.f('ix_incomes_category_id'), table_name='incomes')
    op.drop_index(op.f('ix_incomes_user_id'), table_name='incomes')
    op.drop_index(op.f('ix_incomes_id'), table_name='incomes')
    op.drop_table('incomes')
