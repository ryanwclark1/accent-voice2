"""bump_version_23_02

Revision ID: 0269f5e35792
Revises: c8415eb8bfb5

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0269f5e35792'
down_revision = 'c8415eb8bfb5'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.02'))


def downgrade():
    pass
