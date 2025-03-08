"""bump_version_18_03

Revision ID: 41a523e18fdd
Revises: 36516503ae1b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '41a523e18fdd'
down_revision = '36516503ae1b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.03'))


def downgrade():
    pass
