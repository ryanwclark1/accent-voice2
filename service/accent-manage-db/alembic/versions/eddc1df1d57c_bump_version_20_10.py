"""bump_version_20_10

Revision ID: eddc1df1d57c
Revises: 5600ad4c00b4

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'eddc1df1d57c'
down_revision = '5600ad4c00b4'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.10'))


def downgrade():
    pass
