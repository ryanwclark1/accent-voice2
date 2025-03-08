"""bump_version_24_15

Revision ID: 75212659ab23
Revises: 42f9334e4f25

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '75212659ab23'
down_revision = '42f9334e4f25'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='24.15'))


def downgrade():
    pass
