"""bump_version_24_03

Revision ID: 5022e9450437
Revises: f64ea9c1a1d3

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5022e9450437'
down_revision = 'f64ea9c1a1d3'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.03'))


def downgrade():
    pass
