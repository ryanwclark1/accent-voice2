"""add dialaction categoryval index

Revision ID: 2dbf602f5e31
Revises: 75212659ab23

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2dbf602f5e31'
down_revision = '75212659ab23'


def upgrade():
    op.create_index(
        'dialaction__idx__categoryval',
        'dialaction',
       ['categoryval']
    )

def downgrade():
    op.drop_index('dialaction__idx__categoryval')
