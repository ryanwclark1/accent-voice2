"""bump_version_23_08

Revision ID: df6812f66958
Revises: 30d97294ce1d

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'df6812f66958'
down_revision = '30d97294ce1d'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.08'))


def downgrade():
    pass
