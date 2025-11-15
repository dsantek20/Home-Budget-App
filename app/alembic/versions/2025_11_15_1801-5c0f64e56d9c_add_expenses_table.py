"""add expenses table

Revision ID: 5c0f64e56d9c
Revises: d492542c9c18
Create Date: 2025-11-15 18:01:53.373040

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '5c0f64e56d9c'
down_revision: Union[str, None] = 'd492542c9c18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('expenses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('expense_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('category_id', sa.UUID(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expenses_id'), 'expenses', ['id'], unique=False)
    op.create_index(op.f('ix_expenses_user_id'), 'expenses', ['user_id'], unique=False)
    op.create_index(op.f('ix_expenses_category_id'), 'expenses', ['category_id'], unique=False)
    op.create_index(op.f('ix_expenses_expense_date'), 'expenses', ['expense_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_expenses_expense_date'), table_name='expenses')
    op.drop_index(op.f('ix_expenses_category_id'), table_name='expenses')
    op.drop_index(op.f('ix_expenses_user_id'), table_name='expenses')
    op.drop_index(op.f('ix_expenses_id'), table_name='expenses')
    op.drop_table('expenses')