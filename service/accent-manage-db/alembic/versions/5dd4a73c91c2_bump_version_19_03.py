"""bump_version_19_03

Revision ID: 5dd4a73c91c2
Revises: d81a903b6d1e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '5dd4a73c91c2'
down_revision = 'd81a903b6d1e'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.03'))


def downgrade():
    pass
