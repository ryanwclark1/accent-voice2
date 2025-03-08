"""bump_version_19_16

Revision ID: 449045080bf6
Revises: 8691b32cf44e

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '449045080bf6'
down_revision = '8691b32cf44e'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.16'))


def downgrade():
    pass
