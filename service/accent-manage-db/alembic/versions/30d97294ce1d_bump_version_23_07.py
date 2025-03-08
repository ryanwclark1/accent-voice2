"""bump_version_23_07

Revision ID: 30d97294ce1d
Revises: e507e100aa92

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '30d97294ce1d'
down_revision = 'e507e100aa92'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.07'))


def downgrade():
    pass
