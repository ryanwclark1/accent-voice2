"""bump_version_21_04

Revision ID: 9442da3b20b6
Revises: 1583f90b21ad

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '9442da3b20b6'
down_revision = '1583f90b21ad'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.04'))


def downgrade():
    pass
