"""bump_version_17_17

Revision ID: 57461905b7e6
Revises: 5b427e206bdf

"""

# revision identifiers, used by Alembic.
revision = '57461905b7e6'
down_revision = '5b427e206bdf'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.17'))


def downgrade():
    pass
