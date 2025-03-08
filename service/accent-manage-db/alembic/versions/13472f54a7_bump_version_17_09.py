"""bump_version_17_09

Revision ID: 13472f54a7
Revises: b57ed1e30535

"""

# revision identifiers, used by Alembic.
revision = '13472f54a7'
down_revision = 'b57ed1e30535'

import sqlalchemy as sa

from alembic import op


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='17.09'))


def downgrade():
    pass
