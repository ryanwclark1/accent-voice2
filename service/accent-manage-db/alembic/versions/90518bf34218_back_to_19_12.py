"""back-to-19.12

Revision ID: 90518bf34218
Revises: b3bf380f5241

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '90518bf34218'
down_revision = 'b3bf380f5241'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.12'))


def downgrade():
    pass
