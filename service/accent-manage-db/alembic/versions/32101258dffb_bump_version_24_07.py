"""bump_version_24_07

Revision ID: 32101258dffb
Revises: cce0a44f44b1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '32101258dffb'
down_revision = 'cce0a44f44b1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.07'))


def downgrade():
    pass
