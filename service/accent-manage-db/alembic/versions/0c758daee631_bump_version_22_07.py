"""bump_version_22_07

Revision ID: 0c758daee631
Revises: f2eae4a8353e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0c758daee631'
down_revision = 'f2eae4a8353e'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.07'))


def downgrade():
    pass
