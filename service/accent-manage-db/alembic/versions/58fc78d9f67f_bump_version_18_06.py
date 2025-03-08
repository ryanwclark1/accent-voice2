"""bump_version_18_06

Revision ID: 58fc78d9f67f
Revises: 3a091c2f91bc

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '58fc78d9f67f'
down_revision = '3a091c2f91bc'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='18.06'))


def downgrade():
    pass
