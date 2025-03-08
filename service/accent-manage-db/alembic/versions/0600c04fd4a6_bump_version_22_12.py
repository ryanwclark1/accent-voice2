"""bump_version_22_12

Revision ID: 0600c04fd4a6
Revises: a46c624e7f61

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0600c04fd4a6'
down_revision = 'a46c624e7f61'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.12'))


def downgrade():
    pass
