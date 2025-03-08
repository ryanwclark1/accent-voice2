"""bump_version_24_04

Revision ID: e521f996dfaf
Revises: b65364a583d8

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e521f996dfaf'
down_revision = 'b65364a583d8'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.04'))


def downgrade():
    pass
