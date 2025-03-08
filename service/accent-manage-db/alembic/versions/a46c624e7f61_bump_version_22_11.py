"""bump_version_22_11

Revision ID: a46c624e7f61
Revises: 049ea24c3a0f

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a46c624e7f61'
down_revision = '049ea24c3a0f'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.11'))


def downgrade():
    pass
