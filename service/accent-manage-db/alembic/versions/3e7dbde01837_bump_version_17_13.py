"""bump_version_17_13

Revision ID: 3e7dbde01837
Revises: 508c5a0382dc

"""

# revision identifiers, used by Alembic.
revision = '3e7dbde01837'
down_revision = '508c5a0382dc'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.13'))


def downgrade():
    pass
