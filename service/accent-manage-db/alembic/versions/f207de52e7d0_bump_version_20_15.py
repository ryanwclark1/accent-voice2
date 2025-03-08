"""bump_version_20_15

Revision ID: f207de52e7d0
Revises: e5e53b7dc5d0

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'f207de52e7d0'
down_revision = 'e5e53b7dc5d0'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.15'))


def downgrade():
    pass
