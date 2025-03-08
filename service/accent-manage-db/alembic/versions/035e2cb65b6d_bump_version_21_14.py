"""bump_version_21_14

Revision ID: 035e2cb65b6d
Revises: 37c0864e0b2b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '035e2cb65b6d'
down_revision = '37c0864e0b2b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.14'))


def downgrade():
    pass
