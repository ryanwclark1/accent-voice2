"""bump_version_21_10

Revision ID: cb5666745311
Revises: 978e620de034

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'cb5666745311'
down_revision = '978e620de034'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.10'))


def downgrade():
    pass
