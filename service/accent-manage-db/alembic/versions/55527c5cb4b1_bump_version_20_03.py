"""bump_version_20_03

Revision ID: 55527c5cb4b1
Revises: 4722bbe519b1

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '55527c5cb4b1'
down_revision = '4722bbe519b1'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.03'))


def downgrade():
    pass
