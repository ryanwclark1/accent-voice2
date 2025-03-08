"""bump_version_19_01

Revision ID: e4f459f58795
Revises: 1311cd6c2a63

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e4f459f58795'
down_revision = '1311cd6c2a63'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.01'))


def downgrade():
    pass
