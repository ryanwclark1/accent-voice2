"""bump_version_19_10

Revision ID: 4fe20686380b
Revises: 9b7e32eb0a77

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4fe20686380b'
down_revision = '9b7e32eb0a77'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.10'))


def downgrade():
    pass
