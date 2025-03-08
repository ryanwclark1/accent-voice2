"""bump_version_17_11

Revision ID: 60eb57605f3
Revises: bc9e62985a0

"""

# revision identifiers, used by Alembic.
revision = '60eb57605f3'
down_revision = 'bc9e62985a0'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.11'))


def downgrade():
    pass
