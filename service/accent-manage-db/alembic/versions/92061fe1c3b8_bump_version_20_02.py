"""bump_version_20_02

Revision ID: 92061fe1c3b8
Revises: 0b694daf27e0

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '92061fe1c3b8'
down_revision = '0b694daf27e0'


def upgrade():
    infos = sa.sql.table('infos', sa.sql.column('accent_version'))
    op.execute(infos.update().values(accent_version='20.02'))


def downgrade():
    pass
