"""bump_version_18_01

Revision ID: 40359c5c2c92
Revises: 1815dcbc813f

"""

# revision identifiers, used by Alembic.
revision = '40359c5c2c92'
down_revision = '1815dcbc813f'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.01'))


def downgrade():
    pass
