"""bump_version_19_11

Revision ID: d0f74d74eb5f
Revises: 17ea1bc19d64

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd0f74d74eb5f'
down_revision = '17ea1bc19d64'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.11'))


def downgrade():
    pass
