"""bump_version_19_02

Revision ID: 58cd88054523
Revises: b6a0f4cc7e49

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '58cd88054523'
down_revision = 'b6a0f4cc7e49'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='19.02'))


def downgrade():
    pass
