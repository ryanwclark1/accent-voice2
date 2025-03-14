"""bump_version_23_14

Revision ID: 3a893dbde0e0
Revises: 4fad8395b151

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3a893dbde0e0'
down_revision = '4fad8395b151'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='23.14'))


def downgrade():
    pass
