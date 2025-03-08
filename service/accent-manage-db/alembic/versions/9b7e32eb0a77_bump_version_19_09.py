"""bump_version_19_09

Revision ID: 9b7e32eb0a77
Revises: cac9af37c973

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '9b7e32eb0a77'
down_revision = 'cac9af37c973'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.09'))


def downgrade():
    pass
