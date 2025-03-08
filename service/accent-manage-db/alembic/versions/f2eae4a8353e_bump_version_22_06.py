"""bump_version_22_06

Revision ID: f2eae4a8353e
Revises: 2b65d248c2ad

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'f2eae4a8353e'
down_revision = '2b65d248c2ad'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.06'))


def downgrade():
    pass
