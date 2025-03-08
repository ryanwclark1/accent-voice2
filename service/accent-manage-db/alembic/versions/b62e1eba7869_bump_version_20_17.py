"""bump_version_20_17

Revision ID: b62e1eba7869
Revises: 2f354a1653fc

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b62e1eba7869'
down_revision = '2f354a1653fc'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.17'))


def downgrade():
    pass
