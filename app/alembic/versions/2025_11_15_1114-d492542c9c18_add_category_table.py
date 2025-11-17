"""add category table

Revision ID: d492542c9c18
Revises: a52393673471
Create Date: 2025-11-15 11:14:44.479601

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd492542c9c18'
down_revision: Union[str, None] = 'a52393673471'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('categories',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('is_predefined', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)

    op.execute("""
        INSERT INTO categories (id, name, description, is_predefined, user_id, created_at, updated_at) VALUES
        (gen_random_uuid(), 'Food', 'Food shopping and dining', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Transportation', 'Car, fuel, public transport', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Housing', 'Rent, utilities, maintenance', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Healthcare', 'Medical expenses, insurance', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Entertainment', 'Movies, games, hobbies', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Shopping', 'Clothing, electronics, gifts', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Education', 'Courses, books, tuition', true, NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Bills', 'Phone, internet, subscriptions', true, NULL, NOW(), NOW())
    """)


def downgrade() -> None:
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
