"""Create Author table

Revision ID: 2d2d31f7fdfa
Revises: 
Create Date: 2024-06-30 06:14:48.484018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d2d31f7fdfa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "author",
        sa.Column("ID", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("title", sa.String(50), nullable=True),
        sa.Column("instituition", sa.String(50), nullable=True)
    )

def downgrade() -> None:
    op.drop_table("author")
