"""bump_version_22_13

Revision ID: e53b8ab083c0
Revises: 0600c04fd4a6

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e53b8ab083c0'
down_revision = '0600c04fd4a6'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.13'))


def downgrade():
    pass
