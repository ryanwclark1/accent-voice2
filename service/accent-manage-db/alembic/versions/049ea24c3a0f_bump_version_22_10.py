"""bump_version_22_10

Revision ID: 049ea24c3a0f
Revises: 7541da6ac48f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '049ea24c3a0f'
down_revision = '7541da6ac48f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.10'))


def downgrade():
    pass
