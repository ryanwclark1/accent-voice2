"""bump_version_23_16

Revision ID: 2b68f2a8c0b3
Revises: 91b9efd85e0b

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2b68f2a8c0b3'
down_revision = '91b9efd85e0b'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.16'))


def downgrade():
    pass
