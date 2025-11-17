"""add category type

Revision ID: 52bbc3e14a1b
Revises: 913a42475f4f
Create Date: 2025-11-17 13:01:00.602160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52bbc3e14a1b'
down_revision: Union[str, None] = '913a42475f4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('categories', sa.Column('category_type', sa.String(), nullable=False, server_default='EXPENSE'))

    op.execute("""
        INSERT INTO categories (id, name, description, is_predefined, category_type, user_id, created_at, updated_at) VALUES
        (gen_random_uuid(), 'Salary', 'Monthly salary', true, 'INCOME', NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Freelance', 'Freelance work income', true, 'INCOME', NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Investments', 'Investment returns', true, 'INCOME', NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Gifts', 'Money gifts received', true, 'INCOME', NULL, NOW(), NOW()),
        (gen_random_uuid(), 'Other Income', 'Other sources', true, 'INCOME', NULL, NOW(), NOW())
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM categories 
        WHERE category_type = 'INCOME' AND is_predefined = true
    """)
    op.drop_column('categories', 'category_type')
