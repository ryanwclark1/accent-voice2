"""bump_version_24_01

Revision ID: e1c0718176ec
Revises: f407f5789bd7

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e1c0718176ec'
down_revision = 'f407f5789bd7'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.01'))


def downgrade():
    pass
