"""bump_version_17_12

Revision ID: 508c5a0382dc
Revises: 60eb57605f3

"""

# revision identifiers, used by Alembic.
revision = '508c5a0382dc'
down_revision = '60eb57605f3'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.12'))


def downgrade():
    pass
