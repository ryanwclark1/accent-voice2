"""bump_version_22_08

Revision ID: ae5bee40e9d2
Revises: 0c758daee631

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'ae5bee40e9d2'
down_revision = '0c758daee631'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.08'))


def downgrade():
    pass
