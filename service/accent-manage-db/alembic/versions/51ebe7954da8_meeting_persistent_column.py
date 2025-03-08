"""meeting persistent column

Revision ID: 51ebe7954da8
Revises: ce76c220eaab

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '51ebe7954da8'
down_revision = 'ce76c220eaab'


TABLE_NAME = 'meeting'
COLUMN_NAME = 'persistent'


def upgrade():
    op.add_column(TABLE_NAME, sa.Column(COLUMN_NAME, sa.Boolean, nullable=False, server_default='false'))


def downgrade():
    op.drop_column(TABLE_NAME, COLUMN_NAME)
