"""bump_version_19_14

Revision ID: 4d80d8106d1e
Revises: cbd383662cc0

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4d80d8106d1e'
down_revision = 'cbd383662cc0'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.14'))


def downgrade():
    pass
