"""revert_bump_version_23_14

Revision ID: 4fad8395b151
Revises: 7c04166bf667

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4fad8395b151'
down_revision = '7c04166bf667'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.13'))


def downgrade():
    pass
