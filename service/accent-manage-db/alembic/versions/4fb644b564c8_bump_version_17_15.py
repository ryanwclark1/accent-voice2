"""bump_version_17_15

Revision ID: 4fb644b564c8
Revises: 412b6135f650

"""

# revision identifiers, used by Alembic.
revision = '4fb644b564c8'
down_revision = '412b6135f650'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.15'))


def downgrade():
    pass
