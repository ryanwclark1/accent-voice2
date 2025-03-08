"""bump_version_21_09

Revision ID: 978e620de034
Revises: 84d91026c293

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '978e620de034'
down_revision = '84d91026c293'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='21.09'))


def downgrade():
    pass
