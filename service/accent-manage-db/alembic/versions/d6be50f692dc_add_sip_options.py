"""add sip options

Revision ID: d6be50f692dc
Revises: 5524f5f02959

"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd6be50f692dc'
down_revision = '5524f5f02959'


def upgrade():
    op.add_column('usersip', sa.Column('options',
                                       ARRAY(sa.String, dimensions=2),
                                       nullable=False, server_default='{}'))


def downgrade():
    op.drop_column('usersip', 'options')
