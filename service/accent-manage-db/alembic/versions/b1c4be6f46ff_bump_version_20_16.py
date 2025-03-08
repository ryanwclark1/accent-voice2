"""bump_version_20_16

Revision ID: b1c4be6f46ff
Revises: 2796b8c839c5

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b1c4be6f46ff'
down_revision = '2796b8c839c5'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.16'))


def downgrade():
    pass
