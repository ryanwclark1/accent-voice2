"""bump_version_17_08

Revision ID: 3612e8058d92
Revises: 3e6bc9ae6158

"""

# revision identifiers, used by Alembic.
revision = '3612e8058d92'
down_revision = '3e6bc9ae6158'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.08'))


def downgrade():
    pass
