"""bump_version_18_07

Revision ID: 34748356e196
Revises: b5c40615bc21

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '34748356e196'
down_revision = 'b5c40615bc21'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.07'))


def downgrade():
    pass
