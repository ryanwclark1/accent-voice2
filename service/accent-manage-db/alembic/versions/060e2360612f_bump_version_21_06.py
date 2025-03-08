"""bump_version_21_06

Revision ID: 060e2360612f
Revises: 0f4a7c48613c

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '060e2360612f'
down_revision = '0f4a7c48613c'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.06'))


def downgrade():
    pass
