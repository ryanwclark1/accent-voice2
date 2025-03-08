"""bump_version_22_05

Revision ID: 21b72c41eb6a
Revises: 0ffacfab7041

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '21b72c41eb6a'
down_revision = '0ffacfab7041'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='22.05'))


def downgrade():
    pass
