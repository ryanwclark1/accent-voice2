"""bump_version_19_12

Revision ID: 0a7363700618
Revises: 5047425b0f5c

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0a7363700618'
down_revision = '5047425b0f5c'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.12'))


def downgrade():
    pass
