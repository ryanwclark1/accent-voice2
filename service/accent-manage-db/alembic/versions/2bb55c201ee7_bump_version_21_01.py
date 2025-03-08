"""bump_version_21_01

Revision ID: 2bb55c201ee7
Revises: b1dfaf771da8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2bb55c201ee7'
down_revision = 'b1dfaf771da8'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.01'))


def downgrade():
    pass
