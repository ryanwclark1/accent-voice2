"""bump_version_17_04

Revision ID: 37b9ac945437
Revises: 415b08ed9959

"""

# revision identifiers, used by Alembic.
revision = '37b9ac945437'
down_revision = '415b08ed9959'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.04'))


def downgrade():
    pass
