"""bump_version_20_09

Revision ID: d90ff200ae53
Revises: 06149af25f0d

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd90ff200ae53'
down_revision = '06149af25f0d'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.09'))


def downgrade():
    pass
