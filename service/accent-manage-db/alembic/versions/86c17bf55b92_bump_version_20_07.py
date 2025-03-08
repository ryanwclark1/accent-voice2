"""bump_version_20_07

Revision ID: 86c17bf55b92
Revises: 2a24c3d1d13e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '86c17bf55b92'
down_revision = '2a24c3d1d13e'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.07'))


def downgrade():
    pass
