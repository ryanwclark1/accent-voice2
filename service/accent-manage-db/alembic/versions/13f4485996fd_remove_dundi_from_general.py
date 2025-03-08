"""remove dundi from general

Revision ID: 13f4485996fd
Revises: 30d59d9b4b6e

"""

# revision identifiers, used by Alembic.
revision = '13f4485996fd'
down_revision = '30d59d9b4b6e'

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

from alembic import op


def upgrade():
    op.drop_column('general', 'dundi')


def downgrade():
    op.add_column('general', Column('dundi', Integer, nullable=False, server_default='0'))
