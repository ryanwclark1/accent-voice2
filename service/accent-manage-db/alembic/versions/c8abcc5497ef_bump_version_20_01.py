"""bump_version_20_01

Revision ID: c8abcc5497ef
Revises: cc9063471025

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'c8abcc5497ef'
down_revision = 'cc9063471025'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.01'))


def downgrade():
    pass
