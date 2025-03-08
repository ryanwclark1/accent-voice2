"""bump_version_18_09

Revision ID: 129646f8f81f
Revises: 315f74edddb1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '129646f8f81f'
down_revision = '315f74edddb1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.09'))


def downgrade():
    pass
