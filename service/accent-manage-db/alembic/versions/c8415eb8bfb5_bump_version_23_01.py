"""bump_version_23_01

Revision ID: c8415eb8bfb5
Revises: 1108308b3fd7

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'c8415eb8bfb5'
down_revision = '1108308b3fd7'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.01'))


def downgrade():
    pass
