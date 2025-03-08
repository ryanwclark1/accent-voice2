"""bump_version_17_10

Revision ID: 17653c3f37ce
Revises: fd040214cccb

"""

# revision identifiers, used by Alembic.
revision = '17653c3f37ce'
down_revision = 'fd040214cccb'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.10'))


def downgrade():
    pass
