"""bump_version_21_07

Revision ID: 2b5d68fa7ab8
Revises: 060e2360612f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2b5d68fa7ab8'
down_revision = '060e2360612f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.07'))


def downgrade():
    pass
