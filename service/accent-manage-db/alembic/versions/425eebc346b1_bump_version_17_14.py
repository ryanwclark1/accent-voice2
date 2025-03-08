"""bump_version_17_14

Revision ID: 425eebc346b1
Revises: 3e7dbde01837

"""

# revision identifiers, used by Alembic.
revision = '425eebc346b1'
down_revision = '3e7dbde01837'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.14'))


def downgrade():
    pass
