"""add files table

Revision ID: 7b16eca33991
Revises: 3c840ce77658
Create Date: 2025-12-19 01:31:56.937245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b16eca33991'
down_revision: Union[str, Sequence[str], None] = '3c840ce77658'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. создаём таблицу files
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file', sa.String(length=200), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. ВАЖНО: корректно меняем тип date_born
    op.execute(
        "ALTER TABLE users "
        "ALTER COLUMN date_born "
        "TYPE DATE USING date_born::date"
    )


def downgrade() -> None:
    # возвращаем тип обратно
    op.execute(
        "ALTER TABLE users "
        "ALTER COLUMN date_born "
        "TYPE VARCHAR USING date_born::text"
    )

    op.drop_table('files')
