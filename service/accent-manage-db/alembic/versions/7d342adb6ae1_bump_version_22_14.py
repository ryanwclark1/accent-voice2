"""bump_version_22_14

Revision ID: 7d342adb6ae1
Revises: f9ea1046c8e5

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '7d342adb6ae1'
down_revision = 'f9ea1046c8e5'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.14'))


def downgrade():
    pass
