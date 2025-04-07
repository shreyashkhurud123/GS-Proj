"""Adding GR Subject

Revision ID: 01a4ff0f2322
Revises: 168b1e6b3481
Create Date: 2025-03-31 18:24:12.857300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '01a4ff0f2322'
down_revision: Union[str, None] = '168b1e6b3481'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('grs', sa.Column('subject', sa.String(length=50), nullable=False))

def downgrade() -> None:
    op.drop_column('grs', 'subject')
