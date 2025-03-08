"""bump_version_17_03

Revision ID: 34122e276b2
Revises: c3b40a0998c4

"""

# revision identifiers, used by Alembic.
revision = '34122e276b2'
down_revision = 'c3b40a0998c4'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.03'))


def downgrade():
    pass
