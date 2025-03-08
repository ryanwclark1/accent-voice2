"""bump_version_22_16

Revision ID: b0edbcc1426d
Revises: e04b80f8b6fc

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b0edbcc1426d'
down_revision = 'e04b80f8b6fc'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.16'))


def downgrade():
    pass
